#
# tile.py
# authors: Michael Curley & Drake Moore
#

from enum import Enum, unique


@unique
class Tile(Enum):
    """ represents a tile in a game """
    WALL = 0
    DOOR = 1
    EMPTY = 2
    HALLWAY = 3
    UNKNOWN = 4
    NONE = 5


    def generateLayoutOfSize(self, width: int, height: int) -> list:
        """ generates a layout of the given size entirely comprised of this tile
        type return value is list(list(Tile)) """
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError('A generated Tile layout must have integer dimensions.')
        if width < 0 or height < 0:
            raise ValueError('A generated Tile layout must have positive dimensions.')
        layout = list()
        for row in range(height):
            layout.append(list())
            for column in range(width):
                layout[row].append(self)
        return layout


    def asciiRender(self) -> chr:
        """ returns the ascii representation of this tile """
        return {
            Tile.WALL: 'X',
            Tile.DOOR: ' ',
            Tile.EMPTY: ' ',
            Tile.HALLWAY: ' ',
            Tile.UNKNOWN: '_',
            Tile.NONE: ' '
        }[self]


# ----- end of file ------------------------------------------------------------





