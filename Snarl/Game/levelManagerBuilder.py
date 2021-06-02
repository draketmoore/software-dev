#
# levelManagerBuilder.py
# authors: Michael Curley & Drake Moore
#

from actor import Player, Ghost, Zombie
from consoleController import ConsoleController
from controller import Controller, LocalGhostController, LocalZombieController
from copy import deepcopy
from floorPlan import FloorPlan
from gameState import GameState
from levelManager import LevelManager
from hallway import Hallway
from interactable import Interactable
from level import Level
from tile import Tile
from point import Point
from random import randint
from room import Room
from ruleChecker import RuleChecker
from observer import Observer


class LevelManagerBuilder:
    """ represents a builder object to construct a game manager from a level
    (or level components), players and adversaries """

    # produces an adversary object from a string
    AdversaryGeneratorMap = {
        'ghost': (lambda name, controller, hitpoints, lifepoints:
            Ghost(name, controller = controller, hitpoints = hitpoints, lifepoints = lifepoints)),
        'zombie': (lambda name, controller, hitpoints, lifepoints:
            Zombie(name, controller = controller, hitpoints = hitpoints, lifepoints = lifepoints)),
    }
    AdversaryControllerGeneratorMap = {
        'ghost': (lambda: LocalGhostController()),
        'zombie': (lambda: LocalZombieController())
    }

    def __init__(self):
        self.__clearLocals()


    def registerPlayer(self, playerId: str, playerName: str,
            location: Point = None, controller: Controller = None,
            hitpoints = None, lifepoints = None):
        """ registers a unique player to the game """
        self.__ensureType(playerId, str, 'Player id')
        self.__ensureName(playerId, 'Player id')
        self.__ensureType(playerName, str, 'Player name')
        self.__ensureName(playerName, 'Player name')
        self.__ensureType(location, Point, 'Player location')
        self.__ensureType(controller, Controller, 'Player controller')
        if playerId in self.playerIds or playerName in self.names:
            raise ValueError('A duplicate player was added.')
        self.playerIds.add(playerId)
        self.names.add(playerName)
        if controller is None:
            controller = ConsoleController()
        self.players.append(Player(playerId, playerName, controller = controller,
            hitpoints = hitpoints, lifepoints = lifepoints))
        if location is not None:
            self.addPlayerStartingPoint(location)
        return self


    def registerAdversary(self, adversaryType: str, adversaryName: str,
            location: Point = None, controller: Controller = None,
            hitpoints = None, lifepoints = None):
        """ registers a unique adversary to the game, an adversary may be a
        ghots or zombie """
        self.__ensureType(adversaryName, str, 'Adversary name')
        self.__ensureName(adversaryName, 'Adversary name')
        self.__ensureType(location, Point, 'Adversary location')
        self.__ensureType(controller, Controller, 'Adversary controller')
        if adversaryName in self.names:
            raise ValueError('A duplicate adversary was added.')
        adversaryCreator = self.AdversaryGeneratorMap.get(adversaryType, None)
        if adversaryCreator is None:
            raise ValueError('An unknonwn adversary type was given.')
        self.names.add(adversaryName)
        if controller is None:
            controller = self.AdversaryControllerGeneratorMap[adversaryType]()
        self.adversaries.append(adversaryCreator(adversaryName, controller,
            hitpoints, lifepoints))
        if location is not None:
            self.addAdversaryStartingPoint(location)
        return self


    def registerObserver(self, observerName: str, controller: Controller = None):
        """ registers an observer into the game. """
        self.__ensureType(observerName, str, 'Observer name')
        self.__ensureName(observerName, 'Observer name')
        if observerName in self.names:
            raise ValueError('A duplicate observer was added.')
        self.__ensureType(controller, Controller, 'Observer controller')
        self.names.add(observerName)
        self.observers.append(Observer(observerName, controller)) 
        return self


    def addLevelComponent(self, floorPlan: FloorPlan):
        """ adds a level component to the builder, this may be a hallway,
        room or level, if a level is given that will be used regardless if
        any rooms or hallways are also added """
        self.__ensureType(floorPlan, FloorPlan, 'Level component')
        if isinstance(floorPlan, Level):
            self.level = floorPlan
        elif isinstance(floorPlan, Room):
            self.rooms.append(floorPlan)
        elif isinstance(floorPlan, Hallway):
            self.hallways.append(floorPlan)
        return self


    def addPlayerStartingPoint(self, point: Point):
        """ adds a potential player starting point """
        self.__ensureType(point, Point, 'Player starting point')
        self.playerStartingPoints.append(point)
        return self


    def addAdversaryStartingPoint(self, point: Point):
        """ adds a potential adversary starting point """
        self.__ensureType(point, Point, 'Adversary starting point')
        self.adversaryStartingPoints.append(point)
        return self


    def setKeyLocation(self, keyLocation: Point):
        """ sets the key location for the game """
        self.__ensureType(keyLocation, Point, 'Key location')
        self.keyLocation = keyLocation
        return self


    def setExitLocation(self, exitLocation: Point):
        """ sets the exit location for the game """
        self.__ensureType(exitLocation, Point, 'Exit location')
        self.exitLocation = exitLocation
        return self


    def setKeyCollected(self, keyCollected: bool):
        """ sets if the key has been collected yet """
        self.__ensureType(keyCollected, bool, 'Key collected status')
        self.keyCollected = keyCollected
        return self


    def setRuleChecker(self, ruleChecker: RuleChecker):
        """ sets the rule checker for the game """
        self.__ensureType(ruleChecker, RuleChecker, 'Rule checker')
        self.ruleChecker = ruleChecker
        return self


    def setRandomStartingPoints(self, randomStartingPoints: bool):
        """ sets if random starting points will be used """
        self.__ensureType(randomStartingPoints, bool, 'Random starting points')
        self.randomStartingPoints = randomStartingPoints
        return self


    def build(self):
        """ builds the game from the set components """
        if self.level is None:
            self.level = Level(self.rooms, self.hallways)
        # append default starting points in case not enough were given
        invalidPoints = [self.keyLocation, self.exitLocation]
        if self.randomStartingPoints:
            rooms = self.level.rooms
            self.__setRandomStartingPoints(self.playerStartingPoints,
                    invalidPoints, rooms, len(self.players))
            self.__setRandomStartingPoints(self.adversaryStartingPoints,
                    invalidPoints, rooms, len(self.adversaries))

        else:
            defPlayerPoints, defAdversaryPoints = self.level.getPlayerAndAdversaryStartingPoints(
                    invalidPoints)
            self.playerStartingPoints += defPlayerPoints
            self.adversaryStartingPoints += defAdversaryPoints
        gm = LevelManager(self.level, self.players, self.adversaries,
                self.__distinct(self.playerStartingPoints),
                self.__distinct(self.adversaryStartingPoints),
                self.keyLocation, self.exitLocation, self.keyCollected,
                self.ruleChecker, self.observers)
        self.__clearLocals()
        return gm


    def __clearLocals(self):
        """ sets all local fields to their empty default values """
        self.players = list()
        self.adversaries = list()
        self.observers = list()
        self.playerStartingPoints = list()
        self.adversaryStartingPoints = list()
        self.randomStartingPoints = False
        self.rooms = list()
        self.hallways = list()
        self.level = None
        self.keyLocation = None
        self.exitLocation = None
        self.keyCollected = False
        self.ruleChecker = None
        self.playerIds = set()
        self.names = set()


    def __setRandomStartingPoints(self, outputList: list, invalidPoints: list,
            rooms: list, count: int):
        """ adds random points in rooms to the output list count times """
        outputList.clear()
        emptyPoints = list()
        for room in rooms:
            emptyPoints += room.getTraversablePointsInLayout([Tile.EMPTY])
        for _ in range(count):
            while 1:
                p = emptyPoints.pop(randint(0, len(emptyPoints) - 1))
                if p not in invalidPoints:
                    break
            invalidPoints.append(p)
            outputList.append(p)


    def __distinct(self, l: list):
        """ removes duplicates from the list while maintaining the order """
        r = list()
        for e in l:
            if e not in r:
                r.append(e)
        return r


    def __ensureName(self, name: str, nameType: str):
        """ raises value error if the name is empty """
        if name is None or name == '' or name.isspace():
            raise ValueError('{0} cannot be empty.'.format(nameType))


    def __ensureType(self, o: object, t: type, name: str):
        """ raises a value error if the given object is of the wrong type """
        if o is not None and not isinstance(o, t):
            raise ValueError('{0} must be of type {1}.'.format(name, str(t)))



# ----- end of file ------------------------------------------------------------





