
import numpy as np
import matplotlib.pyplot as plt

total_qubits = 100
subsystem_sizes = np.arange(1, 51)
noise_level = 0.05

def simulate_entropy(n, total_qubits, noise_level):
    S_max = np.log2(n)
    base_entropy = S_max * (1 - np.exp(-n / total_qubits))
    noise = noise_level * np.random.randn()
    return max(0, base_entropy + noise)

entropies = [simulate_entropy(n, total_qubits, noise_level) for n in subsystem_sizes]

plt.figure(figsize=(10, 5))
plt.plot(subsystem_sizes, entropies, marker='o')
plt.xlabel("Subsystem Size (n)")
plt.ylabel("Entropy S(n)")
plt.title("Noisy Page Curve Approximation (v2.2.2)")
plt.grid(True)
plt.tight_layout()
plt.savefig("page_curve_noisy_simulation_v2.2.2.png")
