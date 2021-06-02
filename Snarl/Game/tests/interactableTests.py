#
# interactableTests.py
# authors: Michael Curley & Drake Moore
#

from interactable import Interactable
from unittest import TestCase


class InteractableTests(TestCase):
    """ tests for the Interactable enum """

    def testInteractableAsciiRender_Success(self):
        self.assertEqual('K', Interactable.KEY.asciiRender())
        self.assertEqual('E', Interactable.EXIT.asciiRender())


# ----- end of file ------------------------------------------------------------





