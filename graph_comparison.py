import backtracking as bt

from collections import defaultdict
import itertools
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import similarity_score as ss
import pandas as pd

divide = "\n###################################\n"

def maxCliques(cliques):
    """Find the set of largest cliques"""
    max_len = 0
    for clique in cliques:
        # Has a larger clique has been found?
        if len(clique) > max_len:
            # Update the maximum clique length
            max_len = len(clique)
            # Reset the maximum clique list
            max_cliques = [clique]
        # Is the current clique a maximum clique?
        elif len(clique) == max_len:
            # Add it to the list
            max_cliques.append(clique)
    return max_cliques

def check_adjacency(cliques, cEdges):
    """Check that all vertices are adjacent in the cliques found.
    This function cycles through the clique, initialising and calling
    the is_connected function which actually performs the adjacency check"""
    c_cliques = []
    for clique in cliques:
        # Set the initial vertex for adjacency search
        vi = list(clique)[0]
        v_seen = set()
        connected = is_connected(clique, v_seen, vi, cEdges)
        # Does the clique represent a connected graph?
        if connected == True:
            c_cliques.append(clique)
    return c_cliques

def is_connected(clique, v_seen, vi, cEdges):
    """"This algorithm attempts to visit every vertex in the graph once from
    an initial vertex. It checks whether previously visited vertices are connected
    to any of the remaining vertices."""
    # Add the vertex that initiated the search to the list of seen vertices
    v_seen.add(vi)
    # If all vertices in the clique can be visited, it must be connected
    if len(v_seen) == len(clique): return True
    # Check if the vertices in the clique are connected to any of the seen vertices
    for v2 in clique:
        for vi in v_seen:
            # Exclude any vertices that have already been 'visited'
            if v2 not in v_seen:
                # If the two vertices are connected, proceed
                if ((vi,v2) in cEdges) or ((v2,vi) in cEdges):
                    return is_connected(clique, v_seen, v2, cEdges)
    # If not all vertices can be visited, the graph is disconnected
    return False

def modularProduct(struct1, struct2):
    """Find the modular product of two graphs"""
    # Create local sets of edges and vetrices
    V1 = struct1.nodes
    V2 = struct2.nodes
    E1 = struct1.edges
    E2 = struct2.edges
    # Initialise empty sets for modular product edges and vetices
    modprodV = set()
    modprodE = set()
    # Find the cartesian product of the sets of vertices for each graph
    modprodV = set(itertools.product(V1, V2))
    # Loop through each vertex in the modular product
    for U, V in itertools.product(modprodV, modprodV):
        # Exclude any vertices which share the same point
        if V[0] != U[0] and V[1] != U[1]:
            # Exclude any pair of vertices that are already contained in an edge
            if (U,V) not in modprodE and (V,U) not in modprodE:
                # Any two vertices (u0, u1) and (v0, v1) are adjacent in the modular product if and only if
                # u0 is adjacent to v0 and u1 is adjacent to v1
                if ({U[0],V[0]} in E1) and ({U[1],V[1]} in E2):
                    modprodE.add((U,V))
                # or u0 is NOT adjacent to v0 and u1 is NOT adjacent to v1
                elif ({U[0],V[0]} not in E1) and ({U[1],V[1]} not in E2):
                    modprodE.add((U,V))
    # Return the vertices and edges of theresultant graph
    return modprodV, modprodE

def neighbourSet(V, E):
    """Create the neighbour set for each vertex (adjacency list) from
    the vertex and edge set of a graph"""
    # Create an empty dictionary which will contain the neighbour sets
    neighbours = {}
    # Initialise entries in the dictionary for each vertex
    for vertex in V:
        if vertex not in neighbours:
            neighbours[vertex] = []
    # Loop through each edge
    for edge in E:
        (node1, node2) = tuple(edge)
        # Add an entry in the vertex set for each adjacent vertex
        neighbours[node1].append(node2)
        neighbours[node2].append(node1)
    return neighbours

def BronKerbosch(R, P, X, N):
    """Return the maximal cliques of a graph (Bron-Kerbosch algorithm)"""
    # If there are no more vertices which can be added to R, report clique as maximal
    if P == set() and X == set():
        yield R
    else:
        # Create copy of P to iterate over
        Pit = P.copy()
        for u in P:
            # Yield the maximal cliques from previous recursions
            for r in BronKerbosch(R.union({u}), Pit.intersection(N[u]), X.intersection(N[u]), N):
                yield r
            # Exclude the current vertex from the list of vertices which can be added to R
            Pit.remove(u)
            X.add(u)
        
def BronKerboschPivot(R, P, X, N):
    """Return the maximal cliques of a graph (Bron-Kerbosch with pivoting)"""
    # If there are no more vertices which can be added to R, report clique as maximal
    if P == set():
        if X == set():
            yield R
    else:
        Pit = P.copy()
        # Choose vertex with greatest degree to be the pivot vertex
        ut = None
        for u in P:
            if ut == None or len(N[u]) > len(N[ut]) : ut = u
        for u in P:
            # Only use the current vertex if it is not adjacent to the piuot vertex
            if u not in N[ut] or u == ut:
                # Exclude the current vertex from the list of uertices which can be added to R
                Pit.remove(u)
                # Add the current vertex to R
                Rit = R.union({u})
                # Yield the maximal cliques from preuious recursions
                for r in BronKerboschPivot(Rit, Pit.intersection(N[u]), X.intersection(N[u]), N):
                    yield r
                X.add(u)

def maximalCliquesBK(V, E, ordering=False):
    """Initialises Bron-Kerbosch clique finding algorithms"""
    # Initialise other variables required for Bron-Kerbosch
    N = neighbourSet(V, E)
    # Set R and X to be the empty set
    R = set()
    X = set()
    # Set P to be the vertex set
    P = set(V)
    if ordering == True:
        # Order list of nodes according to degeneracy
        for v in degeneracy_ordering(N):
            cliques = []
            [cliques.append(r) for r in BronKerbosch(R.union({v}), P.intersection(N[v]), X.intersection(N[v]), N)]
            P.remove(v)
            X.add(v)
            return list(cliques)
    else:
        return list(BronKerbosch(R, P, X, N))

def findCedges(E, E1, E2):
    """Find the c-edges in a product graph. Takes the edge set from the
    modular product and checks whether adjacent nodes in the modular 
    product graph correspond to adjacent nodes in both parent graphs"""
    # Initialise the set of c-edges and d-edges
    cEdges = set()
    dEdges = set()
    # For each edge in the modular product, form the edge or vertex pairs to test
    for edge in E:
        # Create the edge or vertex pair in G1
        u1 = edge[0][0]
        u2 = edge[1][0]
        # Create the edge or vertex pair in G2
        v1 = edge[0][1]
        v2 = edge[1][1]
        # If u1 and u2 in G1 are adjacent
        if ({u1,u2} in E1) or ({u2,u1} in E1):
            # If v1 and v2 in G2 are adjacent
            if ({v1,v2} in E2) or ({v2,v1} in E2):
                cEdges.add(edge)
        else:
            dEdges.add(edge)  
    return cEdges, dEdges 

def maximalCliquesCedges(V, E, cEdges, dEdges, progress=False):
    """Initialises the c-clique version of the Bron-Kerbosch algorithm,
    performing the necessary iteration over nodes in the modular product 
    graph. This function also calls the progress bar."""
    cliques = list()
    # Create the neighbour set
    N = neighbourSet(V, E)
    T = set()
    # Print progress bar
    if progress == True:
        printProgressBar(0, len(V), "Progress:", "of vertices checked")
    # Initialise c-clique finding algorithm for each vertex
    for i, u in enumerate(sorted(list(V))):
        # Set P, D, X and R as the empty set
        P = set()
        D = set()
        X = set()
        # Initilise P with list of neighbouring vertices connected via c-edges
        # and D with list of neighbouring vertics connected via d-edges
        for v in N[u]:
            # Check if vertices connected via a c-edges
            if ((u,v) in cEdges) or ((v,u) in cEdges):
                # Has vertex previously been used as a starting vertex?
                if v in T: X.add(v)
                else: P.add(v)
            # Check if vertices connected via d-edge    
            elif ((u,v) in dEdges) or ((v,u) in dEdges): D.add(v)
        R = set({u})
        # Call c-clique finding algorithm
        [cliques.append(r) for r in enumerateCcliques(R, P, D, X, N, T, cEdges)]
        T.add(u)
        if progress == True:
            printProgressBar(i, len(V)-1, "Progress:", "of vertices checked")
    print()
    return cliques

def enumerateCcliques(R, P, D, X, N, T, cEdges):
    """Return the maximal c-cliques of a graph (modified Bron-Kerbosch algorithm)"""
    # If there are no more vertices which can be added to R, report clique as maximal
    if P == set() and X == set():
        yield R
    # Create copy of P to iterate over
    else:
        Pit = P.copy()
        for u in P:
            # Exclude the current vertex from the list of vertices which can be added to R
            Pit.remove(u)
            # Create copies 
            Dit = D.copy()
            Xit = X.copy()
            for v in D:
                # Modification suggested in paper
                if ((u,v) in cEdges) or ((v,u) in cEdges):
                    if v in T: X.add(v)
                    else: Pit.add(v)
                    # Remove the current vertex from the list of d-edges
                    Dit.remove(v)
            D = Dit
            # Add the current vertex to R
            Rit = R.union({u})
            # Yield the maximal cliques from previous recursions
            for r in enumerateCcliques(Rit, 
                                        Pit.intersection(N[u]), 
                                        Dit.intersection(N[u]),
                                        Xit.intersection(N[u]), 
                                        N, T, cEdges): yield r
            X.add(u)

def findSubgraphs(V, E, cEdges, dEdges):
    """Given the modular product, c-edges and d-edges for two graphs, 
    return the full list of: connected induced common subgraphs"""
    # c-clique algorithm 
    # print("Finding cliques...")
    cliques = list(maximalCliquesCedges(V, E, cEdges, dEdges))
    # print("Removing duplicates...")
    cliques = [set(item) for item in set(frozenset(item) for item in cliques)]
    # print("Checking cliques for adjacency...")
    c_cliques = check_adjacency(cliques, cEdges)
    # print(divide)
    return c_cliques

def plotMCSfromNodes(MCS_nodes, graph1, graph2):
    MCS_edges = []
    for node1 in MCS_nodes:
        for node2 in MCS_nodes:
            if node1 != node2:
                v1 = node1[0]
                v2 = node2[0]
                u1 = node1[1]
                u2 = node2[1]
                if v2 in graph1[v1] and u2 in graph2[u1]:
                    MCS_edges.append((node1, node2))
    graphPlot(MCS_nodes, MCS_edges)

def plotMCSfromCEdges(clique_set, cEdges):
    """Take the first maximal clique and create an edge set from
    the modular product graph"""
    # Take the first clique in the set of maximal cliques 
    # and generate a list of nodes for the MCS
    sg_nodes = clique_set[0]
    sg_edges = []
    # Create an edge set using the modular product graph
    for v1 in sg_nodes:
        for v2 in sg_nodes:
            # If an edge exists between two sets of nodes in a clique,
            # add it to the MCS edge set
            if (v1,v2) in cEdges:
                sg_edges.append((v1,v2))
    graphPlot(sg_nodes, sg_edges)

def findGroundNodes(node_list):
    """Check whether nodes represent regular IEs or boundary conditions"""
    ground_nodes = []
    for node in node_list:
        # If the node is a digit rather than a letter, then it designates
        # a boundary condition node
        if node[0].isdigit():
            # Create list of boundary condition nodes
            ground_nodes.append(node)
    # Any nodes that are not b.c. nodes are considered normal nodes
    normal_nodes = [x for x in node_list if x not in ground_nodes]
    return ground_nodes, normal_nodes

def graphPlot(nodes, edges, labels=False):
    """Plot the graph given by a set of nodes and edges, including any
    name labels for elements. Colour the boundary condition nodes blue
    and regular elements red"""
    # Create new networkX graph object
    G = nx.Graph()
    # Add nodes and edges to the graph object
    G.add_edges_from(edges)
    G.add_nodes_from(nodes)
    # Use element names if provided
    if labels != False:
        pos = nx.spring_layout(G, k=1)
        nx.draw_networkx_labels(G, pos, labels, font_size=16)
    # Otherwise label nodes with their element ID
    else:
        pos = nx.spring_layout(G)
        nx.draw_networkx_labels(G, pos)
    # Find the boundary condition nodes in the AG
    grnd, nrml = findGroundNodes(nodes)
    # Colour BC nodes blue and regular nodes red
    nx.draw_networkx_nodes(G, pos, grnd, node_color='b')
    nx.draw_networkx_nodes(G, pos, nrml, node_color='r')
    # Draw and show the graph with no axis
    nx.draw_networkx_edges(G, pos)
    plt.axis('off')
    plt.show()

def importIE(structure, file_path, plot=False):
    """Read an excel file containing an IE model and add the AG 
    to a structure object"""
    # Import necessary information for the IE from the excel file
    elements = pd.read_excel (file_path, sheet_name='Elements', usecols="A:I")
    joints = pd.read_excel (file_path, sheet_name='Joints', usecols="A:H")
    boundary_conditions = pd.read_excel (file_path, sheet_name='Boundary conditions', usecols="A:C")
    # Create full element list for the IE by combining b.c. and regular elements
    boundary_list = [str(bc) for bc in boundary_conditions['Element ID']]
    element_list = list(elements['Element ID']) + boundary_list
    element_keys = element_list + boundary_list
    # Initialise empty dictionary for storing element attributes
    structure.elements = {element: [] for element in element_keys}
    # Create the joint list for the IE
    joint_keys = [tuple(joint.split(', ')) for joint in joints['Joint set']]
    # Initialise placeholders for joint attributes
    joint_values = [[str(i),[],''] for i in range(1, len(joint_keys)+1)]
    structure.joints = dict(zip(joint_keys, joint_values))
    # Update the AG, adding elements and joints from the IE
    structure.addElements()
    structure.addJoints()
    # Add edges to the AG
    structure.edgeList()
    # Plot the graph for the imported structure
    # If the option "elements" is specified, the node labels will be the element name
    if plot == "elements":
        labels_values = list(elements['Name']) + list(boundary_conditions['Name'])
        labels = dict(zip(element_list, labels_values))
        graphPlot(structure.nodeList(), structure.edgeList(), labels)
    # Otherwise the graph is plotted using the element IDs
    elif plot == "nodes":
        graphPlot(structure.nodeList(), structure.edgeList())

def smallestGraphFirst(graph1, graph2):
    # Generate node list
    V1 = graph1.nodeList()
    V2 = graph2.nodeList()
    # The modular product function misses edges if the larger graph is called first
    if len(V1) > len(V2):
        # Swap graphs so largest is graph1
        temp_graph = graph1
        graph1 = graph2
        graph2 = temp_graph
    return graph1, graph2

def largestGraphFirst(graph1, graph2):
    # Generate node list
    V1 = graph1.nodeList()
    V2 = graph2.nodeList()
    # The modular product function misses edges if the larger graph is called first
    if len(V1) < len(V2):
        # Swap graphs so largest is graph1
        temp_graph = graph1
        graph1 = graph2
        graph2 = temp_graph
    return graph1, graph2

def findJaccardDistanceBK(g1, g2, BCmatch=False, plot=False):
    """Handles the process of calculating the Jaccard distance for two graphs
    from the MCS found using the c-clique BK algorithm"""
    graph1, graph2 = smallestGraphFirst(g1, g2)
    # Re-generate node list
    V1 = graph1.nodeList()
    V2 = graph2.nodeList()
    # Generate edge list
    E1 = graph1.edgeList()
    E2 = graph2.edgeList()
    # Plot the two graphs
    if plot == True:
        graphPlot(V1, E1)
        graphPlot(V2, E2)
    # Generate the modular product graph
    V, E = modularProduct(graph1, graph2)
    # print("Modular product vertices:", len(V))
    # print("Modular product edges:", len(E))
    # Create list of c-edges and d-edges within modular product graph
    cEdges, dEdges = findCedges(E, E1, E2)
    # Find the largest cliques
    c_cliques = findSubgraphs(V, E, cEdges, dEdges)
    if BCmatch:
        # Match on boundary conditions alone
        boundary_match = ss.boundaryConditionMatch(c_cliques, graph1, graph2)
        boundary_match.sort(key=len, reverse=True)
        vertex_match = 1 - ss.JaccardIndex(boundary_match[0], V1, V2)
        # Plot largest subgraph with boundary matches
        if plot == True:
            plotMCSfromCEdges(boundary_match, cEdges)
    else:
        # print("Finding largest cliques...")
        # Find the largest MCSs
        max_cliques = maxCliques(c_cliques)
        # Calculate the Jaccard distance using one of the possible MCSs
        vertex_match = 1 - ss.JaccardIndex(max_cliques[0], V1, V2)
        # Plot largest subgraph 
        if plot == True:
            plotMCSfromCEdges(max_cliques, cEdges)
    return vertex_match

def findJaccardDistanceBackTrack(g1, g2, plot=False):
    graph1, graph2 = smallestGraphFirst(g1, g2)
    # Re-generate node list
    V1 = graph1.nodeList()
    V2 = graph2.nodeList()
    # Generate edge list
    E1 = graph1.edgeList()
    E2 = graph2.edgeList()
    # Plot the two graphs
    if plot == True:
        graphPlot(V1, E1)
        graphPlot(V2, E2)
    matches = bt.backtrack(graph1.graph, graph2.graph)
    max_cliques = maxCliques(matches)
    vertex_match = 1 - ss.JaccardIndex(max_cliques[0], V1, V2)
    return vertex_match

def createDistanceMatrix(graph_list, metric, BCmatch=False):
    """Handles the process of creating a distance matrix using whichever
    alogrithm is specified"""
    begin_time = time.time()
    # Create distance matrix with initital distance set to zero
    n = len(graph_list)
    distanceMatrix = np.zeros((n,n))
    # Iterate through pairs of graphs in list
    for i, graph1 in enumerate(graph_list):
        for j, graph2 in enumerate(graph_list):
            # If graphs are not identical, calculate pairwise distances
            if i < j:
                if metric == "JaccardBK":
                    distanceMatrix[i][j] = findJaccardDistanceBK(graph1, graph2, BCmatch)
                if metric == "JaccardBackTrack":
                    distanceMatrix[i][j] = findJaccardDistanceBackTrack(graph1, graph2)
                elif metric == "Spectral":
                    pass
            if i > j:
                # Use symmetry condition for distance matrix
                distanceMatrix[i][j] = distanceMatrix[j][i]
    end_time = time.time()
    print("Time taken:", round(end_time - begin_time, 2), "seconds")
    return distanceMatrix

# Modified from progress bar code
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1):
    """
    Print iterations progress

    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    print('\r%s %s%% %s' % (prefix, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

# Not my code!!!
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Print iterations progress

    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

# Not my code!!!
def degeneracy_ordering(graph):
    """Order vertices by degree"""
    ordering = []
    ordering_set = set()
    degrees = defaultdict(lambda : 0)
    degen = defaultdict(list)
    max_deg = -1
    for v in graph:
        deg = len(graph[v])
        degen[deg].append(v)
        degrees[v] = deg
        if deg > max_deg:
            max_deg = deg
    while True:
        i = 0
        while i <= max_deg:
            if len(degen[i]) != 0:
                break
            i += 1
        else:
            break
        v = degen[i].pop()
        ordering.append(v)
        ordering_set.add(v)
        for w in graph[v]:
            if w not in ordering_set:
                deg = degrees[w]
                degen[deg].remove(w)
                if deg > 0:
                    degrees[w] -= 1
                    degen[deg - 1].append(w)
    ordering.reverse()
    return ordering