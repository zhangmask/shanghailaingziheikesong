from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patches


plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


ROOT = Path(r"d:\Desktop\laingzimuxi")
FIG_DIR = ROOT / "tijiao" / "figures"
ANALYSIS_DIR = ROOT / "tijiao" / "results" / "exp37_analysis"
EXP13_SUMMARY = ROOT / "气象海洋" / "shiyan" / "formula_results_fetch" / "downloaded_results" / "exp13" / "summary.json"
EXP17_SUMMARY = ROOT / "气象海洋" / "shiyan" / "formula_results_fetch" / "downloaded_results" / "exp17" / "summary.json"
EXP10_SUMMARY = ROOT / "气象海洋" / "shiyan" / "formula_results_fetch" / "downloaded_results" / "exp10" / "summary.json"


def load_best_value(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))["best_test"]


def load_exp37_merged() -> pd.DataFrame:
    truth = pd.read_csv(ANALYSIS_DIR / "lorenz96_test_1.csv")
    best = pd.read_csv(ANALYSIS_DIR / "exp37_result.csv").rename(columns={"predicted_value": "pred_best"})
    fixed = pd.read_csv(ANALYSIS_DIR / "exp37_test_fixed.csv").rename(columns={"predicted_value": "pred_fixed"})
    merged = truth.merge(best, on=["time_step", "dimension"], how="inner").merge(
        fixed, on=["time_step", "dimension"], how="inner"
    )
    merged["err_best"] = merged["pred_best"] - merged["true_value"]
    merged["err_fixed"] = merged["pred_fixed"] - merged["true_value"]
    merged["gain_abs_err"] = merged["err_fixed"].abs() - merged["err_best"].abs()
    return merged


def make_gate(ax: plt.Axes, x: float, y: float, text: str, fc: str = "#eef2ff", ec: str = "#334155") -> None:
    rect = patches.FancyBboxPatch(
        (x - 0.24, y - 0.18),
        0.48,
        0.36,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.2,
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=9)


def save_quantum_circuit_schematic() -> None:
    fig, ax = plt.subplots(figsize=(13, 5.5))
    ax.set_xlim(0, 10.8)
    ax.set_ylim(-0.8, 4.6)
    ax.axis("off")

    ys = [3.5, 2.5, 1.5, 0.5]
    for q, y in enumerate(ys):
        ax.plot([0.2, 10.4], [y, y], color="#475569", linewidth=1.6)
        ax.text(0.05, y, f"q{q}", ha="right", va="center", fontsize=10, fontweight="bold")

    # 第一层编码
    for idx, y in enumerate(ys):
        make_gate(ax, 1.0, y, "H", "#e0f2fe")
        make_gate(ax, 2.0, y, f"Ry(x{idx})", "#dcfce7")
        make_gate(ax, 3.2, y, "Rz(0.5x²)", "#fef3c7")

    # 邻接纠缠
    ent_x = 5.0
    for upper, lower in [(ys[0], ys[1]), (ys[1], ys[2]), (ys[2], ys[3])]:
        ax.plot([ent_x, ent_x], [lower, upper], color="#7c3aed", linewidth=1.6)
        ax.scatter([ent_x, ent_x], [upper, lower], s=36, color="#7c3aed")
    make_gate(ax, 5.8, ys[0], "Rz(0.35xixj)", "#fae8ff")
    make_gate(ax, 5.8, ys[1], "Rz(0.35xixj)", "#fae8ff")
    make_gate(ax, 5.8, ys[2], "Rz(0.35xixj)", "#fae8ff")
    make_gate(ax, 6.9, ys[0], "Ry(0.15sum)", "#fee2e2")
    make_gate(ax, 6.9, ys[1], "Ry(0.15sum)", "#fee2e2")
    make_gate(ax, 6.9, ys[2], "Ry(0.15sum)", "#fee2e2")

    # 第二层单比特调整
    for idx, y in enumerate(ys):
        make_gate(ax, 8.2, y, "Ry(0.5x)", "#dcfce7")
        make_gate(ax, 9.3, y, "Rz(0.25x)", "#fef3c7")

    ax.text(5.3, 4.15, "exp37 的 4-qubit 量子特征映射电路示意", ha="center", fontsize=13, fontweight="bold")
    ax.text(
        5.3,
        -0.25,
        "说明：先做单比特特征编码，再做相邻量子比特纠缠，最后用态重叠 |<psi_state|psi_obs>|^2 计算量子相似度。",
        ha="center",
        fontsize=10,
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_quantum_circuit_schematic.png", dpi=220)
    plt.close(fig)


def add_box(ax: plt.Axes, x: float, y: float, w: float, h: float, text: str, color: str) -> None:
    box = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor=color,
        edgecolor="#334155",
        linewidth=1.1,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5)


def arrow(ax: plt.Axes, x1: float, y1: float, x2: float, y2: float) -> None:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", linewidth=1.6, color="#334155"))


def save_method_flowchart() -> None:
    fig, ax = plt.subplots(figsize=(13, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(ax, 0.04, 0.68, 0.18, 0.16, "比赛数据 CSV\ntrue_value / observed_value", "#eff6ff")
    add_box(ax, 0.28, 0.68, 0.18, 0.16, "Lorenz96 + RK4\n集合预测", "#ecfccb")
    add_box(ax, 0.52, 0.68, 0.18, 0.16, "局部窗口提取\ncyclic_window", "#fef3c7")
    add_box(ax, 0.76, 0.68, 0.18, 0.16, "4-qubit 特征映射\nStatevector 相似度", "#fae8ff")

    add_box(ax, 0.20, 0.33, 0.18, 0.16, "rho 权重\n主导观测参与", "#fde68a")
    add_box(ax, 0.43, 0.33, 0.18, 0.16, "J 修正\n弱几何方向修正", "#fecaca")
    add_box(ax, 0.66, 0.33, 0.18, 0.16, "LETKF 更新\n集合子空间分析", "#e2e8f0")
    add_box(ax, 0.42, 0.06, 0.18, 0.16, "result.csv / summary.json\nRMSE 输出", "#dcfce7")

    arrow(ax, 0.22, 0.76, 0.28, 0.76)
    arrow(ax, 0.46, 0.76, 0.52, 0.76)
    arrow(ax, 0.70, 0.76, 0.76, 0.76)
    arrow(ax, 0.85, 0.68, 0.73, 0.49)
    arrow(ax, 0.79, 0.68, 0.56, 0.49)
    arrow(ax, 0.61, 0.68, 0.29, 0.49)
    arrow(ax, 0.38, 0.41, 0.43, 0.41)
    arrow(ax, 0.61, 0.41, 0.66, 0.41)
    arrow(ax, 0.75, 0.33, 0.55, 0.22)

    ax.text(0.5, 0.93, "exp37 完整方法流程图", ha="center", va="center", fontsize=14, fontweight="bold")
    ax.text(
        0.5,
        0.01,
        "关键逻辑：经典 LETKF 是主骨架，量子模块先给 rho 提供结构化相似度，再以弱强度 J 修正集合扰动方向。",
        ha="center",
        va="bottom",
        fontsize=10,
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_method_flowchart.png", dpi=220)
    plt.close(fig)


def save_ablation_logic() -> None:
    exp13 = load_best_value(EXP13_SUMMARY)
    exp17 = load_best_value(EXP17_SUMMARY)
    exp10 = load_best_value(EXP10_SUMMARY)
    rows = [
        ("fixed", 0.12872791254901936, "经典 LETKF"),
        ("rho", exp13["test_1_rmse"], "量子局地化"),
        ("rho + J", 0.12698476904637393, "当前最优"),
        ("rho + adaptive_B", 0.1272579609227456, "次优融合"),
        ("rho + inflation", 0.1272991073509104, "弱有效"),
        ("B only", exp17["test_1_rmse"], "量子 B 修正"),
        ("R only", exp10["test_1_rmse"], "结构化 R"),
    ]
    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]
    notes = [r[2] for r in rows]

    fig, ax = plt.subplots(figsize=(12, 5.4))
    colors = ["#94a3b8", "#60a5fa", "#2563eb", "#38bdf8", "#7dd3fc", "#f59e0b", "#fbbf24"]
    bars = ax.bar(labels, values, color=colors)
    best = min(values)
    ax.axhline(best, color="#1d4ed8", linestyle="--", linewidth=1.2, alpha=0.8)
    for bar, v, note in zip(bars, values, notes):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.00009, f"{v:.6f}\n{note}", ha="center", va="bottom", fontsize=8.8)
    ax.set_title("量子增强方案消融逻辑图：从固定基线到多种融合")
    ax.set_ylabel("test_1 RMSE")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "quantum_ablation_logic.png", dpi=220)
    plt.close(fig)


def save_residual_distribution(merged: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 5))
    bins = np.linspace(
        float(min(merged["err_fixed"].min(), merged["err_best"].min())),
        float(max(merged["err_fixed"].max(), merged["err_best"].max())),
        60,
    )
    ax.hist(merged["err_fixed"], bins=bins, density=True, alpha=0.55, color="#c44e52", label="fixed residual")
    ax.hist(merged["err_best"], bins=bins, density=True, alpha=0.55, color="#4c72b0", label="exp37 residual")
    ax.axvline(float(merged["err_fixed"].mean()), color="#c44e52", linestyle="--", linewidth=1.5)
    ax.axvline(float(merged["err_best"].mean()), color="#4c72b0", linestyle="--", linewidth=1.5)
    ax.set_title("残差分布对比：exp37 vs fixed")
    ax.set_xlabel("Residual = prediction - truth")
    ax.set_ylabel("Density")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_residual_distribution.png", dpi=220)
    plt.close(fig)


def save_bias_variance_analysis(merged: pd.DataFrame) -> None:
    stat = (
        merged.groupby("dimension")
        .apply(
            lambda g: pd.Series(
                {
                    "bias_fixed": float(g["err_fixed"].mean()),
                    "bias_best": float(g["err_best"].mean()),
                    "std_fixed": float(g["err_fixed"].std(ddof=0)),
                    "std_best": float(g["err_best"].std(ddof=0)),
                }
            )
        )
        .reset_index()
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    axes[0].plot(stat["dimension"], stat["bias_fixed"], color="#c44e52", label="fixed")
    axes[0].plot(stat["dimension"], stat["bias_best"], color="#4c72b0", label="exp37")
    axes[0].axhline(0.0, color="black", linewidth=1)
    axes[0].set_title("分维度偏置分析")
    axes[0].set_xlabel("Dimension")
    axes[0].set_ylabel("Mean residual")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.2)

    axes[1].plot(stat["dimension"], stat["std_fixed"], color="#c44e52", label="fixed")
    axes[1].plot(stat["dimension"], stat["std_best"], color="#4c72b0", label="exp37")
    axes[1].set_title("分维度残差波动分析")
    axes[1].set_xlabel("Dimension")
    axes[1].set_ylabel("Residual std")
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.2)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_bias_variance_analysis.png", dpi=220)
    plt.close(fig)


def save_topk_dimension_gain(merged: pd.DataFrame) -> None:
    dim_gain = merged.groupby("dimension", as_index=False)["gain_abs_err"].mean()
    top = dim_gain.sort_values("gain_abs_err", ascending=False).head(5).assign(group="Top-5 gain")
    bottom = dim_gain.sort_values("gain_abs_err", ascending=True).head(5).assign(group="Top-5 loss")
    data = pd.concat([top, bottom], ignore_index=True)

    fig, ax = plt.subplots(figsize=(11, 4.8))
    colors = ["#2563eb" if g == "Top-5 gain" else "#dc2626" for g in data["group"]]
    labels = [f"d{int(d)}" for d in data["dimension"]]
    ax.bar(labels, data["gain_abs_err"], color=colors)
    ax.axhline(0.0, color="black", linewidth=1)
    for i, v in enumerate(data["gain_abs_err"]):
        ax.text(i, v + (0.0004 if v >= 0 else -0.0007), f"{v:.4f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=8.8)
    ax.set_title("exp37 分维度收益 Top-K 分析")
    ax.set_ylabel("Mean(abs_err_fixed - abs_err_exp37)")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_topk_dimension_gain.png", dpi=220)
    plt.close(fig)


def save_qubit_compliance() -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    circles_x = [0.12, 0.22, 0.32, 0.42]
    for i, x in enumerate(circles_x):
        circ = patches.Circle((x, 0.58), 0.035, facecolor="#93c5fd", edgecolor="#1d4ed8", linewidth=1.5)
        ax.add_patch(circ)
        ax.text(x, 0.58, f"q{i}", ha="center", va="center", fontsize=9)
    ax.text(0.27, 0.72, "实际使用量子比特数：4", ha="center", fontsize=14, fontweight="bold")

    bar_x, bar_y, bar_w, bar_h = 0.58, 0.5, 0.28, 0.12
    rect_bg = patches.FancyBboxPatch((bar_x, bar_y), bar_w, bar_h, boxstyle="round,pad=0.02", facecolor="#e5e7eb", edgecolor="#475569")
    rect_fill = patches.FancyBboxPatch((bar_x, bar_y), bar_w * (4 / 30), bar_h, boxstyle="round,pad=0.02", facecolor="#22c55e", edgecolor="#15803d")
    ax.add_patch(rect_bg)
    ax.add_patch(rect_fill)
    ax.text(bar_x + bar_w / 2, bar_y + bar_h / 2, "4 / 30 qubits", ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(0.72, 0.68, "比赛硬件约束", ha="center", fontsize=13, fontweight="bold")
    ax.text(
        0.5,
        0.22,
        "结论：当前最高分主线统一使用 4-qubit 量子特征映射，\n"
        "单次模拟线路规模远低于 30 qubits，不触碰上限。",
        ha="center",
        va="center",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "quantum_qubit_compliance.png", dpi=220)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    merged = load_exp37_merged()
    save_quantum_circuit_schematic()
    save_method_flowchart()
    save_ablation_logic()
    save_residual_distribution(merged)
    save_bias_variance_analysis(merged)
    save_topk_dimension_gain(merged)
    save_qubit_compliance()
    print("generated submission extra figures")


if __name__ == "__main__":
    main()
