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
        s = instruction.render_symbol(painter)
        lines = symbols[s]
        for line in lines:
            c1 = line[0]
            c2 = instruction.end() - line[1]
            surface.draw_line(c1, c2)
