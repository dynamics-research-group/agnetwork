class Network:
    """The network comprises of a set of structures"""
    # Creat list of structures
    structures = {}
    # Create list of elements
    elements = {}
    # Create list of joints
    joints = {}

    def __init__(self,maxclique=None):
        self.maxclique = []
    #     if structureID not in self.structures.keys():
    #         self.structures[structureID] = {} 
        pass

    def modularProduct(self, struct1, struct2):
        """Find the modular product of two graphs"""
        # Create local sets of edges and vetrices
        V1 = Network.structures[struct1]['nodes']
        V2 = Network.structures[struct2]['nodes']
        E1 = Network.structures[struct1]['edges']
        E2 = Network.structures[struct2]['edges']
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
                        if {U[0],V[0]} in E1 and {U[1],V[1]} in E2:
                            modprodE.add((U,V))
                        # or u0 is NOT adjacent to v0 and u1 is NOT adjacent to v1
                        elif {U[0],V[0]} not in E1 and {U[1],V[1]} not in E2:
                            modprodE.add((U,V))
        # Return a dictionary defining the resultant graph
        return {'nodes' : modprodV, 'edges' : modprodE}

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
        if P == set() and X == set():
            self.maxclique.append(R)
            return
        Pit = P.copy()
        for v in P:
            if R == set():
                R = {v}
            else:
                R.add(v)
            self.BronKerbosch(R, Pit.intersection(N[v]), X.intersection(N[v]), N)
            Pit.remove(v)
            X.add(v)

    def maximalCliques(self, V, E):
        N = self.neighbourSet(V, E)
        # Set R and X to be the empty set
        R = set()
        X = set()
        # Set P to be the vertex set
        P = set(V)
        self.BronKerbosch(R, P, X, N)
        print(self.maxclique)

class Structure(Network):
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
        nodes = list(self.elements[self.structureID].keys())
        for node in nodes:
            self.addNode(node)
        return nodes
    
    def addJoints(self):
        """Adds edges from list of joints"""
        local_joints = self.joints[self.structureID]
        for jointID in local_joints:
            # Check whether the joint is connected to any elements
            (node1, node2) = local_joints[jointID][0]
            nodes = self.nodeList()
            if node1 in nodes and node2 in nodes:
                # Add edge defined for a given join ID
                self.addEdge(local_joints[jointID][0])
            else:
                raise ValueError("nodes not found in graph for jointID=" + str(jointID))
    
    def addToNetwork(self):
        """Adds the graph of the structure to the network"""
        Network.structures[self.structureID] = {'nodes' : self.nodeList(), 'edges': self.edgeList()}