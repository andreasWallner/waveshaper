from .RenderInstruction import RenderInstruction
from .BackgroundInstruction import BackgroundInstruction
from .utils import Trace

def get_instruction(symbol, width = None, parameters = None):
  if width is None:
    width = 1

  if symbol == 'B' or symbol == 'b':
    return BackgroundInstruction(parameters[0])
  else:
    param = None if not parameters else parameters[0]
    if symbol.islower():
      width *= 0.5
      symbol = symbol.upper()

    return RenderInstruction(symbol, width, param)
