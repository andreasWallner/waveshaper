#!/usr/bin/python

from waveshaper.Painter import *
from waveshaper.RenderInstruction import *
from waveshaper.MatplotlibSurface import *

s = 'HD'
i = [RenderInstruction(c, 1) for c in s]

s = MatplotlibSurface()
p = Painter(s)
p.paint_sequence(i)
s.show()
