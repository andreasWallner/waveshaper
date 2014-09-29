from OffsetCoord import *

def lsum(l1, l2):
  return (lambda width, env: l1(width, env) + l2(width, env))
 
def lend(l):
  return (lambda width, env: OffsetCoord(width * env.bitwidth, 0) + l1(width, env).flipLR())
 
def lleft(l):
  return (lambda width, env: l(width, env).flipLR())
 
def lright(l):
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
  'L' : [(a_sb, a_sb)],
  'H' : [(a_sa, a_sa)],
  'U' : [(a_sb, a_sb), (a_sa, a_sa)],
}

transitions = {
  ('S', 'L') : [(a_eb, a_sb)],
  ('S', 'H') : [(a_ea, a_sa)],
  ('L', 'S') : [(a_sb, a_eb)],
  ('H', 'S') : [(a_sa, a_ea)],
  ('L', 'H') : [(a_sb, a_sa)],
  ('L', 'L') : [(a_sb, a_sb)],
  ('H', 'H') : [(a_sa, a_sa)],
  ('H', 'L') : [(a_sa, a_sb)],
}

backgrounds = {
  'U' : [],
  'L' : [],
  'H' : [],
}
