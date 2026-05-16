#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于PCA的局部化模块

核心思想：局部化的数学本质是投影到低维子空间
- 对密度矩阵做特征分解
- 保留前r个主成分（特征值最大的）
- 重构降阶密度矩阵

对应经典DA：
- 局部化半径 → 子空间维度 r
- 经验函数 φ(|i-j|) → 数学投影操作
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
import warnings


@dataclass
class PCAFilterResult:
    """PCA降阶滤波结果"""
    # 降阶密度矩阵
    rho_reduced: np.ndarray
    # 保留的主成分数
    n_components: int
    # 特征值（按大小排序）
    eigenvalues: np.ndarray
    # 特征向量
    eigenvectors: np.ndarray
    # 重构误差
    reconstruction_error: float
    # 解释方差比例
    explained_variance_ratio: np.ndarray


class PCALocalization:
    """基于PCA的局部化滤波器"""
    
    def __init__(
        self,
        variance_threshold: float = 0.95,
        max_components: Optional[int] = None,
        min_components: int = 1
    ):
        """
        初始化PCA局部化滤波器
        
        参数:
            variance_threshold: 保留的方差比例（0-1），默认0.95
            max_components: 最大主成分数，None表示无限制
            min_components: 最小主成分数
        """
        self.variance_threshold = variance_threshold
        self.max_components = max_components
        self.min_components = min_components
    
    def localize(self, rho: np.ndarray) -> PCAFilterResult:
        """
        对密度矩阵进行PCA降阶局部化
        
        参数:
            rho: 密度矩阵，形状 (N, N)
        
        返回:
            PCAFilterResult 对象
        """
        # 验证密度矩阵
        if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
            raise ValueError("密度矩阵必须是方阵")
        
        N = rho.shape[0]
        
        # 特征分解（密度矩阵是半正定的）
        eigenvalues, eigenvectors = np.linalg.eigh(rho)
        
        # 按特征值从大到小排序
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # 确定保留的主成分数
        # 方法1：基于方差阈值
        total_variance = np.sum(eigenvalues)
        cumsum = np.cumsum(eigenvalues) / total_variance
        
        # 找到满足阈值的最小n
        n_by_threshold = np.searchsorted(cumsum, self.variance_threshold) + 1
        
        # 方法2：基于最大/最小限制
        if self.max_components is not None:
            n_components = min(n_by_threshold, self.max_components)
        else:
            n_components = n_by_threshold
        
        n_components = max(n_components, self.min_components)
        n_components = min(n_components, N)
        
        # 保留前n_components个主成分
        retained_eigenvalues = eigenvalues[:n_components]
        retained_eigenvectors = eigenvectors[:, :n_components]
        
        # 重构降阶密度矩阵
        # ρ_r = Σ_{i=1}^{r} λ_i |ψ_i⟩⟨ψ_i|
        rho_reduced = retained_eigenvectors @ np.diag(retained_eigenvalues) @ retained_eigenvectors.conj().T
        
        # 计算重构误差
        reconstruction_error = np.linalg.norm(rho - rho_reduced, 'fro') / np.linalg.norm(rho, 'fro')
        
        # 计算解释方差比例
        explained_variance_ratio = retained_eigenvalues / total_variance
        
        return PCAFilterResult(
            rho_reduced=rho_reduced,
            n_components=n_components,
            eigenvalues=eigenvalues,
            eigenvectors=eigenvectors,
            reconstruction_error=reconstruction_error,
            explained_variance_ratio=explained_variance_ratio
        )
    
    def analyze_localization_error(
        self,
        rho: np.ndarray,
        n_components_range: List[int] = None
    ) -> dict:
        """
        分析不同主成分数下的局部化误差
        
        参数:
            rho: 密度矩阵
            n_components_range: 主成分数范围列表
        
        返回:
            分析结果字典
        """
        if n_components_range is None:
            n_components_range = list(range(1, rho.shape[0] + 1))
        
        errors = []
        explained_variances = []
        
        for n in n_components_range:
            # 特征分解
            eigenvalues, eigenvectors = np.linalg.eigh(rho)
            idx = np.argsort(eigenvalues)[::-1]
            eigenvalues_sorted = eigenvalues[idx]
            
            # 重构
            retained_eigenvalues = eigenvalues_sorted[:n]
            retained_eigenvectors = eigenvectors[:, idx[:n]]
            rho_reduced = retained_eigenvectors @ np.diag(retained_eigenvalues) @ retained_eigenvectors.conj().T
            
            # 误差
            error = np.linalg.norm(rho - rho_reduced, 'fro') / np.linalg.norm(rho, 'fro')
            errors.append(error)
            
            # 解释方差
            total_var = np.sum(eigenvalues_sorted)
            explained_var = np.sum(retained_eigenvalues) / total_var
            explained_variances.append(explained_var)
        
        return {
            'n_components': n_components_range,
            'reconstruction_errors': np.array(errors),
            'explained_variances': np.array(explained_variances)
        }


def create_density_matrix_from_ensemble(
    ensemble_states: List[np.ndarray],
    weights: Optional[List[float]] = None
) -> np.ndarray:
    """
    从系综构建密度矩阵
    
    ρ = Σ_k w_k |ψ_k⟩⟨ψ_k|
    
    参数:
        ensemble_states: 纯态列表，每个形状 (N,)
        weights: 权重列表，默认等权重
    
    返回:
        密度矩阵，形状 (N, N)
    """
    N = ensemble_states[0].shape[0]
    n_states = len(ensemble_states)
    
    if weights is None:
        weights = [1.0 / n_states] * n_states
    
    # 归一化权重
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]
    
    # 构建密度矩阵
    rho = np.zeros((N, N), dtype=complex)
    for psi, w in zip(ensemble_states, weights):
        psi = psi / np.linalg.norm(psi)  # 确保归一化
        rho += w * np.outer(psi, psi.conj())
    
    return rho


def compare_localization_methods(
    ensemble_states: List[np.ndarray],
    n_vars: int,
    window_size: int = 10,
    variance_threshold: float = 0.95
) -> dict:
    """
    对比不同局部化方法的效果
    
    参数:
        ensemble_states: 系综状态列表
        n_vars: 总变量数
        window_size: 窗口大小
        variance_threshold: PCA方差阈值
    
    返回:
        对比结果字典
    """
    # 构建密度矩阵
    rho = create_density_matrix_from_ensemble(ensemble_states)
    
    # 方法1：经典局部化（高斯函数）
    def classical_localization(cov_matrix: np.ndarray, loc_radius: int) -> np.ndarray:
        """经典局部化（Gaspari-Cohn函数的简化版）"""
        n = cov_matrix.shape[0]
        loc_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                dist = abs(i - j)
                if dist < loc_radius:
                    # 简化版：高斯函数
                    loc_matrix[i, j] = np.exp(-0.5 * (dist / loc_radius) ** 2)
                else:
                    loc_matrix[i, j] = 0.0
        return cov_matrix * loc_matrix
    
    # 方法2：基于PCA的局部化
    pca_filter = PCALocalization(variance_threshold=variance_threshold)
    pca_result = pca_filter.localize(rho)
    
    # 经典协方差
    states_array = np.array(ensemble_states)
    mean_state = np.mean(states_array, axis=0)
    centered = states_array - mean_state
    classical_cov = np.cov(centered, rowvar=False)
    
    # 经典局部化
    classical_loc_cov = classical_localization(classical_cov, loc_radius=window_size // 2)
    
    # 提取窗口部分
    half_window = window_size // 2
    center = n_vars // 2
    start = max(0, center - half_window)
    end = min(n_vars, center + half_window + 1)
    
    classical_loc_local = classical_loc_cov[start:end, start:end]
    pca_reduced_local = pca_result.rho_reduced[:end-start, :end-start]
    
    # 计算误差
    classical_error = np.linalg.norm(classical_cov[start:end, start:end] - classical_loc_local, 'fro')
    pca_error = pca_result.reconstruction_error
    
    return {
        'classical_localization_error': classical_error,
        'pca_localization_error': pca_error,
        'pca_n_components': pca_result.n_components,
        'pca_reconstruction_error': pca_result.reconstruction_error,
        'pca_explained_variance': np.sum(pca_result.explained_variance_ratio),
        'window_size': window_size,
        'variance_threshold': variance_threshold
    }


def sensitivity_analysis(
    ensemble_states: List[np.ndarray],
    n_vars: int,
    window_sizes: List[int] = None,
    variance_thresholds: List[float] = None
) -> dict:
    """
    局部化敏感性分析
    
    参数:
        ensemble_states: 系综状态列表
        n_vars: 总变量数
        window_sizes: 窗口大小列表
        variance_thresholds: 方差阈值列表
    
    返回:
        敏感性分析结果
    """
    if window_sizes is None:
        window_sizes = [5, 10, 15, 20]
    if variance_thresholds is None:
        variance_thresholds = [0.80, 0.90, 0.95, 0.99]
    
    results = {
        'window_size_analysis': [],
        'variance_threshold_analysis': [],
        'optimal_config': None
    }
    
    # 分析不同窗口大小
    for ws in window_sizes:
        result = compare_localization_methods(
            ensemble_states, n_vars, window_size=ws, variance_threshold=0.95
        )
        results['window_size_analysis'].append({
            'window_size': ws,
            'classical_error': result['classical_localization_error'],
            'pca_error': result['pca_localization_error'],
            'pca_n_components': result['pca_n_components']
        })
    
    # 分析不同方差阈值
    for vt in variance_thresholds:
        result = compare_localization_methods(
            ensemble_states, n_vars, window_size=10, variance_threshold=vt
        )
        results['variance_threshold_analysis'].append({
            'variance_threshold': vt,
            'pca_error': result['pca_localization_error'],
            'pca_n_components': result['pca_n_components'],
            'pca_explained_variance': result['pca_explained_variance']
        })
    
    # 找到最优配置（最小PCA误差）
    min_error = float('inf')
    for vt_analysis in results['variance_threshold_analysis']:
        if vt_analysis['pca_error'] < min_error:
            min_error = vt_analysis['pca_error']
            results['optimal_config'] = {
                'variance_threshold': vt_analysis['variance_threshold'],
                'pca_error': vt_analysis['pca_error'],
                'n_components': vt_analysis['pca_n_components']
            }
    
    return results


def main():
    """演示PCA局部化"""
    print("=" * 60)
    print("基于PCA的局部化模块演示")
    print("=" * 60)
    
    # 示例1：简单系综
    print("\n【示例1】简单系综的PCA局部化")
    print("-" * 40)
    
    n_vars = 20
    n_ensemble = 10
    
    np.random.seed(42)
    ensemble = []
    for _ in range(n_ensemble):
        state = np.random.randn(n_vars) * 0.1
        state += np.sin(np.linspace(0, 2*np.pi, n_vars))
        ensemble.append(state)
    
    # 构建密度矩阵
    rho = create_density_matrix_from_ensemble(ensemble)
    
    # PCA局部化
    pca_filter = PCALocalization(variance_threshold=0.95)
    result = pca_filter.localize(rho)
    
    print(f"密度矩阵维度: {rho.shape}")
    print(f"保留主成分数: {result.n_components}")
    print(f"重构误差: {result.reconstruction_error:.6f}")
    print(f"解释方差比例: {np.sum(result.explained_variance_ratio):.4f}")
    print(f"前5个特征值: {result.eigenvalues[:5]}")
    
    # 示例2：局部化敏感性分析
    print("\n【示例2】局部化敏感性分析")
    print("-" * 40)
    
    n_vars = 40
    n_ensemble = 20
    
    ensemble = []
    for _ in range(n_ensemble):
        state = np.random.randn(n_vars) * 0.1
        state += np.sin(np.linspace(0, 4*np.pi, n_vars))
        ensemble.append(state)
    
    # 窗口大小敏感性
    print("\n窗口大小敏感性:")
    print(f"{'窗口大小':<10} {'经典误差':<15} {'PCA误差':<15} {'PCA维度':<10}")
    print("-" * 55)
    
    for ws in [5, 10, 15, 20]:
        result = compare_localization_methods(ensemble, n_vars, window_size=ws)
        print(f"{ws:<10} {result['classical_localization_error']:<15.6f} "
              f"{result['pca_localization_error']:<15.6f} {result['pca_n_components']:<10}")
    
    # 方差阈值敏感性
    print("\n方差阈值敏感性:")
    print(f"{'阈值':<10} {'PCA误差':<15} {'PCA维度':<10} {'解释方差':<10}")
    print("-" * 50)
    
    for vt in [0.80, 0.90, 0.95, 0.99]:
        result = compare_localization_methods(ensemble, n_vars, window_size=10, variance_threshold=vt)
        print(f"{vt:<10} {result['pca_localization_error']:<15.6f} "
              f"{result['pca_n_components']:<10} {result['pca_explained_variance']:<10.4f}")
    
    # 示例3：误差曲线分析
    print("\n【示例3】重构误差随主成分数变化")
    print("-" * 40)
    
    pca_filter = PCALocalization()
    error_analysis = pca_filter.analyze_localization_error(rho)
    
    print(f"{'主成分数':<10} {'重构误差':<15} {'解释方差':<15}")
    print("-" * 45)
    for i, (n, err, var) in enumerate(zip(
        error_analysis['n_components'],
        error_analysis['reconstruction_errors'],
        error_analysis['explained_variances']
    )):
        if i < 10 or n == error_analysis['n_components'][-1]:  # 只显示前10个和最后一个
            print(f"{n:<10} {err:<15.6f} {var:<15.4f}")
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
