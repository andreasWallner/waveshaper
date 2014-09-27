#!/usr/bin/python

from OffsetCoord import *
from tables import *
from MatplotlibSurface import *


class Instruction(object):
    def __init__(self, symbol, width):
        self.width = width
        self.symbol = symbol

    def render_symbol(self, painter):
        return symbol

    def end(self):
        return (self.width * self.env.bitwidth, 0)


class Bit(object):
    def __init__(self, symbol, width, prev, env):
        self.width = width
        self.env = env
        self.prev = prev
        self.symbol = symbol

    def render(self, surface, following):
        pass

    def start(self):
        return self.prev.end()
        
    def from_start(self, anchor):
        return self.start() + anchors[anchor](self.width, self.env)

    def from_end(self, anchor):
        return self.end() - anchors[anchor](self.width, self.env)

    def render_symbol(self):
        return self.symbol

class Origin(Bit):
    def __init__(self, coord, symbol, env):
        super().__init__(symbol, 0, None, env)
        self.coord = OffsetCoord(coord)

    def start(self):
        return self.coord

    def end(self):
        return self.coord

class End(Bit):
    def __init__(self, symbol, prev, env):
        super().__init__(symbol, 0, prev, env)

    def end(self):
        return self.start()

class BasicBit(Bit):
    def __init__(self, symbol, width, prev, env):
        super().__init__(symbol, width, prev, env)

    def render(self, surface, following):
        super().render(surface, following)

        self.draw_symbol(surface, self.symbol)
        self.draw_transition(surface, self.prev, end=False)
        self.draw_transition(surface, following, end=True)

    def draw_symbol(self, surface, symbol):
        lines = symbols[symbol]
        for line in lines:
            c1 = self.from_start(line[0])
            c2 = self.from_end(line[0])
            surface.draw_line(c1, c2)

    def draw_transition(self, surface, other, end=False):
        f = None
        t = None

        if not end:
            f = other
            t = self
        else:
            f = self
            t = other

        transition = transitions[(f.symbol, t.symbol)]
        for line in transition:
            print(line)
            c1 = f.from_end(line[0])
            c2 = t.from_start(line[1])
            surface.draw_line(c1, c2)

class SimpleSequence(object):
    def __init__(self, symbols, env):
        self.chain = [Origin((0,0), 'S', env)]
        for symbol in symbols:
            new = BasicBit(symbol, 1, self.chain[-1], env)
            self.chain.append(new)
        self.chain.append(End('S', self.chain[-1], env))

    def render(self, surface):
        for i in range(len(self.chain) - 1):
            self.chain[i].render(surface, self.chain[i+1])

env = Env()
seq = SimpleSequence('LLHHLLHH', env)
sf = MatplotlibSurface()
seq.render(sf)
sf.show()
