from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

if plt is not None:
    plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "气象海洋" / "小规模测试"
OUTPUT_DIR = ROOT / "exp3_quantum_kernel_outputs"
REMOTE_INPUT = Path("/home/infra/qda_competition/data/lorenz96_train.csv")
REMOTE_OUTPUT = Path("/home/infra/qda_competition/experiments/quantum_kernel_structure")

N_QUBITS = 4
WINDOW_SIZE = 4
SAMPLE_TIMES = [0, 500, 998]
SAMPLE_CENTERS = [0, 10, 20, 30]
FEATURE_SCALE = np.pi / 2.0


@dataclass
class KernelSample:
    time_step: int
    center: int
    feature: np.ndarray
    label: str


def load_competition_csv(path: Path) -> tuple[np.ndarray, np.ndarray]:
    rows: list[tuple[int, int, float, float]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                (
                    int(row["time_step"]),
                    int(row["dimension"]),
                    float(row["true_value"]),
                    float(row["observed_value"]),
                )
            )

    max_t = max(row[0] for row in rows)
    max_d = max(row[1] for row in rows)
    truth = np.full((max_t + 1, max_d + 1), np.nan, dtype=float)
    obs = np.full((max_t + 1, max_d + 1), np.nan, dtype=float)
    for t, d, true_value, observed_value in rows:
        truth[t, d] = true_value
        obs[t, d] = observed_value
    return obs, truth


def cyclic_window(vec: np.ndarray, center: int, width: int) -> np.ndarray:
    n = len(vec)
    offsets = range(-(width // 2), -(width // 2) + width)
    return np.array([vec[(center + off) % n] for off in offsets], dtype=float)


def build_samples(obs: np.ndarray) -> list[KernelSample]:
    samples: list[KernelSample] = []
    for time_step in SAMPLE_TIMES:
        frame = np.nan_to_num(obs[time_step], nan=0.0)
        for center in SAMPLE_CENTERS:
            feature = cyclic_window(frame, center=center, width=WINDOW_SIZE)
            label = f"t{time_step}_c{center}"
            samples.append(KernelSample(time_step=time_step, center=center, feature=feature, label=label))
    return samples


def standardize_features(samples: list[KernelSample]) -> np.ndarray:
    raw = np.stack([sample.feature for sample in samples], axis=0)
    mean = raw.mean(axis=0, keepdims=True)
    std = raw.std(axis=0, keepdims=True) + 1e-8
    z = (raw - mean) / std
    return FEATURE_SCALE * np.tanh(z)


def build_feature_map(feature: np.ndarray) -> QuantumCircuit:
    qc = QuantumCircuit(N_QUBITS)
    for q, value in enumerate(feature):
        qc.h(q)
        qc.ry(float(value), q)
        qc.rz(float(0.5 * value * value), q)

    for q in range(N_QUBITS - 1):
        angle = float(0.35 * feature[q] * feature[q + 1])
        qc.cz(q, q + 1)
        qc.rz(angle, q + 1)
        qc.ry(float(0.15 * (feature[q] + feature[q + 1])), q)

    for q, value in enumerate(feature):
        qc.ry(float(0.5 * value), q)
        qc.rz(float(0.25 * value), q)
    return qc


def quantum_kernel_matrix(features: np.ndarray) -> np.ndarray:
    states = [Statevector.from_instruction(build_feature_map(feature)) for feature in features]
    n = len(states)
    kernel = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            overlap = np.vdot(states[i].data, states[j].data)
            fidelity = float(np.abs(overlap) ** 2)
            kernel[i, j] = fidelity
            kernel[j, i] = fidelity
    return kernel


def classical_rbf_kernel(features: np.ndarray, gamma: float | None = None) -> np.ndarray:
    if gamma is None:
        gamma = 1.0 / features.shape[1]
    diff = features[:, None, :] - features[None, :, :]
    sq_dist = np.sum(diff * diff, axis=-1)
    return np.exp(-gamma * sq_dist)


def kernel_stats(kernel: np.ndarray) -> dict[str, float]:
    eigvals = np.linalg.eigvalsh(kernel)
    return {
        "min": float(kernel.min()),
        "max": float(kernel.max()),
        "mean": float(kernel.mean()),
        "std": float(kernel.std(ddof=0)),
        "min_eig": float(eigvals.min()),
        "max_eig": float(eigvals.max()),
        "neg_eig_count": int(np.sum(eigvals < -1e-8)),
    }


def time_block_means(kernel: np.ndarray, samples: list[KernelSample]) -> tuple[np.ndarray, list[str]]:
    time_labels = [str(t) for t in SAMPLE_TIMES]
    block = np.zeros((len(SAMPLE_TIMES), len(SAMPLE_TIMES)), dtype=float)
    for i, ti in enumerate(SAMPLE_TIMES):
        idx_i = [k for k, sample in enumerate(samples) if sample.time_step == ti]
        for j, tj in enumerate(SAMPLE_TIMES):
            idx_j = [k for k, sample in enumerate(samples) if sample.time_step == tj]
            block[i, j] = float(kernel[np.ix_(idx_i, idx_j)].mean())
    return block, time_labels


def save_heatmap(matrix: np.ndarray, labels: list[str], out_path: Path, title: str) -> None:
    if plt is None:
        return
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
    if plt is None:
        return
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
    if plt is None:
        return
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


def save_matrix_csv(matrix: np.ndarray, labels: list[str], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label", *labels])
        for label, row in zip(labels, matrix):
            writer.writerow([label, *[f"{value:.12f}" for value in row]])


def build_summary(
    samples: list[KernelSample],
    quantum_kernel: np.ndarray,
    classical_kernel: np.ndarray,
    quantum_block: np.ndarray,
    classical_block: np.ndarray,
) -> dict[str, object]:
    return {
        "config": {
            "n_qubits": N_QUBITS,
            "window_size": WINDOW_SIZE,
            "sample_times": SAMPLE_TIMES,
            "sample_centers": SAMPLE_CENTERS,
            "sample_count": len(samples),
            "plots_generated": plt is not None,
        },
        "sample_labels": [sample.label for sample in samples],
        "quantum_stats": kernel_stats(quantum_kernel),
        "classical_stats": kernel_stats(classical_kernel),
        "quantum_block_means": quantum_block.tolist(),
        "classical_block_means": classical_block.tolist(),
    }


def write_markdown_summary(summary: dict[str, object], out_path: Path) -> None:
    q_stats = summary["quantum_stats"]
    c_stats = summary["classical_stats"]
    lines = [
        "# 实验3量子核结构实验摘要",
        "",
        "## 实验设置",
        "",
        f"- qubits: `{summary['config']['n_qubits']}`",
        f"- 局部窗口长度: `{summary['config']['window_size']}`",
        f"- 时间步: `{summary['config']['sample_times']}`",
        f"- 中心维度: `{summary['config']['sample_centers']}`",
        f"- 样本数: `{summary['config']['sample_count']}`",
        "",
        "## 核矩阵统计",
        "",
        "| kernel | min | max | mean | std | min_eig | neg_eig_count |",
        "|--------|-----|-----|------|-----|---------|---------------|",
        f"| quantum | {q_stats['min']:.6f} | {q_stats['max']:.6f} | {q_stats['mean']:.6f} | {q_stats['std']:.6f} | {q_stats['min_eig']:.6e} | {q_stats['neg_eig_count']} |",
        f"| rbf | {c_stats['min']:.6f} | {c_stats['max']:.6f} | {c_stats['mean']:.6f} | {c_stats['std']:.6f} | {c_stats['min_eig']:.6e} | {c_stats['neg_eig_count']} |",
        "",
        "## 初步判断",
        "",
        "- 若量子核的 `std` 明显大于 0，说明它不是常数矩阵。",
        "- 若 `min_eig` 接近 0 且没有明显负特征值，可认为它近似半正定。",
        "- 若不同时间块均值有差异，说明量子核对局部流型变化有反应。",
        "- 后续是否进入实验 4，需要结合这些结构指标和经典 RBF 对照一起判断。",
        "",
        "## 输出文件",
        "",
        "- `quantum_kernel.csv`",
        "- `rbf_kernel.csv`",
        "- `quantum_time_block.csv`",
        "- `rbf_time_block.csv`",
        "- `quantum_kernel_heatmap.png`",
        "- `rbf_kernel_heatmap.png`",
        "- `kernel_eigen_spectrum.png`",
        "- `time_block_compare.png`",
        "- `summary.json`",
    ]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve_default_input() -> Path:
    local_input = DATA_DIR / "lorenz96_train.csv"
    if local_input.exists():
        return local_input
    return REMOTE_INPUT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="实验3：量子核结构实验")
    parser.add_argument("--input", type=Path, default=resolve_default_input())
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    obs, _truth = load_competition_csv(args.input)
    samples = build_samples(obs)
    features = standardize_features(samples)

    quantum_kernel = quantum_kernel_matrix(features)
    classical_kernel = classical_rbf_kernel(features)
    quantum_block, time_labels = time_block_means(quantum_kernel, samples)
    classical_block, _ = time_block_means(classical_kernel, samples)

    labels = [sample.label for sample in samples]
    save_matrix_csv(quantum_kernel, labels, args.output_dir / "quantum_kernel.csv")
    save_matrix_csv(classical_kernel, labels, args.output_dir / "rbf_kernel.csv")
    save_matrix_csv(quantum_block, time_labels, args.output_dir / "quantum_time_block.csv")
    save_matrix_csv(classical_block, time_labels, args.output_dir / "rbf_time_block.csv")
    save_heatmap(quantum_kernel, labels, args.output_dir / "quantum_kernel_heatmap.png", "Quantum Kernel Heatmap")
    save_heatmap(classical_kernel, labels, args.output_dir / "rbf_kernel_heatmap.png", "RBF Kernel Heatmap")
    save_eigen_plot(quantum_kernel, classical_kernel, args.output_dir / "kernel_eigen_spectrum.png")
    save_block_compare(quantum_block, classical_block, time_labels, args.output_dir / "time_block_compare.png")

    summary = build_summary(samples, quantum_kernel, classical_kernel, quantum_block, classical_block)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_summary(summary, args.output_dir / "summary.md")
    print(f"输出目录: {args.output_dir}")


if __name__ == "__main__":
    main()
