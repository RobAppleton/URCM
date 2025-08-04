
# ============================================
# URCM Projection Operator Validation Script
# Section 17.3 – Multi-Recursive Hilbert Simulation
# ============================================

# Import core scientific libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigvalsh

# ========================
# PARAMETERS
# ========================
# Simulate 5 parallel universes
# Each universe exists in an 8D Hilbert space
# The recursion process runs for 8 complete cycles
num_universes = 5
dim = 8
recursions = 8

# ========================
# OPERATOR DEFINITIONS
# ========================

# Projection operator: collapses a quantum state into the basis state
# with maximum probability amplitude. This simulates measurement.
def projection_operator(state):
    projected = np.zeros_like(state)
    idx = np.argmax(np.abs(state)**2)
    projected[idx] = 1.0
    return projected

# Decoherence model: adds complex Gaussian noise to simulate entanglement loss
def decohere(state, strength=0.2):
    noise = np.random.normal(0, strength, state.shape) + 1j * np.random.normal(0, strength, state.shape)
    decohered = state + noise
    norm = np.linalg.norm(decohered)
    return decohered / norm if norm != 0 else decohered

# Purity metric: Tr(ρ^2), where ρ is the density matrix of the state
def purity(state):
    rho = np.outer(state, np.conj(state))
    return np.real(np.trace(rho @ rho))

# Participation Ratio: 1 / Σp_i^2, reflects how spread out the state amplitudes are
def participation_ratio(state):
    probs = np.abs(state)**2
    return 1 / np.sum(probs**2)

# ========================
# SIMULATION FUNCTION
# ========================
# Evolves all universes through N recursive cycles with or without projection
def run_simulation(apply_projection=True):
    states = [np.random.rand(dim) + 1j*np.random.rand(dim) for _ in range(num_universes)]
    states = [s / np.linalg.norm(s) for s in states]

    entropy_data, purity_data, pr_data = [], [], []

    for cycle in range(recursions):
        new_states = []

        for state in states:
            state = decohere(state, strength=0.1 + 0.05 * cycle)
            if apply_projection:
                state = projection_operator(state)
            new_states.append(state)

        states = new_states

        entropy_cycle, purity_cycle, pr_cycle = [], [], []
        for state in states:
            probs = np.abs(state)**2
            probs = probs[probs > 0]
            entropy_cycle.append(-np.sum(probs * np.log2(probs)))
            purity_cycle.append(purity(state))
            pr_cycle.append(participation_ratio(state))

        entropy_data.append(entropy_cycle)
        purity_data.append(purity_cycle)
        pr_data.append(pr_cycle)

    return {
        "entropy": np.array(entropy_data),
        "purity": np.array(purity_data),
        "participation_ratio": np.array(pr_data)
    }

# ========================
# MAIN EXECUTION
# ========================
# Run both versions: with and without the projection operator 𝑃̂′
with_proj = run_simulation(apply_projection=True)
without_proj = run_simulation(apply_projection=False)

# ========================
# PLOTTING RESULTS
# ========================
# Generate a multi-metric plot comparing projection and non-projection cases
cycles = np.arange(1, recursions + 1)
plt.figure(figsize=(10, 6))
plt.plot(cycles, np.mean(with_proj["entropy"], axis=1), label="Entropy with 𝑃̂′", marker='o')
plt.plot(cycles, np.mean(without_proj["entropy"], axis=1), label="Entropy without 𝑃̂′", marker='s')
plt.plot(cycles, np.mean(with_proj["purity"], axis=1), label="Purity with 𝑃̂′", linestyle='--', marker='^')
plt.plot(cycles, np.mean(without_proj["purity"], axis=1), label="Purity without 𝑃̂′", linestyle='--', marker='v')
plt.plot(cycles, np.mean(with_proj["participation_ratio"], axis=1), label="Participation Ratio with 𝑃̂′", linestyle=':', marker='x')
plt.plot(cycles, np.mean(without_proj["participation_ratio"], axis=1), label="Participation Ratio without 𝑃̂′", linestyle=':', marker='d')
plt.xlabel("Recursion Cycle")
plt.ylabel("Metric Value")
plt.title("URCM Recursive Projection Operator Validation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("urcm_17_3_metrics_output.png", dpi=300)
plt.close()
