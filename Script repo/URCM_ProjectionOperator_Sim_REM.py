
# =============================================
# URCM Projection Operator Simulation – 𝑃̂′
# Validating entropy collapse and observational emergence
# =============================================

import numpy as np
import matplotlib.pyplot as plt

# ========================
# PARAMETERS
# ========================
# Number of simulated universes
num_universes = 5
# Dimension of each universe's Hilbert space
dim = 8
# Number of recursion cycles to simulate
recursions = 8

# ========================
# OPERATOR DEFINITIONS
# ========================

# Projection Operator (𝑃̂′)
# Collapses quantum state to its most probable basis vector
def projection_operator(state):
    idx = np.argmax(np.abs(state)**2)
    projected = np.zeros_like(state)
    projected[idx] = 1.0
    return projected

# Decoherence Model
# Adds noise proportional to entropy slope to simulate loss of coherence
def decohere(state, strength):
    noise = np.random.normal(0, strength, state.shape) + 1j * np.random.normal(0, strength, state.shape)
    result = state + noise
    norm = np.linalg.norm(result)
    return result / norm if norm != 0 else result

# Entropy Metric
# Computes Shannon entropy of the quantum state's probability distribution
def entropy(state):
    probs = np.abs(state)**2
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

# Participation Ratio Metric
# Measures the effective spread of probability across basis states
def participation_ratio(state):
    probs = np.abs(state)**2
    return 1.0 / np.sum(probs**2)

# Purity Metric
# Computes Tr(ρ²) where ρ = |ψ⟩⟨ψ|, should be 1 for pure states
def purity(state):
    rho = np.outer(state, np.conj(state))
    return np.real(np.trace(rho @ rho))

# ========================
# SIMULATION FUNCTION
# ========================
# Evolves the system with or without projection across all recursion cycles
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

# ========================
# RUN BOTH SCENARIOS
# ========================
# Projection-enabled simulation
ent_p, pur_p, pr_p = run_simulation(use_projection=True)
# Control run with decoherence only
ent_np, pur_np, pr_np = run_simulation(use_projection=False)

# ========================
# PLOTTING RESULTS
# ========================
# Plot entropy, purity, and participation ratio for both cases
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
