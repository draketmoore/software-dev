#
# testState snarlParser.py
# authors: Michael Curley & Drake Moore
#

from actor import Player, Zombie, Ghost
from levelManagerBuilder import LevelManagerBuilder
from levelManager import LevelManager
from gameState import GameState
from hallway import Hallway
from interactable import Interactable
from json import dumps as jsonToStr, loads as strToJson
from level import Level
from point import Point
from room import Room
from sys import stdin
from tile import Tile


# ----- globals (constants) ----------------------------------------------------

TYPE_KEY = 'type'
ROOMS_KEY = 'rooms'
HALLWAYS_KEY = 'hallways'
OBJECTS_KEY = 'objects'
TRAVERSABLE_KEY = 'traversable'
REACHABLE_KEY = 'reachable'
OBJECT_KEY = 'object'
KEY_TYPE = 'key'
EXIT_TYPE = 'exit'
LEVEL_KEY = 'level'
PLAYERS_KEY = 'players'
ADVERSARIES_KEY = 'adversaries'
PLAYER_KEY = 'player'
ZOMBIE_KEY = 'zombie'
GHOST_KEY = 'ghost'
EXIT_LOCKED_KEY = 'exit-locked'
NAME_KEY = 'name'
VOID_KEY = 'void'
ROOM_KEY = 'room'
HALLWAY_KEY = 'hallway'
STATE_KEY = 'state'
POSITION_KEY = 'position'
ORIGIN_KEY = 'origin'
BOUNDS_KEY = 'bounds'
LAYOUT_KEY = 'layout'
ROWS_KEY = 'rows'
COLUMNS_KEY = 'columns'
FROM_KEY = 'from'
TO_KEY = 'to'
WAYPOINTS_KEY = 'waypoints'
TILE_ID_MAP = {
    0: Tile.WALL,
    1: Tile.EMPTY,
    2: Tile.DOOR
}
ID_TILE_MAP = {
    Tile.WALL: 0,
    Tile.NONE: 0,
    Tile.UNKNOWN: 0,
    Tile.HALLWAY: 1,
    Tile.EMPTY: 1,
    Interactable.KEY: 1,
    Interactable.EXIT: 1,
    Tile.DOOR: 2
}


# ----- main -------------------------------------------------------------------

class SnarlParser:
    def __init__(self, json = None):
        self.rooms = list()
        self.hallways = list()
        self.process(json)
        self.json = json

    def process(self, json):
        global TYPE_KEY, ROOM_KEY, HALLWAY_KEY, LEVEL_KEY, STATE_KEY
        if isinstance(json, dict):
            f = {
                ROOM_KEY: self.createRoom,
                HALLWAY_KEY: self.createHallway,
                LEVEL_KEY: self.createLevel,
                STATE_KEY: self.createLevelManager
            }.get(json.get(TYPE_KEY, None), None)
            if f is not None:
                f(json)
        elif isinstance(json, list):
            map(self.process, json)


    def createLevelManager(self, jsonState: dict) -> LevelManager:
        """ creates the custom implementation of GameState from the json state """
        global LEVEL_KEY, PLAYERS_KEY, ADVERSARIES_KEY, EXIT_LOCKED_KEY
        builder = LevelManagerBuilder()
        keyLocation, exitLocation, level = self.createLevel(jsonState[LEVEL_KEY])
        builder.addLevelComponent(level)
        builder.setKeyLocation(keyLocation)
        builder.setExitLocation(exitLocation)
        builder.setKeyCollected(not jsonState[EXIT_LOCKED_KEY])
        self.registerPlayers(builder, jsonState[PLAYERS_KEY])
        self.registerAdversaries(builder, jsonState[ADVERSARIES_KEY])
        self.levelManager = builder.build()
        return self.levelManager


    def createLevel(self, jsonLevel: dict) -> (Point, Point, Level):
        """ creates the custom implementation of Level from the json level """
        global ROOMS_KEY, HALLWAYS_KEY, OBJECTS_KEY
        jsonRooms = jsonLevel[ROOMS_KEY]
        jsonHallways = jsonLevel[HALLWAYS_KEY]
        jsonObjects = jsonLevel[OBJECTS_KEY]
        rooms = list(map(self.createRoom, jsonRooms))
        hallways = list(map(self.createHallway, jsonHallways))
        self.keyLocation, self.exitLocation = self.getKeyAndExitPositionsFromJsonObjects(jsonObjects)
        self.level = Level(rooms, hallways)
        return self.keyLocation, self.exitLocation, self.level


    def registerPlayers(self, builder: LevelManagerBuilder, jsonPlayerPositions: list):
        """ registers the players with the game builder """
        ids = 'abcdefghijklmnopqrstuvwxyz0123456789'
        for jsonActorPosition in jsonPlayerPositions:
            _, playerName, jsonPoint = self.getActorTypeNameAndPosition(jsonActorPosition)
            builder.registerPlayer(ids[0], playerName, self.createPoint(jsonPoint))
            ids = ids[1:]


    def registerAdversaries(self, builder: LevelManagerBuilder, jsonAdversaryPositions: list):
        """ registers the adversaries with the game builder """
        for jsonActorPosition in jsonAdversaryPositions:
            adversaryType, adversaryName, jsonPoint = self.getActorTypeNameAndPosition(jsonActorPosition)
            builder.registerAdversary(adversaryType, adversaryName, self.createPoint(jsonPoint))


    def getActorTypeNameAndPosition(self, jsonActorPosition: dict) -> (str, str, list):
        """ returns a tuple of the actor type, name and json point """
        global TYPE_KEY, NAME_KEY, POSITION_KEY
        actorType = jsonActorPosition[TYPE_KEY]
        name = jsonActorPosition[NAME_KEY]
        position = jsonActorPosition[POSITION_KEY]
        return actorType, name, position


    def createRoom(self, jsonRoom: dict) -> Room:
        """ creates the custom implementation of Room from the json room """
        global ORIGIN_KEY, LAYOUT_KEY, TILE_ID_MAP
        jsonOrigin = jsonRoom[ORIGIN_KEY]
        upperLeftPosition = self.createPoint(jsonOrigin)
        jsonLayout = jsonRoom[LAYOUT_KEY]
        layout = list(map(lambda row: list(map(TILE_ID_MAP.get, row)), jsonLayout))
        self.rooms.append(Room(upperLeftPosition, layout))
        return self.rooms[-1]


    def createHallway(self, jsonHallway: dict) -> Hallway:
        """ creates the custom implementation of Hallway from the json hallway """
        global FROM_KEY, TO_KEY, WAYPOINTS_KEY
        jsonFrom = jsonHallway[FROM_KEY]
        jsonTo = jsonHallway[TO_KEY]
        jsonWaypoints = jsonHallway[WAYPOINTS_KEY]
        allJsonWaypoints = [jsonFrom] + jsonWaypoints + [jsonTo]
        allWaypoints = list(map(self.createPoint, allJsonWaypoints))
        self.hallways.append(Hallway(allWaypoints))
        return self.hallways[-1]


    def getKeyAndExitPositionsFromJsonObjects(self, jsonObjects: list) -> (Point, Point):
        """ extracts the key Point and exit Point from the json objects """
        global KEY_TYPE, EXIT_TYPE
        keyPoint = self.extractPointTypeFromJsonObjects(jsonObjects, KEY_TYPE)
        exitPoint = self.extractPointTypeFromJsonObjects(jsonObjects, EXIT_TYPE)
        return keyPoint, exitPoint


    def extractPointTypeFromJsonObjects(self, jsonObjects: list, jsonType: str) -> Point:
        """ extracts a Point from the json objects of the specified type """
        global TYPE_KEY, POSITION_KEY
        jsonObjects = list(filter(lambda jsonObject: jsonObject[TYPE_KEY] == jsonType, jsonObjects))
        if len(jsonObjects) == 1:
            jsonPoint = jsonObjects[0][POSITION_KEY]
        else:
            jsonPoint = None
        return self.createPoint(jsonPoint)


    def createPoint(self, jsonPoint: list) -> Point:
        """ creates the custom implementation of Point from the json point """
        return None if jsonPoint is None else Point(jsonPoint[1], jsonPoint[0])


    # ----- json output --------------------------------------------------------

    def pointToJson(self, point: Point) -> list:
        """ creates a json position from the point """
        return None if point is None else [point.Y, point.X]


    def createActorPosition(self, actorType: str, actorName: str, 
            actorLocation: Point) -> dict:
        """ returns an actor-position object """
        global TYPE_KEY, NAME_KEY, POSITION_KEY
        return { TYPE_KEY: actorType, NAME_KEY: actorName,
            POSITION_KEY: self.pointToJson(actorLocation) }

    
    def createActorPositionLists(self, actors: list) -> (list, list):
        """ returns a tuple of player and adversary actor positions """
        global PLAYER_KEY, ZOMBIE_KEY, GHOST_KEY
        players = list()
        adversaries = list()
        for actor in actors:
            if actor.exited or actor.expelled:
                continue
            if isinstance(actor, Player):
                players.append(self.createActorPosition(PLAYER_KEY,
                    actor.name, actor.location))
            elif isinstance(actor, Zombie):
                adversaries.append(self.createActorPosition(ZOMBIE_KEY,
                    actor.name, actor.location))
            elif isinstance(actor, Ghost):
                adversaries.append(self.createActorPosition(GHOST_KEY,
                    actor.name, actor.location))
        return players, adversaries


    def hallwayToJson(self, hallway: Hallway) -> dict:
        """ creates a json hallway object """
        global TYPE_KEY, HALLWAY_KEY, FROM_KEY, TO_KEY, WAYPOINTS_KEY
        return {
            TYPE_KEY: HALLWAY_KEY,
            FROM_KEY: self.pointToJson(hallway.entryDoorLocation),
            TO_KEY: self.pointToJson(hallway.exitDoorLocation),
            WAYPOINTS_KEY: [ self.pointToJson(p) for p in hallway.waypointsEntryToExit ]
        }


    def roomToJson(self, room: Room) -> dict:
        """ creates a json room object """
        global TYPE_KEY, ROOM_KEY, ORIGIN_KEY, BOUNDS_KEY, LAYOUT_KEY, ROWS_KEY, COLUMNS_KEY
        return {
            TYPE_KEY: ROOM_KEY,
            ORIGIN_KEY: self.pointToJson(room.upperLeftPosition),
            BOUNDS_KEY: { ROWS_KEY: room.height, COLUMNS_KEY: room.width },
            LAYOUT_KEY: list(map(lambda row: list(map(ID_TILE_MAP.get, row)), room.layout))
        }


    def createLevelObject(self, obj: str, loc: Point) -> dict:
        """ creates a key or exit object type """
        global TYPE_KEY, POSITION_KEY
        return { TYPE_KEY: obj, POSITION_KEY: self.pointToJson(loc) }


    def levelToJson(self, rooms: list, hallways: list,
            keyLocation: Point, exitLocation: Point, exitUnlocked: bool) -> dict:
        """ creates a level json object """
        global TYPE_KEY, LEVEL_KEY, ROOMS_KEY, HALLWAYS_KEY, OBJECTS_KEY, KEY_TYPE, EXIT_TYPE
        objects = [ self.createLevelObject(EXIT_TYPE, exitLocation) ]
        if not exitUnlocked:
            objects.append(self.createLevelObject(KEY_TYPE, keyLocation))
        return {
            TYPE_KEY: LEVEL_KEY,
            ROOMS_KEY: [ self.roomToJson(r) for r in rooms ],
            HALLWAYS_KEY: [ self.hallwayToJson(h) for h in hallways ],
            OBJECTS_KEY: objects 
        }


    def gameStateToJson(self, state: GameState) -> dict:
        """ creats a json state from a game state """
        global TYPE_KEY, STATE_KEY, LEVEL_KEY, PLAYERS_KEY, ADVERSARIES_KEY, EXIT_LOCKED_KEY
        players, adversaries = self.createActorPositionLists(state.allActors)
        return { 
            TYPE_KEY: STATE_KEY,
            LEVEL_KEY: self.levelToJson(state.rooms, state.hallways,
                state.keyLocation, state.exitLocation, state.exitUnlocked),
            PLAYERS_KEY: players,
            ADVERSARIES_KEY: adversaries,
            EXIT_LOCKED_KEY: not state.exitUnlocked
        }

    # add more stuff as needed


# ----- end of file ------------------------------------------------------------





