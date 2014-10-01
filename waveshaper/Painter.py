from .OffsetCoord import *
from .tables import *

class Env(object):
    def __init__(self):
        self.lineheight = 1
        self.linewidth = 3
        self.bitwidth = 1
        self.slope = 0.2
        self.color = 'grey'

class Painter(object):
    def __init__(self, surface):
        self.surface = surface
        self.pos = OffsetCoord(0,0)
        self.last_symbol = None
        self.env = Env()
    
    def draw_line(self, c1, c2):
        self.surface.draw_line(self.pos + c1, self.pos + c2, self.env.linewidth)

    def draw_fill(self, vertices):
        vertices = [v + self.pos for v in vertices]
        self.surface.draw_fill(vertices, self.env.color, self.env.linewidth)

    def draw_text(self, text, position):
        self.surface.draw_text(text, position + self.pos)
