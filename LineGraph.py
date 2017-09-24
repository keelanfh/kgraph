# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class MissingTitleException(Exception):
    pass

class Markers(object):
    """Class for axis markers.
    ax object passed from LineGraph.Axis object."""
    def __init__(self, ax, direction):
        self.ax = ax
        self.direction = direction

    def format(self, from_list, to_list=None, show_by_default=False):
        if not to_list:
            to_list = from_list[1]
            from_list = from_list[0]

        def formatter(no, pos):
            """Generate a formatter from two lists"""
            for x in zip(from_list, to_list):
                if x[0] == no:
                    return x[1]
            # Return the number if show_by_default is set
            if show_by_default:
                return no
            else:
                return ""

        if self.direction == 'x':
            self.ax.xaxis.set_major_formatter(FuncFormatter(formatter))
        elif self.direction == 'y':
            self.ax.yaxis.set_major_formatter(FuncFormatter(formatter))

    def __repr__(self):
        return super


class Axis(object):
    """Axis Object. Container for ax"""
    def __init__(self, ax, direction):
        self.ax = ax
        self.direction = direction
        self._markers = Markers(ax, direction)

    @property
    def label(self):
        if self.direction == 'x':
            return self.ax.get_xlabel
        elif self.direction == 'y':
            return self.ax.get_ylabel

    @label.setter
    def label(self, text):
        if self.direction == 'x':
            self.ax.set_xlabel(text)
        elif self.direction == 'y':
            self.ax.set_ylabel(text)


    @property
    def range(self, arange):
        if self.direction == 'x':
            self.ax.set_xlim(arange)
        elif self.direction == 'y':
            self.ax.set_ylim(arange)

    @range.setter
    def setter(self):
        if self.direction == 'x':
            return self.ax.get_xlim
        elif self.direction == 'y':
            return self.ax.get_ylim

    @property
    def markers(self):
        return self._markers

    @markers.setter
    def markers(self, alist):
        if self.direction == 'x':
            self.ax.set_xticks(alist)
        elif self.direction == 'y':
            self.ax.set_yticks(alist)

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
    def __init__(self, x_data, y_data=None, lw=2.5, *args, **kwargs):

        # If only one argument, convert to two
        if not y_data:
            x_data, y_data = zip(*x_data)

        self.data = [DataSet(x_data, y_data)]

        # Generate a Canvas -> Figure -> Axis group
        self.fig = Figure()
        self.ax = self.fig.gca()
        self.canvas = FigureCanvas(self.fig)

        # Set the lineweight at global level (for all DataSets in graph)
        self._lineweight = lw

        # Create Axis objects
        self.x = Axis(self.ax, 'x')
        self.y = Axis(self.ax, 'y')

        # Some formatting changes
        self.ax.grid(b=False)
        self.ax.set_axis_bgcolor('white')
        for spine in ["top", "bottom", "left", "right"]:
            self.ax.spines[spine].set_visible(False)
        # args and kwargs

    def make(self):
        # Need a better way of defining 'ax' object (need a new one by default)
        for dataset in self.data:
            self.ax.plot(dataset.x_data, dataset.y_data, label=1,
                         lw=self.lineweight)

    @property
    def lineweight(self):
        return self._lineweight

    @lineweight.setter
    def lineweight(self, lineweight):
        self._lineweight = lineweight

    @property
    def title(self):
        return self.ax.get_title()

    @title.setter
    def title(self, text):
        self.ax.set_title(text, y=1.05)

    def export(self, filename=None, websafe=False, format='svg'):
        """Exporting to a file"""
        self.make()
        if self.title and not filename:
            filename = self.title + "." + format
        elif not filename:
            raise MissingTitleException("Please supply graph title or filename.")
        if "." not in filename:
            filename += "." + format
        if websafe:
            filename = filename.replace(' ', '-')
        self.fig.savefig(filename, format=format)

    def __add__(self, other):
        self.data += other.data
        return self
