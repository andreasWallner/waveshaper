import matplotlib.pyplot as plt

class MatplotlibSurface(object):
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect='equal')

    def draw_line(self, c1, c2):
        self.ax.plot((c1.x, c2.x), (c1.y, c2.y))

    def show(self):
        plt.show()
