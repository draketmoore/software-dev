#
# hallwayTests.py
# authors: Michael Curley & Drake Moore
#

from hallway import Hallway
from point import Point
from unittest import TestCase

class HallwayTests(TestCase):
    """ tests for the Hallway object """

    def testHallwayHasOnlyOneEnd_ValueError(self):
        with self.assertRaises(ValueError):
            Hallway([Point(0, 0)])


    def testHallwayHasDiagonal_ValueError(self):
        with self.assertRaises(ValueError):
            Hallway([Point(0, 0), Point(1, 1)])


    def testHallwayHasOverlap_ValueError(self):
        with self.assertRaises(ValueError):
            Hallway([
                Point(0, 5,), Point(10, 5), Point(10, 0), Point(5, 0), Point(5, 10)
            ])


    def testHallwayWaypoints_EmptyForStraight(self):
        h = Hallway([Point(0, 0), Point(10, 0)])
        self.assertEqual(list(), h.waypointsEntryToExit)
        self.assertEqual(Point(0, 0), h.entryDoorLocation)
        self.assertEqual(Point(10, 0), h.exitDoorLocation)


    def testHallwayHasSeveralWaypoints_Success(self):
        h = Hallway([Point(0, 0), Point(0, 10), Point(2, 10), Point(2, 2),
            Point(6, 2), Point(6, 3), Point(9, 3), Point(9, 10), Point(10, 10)
        ])
        self.assertEqual([Point(0, 10), Point(2, 10), Point(2, 2),
            Point(6, 2), Point(6, 3), Point(9, 3), Point(9, 10)],
            h.waypointsEntryToExit)
        self.assertEqual(Point(0, 0), h.entryDoorLocation)
        self.assertEqual(Point(10, 10), h.exitDoorLocation)


# ----- end of file ------------------------------------------------------------





