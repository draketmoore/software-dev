#
# ruleChecker.py
# authors: Michael Curley & Drake Moore
#

from actor import Actor, Player, Adversary
from copy import deepcopy
from floorPlan import FloorPlan
from gameState import GameState
from hallway import Hallway
from interactable import Interactable
from level import Level
from tile import Tile
from point import Point
from room import Room


class RuleChecker:
    """ Checks the validity of Actor moves and whether the level has been
    completed or the game is over. """

    def isMoveValid(self, actor: Actor, destinationPoint: Point, floorPlan: FloorPlan) -> bool:
        """ Determines if a move is valid for the given Actor (may be a Player
        or Adversary). A move is valid based on the actor's moveRadius,
        traversableTiles and the locations of other Actors. An Adversary cannot
        move to the same tile as another Adversary and same for a Player.
        However Players and Adversaries may move to the same tiles. """

        # an actor may stay put
        if actor.location == destinationPoint:
            return True

        # make sure destination is within the move range
        if ((abs(actor.location.Y - destinationPoint.Y) + 
            abs(actor.location.X - destinationPoint.X)) > actor.moveRange):
            return False

        # make sure tile is traversible for the actor
        destination = floorPlan.getTileInLayout(destinationPoint)
        if isinstance(destination, Actor):
            bothPlayers = isinstance(actor, Player) and isinstance(destination, Player)
            bothAdversaries = isinstance(actor, Adversary) and isinstance(destination, Adversary)
            return (destination.replacedTile in actor.traversableTiles and
                    not bothPlayers and not bothAdversaries)
        return destination in actor.traversableTiles


    def isLevelOver(self, allPlayers: list) -> bool:
        """ A level is over if any player that hasn't been expelled has made it
        to the exitPortalLocation and the key has been collected. """

        # if key is collected, check if any players have reached the exit
        if all(p.exited or p.expelled for p in allPlayers):
            return True

        return False


    def isGameOver(self, allPlayers: list, currentLevel: int, totalLevels: int) -> bool:
        """ Determines if the game is over, a game is over if isLevelOver and
        the current level is the last level OR all players have been expelled. """
        return currentLevel == totalLevels or all(p.expelled for p in allPlayers)

    
    def isGameWon(self, allPlayers: list) -> bool:
        """ determines if the game has been won if any player has exited """
        return any(p.exited for p in allPlayers)



# ----- end of file ------------------------------------------------------------





