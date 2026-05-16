from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


plt.rcParams["axes.unicode_minus"] = False


def read_matrix_csv(path: Path) -> tuple[list[str], np.ndarray]:
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    labels = rows[0][1:]
    matrix = np.array([[float(x) for x in row[1:]] for row in rows[1:]], dtype=float)
    return labels, matrix


def save_heatmap(matrix: np.ndarray, labels: list[str], out_path: Path, title: str) -> None:
    plt.figure(figsize=(7, 6))
    plt.imshow(matrix, cmap="viridis", aspect="auto")
    plt.colorbar(label="value")
    plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
    plt.yticks(range(len(labels)), labels)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def save_eigen_plot(quantum_kernel: np.ndarray, classical_kernel: np.ndarray, out_path: Path) -> None:
    q_eigs = np.sort(np.linalg.eigvalsh(quantum_kernel))[::-1]
    c_eigs = np.sort(np.linalg.eigvalsh(classical_kernel))[::-1]
    plt.figure(figsize=(7, 4))
    plt.plot(q_eigs, marker="o", linewidth=1.2, label="quantum")
    plt.plot(c_eigs, marker="s", linewidth=1.2, label="rbf")
    plt.xlabel("eigen index")
    plt.ylabel("eigen value")
    plt.title("Kernel Eigen Spectrum")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def save_block_compare(
    quantum_block: np.ndarray,
    classical_block: np.ndarray,
    labels: list[str],
    out_path: Path,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, matrix, title in zip(
        axes,
        [quantum_block, classical_block],
        ["quantum block means", "rbf block means"],
    ):
        im = ax.imshow(matrix, cmap="magma", aspect="auto")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_title(title)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="根据实验3的 CSV 结果补画图")
    parser.add_argument("--input-dir", type=Path, required=True)
    args = parser.parse_args()

    labels, quantum_kernel = read_matrix_csv(args.input_dir / "quantum_kernel.csv")
    _, classical_kernel = read_matrix_csv(args.input_dir / "rbf_kernel.csv")
    time_labels, quantum_block = read_matrix_csv(args.input_dir / "quantum_time_block.csv")
    _, classical_block = read_matrix_csv(args.input_dir / "rbf_time_block.csv")

    save_heatmap(quantum_kernel, labels, args.input_dir / "quantum_kernel_heatmap.png", "Quantum Kernel Heatmap")
    save_heatmap(classical_kernel, labels, args.input_dir / "rbf_kernel_heatmap.png", "RBF Kernel Heatmap")
    save_eigen_plot(quantum_kernel, classical_kernel, args.input_dir / "kernel_eigen_spectrum.png")
    save_block_compare(quantum_block, classical_block, time_labels, args.input_dir / "time_block_compare.png")
    print(f"输出目录: {args.input_dir}")


if __name__ == "__main__":
    main()
