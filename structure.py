from collections import defaultdict

class Network:
    """The network comprises of a set of structures"""
    # Creat list of structures
    structures = {}

    def __init__(self,maxclique=None):
        self.maxclique = []
    #     if structureID not in self.structures.keys():
    #         self.structures[structureID] = {} 

    def modularProduct(self, struct1, struct2):
        """Find the modular product of two graphs"""
        # Create local sets of edges and vetrices
        V1 = struct1.nodes
        V2 = struct2.nodes
        E1 = struct1.edges
        E2 = struct2.edges

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

    def neighbourSet(self, V, E):
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

    def BronKerbosch(self, R, P, X, N):
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
                for r in self.BronKerbosch(R.union({u}), Pit.intersection(N[u]), X.intersection(N[u]), N):
                    yield r
                # Exclude the current vertex from the list of vertices which can be added to R
                Pit.remove(u)
                X.add(u)
            
    
    def BronKerboschPivot(self, R, P, X, N):
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
                    for r in self.BronKerboschPivot(Rit, Pit.intersection(N[u]), X.intersection(N[u]), N):
                        yield r
                    X.add(u)

    def maximalCliquesBK(self, V, E):
        """Initialises Bron-Kerbosch clique finding algorithms"""
        cliques = []
        # Initialise other variables required for Bron-Kerbosch
        N = self.neighbourSet(V, E)
        # Set R and X to be the empty set
        R = set()
        X = set()
        # Set P to be the vertex set
        P = set(V)
        # for v in self.degeneracy_ordering(N):
        #     [cliques.append(r) for r in self.BronKerbosch(R.union({v}), P.intersection(N[v]), X.intersection(N[v]), N)]
        #     P.remove(v)
        #     X.add(v)
        # return list(cliques)
        return list(self.BronKerbosch(R, P, X, N))

    def findCedges(self, E, E1, E2):
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
            if {u1,u2} in E1 or {u2,u1} in E1:
                # If v1 and v2 in G2 are adjacent
                if {v1,v2} in E2 or {v2,v1} in E2:
                    cEdges.add(edge)
            else:
                dEdges.add(edge)  
        return cEdges, dEdges 

    def maximalCliquesCedges(self, V, E, cEdges, dEdges):
        cliques = list()
        # Create the neighbour set
        N = self.neighbourSet(V, E)
        T = set()
        # Initialise c-clique finding algorithm for each vertex
        # for u in sorted(list(V)):
        for u in self.degeneracy_ordering(N):
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
            [cliques.append(r) for r in self.enumerateCcliques(R, P, D, X, N, T, cEdges)]
            T.add(u)
        return cliques

    def enumerateCcliques(self, R, P, D, X, N, T, cEdges):
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
                for r in self.enumerateCcliques(Rit, 
                                                Pit.intersection(N[u]), 
                                                Dit.intersection(N[u]),
                                                Xit.intersection(N[u]), 
                                                N, T, cEdges): yield r
                X.add(u)
            
    def inexactGraphComparison(self, graph1, graph2):
        # Create possible pairs
        pass

    def degeneracy_ordering(self, graph):
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

class Structure(Network):
    # Create list of elements
    elements = {}
    # Create list of joints
    joints = {}

    def __init__(self,
                 structureID,
                 graph=None,
                 nodes=None,
                 edges=None):
        self.structureID = structureID
        if graph == None:
            self.graph = {}
        else:
            self.graph = graph
        self.nodes = nodes
        self.edges = edges
        self.elements[structureID] = {}
        self.joints[structureID] = {}

    def addNode(self, node):
        """Adds node to the graph"""
        if node not in self.graph:
            self.graph[node] = []
            return self.graph[node]
        else:
            return None
    
    def addEdge(self, edges):
        """Add edges to the graph"""
        (node1, node2) = tuple(edges)
        # Add connection to node on graph object
        if node1 in self.graph:
            self.graph[node1].append(node2)
        else:
            raise KeyError("first node not found in graph")
        # Add connection in corresponding node
        if node2 in self.graph:
            self.graph[node2].append(node1)
        else:
            raise KeyError("second node not found in graph")

    def nodeList(self):
        """Returns list of nodes in graph"""
        nodes = list(self.graph.keys())
        self.nodes = nodes
        return nodes

    def edgeList(self):
        """Returns list of edges in graph"""
        edges = []
        for node in self.graph:
            for nxtnode in self.graph[node]:
                    # Check if set of nodes already exist in edges
                    if {nxtnode, node} not in edges:
                        edges.append({node, nxtnode})
        self.edges = edges
        return edges
    
    def addElements(self):
        """Adds nodes from list of elements"""
        nodes = list(self.elements.keys())
        for node in nodes:
            self.addNode(node)
        return nodes
    
    def addJoints(self):
        """Adds edges from list of joints"""
        for jointID in self.joints:
            # Check whether the joint is connected to any elements
            (node1, node2) = self.joints[jointID][0]
            nodes = self.nodeList()
            if node1 in nodes and node2 in nodes:
                # Add edge defined for a given join ID
                self.addEdge(self.joints[jointID][0])
            else:
                raise ValueError("nodes not found in graph for jointID=" + str(jointID))
    
    def addToNetwork(self):
        """Adds the graph of the structure to the network"""
        Network.structures[self.structureID] = {'nodes' : self.nodeList(), 'edges': self.edgeList()}