import itertools

def JaccardIndex(mcs, g1, g2):
    return (len(mcs) * 100) / (len(g1) + len(g2) - len(mcs))

def takeSecond(elem):
    return elem[1]

def takeAverageMatch(elem):
    return (elem[1] + elem[2])/2

def elementAttributeMatching(sg_nodes, elements1, elements2):
    """Check whether the nodes in G1 and G2, which are associated
    with nodes in the subgraph, have matching attributes"""
    match = 0
    for node in sg_nodes:
        # Extract the element IDs from the subgraph nodes
        id1 = node[0]
        id2 = node[1]
        # Check if the elements are ground nodes
        if (elements1[id1][0] != 'Ground') and (elements2[id2][0] != 'Ground'):
            # If either of the elements only contains geometry class information, not other match is possible
            if (len(elements1[id1][1]) == 1) or (len(elements2[id2][1]) == 1):
                # Does the geometry class match?
                if elements1[id1][1][0] == elements2[id2][1][0]:
                    match += 0.5
            # If both of the elements contain shape information, then attempt to match both class and shape
            elif (len(elements1[id1][1]) == 2) and (len(elements2[id2][1]) == 2):
                # Does the geometry class match?
                if elements1[id1][1][0] == elements2[id2][1][0]:
                    # Does the shape match?
                    if elements1[id1][1][1] == elements2[id2][1][1]:
                        match += 1
                    else:
                        match += 0.5

    # Return the average percentage match
    return match/len(sg_nodes)

def jointAttributeMatching(sg_edges, joints1, joints2):
    """Check whether the edges in G1 and G2, which are associated
    with the edges in the subgraph, have matching attributes."""
    match = 0
    # Cycle 
    for edge in sg_edges:
        v1 = edge[0][0]
        v2 = edge[1][0]
        u1 = edge[0][1]
        u2 = edge[1][1]
        # Fetch joint attribute for edge in graph 1
        if (v1,v2) in joints1.keys():
            type1 = joints1[(v1,v2)][2]
        elif (v2,v1) in joints1.keys():
            type1 = joints1[(v2,v1)][2]
        else:
            raise NameError(str(v1,v2) + "edge does not exist in joint list.")
        # Fetch joint attribute for edge in graph 2
        if (u1, u2) in joints2.keys():
            type2 = joints2[(u1, u2)][2]
        elif (u2, u1) in joints2.keys():
            type2 = joints2[(u2, u1)][2]
        else:
            raise NameError(str(u1, u2) + "edge does not exist in joint list.")
        if type1 == type2: match += 1
    return match/len(sg_edges)

def attributeSimilarityScore(max_cliques, cEdges, graph1, graph2):
    max_cliques_with_ss = []
    for sg in max_cliques:
        sg_edges = []
        for v1, v2 in itertools.product(sg, sg):
            if (v1,v2) in cEdges:
                sg_edges.append((v1,v2))
        element_match = elementAttributeMatching(sg, graph1.elements, graph2.elements)
        joint_match = jointAttributeMatching(sg_edges, graph1.joints, graph2.joints)
        max_cliques_with_ss.append([sg, element_match, joint_match])
    max_cliques_with_ss.sort(key=takeAverageMatch, reverse=True)
    return max_cliques_with_ss