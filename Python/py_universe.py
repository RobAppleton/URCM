# py_universe.py

import simulate_B_compression as B
import simulate_C_collapse as C
import simulate_S_reset as S
import pandas as pd

# Run each simulation and collect results
results = []
for label, module in [('B', B), ('C', C), ('S', S)]:
    data = module.run_simulation()
    # Expect data to be a DataFrame with columns ['step', 'fidelity', 'entropy']
    data['channel'] = label
    results.append(data)

# Concatenate all results
df = pd.concat(results, ignore_index=True)

# Save combined results for later analysis
df.to_csv('combined_decoherence_results.csv', index=False)

# Quick summary
print(df.groupby('channel')[['fidelity', 'entropy']].mean())
