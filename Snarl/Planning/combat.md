# Protocol Changes
The only thing added to the protocol is a field off of `player-update` called `health` which indicates to the player how much health they have left.  The protocol is backwards compatible, meaning this `health` field does not need to be included in a `player-update`, the client can accept a JSON blob whether it has health or not.  In the end, it is up to the server to manage the health and hitpoints of a Player/Adversary, so the client did not need any significant update.  Once any Player or Adversary is attacked and their health drops below zero, they are ejected in the same process as originally defined by the protocol. At the end of each level, all player’s hit points get reset to their max.

A `(result)` message now includes an `Attack` as a possible result of a move. The messages field for an `Attack` result is now updated with how many health points the defender has left. 
Ex: 

```
MOVE REQUESTED
X X X X X
X X X X X
X   p   X
    Z   X
X       X
player1 you are at position (12, 1)
you have 100 health left
... (player1 moves down 1)
--------------------------------------------------------------------------------

UPDATED GAMESTATE
Player player1 attacked Zombie zombie0 and reduced their health to 20
X X X X X
X X X X X
X   p   X
    Z   X
X       X
--------------------------------------------------------------------------------

UPDATED GAMESTATE
Zombie zombie0 attacked Player player1 and reduced their health to 85
X X X X X
X X X X X
X   p   X
    Z   X
X       X
--------------------------------------------------------------------------------

MOVE REQUESTED
X X X X X
X X X X X
X   p   X
    Z   X
X       X
player1 you are at position (12, 1)
you have 85 health left
... (player1 moves down 1)
--------------------------------------------------------------------------------

UPDATED GAMESTATE
Zombie zombie0 was expelled
X X X X X
X       X
    p   X
X       X
X X X X X
--------------------------------------------------------------------------------

MOVE REQUESTED
X X X X X
X       X
    p   X
X       X
X X X X X
player1 you are at position (12, 2)
you have 85 health left
```
As can be seen, the player and zombie were right next to each other and traded attacks bouncing back to the position from which they attacked. The relevant messages were displayed to indicate when any actor lost health points. Next, the player did a final attack of 30 points against the zombie’s health of 20 points, so the zombie got ejected from the level, and the player took the zombie’s position.
