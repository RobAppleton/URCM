
# URCM Projection Operator Validation Script
# Section 17.2 – Testing 𝑃̂′ with entropy collapse and decoherence tracking

import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_universes = 5
dim = 8
recursions = 8

# Projection operator (𝑃̂′): collapses to max amplitude state
def projection_operator(state):
    idx = np.argmax(np.abs(state)**2)
    projected = np.zeros_like(state)
    projected[idx] = 1.0
    return projected

# Decoherence model: Gaussian noise scaled by recursion cycle
def decohere(state, strength):
    noise = np.random.normal(0, strength, state.shape) + 1j * np.random.normal(0, strength, state.shape)
    result = state + noise
    norm = np.linalg.norm(result)
    return result / norm if norm != 0 else result

# Metric: Entropy
def entropy(state):
    probs = np.abs(state)**2
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

# Metric: Participation Ratio
def participation_ratio(state):
    probs = np.abs(state)**2
    return 1.0 / np.sum(probs**2)

# Metric: Purity (Tr(ρ²) for pure state vector)
def purity(state):
    rho = np.outer(state, np.conj(state))
    return np.real(np.trace(rho @ rho))

# Run simulation
def run_simulation(use_projection=True):
    states = [np.random.rand(dim) + 1j * np.random.rand(dim) for _ in range(num_universes)]
    states = [s / np.linalg.norm(s) for s in states]
    entropies, purities, prs = [], [], []

    for cycle in range(recursions):
        new_states = []
        for state in states:
            strength = 0.1 + 0.05 * cycle
            state = decohere(state, strength)
            if use_projection:
                state = projection_operator(state)
            new_states.append(state)

        states = new_states
        entropies.append(np.mean([entropy(s) for s in states]))
        purities.append(np.mean([purity(s) for s in states]))
        prs.append(np.mean([participation_ratio(s) for s in states]))

    return entropies, purities, prs

# Run both versions
ent_p, pur_p, pr_p = run_simulation(use_projection=True)
ent_np, pur_np, pr_np = run_simulation(use_projection=False)

# Plotting
cycles = np.arange(1, recursions + 1)
plt.figure(figsize=(10, 6))
plt.plot(cycles, ent_p, label='Entropy with 𝑃̂′', marker='o')
plt.plot(cycles, ent_np, label='Entropy without 𝑃̂′', marker='s')
plt.plot(cycles, pur_p, label='Purity with 𝑃̂′', linestyle='--', marker='^')
plt.plot(cycles, pur_np, label='Purity without 𝑃̂′', linestyle='--', marker='v')
plt.plot(cycles, pr_p, label='Participation Ratio with 𝑃̂′', linestyle=':', marker='x')
plt.plot(cycles, pr_np, label='Participation Ratio without 𝑃̂′', linestyle=':', marker='d')
plt.xlabel('Recursion Cycle')
plt.ylabel('Metric Value')
plt.title('Projection Operator Simulation: Entropy, Purity, Participation Ratio')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('urcm_projection_operator_sim_output.png', dpi=300)
