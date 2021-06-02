# SnarlServer2
To play the game simply run `./snarlServer2` with any of the arguments specified in milestone 9.  Our implementation runs in the terminal so no X session is required; the total output is for ascii characters.  If `--observe` is passed the server will output each updated gamestate, however no output (except errors) will be printed.

# SnarlClient2
To run the client simply run `./snarlClient2` with any of the arguments specified in milestone 9.  Our implementation runs in the terminal so no X session is required; the total output is for ascii characters.

The player using the client will have to enter a unique, non-empty name.  The player will be depicted in the layout as the first character of the unique name, all other players will be represented as a single digit (0-9).

The client player must select a move 0-N from a valid list of moves presented when a move is requested.

Any time a player or adversary makes a move, the client will be updated and the resulting layout will be printed.  Once the client exits or is ejected from the level they will receive updates from their last valid location, but will not be requested for another move.

At the end of the game each player will be updated with the final stats rankings of the game.

# Combat System
Players and adversaries are spawned with a predetermined amount of attack points and health points.  Players attack with 30 points and have 100 health points because we don’t want them to die as easily.  Ghosts attack with 10 points because they can teleport which makes them more powerful than zombies.  Zombies attack with 15 points because they are trapped in only one room.  Both zombies and ghosts have 50 health points, making them an easier target for the player to kill.  We decided to make the adversaries less powerful since they have a full level view which gives them a big advantage over any player. 

A player or adversary makes an attack by moving onto a tile occupied by the opponent. If the attack does not result in the defending party dying, the attacker is moved back to the tile from which they started the attack. If the defender is killed as a result of the attack, the defender is expelled and the attacker is moved onto the defender’s tile. At the end of each level, all player’s hit points get reset to their max.
