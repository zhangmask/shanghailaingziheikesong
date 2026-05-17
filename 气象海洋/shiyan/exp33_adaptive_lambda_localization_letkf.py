from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "exp33_adaptive_lambda_localization_outputs"
REMOTE_BASE = Path("/home/infra/qda_competition")
REMOTE_OUTPUT = REMOTE_BASE / "experiments" / "adaptive_lambda_localization_letkf"

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
LAMBDA_MIN = 0.01
LAMBDA_MAX = 0.08


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


def stable_inverse(mat: np.ndarray) -> np.ndarray:
    eye = np.eye(mat.shape[0], dtype=float)
    for jitter in (0.0, 1e-8, 1e-6, 1e-4):
        try:
            return np.linalg.inv(mat + jitter * eye)
        except np.linalg.LinAlgError:
            continue
    return np.linalg.pinv(mat, hermitian=True)


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


def compute_corr_weights(i: int, x_pert: np.ndarray, y_pert: np.ndarray) -> np.ndarray:
    state_signal = x_pert[:, i]
    state_std = state_signal.std(ddof=1) + EPS
    obs_std = y_pert.std(axis=0, ddof=1) + EPS
    corr = np.abs(((state_signal[:, None] * y_pert).mean(axis=0)) / (state_std * obs_std))
    corr = np.clip(corr, 0.0, 1.0)
    return normalize_weights(0.1 + corr)


def compute_distance_prior(i: int, local_obs_idx: np.ndarray, nx: int, support_radius: int) -> np.ndarray:
    sigma = max(support_radius / 2.0, 1.0)
    distances = np.array([cyclic_distance(i, int(j), nx) for j in local_obs_idx], dtype=float)
    prior = np.exp(-(distances**2) / (2.0 * sigma**2))
    return normalize_weights(0.1 + prior, min_clip=0.05)


def compute_quantum_localization_weights(i: int, x_mean: np.ndarray, obs_vec: np.ndarray, local_obs_idx: np.ndarray, support_radius: int) -> np.ndarray:
    nx = len(x_mean)
    state_window = cyclic_window(x_mean, i, WINDOW_SIZE)[None, :]
    obs_fill = np.nan_to_num(obs_vec, nan=0.0)
    obs_windows = np.stack([cyclic_window(obs_fill, int(j), WINDOW_SIZE) for j in local_obs_idx], axis=0)
    quantum_raw = build_quantum_lookup(state_window, obs_windows)[0]
    dist_prior = compute_distance_prior(i=i, local_obs_idx=local_obs_idx, nx=nx, support_radius=support_radius)
    return dist_prior, quantum_raw


def compute_local_lambda(quantum_signal: float, innovation_signal: float, spread_signal: float) -> float:
    lam = 0.015 + 0.03 * quantum_signal + 0.02 * innovation_signal - 0.015 * spread_signal
    return float(np.clip(lam, LAMBDA_MIN, LAMBDA_MAX))


def summarize_lambda_values(lambda_values: list[float]) -> dict[str, float | int]:
    if not lambda_values:
        return {}
    lam_arr = np.asarray(lambda_values, dtype=float)
    return {
        "lambda_mean": float(lam_arr.mean()),
        "lambda_min": float(lam_arr.min()),
        "lambda_max": float(lam_arr.max()),
        "lambda_count": int(lam_arr.size),
    }


def letkf_update_weighted(
    ensemble: np.ndarray,
    obs_vec: np.ndarray,
    obs_var: float,
    support_radius: int,
    infl: float,
    method: str,
    lam: float | None,
) -> tuple[np.ndarray, dict[str, list[float]]]:
    nens, nx = ensemble.shape
    ana = np.empty_like(ensemble)
    lambda_values: list[float] = []

    x_mean = ensemble.mean(axis=0)
    x_pert = ensemble - x_mean
    obs_idx_all = np.where(~np.isnan(obs_vec))[0]
    if len(obs_idx_all) == 0:
        return ensemble.copy(), {"lambda_values": []}

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

        if method == "fixed":
            weights = np.ones(len(local_obs_idx), dtype=float)
            r_inv = np.diag(weights / obs_var)
            c_mat = ((nens - 1) / infl) * np.eye(nens) + y_pert @ r_inv @ y_pert.T
            pa_tilde = stable_inverse(c_mat)
            w_mean = pa_tilde @ y_pert @ r_inv @ innovation
            w_pert = sym_sqrt((nens - 1) * pa_tilde)
            x_mean_a = x_mean[i] + x_pert[:, i] @ w_mean
            x_pert_a = x_pert[:, i] @ w_pert
            ana[:, i] = x_mean_a + x_pert_a
            continue

        if method == "corr":
            weights = compute_corr_weights(i=i, x_pert=x_pert, y_pert=y_pert)
            r_inv = np.diag(weights / obs_var)
            c_mat = ((nens - 1) / infl) * np.eye(nens) + y_pert @ r_inv @ y_pert.T
            pa_tilde = stable_inverse(c_mat)
            w_mean = pa_tilde @ y_pert @ r_inv @ innovation
            w_pert = sym_sqrt((nens - 1) * pa_tilde)
            x_mean_a = x_mean[i] + x_pert[:, i] @ w_mean
            x_pert_a = x_pert[:, i] @ w_pert
            ana[:, i] = x_mean_a + x_pert_a
            continue

        if method != "adaptive_quantum_localization":
            raise ValueError(f"Unknown method: {method}")

        dist_prior, quantum_raw = compute_quantum_localization_weights(
            i=i,
            x_mean=x_mean,
            obs_vec=obs_vec,
            local_obs_idx=local_obs_idx,
            support_radius=support_radius,
        )
        quantum_signal = float(np.mean(quantum_raw))
        innovation_signal = float(np.tanh(np.mean(np.abs(innovation)) / (OBS_STD + EPS)))
        spread_signal = float(np.tanh(np.mean(np.std(y_pert, axis=0, ddof=1)) / (OBS_STD + EPS)))
        lam_i = compute_local_lambda(quantum_signal, innovation_signal, spread_signal)
        lambda_values.append(lam_i)
        weights = normalize_weights(dist_prior * ((1.0 - lam_i) + lam_i * quantum_raw))
        r_inv = np.diag(weights / obs_var)
        c_mat = ((nens - 1) / infl) * np.eye(nens) + y_pert @ r_inv @ y_pert.T
        pa_tilde = stable_inverse(c_mat)
        w_mean = pa_tilde @ y_pert @ r_inv @ innovation
        w_pert = sym_sqrt((nens - 1) * pa_tilde)
        x_mean_a = x_mean[i] + x_pert[:, i] @ w_mean
        x_pert_a = x_pert[:, i] @ w_pert
        ana[:, i] = x_mean_a + x_pert_a

    return ana, {"lambda_values": lambda_values}

def run_filter(
    obs: np.ndarray,
    truth: np.ndarray,
    method: str,
    lam: float | None,
) -> tuple[np.ndarray, dict[str, float], dict[str, float | int]]:
    nt, nx = obs.shape
    rng = np.random.default_rng(SEED)
    lambda_values: list[float] = []
    init_center = np.where(np.isnan(obs[0]), 0.0, obs[0])
    ensemble = init_center + rng.normal(0.0, OBS_STD, size=(ENS_SIZE, nx))
    analysis = np.zeros((nt, nx), dtype=float)
    analysis[0] = ensemble.mean(axis=0)
    if np.any(~np.isnan(obs[0])):
        ensemble, step_stats = letkf_update_weighted(
            ensemble=ensemble,
            obs_vec=obs[0],
            obs_var=OBS_VAR,
            support_radius=SUPPORT_RADIUS,
            infl=INFL,
            method=method,
            lam=lam,
        )
        lambda_values.extend(step_stats.get("lambda_values", []))
        analysis[0] = ensemble.mean(axis=0)

    for t in range(1, nt):
        for n in range(ENS_SIZE):
            ensemble[n] = rk4_step(ensemble[n], dt=DT, forcing=FORCING)
        if np.any(~np.isnan(obs[t])):
            ensemble, step_stats = letkf_update_weighted(
                ensemble=ensemble,
                obs_vec=obs[t],
                obs_var=OBS_VAR,
                support_radius=SUPPORT_RADIUS,
                infl=INFL,
                method=method,
                lam=lam,
            )
            lambda_values.extend(step_stats.get("lambda_values", []))
        analysis[t] = ensemble.mean(axis=0)

    mask = ~np.isnan(truth)
    rmse = float(np.sqrt(np.mean((analysis[mask] - truth[mask]) ** 2)))
    mae = float(np.mean(np.abs(analysis[mask] - truth[mask])))
    return analysis, {"rmse": rmse, "mae": mae, "count": int(mask.sum())}, summarize_lambda_values(lambda_values)

def resolve_default_output() -> Path:
    if REMOTE_BASE.exists():
        return REMOTE_OUTPUT
    return OUTPUT_DIR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="实验33：局地化自适应 lambda LETKF 验证")
    parser.add_argument("--train-input", type=Path, default=REMOTE_BASE / "data" / "lorenz96_train.csv")
    parser.add_argument("--test-input", type=Path, default=REMOTE_BASE / "data" / "lorenz96_test_1.csv")
    parser.add_argument("--output-dir", type=Path, default=resolve_default_output())
    return parser.parse_args()


def build_experiments() -> list[tuple[str, float | None]]:
    return [("fixed", None), ("corr", None), ("adaptive_quantum_localization", None)]

def result_file_stem(method: str, lam: float | None) -> str:
    if lam is None:
        return method
    return f"{method}_lam_{str(lam).replace('.', '_')}"


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    datasets = [("train", args.train_input), ("test_1", args.test_input)]
    experiments = build_experiments()
    all_results: list[dict[str, float | int | str | None]] = []

    best_test_rmse = float("inf")
    best_test_prediction: Path | None = None
    best_result_record: dict[str, float | int | str | None] | None = None

    for method, lam in experiments:
        rec: dict[str, float | int | str | None] = {
            "method": method,
            "lambda": lam,
            "support_radius": SUPPORT_RADIUS,
        }
        for split, path in datasets:
            obs, truth = load_competition_csv(path)
            analysis, metrics, lambda_stats = run_filter(obs, truth, method=method, lam=lam)
            out_path = args.output_dir / f"{split}_{result_file_stem(method, lam)}.csv"
            save_prediction_csv(out_path, analysis)
            rec[f"{split}_rmse"] = metrics["rmse"]
            rec[f"{split}_mae"] = metrics["mae"]
            rec[f"{split}_count"] = metrics["count"]
            for key, value in lambda_stats.items():
                rec[f"{split}_{key}"] = value
            if split == "test_1" and metrics["rmse"] < best_test_rmse:
                best_test_rmse = metrics["rmse"]
                best_test_prediction = out_path
                best_result_record = rec.copy()
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
            "lambda_bounds": [LAMBDA_MIN, LAMBDA_MAX],
            "adaptive_rule": {
                "base": 0.015,
                "quantum_coeff": 0.03,
                "innovation_coeff": 0.02,
                "spread_coeff": -0.015,
            },
        },
        "results": all_results,
        "best_test": best_result_record,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    with (args.output_dir / "summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "method",
                "lambda",
                "support_radius",
                "train_rmse",
                "train_mae",
                "train_count",
                "train_lambda_mean",
                "train_lambda_min",
                "train_lambda_max",
                "train_lambda_count",
                "test_1_rmse",
                "test_1_mae",
                "test_1_count",
                "test_1_lambda_mean",
                "test_1_lambda_min",
                "test_1_lambda_max",
                "test_1_lambda_count",
            ],
        )
        writer.writeheader()
        writer.writerows(all_results)

    if best_test_prediction is not None:
        shutil.copyfile(best_test_prediction, args.output_dir / "best_test_prediction.csv")
        shutil.copyfile(best_test_prediction, args.output_dir / "result.csv")

    print("BEST_TEST", json.dumps(best_result_record, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
