#
# roomTests.py
# authors: Michael Curley & Drake Moore
#

from interactable import Interactable
from point import Point
from room import Room
from tile import Tile
from unittest import TestCase


class RoomTests(TestCase):
    """ tests for the Room object """

    def testRoomIsTooSmall_ValueError(self):
        with self.assertRaises(ValueError):
            Room(Point(0, 0), [
                [Tile.WALL, Tile.WALL],
                [Tile.WALL, Tile.WALL]
            ])


    def testRoomHasNoDoors_ValueError(self):
        with self.assertRaises(ValueError):
            Room(Point(0, 0), [
                [Tile.WALL, Tile.WALL, Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.WALL, Tile.WALL]
            ])


    def testRoomHasCornerDoors_ValueError(self):
        with self.assertRaises(ValueError):
            Room(Point(0, 0), [
                [Tile.DOOR, Tile.WALL, Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.WALL, Tile.WALL]
            ])
        with self.assertRaises(ValueError):
            Room(Point(0, 0), [
                [Tile.WALL, Tile.WALL, Tile.DOOR],
                [Tile.WALL, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.WALL, Tile.WALL]
            ])
        with self.assertRaises(ValueError):
            Room(Point(0, 0), [
                [Tile.WALL, Tile.WALL, Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.WALL],
                [Tile.DOOR, Tile.WALL, Tile.WALL]
            ])
        with self.assertRaises(ValueError):
            Room(Point(0, 0), [
                [Tile.WALL, Tile.WALL, Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.WALL, Tile.DOOR]
            ])


    def testRoomHasDoorsInCenterWalls_Success(self):
        r = Room(Point(0, 0), [
            [Tile.WALL, Tile.DOOR, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL, Tile.WALL]
        ])
        self.assertEqual([Point(1, 0)], r.relativeDoorLocations)
        r = Room(Point(0, 0), [
            [Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.DOOR],
            [Tile.WALL, Tile.WALL, Tile.WALL]
        ])
        self.assertEqual([Point(2, 1)], r.relativeDoorLocations)
        r = Room(Point(0, 0), [
            [Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.DOOR, Tile.WALL]
        ])
        self.assertEqual([Point(1, 2)], r.relativeDoorLocations)
        r = Room(Point(0, 0), [
            [Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL, Tile.WALL]
        ])
        self.assertEqual([Point(0, 1)], r.relativeDoorLocations)


# ----- end of file ------------------------------------------------------------





