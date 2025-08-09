
import numpy as np
import matplotlib.pyplot as plt

num_subsystems = 25
num_cycles = 20
mu_fidelity_decay = 0.03
sigma_noise = 0.01

fidelities = np.ones((num_subsystems, num_cycles))
for i in range(1, num_cycles):
    noise = np.random.normal(loc=mu_fidelity_decay, scale=sigma_noise, size=num_subsystems)
    fidelities[:, i] = np.clip(fidelities[:, i - 1] - noise, 0, 1)

mean_fidelity = np.mean(fidelities, axis=0)
std_fidelity = np.std(fidelities, axis=0)
cycles = np.arange(1, num_cycles + 1)

plt.figure(figsize=(8, 5))
plt.plot(cycles, mean_fidelity, label="Mean Fidelity", color="green")
plt.fill_between(cycles, mean_fidelity - std_fidelity, mean_fidelity + std_fidelity,
                 color="green", alpha=0.3, label="±1σ Dispersion")
plt.title("Fidelity Dispersion Across 25 Subsystems Over 20 Cycles")
plt.xlabel("Cycle")
plt.ylabel("Fidelity")
plt.grid(True)
plt.legend()
plt.savefig("fidelity_dispersion_25x20.png")
plt.close()
