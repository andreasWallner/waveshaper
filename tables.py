from OffsetCoord import *

anchors = {
    'ea' : (lambda width, env : OffsetCoord(0, env.lineheight / 2)),
    'ec' : (lambda width, env : OffsetCoord(0, 0)),
    'eb' : (lambda width, env : OffsetCoord(0, -env.lineheight / 2)),
    'ba' : (lambda width, env : OffsetCoord(env.lineheight * env.slope * 0.5, env.lineheight / 2)),
    'bc' : (lambda width, env : OffsetCoord(env.lineheight * env.slope * 0.5, 0)),
    'bb' : (lambda width, env : OffsetCoord(env.lineheight * env.slope * 0.5, -env.lineheight / 2)),
    'ca' : (lambda width, env : OffsetCoord(width * env.bitwidth, env.lineheight / 2)),
    'cc' : (lambda width, env : OffsetCoord(width * env.bitwidth, 0)),
    'cb' : (lambda width, env : OffsetCoord(width * env.bitwidth, -env.lineheight / 2)),
}

symbols = {
    'S' : [],
    'L' : [('bb', 'bb')],
    'H' : [('ba', 'ba')],
}

transitions = {
    ('S', 'L') : [('eb', 'bb')],
    ('S', 'H') : [('ea', 'ba')],
    ('L', 'S') : [('bb', 'eb')],
    ('H', 'S') : [('ba', 'ea')],
    ('L', 'H') : [('bb', 'ba')],
    ('L', 'L') : [('bb', 'bb')],
    ('H', 'H') : [('ba', 'ba')],
    ('H', 'L') : [('ba', 'bb')],
}
