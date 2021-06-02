#
# clientController.py
# authors: Michael Curley & Drake Moore
#

from actor import Actor, Player, Zombie, Ghost
from controller import Controller
from floorPlan import FloorPlan
from gameState import ActorGameState
from interactable import Interactable
from json import dumps, loads
from moveResult import MoveResult
from point import Point
from ruleChecker import RuleChecker
from snarlParser import SnarlParser, TILE_ID_MAP
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep


class ClientController:
    """ represents a client controller wrapper """

    def __init__(self, controller: Controller,
            address: str = '127.0.0.1', port: int = 45678,
            clientType = None):
        self.socket = None
        self.__validateController(controller)
        self.controller = controller
        self.__validateClient(clientType)
        self.clientType = clientType
        self.serverInfo, self.socket = self.__makeConnection(address, port)
        self.currentLevel = -1
        self.currentGameState = None
        self.isGameOver = False


    def __del__(self):
        try:
            if self.socket is not None:
                self.socket.close()
        except:
            pass


    def run(self):
        """ runs the main client loop """
        while 1:
            msg = self.__getMsg()
            if not self.processStringMessage(msg):
                if not self.processComplexMessage(msg):
                    raise RuntimeError(f'Server sent an unexpected state: {msg}')
                elif self.isGameOver:
                    break


    def processStringMessage(self, msg: str) -> bool:
        """ returns if a simple string message was processed """
        if msg == 'name':
            res = self.controller.getName()
            if self.clientType == 'ghost':
                self.actor = Ghost(res)
            elif self.clientType == 'zombie':
                self.actor = Zombie(res)
            else: # 'player' or None
                self.actor = Player(res[0] if len(res) > 0 else '0', res)
            self.__sendMsg(res)
        elif msg == 'move':
            move = self.controller.requestMove(self.currentGameState)
            self.__sendMsg({ 'type': 'move', 'to': SnarlParser().pointToJson(move) })
        elif msg in [mr.name for mr in MoveResult]:
            self.controller.updateMoveResult(MoveResult[msg])
        else:
            return False
        return True


    def processComplexMessage(self, msg: dict) -> bool:
        """ returns if a complex dictionary message was processed """
        if isinstance(msg, dict) and 'type' in msg.keys():
            t = msg['type']
            if t == 'start-level':
                self.currentLevel = msg['level']
            elif t == 'player-update':
                self.currentGameState = self.__recreateState(msg)
                self.controller.updateGameState(self.currentGameState)
            elif t == 'end-level':
                self.currentGameState.levelOver = True
                self.controller.updateGameState(self.currentGameState)
            elif t == 'end-game':
                self.controller.updateFinalStats(msg['scores'])
                self.isGameOver = True
            else:
                return False
            return True


    def __recreateState(self, state: dict) -> ActorGameState:
        """ recreates a game state from the partial json state """
        objs = self.__recreateObjects(state['objects'])
        actors = self.__recreateActors(state['actors'])
        self.actor.lifepoints = state.get('health', None)
        self.actor.location = SnarlParser().createPoint(state['position'])
        floorPlan = self.__recreateFloorPlan(state.get('anchor', None), state['layout'])
        for interactable in objs:
            self.__setTileOrActorInFloorPlan(objs[interactable], interactable, floorPlan)
        for actor in actors + [self.actor]:
            self.__setTileOrActorInFloorPlan(actor.location, actor, floorPlan)
        return ActorGameState(self.actor, actors, floorPlan,
                objs.get(Interactable.KEY, None), objs.get(Interactable.EXIT, None),
                False, False, False, False, RuleChecker(),
                currentLevel = self.currentLevel,
                messages = self.__separateMessages(state['message']))


    def __setTileOrActorInFloorPlan(self, location: Point, tileOrActor: any, floorPlan: FloorPlan):
        """ sets the tile or actor in the floor plan if it is within bounds """
        if floorPlan.tilePositionWithinBounds(location):
            if isinstance(tileOrActor, Actor):
                tileOrActor.replacedTile = floorPlan.getTileInLayout(location)
            floorPlan.setTileInLayout(location, tileOrActor)

    
    def __separateMessages(self, messages: str) -> list:
        """ returns a list of the messages """
        return None if messages is None or messages == '' else messages.split(',')


    def __recreateObjects(self, objects: list) -> dict:
        """ returns a dictionary of object locations by interactable key """
        return { Interactable.KEY if o['type'] == 'key' else Interactable.EXIT:
                 SnarlParser().createPoint(o['position']) for o in objects }


    def __recreateActors(self, actors: list) -> list:
        """ returns a list of actors from the json list """
        l = list()
        pids = '123456789'.replace(self.actor.identifier, '')
        for actor in actors:
            t = actor['type']
            name = actor['name']
            loc = SnarlParser().createPoint(actor['position'])
            if t == 'player':
                l.append(Player(pids[0], name, startLocation = loc))
                pids = pids[1:]
            else:
                l.append((Zombie if t == 'zombie' else Ghost)(name, startLocation = loc))
        return l


    def __recreateFloorPlan(self, anchor: list, layout: list) -> (Point, FloorPlan):
        """ recreates a floor plan from a partial json list """
        if anchor is None:
            anchor = self.actor.location -\
                    Point(int(len(layout[0]) / 2), int(len(layout) / 2))
        else:
            anchor = SnarlParser().createPoint(anchor)
        return FloorPlan(anchor, [ [ TILE_ID_MAP[tile] for tile in row ] for row in layout ])


    def __makeConnection(self, address: str, port: int) -> (str, socket):
        """ initiates connection and returns the server-info, socket """
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((address, port))
        welcome = self.__getMsg(s)
        if welcome['type'] != 'welcome':
            raise RuntimeError('Welcome message is invalid.')
        if self.clientType is not None:
            self.__sendMsg(self.clientType, s)
        return welcome['info'], s


    def __getMsg(self, s: socket = None) -> any:
        """ receives a json message from the server """
        sleep(1)
        return loads((self.socket if s is None else s).recv(4096).decode('utf-8'))


    def __sendMsg(self, msg: any, s: socket = None):
        """ sends a json message to the server """
        sleep(1)
        (self.socket if s is None else s).sendall(dumps(msg).encode('utf-8'))


    def __validateController(self, controller: any):
        """ raises value error if the given controller is invalid """
        if not isinstance(controller, Controller):
            raise ValueError('A ClientController must be given a valid controller.')


    def __validateClient(self, clientType: str):
        """ raises value error if the given string is invalid """
        if clientType not in ['player', 'ghost', 'zombie', None]:
            raise ValueError('A ClientController must be given a valid client type.')



# ----- end of file ------------------------------------------------------------





