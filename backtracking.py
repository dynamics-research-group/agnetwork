# Backtracking algorithm
def bound(G1_dash, G2_dash, G1, G2, m, best):
    len_m = len(m)
    if len(G1_dash) + len_m <= best:
        return True
    # elif len(G2_dash) + len_m <= best:
    #     return True
    # else:
    #     candidates = set()
    #     for v1 in G1_dash:
    #         for v2 in G2_dash:
    #                 if compatibleHeuristic(G1[v1], G2[v2], m):
    #                     candidates.add(v2)
    #     if len(candidates) + len_m > best:
    #         return False
    #     else:
    #         return True

def backtrack(G1, G2, filename='best.txt'):
    m_initial = []
    G2_dash = list(sort(G2))
    G1_dash = G1.copy()
    best = 0
    # return list(backtrack_algorithm(G1_dash, G2_dash, G1, G2, m_initial, best))
    with open('subgraphs/' + filename,'w') as f:
        f.write('MCS for graphs \n{0}\n{1}\n \n'.format(list(G1.keys()), list(G2.keys())))
    return [m[0] for m in list(backtrackAlgorithmIter(G1_dash, G2_dash, G1, G2, m_initial, best, filename))]

def backtrackAlgorithmIter(G1_dash, G2_dash, G1, G2, m, best, filename):
    # Create a list of nodes from G1 and G2 that have already been used to form the solution
    v1_list_int = [pair[0] for pair in m]
    v2_list_int = [pair[1] for pair in m]
    ordered_nodes = sort(G1_dash)
    while True:
            if bound(G1_dash, G2_dash, G1, G2, m, best):
                # This new solution cannot have exceed the current best estimate
                break
            try:
                v1 = next(ordered_nodes)
            except:
                # This new solution must exceed the current best estimate, update the best estimate
                best = len(m)
                print(best)
                with open('subgraphs/' + filename,'a') as f:
                    f.write('Length {0} \n{1}\n \n'.format(best, m))
                yield m, best
                break
            # Add the current v1 to the list of nodes that have been tried
            v1_list = v1_list_int + [v1] 
            for v2 in G2_dash:
                    # Check whether the new pair of nodes (v1, v2) can be added to the solution
                    if compatibleHeuristic(set(G1[v1]), set(G2[v2]), m):
                        # Add the current v2 to the list of nodes that have been tried
                        v2_list = v2_list_int + [v2]
                        # Carry on down the tree
                        for M in backtrackAlgorithmIter({v1 : G1_dash[v1] for v1 in G1_dash if v1 not in v1_list}, 
                                                    [v2 for v2 in G2_dash if v2 not in v2_list],
                                                        G1, G2,
                                                        list(m) + [(v1, v2)],
                                                        best, filename): 
                                # Find the length of the current best estimate
                                if len(M[0]) > best: 
                                    best = M[1]
                                yield M
            # Remove the node v1 that has already been tried from the remaining graph G1_dash
            del G1_dash[v1]

   
def backtrackAlgorithmFor(G1_dash, G2_dash, G1, G2, m, best, filename):
    # Create a list of nodes from G1 and G2 that have already been used to form the solution
    v1_list_int = [pair[0] for pair in m]
    v2_list_int = [pair[1] for pair in m]
    ordered_nodes = sort(G1_dash)
    for v1 in ordered_nodes:
        if bound(G1_dash, G2_dash, G1, G2, m, best):
                # This new solution cannot have exceed the current best estimate
                break
        # Add the current v1 to the list of nodes that have been tried
        v1_list = v1_list_int + [v1] 
        for v2 in G2_dash:
                # Check whether the new pair of nodes (v1, v2) can be added to the solution
                if compatibleHeuristic(set(G1[v1]), set(G2[v2]), m):
                    # Add the current v2 to the list of nodes that have been tried
                    v2_list = v2_list_int + [v2]
                    # Carry on down the tree
                    for M in backtrackAlgorithmFor({v : G1_dash[v] for v in G1_dash if v not in v1_list}, 
                                            [u for u in G2_dash if u not in v2_list],
                                                    G1, G2,
                                                    list(m) + [(v1, v2)],
                                                    best, filename): 
                            # Find the length of the current best estimate
                            if len(M[0]) > best: 
                                best = M[1]
                            yield M
        # Remove the node v1 that has already been tried from the remaining graph G1_dash
        del G1_dash[v1]
    if len(m) > best:
        best = len(m)
        print(best)
    with open('subgraphs/' + filename,'a') as f:
        f.write('Length {0} \n{1}\n \n'.format(best, m))
    yield m, best


def sort(graph):
    sorted_graph = sorted(graph.items(), key = lambda item : len(item[1]), reverse=True)
    sorted_nodes = (node[0] for node in sorted_graph)
    return sorted_nodes

def compatibleConnected(Nv1, Nv2, m):
    # If no associations exist, any node is compatible
    if m == []:
        return True
    else:
        for pair in m:
                if pair[0] in Nv1 and pair[1] in Nv2:
                    return True
        return False
    
def compatibleGeneral(Nv1, Nv2, m):
    # If no associations exist, any node is compatible
    # Ensures graph is induced, but not necessarily connected
    if m == []:
        return True
    else:
        for pair in m:
                if pair[0] in Nv1 and pair[1] in Nv2:
                    return True
                if pair[0] not in Nv1 and pair[1] not in Nv2:
                    return True
        return False

def compatibleHeuristic(Nv1, Nv2, m):
    # My best guess as to the heuristic in the paper by Cao
    # Enforces induced subgraphs
    S1 = set()
    S2 = set()
    for pair in m:
        if pair[0] in Nv1:
            S1.add(pair)
        if pair[1] in Nv2:
            S2.add(pair)
    if len(S1) == len(S2):
        if S1 == S2:
            return True
    return False
