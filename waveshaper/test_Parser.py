import unittest
from .Parser import Wave
from .RenderInstruction import RenderInstruction
from .BackgroundInstruction import BackgroundInstruction
from .InstructionSequence import InstructionSequence
from .EnvironmentChangeInstruction import EnvironmentChangeInstruction

class BasicTests(unittest.TestCase):
  def test_minimal(self):
    self.assertEqual(
      Wave().eval('L'),
      InstructionSequence([RenderInstruction('L')], 1))

  def test_width(self):
    self.assertEqual(
      Wave().eval('3L'),
      InstructionSequence([RenderInstruction('L', 3)], 1))

  def test_param(self):
    self.assertEqual(
      Wave().eval('D(0xAA)'),
      InstructionSequence([RenderInstruction('D', 1, '0xAA')], 1))

  def test_multiple_params(self):
    self.assertEqual(
      Wave().eval('3L(x,x,x)'),
      InstructionSequence([RenderInstruction('L', 3, 'x')], 1))

  def test_multiple_instr(self):
    self.assertEqual(
      Wave().eval('LLL'),
      InstructionSequence(3*[RenderInstruction('L')], 1))

  def test_ec_instruction(self):
    self.assertEqual(
      Wave().eval('[foo=bar]'),
      InstructionSequence([EnvironmentChangeInstruction('foo', 'bar')]))

  def test_ec_no_indentifier(self):
    self.assertEqual(
      Wave().eval('[bar]'),
      InstructionSequence([EnvironmentChangeInstruction('color', 'bar')]))

class SequenceTests(unittest.TestCase):
  def test_explicit(self):
    self.assertEqual(
      Wave().eval('{LLL}'),
      InstructionSequence(3*[RenderInstruction('L')], 1))

  def test_mutiple(self):
    self.assertEqual(
      Wave().eval('4{LLL}'),
      InstructionSequence(3*[RenderInstruction('L')], 4))

  def test_mixed(self):
    self.assertEqual(
      Wave().eval('L5{H}L'),
      InstructionSequence([RenderInstruction('L'), InstructionSequence([RenderInstruction('H')], 5), RenderInstruction('L')], 1))

  def test_sequence_param(self):
    self.assertEqual(
      Wave().eval('B({LL})'),
      InstructionSequence([BackgroundInstruction(InstructionSequence(2*[RenderInstruction('L')]))]))

  def test_nested(self):
    self.assertEqual(
      Wave().eval('{2{L}2{H}}'),
      InstructionSequence([InstructionSequence([RenderInstruction('L')], 2), InstructionSequence([RenderInstruction('H')], 2)], 1))

  def test_nested_mixed(self):
    self.assertEqual(
      Wave().eval('2{2{L}H}'),
      InstructionSequence([InstructionSequence([RenderInstruction('L')], 2), RenderInstruction('H')], 2))

  def test_nested_optimizable(self):
    self.assertEqual(
      Wave().eval('{5{L}}'),
      InstructionSequence([RenderInstruction('L')], 5))

  def test_nested_optimizable_calc(self):
    self.assertEqual(
      Wave().eval('2{5{L}}'),
      InstructionSequence([RenderInstruction('L')], 10))

  def test_complete(self):
    self.assertEqual(
      Wave().eval('LH4LB({[grey]H0L})LL(0)'),
      InstructionSequence([
        RenderInstruction('L'),
        RenderInstruction('H'),
        RenderInstruction('L', 4),
        BackgroundInstruction(
          InstructionSequence([
            EnvironmentChangeInstruction('color', 'grey'),
            RenderInstruction('H'),
            RenderInstruction('L', 0)])),
        RenderInstruction('L'),
        RenderInstruction('L', 1, '0') ]))

class RuleTests(unittest.TestCase):
  def test_identifier(self):
    self.assertEqual(
      Wave().eval('_asdf', 'identifier'),
      '_asdf')

  def test_natural(self):
    self.assertEqual(
      Wave().eval('123', 'natural'),
      123)

  def test_float(self):
    self.assertEqual(
      Wave().eval('123', 'float'),
      123)

    self.assertEqual(
      Wave().eval('1.2', 'float'),
      1.2)

    self.assertEqual(
      Wave().eval('.4', 'float'),
      0.4)

  def test_string(self):
    self.assertEqual(
      Wave().eval('asdf', 'string'),
      'asdf')
  
    self.assertEqual(
      Wave().eval('"asdf,xy"', 'string'),
      'asdf,xy')
