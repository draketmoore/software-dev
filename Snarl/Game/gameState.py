#
# gameState.py
# authors: Michael Curley & Drake Moore
#

from actor import Actor
from floorPlan import FloorPlan
from point import Point
from room import Room
from tile import Tile


class GameState:
    """ represents an intermediate game state specific to no actor """

    def __init__(self, allActors: list, floorPlan: FloorPlan,
            keyLocation: Point, exitLocation: Point, keyCollected: bool,
            levelOver: bool, gameOver: bool, gameWon: bool = False,
            rooms: list = None, hallways: list = None,
            currentLevel: int = -1, totalLevels: int = -1,
            messages: list = None):
        """ the floor plan represents the current status of the game """
        self.allActors = allActors
        self.floorPlan = floorPlan
        self.keyLocation = keyLocation
        self.exitLocation = exitLocation
        self.exitUnlocked = keyCollected
        self.levelOver = levelOver
        self.gameOver = gameOver
        self.gameWon = gameWon
        self.rooms = list() if rooms is None else rooms
        self.hallways = list() if hallways is None else hallways
        self.currentLevel = currentLevel
        self.totalLevels = totalLevels
        self.messages = messages
    
   
    def showLayout(self) -> str:
        """ sets the floor plan layout based on the actors fov """
        return self.floorPlan.asciiRender()


class ActorGameState(GameState):
    """ represents an intermediate game state specific to an actor """

    def __init__(self, actor: Actor, allActors: list, floorPlan: FloorPlan,
            keyLocation: Point, exitLocation: Point, keyCollected: bool,
            levelOver: bool, gameOver: bool, gameWon: bool, ruleChecker, # RuleChecker hint circular import
            currentLevel: int = -1, totalLevels: int = -1,
            messages: list = None):
        """ the floor plan represents the current status of the game """
        GameState.__init__(self, allActors, floorPlan, keyLocation, exitLocation,
                keyCollected, levelOver, gameOver, gameWon,
                currentLevel = currentLevel, totalLevels = totalLevels,
                messages = messages)
        self.actor = actor
        self.ruleChecker = ruleChecker
        self.knownLayout = self.__setLayout()
    
    
    def getKnownLayout(self) -> list:
        """ returns a list(list(Tile/Interactable/Actor)) based on the fov """
        return self.knownLayout


    def listValidMoves(self) -> list:
        """ based on the actors current position will return a list of Points
        the actor can move to, this is based on the actors move range and their
        traversable tiles """
        moves = set([self.actor.location])
        bound = self.actor.moveRange
        locationsToCheck = [self.actor.location]
        while bound != 0:
            newLocations = list()
            for loc in locationsToCheck:
                surrounding = self.__getSurroundingTiles(loc)
                newLocations += [p for p in surrounding if p not in moves]
            moves.update(newLocations)
            locationsToCheck = newLocations
            bound -= 1
        r = list(filter(lambda p: self.ruleChecker.isMoveValid(self.actor, p,
            self.floorPlan), moves))
        r.sort()
        return r
    

    def __setLayout(self) -> list:
        """ updates the floor plan layout based on the status of the actor """
        actorLoc = self.actor.location
        moveRange = self.actor.moveRange
        viewRadius = self.actor.viewRadius
        layout = self.floorPlan.produceTileLayout()
        for row in range(self.floorPlan.height):
            for col in range(self.floorPlan.width):
                loc = Point(col, row) + self.floorPlan.upperLeftPosition
                if actorLoc.cardinalDistanceFrom(loc) > viewRadius and viewRadius > 0:
                    self.floorPlan.setTileInLayout(loc, Tile.UNKNOWN)
                if actorLoc.cardinalDistanceFrom(loc) > moveRange:
                    self.floorPlan.setTileInLayout(loc, Tile.UNKNOWN, layout)
        def takeKnownTile(tile) -> bool:
            return tile != Tile.UNKNOWN
        filteredRows = map(lambda row: list(filter(takeKnownTile, row)), layout)
        return list(filter(lambda row: len(row) != 0, filteredRows))


    def __getSurroundingTiles(self, loc: Point) -> list:
        """ returns a list of valid surrounding tiles """
        surrounding = map(lambda p: loc + p,
                [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)])
        surrounding = filter(self.floorPlan.tilePositionWithinBounds, surrounding)
        def canMove(p: Point) -> bool:
            tile = self.floorPlan.getTileInLayout(p)
            return tile in self.actor.traversableTiles or isinstance(tile, Actor)
        surrounding = filter(canMove, surrounding)
        return list(surrounding)



# ----- end of file ------------------------------------------------------------





