import matplotlib.pyplot
from matplotlib.ticker import FuncFormatter

# A wrapper for matplotlib
# Designed to make plotting as easy as possible:
# myPerfectlyCorrelatedData = [(1,1),(2,2),(3,3)]
# myBeautifulGraph = LineGraph(myPerfectlyCorrelatedData)
# myBeautifulGraph.show()

# TODO examine behaviour when changes are made to graph etc. We need to ensure all of these are passed appropriately.
# TODO sort out colours. Need to have nice default colours.

# Set the style used to ggplot. Other styles are available.
matplotlib.pyplot.style.use('ggplot')


class DeletedException(Exception):
    def __init__(self):
        raise Exception('Object has been combined into another object - use that object instead')


class NotAxException(Exception):
    def __init__(self):
        raise Exception('ax object is an instance of matplotlib.Axes - you can\'t set it to something else.')


class NotAxisException(Exception):
    def __init__(self):
        raise Exception('You can\'t set x or y axes to values. Add data using LineGraph() constructor instead.')


class NotFunctionException(Exception):
    def __init__(self):
        raise Exception(
            'You can format using either a function, or a pair of lists describing the translation you want to make to your markers.')


class Markers(object):
    def __init__(self):
        self._markers = None
        self._formatter = None

    def format(self, function_or_from_list, to_list=None):
        if callable(function_or_from_list):
            self._formatter = lambda x, pos: function_or_from_list(x)

        elif to_list is not None:
            def formatter(no, pos):
                for x in zip(function_or_from_list, to_list):
                    if x[0] == no:
                        return x[1]
                return ""

            self._formatter = formatter

        else:
            raise NotFunctionException


class Axis(object):
    def __init__(self, direction):
        self.direction = direction
        self.label = None
        self.range = None
        self._markers = Markers()

    def _get_markers(self):
        return self._markers

    def _set_markers(self, value):
        self._markers._markers = value

    markers = property(_get_markers, _set_markers)


class DataSet(object):
    def __init__(self, x_data, y_data, label=None, weight=None, color=None, *args, **kwargs):
        self.x_data = x_data
        self.y_data = y_data
        self.label = label
        self.weight = weight
        self.color = color
        self.args = args
        self.kwargs = kwargs


class LineGraph(object):
    # Set default values for parameters
    weight = 2.5
    background = 'white'
    grid = False
    color = 'blue'

    def __init__(self, x_data=None, y_data=None, label=None, weight=weight, color=color, *args, **kwargs):

        _default = False

        # Set up a graph with some default data if no data is provided.
        if x_data is None:
            _default = True
            x_data, y_data = range(1, 13), [-32.1, -44.3, -57.9, -64.7, -65.6, -65.2, -66.9, -67.6, -66., -57.1, -43.3,
                                            -32.1]

        # Zip the data if passed as a single list.
        if y_data is None:
            x_data, y_data = zip(*x_data)

        # Create a new dataset with all the information passed to this graph.
        self._data = [DataSet(x_data, y_data, label=label, weight=weight, color=color, *args, **kwargs)]

        # Create the things that will be relevant for the WHOLE GRAPH here.
        # Initialise the axis object, which will initially be None.
        self._ax = None
        # Alias plt
        self.plt = matplotlib.pyplot
        # Set title to None
        self.title = None
        # Set grid and bgcolor from the class variables.
        self.grid = LineGraph.grid
        self.background = LineGraph.background
        self._deleted = False
        self._plotted = False

        # Create Axis objects.
        self._x = Axis('x')
        self.y = Axis('y')

        if _default:
            months = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Dec']
            self.x.markers.format(range(1, 12), months[1:])
            self.title = 'Average daily temperature at Vostok Station, Antartica'
            self.y.label = 'Temperature (degrees C)'

    def _get_x(self):
        return self._x

    def _set_x(self, *args, **kwargs):
        raise NotAxisException

    x = property(_get_x, _set_x)

    def _get_ax(self):
        # _get_ax will be called when attributes of the axis are to be changed.
        # This function needs to raise DeletedException.
        if self._deleted:
            raise DeletedException

        if self._ax is None:
            self._ax = self.plt.figure().gca()
            self.ax.grid(b=False)
            self.ax.set_axis_bgcolor(self.background)
        return self._ax

    def _set_ax(self, *args, **kwargs):
        raise NotAxException

    ax = property(_get_ax, _set_ax)

    def _get_data(self):
        if self._deleted:
            raise DeletedException
        return self._data[0]

    def _set_data(self, *args, **kwargs):
        raise Exception('Can\'t set data!')

    data = property(_get_data, _set_data)

    def _plot(self):
        # """Plots the graph using matplotlib's ax methods.
        # Information from the DataSet object is passed."""

        if not self._plotted:
            self._plotted = True

            if self._deleted:
                raise DeletedException
            for dataset in self._data:
                self.ax.plot(dataset.x_data, dataset.y_data, label=dataset.label, lw=dataset.weight,
                             color=dataset.color, *dataset.args, **dataset.kwargs)
            self.ax.set_title(self.title, y=1.05)
            if self.x.label is not None:
                self.ax.set_xlabel(self.x.label)
            if self.y.label is not None:
                self.ax.set_ylabel(self.y.label)

            try:
                self.ax.set_xticks(self.x.markers._markers)
            except TypeError:
                pass

            try:
                self.ax.set_yticks(self.y.markers._markers)
            except TypeError:
                pass

            if self.x.markers._formatter is not None:
                self.ax.xaxis.set_major_formatter(FuncFormatter(self.x.markers._formatter))
            if self.y.markers._formatter is not None:
                self.ax.yaxis.set_major_formatter(FuncFormatter(self.y.markers._formatter))

            self.ax.set_xlim(self.x.range)
            self.ax.set_ylim(self.y.range)

    def show(self):
        if self._deleted:
            raise DeletedException
        self._plot()
        self.plt.show()

    def export(self, filename=None, filetype='svg'):
        if self._deleted:
            raise DeletedException
        self._plot()
        if filename is None:
            filename = self.title.replace(' ', '-') + '.' + filetype
        self.plt.savefig(filename, format=filetype)

    def __add__(self, other):
        assert isinstance(other, LineGraph)

        # Combine the data together
        self._data += other._data

        # Change the title if something sensible is passed.
        if other.title is not None:
            self.title = other.title

        other._deleted = True
        return self  # Sample usage


if __name__ == '__main__':
    something = LineGraph()
    something.show()
    # something = LineGraph2([(1, 3), (2, 2), (3, 1)])
    # someOtherThing = LineGraph2([(5, 2), (3, 4), (6, 8)])
    # something += someOtherThing
    # something.title = 'This'
    # something.x.label = 'Whatever'
    # something.y.label = 'Another'
    # something.x.markers = [2, 3, 4, 5]
    # something.x.markers.format([2, 3, 4], ['a', 'b', 'c'])
    # something.x.range = [2, 5]
    # something.export()
