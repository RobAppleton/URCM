# =============================================================================
# URCM OSEQUENCE SIMULATION (Resilient v2: Entropy Bounce Fix)
# -----------------------------------------------------------------------------
# • Entropy reseed preserves time_factor unless critical collapse (< 0.1)
# • Initial time_factor set to 1.2 so entropy starts > 0
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from abc import ABC, abstractmethod

max_cycles = 1000
entropy_seed = np.random.beta(2, 5) * 2
boundary_signal = 0.75

class URCMOperator(ABC):
    def __init__(self, symbol: str, op_type: str, conditions=None):
        self.symbol = symbol
        self.op_type = op_type
        self.conditions = conditions or {}

    @abstractmethod
    def execute(self, state, cycle):
        pass

class ReinitialiserOperator(URCMOperator):
    def __init__(self):
        super().__init__("R̂′", "reset")

    def execute(self, state, cycle):
        state['entropy'] = np.random.uniform(0.8, 1.2)
        if state['entropy'] < 0.1:
            state['time_factor'] = 1.2  # only reset time_factor if critically collapsed
        state['direction'] = 1
        state['log'].append((cycle, self.symbol, f"Entropy reseeded to {state['entropy']:.3f}"))
        return state

class BounceTriggerOperator(URCMOperator):
    def __init__(self):
        super().__init__("B̂′", "trigger")

    def execute(self, state, cycle):
        if state.get('entropy', 0.0) < 0.05:
            state['direction'] *= -1
            state['log'].append((cycle, self.symbol, "Bounce triggered"))
        return state

class TimeModulatorOperator(URCMOperator):
    def __init__(self):
        super().__init__("T̂ᵐ′", "modulator")

    def execute(self, state, cycle):
        if state.get('entropy', 0.0) < 1.0:
            state['time_factor'] *= 1.25
            state['log'].append((cycle, self.symbol, "Time modulated upward"))
        return state

class ProjectorOperator(URCMOperator):
    def __init__(self):
        super().__init__("P̂′", "projector")

    def execute(self, state, cycle):
        state['log'].append((cycle, self.symbol, "State projected"))
        return state

class NullOperator(URCMOperator):
    def __init__(self):
        super().__init__("NULL_OP", "null")

    def execute(self, state, cycle):
        state['log'].append((cycle, self.symbol, "No-op"))
        return state

class FixWrapped(URCMOperator):
    def __init__(self, wrapped_operator):
        super().__init__(f"Ĉ_fix ∘ {wrapped_operator.symbol}", wrapped_operator.op_type)
        self.wrapped_operator = wrapped_operator

    def execute(self, state, cycle):
        state = self.wrapped_operator.execute(state, cycle)
        state['time_factor'] = max(1.0, state.get('time_factor', 1.0))
        state['direction'] = state.get('direction', 1)
        state['log'].append((cycle, "Ĉ_fix", f"Boundary enforced"))
        return state

def build_urcm_OSequence_stack():
    return [
        FixWrapped(BounceTriggerOperator()),
        FixWrapped(TimeModulatorOperator()),
        FixWrapped(ReinitialiserOperator()),
        FixWrapped(ProjectorOperator()),
        FixWrapped(NullOperator())
    ]

class URCMSimulation:
    def __init__(self, operator_stack):
        self.stack = operator_stack
        self.max_cycles = max_cycles
        self.pnrc = 0.0
        self.state = {
            'time_factor': 1.2,  # Start with entropy > 0
            'direction': 1,
            'entropy': entropy_seed,
            'boundary_signal': boundary_signal,
            'log': []
        }

    def run(self):
        metrics = []
        prev_entropy = self.state['entropy']

        for cycle in range(self.max_cycles):
            tf = self.state['time_factor']
            entropy = self.state['entropy']
            bs = self.state['boundary_signal']

            if cycle % 5 == 0 and cycle != 0:
                self.state['direction'] *= -1
            if cycle % 7 == 0 and cycle > 0:
                self.state['entropy'] *= 0.96
            if self.state['entropy'] < 0.01:
                for op in self.stack:
                    if "R̂′" in op.symbol:
                        self.state = op.execute(self.state, cycle)

            delta_Cl2 = (np.sin(cycle / 3.0) * tf) ** 2
            Se = -1.2 * np.log(max(tf, 1e-6))
            delta_Se = Se - (-1.2 * np.log(max(prev_entropy, 1e-6)))
            prev_entropy = tf
            rac = abs(bs - tf)

            dir_raw = self.state['direction'] * 0.1
            self.pnrc = dir_raw * self.state['entropy']

            metrics.append({
                'cycle': cycle,
                'ΔCℓ²': delta_Cl2,
                'Sₑ': Se,
                'ΔSₑ': delta_Se,
                'PNRC': self.pnrc,
                'RAC': rac,
                'Ĉ_fix': 1
            })

            for op in self.stack:
                self.state = op.execute(self.state, cycle)

        return pd.DataFrame(metrics)

def main():
    sim = URCMSimulation(build_urcm_OSequence_stack())
    df = sim.run()
    sine_wave = np.sin(np.linspace(0, 2 * np.pi, len(df)))
    fidelity = 1 - np.abs(sine_wave - df['Sₑ'])
    x = df['cycle']

    plt.figure(figsize=(12, 6))
    plt.plot(x, df['ΔCℓ²'], label='ΔCℓ²')
    plt.plot(x, df['Sₑ'], label='Sₑ')
    plt.plot(x, df['PNRC'], label='PNRC (Entropy-Weighted)')
    plt.plot(x, df['RAC'], label='RAC')
    plt.plot(x, sine_wave, label='Sine', linestyle='dotted', color='gray')
    plt.title('URCM Core Metrics – Resilient v2 (1000 Cycles)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 5))
    plt.plot(x, sine_wave, label='Sine', linestyle='dotted', color='gray')
    plt.plot(x, df['Sₑ'], label='Entropy Sₑ', color='blue')
    plt.plot(x, fidelity, label='Fidelity', color='green')
    plt.title('Entropy and Fidelity – Resilient v2')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
