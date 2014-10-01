#!/usr/bin/python
import sys
import waveshaper.tables as tables
import waveshaper.Painter as Painter
import io
import base64
from waveshaper.MatplotlibSurface import MatplotlibSurface
from waveshaper.RenderInstruction import RenderInstruction
from waveshaper.InstructionSequence import InstructionSequence

def plot_symbol(sym):
  s = MatplotlibSurface()
  env = Painter.Env()
  p = Painter.Painter(s)

  i = RenderInstruction(sym, 1)
  i.render_symbol(p)
  i.render_symbol_bg(p)

  s.ax.plot([0, 1], [.5, .5], linewidth=.2, color='grey')
  s.ax.plot([0, 1], [-.5, -.5], linewidth=.2, color='grey')
  s.ax.plot([0.2, 0.2], [.6, -.6], linewidth=.2, color='grey')
  s.ax.plot([0.8, 0.8], [.6, -.6], linewidth=.2, color='grey')

  s.ax.set_xlim([0, 1])
  s.ax.set_ylim([-.6, .6])

  imgdata = io.BytesIO()
  s.fig.set_size_inches([.5, .6])
  s.fig.savefig(imgdata, format='png')
  imgbase64 = base64.b64encode(imgdata.getvalue()).decode('utf-8')

  return imgbase64

def plot_transition(sym1, sym2):
  s = MatplotlibSurface()
  env = Painter.Env()
  p = Painter.Painter(s)

  i = [
    RenderInstruction(sym1, 1),
    RenderInstruction(sym2, 1),
    ]
  seq = InstructionSequence(i)

  try:
    seq.execute(p)
  except KeyError:
    s.ax.plot([0, 2], [.6, -.6], linewidth=.2, color='red')

  s.ax.plot([0, 2], [.5, .5], linewidth=.2, color='grey')
  s.ax.plot([0, 2], [-.5, -.5], linewidth=.2, color='grey')
  s.ax.plot([1, 1], [.6, -.6], linewidth=.2, color='grey')
  s.ax.plot([0.8, 0.8], [.6, -.6], linewidth=.2, color='grey')
  s.ax.plot([1.2, 1.2], [.6, -.6], linewidth=.2, color='grey')
  
  s.ax.set_xlim([0, 2])
  s.ax.set_ylim([-0.6, 0.6])

  imgdata = io.BytesIO()
  s.fig.set_size_inches([1, .6])
  s.fig.savefig(imgdata, format='png')
  imgbase64 = base64.b64encode(imgdata.getvalue()).decode('utf-8')

  return imgbase64

def plot_symbols(f):
  print('<table>', file=f)

  print('<tr>', file=f)
  for sym in sorted(tables.symbols.keys()):
    print('<td style="text-align:center">{0}</td>'.format(sym), file=f)

  print('</tr><tr>', file=f)

  for sym in sorted(tables.symbols.keys()):
    imgdata = plot_symbol(sym)

    tr = '<td><img src="data:image/png;base64,{img}"</img></td>'.format(img = imgdata)
    print(tr, file=f)

  print('</tr>', file=f)

  print('</table>', file=f)

def plot_transitions(f):
  print('<table>', file=f)

  print('<tr><td></td>', file=f)
  for sym in sorted(tables.symbols.keys()):
    print('<td style="text-align:center">{0}</td>'.format(sym), file=f)
  print('</tr>', file=f)

  for sym1 in sorted(tables.symbols.keys()):
    print('<tr>', file=f)
    print('<td>{0}</td>'.format(sym1), file=f)

    for sym2 in sorted(tables.symbols.keys()):
      imgdata = plot_transition(sym1, sym2)

      tr = '<td><img src="data:image/png;base64,{img}"</img></td>'.format(img=imgdata)
      print(tr, file=f)

    print('</tr>', file=f)




def main():
  with open('overview.html', mode='w') as f:
    print('<html><body>', file=f)
    plot_symbols(f)
    print('<br /><br />', file=f)
    plot_transitions(f)
    print('</body></html>', file=f)

if __name__ == '__main__':
  sys.exit(main())
