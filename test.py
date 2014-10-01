#!/usr/bin/python

from waveshaper.Painter import *
from waveshaper.MatplotlibSurface import *
from waveshaper.SimpleParser import parse
from waveshaper.BackgroundInstruction import BackgroundInstruction

seq = parse('2HLHLH3L3H')
s2 = BackgroundInstruction(parse('HH0L'))
seq.instr.insert(5, s2)
print(seq)

s = MatplotlibSurface()
p = Painter(s)
seq.execute(p)
s.show()
