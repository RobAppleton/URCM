
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(123)
cycles = 5
G = nx.Graph()
G.add_node(0, cycle=0)

for i in range(1, cycles + 1):
    G.add_node(i, cycle=i)
    G.add_edge(i, i - 1, fidelity=np.random.uniform(0.7, 1.0))
    if i > 2 and np.random.rand() < 0.8:
        target = np.random.randint(0, i - 1)
        G.add_edge(i, target, fidelity=np.random.uniform(0.4, 0.9))

V = G.number_of_nodes()
E = G.number_of_edges()
beta_0 = nx.number_connected_components(G)
beta_1 = E - V + beta_0

pos = nx.spring_layout(G, seed=123)
plt.figure(figsize=(6, 5))
nx.draw(G, pos, with_labels=True, node_size=600, edge_color='gray', width=2)
plt.title(f"Simplicial Recursion Network (5 Cycles)\nBetti-0: {beta_0}, Betti-1: {beta_1}")
plt.tight_layout()
plt.savefig("simplicial_homology_5_cycles.png")
plt.show()
