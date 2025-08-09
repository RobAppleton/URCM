import numpy as np
import matplotlib.pyplot as plt

timesteps = 150
noise_levels = [0.01, 0.03, 0.05, 0.1, 0.2]
dim = 4

def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

def fidelity_approx(rho1, rho2):
    return np.real(np.trace(rho1 @ rho2))

# Reference state: |00><00|
ref_state = np.zeros((dim, dim))
ref_state[0, 0] = 1.0

results = {}

for gamma in noise_levels:
    rho = np.eye(dim) / dim
    fidelities = []
    entropies = []

    for t in range(timesteps):
        noise = gamma * np.random.randn(dim, dim)
        noise = (noise + noise.T) / 2
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)

        fidelities.append(fidelity_approx(ref_state, rho))
        entropies.append(entropy(rho))

    results[gamma] = {'fidelity': fidelities, 'entropy': entropies}

# Plot
plt.figure(figsize=(12, 5))

for gamma in noise_levels:
    plt.plot(results[gamma]['fidelity'], label=f'γ={gamma}')

plt.title("Fidelity Decay under Varying Decoherence Rates")
plt.xlabel("Timestep")
plt.ylabel("Fidelity")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/calibration_fidelity_plot.png")

plt.figure(figsize=(12, 5))

for gamma in noise_levels:
    plt.plot(results[gamma]['entropy'], label=f'γ={gamma}')

plt.title("Entropy Growth under Varying Decoherence Rates")
plt.xlabel("Timestep")
plt.ylabel("Entropy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/calibration_entropy_plot.png")