# SnarlServer
To play the game simply run `./snarlServer` with any of the arguments specified in the assignment.  Our implementation runs in the terminal so no X session is required; the total output is for ascii characters.  If `--observe` is passed the server will output each updated gamestate, however no output (except errors) will be printed.

# SnarlClient
To run the client simply run `./snarlClient` with any of the arguments specified in the assignment.  Our implementation runs in the terminal so no X session is required; the total output is for ascii characters.

The player using the client will have to enter a unique, non-empty name.  The player will be depicted in the layout as the first character of the unique name, all other players will be represented as a single digit (0-9).

The client player must select a move 0-N from a valid list of moves presented when a move is requested.

Any time a player or adversary makes a move, the client will be updated and the resulting layout will be printed.  Once the client exits or is ejected from the level they will receive updates from their last valid location, but will not be requested for another move.

At the end of the game each player will be updated with the final stats rankings of the game.

## Example start for 2 players, where the player names are `p{N}`:
```
$ ./snarlServer --clients 2

(Player 1)
$ ./snarlClient
Please enter your name: p1

(Player 2)
$ ./snarlClient
Please enter your name: p2

(Player 1)
UPDATED GAMESTATE
X X   1  
X X   E  
X X p    
X X X X X
X X X X X
--------------------------------------------------------------------------------

MOVE REQUESTED
X X   1  
X X   E  
X X p    
X X X X X
X X X X X
p1 you are at position (1, 3)
these are your move options:
0: 2 up
1: 1 up
2: none
3: 1 right, 1 up
4: 1 right
5: 2 right

enter a move index: 

(Player 2)
UPDATED GAMESTATE
X X X X X
X X X X X
X   p   X
X   E    
X 1     X
--------------------------------------------------------------------------------
```

The prompt indicates it is the turn for `p1` who should enter an integer between 0 and 8 (inclusive) to make their move.  If an invalid integer (out of range or just not an integer) is entered the prompt will be printed again.  The same format will follow for `p2` and `p3` until the game is over.  Interaction results are printed along the way after they occur.

### Clarifications:
All Zombies are "Z", all Ghosts are "G", the Key is "K" and the Exit is "E".

All walls and void tiles (outside rooms/halls) are represented by an "X".  The remaining tiles are traversable and represented by a space.

Our message format contains the same suggestions as in the assignment, however we added multiple messages that are separated by a comma. These are not seen in the output because we expect this format, however if used with other implementations a JSON message may be something like `Player drake collected the key,Player mike exited`.

Lastly, our implementation has a one second sleep after each time a message is expected to be received (on both client and server) to avoid race conditions for JSON strings being combined together.  This was intentional so as to make the JSON parsing simpler.
