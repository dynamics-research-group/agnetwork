import networkx as nx
import matplotlib.pyplot as plt
import json

def plot_mcs_from_nodes(MCS_nodes, graph1, graph2):
    MCS_edges = []
    for node1 in MCS_nodes:
        for node2 in MCS_nodes:
            if node1 != node2:
                v1 = node1[0].lower()
                v2 = node2[0].lower()
                u1 = node1[1].lower()
                u2 = node2[1].lower()
                if v2 in graph1[v1] and u2 in graph2[u1]:
                    MCS_edges.append((node1, node2))
    graph_plot(MCS_nodes, MCS_edges)
    return MCS_nodes, MCS_edges

def plot_MCS_from_cedges(clique_set, cEdges):
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
    graph_plot(sg_nodes, sg_edges)

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

def graph_plot(nodes, edges, labels=False):
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

def load_AG_from_json_file(file_path):
	with open(file_path, "r") as infile:
		structure = json.load(infile)
	return structure["attributed_graph"]

if __name__ == "__main__":
	directory = "/Users/Julian/Documents/WorkDocuments/Irreducible Element/IE models/json/" 

	graph1_attributed = load_AG_from_json_file(f"{directory}Randlestown.json")

	graph2_attributed = load_AG_from_json_file(f"{directory}Castledawson.json")

	# MCS_nodes = [('X', 'DD'), ('Q', 'BB'), ('K', 'AA'), ('W', 'CC'), ('E', 'M'), ('J', 'R'), ('L', 'S'), 
	# 			 ('M', 'T'), ('N', 'U'), ('O', 'V'), ('R', 'W'), ('S', 'X'), ('T', 'Y'), ('U', 'Z'), 
	# 			 ('A', 'B'), ('B', 'F'), ('C', 'H'), ('D', 'L'), ('F', 'N'), ('G', 'O'), ('H', 'P'), 
	# 			 ('I', 'Q'), ('Z', 'EE'), ('Y', 'FF')]

	# nodes, edges = plot_mcs_from_nodes(MCS_nodes, graph1_attributed["graph"], graph2_attributed["graph"])

	MCS_nodes2 = [('x', 'dd'), ('q', 'bb'), ('k', 'aa'), ('w', 'cc'), ('j', 'r'), ('l', 's'), ('m', 't'), ('n', 'u'), ('o', 'v'), ('r', 'w'), ('s', 'x'), ('t', 'y'), ('u', 'z'), ('f', 'n'), ('g', 'o'), ('h', 'p'), ('i', 'q'), ('y', 'ee'), ('z', 'ff'), ('2', '2'), ('3', '3')]

	nodes, edges = plot_mcs_from_nodes(MCS_nodes2, graph1_attributed["graph"], graph2_attributed["graph"])

	G = nx.Graph()
	# Add nodes and edges to the graph object
	G.add_edges_from(edges)
	G.add_nodes_from(nodes)