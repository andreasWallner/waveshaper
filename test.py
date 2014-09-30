#!/usr/bin/python

from waveshaper.Painter import *
from waveshaper.bit import *
from waveshaper.MatplotlibSurface import *

s = 'HD'
i = [Instruction(c, 1) for c in s]

s = MatplotlibSurface()
p = Painter(s)
p.paint_sequence(i)
s.show()
