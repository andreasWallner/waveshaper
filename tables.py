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
}

backgrounds = {
  'U' : [],
  'L' : [],
  'H' : [],
}
