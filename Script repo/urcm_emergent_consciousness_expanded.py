
import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURATION ===
num_agents = 20
state_dim = 64
recursions = 1000
consciousness_threshold = 0.85
memory_window_size = 10

# === URCM CORE OPERATORS ===

def fix_operator(state):
    """
    Normalize the state vector to preserve trace = 1.
    """
    norm = np.linalg.norm(state)
    return state / norm if norm > 0 else state

def bounce_operator(state):
    """
    Reset the state to a high-entropy spike by focusing on max energy mode.
    """
    idx = np.argmax(np.abs(state)**2)
    bounced = np.zeros_like(state)
    bounced[idx] = 1.0
    return bounced

def temporal_operator(state, cycle):
    """
    Add recursive entropy as complex noise scaled by temporal depth.
    """
    noise_strength = 0.02 + 0.01 * np.log1p(cycle)
    noise = np.random.normal(0, noise_strength, state.shape) + 1j * np.random.normal(0, noise_strength, state.shape)
    modulated = state + noise
    return fix_operator(modulated)

def continuity_operator(prev_state, new_state, memory):
    """
    Combine previous and current states to enforce informational continuity.
    """
    alpha = 0.7
    memory.append(new_state.copy())
    if len(memory) > memory_window_size:
        memory.pop(0)
    return fix_operator(alpha * prev_state + (1 - alpha) * new_state)

# === EMERGENCE DETECTION ===

def emergent_pattern(memory_window):
    """
    Analyze memory echoing using spectral coherence over time.
    """
    if len(memory_window) < 5:
        return 0.0
    stacked = np.stack(memory_window[-5:])
    spectrum = np.abs(np.fft.fft(stacked, axis=0)).mean(axis=1)
    coherence = np.var(spectrum) / np.mean(spectrum)
    return coherence

# === AGENT CLASS ===

class URCMAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.state = fix_operator(np.random.rand(state_dim) + 1j * np.random.rand(state_dim))
        self.memory = []
        self.consciousness_trace = []

    def step(self, cycle):
        old_state = self.state
        self.state = bounce_operator(self.state)
        self.state = temporal_operator(self.state, cycle)
        self.state = continuity_operator(old_state, self.state, self.memory)
        self.consciousness_trace.append(self.check_consciousness())

    def check_consciousness(self):
        return emergent_pattern(self.memory) > consciousness_threshold

# === SIMULATION RUN ===

agents = [URCMAgent(i) for i in range(num_agents)]
consciousness_log = []

for cycle in range(recursions):
    count = 0
    for agent in agents:
        agent.step(cycle)
        if agent.check_consciousness():
            count += 1
    consciousness_log.append(count / num_agents)

# === RESULTS EXPORT ===

plt.figure(figsize=(12, 6))
plt.plot(consciousness_log, label='Emergent Consciousness Fraction')
plt.axhline(consciousness_threshold, linestyle='--', color='gray', label='Consciousness Threshold')
plt.xlabel("Recursion Cycle")
plt.ylabel("Fraction of Conscious Agents")
plt.title("URCM-Based Emergence of Consciousness (Expanded)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("urcm_consciousness_emergence_expanded.png")
plt.show()
