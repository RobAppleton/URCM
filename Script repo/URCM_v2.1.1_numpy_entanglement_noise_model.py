import numpy as np
import matplotlib.pyplot as plt

# Parameters
timesteps = 200
gamma = 0.05  # noise level
dim = 4  # 2 qubits = 4D Hilbert space

# Initialize maximally mixed state
rho = np.eye(dim) / dim

# Reference pure state approximation: |00><00|
ref_state = np.zeros((dim, dim))
ref_state[0, 0] = 1.0

# Tracking
fidelities = []
entropies = []

def fidelity_approx(rho1, rho2):
    # Use trace overlap approximation (Tr[rho1 * rho2])
    return np.real(np.trace(rho1 @ rho2))

def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

for t in range(timesteps):
    # Apply symmetric random noise
    noise = gamma * np.random.randn(dim, dim)
    noise = (noise + noise.T) / 2  # ensure Hermitian
    rho += noise
    rho = (rho + rho.T) / 2  # ensure Hermitian
    rho /= np.trace(rho)  # normalize

    fidelities.append(fidelity_approx(ref_state, rho))
    entropies.append(entropy(rho))

# Plot
plt.figure(figsize=(10, 5))
plt.plot(fidelities, label='Fidelity Decay')
plt.plot(entropies, label='Entropy Growth')
plt.xlabel("Timestep")
plt.ylabel("Value")
plt.title("Fidelity and Entropy under Decoherence (NumPy Model)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/entanglement_fidelity_entropy_plot_numpy.png")