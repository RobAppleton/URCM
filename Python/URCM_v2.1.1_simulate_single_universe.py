
import numpy as np
import matplotlib.pyplot as plt

# Parameters (can be customized)
num_subsystems = 100
reset_prob = 0.02
batch_size = 50
entropy_threshold = 1e-3

# Initialize mixed state (max entropy)
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
    return np.array([[1, 0], [0, 0]])  # pure state |0><0|

def run_simulation():
    states = [generate_initial_state() for _ in range(num_subsystems)]
    entropies = []
    t = 0
    bounce_timestep = None

    while True:
        for _ in range(batch_size):
            total_entropy = 0
            for i in range(num_subsystems):
                if np.random.rand() < reset_prob:
                    states[i] = entropy_reset(states[i])
                else:
                    states[i] = unitary_evolve(states[i])
                total_entropy += von_neumann_entropy(states[i])
            entropies.append(total_entropy)
            if total_entropy < entropy_threshold:
                bounce_timestep = t
                print(f"Bounce triggered at timestep {t}")
                break
            t += 1
        if bounce_timestep is not None:
            break

    # Save entropy data
    np.save("entropy_trace.npy", np.array(entropies))

    # Plot
    plt.plot(entropies)
    plt.title("Total System Entropy Over Time")
    plt.xlabel("Timestep")
    plt.ylabel("Entropy (a.u.)")
    plt.grid(True)
    plt.savefig("entropy_bounce_extended.png")
    plt.show()

    return bounce_timestep, entropies

if __name__ == "__main__":
    run_simulation()
