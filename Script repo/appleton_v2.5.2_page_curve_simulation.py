
import numpy as np
import matplotlib.pyplot as plt

# Parameters
timesteps = 500
gamma = 0.02
entropy_threshold = 1e-3
dim = 2

# Simulate Page-like curve with a central minimum (information recovery phase)
def simulate_page_like_entropy(dim, timesteps, gamma):
    rho = np.eye(dim) / dim
    entropies = []

    for t in range(timesteps):
        # Decoherence phase
        noise = gamma * np.random.randn(dim, dim)
        noise = (noise + noise.T) / 2
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)

        # Small reverse information recovery to model late-time Hawking correlation
        if 200 < t < 350:
            recovery_noise = -0.5 * gamma * np.random.randn(dim, dim)
            recovery_noise = (recovery_noise + recovery_noise.T) / 2
            rho += recovery_noise
            rho = (rho + rho.T) / 2
            rho /= np.trace(rho)

        # Entropy calculation
        eigvals = np.linalg.eigvalsh(rho)
        eigvals = eigvals[eigvals > 0]
        entropy = -np.sum(eigvals * np.log(eigvals))
        entropies.append(entropy)

    return entropies

entropies = simulate_page_like_entropy(dim, timesteps, gamma)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(entropies, label="Simulated Page-like Curve")
plt.axvline(x=250, color='red', linestyle='--', label='Information Recovery Phase')
plt.title("Simulated Page Curve with Information Recovery")
plt.xlabel("Timestep")
plt.ylabel("Entropy")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save figure
plt.savefig("/mnt/data/page_curve_entropy_recovery_simulation_v2.5.2.png")
