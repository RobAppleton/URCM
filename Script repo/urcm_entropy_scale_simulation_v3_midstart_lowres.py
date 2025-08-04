
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# REM: URCM Simulation — Entropy and Scale Factor Evolution (Double Cycle, Midstate Start)
# REM:
# REM: This simulation starts at the midpoint between two singularities (t = 0.5), when the 
# REM: universe is neither fully collapsed nor fully expanded. From this mid-bounce state,
# REM: it progresses through two full cycles, ending again at a mid-bounce state (t = 2.5).
# REM: The purpose is to verify that the entropy evolution and scale factor oscillations reflect
# REM: two recursive cosmic cycles and signal singularity resets via entropy collapse.
# REM:
# REM: EXPECTED BEHAVIOR:
# REM: - Entropy should rise under decoherence and sharply collapse (reset) twice.
# REM: - Scale factor should complete two bounces, oscillating through contraction and expansion.
# REM: - Caption should mark when the singularity-like entropy collapse occurs.
# REM:
# REM: Name: urcm_entropy_scale_simulation_v3_midstart_lowres.py

# Parameters
timesteps = 400
gamma = 0.02
dim = 2
entropy_threshold = 1e-3
rho = np.eye(dim) / dim  # Start at maximal uncertainty

def apply_noise(rho, gamma=0.0):
    noise = gamma * np.random.randn(*rho.shape)
    noise = (noise + noise.T) / 2
    rho += noise
    rho = (rho + rho.T) / 2
    rho /= np.trace(rho)
    return rho

def entropy(rho):
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 0]
    return -np.sum(eigvals * np.log(eigvals))

def scale_factor(t):
    return 1.0 * (1 + 0.8 * np.sin(4 * np.pi * t)) * (1 - 1.0 / 0.41)

# Time from mid-bounce to mid-bounce: t = 0.5 to 2.5 (two full URCM cycles)
t_vals = np.linspace(0.5, 2.5, timesteps)
entropies, scales = [], []

for t in t_vals:
    a = scale_factor(t)
    rho = apply_noise(rho, gamma)
    S = entropy(rho)
    entropies.append(S)
    scales.append(a)

# Plot setup (not executed)
fig, ax = plt.subplots(figsize=(6, 3.5))  # Low-res canvas
line1, = ax.plot([], [], label="Entropy", lw=1)
line2, = ax.plot([], [], label="Scale Factor", lw=1)
ax.set_xlim(0, len(entropies))
ax.set_ylim(0, max(max(entropies), max(scales)) * 1.1)
ax.legend(fontsize=8)
ax.grid(True)

xdata, y1, y2 = [], [], []

def update(i):
    xdata.append(i)
    y1.append(entropies[i])
    y2.append(scales[i])
    line1.set_data(xdata, y1)
    line2.set_data(xdata, y2)

    if hasattr(update, "caption"):
        update.caption.remove()

    text = f"t={{t_vals[i]:.2f}}: Entropy = {{entropies[i]:.3f}}, Scale = {{scales[i]:.3f}}"
    if entropies[i] < entropy_threshold:
        text += " — Singularity reacquired, universe restarts."

    update.caption = ax.text(0.5, 1.05, text, transform=ax.transAxes,
                             ha="center", fontsize=9, color='darkred')

    return line1, line2, update.caption

# Animation and file save section (not executed per user preference):
# ani = animation.FuncAnimation(fig, update, frames=len(entropies), blit=True)
# ani.save("urcm_entropy_scale_simulation_v3_midstart_lowres.mp4", fps=10, dpi=80, extra_args=['-vcodec', 'libx264'])

# REM: END OF SIMULATION
# REM:
# REM: If the video shows entropy rising and collapsing twice, with scale factor oscillating 
# REM: through two bounce cycles, and bounce captions appear at the correct entropy minima,
# REM: then the simulation successfully demonstrates the URCM recursion from singularity to singularity.
