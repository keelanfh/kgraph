# kgraph
A simple wrapper for matplotlib. Helps to make simple graphs easily, without having to deal with `ax`, `plt`, and all that fun stuff. I put it together when I got fed up with a lot of the syntax on a datavis project.

# Simple use:
`from LineGraph import LineGraph`

`lg = LineGraph([[1,1],[2,2],[3,3]])`

`lg.export('example')`

# List of features available:

Unless otherwise stated, simply assign values to these attributes.

`lg = LineGraph()` - can be set with data as a list of tuples, two lists of matching data, or no data at all (placeholder data will appear).

`lg.title` - set the title

`lg.x.label` and `lg.y.label` - set axis labels

`lg.x.range` - set x axis range

`lg.x.markers` - set x axis markers

`lg.x.markers.format()` - pass a pair of lists describing marker formatting, i.e. if you want numbers mapped to letters, call `lg.x.markers.format([1,2,3],['A','B','C'])`. Alternatively, you can pass a list of tuples, or a function that described the mapping.

`lg2 = LineGraph()`

`lg += lg2`

This is the way to add mutiple data series to the same plot.

New features may be added at any time.
