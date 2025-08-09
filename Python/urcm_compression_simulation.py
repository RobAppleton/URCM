
# URCM Simulation: Encode a bulk density matrix into a boundary representation using URCM's compression operator
# ----------------------------------------------------------------------------------------------
# Description:
# This script simulates the compression of a high-dimensional bulk density matrix into a lower-dimensional 
# boundary state. The purpose is to test the information retention and entropy scaling consistent with the 
# holographic principle and URCM's compression operator (Ĉ). This represents one of the fundamental mechanisms 
# in the URCM model where cosmic states are projected from volumetric to boundary representations prior to bounce.

# Simulation Objective:
# Generate a random bulk density matrix (ρ_bulk), apply a compression operator (Ĉ) via partial trace, and
# produce a boundary state (ρ_boundary). We will compute and compare von Neumann entropies and fidelity
# to assess information retention.

import numpy as np
from scipy.linalg import sqrtm, logm
from numpy.linalg import norm

def create_random_density_matrix(dim):
    # Generate a random complex matrix and normalize it into a density matrix
    psi = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    rho = psi @ psi.conj().T
    return rho / np.trace(rho)

def partial_trace(rho, keep_dim, trace_dim):
    # Trace out one subsystem to simulate boundary compression
    dim_total = keep_dim * trace_dim
    rho = rho.reshape((keep_dim, trace_dim, keep_dim, trace_dim))
    return np.trace(rho, axis1=1, axis2=3)

def von_neumann_entropy(rho):
    # Compute von Neumann entropy: S = -Tr(ρ log ρ)
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 0]
    return -np.sum(evals * np.log2(evals))

def fidelity(rho1, rho2):
    # Compute Uhlmann fidelity between two density matrices
    sqrt_rho1 = sqrtm(rho1)
    product = sqrt_rho1 @ rho2 @ sqrt_rho1
    sqrt_product = sqrtm(product)
    return np.real(np.trace(sqrt_product))**2

# Define dimensions for bulk and boundary spaces
bulk_dim = 8   # 8-dimensional bulk system
boundary_dim = 4  # Keep 4 dimensions, trace out other half

# Step 1: Create a random bulk density matrix
rho_bulk = create_random_density_matrix(bulk_dim)

# Step 2: Compress the bulk state into a boundary by tracing out 4 dimensions
rho_boundary = partial_trace(rho_bulk, boundary_dim, boundary_dim)

# Step 3: Evaluate entropy before and after compression
S_bulk = von_neumann_entropy(rho_bulk)
S_boundary = von_neumann_entropy(rho_boundary)

# Step 4: (Optional) Simulate bounce cycle and check fidelity (rho_bulk → Ĉ → bounce → ρ_boundary recovery)
# In this prototype, we only examine compression

print("Entropy of bulk state: {:.4f} bits".format(S_bulk))
print("Entropy of boundary state: {:.4f} bits".format(S_boundary))
print("Information loss (S_bulk - S_boundary): {:.4f} bits".format(S_bulk - S_boundary))

# Note: Fidelity calculation against expected compressed form would require a known inverse or theoretical output
