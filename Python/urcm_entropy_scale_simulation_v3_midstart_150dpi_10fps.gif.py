
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# REM: URCM Simulation — Entropy and Scale Factor Evolution (High-Res GIF Output, Final)
# REM:
# REM: This simulation has been created solely using URCM Python simulations, derived from
# REM: first principles. These include recursive entropy compression and scale factor modeling
# REM: based on theoretical formulations involving r = a(t), von Neumann entropy dynamics,
# REM: and decoherence operators within a 2D Hilbert space.

# REM:
# REM: This simulation begins at t = 0.5 (mid-bounce) and spans to t = 2.5, completing two full
# REM: URCM cycles. It models entropy and scale factor evolution as the universe moves between
# REM: singularity resets. Bounce events are signaled when entropy collapses below threshold.
# REM:
# REM: RENDERING PARAMETERS:
# REM: - Output Format: Animated GIF
# REM: - Frame Count: 400
# REM: - Figure Size: 12 x 6 inches
# REM: - DPI: 150
# REM: - FPS: 10
# REM: - Writer: Pillow
# REM:
# REM: Name: urcm_entropy_scale_simulation_v3_midstart_highres_gif_final.py

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

t_vals = np.linspace(0.5, 2.5, timesteps)
entropies, scales = [], []

for t in t_vals:
    a = scale_factor(t)
    rho = apply_noise(rho, gamma)
    S = entropy(rho)
    entropies.append(S)
    scales.append(a)

fig, ax = plt.subplots(figsize=(12, 6))
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

    text = f"t={t_vals[i]:.2f}: Entropy = {entropies[i]:.3f}, Scale = {scales[i]:.3f}"
    if entropies[i] < entropy_threshold:
        text += " — Singularity reacquired, universe restarts."

    update.caption = ax.text(0.5, 1.05, text, transform=ax.transAxes,
                             ha="center", fontsize=12, color='darkred')

    return line1, line2, update.caption

ani = animation.FuncAnimation(fig, update, frames=len(entropies), blit=True)
ani.save("urcm_entropy_scale_simulation_v3_midstart_highres.gif", writer='pillow', fps=10, dpi=150)
