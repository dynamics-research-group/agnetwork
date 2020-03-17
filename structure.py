class Network:
    """The network comprises of a set of structures"""
    # Creat list of structures
    structures = {}

    def __init__(self):
        pass
    #     if structureID not in self.structures.keys():
    #         self.structures[structureID] = {} 

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

    def __str__(self):
        return str(self.structureID)

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

    def numberOfNodes(self):
        """Retruns the size of the node set"""
        return len(self.nodeList())

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

    def numberOfEdges(self):
        """Retruns the size of the edge set"""
        return len(self.edgeList())
    
    def addElements(self):
        """Adds nodes from list of elements"""
        nodes = list(self.elements.keys())
        for node in nodes:
            self.addNode(node)
        return nodes
    
    def addJoints(self):
        """Adds edges from list of joints"""
        for key in self.joints.keys():
            # Check whether the joint is connected to any elements
            (node1, node2) = key
            nodes = self.nodeList()
            if node1 in nodes and node2 in nodes:
                # Add edge defined for a given join ID
                self.addEdge(list(key))
            else:
                raise ValueError("nodes not found in graph for jointID=" + str(self.joints[key][0]))
    
    def addToNetwork(self):
        """Adds the graph of the structure to the network"""
        Network.structures[self.structureID] = {'nodes' : self.nodeList(), 'edges': self.edgeList()}