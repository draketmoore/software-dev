#
# serverController.py
# authors: Michael Curley & Drake Moore
#

from actor import Actor, Adversary
from controller import Controller
from gameState import ActorGameState, GameState
from interactable import Interactable
from json import dumps, loads
from moveResult import MoveResult
from point import Point
from snarlDisconnectError import SnarlDisconnectError
from snarlParser import SnarlParser, ID_TILE_MAP
from tile import Tile
from time import sleep


class ServerController(Controller):
    """ represents a controller that manages a tcp connection to a ClientController """

    def __init__(self, connection, useLayoutAnchor: bool = False):
        self.connection = connection
        self.useAnchor = useLayoutAnchor

    def __copy__(self):
        return None

    def __deepcopy__(self, memo):
        return None

    def __del__(self):
        try:
            if self.connection is not None:
                self.connection.close()
        except:
            pass

    def sendMsg(self, msg: any):
        """ sends any json object over the connection, rasies SnarlDisconnectError """
        try:
            if self.connection is not None:
                sleep(1)
                self.connection.sendall(dumps(msg).encode())
        except Exception as e:
            self.connection = None
            raise SnarlDisconnectError(str(e))

    def recvMsg(self) -> any:
        """ receives any json object over the connection, rasies SnarlDisconnectError """
        try:
            if self.connection is None:
                raise RuntimeError('trying to receive data over a broken connection')
            sleep(1)
            return loads(self.connection.recv(1024).decode())
        except Exception as e:
            self.connection = None
            raise SnarlDisconnectError(str(e))

    def updateGameState(self, gameState: ActorGameState):
        """ generates a player-update or an end level message"""
        if gameState.levelOver:
            updateMessage = self.generateEndLevelMessage(gameState)
        else:
            objects, actors = self.getObjectsAndActors(gameState)
            updateMessage = {
                'type': 'player-update',
                'layout': self.getLayout(gameState),
                'position': self.getPosition(gameState),
                'objects': objects,
                'actors': actors,
                'message': None if gameState.messages is None else ','.join(gameState.messages)
            }
            actor = gameState.actor
            if actor.lifepoints is not None:
                updateMessage['health'] = actor.lifepoints
            if self.useAnchor:
                updateMessage['anchor'] = self.getAnchor(gameState)
        self.sendMsg(updateMessage)

    def generateEndLevelMessage(self, gameState: ActorGameState):
        """ generates the end-level message """
        key = None
        for x in [a.name for a in gameState.allActors if a.collectedKey]:
            key = x
        return {
            'type': 'end-level',
            'key': key,
            'exits': [a.name for a in gameState.allActors if a.exited],
            'ejects': [a.name for a in gameState.allActors if a.expelled]
        }

    def requestMove(self, gameState: GameState) -> Point:
        """ sends the move request to the player"""
        # adversaries don't receive regular updates, update prior to asking for move
        if isinstance(gameState.actor, Adversary):
            self.updateGameState(gameState)
        self.sendMsg('move')
        return SnarlParser().createPoint(self.recvMsg()['to'])

    def updateMoveResult(self, moveResult: MoveResult):
        """ sends the move result to the player"""
        self.sendMsg(moveResult.name)

    def updateFinalStats(self, finalStats: list):
        """ sends the final stats over the connection """
        for stat in finalStats:
            stat['type'] = 'player-score'
        self.sendMsg({ 'type': 'end-game',
                       'scores': finalStats })

    def getAnchor(self, gameState) -> list:
        """ returns the json upper left position of the layout """
        return SnarlParser().pointToJson(gameState.floorPlan.upperLeftPosition)

    def getLayout(self, gameState) -> list:
        """ returns the layout replaced by tile id's """
        if self.useAnchor:
            return [ [
                ID_TILE_MAP[tile.replacedTile if isinstance(tile, Actor) else tile]
                    for tile in row ]
            for row in gameState.floorPlan.layout ]
        return self.getNonAnchoredLayout(gameState)

    def getNonAnchoredLayout(self, gameState) -> list:
        """ returns a relative layout based on the actor's fov """
        layout = list()
        knownLayout = gameState.getKnownLayout()
        actorLoc = self.__getRelativeActorLocationInKnownLayout(gameState)
        for row in range(len(knownLayout)):
            layout.append(list())
            for col in range(len(knownLayout[row])):
                tile = knownLayout[row][col]
                if isinstance(tile, Actor):
                    layout[row].append(ID_TILE_MAP[tile.replacedTile])
                else:
                    layout[row].append(ID_TILE_MAP[tile])
        return self.__squareLayout(layout, actorLoc, gameState.actor.viewRadius)

    def __getRelativeActorLocationInKnownLayout(self, gameState) -> Point:
        """ based on a variable size known layout, returns the relative actor location """
        actor = gameState.actor
        vr = actor.moveRange
        loc = actor.location
        ul = gameState.floorPlan.upperLeftPosition
        # relative indexing only depends on upper left position
        return Point(min(vr, loc.X - ul.X), min(vr, loc.Y - ul.Y))

    def __squareLayout(self, layout, loc, center) -> list:
        """ given a known layout, if it is at a border then the layout will not
        be a square, method adds WALL tiles to edges until it is square """
        size = (center * 2) + 1
        for _ in range(center - loc.X):
            for row in layout:
                row.insert(0, ID_TILE_MAP[Tile.WALL])
        while len(layout[0]) < size:
            for row in layout:
                row.append(ID_TILE_MAP[Tile.WALL])
        for _ in range(center - loc.Y):
            layout.insert(0, self.__createVoidRowOfSize(size))
        while len(layout) < size:
            layout.append(self.__createVoidRowOfSize(size))
        return layout

    def __createVoidRowOfSize(self, size) -> list:
        """ returns a row size elements long of void tiles """
        row = list()
        for i in range(size):
            row.append(ID_TILE_MAP[Tile.WALL])
        return row

    def getPosition(self, gameState) -> list:
        """ returns the actor position in json form for the update message """
        return SnarlParser().pointToJson(gameState.actor.location)

    def getObjectsAndActors(self, gameState: ActorGameState) -> (list, list):
        """ returns a tuple of objects json list and actors json list for the update message """
        objects = list()
        actors = list()
        floorPlan = gameState.floorPlan
        anchor = floorPlan.upperLeftPosition
        for col in range(floorPlan.width):
            for row in range(gameState.floorPlan.height):
                loc = anchor + Point(col, row)
                pos = SnarlParser().pointToJson(loc)
                tile = floorPlan.getTileInLayout(loc)
                if isinstance(tile, Actor):
                    actor = tile
                    tile = actor.replacedTile
                    if gameState.actor.location != loc:
                        actors.append({
                            'type': actor.__class__.__name__.lower(),
                            'name': actor.name,
                            'position': pos
                        })
                if isinstance(tile, Interactable):
                    objects.append({
                        'type': 'key' if tile == Interactable.KEY else 'exit',
                        'position': pos
                    })
        return objects, actors



# ----- end of file ------------------------------------------------------------





