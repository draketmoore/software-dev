To: Manager\
From: Michael Curley & Drake Moore

<p>The interface for our game manager is defined below.  The game manager has configurable static fields to determine the number of players and the number of adversaries allowed to participate in a game.  Additionally, the manager can return game states based on a given player or adversary identification string.</p>
<p>These GameState and GameStateLayout objects were defined in a previous milestone.  In short, a GameState provides the minimum information necessary to elaborate the result of a move, while a GameStateLayout provides information for a specific player/adversary based on a turn (the layout aspect provides an additional list of valid moves for the given turn as well as a view of the level that will be a small view for players and the entire level for an adversary, these view radiuses are embedded in the player and adversary objects).</p>
<p>The LevelManager also has a render method that just produces an ascii representation that will be able to be interpreted by a number of view objects.</p>
<p>To handle registering players and adversaries a Builder class is also provided.  The reason for this is that each game will have an unchanging set of players, adversaries and (for now) a single level.  Once all of these components are set through the builder the LevelManager will be constructed for the lifetime of a single game.</p>

```python
class LevelManager:
    """ represents the main manager to control a Snarl level """

    # allow between 1 and 4 players
    NumPlayerRange = range(1, 5)
    # allow between 0 and 10 adversaries (placeholder
    NumAdversaryRange = range(0, 11)

    def getPlayerGameStateLayout(self, playerId: str) -> GameStateLayout:
    """ returns the game state layout for a player """
        pass

    def getAdversaryGameStateLayout(self, adversaryId: str) -> GameStateLayout:
        """ returns the game state layout for an adversary """
        pass

    def movePlayer(self, playerId: str, toLocation: Point) -> GameState:
        """ moves a player to the given location, returns the updated state and interaction result (if any) """
        pass

    def moveAdversary(self, adversaryId: str, toLocation: Point) -> GameState:
        """ movies an adversary to the given location, returns the updated state and interaction result (if any) """
        pass
    
    def asciiRender(self):
        """ renders the entire game in an ascii string """
        pass

    class Builder:
        """ represents the LevelManager builder object to create a game to manage """

        def registerPlayer(self, playerId: str):
            """ adds a player to a game """
            return self

        def registerAdversary(self, type: AdversaryType, adversaryId: str):
            """ adds an adversary of the given type """
            return self

        def addLevelComponent(self, component: FloorPlan):
            """ adds a Room, Hallway or a Level object to manage """
            return self
        
        def buildLevelManager(self):
            """ creates a game based on the set values """
            return LevelManager(...)
```
