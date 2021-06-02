#
# iObserver.py
# authors: Michael Curley & Drake Moore
#

from gameState import GameState
from abc import ABC


class IObserver(ABC):
    """ represents the minimum functionality for the Observer object """

    def updateGameState(self, gameState: GameState):
        """ updates the game state for the observer"""
        raise NotImplementedError


# ----- end of file ------------------------------------------------------------
