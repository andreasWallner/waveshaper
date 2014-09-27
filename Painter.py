from OffsetCoord import *
from tables import *

class Env(object):
    def __init__(self):
        self.lineheight = 1
        self.bitwidth = 2
        self.slope = 0.2

class Painter(object):
    def __init__(self, surface):
        self.surface = surface
        self.pos = OffsetCoord(0,0)
        self.last_symbol = 'S'
        self.env = Env()
    
    def render_symbol(self, instruction):
        s = instruction.render_symbol(self)
        lines = symbols[s]
        for line in lines:
            c1 = anchors[line[0]](instruction.width, self.env)
            c2 = OffsetCoord(instruction.end(self)) - anchors[line[1]](instruction.width, self.env)
            self.draw_line(c1, c2)

    def render_transition(self, right):
        r = right.render_symbol(self)
        transition = transitions[(self.last_symbol, r)]

        for line in transition:
            c1 = -anchors[line[0]](0, self.env)
            c2 = anchors[line[1]](0, self.env)
            self.draw_line(c1, c2)

    def draw_line(self, c1, c2):
        self.surface.draw_line(self.pos + c1, self.pos + c2)

    def paint_sequence(self, seq):
        for instr in seq:
            self.render_transition(instr)
            self.render_symbol(instr)
            self.pos += instr.end(self)
            self.last_symbol = instr.render_symbol(self)
