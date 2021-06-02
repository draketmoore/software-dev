To: Manager\
From: Michael Curley & Drake Moore

<p>Our current adversary strategies are defined as follows: Ghosts and Zombies will both first locate the player closest to them. After locating the closest player, both types of Adversaries will move 1 step in the direction that will bring them closest to the player.</p>
<p>Because Zombies are unable to walk through doors (and hallways as a result), if the closest player is unreachable from its current position, the Zombie will move randomly until the player enters the Zombie’s current room.</p>
<p>Ghosts follow a similar strategy of moving in the general direction of the closest player. Although Ghost’s can traverse wall tiles, they will avoid them if possible.  If a Ghost cannot move any closer to the nearest player, it will attempt to move inside a wall to randomly teleport to a different room.  If no walls are reachable, the Ghost will randomly move in any direction.</p>


### Example where Zombie is outside the door where the player is standing
note: the player is denoted by a "1", the Zombie by "Z" and walls by "X"
```
X X X X X           X X X X X
X       X X X X X X X       X
X     Z 1                   X
X       X X X X X X X       X
X X X X X           X X X X X
```

<p>In the example above, the Player (shown by the character “1”), is standing on top of a door into the hallway. Because the door is not traversable by the Zombie, it will choose random moves in the directions up, down, or left, until the player enters the current room.</p>

### Example where Ghost would travel through a wall
note: the player is denoted by a "1", the Ghost by "G" and walls by "X"
```
  X X X X X
  X 1     X
  X       X
  X       X
  X X   X X
    X   X X X X X X
    X             X
X X X X X X X X   X
X                 X
X   X X X X X X X X
X   X                 X X X X X
X   X X X X X X X X X X G     X
X                             X
X X X X X X X X X X X X       X
                      X X X X X
```
<p> In the  example above, the Player is diagonally across a series of walls from the Ghost. As a result, the Ghost will travel into a wall to randomly teleport to a new location.</p>
