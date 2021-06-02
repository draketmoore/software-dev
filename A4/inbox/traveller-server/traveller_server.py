#!/usr/bin/env python3

existingPlayers = []
existingTowns = []

class Player:
    """
    Represents a player in the game that may travel between different Towns
    
    Args:
        name (string): the name of the Player
        currentTown (Town): the current Town the Player is residing in
    """
    def __init__(self, name, town):
        self.name = name
        self.town = town
        town.currentPlayers.append(self)
        existingPlayers.append(name)

class Town:
    """
    Represents a town to which a player may travel to or from or presently exist in

    Args:
        name (string): the name of the town
        currentPlayers: ([Player]): the current players present in this Town
        connectedTowns: ([Town]): the towns adjacent to this Town
    """
    def __init__(self, name, connectedTowns):
        self.name = name
        self.currentPlayers = []
        self.connectedTowns = connectedTowns
        existingTowns.append(name)

def Create_Town(name, connectedTowns):
    """
    Creates a new town in a given network of towns

    Args:
        name (string): the name of the town to be created
        connectedTowns ([Town]): the adjacent towns to this Town

    Raises:
        Exception: if a town with this name already exists, throw an exception

    Returns:
        Town: the newly created Town
    """
    for t in existingTowns:
        if t == name:
            raise Exception("Town with this name already exists")
    newTown = Town(name, connectedTowns)
    if connectedTowns != [None]:
        for t in connectedTowns:
            t.connectedTowns.append(newTown)
    return newTown

def Place_Player(player, destination):
    """
    Removes player from current town, and places him in a new town

    Args:
        player (Player): the Player to be placed
        destination (Town): the Town where the Player will be placed
    """
    currentTown = player.town
    currentTown.currentPlayers.remove(player)
    destination.currentPlayers.append(player)
    player.town = destination

# list_1 = connectedTowns, list_2 = visited towns
def diff(list_1, list_2):
    """
    Find the difference between list_1 and list_2

    Args:
        list_1 (List): the first list
        list_2 (List): the second list

    Returns:
        List: items in list_1, but not in list_2
    """
    list_dif = [i for i in list_1 if i not in list_2]
    return list_dif

def path_find(current, destination, visited):
    """
    Determine if there is a path between the current town and destination town

    Args:
        current (Town): the starting point of the path
        destination (Town): the end point of the path
        visited ([Town]): the Towns visited while finding a path

    Returns:
        (bool): True if path exists, False otherwise
    """
    if destination in current.connectedTowns:
        return True
    else:
        town_list = diff(current.connectedTowns, visited)
        # print("\n\n")
        # for i in list_dif:
        #     print(i.name)
        if not town_list:
            return False
        visited.append(current)
        for town in town_list:
            if town.currentPlayers:
                visited.append(town)
            return False or path_find(town, destination, visited)

def Path_Query(player, destination):
    """
    Query a path an determine if it is traversable for the Player

    Args:
        player (Player): the player to move to the destination
        destination ([type]): the endpoint of the path

    Returns:
        [type]: [description]
    """
    if destination.currentPlayers:
        return False
    currentTown = player.town 
    return path_find(currentTown, destination, [])


def main():
    """
    Used for testing purposes
    """
    nyc = Create_Town("NYC", [])
    bos = Create_Town("Boston", [nyc])
    chi = Create_Town("Chicago", [bos])
    sf = Create_Town("San Francisco", [chi])
    la = Create_Town("Los Angeles", [sf])
    john = Player("John", la)
    michael = Player("Michael", bos)
    sarah = Player("Sarah", sf)

    #########################################
    #              Simple Tests             #
    # - Change Players/Towns before testing # 
    #########################################


    # Testing path with multiple hops to final destination
    print('Path for John to NYC?')
    print(Path_Query(john, la))
    # Testing path with Player at final destination
    print('Path for John to BOS?')
    print(Path_Query(john, bos))
    # Testing path with Player at intermediate destination
    print('Path for John to SF?')
    print(Path_Query(john, sf))
    # Testing bidirectionality of paths
    print('Path for Michael to NYC?')
    print(Path_Query(michael, nyc))
    
main()