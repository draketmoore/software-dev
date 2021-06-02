# SnarlServer3
To play the game simply run `./snarlServer3` with any of the arguments specified in milestone 9, except now `--clients` has been replaced with `--players`.  An additional argument, `--adversaries`, has been added to indicate the number of remote adversary clients that will connect to the game.  Our implementation runs in the terminal so no X session is required; the total output is for ascii characters.  If `--observe` is passed the server will output each updated gamestate, however no output (except errors) will be printed.

# SnarlClient3
To run the client simply run `./snarlClient3` with any of the arguments specified in milestone 9.  Our implementation runs in the terminal so no X session is required; the total output is for ascii characters.

There is a new optional field while running the executable, `--type`, followed by an option of `ghost`, `zombie`, or `player`. If this field is not included, the client defaults to connecting as a player. If more adversaries are needed than connected, their roles are filled by local instances.

Any player using the client will have to enter a unique, non-empty name.  The player will be depicted in the layout as the first character of the unique name, all other players will be represented as a single digit (0-9).

Any adversary client will have to enter a unique, non-empty name.  However, the adversary will always be depicted in the layout as a `Z` or a `G` if they are a zombie or ghost, respectively.  Players are still depicted as digits 0-9.

The client user must select a move 0-N from a valid list of moves presented when a move is requested.

Any time a player or adversary makes a move, the client will be updated and the resulting layout will be printed.  Once the client exits or is ejected from the level they will receive updates from their last valid location, but will not be requested for another move.  However, any adversary will not receive game state updates until they are requested to move.

At the end of the game each player and remote adversary will be updated with the final stats rankings of the game.  These stats don’t include any information about adversaries.

# AutoAdversaryClient
Contrary to `snarlClient3`, an adversary may play remotely with no user input by running `./autoAdversaryClient` which will utilize the adversary “AI” implemented in previous milestones.  One argument is required, `--type`, which is either `ghost` or `zombie`, which indicates what type of remote AI should be run.
