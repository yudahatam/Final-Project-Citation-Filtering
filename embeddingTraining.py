"""Running the Splitter."""
import json
import random

import matplotlib.image as mpimg
import networkx
import networkx as nx
import numpy
import numpy as np
import torch
import matplotlib.pyplot as plt
import pandas as pd
from networkx import to_numpy_array, from_numpy_array
from param_parser import parameter_parser
from splitter import SplitterTrainer
from utils import tab_printer, graph_reader, saveNewGraph


def embeddingTraining(args):
    """
    Parsing command line parameters.
    Reading data, embedding base graph, creating persona graph and learning a splitter.
    Saving the persona mapping and the embedding.
    """
    torch.manual_seed(args.seed)
    tab_printer(args)
    graph = graph_reader(args.edge_path)

    if len(graph.edges) < 10000:
        print("Saving image of original graph\n")
        nx.draw(graph, with_labels=True, node_size=300, font_color='yellow')
        plt.savefig('../images/graphOrg.jpg')
        plt.close()
        print("Finished image of original graph\n")
    else:
        im=mpimg.imread('../images/TooMuch.jpg')
        plt.imshow(im)
        plt.savefig('../images/graphOrg.jpg')
        plt.close()
    edgeList = list(graph.edges)  # Take list of edges
    edgeListPoints = np.zeros(len(edgeList))  # Create list for point of edges
    '''First training'''
    trainer = SplitterTrainer(graph, args)
    trainer.fit()
    originalEmbedding = trainer.save_embedding().to_numpy()
    '''--------------------------------------------'''
    '''Next trainings'''
    for iteration in range(args.training):
        print('''
            ##########################################
            ###### TRAINING NUMBER {}#################
            ##########################################
        '''.format(iteration + 1))

        '''
            ##########################################
            ###### Randomly remove edges##############
            ##########################################
        '''
        graphForEdit = graph.copy()  # Create copy of graph
        randomList = random.sample(range(0, len(graphForEdit.edges)),
                                   int(len(graphForEdit.edges) / 10))  # Randomly choose 10% of edges
        randomList.sort()  # Sort the chosen edges
        edgesToRemove = []  # list to hold the edges that need to be removed
        nodesToCheckEmbedding = []  # list to hold the id of the node that are needed to check embedding

        for edgeIndex in randomList:  # go over the randomly selected edges and add them to the list
            edgesToRemove.append(edgeList[edgeIndex])
        graphForEdit.remove_edges_from(edgesToRemove)  # remove the edges from the graph

        for edge in edgesToRemove:  # Go over the list and remember the nodes that need to be examined
            nodesToCheckEmbedding.extend(edge)
        nodesToCheckEmbedding = list(dict.fromkeys(nodesToCheckEmbedding))  # remove duplicates from list
        nodesToCheckEmbedding.sort()  # sort list
        '''
            ##########################################
            ########### Further training##############
            ##########################################
        '''
        args.embedding_output_path = '../output/newEmbedding.csv'
        '''When needing to train uncomment this section'''
        secondTrainer = SplitterTrainer(graphForEdit, args)
        secondTrainer.fit()
        newEmbedding = secondTrainer.save_embedding().to_numpy()
        '''---------------------------------------------'''

        '''
            ##########################################
            ########### Points distribution###########
            ##########################################
            This section decides which edge get point
        '''
        origDistOfEmbedding = []  # List to hold the distances between the embedding of the nodes before removal
        newDistOfEmbedding = []  # List to hold the distances between the embedding of the nodes after removal
        for edge in edgesToRemove:
            firstNodeEmbedding = edge[0]  # Get id of first node
            secondNodeEmbedding = edge[1]  # Get id of second node
            firstOrig = originalEmbedding[firstNodeEmbedding]  # Get original embedding of first node
            secondOrig = originalEmbedding[secondNodeEmbedding]  # Get original embedding of second node
            firstNew = newEmbedding[firstNodeEmbedding]  # Get new embedding of first node
            secondNew = newEmbedding[secondNodeEmbedding]  # Get new embedding of second node
            origDistOfEmbedding.append(round(numpy.linalg.norm(firstOrig - secondOrig),
                                             3))  # Add the euclidean distance to the original distance list
            newDistOfEmbedding.append(
                round(numpy.linalg.norm(firstNew - secondNew),
                      3))  # Add the euclidean distance to the new distance list
        barOfAvg = numpy.average(
            origDistOfEmbedding)  # Get the avg of the original distances of the embedding of the nodes from the edges that were removed to be the bar for grading edges

        for i in range(
                len(newDistOfEmbedding)):  # Loop to go over the edges that pass the bar and find their location in the list of all the edges and add a point to it
            if newDistOfEmbedding[i] > barOfAvg:
                edge = edgesToRemove[i]
                edgeListPoints[edgeList.index(edge)] = edgeListPoints[edgeList.index(edge)] + 1
    print(
        "##########################################\n########### Finished Training###########\n##########################################")
    percentage = args.percent
    amountOfedges = int((1 - (percentage / 100)) * len(edgeListPoints))
    removeEdges = []
    for i in range(amountOfedges):
        minValue = min(edgeListPoints)
        indexMinValue = list(edgeListPoints).index(minValue)
        edgeListPoints[indexMinValue] = 9999
        edgeToRemove = edgeList[indexMinValue]
        removeEdges.append(edgeToRemove)
    print(
        "##########################################\n########### Finished grading###########\n##########################################")
    tempGraph = graph.copy()
    tempGraph.remove_edges_from(removeEdges)
    tempEdges = list(tempGraph.edges)
    coreGraph = nx.Graph()
    coreGraph.add_edges_from(tempEdges)
    path = args.edge_path
    path = path.split('/')
    name = path[len(path) - 1]
    name = name.split('.')[0]
    name = name + '_Core'
    print(
        "##########################################\n########### Saving Core Of Graph###########\n##########################################")
    saveNewGraph(coreGraph, name)
    print(
        "##########################################\n########### Finished Saving###########\n##########################################")
    if len(coreGraph.edges) < 10000:
        nx.draw(coreGraph, with_labels=True, node_size=300, font_color='yellow')
        plt.savefig('../images/newGraph.jpg')

