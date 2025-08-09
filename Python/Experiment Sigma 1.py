import numpy as np
import matplotlib.pyplot as plt
from qutip import *

# Simulation parameters
d = 50  # Hilbert space dimension
cycles = 5  # Number of cosmological cycles
noise_strengths = [0.0, 0.1]  # Noise-free and medium noise conditions

def generate_high_entropy_state(d):
    """Generate a high-entropy mixed state as the initial state."""
    psi_list = [rand_ket(d) for _ in range(20)]
    rho = sum([ket2dm(psi) for psi in psi_list]) / 20
    return rho.unit()

def compression_operator(rho):
    """Apply compression operator C: projects to a boundary subspace."""
    proj = Qobj(np.random.rand(d, d)).unit()
    return (proj * rho * proj.dag()).unit()

def entropy_reset_operator(rho):
    """Apply entropy reset operator S: projects to the lowest-entropy eigenstate."""
    eigvals, eigvecs = rho.eigenstates()
    return (eigvecs[0] * eigvecs[0].dag()).unit()

def bounce_operator(rho):
    """Apply bounce operator B: unitary evolution with a random Hermitian Hamiltonian."""
    H = rand_herm(d)
    U = (-1j * H).expm()
    return (U * rho * U.dag()).unit()

def apply_noise(rho, strength):
    """Apply depolarizing noise to the state."""
    identity = qeye(d)
    return ((1 - strength) * rho + strength * (identity / d)).unit()

# Initialize results dictionary
results = {}

for ε in noise_strengths:
    entropy_vals = []
    memory_vals = []

    # Initialize quantum state
    rho_initial = generate_high_entropy_state(d)
    rho_current = rho_initial

    for _ in range(cycles):
        # Apply operator sequence: R = B ∘ S ∘ C
        rho_next = bounce_operator(entropy_reset_operator(compression_operator(rho_current)))

        # Optionally add noise
        rho_next = apply_noise(rho_next, ε)

        # Record von Neumann entropy and fidelity with initial state
        entropy_vals.append(entropy_vn(rho_next))
        memory_vals.append(fidelity(rho_initial, rho_next))

        # Prepare for next cycle
        rho_current = rho_next

    results[ε] = {
        'entropy': entropy_vals,
        'memory': memory_vals
    }

# Plotting
cycles_range = np.arange(1, cycles + 1)
colors = ['orange', 'orangered']

fig, axs = plt.subplots(2, 1, figsize=(8, 8))

# Entropy plot
for idx, ε in enumerate(noise_strengths):
    axs[0].plot(cycles_range, results[ε]['entropy'], label=f"Noise ε = {ε}", color=colors[idx], marker='o')
axs[0].set_title("Entropy per Cycle (Sₙ)")
axs[0].set_xlabel("Cycle")
axs[0].set_ylabel("Von Neumann Entropy")
axs[0].legend()
axs[0].grid(True)

# Fidelity plot
for idx, ε in enumerate(noise_strengths):
    axs[1].plot(cycles_range, results[ε]['memory'], label=f"Noise ε = {ε}", color=colors[idx], marker='s')
axs[1].set_title("Memory Fidelity per Cycle (Mₙ)")
axs[1].set_xlabel("Cycle")
axs[1].set_ylabel("Fidelity")
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
