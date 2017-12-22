import json
import networkx as nx
from collections import defaultdict


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


def computeGraph(workedWith, workedOn):
    G= nx.Graph()
    for author1 in workedWith:
        G.add_node(author1)
        for author2 in workedWith[author1]:
            jDistance= 1-len(workedOn[author1].intersection(workedOn[author2]))/len(workedOn[author1].union(workedOn[author2]))
            G.add_edge(author1,author2,weight=jDistance)
    return G
