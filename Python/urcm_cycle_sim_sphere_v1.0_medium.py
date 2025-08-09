import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as animation
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D

timesteps, gamma, dim = 200, 0.02, 2
dpi, fps = 100, 10
entropy_threshold = 1e-3
rho = np.eye(dim)/dim
rho_ref = np.eye(dim)/dim
t_vals = np.linspace(0.5, 2.5, timesteps)
phase = np.sin(2*np.pi*(t_vals-0.5))

def apply_noise(r,g):
    n = g*np.random.randn(*r.shape); n=(n+n.T)/2
    r+=n; r=(r+r.T)/2; return r/np.trace(r)

def entropy(r):
    vals = np.linalg.eigvalsh(r); vals=vals[vals>0]
    return -(vals*np.log(vals)).sum()

def fidelity(a,b): return np.real(np.trace(a@b))

E,F = [],[]
bounce_cnt=0; last_bounce=-50
for i,t in enumerate(t_vals):
    E.append(entropy(rho));  F.append(fidelity(rho_ref,rho))
    if E[-1]<entropy_threshold and i-last_bounce>40:
        bounce_cnt+=1; last_bounce=i; rho=np.eye(dim)/dim
    else: rho = apply_noise(rho,gamma)

fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(111, projection='3d')

# Initialize sphere
u = np.linspace(0, 2*np.pi, 20)
v = np.linspace(0, np.pi, 20)
u, v = np.meshgrid(u, v)
colors = ['red', 'green', 'blue']  # Color cycle for bounces

def update(i):
    ax.clear()
    # Sphere radius based on URCM phase
    r = 0.5 + 0.5*phase[i]  # Range 0 to 1
    x = r * np.sin(v) * np.cos(u)
    y = r * np.sin(v) * np.sin(u)
    z = r * np.cos(v)
    
    # Color based on bounce count
    color = colors[bounce_cnt % len(colors)]
    ax.plot_surface(x, y, z, color=color, alpha=0.8)
    
    # Set axes limits
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    
    # Text annotations
    for tag in ('cyc_txt','stable_txt','model_txt','copy_txt','info_txt'):
        if hasattr(update, tag): getattr(update, tag).remove()

    cycle_val = t_vals[i]
    update.cyc_txt = ax.text2D(0.01, 1.04, f"Cycle {cycle_val:.3f}",
                               transform=ax.get_figure().gca().transAxes, 
                               ha='left', va='bottom', fontsize=7)

    if 'first_stable' not in update.__dict__ and i>0 and E[i]<entropy_threshold and E[i-1]<entropy_threshold:
        update.first_stable = cycle_val

    y0 = -0.10
    if hasattr(update, 'first_stable'):
        update.stable_txt = ax.text2D(0.01, y0,
                                      f"Stable at {update.first_stable:.3f}",
                                      transform=ax.get_figure().gca().transAxes, 
                                      ha='left', va='top', fontsize=7)
        y0 -= 0.06

    update.model_txt = ax.text2D(0.01, y0,
                                 "URCM cosmological model - R=a.b.c",
                                 transform=ax.get_figure().gca().transAxes, 
                                 ha='left', va='top', fontsize=7)
    y0 -= 0.06

    update.copy_txt = ax.text2D(0.01, y0,
                                "(c) R.W.Appleton " + datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
                                transform=ax.get_figure().gca().transAxes, 
                                ha='left', va='top', fontsize=6)
    y0 -= 0.05

    update.info_txt = ax.text2D(0.01, y0,
                                "all code and documents available robin.appleton@protonmail.com",
                                transform=ax.get_figure().gca().transAxes, 
                                ha='left', va='top', fontsize=5)

    return (ax.plot_surface(x, y, z, color=color), update.cyc_txt,
            *(getattr(update,k) for k in ('stable_txt','model_txt','copy_txt','info_txt')
              if hasattr(update,k)))

ani = animation.FuncAnimation(fig, update, frames=timesteps, blit=False)
ani.save("urcm_cycle_sim_sphere_v1.0_medium.gif", writer='pillow', fps=fps, dpi=dpi, save_all=True, optimize=True)