import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


array = np.array([[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,1,0,0]])
print(array)
nodes = [0,1,2,3]
G = nx.DiGraph()
G.add_nodes_from(nodes)

edges = []
for hi, hv  in enumerate(array):
    for wi, wv in enumerate(hv):
        if(wv): edges.append((nodes[hi], nodes[wi]))
G.add_edges_from(edges)
pos = nx.spring_layout(G)

nx.draw_networkx(G, pos, with_labels=True, node_color="r", alpha=0.8)
plt.axis("off")
plt.show()
