import numpy as np
import matplotlib.pyplot as plt

# Parameters
timesteps = 200
gamma = 0.05  # noise level
dim = 4  # 2 qubits = 4D Hilbert space

# Initialize maximally entangled-like mixed state (simplified version)
rho = np.eye(dim) / dim  # start with high entropy state

# Track fidelity decay and entropy
fidelities = []
entropies = []

# Initial reference state: pure state approximation
ref_state = np.zeros((dim, dim))
ref_state[0, 0] = 1.0  # assume ideal starting state is |00><00|

def fidelity(rho1, rho2):
    sqrt_rho1 = np.real_if_close(np.linalg.sqrtm(rho1))
    inner = sqrt_rho1 @ rho2 @ sqrt_rho1
    return np.real(np.trace(np.linalg.sqrtm(inner))) ** 2

def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

for t in range(timesteps):
    # Simulate a noisy decoherence step (dephasing-like)
    noise = gamma * np.random.randn(dim, dim)
    noise = (noise + noise.T) / 2  # keep Hermitian
    rho += noise
    rho = (rho + rho.T) / 2  # ensure Hermitian
    rho /= np.trace(rho)  # normalize

    fidelities.append(fidelity(ref_state, rho))
    entropies.append(entropy(rho))

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(fidelities, label='Fidelity Decay')
plt.plot(entropies, label='Entropy Growth')
plt.xlabel("Timestep")
plt.ylabel("Value")
plt.title("Simplified Fidelity and Entropy with Decoherence")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/entanglement_fidelity_entropy_plot_numpy.png")