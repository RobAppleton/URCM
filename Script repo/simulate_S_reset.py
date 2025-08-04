import numpy as np
import matplotlib.pyplot as plt

def unitary_random(d):
    Z = np.random.randn(d, d) + 1j * np.random.randn(d, d)
    Q, R = np.linalg.qr(Z)
    return Q

def entropy(rho):
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 1e-12]
    return -np.sum(eigvals * np.log2(eigvals))

def entropy_reset(rho, pure_state):
    return np.outer(pure_state, pure_state.conj())

def simulate():
    d = 8
    rho = np.eye(d) / d
    entropies = []

    for i in range(20):
        S = entropy(rho)
        entropies.append(S)
        if S > 2.0:
            pure = np.zeros(d)
            pure[0] = 1
            rho = entropy_reset(rho, pure)
        else:
            U = unitary_random(d)
            rho = U @ rho @ U.conj().T
            rho = rho / np.trace(rho)

    plt.figure()
    plt.plot(entropies, marker='o')
    plt.xlabel("Cycle")
    plt.ylabel("Entropy")
    plt.title("Noisy Entropy Resets Over Time (Operator S)")
    plt.savefig("page_curve_noisy_simulation_v2.2.2.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    simulate()
