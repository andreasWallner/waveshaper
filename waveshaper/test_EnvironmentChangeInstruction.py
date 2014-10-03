import unittest
from .EnvironmentChangeInstruction import EnvironmentChangeInstruction
from .utils import RealEqualMixin

class tests(unittest.TestCase, RealEqualMixin):
  def test_eq(self):
    self.assertRealEqual(
      EnvironmentChangeInstruction('foo', 'bar'),
      EnvironmentChangeInstruction('foo', 'bar'))

    self.assertRealEqual(
      EnvironmentChangeInstruction(None, 'bar'),
      EnvironmentChangeInstruction('color', 'bar'))

    self.assertRealNotEqual(
      EnvironmentChangeInstruction('foo', 'bar'),
      EnvironmentChangeInstruction('bar', 'bar'))

    self.assertRealNotEqual(
      EnvironmentChangeInstruction('foo', 'bar'),
      EnvironmentChangeInstruction('foo', 'foo'))

  def test_execute(self):
    dp = dummyPainter()

    eci = EnvironmentChangeInstruction(None, 'black')
    eci.execute(dp)
    self.assertEqual(dp.env.color, 'black')
    self.assertEqual(dp.env.foo, 0)

    eci = EnvironmentChangeInstruction('foo', 'red')
    eci.execute(dp)
    self.assertEqual(dp.env.color, 'black')
    self.assertEqual(dp.env.foo, 'red')

    eci = EnvironmentChangeInstruction('bar', 'red')
    eci.execute(dp)
    self.assertEqual(dp.env.color, 'black')
    self.assertEqual(dp.env.foo, 'red')

class dummyEnv(object):
  def __init__(self):
    self.color = None
    self.foo = 0

class dummyPainter(object):
  def __init__(self):
    self.env = dummyEnv()
