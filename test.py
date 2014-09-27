#!/usr/bin/python

from Painter import *
from bit import *
from MatplotlibSurface import *

i = [
    Instruction('L', 1),
    Instruction('H', 1),
    Instruction('H', 1),
    Instruction('L', 1),
    Instruction('H', 1),
]

s = MatplotlibSurface()
p = Painter(s)
p.paint_sequence(i)
s.show()
