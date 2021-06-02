#
# level.py
# authors: Michael Curley & Drake Moore
#

from floorPlan import FloorPlan
from interactable import Interactable
from tile import Tile
from point import Point


class Hallway(FloorPlan):
    """ represents a hallway connecting two doors (these doors should be
    attached to rooms but the object does not assert this) """

    # a hallway must have at least 2 ends
    MinimumWaypoints = 2


    def __init__(self, waypointsEntryToExit: list):
        """ waypointsEntryToExit is a list of Point, when connected, the
        waypoints must only make right angled turns, these waypoints are
        absolute coordinates from which the upperleft position and layout are
        derived """
        self.__validateMinimumWaypointsAndTypes(waypointsEntryToExit)
        self.__validateNoDuplicateWaypoints(waypointsEntryToExit)
        self.__validateWaypointsAreRightAngled(waypointsEntryToExit)
        upperLeftPosition, layout = self.__initializeUpperLeftPositionAndLayout(
                waypointsEntryToExit)
        FloorPlan.__init__(self, upperLeftPosition, layout)

        # the waypoints are technically not a one way path, however, to ensure a
        # standard ordering they are detailed from an entry side to an exit side
        self.entryDoorLocation = waypointsEntryToExit[0]
        self.exitDoorLocation = waypointsEntryToExit[-1]
        self.waypointsEntryToExit = waypointsEntryToExit[1:-1]
        self.entryRoom = None
        self.exitRoom = None


    def tilePositionWithinBounds(self, position: Point, layout: list = None) -> bool:
        """ returns if the given position lies within this floor plan """
        return (super().tilePositionWithinBounds(position, layout) and 
                self.getTileInLayout(position, layout) == Tile.HALLWAY)


    def setEntryRoom(self, room):
        """ sets the hallways entry room """
        self.__ensureRoom(room)
        self.__ensureRoomNotSet(self.entryRoom, 'Entry')
        self.entryRoom = room
    

    def setExitRoom(self, room):
        """ sets the hallways entry room """
        self.__ensureRoom(room)
        self.__ensureRoomNotSet(self.exitRoom, 'Exit')
        self.exitRoom = room
        

    def __validateMinimumWaypointsAndTypes(self, waypointsEntryToExit: list):
        """ raises error if less than minimum are provided or any waypoints are
        not Point objects """
        if len(waypointsEntryToExit) < Hallway.MinimumWaypoints:
            raise ValueError('A Hallway must contain at least {0} waypoints.'.format(
                Hallway.MinimumWaypoints))
        if not all(isinstance(waypoint, Point) for waypoint in waypointsEntryToExit):
            raise ValueError('All Hallway waypoints must be of type Point.')


    def __validateNoDuplicateWaypoints(self, waypointsEntryToExit: list):
        """ raises error if any waypoints exist in the list twice """
        if len(waypointsEntryToExit) != len(set(waypointsEntryToExit)):
            raise ValueError('Duplicate waypoints given in hallway.')
    

    def __validateWaypointsAreRightAngled(self, waypointsEntryToExit: list):
        """ raises error if any waypoint angles are not perpendicular """
        for i in range(1, len(waypointsEntryToExit)):
            startWaypoint = waypointsEntryToExit[i - 1]
            endWaypoint = waypointsEntryToExit[i]
            if startWaypoint.X != endWaypoint.X and startWaypoint.Y != endWaypoint.Y:
                raise ValueError('Hallway waypoints do not make a right angle: {0} to {1}.'.format(
                    str(startWaypoint), str(endWaypoint)))


    def __initializeUpperLeftPositionAndLayout(self,
            waypointsEntryToExit: list) -> (Point, list):
        """ returns a tuple of the upperLeftPosition and the list(list(Tile))
        layout based on the given waypoints """
        minPoint, maxPoint = self.__getMinAndMaxWaypointCoordinates(waypointsEntryToExit)
        # if a hallway is only a straight line the dif of min and max will be 0
        # when in reality it is 1, so must add Point(1, 1)
        area = maxPoint - minPoint + Point(1, 1)
        layout = Tile.NONE.generateLayoutOfSize(area.X, area.Y)
        for i in range(1, len(waypointsEntryToExit)):
            startWaypoint = waypointsEntryToExit[i - 1]
            endWaypoint = waypointsEntryToExit[i]
            middleWaypoint = Point(startWaypoint.X, startWaypoint.Y)
            deltaX, deltaY = self.__getXYDeltaStepValues(startWaypoint, endWaypoint)
            wallShift = Point(abs(deltaY), abs(deltaX))# x, y reversed in Point to get wall locations
            while 1:
                self.__writeNonOverlappingHallAndWalls(middleWaypoint != startWaypoint,
                        minPoint, startWaypoint, middleWaypoint, endWaypoint,
                        wallShift, layout)
                nextWaypoint = middleWaypoint + Point(deltaX, deltaY)
                if middleWaypoint == endWaypoint:
                    # only write the final walls if it is not the end of the hall
                    if endWaypoint != waypointsEntryToExit[-1]:
                        self.__writeFinalWallsToLayout(minPoint, nextWaypoint,
                                wallShift, layout)
                    break
                middleWaypoint = nextWaypoint
        self.__overwriteDoorsInLayoutToNone(minPoint, waypointsEntryToExit, layout)
        return self.__trimNoneTilesFromLayout(minPoint, layout)


    def __getMinAndMaxWaypointCoordinates(self,
            waypointsEntryToExit: list) -> (Point, Point):
        """ returns a tuple of the minimum and maximum points of the waypoints,
        these points add an extra row/column to each side to compensate walls """
        minX = min(map(lambda waypoint: waypoint.X, waypointsEntryToExit)) - 1
        minY = min(map(lambda waypoint: waypoint.Y, waypointsEntryToExit)) - 1
        maxX = max(map(lambda waypoint: waypoint.X, waypointsEntryToExit)) + 1
        maxY = max(map(lambda waypoint: waypoint.Y, waypointsEntryToExit)) + 1
        return Point(minX, minY), Point(maxX, maxY)


    def __getXYDeltaStepValues(self, startWaypoint: Point, endWaypoint: Point) -> (int, int):
        """ returns a tuple of the stepX and stepY in order to move from the
        startWaypoint to the endWaypoint """
        # vertical connection
        if startWaypoint.X == endWaypoint.X:
            deltaX = 0
            deltaY = 1 if startWaypoint.Y < endWaypoint.Y else -1
        # horizontal connection
        else:
            deltaX = 1 if startWaypoint.X < endWaypoint.X else -1
            deltaY = 0
        return deltaX, deltaY


    def __writeNonOverlappingHallAndWalls(self, first: bool, minPoint: Point,
            startWaypoint: Point, middleWaypoint: Point, endWaypoint: Point,
            wallShift: Point, layout: list):
        """ raises value error if the points overlap, otherwise sets the
        hallways and walls accordingly in the mutated layout """
        loc = middleWaypoint - minPoint
        topOrLeftLoc = loc - wallShift
        bottomOrRightLoc = loc + wallShift
        # if its the start there is no way anything can overlap, this
        # logic only holds have the first hall tile is placed
        centerOverlap = layout[loc.Y][loc.X] == Tile.HALLWAY
        topOrLeftOverlap = layout[topOrLeftLoc.Y][topOrLeftLoc.X] == Tile.HALLWAY
        bottomOrRightOverlap = layout[bottomOrRightLoc.Y][bottomOrRightLoc.X] == Tile.HALLWAY
        if first and any([centerOverlap, topOrLeftOverlap, bottomOrRightOverlap]):
            raise ValueError('Hallway has overlapping waypoints between {0} and {1}.'.format(
                str(startWaypoint), str(endWaypoint)))
        layout[loc.Y][loc.X] = Tile.HALLWAY
        if not topOrLeftOverlap:
            layout[topOrLeftLoc.Y][topOrLeftLoc.X] = Tile.WALL
        if not bottomOrRightOverlap:
            layout[bottomOrRightLoc.Y][bottomOrRightLoc.X] = Tile.WALL
    

    def __writeFinalWallsToLayout(self, minPoint: Point, middleWaypoint: Point,
            wallShift: Point, layout: list):
        """ mutates the layout so that the corners of the hallway have walls """
        loc = middleWaypoint - minPoint
        topOrLeftLoc = loc - wallShift
        bottomOrRightLoc = loc + wallShift
        if layout[topOrLeftLoc.Y][topOrLeftLoc.X] != Tile.HALLWAY:
            layout[topOrLeftLoc.Y][topOrLeftLoc.X] = Tile.WALL
        if layout[bottomOrRightLoc.Y][bottomOrRightLoc.X] != Tile.HALLWAY:
            layout[bottomOrRightLoc.Y][bottomOrRightLoc.X] = Tile.WALL


    def __overwriteDoorsInLayoutToNone(self, minPoint: Point,
            waypointsEntryToExit: list, layout: list):
        """ mutates the given layout such that the entry and exit doors are None
        tiles rather than Hallway tiles """
        entryPoint = waypointsEntryToExit[0] - minPoint
        exitPoint = waypointsEntryToExit[-1] - minPoint
        layout[entryPoint.Y][entryPoint.X] = Tile.NONE
        layout[exitPoint.Y][exitPoint.X] = Tile.NONE


    def __trimNoneTilesFromLayout(self, minPoint: Point, layout: list) -> (Point, list):
        """ trims all full rows/columns of Tile.NONE in the layout, returns the
        minPoint and the new layout object (since the min point might change) """
        if all(tile == Tile.NONE for tile in layout[0]):
            layout = layout[1:]
            minPoint.relativeMove(0, 1)
        if all(tile == Tile.NONE for tile in layout[-1]):
            layout = layout[:-1]
        if all(row[0] == Tile.NONE for row in layout):
            for i in range(len(layout)):
                layout[i] = layout[i][1:]
            minPoint.relativeMove(1, 0)
        if all(row[-1] == Tile.NONE for row in layout):
            for i in range(len(layout)):
                layout[i] = layout[i][:-1]
        return minPoint, layout


    def __ensureRoom(self, room: any):
        """ raises value error if the room is not a Room object """
        from room import Room
        if not isinstance(room, Room):
            raise ValueError('The given object is not a Room')


    def __ensureRoomNotSet(self, room, name: str):
        """ raises value error if the given room object is not None """
        if room is not None:
            raise ValueError('{0} room has already been set.'.format(name))


# ----- end of file ------------------------------------------------------------





