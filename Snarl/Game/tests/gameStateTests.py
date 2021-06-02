#
# gameStateTests.py
# authors: Michael Curley & Drake Moore
#

from actor import Actor, Player, Adversary
from floorPlan import FloorPlan
from levelManagerBuilder import LevelManagerBuilder
from levelManager import LevelManager
from gameState import GameState
from hallway import Hallway
from interactable import Interactable
from level import Level
from point import Point
from room import Room
from tile import Tile
from unittest import TestCase


class GameStateTests(TestCase):
    """ Tests for Game States """

    def setUp(self):
        self.builder = LevelManagerBuilder()
        self.builder.setKeyLocation(Point(1, 3)
        ).setExitLocation(Point(12, 11)
        ).addLevelComponent(Room(Point(0, 0), [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.DOOR,  Tile.WALL,  Tile.WALL]
        ])).addLevelComponent(Room(Point(10, 10), [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL]
        ])).addLevelComponent(Hallway([
            Point(2, 4), Point(2, 6), Point(7, 6), Point(7, 8), Point(0, 8),
            Point(0, 12), Point(5, 12), Point(5, 11), Point(10, 11)
        ])).registerPlayer('A', 'actor', Point(3, 3)
        ).registerAdversary('zombie', 'undead jim', Point(3, 2))


    def testPlayerGameState_Success(self):
        gm = self.builder.build()
        gs = gm.getActorGameState('actor')
        self.assertEqual(False, gs.gameWon)
        self.assertEqual(False, gs.gameOver)
        self.assertEqual(False, gs.exitUnlocked)
        self.assertEqual(gm.getActorIfExists('actor'), gs.actor)
        # get tile out of fov and make sure it is UNKNOWN, stuff like that
    

    def testAdversaryGameState_Success(self):
        gm = self.builder.build()
        gs = gm.getActorGameState('undead jim')
        self.assertEqual(False, gs.gameWon)
        self.assertEqual(False, gs.gameOver)
        self.assertEqual(False, gs.exitUnlocked)
        self.assertEqual(gm.getActorIfExists('undead jim'), gs.actor)
        # again do fov stuff but adversary can see whole level

    def testListValidMovesCantTravelThroughTiles_Success(self):
        builder = LevelManagerBuilder()
        builder.setKeyLocation(Point(1, 3)
        ).setExitLocation(Point(12, 11)
        ).addLevelComponent(Room(Point(0, 0), [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.WALL, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.DOOR,  Tile.WALL,  Tile.WALL]
        ])).addLevelComponent(Room(Point(10, 10), [
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL,  Tile.WALL,  Tile.WALL]
        ])).addLevelComponent(Hallway([
            Point(2, 4), Point(2, 6), Point(7, 6), Point(7, 8), Point(0, 8),
            Point(0, 12), Point(5, 12), Point(5, 11), Point(10, 11)
        ])).registerPlayer('A', 'actor', Point(1, 1))
        gm = builder.build()

        # The two tiles to the right of the player can't be reached
        self.assertCountEqual([
            Point(1, 1), Point(1, 2), Point(1, 3),
            Point(2, 2)
        ], gm.getActorGameState('actor').listValidMoves())


    def testPlayerGameStateListValidMoves_Success(self):
        self.assertCountEqual([
            Point(3, 1), Point(3, 2), Point(3, 3),
            Point(2, 2), Point(2, 3), Point(2, 4),
            Point(1, 3)
        ], self.builder.build().getActorGameState('actor').listValidMoves())
    

    def testAdversaryGameStateListValidMoves_Success(self):
        self.assertCountEqual([
            Point(3, 1), Point(3, 2), Point(3, 3),
            Point(2, 2)
        ], self.builder.build().getActorGameState('undead jim').listValidMoves())


    def testPlayerShowLayout_Success(self):
        gm = self.builder.build()
        gs = gm.getActorGameState('actor')
        self.assertEqual(
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n' +
            '_ _       X   _ _ _ _ _ _ _ _\n' +
            '_ _     Z X   _ _ _ _ _ _ _ _\n' +
            '_ _ K   A X   _ _ _ _ _ _ _ _\n' +
            '_ _ X   X X   _ _ _ _ _ _ _ _\n' +
            '_ _ X   X X X _ _ _ _ _ _ _ _\n' +
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n' +
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n' +
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n' +
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n' +
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n' +
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n' +
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n' +
            '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _',
            gs.showLayout())
        self.assertEqual(gs.floorPlan.getTileInLayout(Point(9, 9)), Tile.UNKNOWN)


    def testPlayerGetKnownLayout_Success(self):
        gm = self.builder.build()
        self.assertEqual([
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL, Tile.NONE],
            [Tile.EMPTY, Tile.EMPTY, gm.getActorIfExists('undead jim'), Tile.WALL, Tile.NONE],
            [Interactable.KEY, Tile.EMPTY, gm.getActorIfExists('actor'), Tile.WALL, Tile.NONE],
            [Tile.WALL, Tile.DOOR, Tile.WALL, Tile.WALL, Tile.NONE],
            [Tile.WALL, Tile.HALLWAY, Tile.WALL, Tile.WALL, Tile.WALL]
        ], gm.getActorGameState('actor').getKnownLayout())


    def testAdversaryShowLayout_Success(self):
        self.assertEqual(
            '  X X X X X                  \n' +
            '  X       X                  \n' +
            '  X     Z X                  \n' +
            '  X K   A X                  \n' +
            '  X X   X X                  \n' +
            '    X   X X X X X X          \n' +
            '    X             X          \n' +
            'X X X X X X X X   X          \n' +
            'X                 X          \n' +
            'X   X X X X X X X X          \n' +
            'X   X     X X X X X X X X X X\n' +
            'X   X X X X               E X\n' +
            'X             X X X X X     X\n' +
            'X X X X X X X X       X X X X',
            self.builder.build().getActorGameState('undead jim').showLayout())


        

# ----- end of file ------------------------------------------------------------





