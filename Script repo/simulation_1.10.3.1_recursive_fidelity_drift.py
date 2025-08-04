"""
Simulation: simulation_1.10.3.1_recursive_fidelity_drift.py
Description: Combines prior simulations to explore the relationship between fidelity decay, entropy reset, and recursive dynamics in URCM.
"""

import numpy as np
import matplotlib.pyplot as plt
from appleton_v2_5_2_page_curve_simulation import simulate_page_curve
from appleton_v2_4_1_entanglement_noise_model import generate_entanglement_noise_profile
from appleton_v2_4_1_calibration_noise_study import generate_calibration_drift
from appleton_v2_4_1_simulate_50_universes_safe import simulate_ensemble

# Simulation parameters
num_cycles = 20
num_universes = 50

# Generate noise models
ent_noise = generate_entanglement_noise_profile(num_cycles)
cal_drift = generate_calibration_drift(num_cycles)

# Generate ensemble of universes
universes = simulate_ensemble(num_universes=num_universes, num_cycles=num_cycles)

# Run Page curve simulation
page_curve_data = simulate_page_curve(num_cycles=num_cycles)

# Composite metrics calculation
composite_fidelity = np.mean([u["fidelity"] for u in universes], axis=0)
composite_entropy = page_curve_data["entropy"]
stabilization_point = np.argmax(np.gradient(composite_entropy) < 0.01)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(composite_fidelity, label="Avg Fidelity (across universes)")
plt.plot(composite_entropy, label="Avg Entropy (Page curve)")
plt.axvline(stabilization_point, color='r', linestyle='--', label="Stabilization Point")
plt.xlabel("Cycle")
plt.ylabel("Metric Value")
plt.title("Recursive Fidelity Drift and Entropy Stabilization")
plt.legend()
plt.tight_layout()
output_path = "/mnt/data/simulation_1.10.3.1_recursive_fidelity_drift.png"
plt.savefig(output_path)
plt.close()

output_path
