#### Dear Manager,
<p>Our representation of the game state will be broken up into two main components: the game state (GameState), and the game state layout (GameStateLayout). The GameStateLayout will be a code facing object, allowing characters and adversaries to see information that is only relevant to them. This will prevent both players and adversaries from having access to game components which are not relevant to them. The normal GameState will be the class returned to an actor after a move is made to indicate an interaction result. This will contain information such as whether the exit is unlocked after a key is picked up, whether the game has been won or lost, or if the player is expelled after interacting with an adversary.</p>
<p>The GameStateLayout class will display different information such as the visible layout, valid moves, and interactable objects based on which actor is requesting the information. As a result, our gameStateLayout class will be a field which represents which actor the game state is currently for, as well as two primary methods used to relay information to the actor. The first method, showlayout, will return the layout of the level currently surrounding that actor. If the actor is a character, this method would return the layout of the level currently within the actor’s visible radius. If the actor is an adversary, this method would return the layout of the entire level.</p>
<p>The second method the GameStateLayout class will have is listValidMoves. This method will return a list of the valid moves that are available to the current actor. For example, if the current actor is a player, the method would return a list of all walkable tiles within a 2 tile radius, assuming they are within the player's vision. For an adversary, this method would return all walkable tiles, or tiles containing a player within a 1 block radius.</p>

<p>An example design of the two game state classes are shown below.</p>

```python
# represents the return information after an actor performs a move/interaction
class GameState:
    exitUnlocked: bool # if the exit door is unlocked yet
    gameOver: bool # if the game is won or lost from the perspective of the Actor
    gameWon: bool # from the perspective of the Actor

# provides the actor with information about their surroundings and available moves for their turn
class GameStateLayout(GameState):
    actor: Actor # who the game state is for

    # the layout of the actor’s field of view
    def showLayout() -> FloorPlan:
        pass

    # points are relative to current position
    def listValidMoves() -> list(Point):
        pass

# represents a 2D position on a coordinate system
class Point:
    pass

# represents a base class for either a player or an automated adversary
class Actor:
    pass

# represents a base class containing information about tile placements in a coordinate system
# (“tiles” may be walls, empty, keys, doors, exits, etc.. pretty much anything that is displayed)
class FloorPlan:
    pass
```
