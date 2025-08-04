
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
timesteps = 500
a0 = 1.0  # initial scale factor
H0 = 0.05  # base Hubble-like expansion rate
gamma = 0.02  # noise level baseline

# Time array
t = np.linspace(0, 1, timesteps)

# Define scale factor over time (mimicking a bounce model)
def scale_factor(t):
    return a0 * (1 + 0.8 * np.sin(4 * np.pi * t))  # Bounce-like periodic oscillation

# Modified noise model: gamma modulated by scale factor
def apply_curvature_noise(rho, gamma, a):
    curved_gamma = gamma * (1 + 0.5 * np.cos(2 * np.pi * a))  # curvature-modulated noise
    noise = curved_gamma * np.random.randn(*rho.shape)
    noise = (noise + noise.T) / 2
    rho += noise
    rho = (rho + rho.T) / 2
    rho /= np.trace(rho)
    return rho

# Entropy function
def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

# Simulation
rho = np.eye(2) / 2
entropies = []
scales = []

for i in range(timesteps):
    a = scale_factor(t[i])
    rho = apply_curvature_noise(rho, gamma, a)
    entropies.append(entropy(rho))
    scales.append(a)

# Plot entropy with scale factor overlay
fig, ax1 = plt.subplots(figsize=(10, 5))

color = 'tab:blue'
ax1.set_xlabel('Timestep')
ax1.set_ylabel('Entropy', color=color)
ax1.plot(entropies, color=color, label='Entropy')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Scale Factor (a)', color=color)
ax2.plot(scales, color=color, linestyle='--', label='Scale Factor')
ax2.tick_params(axis='y', labelcolor=color)

plt.title("Entropy Evolution with Scale Factor Modulation")
fig.tight_layout()

# Save figure
plt.savefig("/mnt/data/curvature_modulated_entropy_simulation_v2.6.png")
