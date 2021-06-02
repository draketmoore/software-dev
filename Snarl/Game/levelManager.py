#
# levelManager.py
# authors: Michael Curley & Drake Moore
#

from actor import Actor, Player, Adversary, Ghost, Zombie
from copy import copy
from floorPlan import FloorPlan
from gameState import ActorGameState, GameState
from hallway import Hallway
from interactable import Interactable
from level import Level
from moveResult import MoveResult
from tile import Tile
from point import Point
from random import randint
from room import Room
from ruleChecker import RuleChecker
from snarlDisconnectError import SnarlDisconnectError


class LevelManager:
    """ represents the main manager to produce game states """

    # a game may have a minimum of 1 and a maximum of 4 players
    MinPlayers = 1
    MaxPlayers = 4

    def __init__(self, floorPlan: FloorPlan, players: list, adversaries: list,
            playerStartingPoints: list, adversaryStartingPoints: list,
            keyLocation: Point, exitLocation: Point, keyCollected = False,
            ruleChecker: RuleChecker = None, observers: list = list(),
            currentLevel: int = -1, totalLevels: int = -1):
        """ this class manages a floor plan for a given number of players and
        adversaries, players and adversaries will be placed at a location from
        their corresponding list of Point """
        self.__validatePlayersAndAdversaries(players, adversaries)
        self.floorPlan = floorPlan
        self.__validatePositionIsEmpty(keyLocation, 'Key')
        self.__validatePositionIsEmpty(exitLocation, 'Exit')
        self.keyLocation = keyLocation
        self.exitLocation = exitLocation
        self.playerStartingPoints = playerStartingPoints
        self.adversaryStartingPoints = adversaryStartingPoints
        self.__isolateFloorPlanComponents(self.floorPlan)
        self.ruleChecker = RuleChecker() if ruleChecker is None else ruleChecker
        self.players = { actor.name : actor for actor in players }
        self.adversaries = { actor.name : actor for actor in adversaries }
        self.allActors = players + adversaries
        self.observers = { observer.name: observer for observer in observers if observers }
        self.keyCollected = True if keyLocation is None else keyCollected
        self.gameOver = False
        self.levelOver = False
        self.gameWon = False
        self.messages = list()
        self.stats = dict()
        self.currentLevel = currentLevel
        self.totalLevels = totalLevels
        self.resetActorLocations()
    

    def resetActorLocations(self):
        """ initializes the game by setting actor locations, to be safe call
        as frequently as desired """
        playerStartingPoints = copy(self.playerStartingPoints)
        adversaryStartingPoints = copy(self.adversaryStartingPoints)
        # sets players at appropriate locations
        for playerName in self.players:
            player = self.players[playerName]
            self.__resetActor(player)
            startPoint = playerStartingPoints.pop(0)
            self.__validateInitialPosition(playerName, startPoint,
                    self.keyLocation, self.exitLocation)
            player.location = startPoint
            # on the chance that players and adversaries can start in the same
            # location, make sure they are not placed on duplicate tiles
            if startPoint in adversaryStartingPoints:
                adversaryStartingPoints.remove(startPoint)

        # sets adversaries at appropriate locations
        for adversaryName in self.adversaries:
            adversary = self.adversaries[adversaryName]
            self.__resetActor(adversary)
            startPoint = adversaryStartingPoints.pop(0)
            self.__validateInitialPosition(adversaryName, startPoint,
                    self.keyLocation, self.exitLocation)
            adversary.location = startPoint

    
    def getActorGameState(self, name: str) -> ActorGameState:
        """ returns the game state layout for a player or adversary by their unique name """
        actor = self.getActorIfExists(name)
        if name in self.players.keys():
            allActors = list(map(lambda a: a.getCensoredActor(), self.allActors))
        else:
            allActors = self.allActors
        floorPlan = self.__copyCurrentFloorPlan()
        return ActorGameState(actor, allActors, floorPlan,
                self.keyLocation, self.exitLocation, self.keyCollected,
                self.levelOver, self.gameOver, self.gameWon, self.ruleChecker,
                self.currentLevel, self.totalLevels, self.messages)


    def getObserverGameState(self) -> GameState:
        """ returns a master game state with no censoring """
        return GameState(self.allActors, self.__copyCurrentFloorPlan(),
                self.keyLocation, self.exitLocation, self.keyCollected,
                self.levelOver, self.gameOver, self.gameWon,
                self.rooms, self.hallways,
                self.currentLevel, self.totalLevels, self.messages)
    

    def getActorIfExists(self, name: str) -> Actor:
        """ raises value error if the given name is not a key to the actors """
        actors = list(filter(lambda a: a.name == name, self.allActors))
        if len(actors) == 0:
            raise ValueError('{0} is not a valid actor name.'.format(name))
        return actors[0]

    
    def produceTileLayout(self) -> list:
        """ produces the tile layout for the whole game """
        tileLayout = self.floorPlan.produceTileLayout() # already a copy, can edit freely
        if self.exitLocation is not None:
            self.floorPlan.setTileInLayout(self.exitLocation, Interactable.EXIT, tileLayout)
        if not self.keyCollected and self.keyLocation is not None:
            self.floorPlan.setTileInLayout(self.keyLocation, Interactable.KEY, tileLayout)
        for actor in filter(lambda a: not a.expelled and not a.exited and not a.disconnected, self.allActors):
            if actor.location == self.exitLocation:
                actor.replacedTile = Interactable.EXIT
            elif not self.keyCollected and actor.location == self.keyLocation:
                actor.replacedTile = Interactable.KEY
            else:
                actor.replacedTile = self.floorPlan.getTileInLayout(actor.location)
            self.floorPlan.setTileInLayout(actor.location, actor, tileLayout)
        return tileLayout


    def asciiRender(self) -> str:
        """ renders the entire game in an ascii string """
        def rowToString(tileRow: list) -> str:
            return ' '.join(map(lambda tile: tile.asciiRender(), tileRow))
        return '\n'.join(map(rowToString, self.produceTileLayout()))


    def run(self, currentLevel: int = -1, totalLevels: int = -1, stats: dict = dict()):
        """ runs the overall game loop """
        self.stats = stats
        currentActorNum = 0
        self.updateLevelStart(currentLevel, totalLevels)
        while 1:
            currentActor = self.allActors[currentActorNum]
            if not currentActor.expelled and not currentActor.exited:
                # keep requesting moves from the actor until a valid one is made
                currentActorGs = self.getActorGameState(currentActor.name)
                self.messages = list()
                moveResult = MoveResult.Invalid
                while not moveResult:
                    try:
                        move = currentActor.requestMove(currentActorGs)
                        moveResult = self.moveActor(currentActor.name, move)
                        currentActor.updateMoveResult(moveResult)
                    except SnarlDisconnectError:
                        currentActor.expelled = True
                        currentActor.disconnected = True
                        self.messages = ['{0} {1} disconnected'.format(
                            currentActor.__class__.__name__, currentActor.name)]
                        break
                if self.ruleChecker.isLevelOver(list(self.players.values())):
                    break
                # update the game state of all current actors after every move
                self.updateObservers()
                self.updatePlayers()
            # update current Actor
            currentActorNum = (currentActorNum + 1) % len(self.allActors)
        self.updateLevelOver()


    def updateLevelStart(self, currentLevel: int, totalLevels: int):
        """ updates the actors with the initial game state """
        self.resetActorLocations()
        self.currentLevel = currentLevel
        self.totalLevels = totalLevels
        self.updateObservers()
        self.updatePlayers()


    def updatePlayers(self):
        """ update the game state of all current players after every move """
        # update all players every turn
        for player in [p for p in self.players.values() if not p.disconnected]:
            player.updateGameState(self.getActorGameState(player.name))


    def updateObservers(self):
        """ update the game state of all observers """
        gs = None
        for observerName in self.observers:
            self.observers[observerName].updateGameState(
                    self.getObserverGameState() if gs is None else gs)


    def updateLevelOver(self):
        """ updates the actors with the final level game state """
        if self.currentLevel > 0 and self.totalLevels > 0:
            players = list(self.players.values())
            self.gameOver = self.ruleChecker.isGameOver(players, self.currentLevel, self.totalLevels)
            if self.gameOver:
                self.gameWon = self.ruleChecker.isGameWon(players)
        else:
            self.gameOver = False
            self.gameWon = False
        self.levelOver = True
        self.updateObservers()
        self.updatePlayers()


    def moveActor(self, name: str, destination: Point) -> MoveResult:
        """ moves the specified actor and applies an interaction result  """
        actor = self.getActorIfExists(name)
        floorPlan = self.getActorGameState(name).floorPlan
        if not self.ruleChecker.isMoveValid(actor, destination, floorPlan):
            return MoveResult.Invalid
        prevLocation = actor.location
        actor.move(destination)
        tileOrActor = floorPlan.getTileInLayout(destination)
        if isinstance(actor, Player) and isinstance(tileOrActor, Adversary):
            if self.__allowAttack(actor, tileOrActor):
                return self.__attackActor(actor, tileOrActor, prevLocation)
            return self.__expelActor(actor)
        elif isinstance(actor, Adversary) and isinstance(tileOrActor, Player):
            if self.__allowAttack(actor, tileOrActor):
                return self.__attackActor(actor, tileOrActor, prevLocation)
            return self.__expelActor(tileOrActor)
        elif isinstance(actor, Player) and not self.keyCollected and destination == self.keyLocation:
            return self.__collectKey(actor)
        elif isinstance(actor, Player) and self.keyCollected and destination == self.exitLocation:
            return self.__enterExit(actor)
        elif isinstance(actor, Ghost) and tileOrActor == Tile.WALL:
            self.__teleportGhost(actor, floorPlan)
        self.messages.append(f'{actor.__class__.__name__} {actor.name} moved')
        return MoveResult.OK


    def __allowAttack(self, attacker: Actor, defender: Actor) -> bool:
        """ returns if attacking/defending is allowed between two actors """
        return attacker.hitpoints is not None and attacker.lifepoints is not None and\
                defender.hitpoints is not None and defender.lifepoints is not None


    def __attackActor(self, attacker: Actor, defender: Actor, bounceBackLocation: Point) -> MoveResult:
        """ facilitates an attack between two actors """
        defender.lifepoints -= attacker.hitpoints
        if defender.lifepoints > 0:
            attacker.location = bounceBackLocation
            self.messages.append(f'{attacker.__class__.__name__} {attacker.name} attacked ' +
                    f'{defender.__class__.__name__} {defender.name} and reduced '
                    f'their health to {defender.lifepoints}')
            return MoveResult.Attack
        return self.__expelActor(defender)


    def __expelActor(self, actor: Actor) -> MoveResult:
        """ expels an actor from the level """
        actor.expelled = True
        self.messages.append(f'{actor.__class__.__name__} {actor.name} was expelled')
        if isinstance(actor, Player):
            self.__updatePlayerStats(actor.name, MoveResult.Eject)
        return MoveResult.Eject


    def __collectKey(self, player: Player) -> MoveResult:
        """ collects the key for the associated player """
        self.keyCollected = True
        player.collectedKey = True
        self.messages.append(f'Player {player.name} found the key')
        self.__updatePlayerStats(player.name, MoveResult.Key)
        return MoveResult.Key

    
    def __enterExit(self, player: Player) -> MoveResult:
        """ exits the given player from the level """
        player.exited = True
        self.messages.append(f'Player {player.name} exited')
        self.__updatePlayerStats(player.name, MoveResult.Exit)
        return MoveResult.Exit


    def __updatePlayerStats(self, name: str, stat: MoveResult):
        """ updates the player's stats """
        playerStats = self.stats.get(name, dict())
        playerStats[stat] = playerStats.get(stat, 0) + 1
        self.stats[name] = playerStats


    def __teleportGhost(self, ghost: Ghost, floorPlan: FloorPlan):
        """ teleports the ghost to a random empty tile """
        emptyTiles = floorPlan.getTraversablePointsInLayout([Tile.EMPTY])
        ghost.move(emptyTiles[randint(0, len(emptyTiles) - 1)])


    def __resetActor(self, actor: Actor):
        """ resets the actor's information """
        actor.location = None
        actor.replacedTile = None
        actor.exited = False
        actor.expelled = False
        actor.collectedKey = False
        actor.lifepoints = actor.originalLifepoints


    def __getOtherActorsOfSameType(self, actor) -> list:
        """ gets other actors of the same type (Player or Adversary) """
        actorType = Player if isinstance(actor, Player) else Adversary
        return list(filter(lambda a:
            isinstance(a, actorType) and a.name != actor.name,
            self.allActors))
        

    def __validatePlayersAndAdversaries(self, players: list, adversaries: list):
        """ raises error if the number of players or adversaries are invalid or
        if there are any duplicate names """
        if len(players) <= 0:
            raise ValueError('Must have at least 1 player in the game.')
        if len(players) > self.MaxPlayers:
            raise ValueError('Can not have more than {0} players in the game.'.format(
                self.MaxPlayers))
        if len(adversaries) < 0:
            raise ValueError('Can not have negative adversaries.')
        allActors = players + adversaries
        if len(allActors) != len(set(map(lambda a: a.name, allActors))):
            raise ValueError('All actors in a game must have unique names.')
    

    def __validateInitialPosition(self, name: str, position: Point,
            keyLocation: Point, exitLocation: Point):
        """ raises value error if the positon is non-empty or at key or exit """
        self.__validatePositionIsEmpty(position, name)
        self.__validatePositionsAreNotEqual(position, keyLocation, 'key', name)
        self.__validatePositionsAreNotEqual(position, exitLocation, 'exit', name)
    
    
    def __validatePositionIsEmpty(self, position: Point, name: str):
        """ raises value error if the position is not an empty tile """
        if position is not None and self.floorPlan.getTileInLayout(position) != Tile.EMPTY:
            raise ValueError('{0} cannot be placed at position {1}.'.format(
                name, position))


    def __validatePositionsAreNotEqual(self, position: Point, destination: Point,
            destinationType: str, name: str):
        """ raises value error if the two positions are equal """
        if position == destination:
            raise ValueError('{0} cannot be placed at the {1} location at {2}'.format(
                name, destinationType, destination))


    def __copyCurrentFloorPlan(self) -> FloorPlan:
        """ copies the current floor plan with all actors placed """
        return FloorPlan(self.floorPlan.upperLeftPosition, self.produceTileLayout())


    def __isolateFloorPlanComponents(self, floorPlan: FloorPlan):
        """ pulls out rooms and hallways if possible from the floor plan object """
        self.rooms = list()
        self.hallways = list()
        if isinstance(floorPlan, Level):
            self.rooms = floorPlan.rooms
            self.hallways = floorPlan.hallways
        elif isinstance(floorPlan, Room):
            self.rooms = [floorPlan]
        elif isinstance(floorPlan, Hallway):
            self.hallways = [floorPlan]



# ----- end of file ------------------------------------------------------------





