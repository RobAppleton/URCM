
import numpy as np
import matplotlib.pyplot as plt
import os

# Parameters
num_universes = 50
num_subsystems = 100
reset_prob = 0.02
batch_size = 50
entropy_threshold = 1e-3
max_timesteps = 5000  # fail-safe limit

def generate_initial_state():
    return np.eye(2) / 2  # maximally mixed state

def von_neumann_entropy(rho):
    try:
        eigvals = np.linalg.eigvalsh(rho)
        eigvals = eigvals[eigvals > 0]  # avoid log(0)
        return -np.sum(eigvals * np.log(eigvals))
    except Exception as e:
        print("Error in entropy calculation:", e)
        return np.nan

def unitary_evolve(rho):
    try:
        theta = np.random.rand() * 2 * np.pi
        U = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
        return U @ rho @ U.T.conj()
    except Exception as e:
        print("Error in unitary evolution:", e)
        return rho

def entropy_reset(rho):
    return np.array([[1, 0], [0, 0]])

def run_universe():
    try:
        states = [generate_initial_state() for _ in range(num_subsystems)]
        entropies = []
        t = 0

        while t < max_timesteps:
            for _ in range(batch_size):
                total_entropy = 0
                for i in range(num_subsystems):
                    try:
                        if np.random.rand() < reset_prob:
                            states[i] = entropy_reset(states[i])
                        else:
                            states[i] = unitary_evolve(states[i])
                        ent = von_neumann_entropy(states[i])
                        if not np.isnan(ent):
                            total_entropy += ent
                    except Exception as inner_e:
                        print(f"Subsystem {i} update failed at timestep {t}: {inner_e}")
                entropies.append(total_entropy)
                if total_entropy < entropy_threshold:
                    return entropies, t
                t += 1
        print("Bounce not reached within max_timesteps.")
        return entropies, None
    except Exception as e:
        print("Simulation failure:", e)
        return [], None

def safe_save(filename, data):
    try:
        np.save(filename, data)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Failed to save {filename}: {e}")

def safe_plot(plot_func, filename):
    try:
        plot_func()
        plt.savefig(filename)
        print(f"Saved plot: {filename}")
        plt.close()
    except Exception as e:
        print(f"Plot failed for {filename}: {e}")

# Main simulation
if __name__ == "__main__":
    all_entropies = []
    bounce_times = []

    for u in range(num_universes):
        entropy_trace, bounce = run_universe()
        all_entropies.append(entropy_trace)
        if bounce is not None:
            bounce_times.append(bounce)
        print(f"Universe {u+1}/{num_universes} complete. Bounce: {bounce}")

    def plot_entropy_overlay():
        for trace in all_entropies:
            plt.plot(trace, alpha=0.1, color='blue')
        plt.title("Entropy Curves Across 50 Simulated Universes")
        plt.xlabel("Timestep")
        plt.ylabel("Entropy (a.u.)")
        plt.grid(True)

    def plot_histogram():
        plt.hist(bounce_times, bins=30, color='green', edgecolor='black')
        plt.title("Histogram of Bounce Times Across 50 Universes")
        plt.xlabel("Bounce Timestep")
        plt.ylabel("Frequency")
        plt.grid(True)

    safe_plot(plot_entropy_overlay, "overlay_entropy_50_universes_safe.png")
    safe_plot(plot_histogram, "bounce_histogram_50_universes_safe.png")
    safe_save("all_entropy_traces_50_safe.npy", np.array(all_entropies, dtype=object))
    safe_save("bounce_times_50_safe.npy", np.array(bounce_times))
