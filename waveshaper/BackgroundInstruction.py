from copy import copy

class BackgroundInstruction(object):
  def __init__(self, seq):
    self.seq = seq

  def __repr__(self):
    return 'BackgroundInstruction({0!r})'.format(self.seq)

  def execute(self, painter):
    origEnv = copy(painter.env)
    pos = painter.pos
    ls = painter.last_symbol

    self.seq.execute(painter)

    painter.env = origEnv
    painter.pos = pos
    painter.last_symbol = ls
