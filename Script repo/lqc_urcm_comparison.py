import numpy as np
import matplotlib.pyplot as plt

# Parameters
timesteps = 500
H0 = 0.05  # Hubble parameter (LQC baseline)
a0 = 1.0   # Initial scale factor
gamma = 0.02  # Noise level for entropy
rho_c = 0.41  # Critical density for bounce (in Planck units)
dim = 2       # Hilbert space dimension for entropy
rho_0 = 1.0   # Initial energy density

# LQC scale factor: symmetric bounce
def lqc_scale_factor(t, H0):
    return a0 * np.cosh(H0 * t)

# URCM scale factor: oscillatory with bounce
def urcm_scale_factor(t, H0, rho, rho_c):
    return a0 * (1 + 0.8 * np.sin(4 * np.pi * t)) * (1 - rho/rho_c)

# Entropy calculation
def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

# Apply noise for entropy evolution
def apply_noise(rho, gamma):
    noise = gamma * np.random.randn(dim, dim)
    noise = (noise + noise.T) / 2
    rho += noise
    rho = (rho + rho.T) / 2
    rho /= np.trace(rho)
    return rho

# Simulation
t = np.linspace(-1, 1, timesteps)  # Symmetric time range for bounce
rho = np.eye(dim) / dim  # Initial mixed state
lqc_scales = []
urcm_scales = []
lqc_entropies = []
urcm_entropies = []

for i in range(timesteps):
    # Scale factors
    lqc_scales.append(lqc_scale_factor(t[i], H0))
    urcm_scales.append(urcm_scale_factor(t[i], H0, rho_0, rho_c))
    
    # Entropy: LQC (no reset)
    rho_lqc = apply_noise(rho, gamma)
    lqc_entropies.append(entropy(rho_lqc))
    
    # Entropy: URCM (with reset if below threshold)
    rho_urcm = apply_noise(rho, gamma)
    if entropy(rho_urcm) < 1e-3:  # Reset threshold
        rho_urcm = np.array([[1, 0], [0, 0]])
    urcm_entropies.append(entropy(rho_urcm))
    
    rho = rho_lqc  # Update for next iteration

# Plot results
plt.figure(figsize=(12, 6))

# Scale factor plot
plt.subplot(1, 2, 1)
plt.plot(t, lqc_scales, label="LQC Scale Factor")
plt.plot(t, urcm_scales, label="URCM Scale Factor")
plt.xlabel("Time")
plt.ylabel("Scale Factor (a)")
plt.title("Scale Factor Evolution")
plt.legend()
plt.grid(True)

# Entropy plot
plt.subplot(1, 2, 2)
plt.plot(t, lqc_entropies, label="LQC Entropy")
plt.plot(t, urcm_entropies, label="URCM Entropy")
plt.xlabel("Time")
plt.ylabel("Entropy")
plt.title("Entropy Evolution")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("lqc_urcm_comparison.png")
plt.show()