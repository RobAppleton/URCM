
# URCM Bounce Operator Simulation – Section 17.3
# Simulates recursive cosmological cycles with and without 𝐵̂′

import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_universes = 5
dim = 8
recursions = 10

# Metrics
def entropy(state):
    probs = np.abs(state)**2
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

def participation_ratio(state):
    probs = np.abs(state)**2
    return 1.0 / np.sum(probs**2)

def purity(state):
    rho = np.outer(state, np.conj(state))
    return np.real(np.trace(rho @ rho))

# Operators
def decohere(state, strength):
    noise = np.random.normal(0, strength, state.shape) + 1j*np.random.normal(0, strength, state.shape)
    new_state = state + noise
    return new_state / np.linalg.norm(new_state)

def bounce_operator(state):
    # Collapse to low-entropy basis state (simulated re-expansion)
    idx = np.argmax(np.abs(state)**2)
    reset = np.zeros_like(state)
    reset[idx] = 1.0
    return reset

# Run simulation
def run_simulation(apply_bounce=True):
    states = [np.random.rand(dim) + 1j*np.random.rand(dim) for _ in range(num_universes)]
    states = [s / np.linalg.norm(s) for s in states]

    entropy_record, purity_record, pr_record = [], [], []

    for cycle in range(recursions):
        new_states = []
        for state in states:
            strength = 0.1 + 0.05 * cycle
            state = decohere(state, strength)

            # Apply bounce operator at entropy minima (simulate threshold)
            if apply_bounce and entropy(state) < 2.0:
                state = bounce_operator(state)

            new_states.append(state)

        states = new_states
        entropy_record.append(np.mean([entropy(s) for s in states]))
        purity_record.append(np.mean([purity(s) for s in states]))
        pr_record.append(np.mean([participation_ratio(s) for s in states]))

    return entropy_record, purity_record, pr_record

# Run both bounce-enabled and control simulations
entropy_with_b, purity_with_b, pr_with_b = run_simulation(apply_bounce=True)
entropy_no_b, purity_no_b, pr_no_b = run_simulation(apply_bounce=False)

# Plot results
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
