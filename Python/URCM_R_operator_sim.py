
# URCM Recursive Evolution Operator Simulation
# Validating R̂′ = B̂′ ∘ T̂ᵐ′ ∘ Ĉ_fix across 10 recursion cycles

import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_universes = 5
dim = 10
recursions = 10

def bounce_operator(state):
    # Simulated bounce at entropy minima - rescale state to start anew
    idx = np.argmax(np.abs(state)**2)
    reset = np.zeros_like(state)
    reset[idx] = 1.0
    return reset

def temporal_modulation(state, cycle):
    # Apply entropy slope logic through noise scaled by cycle depth
    noise_strength = 0.05 + 0.02 * cycle
    noise = np.random.normal(0, noise_strength, state.shape) + 1j * np.random.normal(0, noise_strength, state.shape)
    modulated = state + noise
    norm = np.linalg.norm(modulated)
    return modulated / norm if norm != 0 else modulated

def fix_operator(state):
    # Normalize state to preserve trace = 1
    return state / np.linalg.norm(state)

def recursive_R_operator(state, cycle):
    state = fix_operator(state)
    state = temporal_modulation(state, cycle)
    state = bounce_operator(state)
    return state

def participation_ratio(state):
    probs = np.abs(state)**2
    return 1 / np.sum(probs**2)

def entropy(state):
    probs = np.abs(state)**2
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

def run_simulation(use_recursive_operator=True):
    states = [np.random.rand(dim) + 1j*np.random.rand(dim) for _ in range(num_universes)]
    states = [s / np.linalg.norm(s) for s in states]

    entropies = []
    prs = []

    for cycle in range(recursions):
        new_states = []
        for state in states:
            if use_recursive_operator:
                updated = recursive_R_operator(state, cycle)
            else:
                updated = temporal_modulation(state, cycle)  # No bounce/fix logic
            new_states.append(updated)

        states = new_states
        entropies.append(np.mean([entropy(s) for s in states]))
        prs.append(np.mean([participation_ratio(s) for s in states]))

    return entropies, prs

# Run both simulations
with_R, pr_with_R = run_simulation(use_recursive_operator=True)
without_R, pr_without_R = run_simulation(use_recursive_operator=False)

# Plot results
cycles = np.arange(1, recursions + 1)
plt.figure(figsize=(10, 6))
plt.plot(cycles, with_R, label='Entropy with R̂′', marker='o')
plt.plot(cycles, without_R, label='Entropy without R̂′', marker='s')
plt.plot(cycles, pr_with_R, label='Participation Ratio with R̂′', linestyle='--', marker='x')
plt.plot(cycles, pr_without_R, label='Participation Ratio without R̂′', linestyle='--', marker='d')
plt.xlabel('Recursion Cycle')
plt.ylabel('Metric Value')
plt.title('Recursive Operator Simulation: Entropy and Participation Ratio')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("urcm_R_operator_sim_output.png", dpi=300)
