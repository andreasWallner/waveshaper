from copy import copy
class InstructionSequence(object):
  def __init__(self, instructions, count = 1):
    self.instr = instructions
    self.count = count

  def __repr__(self):
    return 'InstructionSequence({0!r}, {1})'.format(self.instr, self.count)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return hasattr(other, '__dict__') and self.__dict__ == other.__dict__
    return NotImplemented

  def __ne__(self, other):
    return not self.__eq__(other)

  def execute(self, painter):
    painter.pushEnv()

    for n in range(self.count):
      for i in self.instr:
        i.execute(painter)

    painter.popEnv()
