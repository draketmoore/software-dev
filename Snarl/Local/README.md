# LocalSnarl
To play the game simply run `./localSnarl` with any of the arguments specified in the assignment.  Our implementation runs in the terminal so no X session is required; the total output is for ascii characters.

Upon start of the game, each player will have to enter a unique, non-empty name.  The first player will be depicted as a “1” in the ascii output, the second player will be “2” and so on.  Each player must select a move 0-N from a valid list of moves presented when each player should move.

Any time a player has an interaction (key collected, exited or expelled) the player will be updated and the resulting layout will be printed.  Once a player exits or is expelled from the game they will no longer have console print outs (they still receive GameState updates, we just decided to not print them since it makes things harder to follow).

At the end of the game each player will be updated with the final stats rankings of the game, if there are three players these rankings will be printed three times, each preceded by the player’s name to indicate which player the rankings were sent to.

Should the `--observe` flag be set, only one player may play in the game.  An observer receives an update after every move, including after adversary moves, so the observer printed layout updates are far more frequent than the players (since player layouts are only printed on their turn).

## Example start for 3 players starting on level 2, where the player names are `p{N}`:
```
$ ./localSnarl --players 3 --start 2
player 1 enter a name: p1
player 2 enter a name: p2
player 3 enter a name: p3

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _   X   X
_ _ _ _ _ _ _ _ _ _ _ _ _ X X   X X
_ _ _ _ _ _ _ _ _ _ _ _ _ X   1   X
_ _ _ _ _ _ _ _ _ _ _ _ _ X   Z   X
_ _ _ _ _ _ _ _ _ _ _ _ _ X     E X
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
p1 you are at position (16, 5)
the exit is LOCKED
the following actors are ejected:

the following actors have exited:

please enter a move number from the following:
0: 1 left
1: 1 left, 1 down
2: 2 up
3: 1 up
4: none
5: 1 down
6: 2 down
7: 1 right
8: 1 right, 1 down
```
The prompt indicates it is the turn for `p1` who should enter an integer between 0 and 8 (inclusive) to make their move.  If an invalid integer (out of range or just not an integer) is entered the prompt will be printed again.  The same format will follow for `p2` and `p3` until the game is over.  Interaction results are printed along the way after they occur.

### Clarifications:
Players are represented in the game by their number (player one == "1"), all Zombies are "Z", all Ghosts are "G", the Key is "K" and the Exit is "E".

All walls are represented by an "X".  The remaining tiles are a mix of EMPTY, DOOR, HALLWAY and NONE (void, outside rooms/halls), however these are displayed as a space character to make the output look simpler.

All tiles outside a player's field of view are replaced by an UNKNOWN tile, represented by "\_" (shown in the above example).

### Side Note:
When a Ghost makes a move into a wall it will randomly teleport to a free tile in a random room.  This allows the possibility that the Ghost teleports back to the original tile (prior to moving inside the wall).  Since this interaction is processed before any other game states are produced, there will be no output to make it look like the Ghost made a move.  The chances of this happeneing are very slim, however we wanted to be sure all user's are aware of this interesting case.
