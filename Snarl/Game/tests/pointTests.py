#
# pointTests.py
# authors: Michael Curley & Drake Moore
#

from point import Point
from unittest import TestCase


class PointTests(TestCase):
    """ tests for the Point object """

    def testPointFromString_None(self):
        self.assertEqual(None, Point.fromStr(''))
        self.assertEqual(None, Point.fromStr('(,)'))
        self.assertEqual(None, Point.fromStr('(1, 1'))
        self.assertEqual(None, Point.fromStr('2, 2'))


    def testPointFromString_Success(self):
        self.assertEqual(Point(0, 0), Point.fromStr('(0, 0)'))
        self.assertEqual(Point(10, 20), Point.fromStr('(10, 20)'))
        self.assertEqual(Point(-22, -19), Point.fromStr('(-22, -19)'))
        self.assertEqual(Point(1922, 10000), Point.fromStr('(1922, 10000)'))


    def testPointRequiresInts_ValueError(self):
        with self.assertRaises(ValueError):
            Point(0, 0.0)
        with self.assertRaises(ValueError):
            Point(0.0, 0)
        with self.assertRaises(ValueError):
            Point(0.0, 0.0)


    def testPointRelativeMoveRequiresInts_ValueError(self):
        p = Point(0, 0)
        with self.assertRaises(ValueError):
            p.relativeMove(1.0, 0)
        with self.assertRaises(ValueError):
            p.relativeMove(0, 1.0)
        with self.assertRaises(ValueError):
            p.relativeMove(1.0, 1.0)
    

    def testPointRelativeMove_UpdatesXY(self):
        p = Point(0, 0)
        p.relativeMove(-1, 10)
        self.assertEqual(Point(-1, 10), p)
        p.relativeMove(10, 20)
        self.assertEqual(Point(9, 30), p)

    
    def testDistanceFrom_Success(self):
        # rounding issues for floats
        self.assertAlmostEqual(1, Point(0, 0).distanceFrom(Point(0, 1)))
        self.assertAlmostEqual(1.41421356, Point(0, 0).distanceFrom(Point(1, 1)))
        self.assertAlmostEqual(1.41421356, Point(-1, -1).distanceFrom(Point(0, 0)))
        self.assertAlmostEqual(54.03702434, Point(10, -15).distanceFrom(Point(-32, 19)))


    def testPointEquality_Success(self):
        self.assertEqual(Point(0, 0), Point(0, 0))
        self.assertEqual(Point(-5, 22), Point(-5, 22))
        self.assertEqual(Point(12, -19), Point(12, -19))

    
    def testPointInEquality_Success(self):
        self.assertNotEqual(Point(0, 0), Point(0, 1))
        self.assertNotEqual(Point(-5, 22), Point(22, -5))
        self.assertNotEqual(Point(10, 10), Point(0, 0))
        self.assertNotEqual(Point(1, 2), Point(1, 3))


    def testPointStrCast_Success(self):
        self.assertEqual('(0, 0)', str(Point(0, 0)))
        self.assertEqual('(-1, 0)', str(Point(-1, 0)))
        self.assertEqual('(0, 19)', str(Point(0, 19)))

    
    def testAddPoints_Success(self):
        self.assertEqual(Point(0, 0), Point(-1, 0) + Point(1, 0))
        self.assertEqual(Point(1, 0), Point(0, 0) + Point(1, 0))
        self.assertEqual(Point(0, 0), Point(-10, -20) + Point(10, 20))
        self.assertEqual(Point(-5, -19), Point(-3, -10) + Point(-2, -9))


    def testSubtractPoints_Success(self):
        self.assertEqual(Point(-2, 0), Point(-1, 0) - Point(1, 0))
        self.assertEqual(Point(-1, 0), Point(0, 0) - Point(1, 0))
        self.assertEqual(Point(-20, -40), Point(-10, -20) - Point(10, 20))
        self.assertEqual(Point(-1, -1), Point(-3, -10) - Point(-2, -9))



# ----- end of file ------------------------------------------------------------





