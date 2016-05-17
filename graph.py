# -*- coding: utf-8 -*-

from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random


# build an ER graph
def graphBuild(N,c):
    graph = nx.erdos_renyi_graph(N,c/N)
    edges = graph.edges()
    mat = adjMatrix(N,edges)
    return mat


# Input : List of edges
# Output : adjacency matrix
def adjMatrix(n, edges):
    matrix = np.zeros((n,n))
    for (a, b) in edges:
        matrix[a,b] = 1
        matrix[b,a] = 1
    return matrix

# Input : Number of nodes, List of edges
# Outputs the corresponding graph, without coloration
def draw_graph(n, edges):
    nodes=range(n)
    G=nx.Graph()
    for node in nodes: G.add_node(node)
    for edge in edges: G.add_edge(edge[0], edge[1])
    pos = nx.shell_layout(G)
    nx.draw(G, pos)
    plt.show()



# Input: Number of colors
# Output : List of n random colors
# TODO : Find a way to have 0 repetition
def makeColor(n):
    cList = []
    these = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for i in range(n):
        fff = []
        for z in xrange(6):
            fff.append(these[random.randint(0,15)])
            ccc = ''.join(fff)
        color = '#' + ccc
        cList.append(color)
    return cList

# Input : Number of colors (3, 5 or 7 for the project)
# Output : List of 3, 5 or 7 colors (chosen in advance)
def colorChoice(n):
    cList = ['#46b94a', '#ff4e50', '#d62971', '#25a1da', '#47f00f', '#345acb', '#fbb904']
    return cList[:n]

# Input : List of nodes, their color and list of edges (ie all info about a graph)
# Output : Corresponding graph with coloration
def draw(nodeList, colorList, edgeList):
    graph = nx.Graph()
    for node in nodeList:
        graph.add_node(node, color = colorList[node])

    for edge in edgeList:
        graph.add_edge(edge[0], edge[1])

    pos=nx.spring_layout(graph)
    plt.figure(3,figsize=(12,9))

    nx.draw_networkx_nodes(graph,pos,nodelist=nodeList,node_color=colorList)

    nx.draw_networkx_edges(graph, pos)
    plt.axis('off')
    plt.draw()
    plt.show()

# Input: coloration (vectors of integers representing colors) and list of all possible colors
# Output: list of colors corresponding to the coloration
def colorList(coloration, cList):
    return [cList[i] for i in coloration]



# Input : Max nb of nodes you want (1000 in our case)
# Output : Parameters for the Erdős-Rényi model : Nb of nodes and proba
def erdosRenyiParam(nb):
    n = random.randint(1,nb)
    p = random.random()
    return (n, p)

# Input : n, p from Erdos Renyi
# Output : List of edges following the Erdős-Rényi model
def randomGraph(n, p):
    vertices = [i for i in range(n)]
    edges = [(i, j) for i in xrange(n) for j in xrange(i) if random.random() < p]
    return edges

