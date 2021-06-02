To: Manager\
From: Michael Curley & Drake Moore

<p>As described in the game-manager.md plan, the data needed for providing information to a user is embedded in the Player object.  Since most of this functionality will be common with an adversary, both Player and Adversary objects will inherit from a base Actor object.</p>
<p>The interface for our Player representation is outlined below.  Generally, a player is just an Actor with some custom fields to initialize the Actor.  The only things necessary to define for a player are just the aspects where it differs from an Adversary.  This includes things like their field of view (2 tiles versus an Adversary that can see the whole level), a range that the Player can move and the tiles that a Player may actually walk on.</p>
<p>An Actor handles moving the current location and provides a render method that produces a string unique to each player.</p>

```python
class Actor:
""" represents an Actor in the game (player or adversary) """

    def __init__(self, asciiIdentifier: str, id: str, moveRange: range = range(0, 2), viewRadius: int: = -1, startLocation: Point = None, traversableTiles: list = None):
        """ initializes an Actor with the above local fields """
        pass
    
    def move(self, destination: Point):
        """ moves the actor to a given location """
        # note: rule checking will have been completed by this point
        pass

    def asciiRender(self) -> str:
        """ renders the player to an ascii string """
        pass

class Player(Actor):
    """ represents a player in the game """

    # a player may move 0-2 tiles
    MoveRange = range(0, 3)

    # a player may only see 2 tiles away
    ViewRadius = 2

    # a list of the tiles able to be traversed by a player
    TraversableTiles = list()
    
    def __init__(self, asciiIdentifier: str, playerId: str, startLocation: Point = None):
        Actor.__init__(self, asciiIdentifier, playerId, self.MoveRange, self.ViewRadius, startLocation, self.TraversableTiles)
```
