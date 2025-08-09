
# =====================================================
# URCM Bounce Operator Simulation Script – Section 17.3
# Validates the role of 𝐵̂′ in recursion stability
# =====================================================

import numpy as np
import matplotlib.pyplot as plt

# ========================
# PARAMETERS
# ========================
# Number of simulated universes
num_universes = 5
# Dimension of Hilbert space per universe
dim = 8
# Number of recursive cycles to simulate
recursions = 10

# ========================
# METRIC DEFINITIONS
# ========================

# Entropy: quantifies randomness in the state
def entropy(state):
    probs = np.abs(state)**2
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

# Participation Ratio: 1 / Σpᵢ², indicates state spread
def participation_ratio(state):
    probs = np.abs(state)**2
    return 1.0 / np.sum(probs**2)

# Purity: Tr(ρ²), checks closeness to pure eigenstates
def purity(state):
    rho = np.outer(state, np.conj(state))
    return np.real(np.trace(rho @ rho))

# ========================
# OPERATOR DEFINITIONS
# ========================

# Decoherence Model
# Adds Gaussian noise scaled by cycle depth
def decohere(state, strength):
    noise = np.random.normal(0, strength, state.shape) + 1j*np.random.normal(0, strength, state.shape)
    new_state = state + noise
    return new_state / np.linalg.norm(new_state)

# Bounce Operator 𝐵̂′
# Resets the system at entropy minima to a basis-dominant low-entropy state
def bounce_operator(state):
    idx = np.argmax(np.abs(state)**2)
    reset = np.zeros_like(state)
    reset[idx] = 1.0
    return reset

# ========================
# SIMULATION FUNCTION
# ========================
# Evolves system with or without bounce operator 𝐵̂′
def run_simulation(apply_bounce=True):
    states = [np.random.rand(dim) + 1j*np.random.rand(dim) for _ in range(num_universes)]
    states = [s / np.linalg.norm(s) for s in states]

    entropy_record, purity_record, pr_record = [], [], []

    for cycle in range(recursions):
        new_states = []
        for state in states:
            strength = 0.1 + 0.05 * cycle
            state = decohere(state, strength)

            # Apply bounce at entropy minima
            if apply_bounce and entropy(state) < 2.0:
                state = bounce_operator(state)

            new_states.append(state)

        states = new_states
        entropy_record.append(np.mean([entropy(s) for s in states]))
        purity_record.append(np.mean([purity(s) for s in states]))
        pr_record.append(np.mean([participation_ratio(s) for s in states]))

    return entropy_record, purity_record, pr_record

# ========================
# EXECUTE SIMULATIONS
# ========================
# With bounce enabled
entropy_with_b, purity_with_b, pr_with_b = run_simulation(apply_bounce=True)
# Control: bounce disabled
entropy_no_b, purity_no_b, pr_no_b = run_simulation(apply_bounce=False)

# ========================
# PLOTTING RESULTS
# ========================
cycles = np.arange(1, recursions + 1)
plt.figure(figsize=(10, 6))
plt.plot(cycles, entropy_with_b, label='Entropy with 𝐵̂′', marker='o')
plt.plot(cycles, entropy_no_b, label='Entropy without 𝐵̂′', marker='s')
plt.plot(cycles, purity_with_b, label='Purity with 𝐵̂′', linestyle='--', marker='^')
plt.plot(cycles, purity_no_b, label='Purity without 𝐵̂′', linestyle='--', marker='v')
plt.plot(cycles, pr_with_b, label='Participation Ratio with 𝐵̂′', linestyle=':', marker='x')
plt.plot(cycles, pr_no_b, label='Participation Ratio without 𝐵̂′', linestyle=':', marker='d')
plt.xlabel('Recursion Cycle')
plt.ylabel('Metric Value')
plt.title('Bounce Operator Simulation: Entropy, Purity, Participation Ratio')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('urcm_bounce_operator_sim_output.png', dpi=300)
