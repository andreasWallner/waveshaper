from .OffsetCoord import *
from .tables import *
from .MatplotlibSurface import *
from .utils import Trace

class RenderInstruction(object):
  def __init__(self, icode, width = 1, text = None):
    self.width = width
    self.icode = icode
    self.text = text

  def __repr__(self):
    return 'RenderInstruction({0!r}, {1}, {2!r})'.format(self.icode, self.width, self.text)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return hasattr(other, '__dict__') and self.__dict__ == other.__dict__
    return NotImplemented

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
    return hash(tuple(sorted(self.__dict__.items())))

  def symbol(self, painter):
    try:
      table = follow_symbol[self.icode]
      try:
        return table[painter.last_symbol]
      except KeyError:
        return table['']
    except KeyError:
      return self.icode

  def end(self, painter):
    return (self.width * painter.env['bitwidth'], 0)

  def execute(self, painter):
    self.render(painter)
    painter.painted(self.end(painter), self.symbol(painter))

  def render(self, painter):
    if painter.last_symbol is not None:
      self.render_transition(painter)
      self.render_transition_bg(painter)

    if self.width != 0:
      self.render_symbol(painter)
      self.render_symbol_bg(painter)
      self.render_symbol_text(painter)

  def render_path(self, vertices, painter, env = 'c'):
    coords = [x(self.width, painter.get_env(env)) for x in vertices]
    for c1, c2 in zip(coords[:-1], coords[1:]):
      painter.draw_line(c1, c2, env)

  def render_polygon(self, vertices, painter, env = 'c'):
    vertices = [v(self.width, painter.get_env(env)) for v in vertices]
    painter.draw_fill(vertices, env)

  def render_symbol(self, painter):
    s = self.symbol(painter)
    
    paths = symbols[s]
    for vertices in paths:
      self.render_path(vertices, painter)

  def render_symbol_bg(self, painter):
    s = self.symbol(painter)
    if s not in backgrounds:
      return

    polygons = backgrounds[s]
    for polygon in polygons:
      vertices, env = polygon
      self.render_polygon(vertices, painter, env)

  def render_symbol_text(self, painter):
    if self.text is not None:
      painter.draw_text(self.text, anchors['cc'](self.width, painter.env))
  
  def render_transition(self, painter):
    paths = transitions[(painter.last_symbol, self.symbol(painter))]
    
    for path in paths:
      vertices, env = path
      self.render_path(vertices, painter, env)

  def render_transition_bg(self, painter):
    idx = (painter.last_symbol, self.symbol(painter))
    if idx not in backgrounds:
      return
    polygons = backgrounds[(painter.last_symbol), self.symbol(painter)]
    
    for polygon in polygons:
      vertices, env = polygon
      self.render_polygon(vertices, painter, env)

