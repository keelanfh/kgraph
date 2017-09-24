from LineGraph import LineGraph

# Basic syntax for a line graph
gr1 = LineGraph([(1, 1), (2, 4), (3, 3)])

# Some of the things you can change easily
gr1.lineweight = 5
gr1.x.label = 'This one thing'
gr1.y.label = 'Another thing'
gr1.title = 'A graph'
gr1.x.markers = [1, 2, 3]
gr1.x.markers.format([1, 2, 3], ['A', 'B', 'C'])

# Export to file
gr1.export(filename='gr1.svg')

gr2 = LineGraph([(1, 3), (2, 2), (3, 1)])
gr2.export(filename='gr2.svg')

# Add two graphs together
gr3 = gr1 + gr2
gr3.export(filename='gr3.svg')
