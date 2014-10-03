import unittest
from .BackgroundInstruction import BackgroundInstruction
from .RenderInstruction import RenderInstruction
from .utils import RealEqualMixin

class tests(unittest.TestCase, RealEqualMixin):
  def test_eq(self):
    self.assertRealEqual(
      BackgroundInstruction(None),
      BackgroundInstruction(None))

    self.assertRealEqual(
      BackgroundInstruction([RenderInstruction('L', 1)]),
      BackgroundInstruction([RenderInstruction('L', 1)]))

    self.assertRealNotEqual(
      BackgroundInstruction([RenderInstruction('L', 1)]),
      BackgroundInstruction([RenderInstruction('H', 1)]))

    self.assertRealNotEqual(
      BackgroundInstruction([RenderInstruction('L', 1)]),
      BackgroundInstruction(None))

