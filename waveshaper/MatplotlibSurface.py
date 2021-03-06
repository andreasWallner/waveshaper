import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

class MatplotlibSurface(object):
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.ax.set_axis_off()

    def __del__(self):
        plt.close(self.fig)

    def draw_line(self, c1, c2, color, linewidth):
        self.ax.plot(
            (c1.x, c2.x),
            (c1.y, c2.y),
            linewidth=linewidth,
            solid_capstyle='round',
            color=color)

    def draw_fill(self, vertices, color, linewidth):
        # convert OffsetCoord to tuples, add one last for CLOSEPOLY, value does not
        # matter since CLOSEPATH vertices are ignored anyway

        vertices = [v.tuple() for v in vertices] + [(0,0)]
        codes = [Path.MOVETO] + (len(vertices)-2)*[Path.LINETO] + [Path.CLOSEPOLY]
        path = Path(vertices, codes)
        patch = patches.PathPatch(
            path,
            facecolor = color,
            edgecolor = color,
            lw = linewidth,
            )
        self.ax.add_patch(patch)

    def draw_text(self, text, position):
        self.ax.text(
            position.x,
            position.y,
            text,
            horizontalalignment='center',
            verticalalignment='center',
            )

    def show(self, block = True):
        plt.show(block=block)

    def clear(self):
      self.ax.clear()
      self.ax.set_axis_off()
