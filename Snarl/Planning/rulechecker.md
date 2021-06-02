To: Manager\
From: Michael Curley & Drake Moore

The interface for the rule checker is outlined below.  From a high level, the class will return only boolean values from the public methods.  Each method has a corresponding doc to describe its functionality.  Generally, each method is passed all the relevant information it would need so the methods are more static; this way the rule checker is completely independent of a game state.

A few important clarifications:
1. An Actor is a base class for either a Player or an Adversary.
2. An Actor has a list of traversable tiles so valid moves can be different based on the child class implementations.
3. An Actor has a move radius, for Players this would be 2 while Adversaries would be 1.
4. A FloorPlan is an object implemented for Milestone 2, it is a general layout of tiles with an upper left position, this tile layout may be a Room, a Hallway or an entire Level with multiple Rooms/Hallways.  We chose to use this FloorPlan base class for validation checking since the Room, Hallway and Level objects enforce a certain style for game play, but the rule checker shouldn’t know (or have to deal with) any of these specifics.
5. Until additional functionality for keys/exits are required, we pass relevant information about the key status and the exit location so they are not tied to the FloorPlan object, additionally Actors are not placed in the FloorPlan since the rule checker outputs hypothetical moves based on the given configuration; in short a validation for one FloorPlan may be tested with several configurations of Actors, key status and exit location while leaving the original FloorPlan unchanged.

```python
class RuleChecker:
""" Checks the validity of Actor moves and whether the level has been completed or the
    game is over. """

def isMoveValid(forActor: Actor, toRelativePoint: Point, onLayout: FloorPlan,
                withOtherActors: list(Actor)) -> bool:
""" Determines if a move is valid for the given Actor (may be a Player or Adversary).
    A move is valid based on the actor’s moveRadius, traversableTiles and the
    locations of other Actors. An Adversary cannot move to the same tile as another
    Adversary and same for a Player. However Players and Adversaries may move to the
    same tiles. """
        pass

def isLevelOver(allPlayers: list(Player), keyCollected: bool,
                exitPortalLocation: Point) -> bool:
""" A level is over if any player that hasn’t been expelled has made it to the
    exitPortalLocation and the key has been collected. """
        pass

def isGameOver(allPlayers: list(Player), keyCollected: bool,
                exitPortalLocation: Point, currentLevel: int, totalLevels: int) -> bool:
""" Determines if the game is over, a game is over if isLevelOver and the current level
    is the last level OR all players have been expelled. """
        pass
```
