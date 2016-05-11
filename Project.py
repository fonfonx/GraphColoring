# -*- coding: utf-8 -*-
"""
Created on Sun May  8 17:28:08 2016

@author: Antoine
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
   

    
# Input : Adjacent matrix and color list
# Output : Random graph and first distance for this random graph
def algo(matrix, cList):
    
    n = len(matrix)
    graph = nx.Graph()
    nodeList = list()
    colors = list()
    
    for i in range(n):
        for j in range(i,n):
            if (matrix[i][j] == 1):
                c1 = random.choice(cList)
                #graph.add_node(i+1, color = c1)
                if (i+1 in nodeList) == False:
                    nodeList.append(i+1)
                    colors.append(c1)
                    graph.add_node(i+1, color = c1)
                
                c2 = random.choice(cList)
                if (j+1 in nodeList) == False:
                    nodeList.append(j+1)
                    colors.append(c2)
                    graph.add_node(j+1, color = c2)
                
                graph.add_edge(i+1,j+1)
    
    pos=nx.circular_layout(graph)
    plt.figure(3,figsize=(12,9))  
        
    for nodes in graph.nodes():
        nx.draw_networkx_nodes(graph, pos, nodelist=[nodes], node_color=graph.node[nodes]['color'])
    nx.draw_networkx_edges(graph, pos)      
    plt.axis('off')
    plt.draw()    
    """
    print 'Unconnected nodes are not drawn as they can be trivialy coloured'
    print graph.node[1]['color']
    print graph.node[2]['color']
    print graph.nodes()
    print nodeList
    print colors
    print graph.edges()
    """
    distance = 0
    for (u,v) in graph.edges():
        if graph.node[u]['color'] == graph.node[v]['color']:
            distance += 1
                     
    print distance
    
    return nodeList, colors, graph.edges()
    """
    for i in range(10):    
        v = random.choice(graph.nodes())
        cListBis = cList
        cListBis.remove(graph.node[v]['color'])
        newColor = random.choice(cListBis)
        graph.node[v]['color'] = newColor
        
        newDistance = 0
        for (u,v) in graph.edges():
            if graph.node[u]['color'] == graph.node[v]['color']:
                newDistance += 1
        
        if newDistance <= distance :
            pos=nx.random_layout(graph)
            plt.figure(3,figsize=(12,9))          
            for nodes in graph.nodes():
                nx.draw_networkx_nodes(graph, pos, nodelist=[nodes], node_color=graph.node[nodes]['color'])
            nx.draw_networkx_edges(graph, pos)      
            plt.axis('off')
            plt.draw()    
"""           
    
# TODO : Pas fini du tout
def opti(nodeList, colorList, edgeList, cList, firstDistance):
    #Only recheck for node with new color
    for i in range(10):    
        v = random.randint(0, len(nodeList))
        
        currentDistance = 0
                
        cListBis = cList
        cListBis.pop(i)
        newColor = random.choice(cListBis)
        colorList[i] = newColor
        
        newDistance = 0
        for (u,v) in graph.edges():
            if graph.node[u]['color'] == graph.node[v]['color']:
                newDistance += 1
        
        if newDistance <= distance :
            pos=nx.random_layout(graph)
            plt.figure(3,figsize=(12,9))          
            for nodes in graph.nodes():
                nx.draw_networkx_nodes(graph, pos, nodelist=[nodes], node_color=graph.node[nodes]['color'])
            nx.draw_networkx_edges(graph, pos)      
            plt.axis('off')
            plt.draw()    
    
