class EnvironmentChangeInstruction(object):
  def __init__(self, envvar, value):
    if envvar is None:
      envvar = 'color'

    self.envvar = envvar
    self.value = value

  def __repr__(self):
    return 'EnvironmentChangeInstruction({0!r}, {1!r})'.format(self.envvar, self.value)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return hasattr(other, '__dict__') and self.__dict__ == other.__dict__
    return NotImplemented

  def __ne__(self, other):
    return not self.__eq__(other)

  def execute(self, painter):
    if hasattr(painter.env, self.envvar):
      setattr(painter.env, self.envvar, self.value)
