import unittest
import io
from .SVGSurface import SVGSurface
from .utils import RealEqualMixin
from .OffsetCoord import OffsetCoord

class tests(unittest.TestCase):
  def setUp(self):
    self.s = SVGSurface()
    self.f = io.BytesIO()

  def test_line(self):
    self.s.draw_line(
      OffsetCoord(1, 2),
      OffsetCoord(4, 5),
      'red',
      2)
    self.s.write(self.f)
    self.assertEqual(
      self.f.getvalue().decode('utf8'),
      results['test_line'])

  def test_fill(self):
    self.s.draw_fill(
      [
        OffsetCoord(0,0),
        OffsetCoord(1,1),
        OffsetCoord(1,0),
        ],
      'black',
      2)
    self.s.write(self.f)
    self.assertEqual(
      self.f.getvalue().decode('utf8'),
      results['test_fill'])

  def test_text(self):
    self.s.draw_text('foo', OffsetCoord(1,5))
    self.s.write(self.f)
    self.assertEqual(
      self.f.getvalue().decode('utf8'),
      results['test_text'])

results = {
  'test_line' : '''<?xml version=\'1.0\' encoding=\'utf8\'?>\n'''
    '''<svg><line style="stroke:red;stroke-width:2" x1="1" x2="4" y1="2" y2="5"></line></svg>''',
  'test_fill' : '''<?xml version=\'1.0\' encoding=\'utf8\'?>\n'''
    '''<svg><polygon points="0,0 1,1 1,0" style="stroke:black;stroke-width:2"></polygon></svg>''',
  'test_text' : '''<?xml version=\'1.0\' encoding=\'utf8\'?>\n'''
    '''<svg><text fill="black" x="1" y="5">foo</text></svg>''',
}