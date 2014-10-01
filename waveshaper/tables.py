from .OffsetCoord import *

def lsum(l1, l2):
  return (lambda width, env: l1(width, env) + l2(width, env))
 
def end(l):
  return (lambda width, env: OffsetCoord(width * env.bitwidth, 0) - l(width, env))

def mirror(l):
  return (lambda width, env: -l(width, env))

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
  'L' : [[a_sb, end(a_sb)]],
  'H' : [[a_sa, end(a_sa)]],
  'Z' : [[a_sc, end(a_sc)]],
  'X' : [[a_sc, end(a_sc)]],
  'U' : [[a_sb, end(a_sb)], [a_sa, end(a_sa)]],
  'D' : [[a_sb, end(a_sb)], [a_sa, end(a_sa)]],
  #'M' : [],
  'CL' : [[a_sb, end(a_sb)]],
  'CH' : [[a_sa, end(a_sa)]],
}

follow_symbol = {
  'C' : {
    'CL' : 'CH',
    'CH' : 'CL',
    'S' : 'CL',
    },
  'T' : {
    'L' : 'H',
    'H' : 'L',
  }
}

symbol_backgrounds = {
  'U' : [[a_sa, end(a_sa), end(a_sb), a_sb]],
}

transitions = {
  ('S', 'S') : [],
  ('S', 'L') : [[left(a_eb), right(a_sb)]],
  ('S', 'H') : [[left(a_ea), right(a_sa)]],
  ('S', 'Z') : [[left(a_ec), right(a_sc)]],
  ('S', 'X') : [[left(a_ec), right(a_sc)]],
  ('S', 'U') : [[left(a_eb), right(a_sb)], [left(a_ea), right(a_sa)]],
  ('S', 'D') : [[right(a_sb), right(a_ec), right(a_sa)]],
  ('S', 'CL') : [[left(a_eb), right(a_sb)]],
  ('S', 'CH') : [[left(a_ea), right(a_sa)]],

  ('L', 'L') : [[left(a_sb), right(a_sb)]],
  ('L', 'H') : [[left(a_sb), right(a_sa)]],
  ('L', 'Z') : [[left(a_sb), right(a_ec)], [left(a_ec), right(a_sc)]],
  ('L', 'X') : [[left(a_sb), right(a_ec)], [left(a_ec), right(a_sc)]],
  ('L', 'U') : [[left(a_sb), right(a_sa)], [left(a_ec), right(a_sb)]],
  ('L', 'D') : [[left(a_sb), right(a_sa)], [left(a_ec), right(a_sb)]],
  ('L', 'CL') : [[left(a_sb), right(a_sb)]],
  ('L', 'CH') : [[left(a_sb), right(a_sa)]],
  
  ('H', 'H') : [[left(a_sa), right(a_sa)]],
  ('H', 'Z') : [[left(a_sa), right(a_ec)], [left(a_ec), right(a_sc)]],
  ('H', 'X') : [[left(a_sa), right(a_ec)], [left(a_ec), right(a_sc)]],
  ('H', 'U') : [[left(a_sa), right(a_sb)], [left(a_ec), right(a_sa)]],
  ('H', 'D') : [[left(a_sa), right(a_sb)], [left(a_ec), right(a_sa)]],
  ('H', 'CL') : [[left(a_sa), right(a_sb)]],
  ('H', 'CH') : [[left(a_sa), right(a_sa)]],

  ('Z', 'Z') : [[left(a_sc), right(a_sc)]],
  ('Z', 'X') : [[left(a_sc), right(a_sc)]],
  ('Z', 'U') : [[left(a_sc), right(a_ec)], [left(a_ec), right(a_sb)], [left(a_ec), right(a_sa)]],
  ('Z', 'D') : [[left(a_sc), right(a_ec)], [left(a_ec), right(a_sb)], [left(a_ec), right(a_sa)]],
  ('Z', 'CL') : [[left(a_sc), left(a_sb)], [left(a_sb), right(a_sb)]],
  ('Z', 'CH') : [[left(a_sc), left(a_sa)], [left(a_sa), right(a_sa)]],

  ('X', 'X') : [[left(a_sc), right(a_sc)]],
  ('X', 'U') : [[left(a_sc), right(a_ec)], [left(a_ec), right(a_sb)], [left(a_ec), right(a_sa)]],
  ('X', 'D') : [[left(a_sc), right(a_ec)], [left(a_ec), right(a_sb)], [left(a_ec), right(a_sa)]],
  ('X', 'CL') : [[left(a_sc), left(a_sb)], [left(a_sb), right(a_sb)]],
  ('X', 'CH') : [[left(a_sc), left(a_sa)], [left(a_sa), right(a_sa)]],

  ('U', 'U') : [[left(a_sb), right(a_sb)], [left(a_sa), right(a_sa)]],
  ('U', 'D') : [[left(a_sa), right(a_sb)], [left(a_sb), right(a_sa)]],
  ('U', 'CL') : [[left(a_sa), right(a_sb)], [left(a_sb), right(a_ec)]],
  ('U', 'CH') : [[left(a_sb), right(a_sa)], [left(a_sa), right(a_ec)]],

  ('D', 'D') : [[left(a_sa), right(a_sb)], [left(a_sb), right(a_sa)]],
  ('D', 'CL') : [[left(a_sa), left(a_sb)], [left(a_sb), right(a_sb)]],
  ('D', 'CH') : [[left(a_sa), left(a_sb)], [left(a_sa), right(a_sa)]],

  ('CL', 'Z') : [[left(a_sc), left(a_sb)], [left(a_sc), right(a_sc)]],
  ('CL', 'X') : [[left(a_sc), left(a_sb)], [left(a_sc), right(a_sc)]],
  ('CH', 'D') : [[left(a_sa), left(a_sb)], [left(a_sb), right(a_sb)], [left(a_sa), right(a_sa)]],
  ('CL', 'CL') : [[left(a_sb), right(a_sb)]],
  ('CL', 'CH') : [[left(a_sb), left(a_sa)], [left(a_sa), right(a_sa)]],

  ('CH', 'Z') : [[left(a_sc), left(a_sa)], [left(a_sc), right(a_sc)]],
  ('CH', 'X') : [[left(a_sc), left(a_sa)], [left(a_sc), right(a_sc)]],
  ('CH', 'D') : [[left(a_sa), left(a_sb)], [left(a_sb), right(a_sb)], [left(a_sa), right(a_sa)]],
  ('CH', 'CH') : [[left(a_sa), right(a_sa)]],
  ('CH', 'CL') : [[left(a_sa), left(a_sb)], [left(a_sb), right(a_sb)]],
}

transition_backgrounds = {
  ('U', 'S') : [(left(a_sb), a_eb, a_ea, left(a_sa))],
  ('U', 'L') : [(a_ec, left(a_sa), left(a_sb))],
  ('U', 'H') : [(a_ec, left(a_sa), left(a_sb))],  
  ('U', 'Z') : [(a_ec, left(a_sa), left(a_sb))],
  ('U', 'X') : [(a_ec, left(a_sa), left(a_sb))],  
  ('U', 'U') : [(left(a_sa), a_sa, a_sb, left(a_sb))],
  ('U', 'D') : [(a_ec, left(a_sa), left(a_sb))],  
  ('U', 'CH') : [(a_ec, left(a_sa), left(a_sb))],  
  ('U', 'CL') : [(a_ec, left(a_sa), left(a_sb))],
}