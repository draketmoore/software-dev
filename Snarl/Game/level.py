#
# level.py
# authors: Michael Curley & Drake Moore
#

from actor import Actor, Adversary, Player
from floorPlan import FloorPlan
from hallway import Hallway
from interactable import Interactable
from tile import Tile
from point import Point
from room import Room

class Level(FloorPlan):
    """ represents a collection of rooms connected by hallways """

    # the minimum number of rooms and hallways for a level
    MinimumHallwayCount = 1
    MinimumRoomCount = 2

    # only allow players/adversaries to be placed in empty tiles
    ActorStartPlacementTiles = [Tile.EMPTY]

    def __init__(self, rooms: list, hallways: list):
        """ initializes a level with the given list of rooms and hallways, a
        level is valid if it has at least 2 rooms and at least 1 hallway """
        self.__validateRoomsConnectedByHallways(rooms, hallways)
        self.__validateNoOverlappingLayouts(rooms, hallways)
        upperLeftPosition, layout = self.__initLevelFloorPlan(rooms, hallways)
        FloorPlan.__init__(self, upperLeftPosition, layout)
        self.rooms = rooms
        self.hallways = hallways
    

    def getPlayerAndAdversaryStartingPoints(self, invalidPoints: list) -> (list, list):
        """ gets the starting points that players and adversaries can spawn in,
        the returned lists are lists of points for players and adversaries,
        respectively """
        topLeftRoom, bottomRightRoom = self.__getTopLeftAndBottomRightRooms()
        topLeftPoints = topLeftRoom.getTraversablePointsInLayout(
                self.ActorStartPlacementTiles)
        bottomRightPoints = bottomRightRoom.getTraversablePointsInLayout(
                self.ActorStartPlacementTiles)
        return (self.__removeElementsFromList(topLeftPoints, invalidPoints),
                self.__removeElementsFromList(bottomRightPoints, invalidPoints))
        
    
    def __validateRoomsConnectedByHallways(self, rooms: list, hallways: list):
        """ raises error if any room is not connected to at least 1 hallway or
        if any hallway does not connect two rooms """
        if len(rooms) <  Level.MinimumRoomCount or len(hallways) < Level.MinimumHallwayCount:
            raise ValueError('A level must have at least {0} room(s) and {1} hallway(s).'.format(
                Level.MinimumRoomCount, Level.MinimumHallwayCount))

        unconnectedDoorLocations = self.__addNeighboringFloorPlansForConnectedRooms(
                rooms, hallways)

        # if any door is not connected to a hallway the level is invalid
        if len(unconnectedDoorLocations) > 0:
            raise ValueError('Doors at ({0}) are not connected to hallways'.format(
                ', '.join(map(str, unconnectedDoorLocations))))


    def __addNeighboringFloorPlansForConnectedRooms(self, rooms: list,
            hallways: list) -> list:
        """ adds neighboring room and hallway references to each others objects,
        retuns a list of unconnected door Points """
        doorLocationsByRoom = self.__mapDoorLocationsByRoom(rooms)

        def raiseHallError(side: str, point: Point):
            raise ValueError('Hallway {0} at {1} does not overlap with a room\'s door.'.format(
                side, str(point)))

        # make sure each hallway end point is connected to a door
        for hallway in hallways:
            entryRoom = None
            exitRoom = None
            for room in doorLocationsByRoom:
                doorLocations = doorLocationsByRoom[room]
                if hallway.entryDoorLocation in doorLocations:
                    entryRoom = room
                if hallway.exitDoorLocation in doorLocations:
                    exitRoom = room

            # each hallway must have an entry and exit room
            if entryRoom is None:
                raiseHallError('entry', hallway.entryDoorLocation)
            elif exitRoom is None:
                raiseHallError('exit', hallway.exitDoorLocation)

            # add references to all neighboring floor plans
            hallway.setEntryRoom(entryRoom)
            hallway.setExitRoom(exitRoom)
            entryRoom.addConnectedHallway(hallway)
            exitRoom.addConnectedHallway(hallway)

            # remove these door locations connected to the current hallway
            doorLocationsByRoom[entryRoom].remove(hallway.entryDoorLocation)
            doorLocationsByRoom[exitRoom].remove(hallway.exitDoorLocation)
        
        # return unconnected flatlist of unconnected door locations
        doorLocationsListOfLists = map(lambda room: doorLocationsByRoom[room], doorLocationsByRoom)
        return [doorLocation for doorLocations in doorLocationsListOfLists for doorLocation in doorLocations]


    def __mapDoorLocationsByRoom(self, rooms: list) -> dict:
        """ returns a dictionary keyed by room objects whose values are a list
        of door locations """
        doorLocationsByRoom = dict()
        for room in rooms:
            doorLocationsByRoom[room] = list(map(
                lambda relativeDoorLocation: room.upperLeftPosition + relativeDoorLocation,
                room.relativeDoorLocations))
        return doorLocationsByRoom

    
    def __validateNoOverlappingLayouts(self, rooms: list, hallways: list):
        """ raises error if any rooms or hallways overlap """
        nonEmptyTiles = list()
        # the entire room should be treated as non-empty
        for room in rooms:
            for row in range(room.height):
                for column in range(room.width):
                    nonEmptyTiles.append(room.upperLeftPosition + Point(column, row))

        # a hallway only occupies a subset of its layout
        for hallway in hallways:
            for row in range(hallway.height):
                for column in range(hallway.width):
                    if hallway.layout[row][column] == Tile.HALLWAY:
                        nonEmptyTiles.append(hallway.upperLeftPosition + Point(column, row))
            
        # sets contain no duplicates, so checks length
        nonEmptyTilesNoDuplicates = set(nonEmptyTiles)
        if len(nonEmptyTiles) != len(nonEmptyTilesNoDuplicates):
            for nonEmptyTile in nonEmptyTilesNoDuplicates:
                nonEmptyTiles.remove(nonEmptyTile)
            raise ValueError('Overlap occurs at coordinates: {0}.'.format(
                ', '.join(map(str, nonEmptyTiles))))


    def __initLevelFloorPlan(self, rooms: list, hallways: list) -> (Point, list):
        """ returns the upper left position and the layout required to construct
        a FloorPlan from the given list of Room and Hallway """
        # initialize an empty total layout of the entire level
        minPoint, maxPoint = self.__getMinAndMaxCoordinates(rooms, hallways)
        totalWidth = maxPoint.X - minPoint.X
        totalHeight = maxPoint.Y - minPoint.Y
        tileLayout = Tile.NONE.generateLayoutOfSize(totalWidth, totalHeight)

        # overwrite the empty layout with the data from each floor plan, write
        # rooms last to ensure doors are included
        for floorPlan in hallways + rooms:
            for row in range(floorPlan.height):
                for column in range(floorPlan.width):
                    nonEmptyTile = floorPlan.layout[row][column]
                    if nonEmptyTile != Tile.NONE:
                        layoutPosition = floorPlan.upperLeftPosition + Point(column, row) - minPoint
                        tileLayout[layoutPosition.Y][layoutPosition.X] = nonEmptyTile
        return minPoint, tileLayout
    

    def __getMinAndMaxCoordinates(self, rooms: list, hallways: list) -> (Point, Point):
        """ returns a tuple of the min and max coordinates of the whole level """
        floorPlans = rooms + hallways
        minX = min(map(lambda floorPlan: floorPlan.upperLeftPosition.X, floorPlans))
        minY = min(map(lambda floorPlan: floorPlan.upperLeftPosition.Y, floorPlans))
        maxX = max(map(lambda floorPlan:
            floorPlan.upperLeftPosition.X + floorPlan.width, floorPlans))
        maxY = max(map(lambda floorPlan:
            floorPlan.upperLeftPosition.Y + floorPlan.height, floorPlans))
        return Point(minX, minY), Point(maxX, maxY)


    def __getTopLeftAndBottomRightRooms(self) -> (Room, Room):
        """ returns a tuple of the top left and bottom right Room in the layout """
        distanceToTopLeftMap = {
            room.upperLeftPosition.distanceFrom(self.upperLeftPosition) : room
            for room in self.rooms
        }
        distanceToBottomRightMap = {
            room.lowerRightPosition.distanceFrom(self.lowerRightPosition) : room
            for room in self.rooms
        }
        minDistanceToTopLeft = min(distanceToTopLeftMap.keys())
        minDistanceToBottomRight = min(distanceToBottomRightMap.keys())
        return (distanceToTopLeftMap[minDistanceToTopLeft],
                distanceToBottomRightMap[minDistanceToBottomRight])
    

    def __removeElementsFromList(self, listToReturn: list, itemsToRemove: list) -> list:
        """ returns a copy of the list to return without any elements from the
        items to remove list """
        return [x for x in listToReturn if x not in itemsToRemove]



# ----- end of file ------------------------------------------------------------





