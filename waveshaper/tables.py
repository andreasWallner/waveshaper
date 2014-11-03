from .OffsetCoord import *

def lsum(l1, l2):
  ''' build sum of two OffsetCoords'''
  return (lambda width, env: l1(width, env) + l2(width, env))
 
def end(l):
  ''' move OffsetCoord to the end of a symbol and mirror it'''
  return (lambda width, env: OffsetCoord(width * env['bitwidth'], 0) - l(width, env))

def mirror(l):
  ''' returns lambda that mirrors point around the origin, use for transitions'''
  return (lambda width, env: -l(width, env))

def left(l):
  ''' returns lambda that calculates point left of a transition center'''
  return (lambda width, env: -l(width, env))
 
def right(l):
  ''' returns lambda that calculates point right of transition center'''
  return (lambda width, env: l(width, env))

def combinate(d1, d2):
  result = {}
  for foo in d1:
    for bar in d2:
      result[foo + bar] = lsum(d1[foo], d2[bar])
  return result

def mirror_path(path):
  """ mirrors a single transition path """
  points, env = path
  
  points = [mirror(p) for p in points]
  if env == 'c':
    env = 'l'
  elif env == 'l':
    env = 'c'
  else:
    raise Exception('unknown env in table')

  return (points, env)

def _populate_mirrored(table):
  """ create mirrored paths for each tuple that does not exist """
  complete = {}
  for key, paths in table.items():
    complete[key] = paths;

    # most likely a symbol background
    print(key)
    if not isinstance(key, tuple):
      continue
    print(key)

    swapped = (key[1], key[0])

    # check if mirrored is defined
    # if yes, skip item, otherwise produce mirrored
    if swapped in table:
      next
    
    mirrored = []
    for path in paths:
      mirrored.append(mirror_path(path))

    complete[swapped] = mirrored
    
  return complete
  

y_offsets = {
  'c' : (lambda width, env: OffsetCoord(0, 0)),
  'b' : (lambda width, env: OffsetCoord(0, -env['lineheight'] / 2)),
  'a' : (lambda width, env: OffsetCoord(0, env['lineheight'] / 2)),
}
 
x_offsets = {
  'e' : (lambda width, env: OffsetCoord(0, 0)),
  's' : (lambda width, env: OffsetCoord(env['lineheight'] * env['slope'], 0)),
  'm' : (lambda width, env: OffsetCoord(env['lineheight'] * env['slope'] / 2, 0)),
  'c' : (lambda width, env: OffsetCoord(width * env['bitwidth'] / 2, 0)),
}

anchors = combinate(x_offsets, y_offsets)
locals().update({'a_' + x : anchors[x] for x in anchors})

""" table that defines the symbol emitted by instructions
 like toggle or clock
 the format:
  {
    instruction : {
      last symbol : next symbol,
      ...
    },
    ...
  }
""" 
follow_symbol = {
  'C' : {
    'CL' : 'CH',
    'CH' : 'CL',
    'S' : 'CL',
    '' : 'CL',
    },
  'T' : {
    'L' : 'H',
    'H' : 'L',
    '' : 'L',
  }
}

""" available symbols and their shapes """
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

""" transitions between symbols 
  mirrored transitions are built afterwards
  
  format:
    {
      (from_symbol, to_symbol) : [
        ([point1, point2, ...], environment),
        ...
        ],
        ...
      }
"""
transitions = {
  ('S', 'S') : [],
  ('S', 'L') : [
    ([left(a_eb), right(a_sb)], 'c'),
    ],
  ('S', 'H') : [
    ([left(a_ea), right(a_sa)], 'c'),
    ],
  ('S', 'Z') : [
    ([left(a_ec), right(a_sc)], 'c'),
    ],
  ('S', 'X') : [
    ([left(a_ec), right(a_sc)], 'c'),
    ],
  ('S', 'U') : [
    ([left(a_eb), right(a_sb)], 'c'),
    ([left(a_ea), right(a_sa)], 'c'),
    ],
  ('S', 'D') : [
    ([right(a_sb), right(a_ec), right(a_sa)], 'c'),
    ],
  ('S', 'CL') : [
    ([left(a_eb), right(a_sb)], 'c'),
    ],
  ('S', 'CH') : [
    ([left(a_ea), right(a_sa)], 'c'),
    ],

  ('L', 'L') : [
    ([left(a_sb), right(a_sb)], 'c'),
    ],
  ('L', 'H') : [
    ([left(a_sb), right(a_sa)], 'c'),
    ],
  ('L', 'Z') : [
    ([left(a_sb), right(a_ec)], 'c'),
    ([left(a_ec), right(a_sc)], 'c'),
    ],
  ('L', 'X') : [
    ([left(a_sb), right(a_ec)], 'c'),
    ([left(a_ec), right(a_sc)], 'c'),
    ],
  ('L', 'U') : [
    ([left(a_sb), right(a_sa)], 'c'),
    ([left(a_ec), right(a_sb)], 'c'),
    ],
  ('L', 'D') : [
    ([left(a_sb), right(a_sa)], 'c'),
    ([left(a_ec), right(a_sb)], 'c'),
    ],
  ('L', 'CL') : [
    ([left(a_sb), right(a_sb)], 'c'),
    ],
  ('L', 'CH') : [
    ([left(a_sb), right(a_sa)], 'c'),
    ],
  
  ('H', 'H') : [
    ([left(a_sa), right(a_sa)], 'c'),
    ],
  ('H', 'Z') : [
    ([left(a_sa), right(a_ec)], 'c'),
    ([left(a_ec), right(a_sc)], 'c'),
    ],
  ('H', 'X') : [
    ([left(a_sa), right(a_ec)], 'c'),
    ([left(a_ec), right(a_sc)], 'c'),
    ],
  ('H', 'U') : [
    ([left(a_sa), right(a_sb)], 'c'),
    ([left(a_ec), right(a_sa)], 'c'),
    ],
  ('H', 'D') : [
    ([left(a_sa), right(a_sb)], 'c'),
    ([left(a_ec), right(a_sa)], 'c'),
    ],
  ('H', 'CL') : [
    ([left(a_sa), right(a_sb)], 'c'),
    ],
  ('H', 'CH') : [
    ([left(a_sa), right(a_sa)], 'c'),
    ],

  ('Z', 'Z') : [
    ([left(a_sc), right(a_sc)], 'c'),
    ],
  ('Z', 'X') : [
    ([left(a_sc), right(a_sc)], 'c'),
    ],
  ('Z', 'U') : [
    ([left(a_sc), right(a_ec)], 'c'),
    ([left(a_ec), right(a_sb)], 'c'),
    ([left(a_ec), right(a_sa)], 'c'),
    ],
  ('Z', 'D') : [
    ([left(a_sc), right(a_ec)], 'c'),
    ([left(a_ec), right(a_sb)], 'c'),
    ([left(a_ec), right(a_sa)], 'c'),
    ],
  ('Z', 'CL') : [
    ([left(a_sc), left(a_sb)], 'c'),
    ([left(a_sb), right(a_sb)], 'c'),
    ],
  ('Z', 'CH') : [
    ([left(a_sc), left(a_sa)], 'c'),
    ([left(a_sa), right(a_sa)], 'c'),
    ],

  ('X', 'X') : [
    ([left(a_sc), right(a_sc)], 'c'),
    ],
  ('X', 'U') : [
    ([left(a_sc), right(a_ec)], 'c'),
    ([left(a_ec), right(a_sb)], 'c'),
    ([left(a_ec), right(a_sa)], 'c'),
    ],
  ('X', 'D') : [
    ([left(a_sc), right(a_ec)], 'c'),
    ([left(a_ec), right(a_sb)], 'c'),
    ([left(a_ec), right(a_sa)], 'c'),
    ],
  ('X', 'CL') : [
    ([left(a_sc), left(a_sb)], 'c'),
    ([left(a_sb), right(a_sb)], 'c'),
    ],
  ('X', 'CH') : [
    ([left(a_sc), left(a_sa)], 'c'),
    ([left(a_sa), right(a_sa)], 'c'),
    ],

  ('U', 'U') : [
    ([left(a_sb), right(a_sb)], 'c'),
    ([left(a_sa), right(a_sa)], 'c'),
    ],
  ('U', 'D') : [
    ([left(a_sa), right(a_sb)], 'c'),
    ([left(a_sb), right(a_sa)], 'c'),
    ],
  ('U', 'CL') : [
    ([left(a_sa), right(a_sb)], 'c'),
    ([left(a_sb), right(a_ec)], 'c'),
    ],
  ('U', 'CH') : [
    ([left(a_sb), right(a_sa)], 'c'),
    ([left(a_sa), right(a_ec)], 'c'),
    ],

  ('D', 'D') : [
    ([left(a_sa), right(a_sb)], 'c'),
    ([left(a_sb), right(a_sa)], 'c'),
    ],
  ('D', 'CL') : [
    ([left(a_sa), left(a_sb)], 'c'),
    ([left(a_sb), right(a_sb)], 'c'),
    ],
  ('D', 'CH') : [
    ([left(a_sa), left(a_sb)], 'c'),
    ([left(a_sa), right(a_sa)], 'c'),
    ],

  ('CL', 'Z') : [
    ([left(a_sc), left(a_sb)], 'c'),
    ([left(a_sc), right(a_sc)], 'c'),
    ],
  ('CL', 'X') : [
    ([left(a_sc), left(a_sb)], 'c'),
    ([left(a_sc), right(a_sc)], 'c'),
    ],
  ('CH', 'D') : [
    ([left(a_sa), left(a_sb)], 'c'),
    ([left(a_sb), right(a_sb)], 'c'),
    ([left(a_sa), right(a_sa)], 'c'),
    ],
  ('CL', 'CL') : [
    ([left(a_sb), right(a_sb)], 'c'),
    ],
  ('CL', 'CH') : [
    ([left(a_sb), left(a_sa)], 'c'),
    ([left(a_sa), right(a_sa)], 'c'),
    ],

  ('CH', 'Z') : [
    ([left(a_sc), left(a_sa)], 'c'),
    ([left(a_sc), right(a_sc)], 'c'),
    ],
  ('CH', 'X') : [
    ([left(a_sc), left(a_sa)], 'c'),
    ([left(a_sc), right(a_sc)], 'c'),
    ],
  ('CH', 'D') : [
    ([left(a_sa), left(a_sb)], 'c'),
    ([left(a_sb), right(a_sb)], 'c'),
    ([left(a_sa), right(a_sa)], 'c'),
    ],
  ('CH', 'CH') : [
    ([left(a_sa), right(a_sa)], 'c'),
    ],
  ('CH', 'CL') : [
    ([left(a_sa), left(a_sb)], 'c'),
    ([left(a_sb), right(a_sb)], 'c'),
    ],
}
transitions = _populate_mirrored(transitions)

backgrounds = {
  'U' : [
    ([a_sa, end(a_sa), end(a_sb), a_sb], 'c')
    ],

  ('U', 'S') : [
    ([left(a_sb), a_eb, a_ea, left(a_sa)], 'c'),
    ],
  ('U', 'L') : [
    ([a_ec, left(a_sa), left(a_sb)], 'c'),
    ],
  ('U', 'H') : [
    ([a_ec, left(a_sa), left(a_sb)], 'c'),
    ],

  ('U', 'Z') : [
    ([a_ec, left(a_sa), left(a_sb)], 'c'),
    ],
  ('U', 'X') : [
    ([a_ec, left(a_sa), left(a_sb)], 'c'),
    ],

  ('U', 'U') : [
    ([left(a_sa), a_sa, a_sb, left(a_sb)], 'c'),
    ],
  ('U', 'D') : [
    ([a_ec, left(a_sa), left(a_sb)], 'c'),
    ],

  ('U', 'CH') : [
    ([a_ec, left(a_sa), left(a_sb)], 'c'),
    ],

  ('U', 'CL') : [
    ([a_ec, left(a_sa), left(a_sb)], 'c'),
    ],
}
backgrounds = _populate_mirrored(backgrounds)
