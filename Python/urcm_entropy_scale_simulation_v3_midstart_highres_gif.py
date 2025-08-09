
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# REM: URCM Simulation — Entropy and Scale Factor Evolution (High-Res GIF Output)
# REM:
# REM: This simulation starts at the midpoint between two singularities (t = 0.5), and 
# REM: spans two complete cycles, ending at the next mid-bounce. It tracks entropy and 
# REM: scale factor evolution to illustrate singularity-collapse and recursion.
# REM:
# REM: This version is optimized for maximum reasonable visual quality (high DPI and figsize).
# REM: It will output an animated GIF using the Pillow writer.
# REM:
# REM: Name: urcm_entropy_scale_simulation_v3_midstart_highres_gif.py

# Parameters
timesteps = 400
gamma = 0.02
dim = 2
entropy_threshold = 1e-3
rho = np.eye(dim) / dim

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

# Midstate to midstate domain
t_vals = np.linspace(0.5, 2.5, timesteps)
entropies, scales = [], []

for t in t_vals:
    a = scale_factor(t)
    rho = apply_noise(rho, gamma)
    S = entropy(rho)
    entropies.append(S)
    scales.append(a)

# High-resolution figure canvas
fig, ax = plt.subplots(figsize=(12, 6))  # Large visual canvas
line1, = ax.plot([], [], label="Entropy", lw=2)
line2, = ax.plot([], [], label="Scale Factor", lw=2)
ax.set_xlim(0, len(entropies))
ax.set_ylim(0, max(max(entropies), max(scales)) * 1.1)
ax.legend(fontsize=12)
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
                             ha="center", fontsize=12, color='darkred')

    return line1, line2, update.caption

# Save as high-resolution animated GIF (not executed by default)
# ani = animation.FuncAnimation(fig, update, frames=len(entropies), blit=True)
# ani.save("urcm_entropy_scale_simulation_v3_midstart_highres.gif", writer='pillow', fps=10, dpi=150)

# REM: This version is optimized for clarity. If the resulting GIF fails to render due to memory
# REM: constraints, reduce `figsize` or `dpi` values.
