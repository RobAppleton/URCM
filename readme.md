# Unified Recursive Cosmological Model (URCM)

The **Unified Recursive Cosmological Model (URCM)** proposes a structurally recursive framework for cosmology that replaces scalar-field inflation and arbitrary initial conditions with symbolic operator logic. URCM models the universe’s origin, evolution, and entropy dynamics as the output of constrained symbolic grammars, governed by operator sets such as `Ĉ`, `Ŝ`, and `T̂`.

This repository contains core simulation scripts, prototype grammars, empirical test modules, and evolving documentation intended for both research and reproducibility.
robin.appleton@protonmail.com

---

## Overview

URCM is designed to:

- Address the low-entropy problem without resorting to inflation.
- Construct cosmic structure via recursive symbolic operations.
- Provide falsifiable predictions and engage directly with empirical data.
- Serve as a testbed for operator-based cosmological simulations.

---

## Key Features

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Recursive Logic Engine   | Simulates evolution via rule-driven symbolic operators.                    |
| Entropy Resolution       | Models entropy as residue of recursive constraint failure.                 |
| Empirical Alignment      | Engages data from Planck, BICEP2, and LiteBIRD missions.                   |
| Comparative Metrics      | Includes falsifiability and self-maintenance tracking across cycles.        |

---

## Directory Structure

```
urcm/
├── urcm_core.py              # Main symbolic recursion engine
├── operators/
│   ├── init_operator_set.py  # Primary operator definitions (Ĉ, Ŝ, T̂)
│   └── transition_rules.py   # Logic for operator evolution and collapse
├── grammars/
│   ├── motif_generator.py    # Builds structured symbolic grammars
│   └── constraint_evaluator.py
├── tests/
│   ├── test_operator_cycles.py
├── data/
│   └── empirical_tests/      # Output data and model comparison snapshots
└── docs/
    └── URCM_Theory.pdf       # Theoretical description of URCM model
```

---

## Installation

Ensure Python 3.8+ and basic scientific libraries (NumPy, Matplotlib) are installed.

```bash
git clone https://github.com/<your-username>/URCM.git
cd URCM
pip install -r requirements.txt
```

---

## Running Simulations

Example: generate 100,000 recursion cycles and visualise operator transitions:

```bash
python urcm_core.py --cycles 100000 --mode symbolic --visualise
```

To test the model against LiteBIRD forecast parameters:

```bash
python tests/test_operator_cycles.py --compare litebird
```

---

## Empirical Context

URCM has been designed with the following datasets and observations in mind:

- Planck 2018 full-mission CMB power spectra
- BICEP2 B-mode polarisation measurements
- LiteBIRD forecast constraints (expected 2030)
- Baryon acoustic oscillations and Type Ia supernovae reconstructions

---

## Documentation

Full model description and working draft preprint can be found in:

- `docs/URCM_Theory.pdf`
- `docs/EmpiricalAppendix_B.pdf`

Key sections include:

- Chapter 1 — Introduction to Recursive Symbolic Cosmology  
- Chapter 6 — Recursive Entropy Constraints  
- Chapter 9.7 — Empirical Counterpoints: BICEP2, LiteBIRD  
- Appendix B — Model Comparison Tables  

---

## Contributing

Researchers, coders, and critics are welcome. See `CONTRIBUTING.md` for:

- Coding and simulation guidelines  
- Protocol for motif or operator proposals  
- Empirical falsifiability rules  

---

## License

MIT License. See `LICENSE.md` for terms.

---

> “If this framework is correct, the universe doesn’t waste — it remembers, cycles, and evolves by recursion, not chance.”
