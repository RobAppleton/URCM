# REM: URCM Simulation — Midcycle Start and Stability-Aware Caption (v1.4)
# REM:
# REM: Starts at midbounce, tracks entropy/fidelity, and shows URCM operator phase.
# REM: Footer and cycle label update visually once stability is reached.
# REM:
# REM: Rendering Parameters:
# REM: - Format: GIF
# REM: - FPS: 10
# REM: - Resolution: 4x2 inches
# REM: - Output: urcm_cycle_sim_v1.4_canonical.gif

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

timesteps = 400
gamma = 0.02
dim = 2
dpi = 80
fps = 10
entropy_threshold = 1e-3
rho = np.eye(dim) / dim
rho_ref = np.eye(dim) / dim

# Midcycle start
t_vals = np.linspace(0.5, 2.5, timesteps)
phase_vals = np.sin(2 * np.pi * (t_vals - 0.5))

def apply_noise(rho, gamma):
    noise = gamma * np.random.randn(*rho.shape)
    noise = (noise + noise.T) / 2
    rho += noise
    rho = (rho + rho.T) / 2
    rho /= np.trace(rho)
    return rho

def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0]
    return -np.sum(vals * np.log(vals))

def fidelity(r1, r2):
    return np.real(np.trace(r1 @ r2))

entropies, fidelities, cycles = [], [], []
operator_C = np.zeros(timesteps)
operator_S = np.zeros(timesteps)
operator_B = np.zeros(timesteps)

bounce_count = 0
last_bounce_frame = -50
sustain_triggered = False
sustain_frame = -1
stable_cycle = None

for i, t in enumerate(t_vals):
    S = entropy(rho)
    F = fidelity(rho_ref, rho)
    entropies.append(S)
    fidelities.append(F)
    cycles.append(bounce_count)

    operator_C[i] = 1 if 0.6 < t % 1.0 < 0.8 else 0
    operator_S[i] = 1 if S < entropy_threshold else 0
    operator_B[i] = 1 if 0.1 < t % 1.0 < 0.3 else 0

    if S < entropy_threshold and (i - last_bounce_frame > 40):
        if bounce_count > 0 and not sustain_triggered:
            sustain_triggered = True
            sustain_frame = i
            stable_cycle = bounce_count
        bounce_count += 1
        last_bounce_frame = i
        rho = np.eye(dim) / dim
    else:
        rho = apply_noise(rho, gamma)

fig, ax = plt.subplots(figsize=(4, 2))
line_E, = ax.plot([], [], label="Entropy", color="blue", lw=1)
line_F, = ax.plot([], [], label="Fidelity", color="red", lw=1)
line_P, = ax.plot([], [], label="URCM Phase", color="black", linestyle=':', lw=0.8)

ax.set_xlim(0, timesteps)
ax.set_ylim(0, 1.1)
ax.legend(loc="upper right", fontsize=6)
ax.set_xticks([])
ax.set_yticks([])

x, yE, yF, yP = [], [], [], []

def update(i):
    x.append(i)
    yE.append(entropies[i])
    yF.append(fidelities[i])
    yP.append(0.5 + 0.5 * phase_vals[i])

    line_E.set_data(x, yE)
    line_F.set_data(x, yF)
    line_P.set_data(x, yP)

    for tag in ["caption", "cycle", "footer1", "footer2"]:
        if hasattr(update, tag):
            getattr(update, tag).remove()

    update.caption = ax.text(0.5, 1.05,
        f"t={t_vals[i]:.2f} | S={entropies[i]:.3f} | F={fidelities[i]:.3f}",
        transform=ax.transAxes, ha="center", va="bottom", fontsize=6)

    if sustain_triggered and i >= sustain_frame:
        cycle_text = f"Cycle {cycles[i]} — STABLE at cycle {stable_cycle}"
        cycle_color = "limegreen"
    else:
        cycle_text = f"Cycle {cycles[i]}"
        cycle_color = "lightgreen"

    update.cycle = ax.text(0.01, 1.05,
        cycle_text,
        transform=ax.transAxes, ha="left", va="bottom", fontsize=6, color=cycle_color)

    update.footer1 = ax.text(0.5, -0.24,
        "© R.W. Appleton 2025. All rights reserved.",
        transform=ax.transAxes, ha="center", va="top", fontsize=6, color="black")

    footer_formula = (
        "URCM (R = B ∘ S ∘ C) has reached stable condition"
        if sustain_triggered and i >= sustain_frame else
        "URCM formalism: R = B ∘ S ∘ C"
    )

    footer_color = "limegreen" if sustain_triggered and i >= sustain_frame else "lightgreen"

    update.footer2 = ax.text(0.5, -0.32,
        footer_formula,
        transform=ax.transAxes, ha="center", va="top", fontsize=6, color=footer_color)

    return line_E, line_F, line_P, update.caption, update.cycle, update.footer1, update.footer2

ani = animation.FuncAnimation(fig, update, frames=timesteps, blit=True)
ani.save(gif_output_path, writer="pillow", fps=fps, dpi=dpi)
