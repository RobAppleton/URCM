
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Define the cube vertices and edges for operator sequences
vertices = {
    '000': (0, 0, 0),
    '100': (1, 0, 0),
    '010': (0, 1, 0),
    '110': (1, 1, 0),
    '001': (0, 0, 1),
    '101': (1, 0, 1),
    '011': (0, 1, 1),
    '111': (1, 1, 1)
}

edges = [
    ('000', '100'), ('000', '010'), ('000', '001'),
    ('100', '110'), ('100', '101'),
    ('010', '110'), ('010', '011'),
    ('001', '011'), ('001', '101'),
    ('110', '111'),
    ('011', '111'),
    ('101', '111')
]

labels = {
    '000': 'Start',
    '100': 'B',
    '010': 'C',
    '001': 'S',
    '110': 'B→C',
    '101': 'B→S',
    '011': 'C→S',
    '111': 'B→C→S'
}

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot vertices
for key, coord in vertices.items():
    ax.scatter(*coord, color='skyblue', s=100)
    ax.text(*coord, f"{labels.get(key, key)}", fontsize=10, ha='center', va='center')

# Plot edges
for edge in edges:
    p1 = np.array(vertices[edge[0]])
    p2 = np.array(vertices[edge[1]])
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='gray')

ax.set_title("Categorical Morphism Cube of Recursive Flows")
ax.set_axis_off()
plt.tight_layout()
plt.savefig("categorical_recursive_cube.png")
plt.show()
