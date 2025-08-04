
# ====================================================
# URCM Temporal Operator Simulation – Section 17.4
# Validates entropy modulation and the emergence of time's arrow
# ====================================================

import numpy as np
import matplotlib.pyplot as plt

# ========================
# PARAMETERS
# ========================
# Number of universes
num_universes = 5
# Dimension of each Hilbert space
dim = 8
# Number of recursion cycles
recursions = 10

# ========================
# METRIC DEFINITIONS
# ========================

# Entropy: Shannon entropy of state's probability distribution
def entropy(state):
    probs = np.abs(state)**2
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

# Entropy Slope: Change in entropy over cycles (ΔS)
def entropy_slope(entropy_series):
    return np.gradient(entropy_series)

# Participation Ratio: Inverse of probability concentration
def participation_ratio(state):
    probs = np.abs(state)**2
    return 1.0 / np.sum(probs**2)

# Purity: Tr(ρ²) for a pure state vector
def purity(state):
    rho = np.outer(state, np.conj(state))
    return np.real(np.trace(rho @ rho))

# ========================
# TEMPORAL MODULATION
# ========================

# Simulated effect of 𝑇̂ᵐ′: Adds decoherence noise growing with cycle index
def apply_temporal_modulation(state, cycle):
    strength = 0.05 + 0.05 * cycle
    noise = np.random.normal(0, strength, state.shape) + 1j*np.random.normal(0, strength, state.shape)
    modulated = state + noise
    return modulated / np.linalg.norm(modulated)

# ========================
# SIMULATION FUNCTION
# ========================
# Evolves systems with or without temporal modulation operator 𝑇̂ᵐ′
def run_temporal_simulation(use_temporal_operator=True):
    states = [np.random.rand(dim) + 1j*np.random.rand(dim) for _ in range(num_universes)]
    states = [s / np.linalg.norm(s) for s in states]

    entropy_values, purity_values, pr_values = [], [], []

    for cycle in range(recursions):
        new_states = []
        for state in states:
            if use_temporal_operator:
                state = apply_temporal_modulation(state, cycle)
            new_states.append(state)

        states = new_states
        entropy_values.append(np.mean([entropy(s) for s in states]))
        purity_values.append(np.mean([purity(s) for s in states]))
        pr_values.append(np.mean([participation_ratio(s) for s in states]))

    return np.array(entropy_values), np.array(purity_values), np.array(pr_values), entropy_slope(entropy_values)

# ========================
# RUN SIMULATIONS
# ========================
e_t, p_t, pr_t, slope_t = run_temporal_simulation(True)   # with 𝑇̂ᵐ′
e_nt, p_nt, pr_nt, slope_nt = run_temporal_simulation(False)  # without 𝑇̂ᵐ′

# ========================
# PLOTTING RESULTS
# ========================
cycles = np.arange(1, recursions + 1)
plt.figure(figsize=(10, 6))
plt.plot(cycles, e_t, label='Entropy with 𝑇̂ᵐ′', marker='o')
plt.plot(cycles, e_nt, label='Entropy without 𝑇̂ᵐ′', marker='s')
plt.plot(cycles, slope_t, label='Entropy Slope with 𝑇̂ᵐ′', linestyle='--', marker='^')
plt.plot(cycles, slope_nt, label='Entropy Slope without 𝑇̂ᵐ′', linestyle='--', marker='v')
plt.xlabel('Recursion Cycle')
plt.ylabel('Metric Value')
plt.title('Temporal Operator Simulation: Entropy and Slope')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('urcm_temporal_operator_sim_output.png', dpi=300)
