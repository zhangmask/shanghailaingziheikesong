#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
量子增强4D-Var数据同化方案

核心创新：用PCA降阶局部化替代经验局部化函数
论文依据：arXiv 2511.07949 - 局部化的数学本质是投影到低维子空间

方案架构：
1. 经典主骨架：4D-Var
2. 量子子模块：PCA降阶局部化（密度矩阵特征分解）
3. 优化器：L-BFGS-B（经典，保证稳定性）
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Optional
from dataclasses import dataclass
from scipy.optimize import minimize
import warnings

# 导入量子模块
import sys
sys.path.insert(0, r'd:\Desktop\laingzimuxi\lunwenfenxi\4')
from pca_localization import PCALocalization, create_density_matrix_from_ensemble
from quantum_covariance import create_ensemble_density_matrix


# ============================================================================
# 1. Lorenz96 模型
# ============================================================================

class Lorenz96Model:
    """Lorenz96混沌模型"""
    
    def __init__(self, N: int = 40, F: float = 8.0):
        self.N = N
        self.F = F
    
    def derivative(self, x: np.ndarray) -> np.ndarray:
        """计算Lorenz96导数"""
        dx = np.zeros(self.N)
        for i in range(self.N):
            x_next = x[(i + 1) % self.N]
            x_prev1 = x[(i - 1) % self.N]
            x_prev2 = x[(i - 2) % self.N]
            dx[i] = (x_next - x_prev2) * x_prev1 - x[i] + self.F
        return dx
    
    def propagate(self, x: np.ndarray, dt: float = 0.05, n_steps: int = 1) -> np.ndarray:
        """RK4传播"""
        x_current = x.copy()
        for _ in range(n_steps):
            k1 = self.derivative(x_current)
            k2 = self.derivative(x_current + 0.5 * dt * k1)
            k3 = self.derivative(x_current + 0.5 * dt * k2)
            k4 = self.derivative(x_current + dt * k3)
            x_current += (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        return x_current


# ============================================================================
# 2. 量子增强局部化
# ============================================================================

class QuantumEnhancedLocalization:
    """量子增强局部化模块"""
    
    def __init__(
        self,
        variance_threshold: float = 0.95,
        ensemble_size: int = 20,
        perturbation_scale: float = 0.1
    ):
        """
        初始化量子增强局部化
        
        参数:
            variance_threshold: PCA方差阈值（决定保留的主成分数r）
            ensemble_size: 系综大小
            perturbation_scale: 背景扰动幅度
        """
        self.variance_threshold = variance_threshold
        self.ensemble_size = ensemble_size
        self.perturbation_scale = perturbation_scale
        
        self.pca_filter = PCALocalization(
            variance_threshold=variance_threshold
        )
    
    def build_background_ensemble(
        self,
        background_state: np.ndarray,
        model: Lorenz96Model
    ) -> List[np.ndarray]:
        """
        构建背景系综
        
        方法：在背景场上添加随机扰动
        """
        ensemble = []
        for _ in range(self.ensemble_size):
            perturbation = np.random.randn(model.N) * self.perturbation_scale
            ensemble.append(background_state + perturbation)
        return ensemble
    
    def compute_quantum_localized_covariance(
        self,
        ensemble: List[np.ndarray]
    ) -> Tuple[np.ndarray, dict]:
        """
        计算量子增强局部化协方差
        
        核心步骤：
        1. 从系综构建密度矩阵 ρ = Σ w_k |ψ_k⟩⟨ψ_k|
        2. 对ρ做特征分解
        3. 保留前r个主成分（方差阈值决定）
        4. 重构降阶协方差
        
        返回:
            (协方差矩阵, 元数据)
        """
        # 构建密度矩阵
        rho = create_density_matrix_from_ensemble(ensemble)
        
        # PCA降阶
        pca_result = self.pca_filter.localize(rho)
        
        # 从降阶密度矩阵提取协方差
        # 注意：密度矩阵是复数的，取实部作为协方差估计
        cov_matrix = pca_result.rho_reduced.real
        
        # 对称化（协方差必须对称）
        cov_matrix = (cov_matrix + cov_matrix.T) / 2
        
        # 确保正定（加小量到对角线）
        min_eig = np.min(np.linalg.eigvalsh(cov_matrix))
        if min_eig < 1e-10:
            cov_matrix += np.eye(cov_matrix.shape[0]) * (1e-6 - min_eig)
        
        metadata = {
            'n_components': pca_result.n_components,
            'reconstruction_error': pca_result.reconstruction_error,
            'explained_variance': np.sum(pca_result.explained_variance_ratio),
            'eigenvalues': pca_result.eigenvalues[:pca_result.n_components]
        }
        
        return cov_matrix, metadata
    
    def get_localization_operator(
        self,
        ensemble: List[np.ndarray]
    ) -> np.ndarray:
        """
        获取局部化算子 L，使得 B = L L^T
        
        使用PCA主成分作为局部化基
        """
        rho = create_density_matrix_from_ensemble(ensemble)
        pca_result = self.pca_filter.localize(rho)
        
        # 返回主成分矩阵
        return pca_result.eigenvectors[:, :pca_result.n_components]


# ============================================================================
# 3. 4D-Var 代价函数
# ============================================================================

def create_4dvar_cost_function(
    model: Lorenz96Model,
    xb: np.ndarray,
    observations: dict,
    B_inv: np.ndarray,
    R: np.ndarray,
    dt: float = 0.05,
    obs_interval: int = 2
) -> callable:
    """
    创建4D-Var代价函数
    
    J(x0) = 1/2 (x0-xb)^T B^{-1} (x0-xb) + 
            1/2 Σ_k (y_k - H x_k)^T R^{-1} (y_k - H x_k)
    
    其中 x_k = M^k(x0)
    """
    # 预计算 R^{-1}
    R_inv = np.linalg.inv(R)
    
    def cost_function(x0: np.ndarray) -> float:
        """计算代价函数值"""
        # 背景项
        bg_term = 0.5 * (x0 - xb) @ B_inv @ (x0 - xb)
        
        # 观测项
        obs_term = 0.0
        x_current = x0.copy()
        
        for k, (time_step, y_k) in enumerate(observations.items()):
            # 传播到观测时刻
            if k > 0:
                steps = obs_interval
                x_current = model.propagate(x_current, dt, steps)
            
            # 计算观测残差（H = I）
            residual = y_k - x_current
            obs_term += 0.5 * residual @ R_inv @ residual
        
        return bg_term + obs_term
    
    return cost_function


def create_4dvar_gradient(
    model: Lorenz96Model,
    xb: np.ndarray,
    observations: dict,
    B_inv: np.ndarray,
    R: np.ndarray,
    dt: float = 0.05,
    obs_interval: int = 2
) -> callable:
    """
    创建4D-Var梯度函数（伴随方法）
    """
    R_inv = np.linalg.inv(R)
    
    def gradient(x0: np.ndarray) -> np.ndarray:
        """计算梯度"""
        # 前向传播，存储轨迹
        trajectory = [x0.copy()]
        x_current = x0.copy()
        
        for k in range(max(observations.keys())):
            x_current = model.propagate(x_current, dt, obs_interval)
            trajectory.append(x_current.copy())
        
        # 伴随变量初始化
        adjoint = np.zeros(model.N)
        
        # 反向传播
        for k in sorted(observations.keys(), reverse=True):
            y_k = observations[k]
            x_k = trajectory[k]
            
            # 观测梯度
            residual = x_k - y_k
            grad_obs = R_inv @ residual
            adjoint += grad_obs
            
            # 伴随传播（线性化模型）
            # 简化：用有限差分近似伴随
            eps = 1e-6
            adjoint_propagated = np.zeros(model.N)
            for i in range(model.N):
                x_perturb = trajectory[k-1].copy()
                x_perturb[i] += eps
                x_forward = model.propagate(x_perturb, dt, obs_interval)
                x_unperturbed = trajectory[k]
                adjoint_propagated[i] = np.dot(adjoint, (x_forward - x_unperturbed)) / eps
            adjoint = adjoint_propagated
        
        # 背景梯度
        grad_bg = B_inv @ (x0 - xb)
        
        return grad_bg + adjoint
    
    return gradient


# ============================================================================
# 4. 量子增强4D-Var主流程
# ============================================================================

@dataclass
class Quantum4DVarResult:
    """量子增强4D-Var结果"""
    x0_optimal: np.ndarray  # 最优初始状态
    trajectory: List[np.ndarray]  # 最优轨迹
    cost_value: float  # 代价函数值
    localization_metadata: dict  # 局部化元数据
    n_iterations: int  # 优化迭代次数


def quantum_enhanced_4dvar(
    model: Lorenz96Model,
    xb: np.ndarray,
    observations: dict,
    ensemble: List[np.ndarray],
    R: np.ndarray,
    dt: float = 0.05,
    max_iter: int = 100
) -> Quantum4DVarResult:
    """
    量子增强4D-Var
    
    核心创新：用量子PCA降阶局部化估计背景协方差B
    """
    print("=" * 60)
    print("量子增强4D-Var 数据同化")
    print("=" * 60)
    
    # 步骤1：量子增强局部化
    print("\n[步骤1] 量子增强局部化...")
    localization = QuantumEnhancedLocalization(variance_threshold=0.95)
    B, loc_metadata = localization.compute_quantum_localized_covariance(ensemble)
    
    print(f"  密度矩阵维度: {B.shape}")
    print(f"  保留主成分数: {loc_metadata['n_components']}")
    print(f"  解释方差比例: {loc_metadata['explained_variance']:.4f}")
    print(f"  重构误差: {loc_metadata['reconstruction_error']:.6f}")
    
    # 计算 B^{-1}
    B_inv = np.linalg.inv(B)
    
    # 步骤2：构建代价函数
    print("\n[步骤2] 构建4D-Var代价函数...")
    cost_func = create_4dvar_cost_function(
        model, xb, observations, B_inv, R, dt=dt
    )
    
    # 步骤3：优化求解
    print("\n[步骤3] 优化求解...")
    result = minimize(
        cost_func,
        xb,
        method='L-BFGS-B',
        options={'maxiter': max_iter, 'disp': False}
    )
    
    x0_optimal = result.x
    cost_value = result.fun
    n_iterations = result.nit
    
    print(f"  最优代价函数值: {cost_value:.6f}")
    print(f"  优化迭代次数: {n_iterations}")
    
    # 步骤4：生成最优轨迹
    print("\n[步骤4] 生成最优轨迹...")
    trajectory = [x0_optimal.copy()]
    x_current = x0_optimal.copy()
    
    for k in range(max(observations.keys())):
        x_current = model.propagate(x_current, dt, n_steps=2)
        trajectory.append(x_current.copy())
    
    print(f"  轨迹长度: {len(trajectory)}")
    
    return Quantum4DVarResult(
        x0_optimal=x0_optimal,
        trajectory=trajectory,
        cost_value=cost_value,
        localization_metadata=loc_metadata,
        n_iterations=n_iterations
    )


# ============================================================================
# 5. 经典4D-Var基线（用于对比）
# ============================================================================

def classical_4dvar(
    model: Lorenz96Model,
    xb: np.ndarray,
    observations: dict,
    B: np.ndarray,
    R: np.ndarray,
    dt: float = 0.05,
    max_iter: int = 100
) -> Quantum4DVarResult:
    """经典4D-Var基线"""
    print("=" * 60)
    print("经典4D-Var 数据同化（基线）")
    print("=" * 60)
    
    B_inv = np.linalg.inv(B)
    
    cost_func = create_4dvar_cost_function(
        model, xb, observations, B_inv, R, dt=dt
    )
    
    result = minimize(
        cost_func,
        xb,
        method='L-BFGS-B',
        options={'maxiter': max_iter, 'disp': False}
    )
    
    x0_optimal = result.x
    cost_value = result.fun
    n_iterations = result.nit
    
    trajectory = [x0_optimal.copy()]
    x_current = x0_optimal.copy()
    
    for k in range(max(observations.keys())):
        x_current = model.propagate(x_current, dt, n_steps=2)
        trajectory.append(x_current.copy())
    
    return Quantum4DVarResult(
        x0_optimal=x0_optimal,
        trajectory=trajectory,
        cost_value=cost_value,
        localization_metadata={'method': 'classical'},
        n_iterations=n_iterations
    )


# ============================================================================
# 6. 主程序
# ============================================================================

def main():
    """主程序"""
    print("=" * 60)
    print("量子增强4D-Var 数据同化方案演示")
    print("=" * 60)
    
    # 参数设置
    N = 40
    F = 8.0
    dt = 0.05
    obs_interval = 2
    n_obs_steps = 20  # 观测时间步数
    
    # 初始化模型
    model = Lorenz96Model(N=N, F=F)
    
    # 生成真值轨迹
    np.random.seed(42)
    true_initial = np.random.randn(N) * 0.1
    true_initial += np.sin(np.linspace(0, 4*np.pi, N))
    true_trajectory = [true_initial.copy()]
    x_true = true_initial.copy()
    
    for _ in range(n_obs_steps):
        x_true = model.propagate(x_true, dt, obs_interval)
        true_trajectory.append(x_true.copy())
    
    # 生成观测（带噪声）
    obs_noise_std = 0.5
    observations = {}
    for k in range(0, n_obs_steps + 1, obs_interval):
        y_k = true_trajectory[k] + np.random.randn(N) * obs_noise_std
        observations[k] = y_k
    
    # 背景场（带误差）
    xb = true_trajectory[0] + np.random.randn(N) * 0.5
    
    # 观测误差协方差
    R = np.eye(N) * (obs_noise_std ** 2)
    
    # 生成背景系综
    ensemble = []
    for _ in range(20):
        perturbation = np.random.randn(N) * 0.1
        ensemble.append(xb + perturbation)
    
    # 经典背景协方差（用于对比）
    ensemble_array = np.array(ensemble)
    centered = ensemble_array - np.mean(ensemble_array, axis=0)
    B_classical = np.cov(centered, rowvar=False)
    # 加局部化
    loc_radius = 10
    loc_matrix = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            dist = min(abs(i - j), N - abs(i - j))
            if dist < loc_radius:
                loc_matrix[i, j] = np.exp(-0.5 * (dist / loc_radius) ** 2)
    B_classical_loc = B_classical * loc_matrix
    
    # 运行量子增强4D-Var
    print("\n" + "=" * 60)
    result_quantum = quantum_enhanced_4dvar(
        model, xb, observations, ensemble, R, dt=dt
    )
    
    # 运行经典4D-Var
    print("\n" + "=" * 60)
    result_classical = classical_4dvar(
        model, xb, observations, B_classical_loc, R, dt=dt
    )
    
    # 计算RMSE
    print("\n" + "=" * 60)
    print("结果对比")
    print("=" * 60)
    
    rmse_quantum = []
    rmse_classical = []
    
    for k, (t, true_x) in enumerate(true_trajectory):
        pred_quantum = result_quantum.trajectory[k]
        pred_classical = result_classical.trajectory[k]
        
        rmse_q = np.sqrt(np.mean((pred_quantum - true_x) ** 2))
        rmse_c = np.sqrt(np.mean((pred_classical - true_x) ** 2))
        
        rmse_quantum.append(rmse_q)
        rmse_classical.append(rmse_c)
    
    print(f"\n{'时间步':<10} {'真值RMSE(量子)':<18} {'真值RMSE(经典)':<18} {'改进':<10}")
    print("-" * 60)
    
    for k in range(len(true_trajectory)):
        improvement = rmse_classical[k] - rmse_quantum[k]
        print(f"{k:<10} {rmse_quantum[k]:<18.6f} {rmse_classical[k]:<18.6f} {improvement:+<10.6f}")
    
    avg_rmse_q = np.mean(rmse_quantum)
    avg_rmse_c = np.mean(rmse_classical)
    
    print("-" * 60)
    print(f"{'平均RMSE':<10} {avg_rmse_q:<18.6f} {avg_rmse_c:<18.6f} {avg_rmse_c - avg_rmse_q:+<10.6f}")
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)
    
    return result_quantum, result_classical


if __name__ == "__main__":
    main()
