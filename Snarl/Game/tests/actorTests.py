#
# actorTests.py
# authors: Michael Curley & Drake Moore
#

from point import Point
from actor import Actor
from tile import Tile
from unittest import TestCase


class ActorTests(TestCase):
    """ Tests for Actors """

    def setUp(self):
        self.actor = Actor('A', 'actor')


    def testActorInit_Success(self):
        actor = Actor('A', 'actor', 1, 2, Point(0, 0), list())


    def testActorMove_Success(self):
        self.actor.move(Point(1, 1))
        self.assertEqual(Point(1, 1), self.actor.location)


    def testActorRender_Success(self):
        self.assertEqual('A', self.actor.asciiRender())


    def testActorIdentifier_ValueError(self):
        with self.assertRaises(ValueError):
            Actor('not one char', 'actor')
    
   
    def testActorMoveRange_ValueError(self):
        with self.assertRaises(ValueError):
            Actor('A', 'actor', 0)
        with self.assertRaises(ValueError):
            Actor('A', 'actor', 'range')


    def testActorTraversibleTiles_valueError(self):
        with self.assertRaises(ValueError):
            Actor('A', 'actor',
                    traversableTiles = [Tile.EMPTY, 'FakeTile', Tile.HALLWAY])


# ----- end of file ------------------------------------------------------------





