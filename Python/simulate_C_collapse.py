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

def simulate_collapse():
    n_universes = 50
    cycles = 20
    data = []

    for _ in range(n_universes):
        rho = np.eye(4) / 4
        series = []
        for t in range(cycles):
            if np.random.rand() < 0.1:
                k = np.random.choice([0, 1])
                proj = np.zeros((4, 4))
                proj[k, k] = 1
                rho = proj @ rho @ proj
                rho /= np.trace(rho)
            else:
                U = unitary_random(4)
                rho = U @ rho @ U.conj().T
            series.append(entropy(rho))
        data.append(series)

    data = np.array(data)
    plt.figure()
    for i in range(len(data)):
        plt.plot(data[i], alpha=0.3)
    plt.xlabel("Cycle")
    plt.ylabel("Entropy")
    plt.title("Stochastic Collapse Trajectories (Operator C)")
    plt.savefig("overlay_entropy_50_universes.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    simulate_collapse()
