#
# moveResult.py
# authors: Michael Curley & Drake Moore
#

from enum import Enum, unique

@unique
class MoveResult(Enum):
    """ represents the result of a move specific to a player """
    OK = 1
    Key = 2
    Exit = 3
    Eject = 4
    Invalid = 5
    Attack = 6

    def __bool__(self) -> bool:
        return self != MoveResult.Invalid


# ----- end of file ------------------------------------------------------------





