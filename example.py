from LineGraph import LineGraph

# Let's say you've got some data:

x = [1,2,3,4,5,6,7,8,9,10]
y = [2,4,5,6,6,7,8,9,1,3]

# You want to make a graph.
# Just try this:

LineGraph(x,y).export('example1')

# Check it out - you should see a new file!

# No titles though... let's sort that:

gr1 = LineGraph(x,y)

gr1.title = 'A graph'
gr1.x.label = 'This one thing'
gr1.y.label = 'Another thing'

# And, if you want to sort anything else out:

gr1.lineweight = 5

# Like specifying where you want the markers to fall, or even formatting them
gr1.x.markers = [1, 2, 3]
gr1.x.markers.format([1, 2, 3], ['A', 'B', 'C'])

gr1.export('example2')

# You can even add graphs together if you have more data:
gr2 = LineGraph([(1, 3), (2, 2), (3, 1)])

gr3 = gr1 + gr2
gr3.export('example3')

# Want to access some more advanced functionality? ax is still there...

gr2.ax.axvline(2)

gr2.export('example4')
