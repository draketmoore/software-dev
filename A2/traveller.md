Traveller Module\
Description for Python 3.6.8\
Authors: Drake Moore & Michael Curley

# Data Definitions
// Represents a player in the game that may travel between different Towns\
class Player:\
    @static List(String) - existingPlayers // a list of all existing player names\
    String - name // the name of the Player\
    Town - currentTown // the current Town the Player is residing in

// Represents a town to which a player may travel to or from or presently exist in\
class Town:\
    @static List(String) - existingTowns // a list of all existing town names\
    String - name // the name of the town\
    List(Player) - currentPlayers // the current players present in this Town\
    List(Town) - connectedTowns // the towns adjacent to this Town


# Api Functions
// Creates a new town in a given network of towns\
// PRE: town with given name does not exist\
// POST: each connected town has a reference to the new town in their connectedTowns field\
def Create_Town (String name, List(Town) connectedTowns) -> Town

// Removes player from current town, and places him in a new town\
// POST: Player’s currentTown is updated to destination. Destination’s currentPlayers list is updated with added Player. Player’s currentTown removes player from the list of current players.\
def Place_Player (Player player, Town destination) -> None

// Checks available paths to the target town, and returns whether it is reachable without encountering another player\
// PRE: Player and destination must both exist\
// POST: Player’s currentTown is unchanged\
def Path_Query (Player player, Town destination) -> Boolean
 

