from copy import copy
from .OffsetCoord import *
from .tables import *

class Painter(object):
    def __init__(self, surface):
        self.surface = surface
        self.pos = OffsetCoord(0,0)
        self.last_symbol = None
        self.env = {
          'lineheight' : 1,
          'linewidth'  : 3,
          'bitwidth'   : 1,
          'slope'      : 0.2,
          'fillcolor'  : 'grey',
          'color'      : 'black',
        }
        self.env['last'] = copy(self.env)

        self._posStack = []
        self._envStack = []

    def get_env(self, env):
        if env == 'c':
            return self.env
        elif env == 'l':
            return self.env['last']
        else:
            raise Exception('invalid environment')

    def painted(self, width, symbol):
        del self.env['last']
        self.env['last'] = copy(self.env)

        self.last_symbol = symbol
        self.pos += width
    
    def draw_line(self, c1, c2, env = 'c'):
        env = self.get_env(env)
        self.surface.draw_line(self.pos + c1, self.pos + c2, env['color'], env['linewidth'])

    def draw_fill(self, vertices, env = 'c'):
        env = self.get_env(env)
        vertices = [v + self.pos for v in vertices]
        self.surface.draw_fill(vertices, env['fillcolor'], env['linewidth'])

    def draw_text(self, text, position):
        self.surface.draw_text(text, position + self.pos)

    def pushPos(self):
      self._posStack.append(self.pos)

    def popPos(self):
      self.pos = self._posStack.pop()

    def pushEnv(self):
      self._envStack.append(copy(self.env))
    
    def popEnv(self):
      self.env = self._envStack.pop()
