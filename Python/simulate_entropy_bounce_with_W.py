
import numpy as np
import matplotlib.pyplot as plt

num_subsystems = 100
timesteps = 200
entropy_threshold = 1e-3
w_strength = 0.05  # strength of speculative W influence

def generate_initial_state():
    return np.eye(2) / 2

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
    return np.array([[1, 0], [0, 0]])

def apply_W_operator(rho, avg_state):
    return 0.95 * rho + 0.05 * avg_state

states = [generate_initial_state() for _ in range(num_subsystems)]
entropies = []

for t in range(timesteps):
    total_entropy = 0
    avg_state = sum(states) / num_subsystems
    for i in range(num_subsystems):
        if np.random.rand() < 0.02:
            states[i] = entropy_reset(states[i])
        else:
            states[i] = unitary_evolve(states[i])
            if np.random.rand() < w_strength:
                states[i] = apply_W_operator(states[i], avg_state)
        total_entropy += von_neumann_entropy(states[i])
    entropies.append(total_entropy)
    if total_entropy < entropy_threshold:
        print(f"Bounce triggered at timestep {t}")
        break

plt.plot(entropies, label="Total Entropy with $W$")
plt.axhline(entropy_threshold, color='red', linestyle='--', label="Threshold")
plt.title("Speculative Simulation: Entropy Collapse with Operator $W$")
plt.xlabel("Timestep")
plt.ylabel("Entropy (a.u.)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("entropy_bounce_simulation_W.png")
plt.show()
