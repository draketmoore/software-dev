#
# gameManager.py
# authors: Michael Curley & Drake Moore
#

from actor import Actor, Player, Adversary, Ghost, Zombie
from floorPlan import FloorPlan
from gameState import ActorGameState, GameState
from hallway import Hallway
from interactable import Interactable
from level import Level
from moveResult import MoveResult
from tile import Tile
from point import Point
from room import Room
from ruleChecker import RuleChecker
from levelManager import LevelManager


class GameManager:
    """ represents a game manager"""

    def __init__(self, levelManagers: list, currentLevelNumber: int = 1, ruleChecker: RuleChecker = None):
        """ initializes a game manager for running multiple levels,
        where the first level indexes from 1 """
        self.__verifyLevelManagers(levelManagers)
        self.levelManagers = levelManagers
        self.currentLevelIndex = currentLevelNumber - 1
        self.totalLevels = len(levelManagers)
        self.currentLevelManager = self.levelManagers[self.currentLevelIndex]
        self.ruleChecker = RuleChecker() if ruleChecker is None else ruleChecker
        self.gameWon = False


    def run(self):
        """ runs through all of the levels"""
        stats = self.__initStats()
        while 1:
            self.currentLevelManager.run(self.currentLevelIndex + 1,
                    self.totalLevels, stats)
            self.gameWon = self.__gameWon()
            self.currentLevelManager.gameWon = self.gameWon
            self.currentLevelIndex += 1
            if self.__isGameOver():
                break
            self.currentLevelManager = self.levelManagers[self.currentLevelIndex]
        friendlyStats = self.__convertToFriendlyStats(stats)
        for actor in self.currentLevelManager.allActors:
            actor.updateFinalStats(friendlyStats)


    def __initStats(self) -> dict:
        """ initializes the stats dictionary for the game """
        return { name: {
            MoveResult.Exit: 0,
            MoveResult.Eject: 0,
            MoveResult.Key: 0
        } for name in self.currentLevelManager.players }


    def __convertToFriendlyStats(self, stats: dict) -> list:
        """ converts the stats dictionary to a user-friendly version """
        stats = [ {
            'name': name,
            'exits': stats[name][MoveResult.Exit],
            'ejects': stats[name][MoveResult.Eject],
            'keys': stats[name][MoveResult.Key]
        } for name in stats ]
        stats = sorted(stats, key = (lambda s: s['exits']), reverse = True)
        return sorted(stats, key = (lambda s: s['keys']), reverse = True)


    def __isGameOver(self):
        """ checks if the game is over """
        return self.ruleChecker.isGameOver(self.currentLevelManager.players.values(),
                                    self.currentLevelIndex, self.totalLevels)


    def __gameWon(self):
        """ checks if the game is won """
        return self.__isGameOver() and self.ruleChecker.isGameWon(
                self.currentLevelManager.players.values())


    def __verifyLevelManagers(self, levelManagers):
        """ Verifies that all level managers are valid"""
        for manager in levelManagers:
            if not isinstance(manager, LevelManager):
                raise ValueError("Must be given a list of valid level managers.")


# ----- end of file ------------------------------------------------------------





