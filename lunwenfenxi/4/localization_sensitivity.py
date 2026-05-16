#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
局部化敏感性分析模块

基于Lorenz96模型测试不同局部化方法的效果
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
import warnings

# 导入已实现的模块
from quantum_covariance import (
    QuantumCovarianceEstimator,
    Observable,
    QuantumState,
    create_ensemble_density_matrix,
    create_localized_observables,
    compare_quantum_classical_covariance
)
from pca_localization import (
    PCALocalization,
    create_density_matrix_from_ensemble,
    compare_localization_methods
)


@dataclass
class Lorenz96State:
    """Lorenz96系统状态"""
    x: np.ndarray  # 状态向量，长度N
    t: float  # 时间


class Lorenz96Model:
    """Lorenz96模型"""
    
    def __init__(self, N: int = 40, F: float = 8.0, g: float = 1.0):
        """
        初始化Lorenz96模型
        
        参数:
            N: 变量数量
            F: 外力参数
            g: 耗散参数
        """
        self.N = N
        self.F = F
        self.g = g
    
    def derivative(self, x: np.ndarray) -> np.ndarray:
        """
        计算Lorenz96的导数
        
        dx_i/dt = (x_{i+1} - x_{i-2}) * x_{i-1} - x_i + F
        
        参数:
            x: 状态向量
        
        返回:
            导数向量
        """
        dx = np.zeros(self.N)
        for i in range(self.N):
            x_next = x[(i + 1) % self.N]
            x_prev1 = x[(i - 1) % self.N]
            x_prev2 = x[(i - 2) % self.N]
            dx[i] = (x_next - x_prev2) * x_prev1 - x[i] + self.F
        return dx
    
    def propagate(self, x: np.ndarray, dt: float = 0.05, n_steps: int = 1) -> np.ndarray:
        """
        传播状态
        
        参数:
            x: 初始状态
            dt: 时间步长
            n_steps: 步数
        
        返回:
            传播后的状态
        """
        x_current = x.copy()
        for _ in range(n_steps):
            dx = self.derivative(x_current)
            x_current += dx * dt
        return x_current
    
    def generate_ensemble(
        self,
        n_ensemble: int,
        initial_state: np.ndarray,
        perturbation_scale: float = 0.1
    ) -> List[np.ndarray]:
        """
        生成系综
        
        参数:
            n_ensemble: 系综大小
            initial_state: 初始状态
            perturbation_scale: 扰动幅度
        
        返回:
            系综状态列表
        """
        ensemble = []
        for _ in range(n_ensemble):
            perturbation = np.random.randn(self.N) * perturbation_scale
            ensemble.append(initial_state + perturbation)
        return ensemble
    
    def generate_true_trajectory(
        self,
        initial_state: np.ndarray,
        n_steps: int,
        dt: float = 0.05
    ) -> List[np.ndarray]:
        """
        生成真值轨迹
        
        参数:
            initial_state: 初始状态
            n_steps: 步数
            dt: 时间步长
        
        返回:
            轨迹列表
        """
        trajectory = []
        x_current = initial_state.copy()
        for _ in range(n_steps):
            trajectory.append(x_current.copy())
            x_current = self.propagate(x_current, dt)
        return trajectory


def classical_localization_gaussian(
    cov_matrix: np.ndarray,
    loc_radius: int
) -> np.ndarray:
    """
    经典局部化（高斯函数）
    
    参数:
        cov_matrix: 协方差矩阵
        loc_radius: 局部化半径
    
    返回:
        局部化后的协方差矩阵
    """
    n = cov_matrix.shape[0]
    loc_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            # 周期性边界
            dist = min(abs(i - j), n - abs(i - j))
            if dist < loc_radius:
                loc_matrix[i, j] = np.exp(-0.5 * (dist / loc_radius) ** 2)
            else:
                loc_matrix[i, j] = 0.0
    
    return cov_matrix * loc_matrix


def classical_localization_gaspari_cohn(
    cov_matrix: np.ndarray,
    loc_radius: int
) -> np.ndarray:
    """
    经典局部化（Gaspari-Cohn函数）
    
    参数:
        cov_matrix: 协方差矩阵
        loc_radius: 局部化半径
    
    返回:
        局部化后的协方差矩阵
    """
    n = cov_matrix.shape[0]
    loc_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            # 周期性边界
            dist = min(abs(i - j), n - abs(i - j))
            s = dist / loc_radius
            
            if s >= 2:
                loc_matrix[i, j] = 0.0
            elif s >= 1:
                loc_matrix[i, j] = (-0.25 * s**4 + 0.5 * s**3 + 0.25 * s**2 - 0.5 * s + 1/6)
            else:
                loc_matrix[i, j] = (-0.25 * s**5 + 0.5 * s**4 + 5/8 * s**3 - 5/3 * s**2 + 1)
    
    return cov_matrix * loc_matrix


def run_localization_sensitivity_experiment(
    n_vars: int = 40,
    n_ensemble: int = 20,
    loc_radii: List[int] = None,
    n_steps: int = 10
) -> dict:
    """
    运行局部化敏感性实验
    
    参数:
        n_vars: 变量数
        n_ensemble: 系综大小
        loc_radii: 局部化半径列表
        n_steps: 同化步数
    
    返回:
        实验结果字典
    """
    if loc_radii is None:
        loc_radii = [5, 10, 15, 20, 25, 30]
    
    # 初始化模型
    model = Lorenz96Model(N=n_vars, F=8.0)
    
    # 生成初始状态
    np.random.seed(42)
    initial_state = np.random.randn(n_vars) * 0.1
    initial_state += np.sin(np.linspace(0, 4*np.pi, n_vars))
    
    # 生成真值轨迹
    true_trajectory = model.generate_true_trajectory(initial_state, n_steps)
    
    # 生成系综
    ensemble = model.generate_ensemble(n_ensemble, initial_state, perturbation_scale=0.1)
    
    results = {
        'loc_radii': loc_radii,
        'rmse_by_radius': [],
        'quantum_vs_classical': [],
        'pca_vs_classical': []
    }
    
    for loc_radius in loc_radii:
        # 对每个半径，运行简单的同化实验
        ensemble_current = [s.copy() for s in ensemble]
        
        rmse_history = []
        
        for step in range(n_steps):
            true_state = true_trajectory[step]
            
            # 计算系综均值
            ensemble_array = np.array(ensemble_current)
            mean_state = np.mean(ensemble_array, axis=0)
            
            # RMSE
            rmse = np.sqrt(np.mean((mean_state - true_state) ** 2))
            rmse_history.append(rmse)
            
            # 计算协方差
            centered = ensemble_array - mean_state
            cov_matrix = np.cov(centered, rowvar=False)
            
            # 应用局部化
            loc_cov = classical_localization_gaussian(cov_matrix, loc_radius)
            
            # 简单的观测更新（假设观测 = 状态 + 噪声）
            observation = true_state + np.random.randn(n_vars) * 0.5
            
            # 卡尔曼更新
            innovation = observation - mean_state
            innovation_cov = loc_cov + np.eye(n_vars) * 0.25
            
            # 简化版：直接更新
            kalman_gain = loc_cov @ np.linalg.inv(innovation_cov)
            mean_updated = mean_state + kalman_gain @ innovation
            
            # 扰动观测（集合扰动）
            for i in range(n_ensemble):
                perturbation = np.random.randn(n_vars) * 0.5
                ensemble_current[i] = mean_updated + perturbation
            
            # 模型传播
            for i in range(n_ensemble):
                ensemble_current[i] = model.propagate(ensemble_current[i], dt=0.05)
        
        # 平均RMSE
        avg_rmse = np.mean(rmse_history)
        results['rmse_by_radius'].append(avg_rmse)
    
    return results


def compare_methods_detailed(
    n_vars: int = 40,
    n_ensemble: int = 20,
    loc_radius: int = 10
) -> dict:
    """
    详细对比不同方法
    
    参数:
        n_vars: 变量数
        n_ensemble: 系综大小
        loc_radius: 局部化半径
    
    返回:
        对比结果
    """
    # 生成系综
    np.random.seed(42)
    ensemble = []
    for _ in range(n_ensemble):
        state = np.random.randn(n_vars) * 0.1
        state += np.sin(np.linspace(0, 4*np.pi, n_vars))
        ensemble.append(state)
    
    # 经典协方差
    ensemble_array = np.array(ensemble)
    mean_state = np.mean(ensemble_array, axis=0)
    centered = ensemble_array - mean_state
    classical_cov = np.cov(centered, rowvar=False)
    
    # 经典局部化
    classical_loc_cov = classical_localization_gaussian(classical_cov, loc_radius)
    
    # 量子协方差
    rho = create_density_matrix_from_ensemble(ensemble)
    observables, obs_start, obs_end = create_localized_observables(n_vars, loc_radius)
    estimator = QuantumCovarianceEstimator(observables)
    quantum_cov = estimator.compute_covariance(QuantumState(rho=rho, basis_names=[]))
    
    # PCA局部化
    pca_filter = PCALocalization(variance_threshold=0.95)
    pca_result = pca_filter.localize(rho)
    
    # 提取经典协方差的对应窗口部分
    n_position_obs = obs_end - obs_start  # 位置算子数量
    classical_cov_local = classical_cov[obs_start:obs_end, obs_start:obs_end]
    classical_loc_cov_local = classical_loc_cov[obs_start:obs_end, obs_start:obs_end]
    
    # 量子协方差只包含位置算子部分（前n_position_obs个）
    quantum_cov_position = quantum_cov[:n_position_obs, :n_position_obs]
    
    # 计算误差
    classical_error = np.linalg.norm(classical_cov - classical_loc_cov, 'fro') / np.linalg.norm(classical_cov, 'fro')
    quantum_error = np.linalg.norm(quantum_cov_position.real - classical_loc_cov_local, 'fro') / np.linalg.norm(classical_cov_local, 'fro')
    pca_error = pca_result.reconstruction_error
    
    return {
        'classical_localization_error': classical_error,
        'quantum_covariance_error': quantum_error,
        'pca_localization_error': pca_error,
        'pca_n_components': pca_result.n_components,
        'quantum_nonclassical': np.linalg.norm(estimator.compute_anticommutator_part(QuantumState(rho=rho, basis_names=[])), 'fro') > 1e-10
    }


def main():
    """演示局部化敏感性分析"""
    print("=" * 60)
    print("局部化敏感性分析（Lorenz96）")
    print("=" * 60)
    
    # 示例1：局部化半径敏感性
    print("\n【示例1】局部化半径敏感性")
    print("-" * 40)
    
    experiment_results = run_localization_sensitivity_experiment(
        n_vars=40,
        n_ensemble=20,
        loc_radii=[5, 10, 15, 20, 25, 30]
    )
    
    print(f"{'局部化半径':<12} {'平均RMSE':<15}")
    print("-" * 30)
    for radius, rmse in zip(experiment_results['loc_radii'], experiment_results['rmse_by_radius']):
        print(f"{radius:<12} {rmse:<15.6f}")
    
    # 示例2：方法对比
    print("\n【示例2】方法对比")
    print("-" * 40)
    
    for loc_radius in [5, 10, 15, 20]:
        result = compare_methods_detailed(n_vars=40, n_ensemble=20, loc_radius=loc_radius)
        print(f"\n局部化半径 = {loc_radius}:")
        print(f"  经典局部化误差: {result['classical_localization_error']:.6f}")
        print(f"  量子协方差误差: {result['quantum_covariance_error']:.6f}")
        print(f"  PCA局部化误差:  {result['pca_localization_error']:.6f}")
        print(f"  PCA保留维度:    {result['pca_n_components']}")
        print(f"  非经典相关:     {result['quantum_nonclassical']}")
    
    # 示例3：综合敏感性分析
    print("\n【示例3】综合敏感性分析")
    print("-" * 40)
    
    print(f"{'半径':<8} {'经典误差':<12} {'量子误差':<12} {'PCA误差':<12} {'PCA维度':<8}")
    print("-" * 55)
    
    for loc_radius in [5, 10, 15, 20]:
        result = compare_methods_detailed(n_vars=40, n_ensemble=20, loc_radius=loc_radius)
        print(f"{loc_radius:<8} {result['classical_localization_error']:<12.6f} "
              f"{result['quantum_covariance_error']:<12.6f} {result['pca_localization_error']:<12.6f} "
              f"{result['pca_n_components']:<8}")
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
