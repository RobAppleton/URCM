
import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_universes = 500
num_subsystems = 100
reset_prob = 0.02
batch_size = 50
entropy_threshold = 1e-3
max_timesteps = 5000  # fail-safe limit

def generate_initial_state():
    return np.eye(2) / 2  # maximally mixed state

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

def run_universe():
    states = [generate_initial_state() for _ in range(num_subsystems)]
    entropies = []
    t = 0

    while t < max_timesteps:
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
                return entropies, t
            t += 1
    return entropies, None  # did not bounce

# Run simulation for all universes
all_entropies = []
bounce_times = []

print("Running 500 universe simulations...")
for u in range(num_universes):
    entropy_trace, bounce = run_universe()
    all_entropies.append(entropy_trace)
    if bounce is not None:
        bounce_times.append(bounce)
    print(f"Universe {u+1}/{num_universes} complete (Bounce: {bounce})", end="\r")

# Plot overlaid entropy curves
plt.figure(figsize=(10, 6))
for trace in all_entropies:
    plt.plot(trace, alpha=0.05, color='blue')
plt.title("Entropy Curves Across 500 Simulated Universes")
plt.xlabel("Timestep")
plt.ylabel("Entropy (a.u.)")
plt.grid(True)
plt.savefig("overlay_entropy_500_universes.png")
plt.show()

# Plot bounce time histogram
plt.figure(figsize=(10, 4))
plt.hist(bounce_times, bins=50, color='green', edgecolor='black')
plt.title("Histogram of Bounce Times Across 500 Universes")
plt.xlabel("Bounce Timestep")
plt.ylabel("Frequency")
plt.grid(True)
plt.savefig("bounce_histogram_500_universes.png")
plt.show()

# Save results
np.save("all_entropy_traces_500.npy", np.array(all_entropies, dtype=object))
np.save("bounce_times_500.npy", np.array(bounce_times))
