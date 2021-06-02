#
# floorPlanTests.py
# authors: Michael Curley & Drake Moore
#

from floorPlan import FloorPlan
from interactable import Interactable
from point import Point
from tile import Tile
from unittest import TestCase

class FloorPlanTests(TestCase):
    """ tests for the FloorPlan object """

    def setUp(self):
        self.baseUpperLeftPosition = Point(0, 0)
        self.baseLayout = [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL]
        ]
        self.fp = FloorPlan(self.baseUpperLeftPosition, self.baseLayout)
        self.negativeUpperLeftPosition = Point(-2, -2)
        self.negativeLayout = [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.WALL, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL]
        ]
        self.negativefp = FloorPlan(self.negativeUpperLeftPosition, self.negativeLayout)
    

    def testBaseFloorPlan_Success(self):
        self.assertEqual(Point(0, 0), self.fp.upperLeftPosition)
        self.assertEqual(Point(4, 6), self.fp.lowerRightPosition)
        self.assertEqual(5, self.fp.width)
        self.assertEqual(7, self.fp.height)


    def testBaseFloorPlanGetTraversableTiles_None(self):
        self.assertCountEqual(list(),
                self.fp.getTraversablePointsInLayout(list()))


    def testBaseFloorPlanGetTraversableTiles_Walls(self):
        self.assertCountEqual([
            Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0),
            Point(0, 1),                                        Point(4, 1),
            Point(0, 2),                                        Point(4, 2),
            Point(0, 3),                                        Point(4, 3),
            Point(0, 4),                                        Point(4, 4),
            Point(0, 5),                                        Point(4, 5),
            Point(0, 6), Point(1, 6), Point(2, 6), Point(3, 6), Point(4, 6)
        ], self.fp.getTraversablePointsInLayout([Tile.WALL]))


    def testBaseFloorPlanGetTraversableTiles_Empty(self):
        self.assertCountEqual([

                         Point(1, 1), Point(2, 1), Point(3, 1),
                         Point(1, 2), Point(2, 2), Point(3, 2),
                         Point(1, 3), Point(2, 3), Point(3, 3),
                         Point(1, 4), Point(2, 4), Point(3, 4),
                         Point(1, 5), Point(2, 5), Point(3, 5)

        ], self.fp.getTraversablePointsInLayout([Tile.EMPTY]))
    

    def testBaseFloorPlanGetTraversableTiles_EmptyAndWalls(self):
        self.assertCountEqual([
            Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0),
            Point(0, 1), Point(1, 1), Point(2, 1), Point(3, 1), Point(4, 1),
            Point(0, 2), Point(1, 2), Point(2, 2), Point(3, 2), Point(4, 2),
            Point(0, 3), Point(1, 3), Point(2, 3), Point(3, 3), Point(4, 3),
            Point(0, 4), Point(1, 4), Point(2, 4), Point(3, 4), Point(4, 4),
            Point(0, 5), Point(1, 5), Point(2, 5), Point(3, 5), Point(4, 5),
            Point(0, 6), Point(1, 6), Point(2, 6), Point(3, 6), Point(4, 6)
        ], self.fp.getTraversablePointsInLayout([Tile.EMPTY, Tile.WALL]))


    def testInvalidUpperLeftPosition_Error(self):
        with self.assertRaises(ValueError):
            FloorPlan(None, self.baseLayout)
        with self.assertRaises(ValueError):
            FloorPlan('Point', self.baseLayout)


    def testInvalidLayout_Error(self):
        with self.assertRaises(ValueError):
            FloorPlan(self.baseUpperLeftPosition, None)
        with self.assertRaises(ValueError):
            FloorPlan(self.baseUpperLeftPosition, 'layout')
        with self.assertRaises(ValueError):
            FloorPlan(self.baseUpperLeftPosition, set())
        with self.assertRaises(ValueError):
            FloorPlan(self.baseUpperLeftPosition, list())


    def testLayoutNotAllTileOrInteractable_Error(self):
        self.baseLayout[0][0] = None
        with self.assertRaises(ValueError):
            FloorPlan(self.baseUpperLeftPosition, self.baseLayout)
        self.setUp()
        self.baseLayout[4][3] = ''
        with self.assertRaises(ValueError):
            FloorPlan(self.baseUpperLeftPosition, self.baseLayout)


    def testLayoutNotAllRowsSameLength_Error(self):
        self.baseLayout[0] = self.baseLayout[0][1:]
        with self.assertRaises(ValueError):
            FloorPlan(self.baseUpperLeftPosition, self.baseLayout)
        self.setUp()
        self.baseLayout[3] = self.baseLayout[3][3:5]
        with self.assertRaises(ValueError):
            FloorPlan(self.baseUpperLeftPosition, self.baseLayout)


    def testProduceTileLayout_Success(self):
        baseTileLayout = self.fp.produceTileLayout()
        self.assertEqual(baseTileLayout, [[Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL]])
        self.assertEqual(baseTileLayout, self.fp.layout)


    def testTilePositionWithinBounds_Success(self):
        self.assertTrue(self.negativefp.tilePositionWithinBounds(Point(-1, 4)))
        self.assertTrue(self.negativefp.tilePositionWithinBounds(Point(-2, -2)))
        self.assertTrue(self.negativefp.tilePositionWithinBounds(Point(0, 0)))
        self.assertTrue(self.negativefp.tilePositionWithinBounds(Point(2, 2)))
        self.assertTrue(self.negativefp.tilePositionWithinBounds(Point(2, 4)))
        
        self.assertFalse(self.negativefp.tilePositionWithinBounds(Point(-2, -3)))
        self.assertFalse(self.negativefp.tilePositionWithinBounds(Point(5, 5)))
        self.assertFalse(self.negativefp.tilePositionWithinBounds(Point(0, -3)))
        self.assertFalse(self.negativefp.tilePositionWithinBounds(Point(0, 5)))


    def testGetTileInLayout_Success(self):
        self.assertEqual(self.negativefp.getTileInLayout(Point(1, 1)), Tile.WALL)
        self.assertNotEqual(self.negativefp.getTileInLayout(Point(0, 0)), Tile.WALL)
        self.assertEqual(self.negativefp.getTileInLayout(Point(-2, -2)), Tile.WALL)
        self.assertEqual(self.negativefp.getTileInLayout(Point(-1, -1)), Tile.EMPTY)
        self.assertEqual(self.negativefp.getTileInLayout(Point(2, 4)), Tile.WALL)


    def testSetTileInLayout_Success(self):
        self.assertEqual(self.negativefp.getTileInLayout(Point(2, 4)), Tile.WALL)
        self.assertEqual(self.negativefp.getTileInLayout(Point(-2, -2)), Tile.WALL)

        self.negativefp.setTileInLayout(Point(2, 4), Tile.HALLWAY)
        self.negativefp.setTileInLayout(Point(-2, -2), Tile.HALLWAY)

        self.assertEqual(self.negativefp.getTileInLayout(Point(2, 4)), Tile.HALLWAY)
        self.assertEqual(self.negativefp.getTileInLayout(Point(-2, -2)), Tile.HALLWAY)
        

    def testAsciiRender_Success(self):
        self.assertEqual(self.negativefp.asciiRender(),
            'X X X X X\n'+
            'X       X\n'+
            'X       X\n'+
            'X     X X\n'+
            'X       X\n'+
            'X       X\n'+
            'X X X X X')
       
        self.negativefp.setTileInLayout(Point(2, 4), Tile.HALLWAY)
        self.negativefp.setTileInLayout(Point(-2, -2), Tile.HALLWAY)
       
        self.assertEqual(self.negativefp.asciiRender(),
            '  X X X X\n'+
            'X       X\n'+
            'X       X\n'+
            'X     X X\n'+
            'X       X\n'+
            'X       X\n'+
            'X X X X  ')



# ----- end of file ------------------------------------------------------------





