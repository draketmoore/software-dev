#
# point.py
# authors: Michael Curley & Drake Moore
#

from math import sqrt


class Point:
    """ represents a 2d relative or absolute cartesian coordinate """

    def __init__(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError('A Point must only represent integer coordinates.')
        self.X = x
        self.Y = y


    def copy(self):
        """ returns a copy of this point """
        return Point(self.X, self.Y)


    def relativeMove(self, deltaX: int, deltaY: int):
        """ relatively moves the point based on the given delta values """
        if not isinstance(deltaX, int) or not isinstance(deltaY, int):
            raise ValueError('A Point can only be moved by integer deltas.')
        self.X += deltaX
        self.Y += deltaY


    def distanceFrom(self, other) -> float:
        """ returns the pythagorean distance from another Point """
        return sqrt((abs(other.X - self.X) ** 2) + (abs(other.Y - self.Y) ** 2))


    def cardinalDistanceFrom(self, other) -> int:
        """ returns the absolute cardinal distance from another Point """
        return max(abs(other.X - self.X), abs(other.Y - self.Y))


    @staticmethod
    def fromStr(point: str):
        """ returns a Point object from the string, or None if invalid format """
        try:
            components = point.split(',')
            x = int(components[0].strip()[1:])
            y = int(components[1].strip()[:-1])
            return Point(x, y)
        except:
            return None

    
    def __add__(self, other):
        return Point(self.X + other.X, self.Y + other.Y)


    def __sub__(self, other):
        return Point(self.X - other.X, self.Y - other.Y)


    def __str__(self) -> str:
        return '({0}, {1})'.format(self.X, self.Y)
   

    def __eq__(self, other: any) -> bool:
        return (isinstance(other, Point) and
                self.X == other.X and self.Y == other.Y)
    

    def __ne__(self, other: any) -> bool:
        return (not isinstance(other, Point) or
                self.X != other.X or self.Y != other.Y)


    def __gt__(self, other: any) -> bool:
        if not isinstance(other, Point):
            raise ValueError('No comparator for non-Point type')
        return (self.X, self.Y) > (other.X, other.Y)
    

    def __ge__(self, other: any) -> bool:
        if not isinstance(other, Point):
            raise ValueError('No comparator for non-Point type')
        return (self.X, self.Y) >= (other.X, other.Y)
    

    def __lt__(self, other: any) -> bool:
        if not isinstance(other, Point):
            raise ValueError('No comparator for non-Point type')
        return (self.X, self.Y) < (other.X, other.Y)
    

    def __le__(self, other: any) -> bool:
        if not isinstance(other, Point):
            raise ValueError('No comparator for non-Point type')
        return (self.X, self.Y) <= (other.X, other.Y)


    def __hash__(self) -> int:
        return hash((self.X, self.Y))


# ----- end of file ------------------------------------------------------------





