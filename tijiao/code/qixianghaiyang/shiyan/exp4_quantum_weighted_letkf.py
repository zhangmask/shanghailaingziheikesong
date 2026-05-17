from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "气象海洋" / "小规模测试"
OUTPUT_DIR = ROOT / "exp4_quantum_weighted_outputs"
REMOTE_BASE = Path("/home/infra/qda_competition")
REMOTE_OUTPUT = REMOTE_BASE / "experiments" / "quantum_weighted_letkf"

ENS_SIZE = 40
INFL = 1.02
OBS_STD = 0.5
OBS_VAR = OBS_STD**2
DT = 0.05
FORCING = 8.0
SEED = 2
SUPPORT_RADIUS = 20
WINDOW_SIZE = 4
N_QUBITS = 4
FEATURE_SCALE = np.pi / 2.0
EPS = 1e-8


def cyclic_distance(i: int, j: int, n: int) -> int:
    d = abs(i - j)
    return min(d, n - d)


def cyclic_window(vec: np.ndarray, center: int, width: int) -> np.ndarray:
    n = len(vec)
    offsets = range(-(width // 2), -(width // 2) + width)
    return np.array([vec[(center + off) % n] for off in offsets], dtype=float)


def lorenz96_rhs(x: np.ndarray, forcing: float = FORCING) -> np.ndarray:
    return (np.roll(x, -1) - np.roll(x, 2)) * np.roll(x, 1) - x + forcing


def rk4_step(x: np.ndarray, dt: float = DT, forcing: float = FORCING) -> np.ndarray:
    k1 = lorenz96_rhs(x, forcing)
    k2 = lorenz96_rhs(x + 0.5 * dt * k1, forcing)
    k3 = lorenz96_rhs(x + 0.5 * dt * k2, forcing)
    k4 = lorenz96_rhs(x + dt * k3, forcing)
    return x + dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0


def sym_sqrt(mat: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh(mat)
    vals = np.clip(vals, 0.0, None)
    return vecs @ np.diag(np.sqrt(vals)) @ vecs.T


def load_competition_csv(path: Path) -> tuple[np.ndarray, np.ndarray]:
    rows: list[tuple[int, int, float, float]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            true_value = float(row["true_value"]) if row["true_value"] != "" else math.nan
            observed_value = float(row["observed_value"]) if row["observed_value"] != "" else math.nan
            rows.append((int(row["time_step"]), int(row["dimension"]), true_value, observed_value))

    max_t = max(row[0] for row in rows)
    max_d = max(row[1] for row in rows)
    truth = np.full((max_t + 1, max_d + 1), np.nan, dtype=float)
    obs = np.full((max_t + 1, max_d + 1), np.nan, dtype=float)
    for t, d, true_value, observed_value in rows:
        truth[t, d] = true_value
        obs[t, d] = observed_value
    return obs, truth


def save_prediction_csv(path: Path, analysis: np.ndarray) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_step", "dimension", "predicted_value"])
        for t in range(analysis.shape[0]):
            for d in range(analysis.shape[1]):
                writer.writerow([t, d, float(analysis[t, d])])


def normalize_weights(weights: np.ndarray, min_clip: float = 0.05) -> np.ndarray:
    weights = np.clip(np.asarray(weights, dtype=float), min_clip, None)
    return weights / (weights.mean() + EPS)


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


def standardize_pair_features(state_windows: np.ndarray, obs_windows: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    stacked = np.concatenate([state_windows, obs_windows], axis=0)
    mean = stacked.mean(axis=0, keepdims=True)
    std = stacked.std(axis=0, keepdims=True) + EPS
    state_z = FEATURE_SCALE * np.tanh((state_windows - mean) / std)
    obs_z = FEATURE_SCALE * np.tanh((obs_windows - mean) / std)
    return state_z, obs_z


def build_quantum_lookup(state_windows: np.ndarray, obs_windows: np.ndarray) -> np.ndarray:
    state_features, obs_features = standardize_pair_features(state_windows, obs_windows)
    state_states = [Statevector.from_instruction(build_feature_map(feature)) for feature in state_features]
    obs_states = [Statevector.from_instruction(build_feature_map(feature)) for feature in obs_features]
    lookup = np.zeros((len(state_states), len(obs_states)), dtype=float)
    for i, state in enumerate(state_states):
        for j, obs_state in enumerate(obs_states):
            overlap = np.vdot(state.data, obs_state.data)
            lookup[i, j] = float(np.abs(overlap) ** 2)
    return lookup


def compute_corr_weights(
    i: int,
    local_obs_idx: np.ndarray,
    x_pert: np.ndarray,
    y_pert: np.ndarray,
) -> np.ndarray:
    state_signal = x_pert[:, i]
    state_std = state_signal.std(ddof=1) + EPS
    obs_std = y_pert.std(axis=0, ddof=1) + EPS
    corr = np.abs(((state_signal[:, None] * y_pert).mean(axis=0)) / (state_std * obs_std))
    corr = np.clip(corr, 0.0, 1.0)
    _ = local_obs_idx
    return normalize_weights(0.1 + corr)


def compute_quantum_lookup_for_step(
    x_mean: np.ndarray,
    obs_vec: np.ndarray,
    obs_idx_all: np.ndarray,
) -> np.ndarray:
    nx = len(x_mean)
    obs_fill = np.nan_to_num(obs_vec, nan=0.0)
    state_windows = np.stack([cyclic_window(x_mean, i, WINDOW_SIZE) for i in range(nx)], axis=0)
    obs_windows = np.stack([cyclic_window(obs_fill, int(j), WINDOW_SIZE) for j in obs_idx_all], axis=0)
    return build_quantum_lookup(state_windows, obs_windows)


def letkf_update_weighted(
    ensemble: np.ndarray,
    obs_vec: np.ndarray,
    obs_var: float,
    support_radius: int,
    infl: float,
    kernel: str,
) -> np.ndarray:
    nens, nx = ensemble.shape
    ana = np.empty_like(ensemble)

    x_mean = ensemble.mean(axis=0)
    x_pert = ensemble - x_mean
    obs_idx_all = np.where(~np.isnan(obs_vec))[0]
    if len(obs_idx_all) == 0:
        return ensemble.copy()

    quantum_lookup = None
    if kernel == "quantum":
        quantum_lookup = compute_quantum_lookup_for_step(x_mean, obs_vec, obs_idx_all)

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

        if kernel == "fixed":
            weights = np.ones(len(local_obs_idx), dtype=float)
        elif kernel == "corr":
            weights = compute_corr_weights(i=i, local_obs_idx=local_obs_idx, x_pert=x_pert, y_pert=y_pert)
        elif kernel == "quantum":
            assert quantum_lookup is not None
            local_pos = np.searchsorted(obs_idx_all, local_obs_idx)
            weights = normalize_weights(quantum_lookup[i, local_pos])
        else:
            raise ValueError(f"Unknown kernel: {kernel}")

        r_inv = np.diag(weights / obs_var)
        c_mat = ((nens - 1) / infl) * np.eye(nens) + y_pert @ r_inv @ y_pert.T
        pa_tilde = np.linalg.inv(c_mat)
        w_mean = pa_tilde @ y_pert @ r_inv @ innovation
        w_pert = sym_sqrt((nens - 1) * pa_tilde)

        x_mean_a = x_mean[i] + x_pert[:, i] @ w_mean
        x_pert_a = x_pert[:, i] @ w_pert
        ana[:, i] = x_mean_a + x_pert_a

    return ana


def run_filter(obs: np.ndarray, truth: np.ndarray, kernel: str) -> tuple[np.ndarray, dict[str, float]]:
    nt, nx = obs.shape
    rng = np.random.default_rng(SEED)
    init_center = np.where(np.isnan(obs[0]), 0.0, obs[0])
    ensemble = init_center + rng.normal(0.0, OBS_STD, size=(ENS_SIZE, nx))
    analysis = np.zeros((nt, nx), dtype=float)

    analysis[0] = ensemble.mean(axis=0)
    if np.any(~np.isnan(obs[0])):
        ensemble = letkf_update_weighted(
            ensemble=ensemble,
            obs_vec=obs[0],
            obs_var=OBS_VAR,
            support_radius=SUPPORT_RADIUS,
            infl=INFL,
            kernel=kernel,
        )
        analysis[0] = ensemble.mean(axis=0)

    for t in range(1, nt):
        for n in range(ENS_SIZE):
            ensemble[n] = rk4_step(ensemble[n], dt=DT, forcing=FORCING)
        if np.any(~np.isnan(obs[t])):
            ensemble = letkf_update_weighted(
                ensemble=ensemble,
                obs_vec=obs[t],
                obs_var=OBS_VAR,
                support_radius=SUPPORT_RADIUS,
                infl=INFL,
                kernel=kernel,
            )
        analysis[t] = ensemble.mean(axis=0)

    mask = ~np.isnan(truth)
    rmse = float(np.sqrt(np.mean((analysis[mask] - truth[mask]) ** 2)))
    mae = float(np.mean(np.abs(analysis[mask] - truth[mask])))
    return analysis, {"rmse": rmse, "mae": mae, "count": int(mask.sum())}


def resolve_default_output() -> Path:
    if Path("/home/infra/qda_competition").exists():
        return REMOTE_OUTPUT
    return OUTPUT_DIR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="实验4：量子核最小接入版 LETKF 验证")
    parser.add_argument("--train-input", type=Path, default=REMOTE_BASE / "data" / "lorenz96_train.csv")
    parser.add_argument("--test-input", type=Path, default=REMOTE_BASE / "data" / "lorenz96_test_1.csv")
    parser.add_argument("--output-dir", type=Path, default=resolve_default_output())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    datasets = [("train", args.train_input), ("test_1", args.test_input)]
    kernels = ["fixed", "corr", "quantum"]
    all_results: list[dict[str, float | int | str]] = []

    for kernel in kernels:
        rec: dict[str, float | int | str] = {"kernel": kernel, "support_radius": SUPPORT_RADIUS}
        for split, path in datasets:
            obs, truth = load_competition_csv(path)
            analysis, metrics = run_filter(obs, truth, kernel=kernel)
            save_prediction_csv(args.output_dir / f"{split}_{kernel}.csv", analysis)
            rec[f"{split}_rmse"] = metrics["rmse"]
            rec[f"{split}_mae"] = metrics["mae"]
            rec[f"{split}_count"] = metrics["count"]
        all_results.append(rec)
        print("DONE", json.dumps(rec, ensure_ascii=False), flush=True)

    summary = {
        "config": {
            "ens_size": ENS_SIZE,
            "infl": INFL,
            "obs_std": OBS_STD,
            "dt": DT,
            "forcing": FORCING,
            "seed": SEED,
            "support_radius": SUPPORT_RADIUS,
            "window_size": WINDOW_SIZE,
            "n_qubits": N_QUBITS,
        },
        "results": all_results,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.output_dir / "summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "kernel",
                "support_radius",
                "train_rmse",
                "train_mae",
                "train_count",
                "test_1_rmse",
                "test_1_mae",
                "test_1_count",
            ],
        )
        writer.writeheader()
        writer.writerows(all_results)

    best_test = min(all_results, key=lambda item: float(item["test_1_rmse"]))
    print("BEST_TEST", json.dumps(best_test, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
