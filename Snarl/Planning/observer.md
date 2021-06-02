To: Manager\
From: Michael Curley & Drake Moore

<p>Our interpretation of a game Observer is implemented through our Actor-Controller design. In our implementation, a Controller acts as the interface between a person and their Actor in the game. Through the Controller the person is updated with the current game state after other actors move, and prompted to enter a valid move when it is their turn. </p>
<p>For our Observer design, we decided to have the Observer extend the Actor class so that it can use this Controller functionality to observe the ongoing game. The game can be viewed either through the lens of an actor, or with a full view of the game, similar to the view of an Adversary. Observers will be kept separate from the game’s players and adversaries so that they can be continuously updated with new game states, but will not have moves requested from them. </p>

```python
class Actor:
	""" existing class, represents a Player or Adversary currently """

	def setController(c):
	""" sets this actor’s instance of a controller """
		pass

	def updateGameState(gs):
	""" updates the current game state for this actor """
		pass

	def requestMove() -> Point:
	""" requests a move from the actor’s current controller """
		pass


class Controller:
	""" represents a controller for a single actor in the game """

	def updateGameState(gamestate):
	""" updates the user with a new game state based on other actor’s moves """
		pass

	def requestMove() -> Point:
	 """ requests a move from the actor """
		pass

class Observer(Actor):
	""" represents an observer for the game """

	def __init__(self, name: str):
		Actor__init__(id = None, name = name, moveRange = 0, viewRadius = -1, startPosition = None, traversableTiles = list())
		pass
```
