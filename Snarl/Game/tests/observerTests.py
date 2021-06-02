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
from controller import Controller
from observer import Observer

class DummyController(Controller):
    def __init__(self):
        self.currentGameState = None
    def updateGameState(self, gameState: GameState):
        self.currentGameState = gameState

class ObserverTests(TestCase):
    """ unit tests for observer class """

    def setUp(self):
        self.builder = LevelManagerBuilder()
        self.builder.setKeyLocation(Point(1, 3)
        ).setExitLocation(Point(12, 11)
        ).addLevelComponent(Room(Point(0, 0), [
            [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL, Tile.DOOR, Tile.WALL, Tile.WALL]
        ])).addLevelComponent(Room(Point(10, 10), [
            [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
            [Tile.DOOR, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.WALL],
            [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL]
        ])).addLevelComponent(Hallway([
            Point(2, 4), Point(2, 6), Point(7, 6), Point(7, 8), Point(0, 8),
            Point(0, 12), Point(5, 12), Point(5, 11), Point(10, 11)
        ])).registerPlayer('A', 'actor', Point(3, 3)
        ).registerAdversary('zombie', 'undead jim', Point(3, 2)
        ).registerObserver('observer1', DummyController())

    def testUpdateGameState_Success(self):
        gm = self.builder.build()
        observer = gm.observers["observer1"]
        self.assertEqual(observer.currentGameState, None)
        gs = gm.getObserverGameState()
        gm.observers["observer1"].updateGameState(gs)
        self.assertEqual(gs, observer.currentGameState)


