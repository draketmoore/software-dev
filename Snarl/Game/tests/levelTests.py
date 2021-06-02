#
# levelTests.py
# authors: Michael Curley & Drake Moore
#

from hallway import Hallway
from interactable import Interactable
from level import Level
from point import Point
from room import Room
from tile import Tile
from unittest import TestCase


class LevelTests(TestCase):
    """ tests for the Level object """

    def setUp(self):
        self.topLeftKeyLayout = [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.DOOR,  Tile.WALL,  Tile.WALL]
        ]
        self.topLeftKeyPosition = Point(1, 3)
        self.topLeftRoomForKey = Room(Point(0, 0), self.topLeftKeyLayout)
        self.bottomRightExitLayout = [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL]
        ]
        self.bottomRightExitPosition = Point(12, 11)
        self.bottomRightRoomForExit = Room(Point(10, 10), self.bottomRightExitLayout)
        self.topLeftToBottomRightWaypoints = [
            Point(2, 4), Point(2, 6), Point(7, 6), Point(7, 8), Point(0, 8),
            Point(0, 12), Point(5, 12), Point(5, 11), Point(10, 11)
        ]
        self.topLeftToBottomRightHallway = Hallway(self.topLeftToBottomRightWaypoints)

        self.topRightRoom = Room(Point(20, -5), [
            [Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL, Tile.WALL]
        ])
        self.baseLevel = Level([self.topLeftRoomForKey, self.bottomRightRoomForExit],
                [self.topLeftToBottomRightHallway])
 

    def testBaseLevel_Success(self):
        self.assertEqual('  X X X X X                  \n' +
                         '  X       X                  \n' +
                         '  X       X                  \n' +
                         '  X       X                  \n' +
                         '  X X   X X                  \n' +
                         '    X   X X X X X X          \n' +
                         '    X             X          \n' +
                         'X X X X X X X X   X          \n' +
                         'X                 X          \n' +
                         'X   X X X X X X X X          \n' +
                         'X   X     X X X X X X X X X X\n' +
                         'X   X X X X                 X\n' +
                         'X             X X X X X     X\n' +
                         'X X X X X X X X       X X X X',
                self.baseLevel.asciiRender())
        self.assertEqual(15, self.baseLevel.width)
        self.assertEqual(14, self.baseLevel.height)


    def testGetPlayerAndAdversaryStartingPoints_Success(self):
        invalidPoints = [self.topLeftKeyPosition, self.bottomRightExitPosition]
        playerPoints, adversaryPoints = self.baseLevel.getPlayerAndAdversaryStartingPoints(
                invalidPoints)
        self.assertCountEqual([
            Point(1, 1), Point(2, 1), Point(3, 1),
            Point(1, 2), Point(2, 2), Point(3, 2),
                         Point(2, 3), Point(3, 3)  # not include key
        ], playerPoints)
        self.assertCountEqual([
            Point(11, 11),                # not include exit portal
            Point(11, 12), Point(12, 12)
        ], adversaryPoints)


    def testNeighboringRoomsAreSet_Success(self):
        self.assertCountEqual([self.topLeftToBottomRightHallway],
                self.topLeftRoomForKey.connectedHallways)
        self.assertCountEqual([self.topLeftToBottomRightHallway],
                self.bottomRightRoomForExit.connectedHallways)
        self.assertEqual(self.topLeftRoomForKey,
                self.topLeftToBottomRightHallway.entryRoom)
        self.assertEqual(self.bottomRightRoomForExit,
                self.topLeftToBottomRightHallway.exitRoom)
        

    def testHallwayDoesNotConnectDoors_ValueError(self):
        hallway = Hallway([Point(0, 7), Point(7, 7)]) # no overlaps with doors or rooms
        with self.assertRaises(ValueError):
            Level([self.topLeftRoomForKey, self.bottomRightRoomForExit], [hallway])


    # a little long, but wanted to group these asserts together in the same
    # method to keep the scope and maintain isolation of the data
    def testHallwayOverlapsWithOtherHallwayOrRoom_ValueError(self):
        # connect a hallway between new door and floating room
        self.topLeftKeyLayout[2][4] = Tile.DOOR
        topLeftRoomNewDoor = Room(Point(0, 0), self.topLeftKeyLayout)
        topLeftToTopRightHallway = Hallway([
            Point(4, 2), Point(10, 2), Point(10, -4), Point(20, -4)
        ])
        # base case success
        self.__clearConnectedAreas(self.baseLevel)
        level = Level(
            [topLeftRoomNewDoor, self.bottomRightRoomForExit, self.topRightRoom],
            [self.topLeftToBottomRightHallway, topLeftToTopRightHallway])
        self.assertEqual('                    X X X X X X X X X X X X X X\n' +
                         '                    X                         X\n' +
                         '                    X   X X X X X X X X X X X X\n' +
                         '                    X   X                      \n' +
                         '                    X   X                      \n' +
                         '  X X X X X         X   X                      \n' +
                         '  X       X X X X X X   X                      \n' +
                         '  X                     X                      \n' +
                         '  X       X X X X X X X X                      \n' +
                         '  X X   X X                                    \n' +
                         '    X   X X X X X X                            \n' +
                         '    X             X                            \n' +
                         'X X X X X X X X   X                            \n' +
                         'X                 X                            \n' +
                         'X   X X X X X X X X                            \n' +
                         'X   X     X X X X X X X X X X                  \n' +
                         'X   X X X X                 X                  \n' +
                         'X             X X X X X     X                  \n' +
                         'X X X X X X X X       X X X X                  ', level.asciiRender())
        topLeftToTopRightHallwayOverlapsOtherHallway = Hallway([
            Point(4, 2), Point(6, 2), Point(6, 7), Point(10, 7), Point(10, -4), Point(20, -4)
        ])
        self.__clearConnectedAreas(level)
        with self.assertRaises(ValueError): 
            Level(
                [topLeftRoomNewDoor, self.bottomRightRoomForExit, self.topRightRoom],
                [self.topLeftToBottomRightHallway, topLeftToTopRightHallwayOverlapsOtherHallway])
        topLeftToTopRightHallwayOverlapsBottomRightRoom = Hallway([
            Point(4, 2), Point(10, 2), Point(10, 10), Point(12, 10), Point(12, -4), Point(20, -4)
        ])
        self.__clearConnectedAreas(level)
        with self.assertRaises(ValueError): 
            Level(
                [topLeftRoomNewDoor, self.bottomRightRoomForExit, self.topRightRoom],
                [self.topLeftToBottomRightHallway, topLeftToTopRightHallwayOverlapsBottomRightRoom])


    def __clearConnectedAreas(self, level):
        for room in level.rooms:
            room.connectedHallways = list()
        for hallway in level.hallways:
            hallway.entryRoom = None
            hallway.exitRoom = None



# ----- end of file ------------------------------------------------------------





