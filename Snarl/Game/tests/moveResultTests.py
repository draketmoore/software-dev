#
# moveResultTests.py
# authors: Michael Curley & Drake Moore
#

from moveResult import MoveResult
from unittest import TestCase


class MoveResultTests(TestCase):
    """ tests for the MoveResult object """

    def testMoveResultBoolean_Success(self):
        self.assertTrue(MoveResult.OK)
        self.assertTrue(MoveResult.Key)
        self.assertTrue(MoveResult.Exit)
        self.assertTrue(MoveResult.Eject)
        # an invalid result should be redone
        self.assertFalse(MoveResult.Invalid)


# ----- end of file ------------------------------------------------------------





