from parsimonious.grammar import Grammar
from .utils import Trace
from .instructions import get_instruction
from .InstructionSequence import InstructionSequence
from .EnvironmentChangeInstruction import EnvironmentChangeInstruction

class Wave(object):
  def __init__(self):
    pass

  def parse(self, source, root=None):
    if root is None:
      root = 'wave'

    grammar = '\n'.join(v.__doc__ for k, v in vars(self.__class__).items()
      if '__' not in k and hasattr(v, '__doc__') and v.__doc__)

    return Grammar(grammar)[root].parse(source)

  def eval(self, source, root=None):
    node = self.parse(source, root) if isinstance(source, str) else source
    method = getattr(self, node.expr_name, lambda node, children: children)
    return method(node, [self.eval(n) for n in node])
  
  def wave(self, node, children):
    'wave = sequence'
    return children

  def symbol(self, node, children):
    'symbol = ~"[a-zA-Z]"'
    return node.text

  def identifier(self, node, children):
    'identifier = ~"[a-zA-Z_]+"'
    return node.text

  def string(self, node, children):
    'string = ( ~"[a-zA-Z0-9]+" ) / ( "\\"" ~"[^\\"]*" "\\"" )'
    text = node.text if node.text[0] != '"' else node.text[1:-1]
    return text

  def sequence_group(self, node, children):
    'sequence_group = natural? "{" sequence+ "}"'
    count, _, seq, _ = children

    count = 1 if not count else count[0]
    if len(seq) == 1 and isinstance(seq[0], InstructionSequence):
      seq[0].count = seq[0].count * count
      return seq[0]
    else:
      return InstructionSequence(seq, count)

  def instructions(self, node, children):
    'instructions = instruction+'
    if len(children) == 1:
      return children[0]
    else:
      return InstructionSequence(children, 1)

  def sequence(self, node, children):
    'sequence = ( sequence_group / instructions )+'
    if len(children) == 1 and isinstance(children[0][0], InstructionSequence):
      return children[0][0]
    else:
      seq = [x[0] for x in children]
      return InstructionSequence(seq, 1)

  def parameter(self, node, children):
    'parameter = string / ( sequence )'
    return children[0]

  def parameters(self, node, children):
    'parameters = parameter ( "," parameter )*'
    par = [children[0]] + ([x[1] for x in children[1]])
    return par

  def ec_instruction(self, node, children):
    'ec_instruction = "[" ( identifier "=" )? string "]"'
    identifier = None if not children[1] else children[1][0][0]
    return EnvironmentChangeInstruction(identifier, children[2])

  def rndr_instruction(self, node, children):
    'rndr_instruction = float? symbol ( "(" parameters ")" )?'

    width, sym, par = children
  
    width = None if not width else width[0]
    par = None if not par else par[0][1]

    return get_instruction(sym, width, par)

  def instruction(self, node, children):
    'instruction = rndr_instruction / ec_instruction'
    return children[0]

  def natural(self, node, children):
    'natural = ~"[0-9]+"'
    return int(node.text)

  def float(self, node, children):
    'float = ( natural ( "." natural )? ) / ( "." natural )'
    return float(node.text)

  def _(self, node, children):
    '_ = ~"\s*"'
    pass
