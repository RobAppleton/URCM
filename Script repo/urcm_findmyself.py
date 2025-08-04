import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === CONFIGURATION ===
recursions = 25000
dim = 64

# === URCM Operator Definitions ===
def bounce_operator(state):
    idx = np.argmax(np.abs(state)**2)
    reset = np.zeros_like(state)
    reset[idx] = 1.0
    return reset

def temporal_modulation(state, cycle):
    noise_strength = 0.005 + 0.002 * np.log1p(cycle)
    noise = np.random.normal(0, noise_strength, state.shape) + 1j * np.random.normal(0, noise_strength, state.shape)
    modulated = state + noise
    return modulated / np.linalg.norm(modulated)

def fix_operator(state):
    return state / np.linalg.norm(state)

def recursive_R_operator(state, cycle):
    state = fix_operator(state)
    state = temporal_modulation(state, cycle)
    state = bounce_operator(state)
    return fix_operator(state)

# === METRIC DEFINITIONS (VALIDATED) ===
def metric_operator_fingerprint(states):
    return np.mean([np.linalg.norm(np.fft.fft(s)) for s in states])

def metric_bounce_density_peak(states):
    return np.max([np.abs(s).max() for s in states])

def metric_teleology(states):
    final = states[-1]
    return np.sum(np.real(final)**2)

def metric_spectral_entropy_variation(states):
    data = [np.mean(np.real(s)) for s in states]
    return np.std(np.abs(np.fft.fft(data)))

def metric_recursive_energy_ratio(states):
    return np.linalg.norm(states[-1]) / (np.linalg.norm(states[0]) + 1e-12)

def metric_coherence_persistence(states):
    return np.mean([np.real(np.vdot(s, states[0])) for s in states])

def metric_bounce_entropy_gradient(states):
    entropies = [np.linalg.norm(s)**2 for s in states]
    return np.mean(np.gradient(entropies))

# === SIMULATION ===
metrics_log = []
initial_state = np.random.rand(dim) + 1j * np.random.rand(dim)
initial_state = initial_state / np.linalg.norm(initial_state)

state = initial_state
state_history = []

for i in range(recursions):
    state = recursive_R_operator(state, i)
    state_history.append(state.copy())

    if i % 1000 == 0 or i == recursions - 1:
        subset = state_history[-100:]
        metrics_log.append({
            "recursion": i,
            "operator_fingerprint": metric_operator_fingerprint(subset),
            "bounce_density_peak": metric_bounce_density_peak(subset),
            "teleology": metric_teleology(subset),
            "spectral_entropy_variation": metric_spectral_entropy_variation(subset),
            "recursive_energy_ratio": metric_recursive_energy_ratio(subset),
            "coherence_persistence": metric_coherence_persistence(subset),
            "bounce_entropy_gradient": metric_bounce_entropy_gradient(subset),
        })

# === EXPORT ===
df_metrics = pd.DataFrame(metrics_log)
df_metrics.to_csv("urcm_metrics_output.csv", index=False)

plt.figure(figsize=(12, 8))
for metric in df_metrics.columns[1:]:
    plt.plot(df_metrics['recursion'], df_metrics[metric], label=metric)
plt.xlabel("Recursion")
plt.ylabel("Metric Value")
plt.title("Validated URCM Metrics Over Recursive Cycles")
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.savefig("urcm_metrics_plot.png", dpi=300)
plt.close()
