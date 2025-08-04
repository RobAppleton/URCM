# Unified Recursive Cosmological Model (URCM)

**A structural alternative to ΛCDM, grounded in symbolic recursion and operator logic.**

The **Unified Recursive Cosmological Model (URCM)** is a novel approach to cosmology that reinterprets the universe’s origin, evolution, and entropy structure using recursive symbolic operators rather than scalar fields or inflationary dynamics. This repository contains the evolving codebase, simulation frameworks, and formal documentation supporting the development and empirical validation of URCM.

---

## Project Scope

URCM aims to:

- Offer a falsifiable alternative to inflationary cosmology.
- Reconstruct entropy asymmetry from first principles.
- Model cosmological evolution through **recursive operator sequences** (`Ĉ`, `Ŝ`, `T̂`, etc.).
- Simulate cyclic cosmology without scalar inflation or conformal fixes.
- Provide testable predictions distinguishable from ΛCDM, CCC, and LQC.

---

## Key Concepts

| Concept                   | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| **Recursive Operators**  | The universe is built from a self-referential symbolic grammar.             |
| **Entropy as Residue**   | Entropy emerges from recursive constraint dynamics, not arbitrary origins.  |
| **Cyclic Resolution**    | The universe undergoes regenerative loops governed by operator logic.       |
| **Empirical Metrics**    | Designed to engage with Planck, BICEP2, LiteBIRD, and other datasets.       |

---

## Repository Structure

```
📂 urcm/
 ├── urcm_core.py              # Core recursive engine and symbolic evaluator
 ├── operators/
 │    ├── init_operator_set.py  # Defines base symbolic operators (Ĉ, Ŝ, etc.)
 │    ├── transition_rules.py   # Phase-switch and collapse logic
 ├── grammars/
 │    ├── motif_generator.py    # Builds symbolic motif chains
 │    └── constraint_evaluator.py
 ├── tests/
 │    ├── test_operator_cycles.py
 └── data/
      ├── sample_runs/
      └── bicep_litebird_comparisons/
```

---

## Installation

```bash
git clone https://github.com/<your-username>/URCM.git
cd URCM
pip install -r requirements.txt
```

---

## Usage

Run a basic simulation to generate a symbolic universe loop and view operator transitions:

```bash
python urcm_core.py --cycles 100000 --mode symbolic --visualise
```

Or execute a comparative test using empirical metrics:

```bash
python tests/test_operator_cycles.py --compare bicep2 --plot
```

---

## Empirical Anchors

- Planck CMB data  
- BICEP2 polarisation curves  
- LiteBIRD forecasted spectrum  
- BAO and SN1a reconstructions  

---

## Documentation

The full theoretical description is available in `docs/URCM_Theory.pdf`, including:

- **Chapter 1**: Foundations of Symbolic Cosmology  
- **Chapter 6**: Recursive Entropy Constraints  
- **Chapter 9.7**: Engagement with BICEP2 and LiteBIRD  
- **Appendix B**: Comparative Model Metrics  

---

## Contributing

We welcome collaboration, critique, and counterexamples. See `CONTRIBUTING.md` for:

- Coding style and grammar rules  
- Empirical falsification tests  
- How to propose motif libraries  

---

## License

This repository is licensed under the MIT License. See `LICENSE.md` for details.

---

> *“If I am correct, the universe is alive — not in a biological sense, but in how it reuses, recycles, and remembers.”*
