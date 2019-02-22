class Structure:
    # Create list of elements
    elements = {}
    # Create list of joints
    joints = {}
    # Initialise structure with either pre-defined or empty graph object
    def __init__(self,
                structureID,
                graph=None,
                nodes=None,
                edges=None):
        self.structureID = structureID
        if graph == None:
            graph = {}
        self.graph = graph
        self.nodes = {}
        self.edges = {}

    # Adds node to the graph
    def addNode(self,node):
        if node not in self.graph:
            self.graph[node] = []
            return self.graph[node]
        else:
            return None
    
    # Add edges to the graph
    def addEdge(self,edges):
        (node1, node2) = tuple(edges)
        # Add connection to node on graph object
        if node1 in self.graph:
            self.graph[node1].append(node2)
        else:
            raise KeyError("First node not found in graph")
        # Add connection in corresponding node
        if node2 in self.graph:
            self.graph[node2].append(node1)
        else:
            raise KeyError("Second node not found in graph")

    # Returns list of nodes in graph
    def nodeList(self):
        nodes = list(self.graph.keys())
        return nodes

    # Returns list of edges in graph
    def edgeList(self):
        edges = []
        for node in self.graph:
            for nxtnode in self.graph[node]:
                    # Check if set of nodes already exist in edges
                    if {nxtnode, node} not in edges:
                        edges.append({node, nxtnode})
        return edges
    
    # Adds nodes from list of elements
    def addElements(self):
        nodes = self.elements.keys()
        if len(self.graph) != len(nodes):
            self.graph = {}
        for node in nodes:
            self.addNode(node)
    
    # Adds edges from list of joints
    def addJoints(self):
        for jointID in self.joints:
            # Check whether the joint is connected to any elements
            (node1, node2) = self.joints[jointID][0]
            nodes = self.nodeList()
            if node1 in nodes and node2 in nodes:
                # Add edge defined for a given join ID
                self.addEdge(self.joints[jointID][0])