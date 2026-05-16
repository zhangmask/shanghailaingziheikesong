from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["axes.unicode_minus"] = False


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "气象海洋" / "小规模测试"
OUTPUT_DIR = ROOT / "exp2_structure_outputs"

ENS_SIZE = 40
INFL = 1.02
OBS_STD = 0.5
OBS_VAR = OBS_STD**2
DT = 0.05
FORCING = 8.0
SEED = 2
SUPPORT_RADIUS = 20
EPS = 1e-8


@dataclass
class Snapshot:
    time_step: int
    kernel: str
    weight_matrix: np.ndarray
    state_index: int
    weight_curve: np.ndarray


def cyclic_distance(i: int, j: int, n: int) -> int:
    d = abs(i - j)
    return min(d, n - d)


def lorenz96_rhs(x: np.ndarray, forcing: float = FORCING) -> np.ndarray:
    return (np.roll(x, -1) - np.roll(x, 2)) * np.roll(x, 1) - x + forcing


def rk4_step(x: np.ndarray, dt: float = DT, forcing: float = FORCING) -> np.ndarray:
    k1 = lorenz96_rhs(x, forcing)
    k2 = lorenz96_rhs(x + 0.5 * dt * k1, forcing)
    k3 = lorenz96_rhs(x + 0.5 * dt * k2, forcing)
    k4 = lorenz96_rhs(x + dt * k3, forcing)
    return x + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0


def sym_sqrt(mat: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh(mat)
    vals = np.clip(vals, 0.0, None)
    return vecs @ np.diag(np.sqrt(vals)) @ vecs.T


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


def normalize_weights(weights: np.ndarray, min_clip: float = 0.05) -> np.ndarray:
    weights = np.clip(np.asarray(weights, dtype=float), min_clip, None)
    return weights / (weights.mean() + EPS)


def compute_weights(
    kernel: str,
    i: int,
    local_obs_idx: np.ndarray,
    x_pert: np.ndarray,
    y_pert: np.ndarray,
    innovation: np.ndarray,
    nx: int,
    support_radius: int,
) -> np.ndarray:
    if kernel == "fixed":
        return np.ones(len(local_obs_idx), dtype=float)

    state_signal = x_pert[:, i]
    state_std = state_signal.std(ddof=1) + EPS
    obs_std = y_pert.std(axis=0, ddof=1) + EPS
    corr = np.abs(((state_signal[:, None] * y_pert).mean(axis=0)) / (state_std * obs_std))
    corr = np.clip(corr, 0.0, 1.0)

    innov_scale = max(float(np.std(innovation, ddof=0)), math.sqrt(OBS_VAR), 0.25)
    innov_weight = np.exp(-np.abs(innovation) / (innov_scale + EPS))

    dist = np.array([cyclic_distance(i, j, nx) for j in local_obs_idx], dtype=float)
    if support_radius <= 0:
        dist_weight = np.ones_like(dist)
    else:
        sigma = max(support_radius / 2.5, 1.0)
        dist_weight = np.exp(-0.5 * (dist / sigma) ** 2)

    if kernel == "corr":
        return normalize_weights(0.1 + corr)
    if kernel == "innov":
        return normalize_weights(innov_weight)
    if kernel == "hybrid":
        return normalize_weights((0.15 + 0.85 * corr) * innov_weight * dist_weight)
    raise ValueError(f"Unknown kernel: {kernel}")


def collect_weight_matrix(
    ensemble: np.ndarray,
    obs_vec: np.ndarray,
    kernel: str,
    support_radius: int,
) -> np.ndarray:
    nens, nx = ensemble.shape
    weight_matrix = np.zeros((nx, nx), dtype=float)
    x_mean = ensemble.mean(axis=0)
    x_pert = ensemble - x_mean
    obs_idx_all = np.where(~np.isnan(obs_vec))[0]
    if len(obs_idx_all) == 0:
        return weight_matrix

    for i in range(nx):
        local_obs_idx = np.array(
            [j for j in obs_idx_all if cyclic_distance(i, j, nx) <= support_radius],
            dtype=int,
        )
        y_local = obs_vec[local_obs_idx]
        y_ens = ensemble[:, local_obs_idx]
        y_mean = y_ens.mean(axis=0)
        y_pert = y_ens - y_mean
        innovation = y_local - y_mean
        weights = compute_weights(
            kernel=kernel,
            i=i,
            local_obs_idx=local_obs_idx,
            x_pert=x_pert,
            y_pert=y_pert,
            innovation=innovation,
            nx=nx,
            support_radius=support_radius,
        )
        weight_matrix[i, local_obs_idx] = weights
    return weight_matrix


def letkf_update_proxy(
    ensemble: np.ndarray,
    obs_vec: np.ndarray,
    obs_var: float,
    support_radius: int,
    infl: float,
    kernel: str,
) -> tuple[np.ndarray, np.ndarray]:
    nens, nx = ensemble.shape
    ana = np.empty_like(ensemble)

    x_mean = ensemble.mean(axis=0)
    x_pert = ensemble - x_mean
    obs_idx_all = np.where(~np.isnan(obs_vec))[0]
    if len(obs_idx_all) == 0:
        return ensemble.copy(), np.zeros((nx, nx), dtype=float)

    weight_matrix = np.zeros((nx, nx), dtype=float)

    for i in range(nx):
        local_obs_idx = np.array(
            [j for j in obs_idx_all if cyclic_distance(i, j, nx) <= support_radius],
            dtype=int,
        )
        if len(local_obs_idx) == 0:
            ana[:, i] = ensemble[:, i]
            continue

        y_local = obs_vec[local_obs_idx]
        y_ens = ensemble[:, local_obs_idx]
        y_mean = y_ens.mean(axis=0)
        y_pert = y_ens - y_mean
        innovation = y_local - y_mean
        weights = compute_weights(
            kernel=kernel,
            i=i,
            local_obs_idx=local_obs_idx,
            x_pert=x_pert,
            y_pert=y_pert,
            innovation=innovation,
            nx=nx,
            support_radius=support_radius,
        )
        weight_matrix[i, local_obs_idx] = weights

        r_inv = np.diag(weights / obs_var)
        c_mat = ((nens - 1) / infl) * np.eye(nens) + y_pert @ r_inv @ y_pert.T
        pa_tilde = np.linalg.inv(c_mat)
        w_mean = pa_tilde @ y_pert @ r_inv @ innovation
        w_pert = sym_sqrt((nens - 1) * pa_tilde)

        x_mean_a = x_mean[i] + x_pert[:, i] @ w_mean
        x_pert_a = x_pert[:, i] @ w_pert
        ana[:, i] = x_mean_a + x_pert_a

    return ana, weight_matrix


def run_assimilation(obs: np.ndarray, snapshot_times: list[int]) -> dict[str, dict[int, np.ndarray]]:
    rng = np.random.default_rng(SEED)
    n_steps, nx = obs.shape
    obs0 = np.nan_to_num(obs[0], nan=0.0)

    histories: dict[str, dict[int, np.ndarray]] = {}
    for kernel in ["fixed", "corr", "innov", "hybrid"]:
        ensemble = obs0[None, :] + OBS_STD * rng.standard_normal((ENS_SIZE, nx))
        weight_matrices: dict[int, np.ndarray] = {}
        for t in range(n_steps):
            if t > 0:
                ensemble = np.stack([rk4_step(member) for member in ensemble], axis=0)
            ensemble, weight_matrix = letkf_update_proxy(
                ensemble=ensemble,
                obs_vec=obs[t],
                obs_var=OBS_VAR,
                support_radius=SUPPORT_RADIUS,
                infl=INFL,
                kernel=kernel,
            )
            if t in snapshot_times:
                weight_matrices[t] = weight_matrix
        histories[kernel] = weight_matrices
    return histories


def pick_snapshot_times(obs: np.ndarray) -> list[int]:
    counts = np.sum(~np.isnan(obs), axis=1)
    observed_steps = np.where(counts > 0)[0]
    if len(observed_steps) == 0:
        return [0]
    candidates = {
        int(observed_steps[0]),
        int(observed_steps[len(observed_steps) // 2]),
        int(observed_steps[-1]),
    }
    return sorted(candidates)


def save_heatmaps(snapshots: dict[str, Snapshot]) -> None:
    for kernel, snapshot in snapshots.items():
        plt.figure(figsize=(7, 5.5))
        plt.imshow(snapshot.weight_matrix, aspect="auto", cmap="viridis")
        plt.colorbar(label="weight")
        plt.title(f"{kernel} weight matrix, t={snapshot.time_step}")
        plt.xlabel("obs dim j")
        plt.ylabel("state dim i")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"实验2_权重热图_{kernel}_t{snapshot.time_step}.png", dpi=180)
        plt.close()


def save_curve_plot(all_snapshots: list[Snapshot]) -> None:
    fig, axes = plt.subplots(1, len(all_snapshots), figsize=(15, 4), sharey=True)
    if len(all_snapshots) == 1:
        axes = [axes]
    for ax, snapshot in zip(axes, all_snapshots):
        ax.plot(snapshot.weight_curve, marker="o", markersize=2.5, linewidth=1.2)
        ax.set_title(f"{snapshot.kernel}, t={snapshot.time_step}, i={snapshot.state_index}")
        ax.set_xlabel("obs dim j")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("normalized weight")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "实验2_典型权重曲线.png", dpi=180)
    plt.close()


def summarize_matrix(mat: np.ndarray) -> dict[str, float]:
    nz = mat[mat > 0]
    if nz.size == 0:
        return {"min": 0.0, "max": 0.0, "mean": 0.0, "std": 0.0, "sparsity": 1.0}
    return {
        "min": float(nz.min()),
        "max": float(nz.max()),
        "mean": float(nz.mean()),
        "std": float(nz.std(ddof=0)),
        "sparsity": float(np.mean(mat <= 0.0)),
    }


def write_summary(
    snapshot_times: list[int],
    histories: dict[str, dict[int, np.ndarray]],
    state_index: int,
) -> None:
    snapshot_payload: dict[str, dict[str, dict[str, float]]] = {}
    for kernel, matrices in histories.items():
        snapshot_payload[kernel] = {}
        for t in snapshot_times:
            snapshot_payload[kernel][str(t)] = summarize_matrix(matrices[t])

    json_path = OUTPUT_DIR / "实验2_权重结构统计.json"
    json_path.write_text(json.dumps(snapshot_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 实验2权重结构补充分析",
        "",
        f"- 固定参数：`ens_size={ENS_SIZE}`，`infl={INFL}`，`obs_std={OBS_STD}`，`support_radius={SUPPORT_RADIUS}`，`seed={SEED}`",
        f"- 代表时间步：`{snapshot_times}`",
        f"- 代表状态维度：`i={state_index}`",
        "",
        "## 结构统计",
        "",
        "| kernel | time_step | min | max | mean | std |",
        "|--------|-----------|-----|-----|------|-----|",
    ]

    for kernel in ["fixed", "corr", "innov", "hybrid"]:
        for t in snapshot_times:
            stats = snapshot_payload[kernel][str(t)]
            lines.append(
                f"| {kernel} | {t} | {stats['min']:.4f} | {stats['max']:.4f} | {stats['mean']:.4f} | {stats['std']:.4f} |"
            )

    mid_t = snapshot_times[1]
    fixed_std = snapshot_payload["fixed"][str(mid_t)]["std"]
    corr_std = snapshot_payload["corr"][str(mid_t)]["std"]
    innov_std = snapshot_payload["innov"][str(mid_t)]["std"]
    hybrid_std = snapshot_payload["hybrid"][str(mid_t)]["std"]

    lines.extend(
        [
            "",
            "## 观察结论",
            "",
            f"- `fixed` 在 `t={mid_t}` 的权重标准差为 `{fixed_std:.4f}`，几乎是常数矩阵，对应全局等权。",
            f"- `corr` 在 `t={mid_t}` 的权重标准差升到 `{corr_std:.4f}`，说明它确实引入了结构，但波动仍偏温和。",
            f"- `innov` 在 `t={mid_t}` 的权重标准差为 `{innov_std:.4f}`，会更强地按残差大小压缩部分观测。",
            f"- `hybrid` 在 `t={mid_t}` 的权重标准差为 `{hybrid_std:.4f}`，通常表现为更尖锐的抑制，容易把多个经验偏好叠加成过强降权。",
            "",
            "## 输出文件",
            "",
            "- `实验2_权重热图_fixed_*.png`",
            "- `实验2_权重热图_corr_*.png`",
            "- `实验2_权重热图_innov_*.png`",
            "- `实验2_权重热图_hybrid_*.png`",
            "- `实验2_典型权重曲线.png`",
            "- `实验2_权重结构统计.json`",
        ]
    )

    (OUTPUT_DIR / "实验2_权重结构分析_summary.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    obs, _truth = load_competition_csv(DATA_DIR / "lorenz96_train.csv")
    snapshot_times = pick_snapshot_times(obs)
    histories = run_assimilation(obs, snapshot_times)
    state_index = 10
    mid_t = snapshot_times[1]

    heatmap_snapshots = {
        kernel: Snapshot(
            time_step=mid_t,
            kernel=kernel,
            weight_matrix=histories[kernel][mid_t],
            state_index=state_index,
            weight_curve=histories[kernel][mid_t][state_index],
        )
        for kernel in histories
    }
    save_heatmaps(heatmap_snapshots)

    curve_snapshots = [
        Snapshot(
            time_step=mid_t,
            kernel=kernel,
            weight_matrix=histories[kernel][mid_t],
            state_index=state_index,
            weight_curve=histories[kernel][mid_t][state_index],
        )
        for kernel in ["fixed", "corr", "innov", "hybrid"]
    ]
    save_curve_plot(curve_snapshots)
    write_summary(snapshot_times, histories, state_index)
    print(f"输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
