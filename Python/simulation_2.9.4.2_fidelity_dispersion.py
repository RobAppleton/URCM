
import numpy as np
import matplotlib.pyplot as plt

def simulate_fidelity_dispersion(num_subsystems=25, num_cycles=30, mean_decay=0.03, noise_level=0.02):
    fidelities = np.ones((num_cycles + 1, num_subsystems))

    for cycle in range(1, num_cycles + 1):
        noise = np.random.normal(loc=0.0, scale=noise_level, size=num_subsystems)
        decay = 1.0 - mean_decay + noise
        fidelities[cycle] = fidelities[cycle - 1] * decay
        fidelities[cycle] = np.clip(fidelities[cycle], 0, 1)

    return fidelities

# Run simulation
fidelity_matrix = simulate_fidelity_dispersion()

# Compute curvature proxy
curvature_proxy = np.std(fidelity_matrix, axis=1)

# Plot fidelity heatmap
plt.figure(figsize=(10, 6))
plt.imshow(fidelity_matrix.T, aspect='auto', cmap='viridis', interpolation='nearest')
plt.colorbar(label='Fidelity')
plt.title('Fidelity Across Subsystems Over Cycles (Emergent Dispersion)')
plt.xlabel('Cycle')
plt.ylabel('Subsystem')
plt.savefig("fidelity_dispersion_heatmap.png")
plt.show()

# Plot curvature proxy
plt.figure()
plt.plot(np.arange(fidelity_matrix.shape[0]), curvature_proxy, marker='o')
plt.title('Curvature Proxy via Fidelity Dispersion')
plt.xlabel('Cycle')
plt.ylabel('Standard Deviation of Fidelity')
plt.grid(True)
plt.savefig("curvature_proxy_stddev_plot.png")
plt.show()
