from collections import defaultdict

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
    """Check that all vertices are adjacent in the cliques found"""
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
    # The modular product function misses edges if the larger graph is called first
    if len(V1) > len(V2):
        raise Exception("Smaller graph first please.")
    # Initialise empty sets for modular product edges and vetices
    modprodV = set()
    modprodE = set()
    # Find the cartesian product of the sets of vertices for each graph
    [modprodV.add((u, v)) for u in V1 for v in V2]
    # Loop through each vertex in the modular product
    for U in modprodV:
        # Compare with every other vertex in the modular product
        for V in modprodV:
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
    """Create the neighbour set for each vertex"""
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
            # Add the current vertex to R
            #Rit = R.union({u})
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

def maximalCliquesBK(V, E):
    """Initialises Bron-Kerbosch clique finding algorithms"""
    # Initialise other variables required for Bron-Kerbosch
    N = neighbourSet(V, E)
    # Set R and X to be the empty set
    R = set()
    X = set()
    # Set P to be the vertex set
    P = set(V)
    # for v in degeneracy_ordering(N):
    #     [cliques.append(r) for r in BronKerbosch(R.union({v}), P.intersection(N[v]), X.intersection(N[v]), N)]
    #     P.remove(v)
    #     X.add(v)
    # return list(cliques)
    return list(BronKerbosch(R, P, X, N))

def findCedges(E, E1, E2):
    """Find the c-edges in a product graph"""
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

def maximalCliquesCedges(V, E, cEdges, dEdges):
    cliques = list()
    # Create the neighbour set
    N = neighbourSet(V, E)
    T = set()
    # Initialise c-clique finding algorithm for each vertex
    for i, u in enumerate(sorted(list(V))):
    # for u in degeneracy_ordering(N):
    # for u in V:
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
        printProgressBar(i, len(V), "Progress:", "Complete")
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

def mcsSimilarityScore(mcs, g1, g2):
    return (len(mcs) * 100) / (len(g1) + len(g2) - len(mcs))

def inexactGraphComparison(graph1, graph2):
    # Create possible pairs
    pass

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