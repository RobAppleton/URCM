import numpy as np
import matplotlib.pyplot as plt

timesteps = 500
entropy_threshold = 1e-3
gamma = 0.02  # Noise level
use_noise = True

rho = np.eye(2) / 2
entropies = []


def apply_noise(rho, gamma=0.0):
    if gamma > 0.0:
        noise = gamma * np.random.randn(*rho.shape)
        noise = (noise + noise.T) / 2  # Hermitian
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)
    return rho


def entropy(rho):
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 0]
    return -np.sum(eigvals * np.log(eigvals))

for t in range(timesteps):
    if use_noise:
        rho = apply_noise(rho, gamma)
    ent = entropy(rho)
    entropies.append(ent)
    if ent < entropy_threshold:
        break

plt.plot(entropies)
plt.title("Single Universe Entropy with Noise" if use_noise else "Entropy without Noise")
plt.xlabel("Timestep")
plt.ylabel("Entropy")
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/single_universe_entropy_noise_v2.1.2.png")