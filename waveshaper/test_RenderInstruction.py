import unittest
from .RenderInstruction import RenderInstruction
from .utils import RealEqualMixin

class tests(unittest.TestCase, RealEqualMixin):
  def test_eq(self):
    self.assertRealEqual(
      RenderInstruction('L', 1),
      RenderInstruction('L', 1))

    self.assertRealEqual(
      RenderInstruction('L', 1, 'foo'),
      RenderInstruction('L', 1, 'foo'))

    self.assertRealNotEqual(
      RenderInstruction('L', 1),
      RenderInstruction('H', 1))

    self.assertRealNotEqual(
      RenderInstruction('L', 1),
      RenderInstruction('L', 2))

    self.assertRealNotEqual(
      RenderInstruction('L', 1),
      RenderInstruction('L', 1, 'foo'))
