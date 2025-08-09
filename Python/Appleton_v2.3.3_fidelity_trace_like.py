
import numpy as np
import matplotlib.pyplot as plt

num_subsystems = 25
num_cycles = 20
mu_drift = 0.03
sigma_drift = 0.01

trace_like_fidelity = np.ones((num_subsystems, num_cycles))
for i in range(1, num_cycles):
    drift = np.random.normal(loc=mu_drift, scale=sigma_drift, size=num_subsystems)
    trace_like_fidelity[:, i] = np.clip(trace_like_fidelity[:, i - 1] - drift, 0, 1)

mean_trace = np.mean(trace_like_fidelity, axis=0)
std_trace = np.std(trace_like_fidelity, axis=0)
cycles = np.arange(1, num_cycles + 1)

plt.figure(figsize=(8, 5))
plt.plot(cycles, mean_trace, label="Mean Trace-like Similarity", color="purple")
plt.fill_between(cycles, mean_trace - std_trace, mean_trace + std_trace,
                 color="purple", alpha=0.3, label="±1σ Dispersion")
plt.title("Alternative Fidelity Metric (Trace-like) – 25 Subsystems")
plt.xlabel("Cycle")
plt.ylabel("Similarity Score")
plt.grid(True)
plt.legend()
plt.savefig("fidelity_dispersion_trace_like_25x20.png")
plt.close()
