#
# consoleController.py
# authors: Michael Curley & Drake Moore
#

from controller import Controller
from gameState import GameState
from point import Point
from tile import Tile
from interactable import Interactable
from moveResult import MoveResult


class ConsoleController(Controller):
    """ represents a simple console i/o controller """

    def getName(self) -> str:
        """ requests the name from the player """
        return input('Please enter your name: ')
    
    def updateFinalStats(self, finalStats: list):
        """ prints final stats to stdout """
        print('the final stats rankings are:')
        place = 1
        for stat in finalStats:
            print('{0}: {1}'.format(place, stat['name']))
            print('   times exited:   {0}'.format(stat['exits']))
            print('   keys collected: {0}'.format(stat['keys']))
            print('   times ejected:  {0}'.format(stat['ejects']))
            print(('-' * 80) + '\n')
            place += 1

    def updateGameState(self, gameState: GameState):
        """ updates the user if the game or level is over """
        from actor import Player
        if isinstance(gameState.actor, Player):
            print('UPDATED GAMESTATE')
            self.__printPlayerEvent(gameState)
            self.__printEndingEvent(gameState)
            print(gameState.showLayout())
            print(('-' * 80) + '\n')

    def __printPlayerEvent(self, gameState: GameState) -> bool:
        """ prints a player event, if any, returns if layout should be printed """
        if gameState.messages is not None:
            for message in gameState.messages:
                print(message)
            return True
        return False
            
    def __printEndingEvent(self, gameState: GameState) -> bool:
        """ prints an ending event, if any, returns if layout should be printed """
        prompt = 'Player {0}'.format(gameState.actor.name)
        if gameState.gameOver:
            print('{0} the game is over, you {1}!'.format(prompt,
                'won' if gameState.gameWon else 'lost'))
            if not gameState.gameWon and \
                    gameState.currentLevel > 0 and gameState.totalLevels > 0:
                print((' ' * len(prompt)) + 'you made it to level {0} out of {1}'.format(
                    gameState.currentLevel, gameState.totalLevels))
        elif gameState.levelOver:
            print('{0} you have completed '.format(prompt), end = '')
            if gameState.currentLevel > 0:
                print('level {0}{1}'.format(gameState.currentLevel,
                    ' out of {0}'.format(gameState.totalLevels if
                        gameState.totalLevels > 0 else '')))
            else:
                print('the level')
        else:
            return False
        return True

    def __printNonPlayingState(self, gameState: GameState) -> bool:
        """ prints the layout if an actor is expelled or exited """
        if gameState.actor.expelled or gameState.actor.exited:
            print(gameState.showLayout())
            return True
        return False

    def updateMoveResult(self, moveResult: MoveResult):
        """ prints the result to stdout """
        #print(f'move result: {moveResult.name.lower()}')
        pass # TODO do we want to output anything?

    def requestMove(self, gameState: GameState) -> Point:
        """ requests a move from the actor """
        print('MOVE REQUESTED')
        print(gameState.showLayout())
        print(self.__createPrompt(gameState))
        validMoves = gameState.listValidMoves()
        while 1:
            try:
                i = int(input('enter a move index: '))
                if i >= 0 and i < len(validMoves):
                    move = validMoves[i]
                    break
            except (ValueError, IndexError):
                pass # expected
            print('Error: Please enter a move number between 0 and {0}'.format(
                    len(validMoves) - 1))
        print(('-' * 80) + '\n')
        return move

    def __createPrompt(self, gameState: GameState) -> str:
        """ generates the prompt to print to the user """
        moveNum = 0
        moveOptions = ''
        validMoves = gameState.listValidMoves()
        for move in validMoves:
            relMove = move - gameState.actor.location
            englishMove = list()
            if relMove.X != 0:
                englishMove.append('{0} {1}'.format(abs(relMove.X),
                        'right' if relMove.X > 0 else 'left'))
            if relMove.Y != 0:
                englishMove.append('{0} {1}'.format(abs(relMove.Y),
                        'up' if relMove.Y < 0 else 'down'))
            englishMove = ', '.join(englishMove).strip()
            moveOptions += '{0}: {1}\n'.format(moveNum,
                    'none' if englishMove == '' else englishMove)
            moveNum += 1
        prompt = '{0} you are at position {1}\n'.format(gameState.actor.name,
                gameState.actor.location)
        if gameState.actor.lifepoints is not None:
            prompt += 'you have {0} health left\n'.format(gameState.actor.lifepoints)
        prompt += 'these are your move options:\n{0}'.format(moveOptions)
        return prompt



# ----- end of file ------------------------------------------------------------





