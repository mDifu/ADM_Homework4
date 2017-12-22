import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
    
def conferenceSubgraph(graph, conferences, conferenceId):
    ret= graph.subgraph(conferences[conferenceId])
    print("\nThis is the subgraph induced by the set of autor who published in the input conference, We took %d as conference" %(conferenceId))
    plt.clf()
    nx.draw_networkx(ret, node_size=15, with_labels= False)
    plt.show()
    return ret
    
def degree(graph):
    degree= sorted(list(nx.degree_centrality(graph).values()))[::-1]
    #histogram
    plt.hist(degree)
    plt.title("Nodes Degree(histogram)")
    plt.xlabel('Degree Centrality ')
    plt.ylabel('The Number of Nodes')
    plt.show()
    #loglog
    plt.loglog(degree, 'b', marker = 'o')
    plt.title("Nodes Degree(loglog scale)")
    plt.xlabel('The Number of Nodes')
    plt.ylabel('Degree Centrality ')
    plt.show()
    print("In the next graph node's size depends by their Dregree centrality")
    plt.figure(figsize=(6,6))
    pos_c= nx.spring_layout(graph, iterations = 1000)
    nsize = np.array([v for v in (list(nx.degree_centrality(graph).values()))])
    nsize = 600*(nsize  - min(nsize))/(max(nsize) - min(nsize))
    nodes=nx.draw_networkx_nodes(graph, pos = pos_c, node_size = nsize)
    nodes.set_edgecolor('b')
    nx.draw_networkx_edges(graph, pos = pos_c, alpha = .1)
    plt.axis('off') 
    plt.show()
        
def closeness(graph):
    closeness  = sorted(list(nx.closeness_centrality(graph).values()))[::-1]    
    plt.title("Clossness Centrality Plot (loglogscale)")
    plt.xlabel('number of nodes')
    plt.ylabel('Clossness Centrality')
    plt.loglog(closeness,marker='o')
    plt.show()    
    print("In the following graph node's size depends by their Closeness centrality")
    plt.figure(figsize=(6,6))
    pos_c= nx.spring_layout(graph, iterations = 1000)
    nsize = np.array([v for v in list(nx.closeness_centrality(graph).values())])
    nsize = 400*(nsize  - min(nsize))/(max(nsize) - min(nsize))
    nodes=nx.draw_networkx_nodes(graph, pos = pos_c, node_size = nsize)
    nodes.set_edgecolor('b')
    nx.draw_networkx_edges(graph, pos = pos_c, alpha = .1)
    plt.axis('off') 
    plt.show()
    
def betweenness(graph):
    betweenness= sorted(list(nx.betweenness_centrality(graph).values()))[::-1]
    plt.loglog(betweenness, marker = 'o')
    plt.title("Betweenness Centrality Plot (loglog scale)")
    plt.xlabel('Number of Nodes')
    plt.ylabel('Betweenness Centrality')
    plt.show()
    print("In the next graph node's size depends by their Betweenness centrality")
    plt.figure(figsize=(6,6))
    pos_c= nx.spring_layout(graph, iterations = 1000)
    nsize = np.array([v for v in list(nx.betweenness_centrality(graph).values())])
    nsize = 500*(nsize  - min(nsize))/(max(nsize) - min(nsize))
    nodes=nx.draw_networkx_nodes(graph, pos = pos_c, node_size = nsize)
    nodes.set_edgecolor('b')
    nx.draw_networkx_edges(graph, pos = pos_c, alpha = .1)
    plt.axis('off') 
    plt.show()

def ego_graph(graph, author, hops):
    print("The graph above is the ego graph of author with hop distance at most %d from author %d" %(hops, author))
    ego= nx.ego_graph(graph, author, radius=hops, center=True, undirected=False, distance=None)
    plt.clf()
    nx.draw_networkx(ego, node_size=3, with_labels= False)
    plt.show()
    return ego