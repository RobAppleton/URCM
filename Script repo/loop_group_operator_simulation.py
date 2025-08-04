
import numpy as np
import matplotlib.pyplot as plt

# Number of recursive cycles (loop traversals)
cycles = 100

# Define operator phases on the loop (mod 2pi traversal)
theta = np.linspace(0, 2 * np.pi, cycles)
B = np.sin(theta)            # Operator B oscillation
S = np.sign(np.sin(2*theta)) # Operator S binary flip
C = np.cos(theta)            # Operator C oscillation

# Composite recursive signal (interpreted as loop group dynamics)
R = B * S * C

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(theta, R, label="Recursive Loop Composite R = B ∘ S ∘ C", color='darkgreen')
plt.plot(theta, B, '--', label="B(θ) = sin(θ)", alpha=0.5)
plt.plot(theta, S, '--', label="S(θ) = sign(sin(2θ))", alpha=0.5)
plt.plot(theta, C, '--', label="C(θ) = cos(θ)", alpha=0.5)
plt.title("Simulated Loop Group Traversal of Recursive Operators")
plt.xlabel("θ (Cycle Phase)")
plt.ylabel("Operator Output")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("loop_group_traversal.png")
plt.show()
