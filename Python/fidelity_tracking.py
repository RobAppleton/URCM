
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg

# Parameters
cycles = 20
d = 4

def generate_initial_state(d):
    psi_list = [np.random.randn(d) + 1j*np.random.randn(d) for _ in range(5)]
    psi_list = [psi / np.linalg.norm(psi) for psi in psi_list]
    rho = sum(np.outer(psi, psi.conj()) for psi in psi_list) / len(psi_list)
    return rho / np.trace(rho)

def fidelity(rho1, rho2):
    sqrt_rho1 = scipy.linalg.sqrtm(rho1)
    inner = scipy.linalg.sqrtm(sqrt_rho1 @ rho2 @ sqrt_rho1)
    return np.real(np.trace(inner))**2

def apply_random_noise(rho, noise_level=0.05):
    noise = noise_level * (np.random.randn(*rho.shape) + 1j*np.random.randn(*rho.shape))
    noise = (noise + noise.conj().T) / 2
    rho += noise
    rho = (rho + rho.conj().T) / 2
    rho /= np.trace(rho)
    return rho

rho0 = generate_initial_state(d)
rho = rho0.copy()
fidelities = [1.0]

for i in range(1, cycles + 1):
    rho = apply_random_noise(rho)
    fidelities.append(fidelity(rho0, rho))

plt.figure(figsize=(10, 5))
plt.plot(fidelities, marker='o')
plt.xlabel("Cycle")
plt.ylabel("Fidelity to Initial State")
plt.title("Fidelity Decay Across Recursive Cycles")
plt.grid(True)
plt.tight_layout()
plt.savefig("fidelity_decay_simulation.png")
