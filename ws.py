#!/usr/bin/python
try:
  import readline
except ImportError:
  import pyreadline as readline

from waveshaper.Parser import Wave
from waveshaper.MatplotlibSurface import MatplotlibSurface
from waveshaper.SVGSurface import SVGSurface
from waveshaper.Painter import Painter

surface = MatplotlibSurface()
surface.show(block=False)

seq = None
while True:
  i = input('wave? ')

  if i.strip() == '\q':
    break

  if i.strip().startswith('\w '):
    filename = i.strip()[3:]
    svg = SVGSurface()
    painter = Painter(svg)
    seq.execute(painter)
    svg.write(filename)
    continue

  try:
    surface.clear()
    painter = Painter(surface)
    seq = Wave().eval(i)
    seq.execute(painter)
    surface.fig.canvas.draw()
  except Exception as e:
    print(str(e))
