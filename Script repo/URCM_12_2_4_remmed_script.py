
# URCM Simulation: Local Entropy Inversions During Recursive Collapse

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Set seed for reproducibility
np.random.seed(101)

# Define the number of independent simulation runs and recursion cycles
num_simulations = 100
max_cycles = 50

# Create a matrix to hold entropy values for each run
entropy_matrix = []

# Begin simulation over multiple independent runs
for i in range(num_simulations):
    entropy = 1.0  # Start with normalised entropy
    series = []
    for _ in range(max_cycles):
        if np.random.rand() < 0.1:
            # 10% chance of local entropy inversion (a temporary increase)
            entropy *= np.random.uniform(1.01, 1.1)
        else:
            # Otherwise, entropy decreases as expected
            entropy *= np.random.uniform(0.90, 0.98)
        series.append(entropy)
    entropy_matrix.append(series)

# Convert simulation output into a pandas DataFrame
df_entropy = pd.DataFrame(entropy_matrix)
df_entropy.columns = [f"Cycle_{i+1}" for i in range(max_cycles)]
df_entropy["Simulation"] = np.arange(1, num_simulations + 1)

# Compute mean and standard deviation of entropy at each cycle
mean_entropy = df_entropy.drop(columns=["Simulation"]).mean()
std_entropy = df_entropy.drop(columns=["Simulation"]).std()
cycles = np.arange(1, max_cycles + 1)

# Convert to NumPy arrays for plotting
mean_entropy = mean_entropy.to_numpy(dtype=np.float64)
std_entropy = std_entropy.to_numpy(dtype=np.float64)
cycles = np.array(cycles, dtype=np.float64)

# Plot the results with confidence bands (±1 standard deviation)
plt.figure(figsize=(10, 6))
plt.plot(cycles, mean_entropy, label="Mean Entropy")
plt.fill_between(cycles, mean_entropy - std_entropy, mean_entropy + std_entropy, alpha=0.3)
plt.title("Entropy with Local Inversions Over Recursive Cycles")
plt.xlabel("Cycle")
plt.ylabel("Entropy")
plt.grid(True)
plt.tight_layout()

# Save the plot as an image file
plt.savefig("URCM_12_2_4_entropy_spikes.png")
plt.close()
