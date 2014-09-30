from .utils import Trace

class OffsetCoord(object):
    def __init__(self, c, y = None):
        if y is not None:
            self.x = c
            self.y = y
        elif c is OffsetCoord:
            self.x = c.x
            self.y = c.y
        else:
            self.x = c[0]
            self.y = c[1]

    def __str__(self):
        return "{}, {}".format(self.x, self.y)

    def __repr__(self):
        return "OffsetCoord({}, {})".format(self.x, self.y)
    
    def __neg__(self):
        return OffsetCoord(-self.x, self.y)

    def __add__(self, other):
        if not isinstance(other, OffsetCoord):
            other = OffsetCoord(other)

        return OffsetCoord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, OffsetCoord):
            other = OffsetCoord(other)

        return OffsetCoord(self.x - other.x, self.y + other.y)

    def flip(self):
        return OffsetCoord(-self.x, -self.y)

    def tuple(self):
        return (self.x, self.y)
