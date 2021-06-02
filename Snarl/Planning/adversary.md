To: Manager\
From: Michael Curley & Drake Moore

<p>The interface and implementation of our Adversary class is outlined below. All actors (players and adversaries) extend from the IActor interface, and the Actor subclass. The Actor class contains all of the functionality and information needed by both Players and Adversaries. The primary difference between an Adversary and a Player are the fields that define the Adversary's view radius and move range. </p>
<p> Our LevelManager’s main game loop function updates Player’s game states after every move is made, but only updates Adversaries when it is their turn. Additionally, Players are provided a view of the Level confined to their view radius, as well as restricted Actor information. Players are given a list of censored Actor statuses (for both Players and Adversaries) with only basic information such as: Actor’s expelled/exited fields, name, and their identifier. An adversary is given a negative view radius, meaning it gains complete view access to the entire level layout, and is given unrestricted view access to all Actor’s information (again, this includes both Players and other Adversaries), including their locations. </p>
<p>As commented in our LocalPlayer and LocalObserver implementations for this milestone, the idea of a “Local” object is defined by an Actor’s Controller object.  A definition for a LocalAdversary is included, however the base Adversary is flexible such that any sort of controller (to receive updates and provide game moves) may be assigned to any Adversary.</p>

```python
class IActor(ABC):
    """ represents the minimum functionality for an actor object """

    def updateGameState(self, gameState):
        """ updates the game state for the actor """
        raise NotImplementedError

    def requestMove(self, gameState) -> Point:
        """ requests a move based on the given game state for the actor """
        raise NotImplementedError


class Actor(IActor):
    """ represents an Actor in the game (a player or adversary) """

    def __init__(self, identifier: str, name: str, moveRange: int = 1,
            viewRadius: int = -1, startLocation: Point = None,
            traversableTiles: list = None):
        pass

    def move(self, destination: Point):
        """ moves the actor to the given location """  
        pass

    def asciiRender(self) -> str:
        """ returns the actor's identifier for ascii rendering """
        pass

    def updateGameState(self, gameState: GameState):
        """ updates the current game state for this actor """
        pass

    def requestMove(self) -> Point:
        """ returns a point based on the current game state """
        pass

class Adversary(Actor):
    """ Represents an adversary in the game """

     def __init__(self, identifier: str, name: str, startLocation: Point = None,
            traversableTiles: list = None, controller = None):
        """ initializes an adversary in the game """
        pass

class LocalAdversary(Adversary):
    """ Represents a local adversary in the game """

     def __init__(self, identifier: str, name: str, startLocation: Point = None,
            traversableTiles: list = None):
        """ initializes a local adversary in the game """
        Adversary.__init__(identifier, name, startLocation, traversableTiles,
                ConsoleController())
        pass
```
