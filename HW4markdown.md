
# Homework 4
### Group 12: Mattia Di Fulvio, Esin Ildiz, Giannis Lakafosis

# createGraph.py: Parsing Data and Creating the Graph


```python
import json
import networkx as nx
from collections import defaultdict
```

So far, we simply imported the json and networkx libraries and defaultdict.


```python
def parseFile(path):
    json_data=open(path).read()
    dataset = json.loads(json_data)
    #Declare structures that We will use
    conferences= defaultdict(set)
    workedWith = defaultdict(set)
    workedOn   = defaultdict(set)
    #Analyze the file    
    for entry in dataset:
        people={author["author_id"] for author in entry["authors"]}
        #Compute the list of people who published in a conference for every conference
        if entry["id_conference_int"] not in conferences:
            conferences[entry["id_conference_int"]] = people
        else:
            conferences[entry["id_conference_int"]].update(people)
        for author in entry["authors"]: 
            #Compute the list of people who worked with every author
            if author["author_id"] not in workedWith.keys():
                workedWith[author["author_id"]] = people-{author["author_id"]}
            else:
                workedWith[author["author_id"]].update(people-{author["author_id"]})
            #Compute the list of publication for every author
            if author["author_id"] not in workedOn:
                workedOn[author["author_id"]]= {entry["id_publication_int"]}
            else:
                workedOn[author["author_id"]].add(entry["id_publication_int"])
    return computeGraph(workedWith, workedOn), conferences
```

In the previous module We parsed the file and stored the information We need in three defaultdicts:

__conferences__ contains an entry for every conference and the corresponding value is the set of authors who published at least once in that conference.<br> Structure: __Key__=id_conference_int, __Value__=set of author_id

__workedWith__ contains an entry for every author and the corresponding value is the set of authors who published at least once with him.<br> Structure: __Key__=author_id, __Value__=set of author_id

__workedOn__ contains an entry for every author and the corresponding value is the set of publications the author wrote.<br> Structure: __Key__=author_id, __Value__=set of id_publication_int

We read the whole dataset only once(the main for loop) and for every entry(publication) We compute the list of people who worked on it. Then, We add them in the corresponding entry of __conferences__ and later for each of them We update __workedWith__ and __workedOn__.<br> It's not easy to estimate a precise complexity but We think It sould be around __O(n*m)__ where __n__= number of publication __m__= average number of people who worked on a publication.

After this We return a tuple made up by a graph and conferences' defaultdict.


```python
def computeGraph(workedWith, workedOn):
    G= nx.Graph()
    for author1 in workedWith:
        G.add_node(author1)
        for author2 in workedWith[author1]:
            jDistance= 1-len(workedOn[author1].intersection(workedOn[author2]))/len(workedOn[author1].union(workedOn[author2]))
            G.add_edge(author1,author2,weight=jDistance)
    return G
```

For each author:
We add his node cause __some of them worked alone__ and We can't use the built in function of add_edge because They will not have any edge and They wouldn't be in the graph.
Then we add an edge for every author who worked with the one We are actually exploring(We use __workedWith__), the weight of this edge is equal to the __jaccard distance__ that we compute using the __workedOn__ data structures of both authors.<br>
__jaccard distance(a1, a2)=** 1 − J(p1, p2)**__ where a1,a2 are authors and p1,p2 are the publications they wrote (workedOn[author])

# visualizations.py: Statistics and Visualizations

For this part We found useful functions in networkx library


```python
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
```


```python
def conferenceSubgraph(graph, conferences, conferenceId):
    ret= graph.subgraph(conferences[conferenceId])
    print("\nThis is the subgraph induced by the set of autor who published in the input conference, We took %d as conference" %(conferenceId))
    plt.clf()
    nx.draw_networkx(ret, node_size=15, with_labels= False)
    plt.show()
    return ret
```

The above function takes as input: a graph, the conferences dictionay and the id of a conference.<br>
The functions plot the subgraph induced by the set of author who published at leat once in the input conference and returns it.


```python
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
```

__Degree centrality__: Here We simply compute the degree centrality of the graph we have in input.<br>
We show an histogram, a loglog plot and a We also show the input graph with the node's size related to their Degree centrality. 


```python
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
```

__Closeness centrality__: Here We simply compute the closeness centrality of the graph we have in input.<br>
We show a loglog plot and a We also show the input graph with the node's size related to their Closeness centrality.


```python
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
```

__Betweenness centrality__: Here We simply compute the Betweenness centrality of the graph we have in input.<br>
We show a loglog plot and a We also show the input graph with the node's size related to their Betweenness centrality.


```python
def ego_graph(graph, author, hops):
    print("The graph above is the ego graph of author with hop distance at most %d from author %d" %(hops, author))
    ego= nx.ego_graph(graph, author, radius=hops, center=True, undirected=False, distance=None)
    plt.clf()
    nx.draw_networkx(ego, node_size=3, with_labels= False)
    plt.show()
    return ego
```

In the function above We use __nx.ego_graph__ from networkx, then we plot and return the graph.

# dijkstra.py: Shortest Path


```python
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
```

The cell above contains the function We use to compute the weight of the __shortest path__.<br>
The function takes the __graph__, the __start__ and the __end__ nodes as inputs.

If the start or the end node are not in the graph We print a message and We return an empty dict.<br>
Else We initialize two dictionaries which are explored and unexplored.
At the begining, __explored dict__ has only "start node" as a key and its value is 0 and __unexplored dict__ is initiliazed with all the nodes(except the start nodes) as keys and their values set to np.Inf<br>
Then We repeat the following steps until We reach the end node:<br>
__1)__ Select a __current__ node(the first time is the start node)<br>
__2)__ For __every edge__ of the current node<br>
__2.1)__ We check if the node We can reach has a path more expensive than the one we have currently.<br>
__2.1a)__ If the path we have currently is __more expensive__ We continue to check it for the next other edge(point __2__), in this way __We don't overload too much the Heap__<br>
__2.1b)__ __Otherwise__ We update the cost of the path and We push an entry in the heap we use to keep trace of the cost<br>
__3)__ We pop one element from the heap __until We find an unexplored node__, it is the __new current__ and if it is different from "end" and his cost is not np.Inf, We update __explored__ and __unexplored__ and We repeat all the step from 1, otherwhise We return explored.<br>

We use a heap cause it is the fastest way to get the unexplored element with the minimum value, It may happen that one element appears more than one time in the heap cause it could be there but then We find a less expensive path for it and We push it again, that's the reason why We check if the element We pop is in explored. The cost for taking the minimum element in the heap is O(log(n)) and We check if it is explored or not in O(1) cause dictionaries are based on hashmap.

The function complexity is __O(Dijkstra) => O(|V^2|)__ where V is the number of vertex in the graph



```python
def shortestPathWeight(graph, author):
    print("Trying to reach Aris from author: %d" %(author))
    distances = dijkstra(graph, author, 256176)
    if 256176 not in distances:
        print("You can't reach Aris starting from this author.")
        return
    print("The weight of the shortest path between Aris and the other author is:"+ str((distances[256176])))
    return distances[256176]
```

In the previous blocks We simply use the funcion We already talked about.


```python
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
```

There are different option to compute the group number:<br>
__1)__Compute the shortest path for every graph's node and use as group number the smallest value from the node to one of those in the input list __n((O(Dijkstra)) => O(n*|V^2|)__<br>
__2)__Compute the shortest path for every node in the input list(let's say they are k) and take the minimum valeue for every node __O(k*|V^2|)__<br>
__3)__Use the Dijkstra algorithm in a multisource way __O(|V^2|)__

The code above is a __multisource version__ of the previous algorithm We simply initialize the explored dictionary with all the nodes in input and for all of them We check the edges We can reach and We update their cost, then We select the starter and We continue like in the previous version.


```python
def groupNumber(graph, sublist):
    number = {key: np.Inf for key in graph.nodes()}
    prov= multisourceDijkstra(graph, sublist)
    for key in prov:
        number[key]=min(number[key], prov[key])
    print("The group numbers are:")
    print(number)
    return number
```

In the previous algorithm We stop if We meet a node with cost np.Inf so We add those node in the groupNumber function, then We print and return the final dictionary who has the following structure: __key__=author_id, __value__=group number
