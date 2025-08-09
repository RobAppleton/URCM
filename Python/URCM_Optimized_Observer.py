import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.stats import skew

# --- Core Modules ---

def cycle_entropy_slope(cycle):
    return 0.01 * np.sin(cycle / 5)

def expansion_dilution(Λ):
    return Λ * 0.001

def recursive_universe_step(state, cycle, Λ_eff):
    entropy_slope = cycle_entropy_slope(cycle)
    dark_energy_mod = Λ_eff * (1 + 0.01 * np.sin(cycle / 10))
    matter_growth = dark_matter_growth(state['density'], entropy_slope)

    new_density = state['density'] + matter_growth - expansion_dilution(dark_energy_mod)
    new_entropy = state['entropy'] + entropy_slope

    return {
        'density': new_density,
        'entropy': new_entropy,
        'Λ': dark_energy_mod,
        'cycle': cycle + 1
    }

def dark_matter_growth(density, entropy_gradient):
    fluctuation = np.random.normal(0, 0.01, size=density.shape)
    growth = 0.05 * np.tanh(entropy_gradient) * (1 + fluctuation)
    return density * growth

def predict_clock_drift(cycles, base_drift=1e-18):
    return base_drift * (1 + 0.001 * np.sin(2 * np.pi * cycles / 50))

# --- Optimized Metrics ---

def extract_metrics(state_series):
    entropy_series = [s['entropy'] for s in state_series]
    Λ_series = [s['Λ'] for s in state_series]
    density_series = [s['density'] for s in state_series]
    clock_drift = predict_clock_drift(np.arange(len(state_series)))

    # 1. Clock Drift Spectrum
    clock_drift_fft = np.abs(fft(clock_drift - np.mean(clock_drift)))
    clock_freqs = np.fft.fftfreq(len(clock_drift))

    # 2. CMB Low-ℓ Envelope
    cmb_variance = [np.std(s['density']) for s in state_series]
    window = 500
    cmb_low_l = np.array([np.std(cmb_variance[i:i+window]) for i in range(len(cmb_variance)-window)])

    # 3. Lensing Gradient Distortion (Skew)
    density_skew = [skew(s['density'].flatten()) for s in state_series]

    # 4. Λ(t) Drift Reversals
    Λ_diff = np.diff(Λ_series)
    Λ_reversals = np.where(np.diff(np.sign(Λ_diff)) != 0)[0]

    # 5. Entropy Collapse + Λ Spike Coincidence
    entropy_minima = np.where(np.array(entropy_series) < np.percentile(entropy_series, 2))[0]
    Λ_peaks = np.where(np.array(Λ_series) > np.percentile(Λ_series, 98))[0]
    coincidence_events = np.intersect1d(entropy_minima, Λ_peaks)

    return {
        'entropy': entropy_series,
        'Λ_trace': Λ_series,
        'cmb_low_l': cmb_low_l,
        'density_skew': density_skew,
        'clock_freqs': clock_freqs[:len(clock_freqs)//2],
        'clock_spectrum': clock_drift_fft[:len(clock_drift_fft)//2],
        'Λ_reversals': Λ_reversals,
        'coincidence_events': coincidence_events
    }

# --- Simulation Driver ---

def run_simulation(cycles=25000):
    state_series = [{
        'density': np.ones((10, 10)) * 0.5,
        'entropy': 0.0,
        'Λ': 0.7,
        'cycle': 0
    }]
    for i in range(cycles):
        state_series.append(recursive_universe_step(state_series[-1], i, state_series[-1]['Λ']))
    return extract_metrics(state_series)
