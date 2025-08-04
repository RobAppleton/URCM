
"""
URCM Theme Scanner

This Python script scans all `.py` files in a specified directory for recurring conceptual themes specific to the Universal Recursive Causal Model (URCM) theory.
It is entirely self-contained and identifies patterns such as von Neumann entropy calculations, random unitary operators, entropy modulation, and core URCM operator structures.

The script is intended to assist in large-scale codebase analysis to find coherence and common motifs in URCM research implementations.
"""

import os
import ast
from collections import defaultdict
import re
import pandas as pd

# Define regex patterns for URCM-related themes
THEMATIC_PATTERNS = {
    # Detects von Neumann entropy references or its core expression
    "von_Neumann_entropy": re.compile(r"von\s*Neumann\s*entropy|S\s*=\s*-?Tr", re.IGNORECASE),

    # Flags any use of random unitary matrices, including Haar measures
    "random_unitary": re.compile(r"random\s*unitary|unitary_matrix|haar\s*measure", re.IGNORECASE),

    # Searches for recursive operator code tokens used in URCM (e.g., \u2116-encoded or LaTeX-like)
    "recursive_operator": re.compile(r"\bR_hat\b|\bT_hat\b|\bB_hat\b|\brecursive_operator", re.IGNORECASE),

    # Captures entropy modulation operator mentions (Sₑ) and variants
    "entropy_modulation": re.compile(r"S_e\b|entropy\s*modulat", re.IGNORECASE),

    # Flags predictive anomaly structures: Phase Noise Recursion Code (PNRC), Recursive Action Code (RAC), delta-Cℓ²
    "operator_action_signature": re.compile(r"PNRC|RAC|DeltaC", re.IGNORECASE)
}


def extract_code_features(file_content):
    """
    Scans a Python file’s content and returns all URCM theme matches by line number.
    """
    matches = defaultdict(list)
    for theme, pattern in THEMATIC_PATTERNS.items():
        for line_num, line in enumerate(file_content.splitlines(), start=1):
            if pattern.search(line):
                matches[theme].append((line_num, line.strip()))
    return matches


def analyze_python_scripts(directory):
    """
    Scans every .py file in the directory, applies URCM theme extraction, and aggregates results.
    """
    analysis_results = {}
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    features = extract_code_features(content)
                    if features:
                        analysis_results[filename] = features
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return analysis_results

# Example usage:
# directory = '/mnt/data/urcm_scripts'
# results = analyze_python_scripts(directory)

# Optional: convert results into a displayable DataFrame
# summary = []
# for script, themes in results.items():
#     for theme, occurrences in themes.items():
#         summary.append({
#             "Script": script,
#             "Theme": theme,
#             "Occurrences": len(occurrences),
#             "Example Line": occurrences[0][1] if occurrences else ""
#         })

# df_summary = pd.DataFrame(summary)
# df_summary.to_csv("urcm_theme_summary.csv", index=False)
