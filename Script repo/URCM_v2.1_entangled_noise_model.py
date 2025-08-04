import numpy as np
from qutip import *
import matplotlib.pyplot as plt

# Parameters
timesteps = 200
gamma = 0.05  # decoherence rate
noise_type = 'dephasing'  # can switch to 'amplitude'

def entangle_and_noise_step(rho):
    # Entangling unitary (CNOT followed by rotation)
    H = hadamard_transform(1)
    U_ent = cnot(N=2, control=0, target=1)
    R = rx(np.pi / 4)
    U = tensor(R, identity(2)) * U_ent

    rho = U * rho * U.dag()

    # Apply noise to each qubit
    if noise_type == 'dephasing':
        E0 = np.sqrt(1 - gamma) * qeye(2)
        E1 = np.sqrt(gamma) * sigmaz()
    elif noise_type == 'amplitude':
        E0 = Qobj([[1, 0], [0, np.sqrt(1 - gamma)]])
        E1 = Qobj([[0, np.sqrt(gamma)], [0, 0]])
    else:
        raise ValueError("Unknown noise type")

    E = [E0, E1]
    rho = apply_channel(rho, E, targets=[0])
    rho = apply_channel(rho, E, targets=[1])
    return rho

def apply_channel(rho, E_ops, targets):
    for t in targets:
        rho_new = 0
        for E in E_ops:
            op = gate_expand_1toN(E, 2, t)
            rho_new += op * rho * op.dag()
        rho = rho_new
    return rho

# Initial state: Bell state
psi0 = (tensor(basis(2,0), basis(2,0)) + tensor(basis(2,1), basis(2,1))).unit()
rho0 = ket2dm(psi0)
rho = rho0

fidelities = []
entropies = []

for t in range(timesteps):
    fidelity = fidelity(rho0, rho)
    fidelities.append(fidelity)
    entropies.append(entropy_vn(rho))

    rho = entangle_and_noise_step(rho)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(fidelities, label='Fidelity Decay')
plt.plot(entropies, label='Entropy Growth')
plt.xlabel("Timestep")
plt.ylabel("Value")
plt.legend()
plt.title("Fidelity and Entropy over Entangled Evolution with Noise")
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/entanglement_fidelity_entropy_plot.png")