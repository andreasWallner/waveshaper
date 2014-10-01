from .RenderInstruction import RenderInstruction
from .BackgroundInstruction import BackgroundInstruction
from .InstructionSequence import InstructionSequence

def parse(string):
  ''' in no way finished and very dumb parser, only to ease testing'''
  result = []
  width = None

  for nc in string:
    if nc in '1234567890':
      if width is None:
        width = int(nc)
      else:
        width = width * 10 + int(nc)

    elif nc in 'LHUDCXZS':
      if width is None:
        width = 1
      result.append(RenderInstruction(nc, width))
      width = None

    elif nc in 'lhudcxzs':
      if width is None:
        width = 1
      result.append(RenderInstruction(nc, width*0.5))
      width = None

    else:
      raise Exception('invalid symbol contained')

  return InstructionSequence(result)
