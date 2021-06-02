#
# floorPlan.py
# authors: Michael Curley & Drake Moore
#

from copy import deepcopy
from interactable import Interactable
from point import Point
from random import randint
from tile import Tile


class FloorPlan:
    """ represents a floor plan for any room/hallway within a level, a floor
    plan has an anchor coordinate point in the upper left and a layout for the
    room """
    
    def __init__(self, upperLeftPosition: Point, layout: list):
        """ the layout is a list(list(Tile)), every sublist of the main list
        must be the same length """
        self.__validateUpperLeftPosition(upperLeftPosition)
        self.__validateLayout(layout)
        self.layout = layout
        self.height = len(layout)
        self.width = len(layout[0])
        self.upperLeftPosition = upperLeftPosition
        self.lowerRightPosition = (upperLeftPosition +
                Point(self.width, self.height) - Point(1, 1))
    

    def getTraversablePointsInLayout(self, traversableTiles: list,
            layout: list = None) -> list:
        """ returns a list of the traversable point locations in the floor plan
        layout based on the givne list of traversableTiles, which is a list of
        Tile or Interactable """
        layout = self.layout if layout is None else layout
        traversablePoints = list()
        for row in range(self.height):
            for col in range(self.width):
                if layout[row][col] in traversableTiles:
                    traversablePoints.append(Point(col, row) + self.upperLeftPosition)
        return traversablePoints


    def getRandomTraversablePointInLayout(self, traversableTiles: list,
            layout: list = None) -> Point:
        """ returns a random traversable point in the layout """
        traversablePoints = self.getTraversablePointsInLayout(traversableTiles, layout)
        return traversablePoints[randint(0, len(traversablePoints) - 1)]


    def produceTileLayout(self) -> list:
        """ returns the tile layout for this floor plan """
        return deepcopy(self.layout)


    def tilePositionWithinBounds(self, position: Point, layout: list = None) -> bool:
        """ returns if the given position lies within this floor plan """
        layout = self.layout if layout is None else layout
        layoutPosition = self.__getLayoutPositionFromAbsolute(position)
        return (layoutPosition.X >= 0 and layoutPosition.X < len(layout[0])
                and layoutPosition.Y >= 0 and layoutPosition.Y < len(layout))


    def getTileInLayout(self, position: Point, layout: list = None) -> Tile:
        """ returns the tile in the layout at the given position, if the given
        layout is None self.layout is used """
        layout = self.layout if layout is None else layout
        layoutPosition = self.__getLayoutPositionFromAbsolute(position)
        return layout[layoutPosition.Y][layoutPosition.X]


    def setTileInLayout(self, position: Point, tile: any, layout: list = None):
        """ sets the tile in the layout at the given position, the given 'tile'
        may be a Tile, Interactable or Actor, if the given layout is None
        self.layout is used """
        from actor import Actor # TODO circular import error, moved here for now
        if (not isinstance(tile, Tile) and not isinstance(tile, Interactable)
                and not isinstance(tile, Actor)):
            raise ValueError('A FloorPlan cannot have a {0} placed in its layout'.format(
                type(tile)))
        layout = self.layout if layout is None else layout
        layoutPosition = self.__getLayoutPositionFromAbsolute(position)
        layout[layoutPosition.Y][layoutPosition.X] = tile
    

    def asciiRender(self) -> str:
        """ renders the floor plan from ascii subcomponents, returned as a string """
        tileLayout = self.produceTileLayout()
        # render each tile/interactable, join them and return
        def rowToString(tileRow: list) -> str:
            return ' '.join(map(lambda tile: tile.asciiRender(), tileRow))
        return '\n'.join(map(rowToString, tileLayout))


    def __validateUpperLeftPosition(self, upperLeftPosition: Point):
        """ raises error if the point object is invalid """
        if not isinstance(upperLeftPosition, Point):
            raise ValueError('FloorPlan given an invalid upper left position')

    
    def __validateLayout(self, layout: list):
        """ layout is of the same type as in __init__, raises ValueError if the
        layout is invalid """
        layoutTypeValid = isinstance(layout, list) and all(isinstance(row, list) for row in layout)
        if not layoutTypeValid:
            raise ValueError('FloorPlan given a layout that is not a list of lists.')
        
        allRowsSameLength = len(set(map(lambda row: len(row), layout))) == 1
        if not allRowsSameLength:
            raise ValueError('FloorPlan given a layout with different size rows.')

        from actor import Actor # TODO circular import
        allListObjectsAreValid = all(
                isinstance(tile, Tile) or
                isinstance(tile, Interactable) or
                isinstance(tile, Actor)
                for tile in [tile for row in layout for tile in row])
        if not allListObjectsAreValid:
            raise ValueError('FloorPlan must be given a layout of only Tile.')

    
    def __getLayoutPositionFromAbsolute(self, absolutePosition: Point) -> Point:
        """ returns a point that may be indexed to this floor plan's layout """
        return absolutePosition - self.upperLeftPosition



# ----- end of file ------------------------------------------------------------





