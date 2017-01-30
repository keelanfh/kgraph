# kgraph
A simple wrapper for matplotlib. Helps to make simple graphs easily, without having to deal with ax, plt, and all that fun stuff.

# Simple use:
`from kgraph import LineGraph`
`lg = LineGraph([1,1],[2,2],[3,3])`
`lg.show()`

# List of features available:

Unless otherwise stated, simply assign values to these attributes.

`lg.title` - set the title
`lg.x.label` and `lg.y.label` - set axis labels
`lg.x.range` - set x axis range
`lg.x.markers` - set x axis markers
`lg.x.markers.format()` - pass a pair of lists describing marker formatting, i.e. if you want numbers mapped to letters, call `lg.x.markers.format([1,2,3],[4,5,6])`


This is very much under development and new features may be added at any time.
