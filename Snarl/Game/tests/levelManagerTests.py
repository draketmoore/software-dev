#
# levelManagerTests.py
# authors: Michael Curley & Drake Moore
#

from hallway import Hallway
from interactable import Interactable
from level import Level
from point import Point
from room import Room
from tile import Tile
from actor import Actor
from levelManagerBuilder import LevelManagerBuilder
from gameState import GameState
from levelManager import LevelManager
from floorPlan import FloorPlan
from unittest import TestCase


class LevelManagerTests(TestCase):
    """ tests for game manager """

    def setUp(self):
        self.builder = LevelManagerBuilder(
            ).setKeyLocation(Point(1, 3)
            ).setExitLocation(Point(12, 13)
            ).addLevelComponent(Room(Point(0, 0), [
                [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.WALL,  Tile.DOOR,  Tile.WALL,  Tile.WALL]
            ])).addLevelComponent(Room(Point(10, 10), [
                [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL, Tile.WALL],
                [Tile.DOOR, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
                [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL, Tile.WALL]
            ])).addLevelComponent(Hallway([
                Point(2, 4), Point(2, 6), Point(7, 6), Point(7, 8), Point(0, 8),
                Point(0, 12), Point(5, 12), Point(5, 11), Point(10, 11)
            ]))


    def registerDefaultPlayersAndAdversaries(self):
        self.builder.registerPlayer('m', 'mike'
            ).registerPlayer('d', 'drake'
            ).registerAdversary('zombie', 'zombie0'
            ).registerAdversary('zombie', 'zombie1'
            ).registerAdversary('zombie', 'zombie2'
            ).registerAdversary('ghost', 'ghost1'
            ).registerAdversary('ghost', 'ghost2'
            ).registerAdversary('ghost', 'ghost3')
        


    def testLevelManager_Success(self):
        self.registerDefaultPlayersAndAdversaries()
        gm = self.builder.build()
        self.assertEqual('  X X X X X                    \n' +
                         '  X m d   X                    \n' +
                         '  X       X                    \n' +
                         '  X K     X                    \n' +
                         '  X X   X X                    \n' +
                         '    X   X X X X X X            \n' +
                         '    X             X            \n' +
                         'X X X X X X X X   X            \n' +
                         'X                 X            \n' +
                         'X   X X X X X X X X            \n' +
                         'X   X     X X X X X X X X X X X\n' +
                         'X   X X X X             Z Z Z X\n' +
                         'X             X X X X X G G G X\n' +
                         'X X X X X X X X       X   E   X\n' +
                         '                      X X X X X', gm.asciiRender())

    
    def testMovePlayer_Success(self):
        self.registerDefaultPlayersAndAdversaries()
        gm = self.builder.build()
        gm.moveActor('mike', Point(2, 2))
        self.assertEqual('  X X X X X                    \n' +
                         '  X   d   X                    \n' +
                         '  X   m   X                    \n' +
                         '  X K     X                    \n' +
                         '  X X   X X                    \n' +
                         '    X   X X X X X X            \n' +
                         '    X             X            \n' +
                         'X X X X X X X X   X            \n' +
                         'X                 X            \n' +
                         'X   X X X X X X X X            \n' +
                         'X   X     X X X X X X X X X X X\n' +
                         'X   X X X X             Z Z Z X\n' +
                         'X             X X X X X G G G X\n' +
                         'X X X X X X X X       X   E   X\n' +
                         '                      X X X X X', gm.asciiRender())


    def testLevelManagerTooManyPlayers_ValueError(self):
        self.builder.registerPlayer('m', 'mike'
            ).registerPlayer('d', 'drake'
            ).registerPlayer('j', 'jane'
            ).registerPlayer('b', 'bob'
            ).registerPlayer('s', 'sam') # 5 players in the game
        with self.assertRaises(ValueError):
            self.builder.build()


    def testLevelManagerTooFewPlayers_ValueError(self):
        # no players in the game
        with self.assertRaises(ValueError):
            self.builder.build()


    def testLevelManagerPlayerGameState_Success(self):
        self.registerDefaultPlayersAndAdversaries()
        gm = self.builder.build()
        gs = gm.getActorGameState('mike')
        self.assertEqual(gm.players['mike'].identifier, gs.actor.identifier)
        self.assertEqual(gm.players['mike'].name, gs.actor.name)


    def testLevelManagerAdversaryGameState_Success(self):
        self.registerDefaultPlayersAndAdversaries()
        gm = self.builder.build()
        gs = gm.getActorGameState('zombie0')
        self.assertEqual(gm.adversaries['zombie0'].identifier, gs.actor.identifier)
        self.assertEqual(gm.adversaries['zombie0'].name, gs.actor.name)


    def testLevelManagerGameState_Error(self):
        self.registerDefaultPlayersAndAdversaries()
        gm = self.builder.build()
        with self.assertRaises(ValueError):
            gm.getActorGameState('not a real player or adversary name')

    
    def testProduceTileLayoutIncludesKeyAndExit_Success(self):
        self.registerDefaultPlayersAndAdversaries()
        gm = self.builder.build()
        tileLayout = gm.produceTileLayout()
        self.assertEqual(Interactable.KEY, tileLayout[3][2])
        self.assertEqual(Interactable.EXIT, tileLayout[13][13])


    def testKeyInHallway_ValueError(self):
        self.builder.setKeyLocation(Point(2, 6)) # in hallway
        self.registerDefaultPlayersAndAdversaries()
        with self.assertRaises(ValueError):
            self.builder.build()
    

    def testKeyInVoid_ValueError(self):
        self.builder.setKeyLocation(Point(-1, 0)) # outside top room
        self.registerDefaultPlayersAndAdversaries()
        with self.assertRaises(ValueError):
            self.builder.build()
    

    def testExitInHallway_ValueError(self):
        self.builder.setExitLocation(Point(8, 11)) # in hallway
        self.registerDefaultPlayersAndAdversaries()
        with self.assertRaises(ValueError):
            self.builder.build()
    

    def testExitInVoid_ValueError(self):
        self.builder.setExitLocation(Point(9, 13)) # outside bottom room
        self.registerDefaultPlayersAndAdversaries()
        with self.assertRaises(ValueError):
            self.builder.build()


# ----- end of file ------------------------------------------------------------





