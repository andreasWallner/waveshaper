from OffsetCoord import *

def lsum(l1, l2):
  return (lambda width, env: l1(width, env) + l2(width, env))
 
def end(l):
  return (lambda width, env: OffsetCoord(width * env.bitwidth, 0) - l(width, env))
 
def left(l):
  """ returns lambda that calculates point left of a transition center"""
  return (lambda width, env: -l(width, env))
 
def right(l):
  """ returns lambda that calculates point right of transition center"""
  return (lambda width, env: l(width, env))

def combinate(d1, d2):
  result = {}
  for foo in d1:
    for bar in d2:
      result[foo + bar] = lsum(d1[foo], d2[bar])
  return result

y_offsets = {
  'c' : (lambda width, env: OffsetCoord(0, 0)),
  'b' : (lambda width, env: OffsetCoord(0, -env.lineheight / 2)),
  'a' : (lambda width, env: OffsetCoord(0, env.lineheight / 2)),
}
 
x_offsets = {
  'e' : (lambda width, env: OffsetCoord(0, 0)),
  's' : (lambda width, env: OffsetCoord(env.lineheight * env.slope, 0)),
  'm' : (lambda width, env: OffsetCoord(env.lineheight * env.slope / 2, 0)),
  'c' : (lambda width, env: OffsetCoord(width * env.bitwidth / 2, 0)),
}

anchors = combinate(x_offsets, y_offsets)
locals().update({'a_' + x : anchors[x] for x in anchors})

symbols = {
  'S' : [],
  'L' : [(a_sb, end(a_sb))],
  'H' : [(a_sa, end(a_sa))],
  'U' : [(a_sb, end(a_sb)), (a_sa, end(a_sa))],
  'D' : [(a_sb, end(a_sb)), (a_sa, end(a_sa))],
  'CL' : [(a_sb, end(a_sb))],
  'CH' : [(a_sa, end(a_sa))],
}

follow_symbol = {
  'C' : {
    'CL' : 'CH',
    'CH' : 'CL',
    'S' : 'CL',
  }
}

symbol_backgrounds = {
  'U' : [[a_sa, end(a_sa), end(a_sb), a_sb]],
}

transitions = {
  ('S', 'L') : [(left(a_eb), right(a_sb))],
  ('S', 'H') : [(left(a_ea), right(a_sa))],
  ('L', 'S') : [(left(a_sb), right(a_eb))],
  ('H', 'S') : [(left(a_sa), right(a_ea))],
  ('L', 'H') : [(left(a_sb), right(a_sa))],
  ('L', 'L') : [(left(a_sb), right(a_sb))],
  ('H', 'H') : [(left(a_sa), right(a_sa))],
  ('H', 'L') : [(left(a_sa), right(a_sb))],
  ('H', 'U') : [(left(a_sa), right(a_sb)), (left(a_cc), right(a_sa))],
  ('U', 'H') : [(left(a_sb), right(a_sa)), (left(a_sa), right(a_cc))],
  ('U', 'U') : [(left(a_sb), right(a_sb)), (left(a_sa), right(a_sa))],
  ('U', 'S') : [(left(a_sb), right(a_eb)), (left(a_sa), right(a_ea))],
  ('H', 'D') : [(left(a_sa), right(a_sb)), (left(a_cc), right(a_sa))],
  ('D', 'H') : [(left(a_sb), right(a_sa)), (left(a_sa), right(a_cc))],
  ('D', 'D') : [(left(a_sa), right(a_sb)), (left(a_sb), right(a_sa))],
  ('D', 'U') : [(left(a_sa), right(a_sb)), (left(a_sb), right(a_sa))],
  ('U', 'D') : [(left(a_sa), right(a_sb)), (left(a_sb), right(a_sa))],
  ('D', 'S') : [(left(a_sb), right(a_ec)), (left(a_sa), right(a_ec))],
  ('S', 'D') : [(left(a_ec), right(a_sb)), (left(a_ec), right(a_sa))],
  ('S', 'S') : [],
  ('CL', 'CH') : [(left(a_sb), left(a_sa)), (left(a_sa), right(a_sa))],
  ('CH', 'CL') : [(left(a_sa), left(a_sb)), (left(a_sb), right(a_sb))],
  ('S', 'CH') : [(left(a_ea), right(a_sa))],
  ('S', 'CL') : [(left(a_eb), right(a_sb))],
  ('CH', 'S') : [(left(a_sa), right(a_ea))],
  ('CL', 'S') : [(left(a_sb), right(a_eb))],
}

transition_backgrounds = {
  ('H', 'U') : [(a_ec, a_sa, a_sb)],
  ('U', 'H') : [(a_ec, left(a_sa), left(a_sb))],  
  ('L', 'U') : [(a_ec, a_sa, a_sb)],
  ('U', 'L') : [(a_ec, left(a_sa), left(a_sb))],
  ('U', 'U') : [(left(a_sa), a_sa, a_sb, left(a_sb))],
  ('U', 'S') : [(left(a_sb), a_eb, a_ea, left(a_sa))],
  ('S', 'U') : [(left(a_eb), a_sb, a_sa, left(a_ea))],
}