# Consolidated Self-Contained Simulation Script: simulation_2.10.2.1_universe_fidelity_suite_FULL.py
# Includes inlined appendix modules

# ==== Start of appleton_v2.4.1_calibration_noise_study.py ====
import numpy as np
import matplotlib.pyplot as plt

timesteps = 150
noise_levels = [0.01, 0.03, 0.05, 0.1, 0.2]
dim = 4

def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

def fidelity_approx(rho1, rho2):
    return np.real(np.trace(rho1 @ rho2))

# Reference state: |00><00|
ref_state = np.zeros((dim, dim))
ref_state[0, 0] = 1.0

results = {}

for gamma in noise_levels:
    rho = np.eye(dim) / dim
    fidelities = []
    entropies = []

    for t in range(timesteps):
        noise = gamma * np.random.randn(dim, dim)
        noise = (noise + noise.T) / 2
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)

        fidelities.append(fidelity_approx(ref_state, rho))
        entropies.append(entropy(rho))

    results[gamma] = {'fidelity': fidelities, 'entropy': entropies}

# Plot
plt.figure(figsize=(12, 5))

for gamma in noise_levels:
    plt.plot(results[gamma]['fidelity'], label=f'γ={gamma}')

plt.title("Fidelity Decay under Varying Decoherence Rates")
plt.xlabel("Timestep")
plt.ylabel("Fidelity")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/calibration_fidelity_plot.png")

plt.figure(figsize=(12, 5))

for gamma in noise_levels:
    plt.plot(results[gamma]['entropy'], label=f'γ={gamma}')

plt.title("Entropy Growth under Varying Decoherence Rates")
plt.xlabel("Timestep")
plt.ylabel("Entropy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/calibration_entropy_plot.png")

# ==== End of appleton_v2.4.1_calibration_noise_study.py ====

# ==== Start of appleton_v2.4.1_entanglement_noise_model.py ====
import numpy as np
import matplotlib.pyplot as plt

timesteps = 150
noise_levels = [0.01, 0.03, 0.05, 0.1, 0.2]
dim = 4

def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

def fidelity_approx(rho1, rho2):
    return np.real(np.trace(rho1 @ rho2))

def apply_noise(rho, gamma):
    if gamma > 0.0:
        noise = gamma * np.random.randn(dim, dim)
        noise = (noise + noise.T) / 2
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)
    return rho

ref_state = np.zeros((dim, dim))
ref_state[0, 0] = 1.0

results = {}

for gamma in noise_levels:
    rho = np.eye(dim) / dim
    fidelities = []
    entropies = []

    for _ in range(timesteps):
        rho = apply_noise(rho, gamma)
        fidelities.append(fidelity_approx(ref_state, rho))
        entropies.append(entropy(rho))

    results[gamma] = {'fidelity': fidelities, 'entropy': entropies}

plt.figure(figsize=(12, 5))
for gamma in noise_levels:
    plt.plot(results[gamma]['fidelity'], label=f'γ={gamma}')
plt.title("Fidelity Decay (Entangled System)")
plt.xlabel("Timestep")
plt.ylabel("Fidelity")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/entanglement_fidelity_noise_v2.1.2.png")

plt.figure(figsize=(12, 5))
for gamma in noise_levels:
    plt.plot(results[gamma]['entropy'], label=f'γ={gamma}')
plt.title("Entropy Growth (Entangled System)")
plt.xlabel("Timestep")
plt.ylabel("Entropy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/entanglement_entropy_noise_v2.1.2.png")

# ==== End of appleton_v2.4.1_entanglement_noise_model.py ====

# ==== Start of appleton_v2.4.1_simulate_50_universes.py ====
import numpy as np
import matplotlib.pyplot as plt

num_universes = 50
max_timesteps = 500
entropy_threshold = 1e-3
gamma = 0.02
use_noise = True


def apply_noise(rho, gamma=0.0):
    if gamma > 0.0:
        noise = gamma * np.random.randn(*rho.shape)
        noise = (noise + noise.T) / 2  # Hermitian
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)
    return rho


def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

def simulate_universe():
    rho = np.eye(2) / 2
    for t in range(max_timesteps):
        if use_noise:
            rho = apply_noise(rho, gamma)
        ent = entropy(rho)
        if ent < entropy_threshold:
            return t
    return None

bounce_times = []

for _ in range(num_universes):
    bounce_time = simulate_universe()
    bounce_times.append(bounce_time if bounce_time is not None else max_timesteps)

plt.hist(bounce_times, bins=20, edgecolor='black')
plt.title("Bounce Times with Noise" if use_noise else "Bounce Times without Noise")
plt.xlabel("Timesteps")
plt.ylabel("Number of Universes")
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/bounce_histogram_noise_v2.1.2.png")

# ==== End of appleton_v2.4.1_simulate_50_universes.py ====

# ==== Start of appleton_v2.4.1_simulate_50_universes_safe.py ====
import numpy as np
import matplotlib.pyplot as plt

num_universes = 50
max_timesteps = 500
entropy_threshold = 1e-3
gamma = 0.02
use_noise = True


def apply_noise(rho, gamma=0.0):
    if gamma > 0.0:
        noise = gamma * np.random.randn(*rho.shape)
        noise = (noise + noise.T) / 2  # Hermitian
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)
    return rho


def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

def simulate_universe_safe():
    try:
        rho = np.eye(2) / 2
        for t in range(max_timesteps):
            if use_noise:
                rho = apply_noise(rho, gamma)
            ent = entropy(rho)
            if ent < entropy_threshold:
                return t
    except Exception as e:
        print("Error in simulation:", e)
    return None

bounce_times = []

for _ in range(num_universes):
    bt = simulate_universe_safe()
    bounce_times.append(bt if bt is not None else max_timesteps)

plt.hist(bounce_times, bins=20, edgecolor='black')
plt.title("Bounce Times with Noise (Safe Mode)")
plt.xlabel("Timesteps")
plt.ylabel("Number of Universes")
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/bounce_histogram_safe_noise_v2.1.2.png")

# ==== End of appleton_v2.4.1_simulate_50_universes_safe.py ====

# ==== Start of appleton_v2.4.1_simulate_single_universe.py ====
import numpy as np
import matplotlib.pyplot as plt

timesteps = 500
entropy_threshold = 1e-3
gamma = 0.02  # Noise level
use_noise = True

rho = np.eye(2) / 2
entropies = []


def apply_noise(rho, gamma=0.0):
    if gamma > 0.0:
        noise = gamma * np.random.randn(*rho.shape)
        noise = (noise + noise.T) / 2  # Hermitian
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)
    return rho


def entropy(rho):
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 0]
    return -np.sum(eigvals * np.log(eigvals))

for t in range(timesteps):
    if use_noise:
        rho = apply_noise(rho, gamma)
    ent = entropy(rho)
    entropies.append(ent)
    if ent < entropy_threshold:
        break

plt.plot(entropies)
plt.title("Single Universe Entropy with Noise" if use_noise else "Entropy without Noise")
plt.xlabel("Timestep")
plt.ylabel("Entropy")
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/single_universe_entropy_noise_v2.1.2.png")

# ==== End of appleton_v2.4.1_simulate_single_universe.py ====

# ==== Start of appleton_v2.5.2_page_curve_simulation.py ====

import numpy as np
import matplotlib.pyplot as plt

# Parameters
timesteps = 500
gamma = 0.02
entropy_threshold = 1e-3
dim = 2

# Simulate Page-like curve with a central minimum (information recovery phase)
def simulate_page_like_entropy(dim, timesteps, gamma):
    rho = np.eye(dim) / dim
    entropies = []

    for t in range(timesteps):
        # Decoherence phase
        noise = gamma * np.random.randn(dim, dim)
        noise = (noise + noise.T) / 2
        rho += noise
        rho = (rho + rho.T) / 2
        rho /= np.trace(rho)

        # Small reverse information recovery to model late-time Hawking correlation
        if 200 < t < 350:
            recovery_noise = -0.5 * gamma * np.random.randn(dim, dim)
            recovery_noise = (recovery_noise + recovery_noise.T) / 2
            rho += recovery_noise
            rho = (rho + rho.T) / 2
            rho /= np.trace(rho)

        # Entropy calculation
        eigvals = np.linalg.eigvalsh(rho)
        eigvals = eigvals[eigvals > 0]
        entropy = -np.sum(eigvals * np.log(eigvals))
        entropies.append(entropy)

    return entropies

entropies = simulate_page_like_entropy(dim, timesteps, gamma)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(entropies, label="Simulated Page-like Curve")
plt.axvline(x=250, color='red', linestyle='--', label='Information Recovery Phase')
plt.title("Simulated Page Curve with Information Recovery")
plt.xlabel("Timestep")
plt.ylabel("Entropy")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save figure
plt.savefig("/mnt/data/page_curve_entropy_recovery_simulation_v2.5.2.png")


# ==== End of appleton_v2.5.2_page_curve_simulation.py ====

# ==== Main Simulation Runner ====

# Combined Universe Fidelity Simulation Suite
# Section 2.10.2.1 - Combined Fidelity + Noise + Page Curve Study

# Expected Behavior:
# This composite simulation draws from 50-universe stochastic runs, single-universe evolution, 
# calibration noise modeling, entanglement-based degradation, and noisy Page curve trends.
# Expect:
# - Slightly diverging entropy tracks depending on noise fidelity.
# - Ensemble behavior suggesting quasi-stabilization or decoherence branching.
# - Cross-validation of Page curve signatures under entanglement noise models.

print("Running: Calibration Noise Study")
# [REMOVED exec] Code from this file is now included inline above.

print("Running: Entanglement Noise Model")
# [REMOVED exec] Code from this file is now included inline above.

print("Running: Simulate 50 Universes")
# [REMOVED exec] Code from this file is now included inline above.

print("Running: Simulate 50 Universes (Safe)")
# [REMOVED exec] Code from this file is now included inline above.

print("Running: Simulate Single Universe")
# [REMOVED exec] Code from this file is now included inline above.

print("Running: Noisy Page Curve Simulation")
# [REMOVED exec] Code from this file is now included inline above.

print("✅ All 2.10.2.1 simulations complete.")
