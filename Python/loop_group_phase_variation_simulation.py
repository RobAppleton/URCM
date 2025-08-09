
import numpy as np
import matplotlib.pyplot as plt

# Phase-based recursion: show what happens when operator phases vary
cycles = 100
theta = np.linspace(0, 2 * np.pi, cycles)

# Define operator variations with phase shifts
B = np.sin(theta)                     # Standard sine for B
S = np.sign(np.sin(2 * theta + np.pi / 4))  # Shifted binary toggle for S
C = np.cos(theta + np.pi / 3)        # Phase-shifted cosine for C

# Composite recursive operator
R = B * S * C

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(theta, R, label="Phase-shifted R = B ∘ S ∘ C", color='crimson')
plt.plot(theta, B, '--', label="B(θ) = sin(θ)", alpha=0.5)
plt.plot(theta, S, '--', label="S(θ) = sign(sin(2θ + π/4))", alpha=0.5)
plt.plot(theta, C, '--', label="C(θ) = cos(θ + π/3)", alpha=0.5)
plt.title("Loop Group Phase Variation and Resonance")
plt.xlabel("θ (Cycle Phase)")
plt.ylabel("Operator Output")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("loop_group_phase_variation.png")
plt.show()
