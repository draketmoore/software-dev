#
# room.py
# authors: Michael Curley & Drake Moore
#

from floorPlan import FloorPlan
from tile import Tile
from point import Point


class Room(FloorPlan):
    """ represents a room in a level, a room is just a floor plan with at least
    1 door located at the extreme boundary of the room and all boundaries are
    walls, there may be other walls in the room but at least the edges must be
    walls """

    # a room must be at least 3x3, walls on each side with an empty space in the
    # middle
    MinimumLayoutSize = 3

    # the minimum number of doors in a room
    MinimumDoorCount = 1

    def __init__(self, upperLeftPosition: Point, layout: list):
        """ layout is of the same type as floor plan """
        FloorPlan.__init__(self, upperLeftPosition, layout)
        self.__validateLayoutIsLargeEnough()
        self.__validateLayoutBoundariesAreWallsOrDoors()
        relativeDoorLocations = self.__getRelativeDoorLocations()
        self.__validateMinimumDoorsPresent(relativeDoorLocations)
        self.__validateDoorsAreOnBoundaries(relativeDoorLocations)
        self.relativeDoorLocations = relativeDoorLocations
        self.connectedHallways = list()


    def addConnectedHallway(self, hallway):
        """ adds a hallway to this rooms connected hallways """
        from hallway import Hallway
        if not isinstance(hallway, Hallway):
            raise ValueError('Given object is not a hallway.')
        if len(self.connectedHallways) == len(self.relativeDoorLocations):
            raise ValueError('This room already has all its hallways connected.')
        self.connectedHallways.append(hallway)


    def __validateLayoutIsLargeEnough(self):
        """ raises an error if the room is too small """
        if self.width < Room.MinimumLayoutSize or self.height < Room.MinimumLayoutSize:
            raise ValueError('A Room must be of least size {0}x{0}'.format(
                Room.MinimumLayoutSize))


    def __validateLayoutBoundariesAreWallsOrDoors(self):
        """ raises an error if the boundaries of the room are not all walls """
        def raiseErrorFor(side: str):
            raise ValueError('Room given a layout with {0} side containing non wall or door.'.format(
                side))
        if not self.__layoutRowIsAllWallsOrDoors(0):
            raiseErrorFor('top') 
        if not self.__layoutRowIsAllWallsOrDoors(-1):
            raiseErrorFor('bottom')
        if not self.__layoutColumnIsAllWallsOrDoors(0):
            raiseErrorFor('left')
        if not self.__layoutColumnIsAllWallsOrDoors(-1):
            raiseErrorFor('right')


    def __layoutRowIsAllWallsOrDoors(self, index: int) -> bool:
        """ returns if all tiles in the row of self.layout are walls """
        return all(self.__tileIsWallOrDoor(tile) for tile in self.layout[index])


    def __layoutColumnIsAllWallsOrDoors(self, index: int) -> bool:
        """ returns if all tiles in the column of self.layout are walls """
        return all(self.__tileIsWallOrDoor(tile) for tile in
                map(lambda row: row[index], self.layout))


    def __tileIsWallOrDoor(self, tile: any) -> bool:
        """ returns if the tile is a wall or door """
        return tile in [Tile.WALL, Tile.DOOR]


    def __getRelativeDoorLocations(self) -> list:
        """ returns a list of Point locations of the doors based on the
        FloorPlan layout """
        relativeDoorLocations = list()
        for row in range(self.height):
            for column in range(self.width):
                if self.layout[row][column] == Tile.DOOR:
                    relativeDoorLocations.append(Point(column, row))
        return relativeDoorLocations


    def __validateMinimumDoorsPresent(self, relativeDoorLocations: list):
        """ raises an error if the minimum number of doors are not present """
        if len(relativeDoorLocations) < Room.MinimumDoorCount:
            raise ValueError('Room not given enough doors (< {0}).'.format(
                Room.MinimumDoorCount))


    def __validateDoorsAreOnBoundaries(self, relativeDoorLocations: list):
        """ raises an error detailing which door locations are invalid if any
        are not on the boundaries of the room or if any are in corners """
        invalidLocations = list()
        for relativeDoorLocation in relativeDoorLocations:
            # door is in corner...
            if (relativeDoorLocation == Point(0, 0) # top left
                    or relativeDoorLocation == Point(0, self.height - 1) # bottom left
                    or relativeDoorLocation == Point(self.width - 1, 0) # top right
                    or relativeDoorLocation == Point(self.width - 1, self.height - 1)): # bottom right
                invalidLocations.append(relativeDoorLocation)

            # door is on left or right side
            if relativeDoorLocation.X in [0, self.width - 1]:
                # door does not fall in bounds of the wall
                if relativeDoorLocation.Y < 0 or relativeDoorLocation.Y >= self.height:
                    invalidLocations.append(relativeDoorLocation)
            # door is on top or bottom
            elif relativeDoorLocation.Y in [0, self.height - 1]:
                if relativeDoorLocation.X < 0 or relativeDoorLocation.X >= self.width:
                    invalidLocations.append(relativeDoorLocation)
            # door is not (on top or botton) and is not (on left or right)
            else:
                invalidLocations.append(relativeDoorLocation)
        # raise the error if any doors are invalid
        if len(invalidLocations) != 0:
            raise ValueError('Room given doors not on boundaries or in corners: {0}.'.format(
                ', '.join(map(str, invalidLocations))))


# ----- end of file ------------------------------------------------------------





