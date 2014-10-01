from .OffsetCoord import *
from .tables import *
from .MatplotlibSurface import *
from .utils import Trace

class RenderInstruction(object):
  def __init__(self, icode, width, text = None):
    self.width = width
    self.icode = icode
    self.text = text

  def __repr__(self):
    return 'RenderInstruction({0!r}, {1}, {2!r})'.format(self.icode, self.width, self.text)

  def symbol(self, painter):
    try:
      table = follow_symbol[self.icode]
      return table[painter.last_symbol]
    except KeyError:
      return self.icode

  def end(self, painter):
    return (self.width * painter.env.bitwidth, 0)

  def execute(self, painter):
    self.render(painter)
    painter.pos += self.end(painter)
    painter.last_symbol = self.symbol(painter)

  def render(self, painter):
    if painter.last_symbol is not None:
      self.render_transition(painter)
      self.render_transition_bg(painter)

    if self.width != 0:
      self.render_symbol(painter)
      self.render_symbol_bg(painter)
      self.render_symbol_text(painter)

  def render_symbol(self, painter):
    s = self.symbol(painter)
    
    paths = symbols[s]
    for verts in paths:
      for v1, v2 in zip(verts[:-1], verts[1:]):
        c1 = v1(self.width, painter.env)
        c2 = v2(self.width, painter.env)
        painter.draw_line(c1, c2)

  def render_symbol_bg(self, painter):
    try:
      s = self.symbol(painter)
      
      polygons = symbol_backgrounds[s]
      for polygon in polygons:
        vertices = [v(self.width, painter.env) for v in polygon]
        painter.draw_fill(vertices)
    except KeyError:
      pass

  def render_symbol_text(self, painter):
    if self.text is None:
      return

    painter.draw_text(self.text, anchors['cc'](self.width, painter.env))

  def render_transition(self, painter):
    paths = []
    try:
      paths = transitions[(painter.last_symbol, self.symbol(painter))]
    except KeyError:
      mirrored = transitions[(self.symbol(painter), painter.last_symbol)]
      for lines in mirrored:
        paths.append([mirror(v) for v in lines])

    for verts in paths:
      for v1, v2 in zip(verts[:-1], verts[1:]):
        c1 = v1(self.width, painter.env)
        c2 = v2(self.width, painter.env)
        painter.draw_line(c1, c2)

  def render_transition_bg(self, painter):
    try:
      try:
        polygons = transition_backgrounds[(painter.last_symbol), self.symbol(painter)]
      except KeyError:
        mirrored = transition_backgrounds[(self.symbol(painter), painter.last_symbol)]
        polygons = []
        for polygon in mirrored:
          vertices = [mirror(v) for v in polygon]
          polygons.append(vertices)

      for polygon in polygons:
        vertices = [v(self.width, painter.env) for v in polygon]
        painter.draw_fill(vertices)
    except KeyError:
      pass
    

