#!/usr/bin/python

from Painter import *
from bit import *
from MatplotlibSurface import *

s = 'LHLHLH'
i = [Instruction(c, 1) for c in s] + [Instruction('D', 2, 'A'), Instruction('S', 1)]

s = MatplotlibSurface()
p = Painter(s)
p.paint_sequence(i)
s.show()
