"""Data reading and printing utils."""

import pandas as pd
import networkx as nx
from texttable import Texttable


def tab_printer(args):
    """
    Function to print the logs in a nice tabular format.
    :param args: Parameters used for the model.
    """
    args = vars(args)
    keys = sorted(args.keys())
    t = Texttable()
    t.add_rows([["Parameter", "Value"]])
    t.add_rows([[k.replace("_", " ").capitalize(), args[k]] for k in keys])
    print(t.draw())


def graph_reader(path):
    """
    Function to read the graph from the path.
    :param path: Path to the edge list.
    :return graph: NetworkX object returned.
    """
    with open(path) as f:
        nodeDict = dict()
        counter = 0
        graph = nx.Graph()
        for line in f:
            nodes = line.replace('\n', '').split(',')
            fnode, snode = int(nodes[0]), int(nodes[1])
            if bool:
                if fnode not in nodeDict:
                    nodeDict[fnode] = counter
                    counter = counter + 1
                if snode not in nodeDict:
                    nodeDict[snode] = counter
                    counter = counter + 1
                graph.add_edge(nodeDict[fnode], nodeDict[snode])
            else:
                graph.add_edge(fnode, snode)
    return graph


# Save output graph
def saveNewGraph(graph, name):
    edges = list(graph.edges)
    file = open('../output/' + name + '.edgelist', 'w')
    for edge in edges:
        fnode = edge[0]
        snode = edge[1]
        edgeToPrint = str(fnode) + ',' + str(snode) + '\n'
        file.write(edgeToPrint)
