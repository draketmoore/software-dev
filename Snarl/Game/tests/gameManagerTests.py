#
# gameManagerTests.py
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
from gameManager import GameManager
from unittest import TestCase


class GameManagerTests(TestCase):
    """ tests for game manager """

    def setUp(self):
        self.builder = LevelManagerBuilder(
            ).setKeyLocation(Point(1, 3)
            ).setExitLocation(Point(2, 3)
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

        self.registerDefaultPlayersAndAdversaries()
        levelManager1 = self.builder.build()

        self.builder = LevelManagerBuilder(
        ).setKeyLocation(Point(12, 13)
        ).setExitLocation(Point(1, 3)
        ).addLevelComponent(Room(Point(0, 0), [
            [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL, Tile.DOOR, Tile.WALL, Tile.WALL]
        ])).addLevelComponent(Room(Point(10, 10), [
            [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL]
        ])).addLevelComponent(Hallway([
            Point(2, 4), Point(2, 6), Point(7, 6), Point(7, 8), Point(0, 8),
            Point(0, 12), Point(5, 12), Point(5, 11), Point(10, 11)
        ]))
        self.registerDefaultPlayersAndAdversaries()
        levelManager2 = self.builder.build()
        self.gm = GameManager([levelManager1, levelManager2])


    def registerDefaultPlayersAndAdversaries(self):
        self.builder.registerPlayer('m', 'mike'
            ).registerPlayer('d', 'drake'
            ).registerAdversary('zombie', 'zombie0'
            ).registerAdversary('zombie', 'zombie2'
            ).registerAdversary('ghost', 'ghost1'
            ).registerAdversary('ghost', 'ghost2')

    def testRun(self):
        #self.assertTrue(self.gm.run())
        pass






# ----- end of file ------------------------------------------------------------





