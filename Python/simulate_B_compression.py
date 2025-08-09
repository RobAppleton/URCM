import numpy as np
import matplotlib.pyplot as plt

def partial_trace(rho, keep, dims):
    reshaped = rho.reshape([dims[0], dims[1], dims[0], dims[1]])
    traced = np.trace(reshaped, axis1=1, axis2=3)
    return traced

def entropy(rho):
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 1e-12]
    return -np.sum(eigvals * np.log2(eigvals))

def simulate():
    d = 4
    psi = np.random.randn(d) + 1j * np.random.randn(d)
    psi = psi / np.linalg.norm(psi)
    rho = np.outer(psi, psi.conj())

    entropies = []
    for _ in range(20):
        rho = np.kron(rho, rho)
        rho = partial_trace(rho, keep=0, dims=[2, 2])
        rho = rho / np.trace(rho)
        entropies.append(entropy(rho))

    plt.figure()
    plt.plot(entropies, label="Entropy after compression")
    plt.xlabel("Cycle")
    plt.ylabel("Von Neumann Entropy")
    plt.title("Entropy Compression Over Recursive Cycles (Operator B)")
    plt.legend()
    plt.grid(True)
    plt.savefig("entropy_bounce_extended.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    simulate()
