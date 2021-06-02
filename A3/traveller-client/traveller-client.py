#!/usr/bin/env python3
#
# traveller-client.py
# authors: Michael Curley & Drake Moore
# NOTE: this will not run until traveller module is completed
#

from json import loads as strToJson
from shlex import split as whitespaceSplit
from sys import argv, stdin
import traveller

# globals (constants)
COMMAND_KEY = 'command'
PARAMS_KEY = 'params'
ROADS_COMMAND = 'roads'
ROADS_FROM_TOWN_KEY = 'from'
ROADS_TO_TOWN_KEY = 'to'
PLACE_COMMAND = 'place'
PASSAGE_SAFE_COMMAND = 'passage-safe?'
CHARACTER_KEY = 'character'
TOWN_KEY = 'town'


# ----- main -------------------------------------------------------------------

# client implementation of the traveller warmup assignment task 3 for cs4500
def main(): 
    # get all standard input until EOF, parse input to json strings
    inputStr = stdin.read()
    jsonStrings = parseToJsonStrings(inputStr)

    # iterate over all json strings and print the formatted total json objects
    towns = list()
    players = list()
    firstCommand = True
    for jsonStr in jsonStrings:
        # try to pull out the json command object from the string
        try:
            jsonCommand = strToJson(jsonStr)
        except Exception as e:
            print('Error: json input could not be parsed to a valid object', e)
            break
        # for an unexpected json value shutdown
        if not isinstance(jsonCommand, dict):
            print('Error: unexepected json type encountered:', type(jsonCommand))
            break
        
        # make sure valid command is given
        command = jsonCommand.get(COMMAND_KEY, None)
        params = jsonCommand.get(PARAMS_KEY, None)
        if command is not None and params is not None:
            try:
                # first command must be a ROADS command, if not shutdown
                if firstCommand:
                    if command != ROADS_COMMAND:
                        print('Error: first command must be of type "roads"')
                        break
                    towns, msg = executeRoadsCommand(params)
                    firstCommand = False
                    print(msg)
                
                # only the first command can be roads
                elif command == ROADS_COMMAND:
                    print('Error: only the first command can be of type "roads"')
                
                # execute place command
                elif command == PLACE_COMMAND:
                    print(executePlaceCommand(towns, players, params))

                # execute passage safe command
                elif command == PASSAGE_SAFE_COMMAND:
                    print(executePassageSafeCommand(towns, players, params))

            # on error, shutdown but print the exception
            except Exception as e:
                print('Error executing command:', e)


# ----- town network functions -------------------------------------------------

# generic function, returns the object from the given list of based on the given
# string name (may be used on any list of objects containing a 'name' field)
def getObjectByName(name, objs):
    for obj in objs:
        if name == obj.name:
            return obj
    return None

# returns a list of Town objects created by the indicated params
# params must be a list of dictionaries, each dictionary must have the fields:
#   from: Town name
#   to: Town name
def executeRoadsCommand(params):
    global ROADS_FROM_TOWN_KEY, ROADS_TO_TOWN_KEY
    
    # assemble a dictionary of connected towns by string names
    connectedTownsInput = dict()
    for fromToCommand in params:
        fromTownName = fromToCommand[ROADS_FROM_TOWN_KEY]
        toTownName = fromToCommand[ROADS_TO_TOWN_KEY]
        if fromTownName not in connectedTownsInput.keys():
            connectedTownsInput[fromTownName] = set()
        if toTownName not in connectedTownsInput.keys():
            connectedTownsInput[toTownName] = set()
        connectedTownsInput[fromTownName].add(toTownName)
        connectedTownsInput[toTownName].add(fromTownName)

    # since town creation (per the API) requires objects returned by the API, we
    # must create towns with the least number of connected towns first, this
    # ensures the simple data is created prior to the more complex connections
    towns = list()
    creationOrder = sorted(list(connectedTownsInput.keys()),
            key=lambda townName: len(connectedTownsInput[townName]))
    for townName in creationOrder:
        # get all connected town objects that have already been created
        connectedTownObjects = list(
                filter(lambda town: town is not None,
                    map(lambda name: getObjectByName(name, towns),
                        connectedTownsInput[townName])))
        towns.append(traveller.Create_Town(townName, connectedTownObjects))
    return towns, 'Towns Created: {0}'.format(towns)

# executes place command given a valid list of Town and Player objects
# params must be a dictionary with the following keys
#   character: Player name (will be created if not exists)
#   town: Town name (must exist)
# the players list will be updated to contain the new Player if created
def executePlaceCommand(towns, players, params):
    global CHARACTER_KEY, TOWN_KEY

    # pull out the string names and try to get the corresponding objects
    playerName = params[CHARACTER_KEY]
    townName = params[TOWN_KEY]
    playerObj = getObjectByName(playerName, players)
    townObj = getObjectByName(townName, towns)

    # ignores command if town does not exist
    if townObj is None:
        return 'Error: town must exist before a player can be placed'

    # if player does not exist, create new player and add it to player list
    if playerObj is None:
        # NOTE: pending implementation details, will update once constructor is
        #       known for the Player object, assuming that the player is created
        #       only with its own name
        playerObj = traveller.Player(playerName)

    # player and town are valid, place the plaer in the town
    traveller.Place_Player(playerObj, townObj)
    return 'Player {0} placed in {1}'.format(playerName, townName)

# executes a passage safe command given a valid list of Town and Player objects
# params must be a dictionary with the following keys
#   character: Player name (must exist)
#   town: Town name (must exist)
def executePassageSafeCommand(towns, players, params):
    global CHARACTER_KEY, TOWN_KEY
    
    # pull out the string names and try to get the corresponding objects
    playerName = params[CHARACTER_KEY]
    townName = params[TOWN_KEY]
    playerObj = getOBjectByName(playerName, players)
    townObj = getObjectByName(townName, towns)

    # ignore command if town or player do not exist
    if playerObj is None or townObj is None:
        return 'Error: player and town must both exist to determine safe passage'
    
    safePassage = traveller.Path_Query(playerObj, townObj)
    return 'Player {0} can travel to {1}: {2}'.format(
            playerName, townName, safePassage)


# ----- json parsing functions -------------------------------------------------

# parses the inputStr (json objects delimited by whitespace) to a list of well
# formed json strings
def parseToJsonStrings(inputStr):
    curJson = ''
    strings = list()
    splitList = whitespaceSplit(inputStr, posix = False)
    for s in splitList:
        curJson += s
        # attempt to convert the string to a json object, if it fails try with
        # the next string appended
        try:
            blob = strToJson(curJson)
            strings.append(curJson)
            curJson = ''
        except:
            pass
    return strings



# ----- linux entry ------------------------------------------------------------

if __name__ == '__main__':
    main()


# ----- end of file ------------------------------------------------------------
