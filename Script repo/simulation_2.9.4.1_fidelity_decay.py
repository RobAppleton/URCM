
import numpy as np
import matplotlib.pyplot as plt

def simulate_recursive_decay(num_cycles=30, initial_fidelity=1.0, decay_c=0.05, scatter_prob=0.1):
    fidelities = [initial_fidelity]
    current_fidelity = initial_fidelity

    for i in range(num_cycles):
        # Apply collapse (entropy increase)
        current_fidelity *= (1 - decay_c)

        # Apply scatter (random stochastic hit)
        if np.random.rand() < scatter_prob:
            current_fidelity *= np.random.uniform(0.8, 1.0)  # simulate stochastic fidelity disruption

        # Clip to 0
        current_fidelity = max(current_fidelity, 0)
        fidelities.append(current_fidelity)

    return fidelities

# Run and plot the simulation
fidelities = simulate_recursive_decay()
cycles = list(range(len(fidelities)))

plt.figure()
plt.plot(cycles, fidelities, marker='o')
plt.title("Recursive Operator Chain Fidelity Decay (Emergent Irreversibility)")
plt.xlabel("Recursion Cycle")
plt.ylabel("Subsystem Fidelity")
plt.grid(True)
plt.savefig("fidelity_decay_recursive_simulation.png")
plt.show()
