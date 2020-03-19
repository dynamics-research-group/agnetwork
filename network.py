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
        weights[str(graph)] = np.random.rand(len(graph_list))
        # Lower triangle is the same as the upper triangle
        weights[str(graph)][i:] = 0
    return weights

def updateWeights(weights, graph_list, iterations=10):
    for x in range(iterations):
        # Create all possible pairwise combinations for the graphs ignoring order
        list_of_comparisons = itertools.combinations(graph_list, 2)
        for comparison in list_of_comparisons:
            # Calculate the difference in number of nodes for a given pair of graphs
            diff = comparison[0].numberOfNodes() - comparison[1].numberOfNodes()
            # Square the difference to ensure symmetry
            adjust = diff * diff 
            # Get the row number for the first graph
            row_num = list(weights.keys()).index(str(comparison[0]))
            # row_num = network_weights.index.get_loc(str(comparison[0]))
            graph = str(comparison[1])
            # Update the corresponding entry in the weights dictionary
            weights[graph][row_num] += weights[graph][row_num] + adjust
        # Find the maximum weight after all entries have been updated
        max_weight = max(i for v in weights.values() for i in v) 
        # for v in myDict.values():
        #     for i in v:
        #         m = i if i > m else m
        # Normalise each weight w.r.t. the maximum
        for x, y in weights.items():
            weights[x] = y/max_weight
    return weights