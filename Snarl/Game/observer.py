#
# observer.py
# authors: Michael Curley & Drake Moore
#

from controller import Controller, SingleLocalObserverController
from iObserver import IObserver
from gameState import GameState


class Observer(IObserver):
    """ Observer implementation """

    def __init__(self, name: str, controller = None):
        """ observer can be added at any point of the game with the current game state
            Controller defaults to local controller """
        self.__validateController(controller)
        self.name = name
        self.currentGameState = None
        self.controller = SingleLocalObserverController() if controller is None else controller


    def updateGameState(self, gameState: GameState):
        """ updates the game state for the observer """
        self.currentGameState = gameState
        self.controller.updateGameState(gameState)
    

    def __validateController(self, controller):
        """ raises value error if the given controller is invalid """
        if controller is not None and not isinstance(controller, Controller):
            raise ValueError('An Observer must be given a valid controller or None.')



# ----- end of file ------------------------------------------------------------

