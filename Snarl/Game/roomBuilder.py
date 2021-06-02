#
# roomBuilder.py
# authors: Michael Curley & Drake Moore
#

from room import Room
from tile import Tile
from point import Point


class RoomBuilder:
    """ represents a builder to create a room object """

    def __init__(self):
        self.__clearLocals()


    def setUpperLeftPosition(self, position: Point):
        """ sets the upper left position of the room """
        self.__ensureType(position, Point, 'Upper left position')
        self.upperLeftPosition = position
        return self


    def setSize(self, width: int, height: int):
        """ sets the size of the room """
        self.__ensureType(width, int, 'Width')
        self.__ensureType(height, int, 'Height')
        if min(width, height) < Room.MinimumLayoutSize:
            raise ValueError('A room must be at least of size {0}x{0}'.format(
                Room.MinimumLayoutSize))
        self.width = width
        self.height = height
        return self


    def addWalls(self, locations: list):
        """ adds walls to the room at the specified relative Point locations,
        top left is (0, 0) """
        self.__ensureLocationList(locations)
        self.walls += locations
        return self


    def addDoors(self, locations: list):
        """ adds the doors to the room at the specified relative Point
        locations, top left is (0, 0) """
        self.__ensureLocationList(locations)
        self.doors += locations
        return self


    def build(self) -> Room:
        """ builds the room object """
        layout = Tile.EMPTY.generateLayoutOfSize(self.width, self.height)
        # set boundaries to all walls
        for row in range(self.height):
            if row == 0 or row == self.height - 1:
                layout[row] = list(map(lambda t: Tile.WALL, layout[row]))
            else:
                layout[row][0] = Tile.WALL
                layout[row][-1] = Tile.WALL
        self.__setLocationsToType(layout, self.walls, lambda: Tile.WALL, 'wall')
        self.__setLocationsToType(layout, self.doors, lambda: Tile.DOOR, 'door')
        room = Room(self.upperLeftPosition, layout)
        self.__clearLocals()
        return room


    def __setLocationsToType(self, layout: list, locations: list,
            tileProducer, tileType: str):
        """ sets the locations in the layout to the produced tile type """
        for loc in locations:
            if loc.X < 0 or loc.X >= self.width or loc.Y < 0 or loc.Y >= self.height:
                raise ValueError('A {0} tile was placed outside the room at: {1}'.format(
                    tileType, str(loc)))
            layout[loc.Y][loc.X] = tileProducer()


    def __clearLocals(self):
        """ clears the local fields to their default values """
        self.upperLeftPosition = Point(0, 0)
        self.width = Room.MinimumLayoutSize
        self.height = Room.MinimumLayoutSize
        self.walls = list()
        self.doors = list()


    def __ensureLocationList(self, locations: list):
        """ raises value error if the given object is not a list of Point """
        self.__ensureType(locations, list, 'Locations')
        map(lambda p: self.__ensureType(p, Point, 'Each location'), locations)
    

    def __ensureType(self, o: object, t: type, name: str):
        """ raises a value error if the given object is of the wrong type """
        if not isinstance(o, t):
            raise ValueError('{0} must be of type {1}.'.format(name, str(t)))



# ----- end of file ------------------------------------------------------------





