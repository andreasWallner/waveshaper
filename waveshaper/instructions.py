from RenderInstruction import RenderInstruction
from BackgroundInstruction import BackgroundInstruction
from utils import Trace

def get_instruction(symbol, width = None, parameters = None):
  if width is None:
    width = 1

  if symbol == 'B':
    return BackgroundInstruction(parameters[0])
  else:
    param = None if not parameters else parameters[0]
    return RenderInstruction(symbol, width, param)
