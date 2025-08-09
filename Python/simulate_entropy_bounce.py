
import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_subsystems = 100
timesteps = 200
entropy_threshold = 1e-3

# Initialize pure states with zero entropy
def generate_initial_state():
    return np.eye(2) / 2  # maximally mixed state for simplicity

def von_neumann_entropy(rho):
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 0]
    return -np.sum(eigvals * np.log(eigvals))

def unitary_evolve(rho):
    theta = np.random.rand() * 2 * np.pi
    U = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    return U @ rho @ U.T.conj()

def entropy_reset(rho):
    return np.array([[1, 0], [0, 0]])  # pure state |0><0|

# Simulate
states = [generate_initial_state() for _ in range(num_subsystems)]
entropies = []

for t in range(timesteps):
    total_entropy = 0
    for i in range(num_subsystems):
        if np.random.rand() < 0.02:  # simulate absorption by black hole
            states[i] = entropy_reset(states[i])
        else:
            states[i] = unitary_evolve(states[i])
        total_entropy += von_neumann_entropy(states[i])
    entropies.append(total_entropy)
    if total_entropy < entropy_threshold:
        print(f"Bounce triggered at timestep {t}")
        break

# Plot entropy over time
plt.plot(entropies)
plt.title("Total System Entropy Over Time")
plt.xlabel("Timestep")
plt.ylabel("Entropy (a.u.)")
plt.grid(True)
plt.savefig("/mnt/data/entropy_bounce_simulation.png")
plt.show()
