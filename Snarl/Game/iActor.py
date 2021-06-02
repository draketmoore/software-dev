#
# iActor.py
# authors: Michael Curley & Drake Moore
#

from abc import ABC
from point import Point

class IActor(ABC):
    """ represents the minimum functionality for an actor object """

    def updateGameState(self, gameState):
        """ updates the game state for the actor """
        raise NotImplementedError


    def requestMove(self, gameState) -> Point:
        """ requests a move based on the given game state for the actor """
        raise NotImplementedError


# ----- end of file ------------------------------------------------------------





