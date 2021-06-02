#
# levelManagerBuilderTests.py
# authors: Michael Curley & Drake Moore
#

from hallway import Hallway
from level import Level
from point import Point
from room import Room
from tile import Tile
from actor import Actor, Player, Zombie, Ghost
from levelManagerBuilder import LevelManagerBuilder
from gameState import GameState
from floorPlan import FloorPlan
from unittest import TestCase


class LevelManagerBuilderTests(TestCase):
    """ tests for game manager builder """

    def setUp(self):
        self.builder = LevelManagerBuilder(
        ).setKeyLocation(Point(1, 3)
        ).setExitLocation(Point(12, 11)
        ).setKeyCollected(False
        ).addLevelComponent(Room(Point(0, 0), [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.DOOR],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.DOOR,  Tile.WALL,  Tile.WALL]
        ])).addLevelComponent(Room(Point(20, -5), [
            [Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL, Tile.WALL]
        ])).addLevelComponent(Room(Point(10, 10), [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL]
        ])).addLevelComponent(Hallway([
            Point(4, 2), Point(10, 2), Point(10, -4), Point(20, -4)
        ])).addLevelComponent(Hallway([
            Point(2, 4), Point(2, 6), Point(7, 6), Point(7, 8), Point(0, 8),
            Point(0, 12), Point(5, 12), Point(5, 11), Point(10, 11)
        ]))


    def __registerDefaults(self):
        self.builder.registerPlayer('M', 'mike', Point(2, 2)
            ).registerAdversary('zombie', 'zombay'
            ).registerAdversary('ghost', 'ghostie')


    def testBaseLevelManagerBuilder_Success(self):
        self.__registerDefaults()
        gm = self.builder.build()
        self.assertEqual(Point(1, 3), gm.keyLocation)
        self.assertEqual(Point(12, 11), gm.exitLocation)
        self.assertFalse(gm.keyCollected)
        self.assertTrue(isinstance(gm.getActorIfExists('mike'), Player))
        self.assertEqual('mike', gm.getActorIfExists('mike').name)
        self.assertEqual(Point(2, 2), gm.getActorIfExists('mike').location)
        self.assertTrue(isinstance(gm.getActorIfExists('zombay'), Zombie))
        self.assertEqual('zombay', gm.getActorIfExists('zombay').name)
        self.assertTrue(isinstance(gm.getActorIfExists('ghostie'), Ghost))
        self.assertEqual('ghostie', gm.getActorIfExists('ghostie').name)
        with self.assertRaises(ValueError):
            gm.getActorIfExists('bob') # is not in the game


    def testLevelManagerBuilderTooManyPlayers_ValueError(self):
        # mike already registered, > 4 players is an error
        self.__registerDefaults()
        self.builder.registerPlayer('a', 'alice'
            ).registerPlayer('b', 'bob'
            ).registerPlayer('c', 'carol'
            ).registerPlayer('d', 'drake')
        with self.assertRaises(ValueError):
            self.builder.build()


    def testLevelManagerBuilderTooFewPlayers_ValueError(self):
        with self.assertRaises(ValueError):
            self.builder.build()


    def testLevelManagerBuilderRegisterDuplicatePlayerNames_ValueError(self):
        self.__registerDefaults()
        with self.assertRaises(ValueError):
            self.builder.registerPlayer('x', 'mike') # dif id, dup name
        with self.assertRaises(ValueError):
            self.builder.registerPlayer('M', 'mary') # dup id, dif name
        with self.assertRaises(ValueError):
            self.builder.registerPlayer('x', 'ghostie') # player with adversary name
        with self.assertRaises(ValueError):
            self.builder.registerAdversary('ghost', 'mike') # adversary with player name

    
    def testLevelManagerBuilderRegisterDuplicateAdversaryNames_ValueError(self):
        self.__registerDefaults()
        with self.assertRaises(ValueError):
            self.builder.registerAdversary('ghost', 'zombay') # dup name
        with self.assertRaises(ValueError):
            self.builder.registerAdversary('zombie', 'ghostie') # dup name

    
    def testLevelManagerBuilderInvalidAdversaryType_ValueError(self):
        with self.assertRaises(ValueError):
            self.builder.registerAdversary('monster', 'john')
        with self.assertRaises(ValueError):
            self.builder.registerAdversary('werewolf', 'doe')


    def testLevelManagerBuilderProducesLayout_Success(self):
        self.__registerDefaults()
        self.assertEqual('' +
            '                    X X X X X X X X X X X X X X\n' +
            '                    X                         X\n' +
            '                    X   X X X X X X X X X X X X\n' +
            '                    X   X                      \n' +
            '                    X   X                      \n' +
            '  X X X X X         X   X                      \n' +
            '  X       X X X X X X   X                      \n' +
            '  X   M                 X                      \n' +
            '  X K     X X X X X X X X                      \n' +
            '  X X   X X                                    \n' +
            '    X   X X X X X X                            \n' +
            '    X             X                            \n' +
            'X X X X X X X X   X                            \n' +
            'X                 X                            \n' +
            'X   X X X X X X X X                            \n' +
            'X   X     X X X X X X X X X X                  \n' +
            'X   X X X X             Z E X                  \n' +
            'X             X X X X X G   X                  \n' +
            'X X X X X X X X       X X X X                  ',
                self.builder.build().asciiRender())



# ----- end of file ------------------------------------------------------------





