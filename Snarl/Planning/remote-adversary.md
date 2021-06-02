# Protocol Changes
The first change made to the protocol is that clients may now identify themselves to the server.  Originally, the server sends a `server-welcome` message followed by `“name”`.  In our updated version, if a client responds to the `server-welcome` message with `player`, `ghost` or `zombie` within 10 seconds they will be registered as such.  If no type is sent, then the server assumes the client is a player and thus backwards compatibility is ensured.

The only other change made to the snarl protocol for the remote adversary task was a field called `anchor` off of a `player-update`.  Since an adversary may see the whole level they may not be at the center of the layout.  To compensate for this (and to avoid creating a massive square level with filler tiles just to have an adversary in the center), this anchor field was added and represents the upper left position of the layout.  If this field is included in a `player-update` then the actor is not assumed to be at the center.  Other than that the protocol was not modified.  Per the description, actors and objects are included in the JSON blob if they are within the field of view of the player/adversary, and since an adversary can see the whole level they get all this information.  If this anchor field is not included, the adversary will be at the center of the layout (just like a player) and backwards compatibility is ensured.

Example Remote Ghost Adversary:
```
MOVE REQUESTED
X X X X X X X X X X X X X X X
X       X X X X X X X       X
X   E   1               K   X
X   G Z X X X X X X X       X
X X X X X X X X X X X X X X X
consoleGhost you are at position (2, 3)
these are your move options:
0: 1 left
1: 1 up
2: none
3: 1 down

enter a move index: 
```
