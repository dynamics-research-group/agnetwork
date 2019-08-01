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
        # Initialise empty sets for modular product edges and vetices
        modprodV = set()
        modprodE = set()
        # Find the cartesian product of the sets of vertices for each graph
        for u in V1:
            for v in V2:
                modprodV.add((u, v))
        # Loop through each vertex in the modular product
        for U in modprodV:
            # Compare with every other vertex in the modular product
            for V in modprodV:
                # Exclude any vertices share the same point
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
        # Create copy of P to iterate over
        Pit = P.copy()
        for u in P:
            # Exclude the current vertex from the list of vertices which can be added to R
            Pit.remove(u)
            # Add the current vertex to R
            Rit = R.union({u})
            # Yield the maximal cliques from previous recursions
            for r in self.BronKerbosch(Rit, Pit.intersection(N[u]), X.intersection(N[u]), N):
                yield r
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
        # Initialise other variables required for Bron-Kerbosch
        N = self.neighbourSet(V, E)
        # Set R and X to be the empty set
        R = set()
        X = set()
        # Set P to be the vertex set
        P = set(V)
        r = self.BronKerboschPivot(R, P, X, N)
        return list(r)

    def findCedges(self, E, E1, E2):
        """Find the c-edges in a product graph"""
        # Initialise the set of c-edges
        cedges = set()
        # For each edge in the modular prodcut, form the edge or vertex pairs to test
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
                    cedges.add(edge)
        return cedges           

    def maximalCliquesCedges(self, V, E, cEdges):
        cliques = []
        T = set()
        # Create the neighbour set
        N = self.neighbourSet(V, E)
        # Initialise c-clique finding algorithm for each vertex
        for u in V:
            # Set R, D, X and R as the empty set
            P = set(V)
            D = set()
            X = set()
            # Initilise P with list of neighbouring vertices connected via c-edges
            # and D with list of neighbouring vertics connected via d-edges
            for v in N[u]:
                if (u,v) in cEdges or (v,u) in cEdges:
                    if v in T:
                        X.add(v)
                    else:
                        P.add(v)
                else: D.add(v)
            R = set({u})
            # Call c-clique finding algorithm
            r = self.enumerateCcliques(R, P, D, X, N, cEdges)
            T.add(u)
            cliques.append(list(r))
        return cliques

    def enumerateCcliques(self, R, P, D, X, N, cEdges):
        """Return the maximal c-cliques of a graph (modified Bron-Kerbosch algorithm)"""
        # If there are no more vertices which can be added to R, report clique as maximal
        if P == set() and X == set():
            yield R
        # Create copy of P to iterate over
        Pit = P.copy()
        for u in P:
            # Exclude the current vertex from the list of vertices which can be added to R
            Pit.remove(u)
            # Create copy of D for iteration
            Dit = D.copy()
            for v in D:
                if {u, v} in cEdges or {v, u} in cEdges:
                    # Add the current vertex to P
                    Pit = P.union({u})
                    # Remove the current vertex from the list of d-edges
                    Dit.remove(v)
            # Add the current vertex to R
            R = R.union({u})
            # Yield the maximal cliques from previous recursions
            for r in self.enumerateCcliques(R, 
                                            Pit.intersection(N[u]), 
                                            D.intersection(N[u]),
                                            X.intersection(N[u]), 
                                            N, cEdges):
                yield r
            X.add(u)
        pass

    def inexactGraphComparison(self, graph1, graph2):
        # Create possible pairs
        pass

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