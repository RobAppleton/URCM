
import numpy as np
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    if file_path.endswith('.csv'):
        return np.loadtxt(file_path, delimiter=',')
    elif file_path.endswith('.npy'):
        return np.load(file_path)
    else:
        raise ValueError("Unsupported file format: " + file_path)

def analyze_statistics(data, label=""):
    print(f"--- Analysis for {label} ---")
    print(f"Mean: {np.mean(data):.4f}")
    print(f"Std Dev: {np.std(data):.4f}")
    print(f"Min: {np.min(data):.4f}")
    print(f"Max: {np.max(data):.4f}")
    print(f"Non-zero count: {np.count_nonzero(data)} / {data.size}")
    print()

def plot_distribution(data, title, save_path):
    plt.figure(figsize=(8, 5))
    plt.hist(data.flatten(), bins=50, alpha=0.7, color='navy')
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def main():
    # Paths to outputs (user must adjust as needed)
    output_files = {
        "Fidelity Decay": "fidelity_decay_output.npy",
        "Dispersion Heatmap": "fidelity_dispersion_heatmap_output.npy",
        "Recursive Stabilization": "recursive_stabilization_output.npy",
        "Directional Entropy Flow": "directional_entropy_flow_output.npy"
    }

    for label, file_path in output_files.items():
        if os.path.exists(file_path):
            data = load_data(file_path)
            analyze_statistics(data, label)
            plot_distribution(data, f"{label} Distribution", f"{label.replace(' ', '_').lower()}_distribution.png")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()
