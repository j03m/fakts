import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add neurons as nodes
# Input Layer
G.add_node('Input1')

# First Hidden Layer
for i in range(1, 5):
    G.add_node(f'H1_{i}')

# Add edges to represent the weights between neurons
# From Input Layer to First Hidden Layer
for i in range(1, 5):
    G.add_edge('Input1', f'H1_{i}', weight=f'w_{i}')

# Create plot
pos = {'Input1': (0, 0.5)}
for i in range(1, 5):
    pos[f'H1_{i}'] = (1, i / 4)

edge_labels = nx.get_edge_attributes(G, 'weight')

nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, font_size=18)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=14)
plt.title('Connections from Input Layer to First Hidden Layer')
plt.show()
