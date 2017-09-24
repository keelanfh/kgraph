from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# plt.style.use('ggplot')

graphs_used = 0


class Markers(object):
    def __init__(self, ax, direction):
        self.ax = ax
        self.direction = direction

    def format(self, from_list, to_list=False):
        if not to_list:
            to_list = from_list[1]
            from_list = from_list[0]

        def formatter(no, pos):
            for x in zip(from_list, to_list):
                if x[0] == no:
                    return x[1]
            return ""

        if self.direction == 'x':
            self.ax.xaxis.set_major_formatter(FuncFormatter(formatter))

    def __str__(self):
        return super


class Axis(object):
    def __init__(self, ax, direction):
        self.ax = ax
        self.direction = direction
        self._markers = Markers(ax, direction)

    def _set_label(self, text):
        if self.direction == 'x':
            self.ax.set_xlabel(text)
        elif self.direction == 'y':
            self.ax.set_ylabel(text)

    def _get_label(self):
        if self.direction == 'x':
            return self.ax.get_xlabel
        elif self.direction == 'y':
            return self.ax.get_ylabel

    label = property(_get_label, _set_label)

    def _set_range(self, arange):
        if self.direction == 'x':
            self.ax.set_xlim(arange)
        elif self.direction == 'y':
            self.ax.set_ylim(arange)

    def _get_range(self):
        if self.direction == 'x':
            return self.ax.get_xlim
        elif self.direction == 'y':
            return self.ax.get_ylim

    range = property(_get_range, _set_range)

    def _set_markers(self, alist):
        if self.direction == 'x':
            self.ax.set_xticks(alist)
        elif self.direction == 'y':
            self.ax.set_yticks(alist)

    def _get_markers(self):
        return self._markers

    markers = property(_get_markers, _set_markers)


class DataSet(object):
    def __init__(self, x_data, y_data, label=None, lw=None, color=None):
        self.x_data = x_data
        self.y_data = y_data
        self.label = label
        self.lw = lw
        self.color = color

    def __repr__(self):
        return "".join(["{x_data: ", self.x_data.__repr__(), ",\ny_data: ", self.y_data.__repr__(), "}"])


class LineGraph(object):
    graphs_used += 1
    def __init__(self, x_data, y_data=None, lw=2.5, *args, **kwargs):
        # LineGraph.instances += 1
        # self.plt = plt

        # If only one argument, convert to two
        if not y_data:
            x_data, y_data = zip(*x_data)

        self.data = [DataSet(x_data, y_data)]

        # Create the axes object
        self.fig = Figure()
        self.ax = self.fig.gca()
        self.canvas = FigureCanvas(self.fig)
        self._lineweight = lw
        self.x = Axis(self.ax, 'x')
        self.y = Axis(self.ax, 'y')
        self.ax.grid(b=False)
        self.ax.set_axis_bgcolor('white')
        for spine in ["top", "bottom", "left", "right"]:
            self.ax.spines[spine].set_visible(False)
        self.made = False

        # args and kwargs

    def make(self):
        # Need a better way of defining 'ax' object (need a new one by default)
        self.made = True
        for dataset in self.data:
            self.ax.plot(dataset.x_data, dataset.y_data, label=1,
                         lw=self.lineweight)

    def _get_lineweight(self):
        return self._lineweight

    def _set_lineweight(self, lineweight):
        self._lineweight = lineweight

    lineweight = property(_get_lineweight, _set_lineweight)

    def _get_title(self):
        return self.ax.get_title()

    def _set_title(self, text):
        self.ax.set_title(text, y=1.05)

    title = property(_get_title, _set_title)

    def show(self):
        #TODO not working at present
        if self.made:
            raise Exception('.show() call must be made after changes to plot')
        self.make()
        self.plt.show()

    def export(self, filename=None, websafe=False, format='svg'):
        self.make()
        if not filename:
            filename = self.title + '.svg'
        if websafe:
            filename = filename.replace(' ', '-')
        self.fig.savefig(filename, format=format)

    def colors(self):
        pass

    def __add__(self, other):
        self.data += other.data
        return self
