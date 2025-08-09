
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import numpy as np

# Define recursive operators
operators = ['B', 'C', 'S']
max_depth = 3  # recursion depth

# Generate all paths of a certain depth
paths = list(itertools.product(operators, repeat=max_depth))

# Normalize paths by circular permutation (loop equivalence)
def normalize_path(path):
    perms = [tuple(path[i:] + path[:i]) for i in range(len(path))]
    return min(perms)

equivalence_classes = {}
for p in paths:
    norm = normalize_path(list(p))
    if norm not in equivalence_classes:
        equivalence_classes[norm] = []
    equivalence_classes[norm].append(p)

# Create graph
G = nx.DiGraph()
for i, (norm, members) in enumerate(equivalence_classes.items()):
    class_name = "→".join(norm)
    G.add_node(class_name, size=len(members))
    for m in members:
        path_name = "→".join(m)
        G.add_node(path_name)
        G.add_edge(path_name, class_name)

# Draw graph
sizes = [300 + 200 * G.nodes[n].get('size', 1) for n in G.nodes]
colors = ['skyblue' if '→' in n and n.count('→') == max_depth - 1 else 'lightgray' for n in G.nodes]

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=sizes, node_color=colors, edge_color='gray', arrows=True)
plt.title("Homotopy Equivalence of Recursive Operator Paths (Depth = 3)")
plt.tight_layout()
plt.savefig("recursive_operator_homotopy.png")
plt.show()
