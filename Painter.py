from OffsetCoord import *
from tables import *

class Env(object):
    def __init__(self):
        self.lineheight = 1
        self.linewidth = 4
        self.bitwidth = 2
        self.slope = 0.2

class Painter(object):
    def __init__(self, surface):
        self.surface = surface
        self.pos = OffsetCoord(0,0)
        self.last_symbol = 'S'
        self.env = Env()
    
    def draw_line(self, c1, c2):
        self.surface.draw_line(self.pos + c1, self.pos + c2, self.env.linewidth)

    def paint_sequence(self, seq):
        for instr in seq:
            instr.render(self)
            self.pos += instr.end(self)
            self.last_symbol = instr.symbol(self)
