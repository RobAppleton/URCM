import numpy as np
import pandas as pd
from qutip import *

# Parameters
d = 20  # Hilbert space dimension
cycles = 3  # Number of cycles

# Initial high-entropy state (random mixed state)
def generate_high_entropy_state(d):
    psi_list = [rand_ket(d) for _ in range(20)]
    rho = sum([ket2dm(psi) for psi in psi_list]) / 20
    return rho

# Compression operator: simulate projection to a boundary subspace
def compression_operator(rho):
    proj = Qobj(np.random.rand(d, d))
    proj = proj.unit()
    return (proj * rho * proj.dag()).unit()

# Entropy reset operator: simulate purification to dominant eigenstate
def entropy_reset_operator(rho):
    eigvals, eigvecs = rho.eigenstates()
    purified = eigvecs[0] * eigvecs[0].dag()  # dominant eigenvector
    return purified.unit()

# Bounce operator: simulate with unitary evolution
def bounce_operator(rho):
    H = rand_herm(d)
    U = (-1j * H).expm()
    return (U * rho * U.dag()).unit()

# Simulation loop
entropy_vals = []
memory_vals = []

rho_current = generate_high_entropy_state(d)
rho_prev = rho_current

for cycle in range(cycles):
    rho_boundary = compression_operator(rho_current)
    rho_purified = entropy_reset_operator(rho_boundary)
    rho_next = bounce_operator(rho_purified)

    # Record entropy
    S = entropy_vn(rho_next)
    entropy_vals.append(S)

    # Record fidelity (memory overlap)
    F = fidelity(rho_prev, rho_next)
    memory_vals.append(F)

    rho_prev = rho_current
    rho_current = rho_next

# Output results
df = pd.DataFrame({
    "Cycle": list(range(1, cycles + 1)),
    "Entropy (Sₙ)": entropy_vals,
    "Memory Fidelity (Mₙ)": memory_vals
})

print(df)
