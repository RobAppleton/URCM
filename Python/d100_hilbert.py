
import numpy as np
import matplotlib.pyplot as plt
from qutip import *

# Parameters
d = 100
cycles = 5
noise_levels = [0.0, 0.01, 0.05, 0.1]
initial_state = basis(d, 0)

# Define unitary operator: a shift with phase
theta = 2 * np.pi / d
U = sum([basis(d, (i + 1) % d) * basis(d, i).dag() * np.exp(1j * theta) for i in range(d)]).unit()

# Depolarizing noise function
def depolarize(rho, level):
    return (1 - level) * rho + level * (qeye(d) / d)

# Simulation
results = {}
for noise in noise_levels:
    state = initial_state.proj()
    entropies = []
    for _ in range(cycles):
        state = U * state * U.dag()
        state = depolarize(state, noise)
        entropies.append(entropy_vn(state))
    results[noise] = entropies

# Plot
for noise, trace in results.items():
    plt.plot(range(1, cycles + 1), trace, label=f"Noise {noise}")
plt.xlabel("Cycle")
plt.ylabel("Von Neumann Entropy")
plt.title("Entropy over Cycles with Varying Noise")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
