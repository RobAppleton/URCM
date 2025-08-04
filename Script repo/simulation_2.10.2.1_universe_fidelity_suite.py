
# Combined Universe Fidelity Simulation Suite
# Section 2.10.2.1 - Combined Fidelity + Noise + Page Curve Study

# Expected Behavior:
# This composite simulation draws from 50-universe stochastic runs, single-universe evolution, 
# calibration noise modeling, entanglement-based degradation, and noisy Page curve trends.
# Expect:
# - Slightly diverging entropy tracks depending on noise fidelity.
# - Ensemble behavior suggesting quasi-stabilization or decoherence branching.
# - Cross-validation of Page curve signatures under entanglement noise models.

print("Running: Calibration Noise Study")
exec(open("appleton_v2.4.1_calibration_noise_study.py").read())

print("Running: Entanglement Noise Model")
exec(open("appleton_v2.4.1_entanglement_noise_model.py").read())

print("Running: Simulate 50 Universes")
exec(open("appleton_v2.4.1_simulate_50_universes.py").read())

print("Running: Simulate 50 Universes (Safe)")
exec(open("appleton_v2.4.1_simulate_50_universes_safe.py").read())

print("Running: Simulate Single Universe")
exec(open("appleton_v2.4.1_simulate_single_universe.py").read())

print("Running: Noisy Page Curve Simulation")
exec(open("appleton_v2.5.2_page_curve_simulation.py").read())

print("✅ All 2.10.2.1 simulations complete.")
