import numpy as np
import itertools

def createGraphDict(graph_list):
    graph_dict = dict()
    for graph in graph_list:
        graph_dict[str(graph)] = graph
    return graph_dict

def initWeightsDict(graph_list):
    weights = dict()
    for i, graph in enumerate(graph_list):
        # Initialise random weights
        weights[graph] = np.random.rand(len(graph_list))
        # Lower triangle is the same as the upper triangle
        weights[graph][i:] = 0
    return weights

def updateWeights(weights, iterations=10):
    for x in range(iterations):
        # Iterate through all possible pairwise combinations for the graphs ignoring order
        for comparison in itertools.combinations(weights.keys(), 2):
            # Calculate the difference in number of nodes for a given pair of graphs
            diff = comparison[0].numberOfNodes() - comparison[1].numberOfNodes()
            # Square the difference to ensure symmetry
            adjust = diff * diff 
            # Get the row number for the first graph
            row_num = list(weights.keys()).index(comparison[0])
            # Update the corresponding entry in the weights dictionary
            weights[comparison[1]][row_num] += adjust
        # Find the maximum weight after all entries have been updated
        max_weight = max(i for v in weights.values() for i in v) 
        # for v in myDict.values():
        #     for i in v:
        #         m = i if i > m else m
        # Normalise each weight w.r.t. to the max
        for x, y in weights.items():
            weights[x] = y/max_weight
    return weights

def addNewGraph(graph, weights):
    # graph_list = weights.keys()
    weights[graph] = np.random.rand(len(weights.keys()))
    for entry in weights:
        weights[entry] = np.append(weights[entry], [0])
    return weights