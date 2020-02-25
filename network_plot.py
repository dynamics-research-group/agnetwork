import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G1 = nx.Graph()

G1.add_edge('t1', 'a1')
G1.add_edge('t1', 'a2')
G1.add_edge('t1', 'b1')
G1.add_edge('t1', 'b2')
G1.add_edge('t1', 'b3')
G1.add_edge('a1', 'a2')
G1.add_edge('a1', 'b1')
G1.add_edge('a1', 'b2')
G1.add_edge('a1', 'b3')
G1.add_edge('a2', 'b1')
G1.add_edge('a2', 'b2')
G1.add_edge('a2', 'b3')
G1.add_edge('b1', 'b2')
G1.add_edge('b1', 'b3')
G1.add_edge('b2', 'b3')

pos = nx.circular_layout(G1)
 
widths = np.square(np.array([0.38,0.37,0.25,0.38,0.23,0.59,0.14,0.23,0.3,0.17,0.26,0.35,0.44,0.33,0.58]))

nx.draw_networkx_nodes(G1, pos, node_color='w', node_size=700)
nx.draw_networkx_edges(G1, pos, edge_color='b', width=widths*4)
nx.draw_networkx_labels(G1, pos, font_size=20, font_family='sans-serif')

plt.axis('off')
plt.show()

# G2 = nx.Graph()

# G2.add_node('t1')
# G2.add_node('a1')
# G2.add_node('a2')
# G2.add_node('b1')
# G2.add_node('b2')
# G2.add_node('b3')

# pos = {'t1': np.array([0, 0]), 
#        'a1': np.array([-0.01, 0.14]), 
#        'a2': np.array([0.01, 0.14]), 
#        'b1': np.array([0, 0.06]),
#        'b2': np.array([0, 0.14]),
#        'b3': np.array([0.01, 0.05])}

# nx.draw_networkx_nodes(G2, pos, node_color='w', node_size=700)
# nx.draw_networkx_edges(G2, pos, edge_color='b', width=widths*4)
# nx.draw_networkx_labels(G2, pos, font_size=20, font_family='sans-serif')

# plt.axis('off')
# plt.show()