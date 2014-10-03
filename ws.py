#!/usr/bin/python

import readline

from waveshaper.Parser import Wave
from waveshaper.MatplotlibSurface import MatplotlibSurface
from waveshaper.Painter import Painter

surface = MatplotlibSurface()
surface.show(block=False)

while True:
  i = input('wave? ')

  if i == 'quit':
    break

  try:
    surface.clear()
    painter = Painter(surface)
    seq = Wave().eval(i)
    seq.execute(painter)
    surface.fig.canvas.draw()
  except Exception as e:
    print(str(e))
