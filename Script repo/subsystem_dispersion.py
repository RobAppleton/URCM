
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg

subsystems = 25
cycles = 20
noise_level = 0.05

def generate_initial_subsystems(subsystems):
    rho_list = []
    for _ in range(subsystems):
        psi = np.random.randn(2) + 1j*np.random.randn(2)
        psi /= np.linalg.norm(psi)
        rho = np.outer(psi, psi.conj())
        rho_list.append(rho)
    return rho_list

def fidelity_simple(rho1, rho2):
    sqrt_rho1 = scipy.linalg.sqrtm(rho1)
    inner = scipy.linalg.sqrtm(sqrt_rho1 @ rho2 @ sqrt_rho1)
    return np.real(np.trace(inner))**2

def noisy_evolve(rho, noise_level):
    noise = noise_level * (np.random.randn(*rho.shape) + 1j*np.random.randn(*rho.shape))
    noise = (noise + noise.conj().T) / 2
    rho += noise
    rho = (rho + rho.conj().T) / 2
    rho /= np.trace(rho)
    return rho

initial_states = generate_initial_subsystems(subsystems)
current_states = [rho.copy() for rho in initial_states]
fidelity_matrix = np.zeros((cycles + 1, subsystems))

for i in range(cycles + 1):
    for j in range(subsystems):
        fidelity_matrix[i, j] = fidelity_simple(initial_states[j], current_states[j])
        current_states[j] = noisy_evolve(current_states[j], noise_level)

plt.figure(figsize=(12, 6))
plt.imshow(fidelity_matrix.T, aspect='auto', cmap='viridis', interpolation='nearest')
plt.colorbar(label="Fidelity")
plt.xlabel("Cycle")
plt.ylabel("Subsystem Index")
plt.title("Subsystem Fidelity Dispersion Over Cycles")
plt.tight_layout()
plt.savefig("subsystem_fidelity_heatmap.png")
