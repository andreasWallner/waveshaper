from copy import copy

class InstructionSequence(object):
  def __init__(self, instructions):
    self.instr = instructions

  def __repr__(self):
    return 'InstructionSequence({0!r})'.format(self.instr)

  def execute(self, painter):
    oldEnv = copy(painter.env)

    for i in self.instr:
      i.execute(painter)

    painter.env = oldEnv
