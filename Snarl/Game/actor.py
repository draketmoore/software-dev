#
# actor.py
# authors: Michael Curley & Drake Moore
#

from iActor import IActor
from interactable import Interactable
from moveResult import MoveResult
from tile import Tile
from point import Point
from copy import copy
from room import Room


class Actor(IActor):
    """ represents an Actor in the game (a player or adversary) """
    
    # default list of the tiles that are able to be traversed by the actor
    DefaultTraversableTiles = [Tile.EMPTY, Tile.HALLWAY, Tile.DOOR]


    def __init__(self, identifier: str, name: str, moveRange: int = 1,
            viewRadius: int = -1, startLocation: Point = None,
            traversableTiles: list = None, controller = None,
            hitpoints: int = None, lifepoints: int = None):
        """ an actor may not have a starting location or require special
        traversable tiles, traversable tiles is a list of Tile or Interactable,
        identifier must be a 1 character string """
        self.__validateIdentifier(identifier)
        self.__validateMoveRange(moveRange)
        self.__validateTraversableTiles(traversableTiles)
        self.__validateController(controller)
        self.identifier = identifier
        self.name = name
        self.moveRange = moveRange
        self.viewRadius = viewRadius
        self.location = startLocation
        self.traversableTiles = set(self.DefaultTraversableTiles if
                traversableTiles is None else traversableTiles)
        from consoleController import ConsoleController # TODO circular dependency
        self.controller = ConsoleController() if controller is None else controller
        self.expelled = False
        self.exited = False
        self.collectedKey = False
        self.replacedTile = None
        self.disconnected = False
        self.hitpoints = hitpoints
        self.lifepoints = lifepoints
        self.originalLifepoints = lifepoints


    def move(self, destination: Point):
        """ moves the actor to the given location """
        # note: rule checking will already have been completed by this point
        self.location = destination


    def asciiRender(self) -> str:
        """ returns the actor's identifier for ascii rendering """
        return self.identifier
    

    def updateFinalStats(self, finalStats: list):
        """ updates the final stats for this actor """
        self.controller.updateFinalStats(finalStats)


    def updateGameState(self, gameState):
        """ updates the current game state for this actor """
        from gameState import GameState # TODO circular dependency
        if not isinstance(gameState, GameState):
            raise ValueError('An Actor must be given a valid GameState.')
        self.controller.updateGameState(gameState)


    def requestMove(self, gameState) -> Point:
        """ returns a point based on the given game state """
        from gameState import GameState # TODO circular dependency
        if not isinstance(gameState, GameState):
            raise ValueError('An Actor must be given a valid GameState.')
        return self.controller.requestMove(gameState)
    

    def updateMoveResult(self, moveResult: MoveResult) -> Point:
        """ updates an actor with their move result """
        return self.controller.updateMoveResult(moveResult)


    def getCensoredActor(self):
        """ returns a copy of this actor with censored game state information """
        censoredActor = copy(self)
        censoredActor.controller = None
        censoredActor.currentGameState = None
        censoredActor.location = None
        return censoredActor


    def __validateIdentifier(self, identifier: str):
        """ raises value error if the identifier is not a 1 char string """
        if not isinstance(identifier, str) or len(identifier) != 1:
            raise ValueError('An Actor identifier must be a one character string.')


    def __validateMoveRange(self, moveRange: int):
        """ raises value error if the move range is not an integer > 0 """
        if not isinstance(moveRange, int) or moveRange <= 0:
            raise ValueError('An Actor moveRange must be a positive integer.')


    def __validateTraversableTiles(self, traversableTiles: list):
        """ raises value error if the traversable tiles is not a list of
        Interactable or Tile """
        if traversableTiles is not None and (
                not isinstance(traversableTiles, list) or
                not all(isinstance(tile, Interactable) or isinstance(tile, Tile)
                    for tile in traversableTiles)):
            raise ValueError('An Actor traversableTiles must be a list of Interactable or Tile')

    
    def __validateController(self, controller):
        """ raises value error if the given controller is invalid """
        from controller import Controller
        if controller is not None and not isinstance(controller, Controller):
            raise ValueError('An Actor must be given a valid controller or None.')



# ----- stub classes until further details provided ----------------------------

class Player(Actor):
    """ represents a Player in the game """
    PlayerMoveRange = 2
    PlayerViewRadius = 2
    PlayerTraversableTiles = Actor.DefaultTraversableTiles + [
            Interactable.KEY,
            Interactable.EXIT
        ]

    def __init__(self, identifier: str, name: str,
            startLocation: Point = None, controller = None,
            hitpoints: int = None, lifepoints: int = None):
        Actor.__init__(self, identifier, name,
                moveRange = self.PlayerMoveRange,
                viewRadius = self.PlayerViewRadius,
                startLocation = startLocation,
                traversableTiles = self.PlayerTraversableTiles,
                controller = controller,
                hitpoints = hitpoints,
                lifepoints = lifepoints)




class Adversary(Actor):
    """ represents an Adversary in the game """
    AdversaryMoveRange = 1

    def __init__(self, identifier: str, name: str, startLocation: Point = None,
            traversableTiles: list = None, controller = None,
            hitpoints: int = None, lifepoints: int = None):
        Actor.__init__(self, identifier, name,
                moveRange = self.AdversaryMoveRange,
                startLocation = startLocation,
                traversableTiles = traversableTiles,
                controller = controller,
                hitpoints = hitpoints,
                lifepoints = lifepoints)


class Zombie(Adversary):
    """ represents a Zombie Adversary in the game """
    ZombieIdentifier = 'Z'
    ZombieTraversableTiles = [Tile.EMPTY, Interactable.KEY, Interactable.EXIT]

    def __init__(self, name: str, startLocation: Point = None, controller = None,
            hitpoints: int = None, lifepoints: int = None):
        Adversary.__init__(self, self.ZombieIdentifier, name,
                traversableTiles = self.ZombieTraversableTiles,
                startLocation = startLocation, controller = controller,
                hitpoints = hitpoints, lifepoints = lifepoints)


class Ghost(Adversary):
    """ represents a Ghost Adversary in the game """
    GhostIdentifier = 'G'
    GhostTraversableTiles = Actor.DefaultTraversableTiles + [Tile.WALL,
            Interactable.KEY, Interactable.EXIT]

    def __init__(self, name: str, startLocation: Point = None, controller = None,
            hitpoints: int = None, lifepoints: int = None):
        Adversary.__init__(self, self.GhostIdentifier, name,
                startLocation = startLocation,
                traversableTiles = self.GhostTraversableTiles,
                controller = controller,
                hitpoints = hitpoints, lifepoints = lifepoints)


# ----- end of file ------------------------------------------------------------





