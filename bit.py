#!/usr/bin/python

from OffsetCoord import *
from tables import *
from MatplotlibSurface import *


class Instruction(object):
    def __init__(self, symbol, width):
        self.width = width
        self.symbol = symbol

    def render_symbol(self, painter):
        return self.symbol

    def end(self, painter):
        return (self.width * painter.env.bitwidth, 0)

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

