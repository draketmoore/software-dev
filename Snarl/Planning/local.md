<pre>
START UP COMMUNICATION
    Player                Game Framework
       |                        |
  join |----------------------->|
       |<-----------------------| join success/fail
       |                        |
       V                        V

GAMEPLAY (PROCESSING) COMMUNICATION
    Player                 Adversaries             Game Framework
       |                        |                        |
       |                        |<-----------------------| total level layout (to all)
       |<------------------------------------------------| players left (to all)
       |<------------------------------------------------| current room layout (to each)
       |                        |                        |
  move |------------------------------------------------>|
       |<------------------------------------------------| invalid/valid, tile interaction result
       |                        |                        |
       |<------------------------------------------------| level won? (to all)
       |                        |                        |
      ...      repeat moves for each player joined      ...
       |                        |                        |
       |                        |                        |
       |                   move |----------------------->|
       |                        |<-----------------------| invalid/valid, tile interaction result
       |                        |                        |
       |                       ...  for each adversary  ...
       |                        |                        |
       V                        V                        V

SHUTDOWN COMMUNICATION
    Player                Game Framework
       |                        |
       |<-----------------------| final game results, win/lose, score, time, etc...
       |                        |           (pending design updates)
       X                        X
</pre>
