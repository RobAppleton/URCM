import numpy as np
import matplotlib.pyplot as plt

num_universes = 50
max_timesteps = 500
entropy_threshold = 1e-3
gamma = 0.02
use_noise = True


def apply_noise(rho, gamma=0.0):
    if gamma > 0.0:
        noise = gamma * np.random.randn(*rho.shape)
        noise = (noise + noise.T) / 2  # Hermitian
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)
    return rho


def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

def simulate_universe_safe():
    try:
        rho = np.eye(2) / 2
        for t in range(max_timesteps):
            if use_noise:
                rho = apply_noise(rho, gamma)
            ent = entropy(rho)
            if ent < entropy_threshold:
                return t
    except Exception as e:
        print("Error in simulation:", e)
    return None

bounce_times = []

for _ in range(num_universes):
    bt = simulate_universe_safe()
    bounce_times.append(bt if bt is not None else max_timesteps)

plt.hist(bounce_times, bins=20, edgecolor='black')
plt.title("Bounce Times with Noise (Safe Mode)")
plt.xlabel("Timesteps")
plt.ylabel("Number of Universes")
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/bounce_histogram_safe_noise_v2.1.2.png")