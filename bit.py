#!/usr/bin/python

from OffsetCoord import *
from tables import *
from MatplotlibSurface import *
from utils import Trace


class Instruction(object):
  def __init__(self, icode, width, text = None):
    self.width = width
    self.icode = icode
    self.text = text

  def __repr__(self):
    return 'Instruction({0!r}, {1})'.format(self.icode, self.width)

  def symbol(self, painter):
    try:
      table = follow_symbol[self.icode]
      return table[painter.last_symbol]
    except KeyError:
      pass

    return self.icode

  def end(self, painter):
    return (self.width * painter.env.bitwidth, 0)

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
    
    lines = symbols[s]
    for line in lines:
      c1 = line[0](self.width, painter.env)
      c2 = line[1](self.width, painter.env)
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
    transition = transitions[(painter.last_symbol, self.symbol(painter))]

    for line in transition:
      c1 = line[0](0, painter.env)
      c2 = line[1](0, painter.env)
      painter.draw_line(c1, c2)

  def render_transition_bg(self, painter):
    try:
      polygons = transition_backgrounds[(painter.last_symbol), self.symbol(painter)]

      for polygon in polygons:
        vertices = [v(self.width, painter.env) for v in polygon]
        painter.draw_fill(vertices)
    except KeyError:
      pass
    

