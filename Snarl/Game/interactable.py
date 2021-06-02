#
# interactable.py
# authors: Michael Curley & Drake Moore
#

from enum import Enum, unique


@unique
class Interactable(Enum):
    """ represents an interactable item in the game """
    KEY = 0
    EXIT = 1


    def asciiRender(self) -> chr:
        """ returns the ascii representation of this interactable """
        return {
            Interactable.KEY: 'K',
            Interactable.EXIT: 'E'
        }[self]


# ----- end of file ------------------------------------------------------------





