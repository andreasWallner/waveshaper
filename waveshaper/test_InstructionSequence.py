import unittest
from copy import copy
from .InstructionSequence import InstructionSequence
from .EnvironmentChangeInstruction import EnvironmentChangeInstruction
from .utils import RealEqualMixin

class tests(unittest.TestCase, RealEqualMixin):
  def test_eq(self):
    self.assertRealEqual(
      InstructionSequence(None, 1),
      InstructionSequence(None, 1))

    self.assertRealNotEqual(
      InstructionSequence(None, 1),
      InstructionSequence(None, 2))

    self.assertRealEqual(
      InstructionSequence(['foo'], 1),
      InstructionSequence(['foo'], 1))

    self.assertRealNotEqual(
      InstructionSequence(['foo'], 1),
      InstructionSequence(['bar'], 1))

    self.assertRealNotEqual(
      InstructionSequence(['foo'], 1),
      InstructionSequence(['foo'], 2))

  def test_execute_single(self):
    seq = [dummyInstr(1), dummyInstr(2), dummyInstr(3)]
    p = dummyPainter()

    inseq = InstructionSequence(seq, 1)
    inseq.execute(p)

    for s in seq:
      self.assertEqual(s.callcnt, 1)
      self.assertEqual(s.painter, p)

    self.assertEqual(p.painted, [1,2,3])

  def test_execute_multiple(self):
    seq = [dummyInstr(1), dummyInstr(2)]
    p = dummyPainter()

    inseq = InstructionSequence(seq, 2)
    inseq.execute(p)

    for s in seq:
      self.assertEqual(s.callcnt, 2)
      self.assertEqual(s.painter, p)

    self.assertEqual(p.painted, [1,2,1,2])

  def test_envStack(self):
    seq = [
      dummyInstr(1),
      EnvironmentChangeInstruction('test', 2),
      dummyInstr(2),
      ]
    p = dummyPainter()

    inseq = InstructionSequence(seq, 1)
    inseq.execute(p)

    for s in seq:
      if type(s) is dummyInstr:
        self.assertEqual(s.callcnt, 1)
        self.assertEqual(s.painter, p)

    self.assertEqual(p.painted, [1,2])
    self.assertEqual(
      p.paintedEnv,
      [
        {'test' : 1},
        {'test' : 2},
        ])

  def test_xy(self):
    # 
    pass
    
class dummyInstr(object):
  def __init__(self, name):
    self.name = name
    self.callcnt = 0
    self.painter = None

  def execute(self, painter):
    self.callcnt += 1
    self.painter = painter
    painter.paint(self.name, painter.env)

class dummyPainter(object):
  def __init__(self):
    self.env = {'test' : 1}
    self.pushed = []
    self.painted = []
    self.paintedEnv = []

  def paint(self, name, env):
    self.painted.append(name)
    self.paintedEnv.append(copy(env))

  def pushEnv(self):
    self.pushed.append(copy(self.env))

  def popEnv(self):
    self.env = self.pushed.pop()
