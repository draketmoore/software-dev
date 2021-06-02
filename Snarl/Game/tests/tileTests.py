#
# tileTests.py
# authors: Michael Curley & Drake Moore
#

from tile import Tile
from unittest import TestCase


class TileTests(TestCase):
    """ tests for the Tile object """

    def testTileAsciiRender_Success(self):
        # ignoring these while trying different game styles
        #self.assertEqual('W', Tile.WALL.asciiRender())
        #self.assertEqual('D', Tile.DOOR.asciiRender())
        #self.assertEqual(' ', Tile.EMPTY.asciiRender())
        #self.assertEqual('H', Tile.HALLWAY.asciiRender())
        #self.assertEqual('?', Tile.UNKNOWN.asciiRender())
        pass


    def testTileGenerateLayoutRequiresInts_ValueError(self):
        with self.assertRaises(ValueError):
            Tile.EMPTY.generateLayoutOfSize(2, 2.0)
        with self.assertRaises(ValueError):
            Tile.EMPTY.generateLayoutOfSize(2.0, 2)
        with self.assertRaises(ValueError):
            Tile.EMPTY.generateLayoutOfSize(2.0, 2.0)


    def testTileGenerateLayoutRequiresPositives_ValueError(self):
        with self.assertRaises(ValueError):
            Tile.EMPTY.generateLayoutOfSize(2, -2)
        with self.assertRaises(ValueError):
            Tile.EMPTY.generateLayoutOfSize(-2, 2)
        with self.assertRaises(ValueError):
            Tile.EMPTY.generateLayoutOfSize(-2, -2)


    def testTileGenerateLayout_Success(self):
        any0x0Layout = list()
        self.assertEqual(any0x0Layout, Tile.EMPTY.generateLayoutOfSize(0, 0))
        e = Tile.EMPTY
        empty2x2Layout = [[e, e], [e, e]]
        self.assertEqual(empty2x2Layout, Tile.EMPTY.generateLayoutOfSize(2, 2))
        u = Tile.UNKNOWN
        unknown4x3Layout = [[u, u, u, u], [u, u, u, u], [u, u, u, u]]
        self.assertEqual(unknown4x3Layout, Tile.UNKNOWN.generateLayoutOfSize(4, 3))


# ----- end of file ------------------------------------------------------------





