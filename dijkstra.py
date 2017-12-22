import numpy as np
import heapq

def dijkstra(graph,start, end):
    heap= []
    nodes= graph.nodes()
    if start not in nodes or end not in nodes:
        print("The node in input is not in the graph")
        return {}
    explored={start:0}
    unexplored = {key: np.Inf for key in nodes if key!=start}
    current= start
    while current!=end:
        for edge in graph.edges(current):
            other= edge[1]
            edgeWeight= graph.get_edge_data(current,other)["weight"]
            try:
                if explored[current]+edgeWeight < unexplored[other]:
                    unexplored[other]= explored[current]+edgeWeight
                    heapq.heappush(heap, (unexplored[other], other))
            except: continue #avoiding keyerror when a node is already explored
        while True:
            if len(heap)==0: return explored
            cWeight, current= heapq.heappop(heap)
            if current not in explored: break
        if cWeight== np.Inf: break
        else: 
            unexplored.pop(current, None)
            explored[current]= cWeight
    return explored

def shortestPathWeight(graph, author):
    print("Trying to reach Aris from author: %d" %(author))
    distances = dijkstra(graph, author, 256176)
    if 256176 not in distances:
        print("You can't reach Aris starting from this author.")
        return
    print("The weight of the shortest path between Aris and the other author is: "+ str(distances[256176]))
    return distances[256176]

def multisourceDijkstra(graph,startList):
    heap= []
    nodes= graph.nodes()
    explored={key:0 for key in startList if key in nodes}
    unexplored = {key: np.Inf for key in nodes if key not in startList}
    
    #mod the first part to make the algorithm multisource
    for starter in explored.keys():    
        for edge in graph.edges(starter):
            other= edge[1]
            edgeWeight= graph.get_edge_data(starter,other)["weight"]
            try:
                if edgeWeight < unexplored[other]:
                    unexplored[other]= edgeWeight
                    heapq.heappush(heap, (unexplored[other], other))
            except: continue #avoiding keyerror when a node is already explored
    #select the starter
    while True:
        if len(heap)==0: return explored
        cWeight, current= heapq.heappop(heap)
        if current not in explored: break
    if cWeight== np.Inf: return explored     #maybe useless
    else: 
        unexplored.pop(current, None)
        explored[current]= cWeight
    
    #classic Dijkstra
    while len(unexplored.keys())>0:
        for edge in graph.edges(current):
            other= edge[1]
            edgeWeight= graph.get_edge_data(current,other)["weight"]
            try:
                if explored[current]+edgeWeight < unexplored[other]: #cWeight instead of explored[current]
                    unexplored[other]= explored[current]+edgeWeight
                    heapq.heappush(heap, (unexplored[other], other))
            except: continue #avoiding keyerror when a node is already explored
        while True:
            if len(heap)==0: return explored
            cWeight, current= heapq.heappop(heap)
            if current not in explored: break
        if cWeight== np.Inf: break
        else: 
            unexplored.pop(current, None)
            explored[current]= cWeight
    return explored

def groupNumber(graph, sublist):
    number = {key: np.Inf for key in graph.nodes()}
    prov= multisourceDijkstra(graph, sublist)
    for key in prov:
        number[key]=min(number[key], prov[key])
    print("The group numbers are:")
    print(number)
    return number

