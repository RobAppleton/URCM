
import numpy as np
import matplotlib.pyplot as plt

def simulate_recursive_stabilization(num_cycles=50, scatter_prob=0.2, bounce_interval=5):
    fidelity_A = [1.0]
    fidelity_B = [1.0]

    for cycle in range(1, num_cycles + 1):
        # Case A: scatter only
        f_A = fidelity_A[-1]
        if np.random.rand() < scatter_prob:
            f_A *= np.random.uniform(0.85, 0.95)
        fidelity_A.append(max(f_A, 0))

        # Case B: scatter + bounce
        f_B = fidelity_B[-1]
        if np.random.rand() < scatter_prob:
            f_B *= np.random.uniform(0.85, 0.95)

        if cycle % bounce_interval == 0:
            f_B *= 1.05  # Bounce: coherence restoration

        f_B = min(f_B, 1.0)
        fidelity_B.append(f_B)

    return fidelity_A, fidelity_B

# Run and plot
fidelity_scatter_only, fidelity_with_bounce = simulate_recursive_stabilization()
cycles = list(range(len(fidelity_scatter_only)))

plt.figure()
plt.plot(cycles, fidelity_scatter_only, label="Scatter Only", linestyle='--', marker='x')
plt.plot(cycles, fidelity_with_bounce, label="Scatter + Bounce Every 5 Cycles", linestyle='-', marker='o')
plt.title("Recursive Stabilization of Noisy Subsystems")
plt.xlabel("Cycle")
plt.ylabel("Fidelity")
plt.legend()
plt.grid(True)
plt.savefig("recursive_stabilization_fidelity_comparison.png")
plt.show()
