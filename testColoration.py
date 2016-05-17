from graph_class import *

G=Graph(100,5)
G.erdosRenyi(3)
G.randomColoration()
#G.vizualisation()
G.metropolisAlgo(500)

