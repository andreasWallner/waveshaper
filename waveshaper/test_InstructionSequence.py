import unittest
from InstructionSequence import InstructionSequence
from utils import RealEqualMixin

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
    seq = [dummyInstr(), dummyInstr(), dummyInstr()]
    p = dummyPainter()

    inseq = InstructionSequence(seq, 1)
    inseq.execute(p)

    for s in seq:
      self.assertEqual(s.callcnt, 1)
      self.assertEqual(s.painter, p)

  def test_execute_multiple(self):
    seq = [dummyInstr(), dummyInstr(), dummyInstr()]
    p = dummyPainter()

    inseq = InstructionSequence(seq, 5)
    inseq.execute(p)

    for s in seq:
      self.assertEqual(s.callcnt, 5)
      self.assertEqual(s.painter, p)
    
class dummyInstr(object):
  def __init__(self):
    self.callcnt = 0
    self.painter = None

  def execute(self, painter):
    self.callcnt += 1
    self.painter = painter

class dummyPainter(object):
  def __init__(self):
    self.env = None
