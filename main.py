import visualizations as vis
import createGraph as cg
import dijkstra as dij
import networkx as nx


path="C:\\Users\\matti\\Desktop\\reduced_dblp.json"

if __name__ == "__main__":
    print("REMEMBER TO CHANGE THE PATH IF THE FILE IS NOT IN THE SAME FOLDER OF THE CODE!")
    path="full_dblp.json"
    #Part 1
    G, conferences= cg.parseFile(path)
    print(nx.info(G))
    #Part 2 subgraph
    conferenceId=4627          #We took conference for plot something
    newGraph= vis.conferenceSubgraph(G, conferences, conferenceId)
    #Part 2 measures
    vis.degree(newGraph)       #degree centrality
    vis.closeness(newGraph)    #closeness centrality
    vis.betweenness(newGraph)  #betweenness centrality
    #Part 2 hop distance
    vis.ego_graph(G, 20405,3)
    #Part 3
    dij.shortestPathWeight(G, 365452)
    dij.groupNumber(G, [582465, 256176, 365452, 1, 49218, 2204, 4, 108326, 65019, 745219, 70837, 1703, 361, 259391, 716403, 1553, 572495, 309791, 408460, 605860])