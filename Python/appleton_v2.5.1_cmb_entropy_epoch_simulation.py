
import numpy as np
import matplotlib.pyplot as plt

# Simulating entropy bounces/plateaus inspired by cosmological epoch transitions
timesteps = 500
epochs = [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500)]
noise_levels = [0.01, 0.03, 0.005, 0.04, 0.002]  # alternating expansion/contraction/noise-reset

def simulate_entropy_bounces(timesteps, epochs, noise_levels):
    rho = np.eye(2) / 2
    entropies = []

    for idx, (start, end) in enumerate(epochs):
        gamma = noise_levels[idx]
        for t in range(start, end):
            noise = gamma * np.random.randn(2, 2)
            noise = (noise + noise.T) / 2
            rho += noise
            rho = (rho + rho.T) / 2
            rho /= np.trace(rho)

            eigvals = np.linalg.eigvalsh(rho)
            eigvals = eigvals[eigvals > 0]
            entropy = -np.sum(eigvals * np.log(eigvals))
            entropies.append(entropy)

    return entropies

entropies = simulate_entropy_bounces(timesteps, epochs, noise_levels)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(entropies, label="Simulated Cosmological Entropy Curve")
plt.title("Recursive Epoch Entropy Plateaus and Bounces")
plt.xlabel("Timestep")
plt.ylabel("Entropy")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save plot
plt.savefig("/mnt/data/cosmological_entropy_epochs_simulation_v2.5.1.png")
