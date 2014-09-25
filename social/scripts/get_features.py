# import glob
# import re
# a = glob.glob("../raw/egonets/*.egonet")

# for i in a:
# 	temp = re.search(r'\d+', i)
# 	print temp.group(0)
# 	with open(i) as f:
# 		for line in f:
# 			print line

import igraph

from igraph import Graph

g = Graph()
g.add_vertices(1000)


with open('raw/egonets/0.egonet') as f:
	for i in f:
		line = i.split(':')
		inner = int(line[0])
		friends = line[1].strip('\n').split(' ')[1:]
		if len(friends) > 1:
			friends = [int(x) for x in friends]
			g.add_edges([(0,inner)])
			for friend in friends:
				g.add_edges([(inner,friend)])


layout = g.layout("kk")
igraph.plot(g, layout = layout)