
import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
num_universes = 10
timesteps = 1000
dimension = 10  # Dimensional space for each universe
threshold = 0.1  # Threshold distance for intersection/linking
link_matrix = np.zeros((num_universes, num_universes, timesteps))

# Random walk function in 10D
def random_walk(start, steps):
    walk = [start]
    for _ in range(steps - 1):
        step = np.random.normal(0, 0.05, dimension)
        walk.append(walk[-1] + step)
    return np.array(walk)

# Generate paths for each universe in 10D space
trajectories = [random_walk(np.random.rand(dimension), timesteps) for _ in range(num_universes)]

# Calculate distances and detect intersections
for t in range(timesteps):
    for i in range(num_universes):
        for j in range(i + 1, num_universes):
            dist = np.linalg.norm(trajectories[i][t] - trajectories[j][t])
            if dist < threshold:
                link_matrix[i][j][t] = 1
                link_matrix[j][i][t] = 1

# Count total links per timestep
link_counts = np.sum(link_matrix, axis=(0, 1)) / 2  # divide by 2 to account for symmetry

# Plot the result
plt.figure(figsize=(12, 6))
plt.plot(range(timesteps), link_counts, label='Number of Inter-Universe Link Events')
plt.xlabel('Timestep')
plt.ylabel('Links Detected')
plt.title('Quantum Link Events Between 10-Dimensional Universes Over Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
