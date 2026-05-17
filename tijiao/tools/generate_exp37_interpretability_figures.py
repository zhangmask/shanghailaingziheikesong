from __future__ import annotations
import csv
import importlib.util
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patches


# 尽量使用 Windows 常见中文字体，避免标题乱码。
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


ROOT = Path(r"d:\Desktop\laingzimuxi")
ANALYSIS_DIR = ROOT / "tijiao" / "results" / "exp37_analysis"
FIG_DIR = ROOT / "tijiao" / "figures"
EXP37_SCRIPT = ROOT / "气象海洋" / "shiyan" / "exp37_rho_J_weak_fusion_letkf.py"
TEST_INPUT = ANALYSIS_DIR / "lorenz96_test_1.csv"


class LocalExp37Shim:
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

    @staticmethod
    def cyclic_distance(i: int, j: int, n: int) -> int:
        d = abs(i - j)
        return min(d, n - d)

    @staticmethod
    def cyclic_window(vec: np.ndarray, center: int, width: int) -> np.ndarray:
        n = len(vec)
        offsets = range(-(width // 2), -(width // 2) + width)
        return np.array([vec[(center + off) % n] for off in offsets], dtype=float)

    @staticmethod
    def lorenz96_rhs(x: np.ndarray, forcing: float = FORCING) -> np.ndarray:
        return (np.roll(x, -1) - np.roll(x, 2)) * np.roll(x, 1) - x + forcing

    @staticmethod
    def rk4_step(x: np.ndarray, dt: float = DT, forcing: float = FORCING) -> np.ndarray:
        k1 = LocalExp37Shim.lorenz96_rhs(x, forcing)
        k2 = LocalExp37Shim.lorenz96_rhs(x + 0.5 * dt * k1, forcing)
        k3 = LocalExp37Shim.lorenz96_rhs(x + 0.5 * dt * k2, forcing)
        k4 = LocalExp37Shim.lorenz96_rhs(x + dt * k3, forcing)
        return x + dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0

    @staticmethod
    def sym_sqrt(mat: np.ndarray) -> np.ndarray:
        vals, vecs = np.linalg.eigh(mat)
        vals = np.clip(vals, 0.0, None)
        return vecs @ np.diag(np.sqrt(vals)) @ vecs.T

    @staticmethod
    def stable_inverse(mat: np.ndarray) -> np.ndarray:
        eye = np.eye(mat.shape[0], dtype=float)
        for jitter in (0.0, 1e-8, 1e-6, 1e-4):
            try:
                return np.linalg.inv(mat + jitter * eye)
            except np.linalg.LinAlgError:
                continue
        return np.linalg.pinv(mat, hermitian=True)

    @staticmethod
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

    @staticmethod
    def normalize_weights(weights: np.ndarray, min_clip: float = 0.05) -> np.ndarray:
        weights = np.clip(np.asarray(weights, dtype=float), min_clip, None)
        return weights / (weights.mean() + LocalExp37Shim.EPS)

    @staticmethod
    def standardize_pair_features(state_windows: np.ndarray, obs_windows: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        stacked = np.concatenate([state_windows, obs_windows], axis=0)
        mean = stacked.mean(axis=0, keepdims=True)
        std = stacked.std(axis=0, keepdims=True) + LocalExp37Shim.EPS
        state_z = LocalExp37Shim.FEATURE_SCALE * np.tanh((state_windows - mean) / std)
        obs_z = LocalExp37Shim.FEATURE_SCALE * np.tanh((obs_windows - mean) / std)
        return state_z, obs_z

    @staticmethod
    def _apply_single_qubit_gate(state: np.ndarray, gate: np.ndarray, qubit: int) -> np.ndarray:
        out = state.copy()
        step = 1 << qubit
        block = step << 1
        for base in range(0, len(state), block):
            for inner in range(step):
                idx0 = base + inner
                idx1 = idx0 + step
                a0 = state[idx0]
                a1 = state[idx1]
                out[idx0] = gate[0, 0] * a0 + gate[0, 1] * a1
                out[idx1] = gate[1, 0] * a0 + gate[1, 1] * a1
        return out

    @staticmethod
    def _apply_cz(state: np.ndarray, control: int, target: int) -> np.ndarray:
        out = state.copy()
        for idx in range(len(state)):
            if ((idx >> control) & 1) and ((idx >> target) & 1):
                out[idx] *= -1.0
        return out

    @staticmethod
    def _build_statevector(feature: np.ndarray) -> np.ndarray:
        n_qubits = LocalExp37Shim.N_QUBITS
        state = np.zeros(2**n_qubits, dtype=complex)
        state[0] = 1.0 + 0.0j
        h_gate = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / np.sqrt(2.0)

        for q, value in enumerate(feature):
            state = LocalExp37Shim._apply_single_qubit_gate(state, h_gate, q)
            ry = np.array(
                [
                    [np.cos(value / 2.0), -np.sin(value / 2.0)],
                    [np.sin(value / 2.0), np.cos(value / 2.0)],
                ],
                dtype=complex,
            )
            rz = np.array(
                [
                    [np.exp(-0.5j * value * value), 0.0],
                    [0.0, np.exp(0.5j * value * value)],
                ],
                dtype=complex,
            )
            state = LocalExp37Shim._apply_single_qubit_gate(state, ry, q)
            state = LocalExp37Shim._apply_single_qubit_gate(state, rz, q)

        for q in range(n_qubits - 1):
            angle = float(0.35 * feature[q] * feature[q + 1])
            state = LocalExp37Shim._apply_cz(state, q, q + 1)
            rz = np.array(
                [
                    [np.exp(-0.5j * angle), 0.0],
                    [0.0, np.exp(0.5j * angle)],
                ],
                dtype=complex,
            )
            ry_angle = float(0.15 * (feature[q] + feature[q + 1]))
            ry = np.array(
                [
                    [np.cos(ry_angle / 2.0), -np.sin(ry_angle / 2.0)],
                    [np.sin(ry_angle / 2.0), np.cos(ry_angle / 2.0)],
                ],
                dtype=complex,
            )
            state = LocalExp37Shim._apply_single_qubit_gate(state, rz, q + 1)
            state = LocalExp37Shim._apply_single_qubit_gate(state, ry, q)

        for q, value in enumerate(feature):
            ry = np.array(
                [
                    [np.cos(0.25 * value), -np.sin(0.25 * value)],
                    [np.sin(0.25 * value), np.cos(0.25 * value)],
                ],
                dtype=complex,
            )
            rz = np.array(
                [
                    [np.exp(-0.125j * value), 0.0],
                    [0.0, np.exp(0.125j * value)],
                ],
                dtype=complex,
            )
            state = LocalExp37Shim._apply_single_qubit_gate(state, ry, q)
            state = LocalExp37Shim._apply_single_qubit_gate(state, rz, q)

        return state

    @staticmethod
    def build_quantum_lookup(state_windows: np.ndarray, obs_windows: np.ndarray) -> np.ndarray:
        state_features, obs_features = LocalExp37Shim.standardize_pair_features(state_windows, obs_windows)
        state_states = [LocalExp37Shim._build_statevector(feature) for feature in state_features]
        obs_states = [LocalExp37Shim._build_statevector(feature) for feature in obs_features]
        lookup = np.zeros((len(state_states), len(obs_states)), dtype=float)
        for i, state in enumerate(state_states):
            for j, obs_state in enumerate(obs_states):
                overlap = np.vdot(state, obs_state)
                lookup[i, j] = float(np.abs(overlap) ** 2)
        return lookup

    @staticmethod
    def compute_corr_weights(i: int, x_pert: np.ndarray, y_pert: np.ndarray) -> np.ndarray:
        state_signal = x_pert[:, i]
        state_std = state_signal.std(ddof=1) + LocalExp37Shim.EPS
        obs_std = y_pert.std(axis=0, ddof=1) + LocalExp37Shim.EPS
        corr = np.abs(((state_signal[:, None] * y_pert).mean(axis=0)) / (state_std * obs_std))
        corr = np.clip(corr, 0.0, 1.0)
        return LocalExp37Shim.normalize_weights(0.1 + corr)

    @staticmethod
    def compute_distance_prior(i: int, local_obs_idx: np.ndarray, nx: int, support_radius: int) -> np.ndarray:
        sigma = max(support_radius / 2.0, 1.0)
        distances = np.array([LocalExp37Shim.cyclic_distance(i, int(j), nx) for j in local_obs_idx], dtype=float)
        prior = np.exp(-(distances**2) / (2.0 * sigma**2))
        return LocalExp37Shim.normalize_weights(0.1 + prior, min_clip=0.05)

    @staticmethod
    def compute_quantum_localization_weights(
        i: int,
        x_mean: np.ndarray,
        obs_vec: np.ndarray,
        local_obs_idx: np.ndarray,
        support_radius: int,
    ) -> tuple[np.ndarray, np.ndarray]:
        nx = len(x_mean)
        state_window = LocalExp37Shim.cyclic_window(x_mean, i, LocalExp37Shim.WINDOW_SIZE)[None, :]
        obs_fill = np.nan_to_num(obs_vec, nan=0.0)
        obs_windows = np.stack(
            [LocalExp37Shim.cyclic_window(obs_fill, int(j), LocalExp37Shim.WINDOW_SIZE) for j in local_obs_idx],
            axis=0,
        )
        quantum_raw = LocalExp37Shim.build_quantum_lookup(state_window, obs_windows)[0]
        dist_prior = LocalExp37Shim.compute_distance_prior(i=i, local_obs_idx=local_obs_idx, nx=nx, support_radius=support_radius)
        return dist_prior, quantum_raw

    @staticmethod
    def build_j_corrected_state_signal(
        i: int,
        x_mean: np.ndarray,
        x_pert: np.ndarray,
        y_pert: np.ndarray,
        obs_vec: np.ndarray,
        local_obs_idx: np.ndarray,
        lam_j: float,
    ) -> tuple[np.ndarray, float]:
        state_window = LocalExp37Shim.cyclic_window(x_mean, i, LocalExp37Shim.WINDOW_SIZE)[None, :]
        obs_fill = np.nan_to_num(obs_vec, nan=0.0)
        obs_windows = np.stack(
            [LocalExp37Shim.cyclic_window(obs_fill, int(j), LocalExp37Shim.WINDOW_SIZE) for j in local_obs_idx],
            axis=0,
        )
        quantum_weights = LocalExp37Shim.normalize_weights(
            LocalExp37Shim.build_quantum_lookup(state_window, obs_windows)[0],
            min_clip=0.1,
        )
        local_mode = y_pert @ quantum_weights
        local_mode = local_mode - local_mode.mean()
        local_mode = local_mode / (np.linalg.norm(local_mode) + LocalExp37Shim.EPS)

        state_signal = x_pert[:, i]
        coupling = float(np.dot(state_signal, local_mode) / (np.linalg.norm(state_signal) + LocalExp37Shim.EPS))
        j_mode = coupling * local_mode
        corrected = state_signal + lam_j * j_mode
        corrected = corrected - corrected.mean()
        correction_strength = float(
            np.linalg.norm(corrected - state_signal) / (np.linalg.norm(state_signal) + LocalExp37Shim.EPS)
        )
        return corrected, correction_strength

    @staticmethod
    def letkf_update_weighted(
        ensemble: np.ndarray,
        obs_vec: np.ndarray,
        obs_var: float,
        support_radius: int,
        infl: float,
        method: str,
        lam_rho: float | None,
        lam_j: float | None,
    ) -> tuple[np.ndarray, dict[str, float]]:
        nens, nx = ensemble.shape
        ana = np.empty_like(ensemble)
        correction_total = 0.0
        correction_steps = 0
        x_mean = ensemble.mean(axis=0)
        x_pert = ensemble - x_mean
        obs_idx_all = np.where(~np.isnan(obs_vec))[0]
        if len(obs_idx_all) == 0:
            return ensemble.copy(), {"avg_j_correction_strength": 0.0}

        for i in range(nx):
            local_obs_idx = np.array(
                [j for j in obs_idx_all if LocalExp37Shim.cyclic_distance(i, j, nx) <= support_radius],
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
            elif method == "corr":
                weights = LocalExp37Shim.compute_corr_weights(i=i, x_pert=x_pert, y_pert=y_pert)
                r_inv = np.diag(weights / obs_var)
            elif method == "rho_j_weak_fusion":
                dist_prior, quantum_raw = LocalExp37Shim.compute_quantum_localization_weights(
                    i=i,
                    x_mean=x_mean,
                    obs_vec=obs_vec,
                    local_obs_idx=local_obs_idx,
                    support_radius=support_radius,
                )
                weights = LocalExp37Shim.normalize_weights(
                    dist_prior * ((1.0 - float(lam_rho)) + float(lam_rho) * quantum_raw)
                )
                r_inv = np.diag(weights / obs_var)
            else:
                raise ValueError(f"Unknown method: {method}")

            c_mat = ((nens - 1) / infl) * np.eye(nens) + y_pert @ r_inv @ y_pert.T
            pa_tilde = LocalExp37Shim.stable_inverse(c_mat)
            w_mean = pa_tilde @ y_pert @ r_inv @ innovation
            w_pert = LocalExp37Shim.sym_sqrt((nens - 1) * pa_tilde)

            if method == "rho_j_weak_fusion":
                corrected_signal, strength = LocalExp37Shim.build_j_corrected_state_signal(
                    i=i,
                    x_mean=x_mean,
                    x_pert=x_pert,
                    y_pert=y_pert,
                    obs_vec=obs_vec,
                    local_obs_idx=local_obs_idx,
                    lam_j=float(lam_j),
                )
                x_mean_a = x_mean[i] + corrected_signal @ w_mean
                x_pert_a = corrected_signal @ w_pert
                correction_total += strength
                correction_steps += 1
            else:
                x_mean_a = x_mean[i] + x_pert[:, i] @ w_mean
                x_pert_a = x_pert[:, i] @ w_pert

            ana[:, i] = x_mean_a + x_pert_a

        stats = {
            "avg_j_correction_strength": float(correction_total / max(correction_steps, 1)),
        }
        return ana, stats


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary = pd.read_csv(ANALYSIS_DIR / "exp37_summary.csv")
    truth = pd.read_csv(ANALYSIS_DIR / "lorenz96_test_1.csv")
    best = pd.read_csv(ANALYSIS_DIR / "exp37_result.csv")
    fixed = pd.read_csv(ANALYSIS_DIR / "exp37_test_fixed.csv")
    corr = pd.read_csv(ANALYSIS_DIR / "exp37_test_corr.csv")
    return summary, truth, best, fixed, corr


def merge_predictions(
    truth: pd.DataFrame,
    best: pd.DataFrame,
    fixed: pd.DataFrame,
    corr: pd.DataFrame,
) -> pd.DataFrame:
    merged = truth.merge(
        best.rename(columns={"predicted_value": "pred_best"}),
        on=["time_step", "dimension"],
        how="inner",
    ).merge(
        fixed.rename(columns={"predicted_value": "pred_fixed"}),
        on=["time_step", "dimension"],
        how="inner",
    ).merge(
        corr.rename(columns={"predicted_value": "pred_corr"}),
        on=["time_step", "dimension"],
        how="inner",
    )
    merged["err_best"] = merged["pred_best"] - merged["true_value"]
    merged["err_fixed"] = merged["pred_fixed"] - merged["true_value"]
    merged["err_corr"] = merged["pred_corr"] - merged["true_value"]
    merged["abs_err_best"] = merged["err_best"].abs()
    merged["abs_err_fixed"] = merged["err_fixed"].abs()
    merged["abs_err_corr"] = merged["err_corr"].abs()
    merged["gain_abs_err"] = merged["abs_err_fixed"] - merged["abs_err_best"]
    return merged


def load_exp37_module():
    spec = importlib.util.spec_from_file_location("exp37_module", EXP37_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载实验脚本: {EXP37_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except ModuleNotFoundError as exc:
        if exc.name != "qiskit":
            raise
        return LocalExp37Shim


def select_representative_case(merged: pd.DataFrame) -> tuple[int, int]:
    per_t = merged.groupby("time_step", as_index=False)["gain_abs_err"].mean().sort_values("gain_abs_err", ascending=False)
    candidate_times = per_t.head(10).sort_values("time_step")
    best_time = int(candidate_times.iloc[0]["time_step"])
    block = merged[merged["time_step"] == best_time].sort_values("gain_abs_err", ascending=False)
    best_dim = int(block.iloc[0]["dimension"])
    return best_time, best_dim


def extract_local_case(module, target_time: int, target_dim: int, lam_rho: float, lam_j: float) -> dict[str, object]:
    obs, truth = module.load_competition_csv(TEST_INPUT)
    nt, nx = obs.shape
    rng = np.random.default_rng(module.SEED)
    init_center = np.where(np.isnan(obs[0]), 0.0, obs[0])
    ensemble = init_center + rng.normal(0.0, module.OBS_STD, size=(module.ENS_SIZE, nx))

    for t in range(nt):
        if t > 0:
            for n in range(module.ENS_SIZE):
                ensemble[n] = module.rk4_step(ensemble[n], dt=module.DT, forcing=module.FORCING)

        obs_vec = obs[t]
        x_mean = ensemble.mean(axis=0)
        x_pert = ensemble - x_mean
        obs_idx_all = np.where(~np.isnan(obs_vec))[0]
        local_obs_idx = np.array(
            [j for j in obs_idx_all if module.cyclic_distance(target_dim, j, nx) <= module.SUPPORT_RADIUS],
            dtype=int,
        )
        y_ens = ensemble[:, local_obs_idx]
        y_mean = y_ens.mean(axis=0)
        y_pert = y_ens - y_mean

        if t == target_time:
            obs_fill = np.nan_to_num(obs_vec, nan=0.0)
            state_window = module.cyclic_window(x_mean, target_dim, module.WINDOW_SIZE)
            obs_windows = np.stack(
                [module.cyclic_window(obs_fill, int(j), module.WINDOW_SIZE) for j in local_obs_idx],
                axis=0,
            )
            dist_prior = module.compute_distance_prior(
                i=target_dim,
                local_obs_idx=local_obs_idx,
                nx=nx,
                support_radius=module.SUPPORT_RADIUS,
            )
            quantum_raw = module.build_quantum_lookup(state_window[None, :], obs_windows)[0]
            rho_weights = module.normalize_weights(
                dist_prior * ((1.0 - float(lam_rho)) + float(lam_rho) * quantum_raw)
            )
            corr_weights = module.compute_corr_weights(i=target_dim, x_pert=x_pert, y_pert=y_pert)

            quantum_weights = module.normalize_weights(quantum_raw, min_clip=0.1)
            local_mode = y_pert @ quantum_weights
            local_mode = local_mode - local_mode.mean()
            local_mode = local_mode / (np.linalg.norm(local_mode) + module.EPS)
            state_signal = x_pert[:, target_dim]
            coupling = float(np.dot(state_signal, local_mode) / (np.linalg.norm(state_signal) + module.EPS))
            j_mode = coupling * local_mode
            corrected_signal = state_signal + float(lam_j) * j_mode
            corrected_signal = corrected_signal - corrected_signal.mean()
            correction_strength = float(
                np.linalg.norm(corrected_signal - state_signal) / (np.linalg.norm(state_signal) + module.EPS)
            )

            state_offsets = list(range(-5, 6))
            state_centers = np.array([(target_dim + off) % nx for off in state_offsets], dtype=int)
            state_windows = np.stack(
                [module.cyclic_window(x_mean, int(center), module.WINDOW_SIZE) for center in state_centers],
                axis=0,
            )
            quantum_matrix = module.build_quantum_lookup(state_windows, obs_windows)

            distances = np.array(
                [module.cyclic_distance(target_dim, int(j), nx) for j in local_obs_idx],
                dtype=int,
            )
            best_match_pos = int(np.argmax(quantum_raw))
            nearest_pos = int(np.argmin(distances))
            weakest_pos = int(np.argmin(quantum_raw))
            window_offsets = np.arange(-(module.WINDOW_SIZE // 2), -(module.WINDOW_SIZE // 2) + module.WINDOW_SIZE)

            return {
                "time_step": target_time,
                "dimension": target_dim,
                "state_window": state_window,
                "state_signal": state_signal,
                "corrected_signal": corrected_signal,
                "correction_strength": correction_strength,
                "coupling": coupling,
                "local_obs_idx": local_obs_idx,
                "distances": distances,
                "obs_windows": obs_windows,
                "dist_prior": dist_prior,
                "quantum_raw": quantum_raw,
                "rho_weights": rho_weights,
                "corr_weights": corr_weights,
                "quantum_matrix": quantum_matrix,
                "state_centers": state_centers,
                "window_offsets": window_offsets,
                "best_match_pos": best_match_pos,
                "nearest_pos": nearest_pos,
                "weakest_pos": weakest_pos,
                "truth_series": truth[target_time],
                "observed_series": obs_vec,
                "x_mean_series": x_mean,
            }

        if np.any(~np.isnan(obs_vec)):
            ensemble, _ = module.letkf_update_weighted(
                ensemble=ensemble,
                obs_vec=obs_vec,
                obs_var=module.OBS_VAR,
                support_radius=module.SUPPORT_RADIUS,
                infl=module.INFL,
                method="rho_j_weak_fusion",
                lam_rho=lam_rho,
                lam_j=lam_j,
            )

    raise RuntimeError(f"未找到目标时间步: {target_time}")


def save_error_distribution(merged: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    bins = np.linspace(0.0, float(max(merged["abs_err_fixed"].max(), merged["abs_err_best"].max())), 45)
    ax.hist(
        merged["abs_err_fixed"],
        bins=bins,
        alpha=0.55,
        color="#c44e52",
        label="fixed absolute error",
        density=True,
    )
    ax.hist(
        merged["abs_err_best"],
        bins=bins,
        alpha=0.55,
        color="#4c72b0",
        label="exp37 absolute error",
        density=True,
    )
    ax.axvline(float(merged["abs_err_fixed"].mean()), color="#c44e52", linestyle="--", linewidth=1.5)
    ax.axvline(float(merged["abs_err_best"].mean()), color="#4c72b0", linestyle="--", linewidth=1.5)
    ax.set_title("exp37 与 fixed 的绝对误差分布对比")
    ax.set_xlabel("Absolute Error")
    ax.set_ylabel("Density")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_error_distribution.png", dpi=220)
    plt.close(fig)


def save_error_improvement_heatmap(merged: pd.DataFrame) -> None:
    heat = (
        merged.pivot(index="time_step", columns="dimension", values="gain_abs_err")
        .sort_index()
        .sort_index(axis=1)
    )
    vmax = float(np.nanpercentile(np.abs(heat.values), 98))
    fig, ax = plt.subplots(figsize=(12, 5.2))
    im = ax.imshow(heat.values, aspect="auto", cmap="coolwarm", vmin=-vmax, vmax=vmax)
    ax.set_title("exp37 相对 fixed 的绝对误差改善热力图")
    ax.set_xlabel("Dimension")
    ax.set_ylabel("Time Step")
    cbar = fig.colorbar(im, ax=ax, shrink=0.88)
    cbar.set_label("fixed abs error - exp37 abs error")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_error_improvement_heatmap.png", dpi=220)
    plt.close(fig)


def save_parameter_profiles(summary: pd.DataFrame) -> None:
    fusion = summary[summary["method"] == "rho_j_weak_fusion"].copy()
    fusion = fusion.sort_values(["lambda_rho", "lambda_j"])

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))

    for lam_rho, group in fusion.groupby("lambda_rho"):
        group = group.sort_values("lambda_j")
        axes[0].plot(
            group["lambda_j"],
            group["test_1_rmse"],
            marker="o",
            linewidth=2,
            label=f"lambda_rho={lam_rho:.2f}",
        )
    axes[0].set_title("固定 lambda_rho 时，lambda_j 对 RMSE 的影响")
    axes[0].set_xlabel("lambda_j")
    axes[0].set_ylabel("test_1 RMSE")
    axes[0].grid(alpha=0.25)
    axes[0].legend(frameon=False)

    for lam_j, group in fusion.groupby("lambda_j"):
        group = group.sort_values("lambda_rho")
        axes[1].plot(
            group["lambda_rho"],
            group["test_1_rmse"],
            marker="o",
            linewidth=2,
            label=f"lambda_j={lam_j:.3f}",
        )
    axes[1].set_title("固定 lambda_j 时，lambda_rho 对 RMSE 的影响")
    axes[1].set_xlabel("lambda_rho")
    axes[1].set_ylabel("test_1 RMSE")
    axes[1].grid(alpha=0.25)
    axes[1].legend(frameon=False)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_parameter_profiles.png", dpi=220)
    plt.close(fig)


def save_prediction_scatter(merged: pd.DataFrame) -> None:
    sample_n = min(3500, len(merged))
    sampled = merged.sample(sample_n, random_state=42)
    min_v = float(min(sampled["true_value"].min(), sampled["pred_best"].min(), sampled["pred_fixed"].min()))
    max_v = float(max(sampled["true_value"].max(), sampled["pred_best"].max(), sampled["pred_fixed"].max()))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharex=True, sharey=True)
    axes[0].scatter(sampled["true_value"], sampled["pred_fixed"], s=8, alpha=0.35, color="#c44e52")
    axes[1].scatter(sampled["true_value"], sampled["pred_best"], s=8, alpha=0.35, color="#4c72b0")
    for ax, title in zip(axes, ["fixed", "exp37 best"]):
        ax.plot([min_v, max_v], [min_v, max_v], color="black", linestyle="--", linewidth=1)
        ax.set_title(f"Truth vs Prediction: {title}")
        ax.set_xlabel("True Value")
        ax.set_ylabel("Predicted Value")
        ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_prediction_scatter.png", dpi=220)
    plt.close(fig)


def save_dimension_gain(merged: pd.DataFrame) -> None:
    dim_gain = merged.groupby("dimension", as_index=False)["gain_abs_err"].mean().sort_values("gain_abs_err", ascending=False)
    fig, ax = plt.subplots(figsize=(11.5, 4.6))
    colors = np.where(dim_gain["gain_abs_err"] >= 0, "#4c72b0", "#c44e52")
    ax.bar(dim_gain["dimension"].astype(str), dim_gain["gain_abs_err"], color=colors)
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_title("exp37 相对 fixed 的分维度平均误差改善")
    ax.set_xlabel("Dimension")
    ax.set_ylabel("Mean(abs_err_fixed - abs_err_exp37)")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_dimension_gain.png", dpi=220)
    plt.close(fig)


def save_time_rmse_trend(merged: pd.DataFrame) -> None:
    per_t = (
        merged.groupby("time_step")
        .apply(
            lambda g: pd.Series(
                {
                    "rmse_fixed": float(np.sqrt(np.mean(np.square(g["err_fixed"])))),
                    "rmse_best": float(np.sqrt(np.mean(np.square(g["err_best"])))),
                }
            )
        )
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(11.5, 4.6))
    ax.plot(per_t["time_step"], per_t["rmse_fixed"], color="#c44e52", linewidth=1.6, label="fixed")
    ax.plot(per_t["time_step"], per_t["rmse_best"], color="#4c72b0", linewidth=1.6, label="exp37")
    ax.set_title("逐时间步 RMSE 趋势：exp37 vs fixed")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("RMSE over 20 dimensions")
    ax.grid(alpha=0.2)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_time_rmse_trend.png", dpi=220)
    plt.close(fig)


def save_case_slices(merged: pd.DataFrame) -> None:
    per_t = (
        merged.groupby("time_step")["gain_abs_err"]
        .mean()
        .reset_index()
        .sort_values("gain_abs_err", ascending=False)
    )
    if len(per_t) >= 3:
        selected_times = [int(per_t.iloc[0]["time_step"]), int(per_t.iloc[len(per_t) // 2]["time_step"]), int(per_t.iloc[-1]["time_step"])]
    else:
        selected_times = sorted(merged["time_step"].unique()[:3].tolist())

    fig, axes = plt.subplots(len(selected_times), 1, figsize=(11, 3.4 * len(selected_times)), sharex=True)
    if len(selected_times) == 1:
        axes = [axes]

    for ax, t in zip(axes, selected_times):
        block = merged[merged["time_step"] == t].sort_values("dimension")
        ax.plot(block["dimension"], block["true_value"], color="black", linewidth=2, label="truth")
        ax.plot(block["dimension"], block["pred_fixed"], color="#c44e52", linewidth=1.6, label="fixed")
        ax.plot(block["dimension"], block["pred_best"], color="#4c72b0", linewidth=1.6, label="exp37")
        gain = float(block["gain_abs_err"].mean())
        ax.set_title(f"时间片 t={t} 的预测曲线对比，平均误差改善={gain:.4f}")
        ax.set_ylabel("State Value")
        ax.grid(alpha=0.2)
        ax.legend(frameon=False, ncol=3, fontsize=9)

    axes[-1].set_xlabel("Dimension")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_case_slices.png", dpi=220)
    plt.close(fig)


def save_timestep_gain_box(merged: pd.DataFrame) -> None:
    per_t = (
        merged.groupby("time_step")
        .apply(
            lambda g: pd.Series(
                {
                    "rmse_fixed": float(np.sqrt(np.mean(np.square(g["err_fixed"])))),
                    "rmse_best": float(np.sqrt(np.mean(np.square(g["err_best"])))),
                    "gain": float(np.mean(g["gain_abs_err"])),
                }
            )
        )
        .reset_index()
    )
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    axes[0].boxplot([per_t["rmse_fixed"], per_t["rmse_best"]], tick_labels=["fixed", "exp37"], patch_artist=True)
    axes[0].set_title("逐时间步 RMSE 分布")
    axes[0].set_ylabel("RMSE")
    axes[0].grid(axis="y", alpha=0.2)

    axes[1].hist(per_t["gain"], bins=36, color="#4c72b0", alpha=0.75)
    axes[1].axvline(float(per_t["gain"].mean()), color="black", linestyle="--", linewidth=1.3)
    axes[1].set_title("逐时间步平均误差改善分布")
    axes[1].set_xlabel("Mean(abs_err_fixed - abs_err_exp37)")
    axes[1].set_ylabel("Count")
    axes[1].grid(alpha=0.2)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_timestep_distribution.png", dpi=220)
    plt.close(fig)


def add_box(ax: plt.Axes, xy: tuple[float, float], width: float, height: float, text: str, color: str) -> None:
    box = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor=color,
        edgecolor="#2f2f2f",
        linewidth=1.2,
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=10)


def add_arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="->", linewidth=1.8, color="#333333"),
    )


def save_method_schematic(summary: pd.DataFrame) -> None:
    best_row = summary.loc[summary["test_1_rmse"].idxmin()]
    fig, ax = plt.subplots(figsize=(11.8, 5.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(ax, (0.05, 0.60), 0.18, 0.18, "Lorenz96 local state\n+ local observations", "#edf2ff")
    add_box(ax, (0.30, 0.60), 0.18, 0.18, "Quantum feature map\n(4 qubits)", "#e8f7ee")
    add_box(ax, (0.55, 0.68), 0.18, 0.12, "rho weighting\nmain control", "#fff3cd")
    add_box(ax, (0.55, 0.47), 0.18, 0.12, "J correction\nweak geometry tweak", "#fde2e4")
    add_box(ax, (0.79, 0.56), 0.16, 0.16, "LETKF update\nensemble subspace", "#e9ecef")

    add_arrow(ax, (0.23, 0.69), (0.30, 0.69))
    add_arrow(ax, (0.48, 0.69), (0.55, 0.74))
    add_arrow(ax, (0.48, 0.64), (0.55, 0.53))
    add_arrow(ax, (0.73, 0.74), (0.79, 0.66))
    add_arrow(ax, (0.73, 0.53), (0.79, 0.62))

    ax.text(0.08, 0.28, "Best setting", fontsize=12, fontweight="bold")
    ax.text(
        0.08,
        0.20,
        (
            f"lambda_rho = {best_row['lambda_rho']:.3f}\n"
            f"lambda_j = {best_row['lambda_j']:.3f}\n"
            f"test_1 RMSE = {best_row['test_1_rmse']:.6f}\n"
            f"avg J strength = {best_row['test_1_avg_j_correction_strength']:.6f}"
        ),
        fontsize=10.5,
    )
    ax.text(
        0.47,
        0.18,
        "Interpretation:\n"
        "1. rho remains the dominant observation selection signal.\n"
        "2. J only applies a weak directional correction.\n"
        "3. The best score appears when J is small but consistently positive.",
        fontsize=10.2,
        ha="left",
        va="center",
    )

    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_method_schematic.png", dpi=220)
    plt.close(fig)


def save_observed_truth_prediction_slice(merged: pd.DataFrame, case: dict[str, object]) -> None:
    target_time = int(case["time_step"])
    target_dim = int(case["dimension"])
    block = merged[merged["time_step"] == target_time].sort_values("dimension")
    avg_gain = float(block["gain_abs_err"].mean())

    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.plot(block["dimension"], block["true_value"], color="black", linewidth=2.0, label="truth")
    ax.plot(block["dimension"], block["pred_fixed"], color="#c44e52", linewidth=1.6, label="fixed")
    ax.plot(block["dimension"], block["pred_best"], color="#4c72b0", linewidth=1.8, label="exp37")
    ax.scatter(
        block["dimension"],
        block["observed_value"],
        color="#2ca02c",
        s=16,
        alpha=0.75,
        label="observed",
        zorder=3,
    )
    ax.axvline(target_dim, color="#1d4ed8", linestyle="--", linewidth=1.3)
    ax.set_title(f"代表性时间片 t={target_time} 的 truth / observed / fixed / exp37 对比")
    ax.set_xlabel("Dimension")
    ax.set_ylabel("Value")
    ax.text(
        0.01,
        0.98,
        f"平均绝对误差改善 = {avg_gain:.4f}，焦点维度 d={target_dim}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10,
        bbox=dict(facecolor="white", edgecolor="#cbd5e1", boxstyle="round,pad=0.25"),
    )
    ax.grid(alpha=0.2)
    ax.legend(frameon=False, ncol=4, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_observed_truth_fixed_best_slice.png", dpi=220)
    plt.close(fig)


def save_local_window_explanation(case: dict[str, object]) -> None:
    offsets = np.asarray(case["window_offsets"], dtype=int)
    state_window = np.asarray(case["state_window"], dtype=float)
    obs_windows = np.asarray(case["obs_windows"], dtype=float)
    best_match = int(case["best_match_pos"])
    nearest = int(case["nearest_pos"])
    weakest = int(case["weakest_pos"])
    local_obs_idx = np.asarray(case["local_obs_idx"], dtype=int)
    quantum_raw = np.asarray(case["quantum_raw"], dtype=float)
    state_signal = np.asarray(case["state_signal"], dtype=float)
    corrected_signal = np.asarray(case["corrected_signal"], dtype=float)
    correction_strength = float(case["correction_strength"])
    coupling = float(case["coupling"])

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

    axes[0].plot(offsets, state_window, marker="o", linewidth=2.2, color="black", label="局地状态窗口")
    axes[0].plot(
        offsets,
        obs_windows[best_match],
        marker="o",
        linewidth=1.8,
        color="#4c72b0",
        label=f"最佳匹配观测窗口 j={local_obs_idx[best_match]}",
    )
    axes[0].plot(
        offsets,
        obs_windows[nearest],
        marker="o",
        linewidth=1.6,
        color="#2ca02c",
        linestyle="--",
        label=f"最近观测窗口 j={local_obs_idx[nearest]}",
    )
    axes[0].plot(
        offsets,
        obs_windows[weakest],
        marker="o",
        linewidth=1.6,
        color="#c44e52",
        linestyle=":",
        label=f"最弱匹配观测窗口 j={local_obs_idx[weakest]}",
    )
    axes[0].set_title("局部窗口模式匹配解释")
    axes[0].set_xlabel("Window Offset")
    axes[0].set_ylabel("Window Value")
    axes[0].text(
        0.02,
        0.03,
        f"最佳匹配量子相似度={quantum_raw[best_match]:.4f}\n最弱匹配量子相似度={quantum_raw[weakest]:.4f}",
        transform=axes[0].transAxes,
        fontsize=9.5,
        ha="left",
        va="bottom",
        bbox=dict(facecolor="white", edgecolor="#cbd5e1", boxstyle="round,pad=0.25"),
    )
    axes[0].grid(alpha=0.2)
    axes[0].legend(frameon=False, fontsize=9)

    ens_idx = np.arange(len(state_signal))
    axes[1].plot(ens_idx, state_signal, color="#94a3b8", linewidth=1.8, label="原始状态扰动")
    axes[1].plot(ens_idx, corrected_signal, color="#7c3aed", linewidth=1.8, label="J 修正后扰动")
    axes[1].fill_between(ens_idx, state_signal, corrected_signal, color="#c4b5fd", alpha=0.35)
    axes[1].set_title("J 几何修正如何微调集合方向")
    axes[1].set_xlabel("Ensemble Member")
    axes[1].set_ylabel("Signal")
    axes[1].text(
        0.02,
        0.03,
        f"coupling={coupling:.4f}\n相对修正强度={correction_strength:.4f}",
        transform=axes[1].transAxes,
        fontsize=9.5,
        ha="left",
        va="bottom",
        bbox=dict(facecolor="white", edgecolor="#cbd5e1", boxstyle="round,pad=0.25"),
    )
    axes[1].grid(alpha=0.2)
    axes[1].legend(frameon=False)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_local_window_explanation.png", dpi=220)
    plt.close(fig)


def save_quantum_similarity_matrix(case: dict[str, object]) -> None:
    quantum_matrix = np.asarray(case["quantum_matrix"], dtype=float)
    state_centers = np.asarray(case["state_centers"], dtype=int)
    local_obs_idx = np.asarray(case["local_obs_idx"], dtype=int)
    target_dim = int(case["dimension"])
    target_row = int(np.where(state_centers == target_dim)[0][0])

    fig, ax = plt.subplots(figsize=(12.2, 5.2))
    im = ax.imshow(quantum_matrix, aspect="auto", cmap="viridis")
    ax.set_title("局地状态窗口与观测窗口的量子相似度矩阵")
    ax.set_xlabel("Observation Window Center")
    ax.set_ylabel("State Window Center")
    ax.set_xticks(np.arange(len(local_obs_idx)))
    ax.set_xticklabels(local_obs_idx.astype(str), rotation=90, fontsize=8)
    ax.set_yticks(np.arange(len(state_centers)))
    ax.set_yticklabels(state_centers.astype(str), fontsize=9)
    ax.axhline(target_row, color="white", linestyle="--", linewidth=1.2, alpha=0.9)
    cbar = fig.colorbar(im, ax=ax, shrink=0.9)
    cbar.set_label(r"Quantum overlap $|\langle \psi_x | \psi_y \rangle|^2$")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_quantum_similarity_matrix.png", dpi=220)
    plt.close(fig)


def save_rho_vs_corr_weights(case: dict[str, object]) -> None:
    local_obs_idx = np.asarray(case["local_obs_idx"], dtype=int)
    rho_weights = np.asarray(case["rho_weights"], dtype=float)
    corr_weights = np.asarray(case["corr_weights"], dtype=float)
    dist_prior = np.asarray(case["dist_prior"], dtype=float)
    distances = np.asarray(case["distances"], dtype=int)

    x = np.arange(len(local_obs_idx))
    width = 0.38
    fig, ax = plt.subplots(figsize=(12.5, 5))
    ax.bar(x - width / 2, rho_weights, width=width, color="#4c72b0", alpha=0.88, label="rho 融合权重")
    ax.bar(x + width / 2, corr_weights, width=width, color="#c44e52", alpha=0.80, label="corr 权重")
    ax.plot(x, dist_prior, color="#2ca02c", linewidth=1.4, marker="o", markersize=3.5, label="距离先验")
    ax.set_title("同一局地窗口下 rho 权重与 corr 权重对比")
    ax.set_xlabel("Local Observation Index")
    ax.set_ylabel("Normalized Weight")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{j}\n(dist={d})" for j, d in zip(local_obs_idx, distances)], fontsize=8)
    ax.grid(axis="y", alpha=0.2)
    ax.legend(frameon=False, ncol=3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "exp37_rho_vs_corr_weights.png", dpi=220)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    summary, truth, best, fixed, corr = load_data()
    merged = merge_predictions(truth, best, fixed, corr)
    exp37_module = load_exp37_module()
    best_row = summary.loc[summary["test_1_rmse"].idxmin()]
    target_time, target_dim = select_representative_case(merged)
    case = extract_local_case(
        exp37_module,
        target_time=target_time,
        target_dim=target_dim,
        lam_rho=float(best_row["lambda_rho"]),
        lam_j=float(best_row["lambda_j"]),
    )
    save_error_distribution(merged)
    save_error_improvement_heatmap(merged)
    save_parameter_profiles(summary)
    save_prediction_scatter(merged)
    save_dimension_gain(merged)
    save_time_rmse_trend(merged)
    save_case_slices(merged)
    save_timestep_gain_box(merged)
    save_method_schematic(summary)
    save_observed_truth_prediction_slice(merged, case)
    save_local_window_explanation(case)
    save_quantum_similarity_matrix(case)
    save_rho_vs_corr_weights(case)
    print("generated exp37 interpretability figures")


if __name__ == "__main__":
    main()
