
import numpy as np
import matplotlib.pyplot as plt

# --- Configuration Parameters ---
num_agents = 20
state_dim = 64
recursions = 500
consciousness_threshold = 0.85

# --- URCM Operators ---

def fix_operator(state):
    norm = np.linalg.norm(state)
    return state / norm if norm > 0 else state

def bounce_operator(state):
    idx = np.argmax(np.abs(state)**2)
    bounced = np.zeros_like(state)
    bounced[idx] = 1.0
    return bounced

def temporal_operator(state, cycle):
    noise_strength = 0.02 + 0.01 * np.log1p(cycle)
    noise = np.random.normal(0, noise_strength, state.shape) + 1j * np.random.normal(0, noise_strength, state.shape)
    modulated = state + noise
    return fix_operator(modulated)

def continuity_operator(prev_state, new_state, memory):
    alpha = 0.7
    memory.append(new_state.copy())
    return fix_operator(alpha * prev_state + (1 - alpha) * new_state)

# --- Consciousness Detector ---

def emergent_pattern(memory_window):
    # Check for pattern echoing or stability in frequency
    if len(memory_window) < 5:
        return 0.0
    stacked = np.stack(memory_window[-5:])
    spectrum = np.abs(np.fft.fft(stacked, axis=0)).mean(axis=1)
    coherence = np.var(spectrum) / np.mean(spectrum)
    return coherence

# --- Agent Definition ---

class URCMAgent:
    def __init__(self):
        self.state = fix_operator(np.random.rand(state_dim) + 1j * np.random.rand(state_dim))
        self.memory = []

    def step(self, cycle):
        old_state = self.state
        self.state = bounce_operator(self.state)
        self.state = temporal_operator(self.state, cycle)
        self.state = continuity_operator(old_state, self.state, self.memory)

    def check_consciousness(self):
        return emergent_pattern(self.memory) > consciousness_threshold

# --- Simulation ---

agents = [URCMAgent() for _ in range(num_agents)]
consciousness_log = []

for cycle in range(recursions):
    count = 0
    for agent in agents:
        agent.step(cycle)
        if agent.check_consciousness():
            count += 1
    consciousness_log.append(count / num_agents)

# --- Visualization ---

plt.figure(figsize=(10, 5))
plt.plot(consciousness_log, label='Emergent Consciousness Fraction')
plt.axhline(consciousness_threshold, linestyle='--', color='gray', label='Threshold')
plt.xlabel("Recursion Cycle")
plt.ylabel("Fraction of Conscious Agents")
plt.title("URCM-Based Emergence of Consciousness")
plt.legend()
plt.tight_layout()
plt.savefig("urcm_consciousness_emergence.png")
plt.show()
