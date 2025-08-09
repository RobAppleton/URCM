
import numpy as np
import matplotlib.pyplot as plt

def simulate_entropy_flow(operator_order, num_cycles=30, initial_entropy=0.1):
    entropy = [initial_entropy]
    current_entropy = initial_entropy

    for cycle in range(num_cycles):
        for op in operator_order:
            if op == 'B':
                current_entropy *= 0.95
            elif op == 'C':
                current_entropy += 0.05
            elif op == 'S':
                current_entropy += np.random.uniform(0.01, 0.03)
        current_entropy = min(current_entropy, 1.0)
        entropy.append(current_entropy)

    return entropy

order_forward = ['B', 'C', 'S']
order_reverse = ['S', 'C', 'B']

entropy_forward = simulate_entropy_flow(order_forward)
entropy_reverse = simulate_entropy_flow(order_reverse)

plt.figure()
plt.plot(entropy_forward, label="B → C → S", marker='o')
plt.plot(entropy_reverse, label="S → C → B", marker='x')
plt.title("Entropy Flow Under Different Operator Orders")
plt.xlabel("Cycle")
plt.ylabel("Entropy")
plt.legend()
plt.grid(True)
plt.savefig("entropy_flow_operator_order.png")
plt.show()
