#!/usr/bin/python

from OffsetCoord import *
from tables import *
from MatplotlibSurface import *


class Instruction(object):
    def __init__(self, icode, width):
        self.width = width
        self.icode = icode

    def symbol(self, painter):
        return self.icode

    def end(self, painter):
        return (self.width * painter.env.bitwidth, 0)

    def at_start(self, anchor, painter):
        return anchors[anchor](self.width, painter.env)

    def at_end(self, anchor, painter):
        offset = anchors[anchor](self.width, painter.env)
        return OffsetCoord(self.width * painter.env.bitwidth, 0) - offset

    def render(self, painter):
        self.render_transition(painter)
        if self.width != 0:
            self.render_symbol(painter)

    def render_symbol(self, painter):
        s = self.symbol(painter)
        
        lines = symbols[s]
        for line in lines:
            c1 = self.at_start(line[0], painter)
            c2 = self.at_end(line[1], painter)
            print(c1)
            print(c2)
            painter.draw_line(c1, c2)

    def render_transition(self, painter):
        transition = transitions[(painter.last_symbol, self.symbol(painter))]

        for line in transition:
            c1 = -anchors[line[0]](0, painter.env)
            c2 = anchors[line[1]](0, painter.env)
            painter.draw_line(c1, c2)

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

