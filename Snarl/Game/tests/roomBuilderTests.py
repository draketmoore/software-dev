#
# roomBuilderTests.py
# authors: Michael Curley & Drake Moore
#

from point import Point
from roomBuilder import RoomBuilder
from unittest import TestCase


class RoomBuilderTests(TestCase):
    """ tests for the RoomBuilder object """

    def setUp(self):
        """ initializes an empty room builder """
        self.builder = RoomBuilder()


    def testRoomBuilderDefault_ValueError(self):
        """ tests an empty builder throws an error """
        with self.assertRaises(ValueError):
            RoomBuilder().build()

    def testRoomBuilderSimple_Success(self):
        """ tests a simple room builder works """
        self.builder.setUpperLeftPosition(Point(0, 0))
        self.builder.setSize(5, 6)
        self.builder.addDoors([Point(0, 2)])
        room = self.builder.build()

        self.assertEqual('X X X X X\n' +
                         'X       X\n' +
                         '        X\n' +
                         'X       X\n' +
                         'X       X\n' +
                         'X X X X X',
                         room.asciiRender())

    def testRoomBuilderComplex_Success(self):
        """ tests a more complex room builder works """
        self.builder.setUpperLeftPosition(Point(2, 2))
        self.builder.setSize(5, 9)
        self.builder.addDoors([Point(0, 7), Point(3, 0)])
        self.builder.addWalls([Point(1, 1), Point(2, 2), Point(3, 3)])
        room = self.builder.build()
        self.assertEqual('X X X   X\n' +
                         'X X     X\n' +
                         'X   X   X\n' +
                         'X     X X\n' +
                         'X       X\n' +
                         'X       X\n' +
                         'X       X\n' +
                         '        X\n' +
                         'X X X X X',
                         room.asciiRender())

    def testRoomBuilderNoDoor_ValueError(self):
        """ tests a room with no door throws an error """
        self.builder.setUpperLeftPosition(Point(0, 0))
        self.builder.setSize(5, 9)

        with self.assertRaises(ValueError):
            self.builder.build()

    def testRoomBuilderCornerDoor_ValueError(self):
        """ tests a room with a door in the corner throws an error """
        self.builder.setUpperLeftPosition(Point(0, 0))
        self.builder.setSize(5, 9)
        self.builder.addDoors([Point(0, 8)])

        with self.assertRaises(ValueError):
            self.builder.build()

    def testRoomBuilderCenterDoor_ValueError(self):
        """ tests a room with a door in the middle of the room throws an error """
        self.builder.setUpperLeftPosition(Point(0, 0))
        self.builder.setSize(5, 9)
        self.builder.addDoors([Point(2, 3)])

        with self.assertRaises(ValueError):
            self.builder.build()

    def testRoomBuilderOutsideDoor_ValueError(self):
        """ tests a room with a door outside the room throws an error """
        self.builder.setUpperLeftPosition(Point(0, 0))
        self.builder.setSize(5, 9)
        self.builder.addDoors([Point(0, 10)])

        with self.assertRaises(ValueError):
            self.builder.build()

    def testRoomBuilderOutsideWall_ValueError(self):
        """ tests a room with a wall outside the room throws an error """
        self.builder.setUpperLeftPosition(Point(0, 0))
        self.builder.setSize(5, 9)
        self.builder.addDoors([Point(0, 2)])
        self.builder.addWalls([Point(10, 10)])

        with self.assertRaises(ValueError):
            self.builder.build()


# ----- end of file ------------------------------------------------------------





