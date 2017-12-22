# ADM_Homework4
## Main Structure:
Our project is structured in 4 fliles: __createGraph.py, visualizations.py, dijkstra.py, main.py__

## createGraph.py
__Imports:__ json, networkx, collections defaultdict
__Functions:__
* parseFile:
&nbsp;&nbsp;&nbsp;&nbsp;Takes as input a String that is the path where the file is located.
&nbsp;&nbsp;&nbsp;&nbsp;Returns a tuple (graph, conferences) where graph is a graph object from networkx library and conferences is a dictionary with this structure: __Key__=id_conference_int, __Value__=set of author_id
* computeGraph
