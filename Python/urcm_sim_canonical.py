# urcm_sim_canonical.py – URCM OSequence Simulation with Canonical PNRC Fix
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from abc import ABC, abstractmethod

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
        state['time_factor'] = 1.0
        state['direction'] = 1
        state['log'].append((cycle, self.symbol, "State reinitialised"))
        return state

class BounceTriggerOperator(URCMOperator):
    def __init__(self):
        super().__init__("B̂′", "trigger")

    def execute(self, state, cycle):
        entropy = state.get('entropy', 0.0)
        if entropy < 0.05:
            state['direction'] *= -1
            state['log'].append((cycle, self.symbol, "Bounce triggered"))
        return state

class TimeModulatorOperator(URCMOperator):
    def __init__(self):
        super().__init__("T̂ᵐ′", "modulator")

    def execute(self, state, cycle):
        state['time_factor'] *= 1.1
        state['log'].append((cycle, self.symbol, "Time factor modulated"))
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
    def __init__(self, wrapped_operator: URCMOperator):
        super().__init__(f"Ĉ_fix ∘ {wrapped_operator.symbol}", f"wrapped_{wrapped_operator.op_type}")
        self.wrapped_operator = wrapped_operator

    def execute(self, state, cycle):
        state['time_factor'] = max(1.0, state.get('time_factor', 1.0))
        state['direction'] = state.get('direction', 1)
        state['log'].append((cycle, "Ĉ_fix (pre)", f"Before {self.wrapped_operator.symbol}"))
        state = self.wrapped_operator.execute(state, cycle)
        state['log'].append((cycle, "Ĉ_fix (post)", f"After {self.wrapped_operator.symbol}"))
        return state

class URCMSimulationCanonicalPNRC(ABC):
    def __init__(self, operator_stack, max_cycles=40, entropy_seed=1.2, boundary_signal=0.75):
        self.stack = operator_stack
        self.max_cycles = max_cycles
        self.pnrc_window = deque()
        self.pnrc = 0.0
        self.state = {
            'time_factor': 1.0,
            'direction': 1,
            'entropy': entropy_seed,
            'boundary_signal': boundary_signal,
            'log': []
        }

    def run(self):
        metrics = []
        for cycle in range(self.max_cycles):
            entropy = self.state['entropy']
            n_window = 6 if entropy < 0.1 else 12 if entropy > 0.9 else 8
            weight = 0.1

            if cycle % 6 == 0 and cycle != 0:
                self.state['direction'] *= -1
                self.state['log'].append((cycle, "Bounce", "Direction flipped"))

            if cycle % 5 == 0 and cycle > 0:
                self.state['entropy'] *= 0.92
                self.state['log'].append((cycle, "Compression", "Entropy compressed"))

            if self.state['entropy'] < 0.01:
                self.state['entropy'] = np.random.uniform(0.3, 0.6)
                self.state['log'].append((cycle, "Reseed", f"Entropy reseeded to {self.state['entropy']:.3f}"))

            if any("P̂′" in op.symbol for op in self.stack):
                self.pnrc_window.append(self.state['direction'] * weight)
                if len(self.pnrc_window) > n_window:
                    self.pnrc_window.popleft()
                window_array = np.array(self.pnrc_window)
                self.pnrc = float(np.sum(window_array - np.mean(window_array)))
            else:
                self.pnrc = 0.0

            tf = self.state['time_factor']
            bs = self.state['boundary_signal']
            delta_Cl2 = (np.sin(cycle / 3.0) * tf) ** 2
            Se = -1.2 * np.log(max(tf, 1e-6))
            rac = abs(bs - tf)

            metrics.append({
                'cycle': cycle,
                'ΔCℓ²': delta_Cl2,
                'Sₑ': Se,
                'PNRC': self.pnrc,
                'RAC': rac
            })

            for op in self.stack:
                self.state = op.execute(self.state, cycle)

        return self.state, metrics

def build_urcm_OSequence_stack():
    return [
        FixWrapped(BounceTriggerOperator()),
        FixWrapped(TimeModulatorOperator()),
        FixWrapped(ReinitialiserOperator()),
        FixWrapped(ProjectorOperator()),
        FixWrapped(NullOperator())
    ]

def main():
    stack = build_urcm_OSequence_stack()
    sim = URCMSimulationCanonicalPNRC(stack)
    final_state, metrics = sim.run()
    df_metrics = pd.DataFrame(metrics)
    sine_wave = np.sin(np.linspace(0, 2 * np.pi, len(df_metrics)))
    fidelity = 1 - np.abs(sine_wave - df_metrics['Sₑ'])
    x = df_metrics['cycle']

    plt.figure(figsize=(12, 6))
    plt.plot(x, df_metrics['ΔCℓ²'], label='ΔCℓ²')
    plt.plot(x, df_metrics['Sₑ'], label='Sₑ')
    plt.plot(x, df_metrics['PNRC'], label='PNRC (zero-centered)')
    plt.plot(x, df_metrics['RAC'], label='RAC')
    plt.plot(x, sine_wave, label='Information-Free Sine', linestyle='dotted', color='gray')
    plt.title('URCM Canonical PNRC Evolution')
    plt.xlabel('Cycle')
    plt.ylabel('Metric Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 5))
    plt.plot(x, sine_wave, label='Information-Free Sine', linestyle='dotted', color='gray')
    plt.plot(x, df_metrics['Sₑ'], label='Entropy Sₑ', color='blue')
    plt.plot(x, fidelity, label='Fidelity', color='green')
    plt.title('Entropy and Fidelity (Canonical PNRC)')
    plt.xlabel('Cycle')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
