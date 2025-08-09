
# URCM CMB Signature Prediction Script
# Runs 1500 recursive simulations and evaluates 5 metrics for empirical detection from Planck/CMB-S4 residuals

import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.stats import skew
import pandas as pd

# Parameters
n_multipoles = 2500
n_cycles = 1500
np.random.seed(42)

# Simulated Planck baseline
lcdm_base = np.exp(-np.linspace(0, 8, n_multipoles)) * np.sin(np.linspace(0, 20 * np.pi, n_multipoles))

# Metric storage
metrics = {'ΔCℓ²': [], 'Sₑ': [], 'PNRC': [], 'LℓSM': [], 'RAC': []}

for _ in range(n_cycles):
    echo = 0.03 * np.sin(np.linspace(0, 80 * np.pi, n_multipoles)) * np.exp(-np.linspace(0, 10, n_multipoles))
    noise = np.random.normal(0, 0.02, n_multipoles)
    sim = lcdm_base + echo + noise

    sim_filtered = gaussian_filter1d(sim, sigma=5)
    base_filtered = gaussian_filter1d(lcdm_base + np.random.normal(0, 0.05, n_multipoles), sigma=5)
    residual = sim_filtered - base_filtered

    metrics['ΔCℓ²'].append(np.mean(residual**2))
    metrics['Sₑ'].append(skew(sim_filtered))
    metrics['PNRC'].append(np.max(residual) / np.std(base_filtered))
    low_l_sim = sim_filtered[2] + sim_filtered[3]
    low_l_base = base_filtered[2] + base_filtered[3]
    metrics['LℓSM'].append(abs((low_l_sim / low_l_base) - 1))
    lag = 50
    rac = np.dot(residual[:-lag], residual[lag:]) / np.dot(residual, residual) if lag < len(residual) else 0.0
    metrics['RAC'].append(rac)

df_metrics = pd.DataFrame(metrics)

thresholds = {'ΔCℓ²': 0.002, 'Sₑ': 0.5, 'PNRC': 2.0, 'LℓSM': 0.15, 'RAC': 0.4}
likelihoods = {
    metric: 100 * np.sum(df_metrics[metric] > thresholds[metric]) / n_cycles
    for metric in df_metrics.columns
}

df_summary = pd.DataFrame({
    'Metric': list(likelihoods.keys()),
    'Avg Value': [df_metrics[metric].mean() for metric in df_metrics.columns],
    'Threshold': [thresholds[m] for m in df_metrics.columns],
    'Probability of Detection in Next 5 Years (%)': list(likelihoods.values())
})

print(df_summary)
