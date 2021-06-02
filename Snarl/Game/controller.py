#
# controller.py
# authors: Michael Curley & Drake Moore
#

from gameState import GameState
from point import Point
from random import randint
from tile import Tile
from interactable import Interactable
from moveResult import MoveResult
from uuid import uuid1


class Controller:
    """ represents a controller for a single actor or observer in the game """

    def getName(self) -> str:
        """ give a unique name for this controller """
        return str(uuid1())

    def updateGameState(self, gameState: GameState):
        pass

    def requestMove(self, gameState: GameState) -> Point:
        raise NotImplementedError

    def updateMoveResult(self, moveResult: MoveResult):
        pass

    def updateFinalStats(self, finalStats: list):
        """ stats is a list of dictionarys with a name: name field """
        pass


class SingleLocalObserverController(Controller):
    """ represents a local controller for an observer to print out updates """

    def updateGameState(self, gameState: GameState):
        """ prints the updated layout """
        print('observer update:')
        if gameState.messages is not None:
            for message in gameState.messages:
                print(message)
        print(gameState.showLayout())
        print(('-' * 80) + '\n')


class NoMoveController(Controller):
    """ represents a controller that never moves and does not update anything """

    def __init__(self, updateDelegate = None):
        """ may be given a delegate function pointer to execute something upon
        update, this is a shortcut rather than implementing a new class """
        self.gameStates = list()
        self.updateDelegate = updateDelegate


    def updateGameState(self, gameState: GameState):
        """ adds the game state to the running list """
        self.gameStates.append(gameState)
        if self.updateDelegate is not None:
            self.updateDelegate(gameState)


    def requestMove(self, gameState: GameState) -> Point:
        """ always returns the same location """
        return gameState.actor.location


class ClosestPlayerController(Controller):
    """ represents a controller where every move is an attempt to move to the
    closest player """

    def updateGameState(self, gameState: GameState):
        """ no need for update, override so no error is raised """
        pass

    def preferredMoves(self, gameState: GameState) -> list:
        """ returns a list of preferred moves based on the game state """
        return gameState.listValidMoves()

    def requestMove(self, gameState: GameState) -> Point:
        """ returns a move that will bring the actor to the nearest player """
        from actor import Player
        distances = { gameState.actor.location.distanceFrom(p.location): p.location
                for p in filter(lambda a: isinstance(a, Player), gameState.allActors) }
        if len(distances) == 0:
            return gameState.actor.location
        closestPoint = distances[min(distances.keys())]
        distances = { closestPoint.distanceFrom(loc): loc
                for loc in self.preferredMoves(gameState) }
        return distances[min(distances.keys())]


class LocalZombieController(ClosestPlayerController):
    """ represents a controller for a zombie that moves to the closest player,
    if the zombie's best move is no move, it will make a random decision """

    def getName(self) -> str:
        return f'Zombie({super().getName()})'

    def requestMove(self, gameState: GameState) -> Point:
        """ returns a move that will bring the zombie to the nearest player or
        to a random spot if that move is invalid """
        bestMove = super().requestMove(gameState)
        if bestMove == gameState.actor.location:
            # if the zombie's best move is to stay put, we will choose a random
            # different move to keep the zombie moving (if possible)
            validMoves = gameState.listValidMoves()
            validMoves.remove(bestMove)
            if len(validMoves) > 0:
                bestMove = validMoves[randint(0, len(validMoves) - 1)]
        return bestMove


class LocalGhostController(ClosestPlayerController):
    """ represents a controller for a ghost that moves to the closest player,
    if the ghost's best move is no move, it will try to move to a wall tile """

    def getName(self) -> str:
        return f'Ghost({super().getName()})'

    def preferredMoves(self, gameState: GameState) -> list:
        """ returns a list of valid moves excluding wall destinations """
        return list(filter(lambda loc:
            gameState.floorPlan.getTileInLayout(loc) != Tile.WALL,
            gameState.listValidMoves()))

    def requestMove(self, gameState: GameState) -> Point:
        """ returns a move that will bring the ghost to the nearest player, if
        not will attempt to move to a wall and lastly will select a random
        location """
        bestMove = super().requestMove(gameState)
        if bestMove == gameState.actor.location:
            # if the ghost's best move is to stay put, we will try to move to a
            # wall location, if not choose something random
            validMoves = gameState.listValidMoves()
            prefMoves = self.preferredMoves(gameState)
            wallMoves = list(filter(lambda m: m not in prefMoves, validMoves))
            if len(wallMoves) != 0:
                # move to a wall if possible
                bestMove = wallMoves[0]
            else:
                # move randomly
                validMoves.remove(bestMove)
                if len(validMoves) > 0:
                    bestMove = validMoves[randint(0, len(validMoves) - 1)]
        return bestMove


# ----- end of file ------------------------------------------------------------





