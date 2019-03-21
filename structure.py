class Network:
    """The network comprises of a set of structures"""
    # Creat list of structures
    structures = {}
    # Create list of elements
    elements = {}
    # Create list of joints
    joints = {}

    def __init__(self):
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

        modularV = set()
        modularE = set()

        for u in V1:
            for v in V2:
                modularV.add((u, v))

        for U in modularV:
            for V in modularV:
                if U[0] != V[0] and U[1] != V[1]:
                    if (U[0],V[0]) in E1 and (U[1],V[1]) in E2:
                        if (U,V) and (V,U) not in modularE:
                            modularE.add((U,V))
                    elif (U[0],V[0]) not in E1 and (U[1],V[1]) not in E2:
                        if (U,V) and (V,U) not in modularE:
                            modularE.add((U,V))
        
        print(modularV)
        print(len(modularV))
        print(modularE)
        print(len(modularE))

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