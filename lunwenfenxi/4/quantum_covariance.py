#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
量子协方差估计模块

基于论文分析：量子协方差可以捕捉经典协方差无法描述的非经典相关（如纠缠）
核心公式：C_ij = Tr(ρ A_i A_j) - Tr(ρ A_i)Tr(ρ A_j)

对数据同化的启示：
- 可以用量子协方差替代经典协方差进行LETKF更新
- 可捕捉高阶相关和纠缠
- 非交换性：[A_i, A_j] ≠ 0 时，C_ij ≠ C_ji
"""

import numpy as np
from typing import List, Tuple, Optional, Union
from dataclasses import dataclass
import warnings


@dataclass
class QuantumState:
    """量子态（密度矩阵）"""
    rho: np.ndarray  # 密度矩阵，形状 (N, N)，N = 希尔伯特空间维度
    basis_names: List[str]  # 基向量名称
    
    def __post_init__(self):
        """验证密度矩阵的有效性"""
        # 验证维度
        if self.rho.ndim != 2 or self.rho.shape[0] != self.rho.shape[1]:
            raise ValueError("密度矩阵必须是方阵")
        
        # 验证迹为1
        trace = np.trace(self.rho)
        if not np.isclose(trace, 1.0, atol=1e-10):
            warnings.warn(f"密度矩阵迹不为1: {trace:.6f}")
        
        # 验证厄米性
        if not np.allclose(self.rho, self.rho.conj().T):
            warnings.warn("密度矩阵不是厄米矩阵")
        
        # 验证半正定性（特征值非负）
        eigvals = np.linalg.eigvalsh(self.rho)
        if np.any(eigvals < -1e-10):
            warnings.warn(f"密度矩阵有负特征值: min={np.min(eigvals):.6f}")


@dataclass
class Observable:
    """可观测量算子"""
    operator: np.ndarray  # 算子矩阵，形状 (N, N)
    name: str  # 算子名称
    
    def expectation(self, state: QuantumState) -> np.complex128:
        """计算期望值 ⟨A⟩ = Tr(ρ A)"""
        return np.trace(state.rho @ self.operator)


class QuantumCovarianceEstimator:
    """量子协方差估计器"""
    
    def __init__(self, observables: List[Observable]):
        """
        初始化量子协方差估计器
        
        参数:
            observables: 可观测量算子列表 [A_1, A_2, ..., A_n]
        """
        self.observables = observables
        self.n_obs = len(observables)
        
        # 验证所有算子维度一致
        dim = observables[0].operator.shape[0]
        for obs in observables:
            if obs.operator.shape != (dim, dim):
                raise ValueError("所有可观测量算子必须有相同的维度")
    
    def compute_covariance(self, state: QuantumState) -> np.ndarray:
        """
        计算量子协方差矩阵
        
        C_ij = Tr(ρ A_i A_j) - Tr(ρ A_i)Tr(ρ A_j)
        
        返回:
            协方差矩阵，形状 (n_obs, n_obs)
        """
        # 计算每个算子的期望值
        expectations = np.array([obs.expectation(state) for obs in self.observables])
        
        # 初始化协方差矩阵
        cov_matrix = np.zeros((self.n_obs, self.n_obs), dtype=complex)
        
        # 计算协方差
        for i in range(self.n_obs):
            for j in range(self.n_obs):
                # Tr(ρ A_i A_j)
                product_expectation = np.trace(state.rho @ self.observables[i].operator @ self.observables[j].operator)
                # C_ij = Tr(ρ A_i A_j) - Tr(ρ A_i)Tr(ρ A_j)
                cov_matrix[i, j] = product_expectation - expectations[i] * expectations[j]
        
        return cov_matrix
    
    def compute_symmetric_part(self, state: QuantumState) -> np.ndarray:
        """
        计算对称部分（经典协方差的量子推广）
        
        C^sym_ij = (1/2) Tr(ρ {A_i, A_j}) - Tr(ρ A_i)Tr(ρ A_j)
        其中 {A, B} = AB + BA 是反对易子
        
        返回:
            对称协方差矩阵，形状 (n_obs, n_obs)
        """
        expectations = np.array([obs.expectation(state) for obs in self.observables])
        
        cov_sym = np.zeros((self.n_obs, self.n_obs), dtype=complex)
        
        for i in range(self.n_obs):
            for j in range(self.n_obs):
                # 反对易子 {A_i, A_j} = A_i A_j + A_j A_i
                anti_comm = (self.observables[i].operator @ self.observables[j].operator + 
                           self.observables[j].operator @ self.observables[i].operator)
                sym_expectation = np.trace(state.rho @ anti_comm) / 2
                cov_sym[i, j] = sym_expectation - expectations[i] * expectations[j]
        
        return cov_sym
    
    def compute_anticommutator_part(self, state: QuantumState) -> np.ndarray:
        """
        计算反对易部分（与经典协方差的区别）
        
        C^anti_ij = (1/2) Tr(ρ [A_i, A_j])
        其中 [A, B] = AB - BA 是对易子
        
        返回:
            反对易协方差矩阵，形状 (n_obs, n_obs)
        """
        anti_cov = np.zeros((self.n_obs, self.n_obs), dtype=complex)
        
        for i in range(self.n_obs):
            for j in range(self.n_obs):
                # 对易子 [A_i, A_j] = A_i A_j - A_j A_i
                commutator = (self.observables[i].operator @ self.observables[j].operator - 
                            self.observables[j].operator @ self.observables[i].operator)
                anti_cov[i, j] = np.trace(state.rho @ commutator) / (2j)  # 除以2i使结果为实数
        
        return anti_cov
    
    def analyze_nonclassical_correlation(self, state: QuantumState) -> dict:
        """
        分析非经典相关性
        
        返回:
            包含各种度量信息的字典
        """
        cov = self.compute_covariance(state)
        cov_sym = self.compute_symmetric_part(state)
        cov_anti = self.compute_anticommutator_part(state)
        
        # 计算非交换性度量
        non_symmetric_norm = np.linalg.norm(cov - cov.conj().T, 'fro')
        
        # 计算反对易部分范数（量子特有）
        anti_norm = np.linalg.norm(cov_anti, 'fro')
        
        # 计算与经典协方差的差异
        classical_like = np.linalg.norm(cov_sym - cov_sym.conj().T, 'fro')
        
        return {
            'covariance_matrix': cov,
            'symmetric_part': cov_sym,
            'anticommutator_part': cov_anti,
            'non_symmetric_norm': non_symmetric_norm,
            'anticommutator_norm': anti_norm,
            'classical_like_norm': classical_like,
            'is_classical': anti_norm < 1e-10,
            'observables_names': [obs.name for obs in self.observables]
        }


def create_ensemble_density_matrix(
    ensemble_states: List[np.ndarray],
    weights: Optional[List[float]] = None
) -> QuantumState:
    """
    从系综构建密度矩阵
    
    ρ = Σ_k w_k |ψ_k⟩⟨ψ_k|
    
    参数:
        ensemble_states: 纯态列表，每个形状 (N,)
        weights: 权重列表，默认等权重
    
    返回:
        QuantumState 对象
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
    
    return QuantumState(rho=rho, basis_names=[f"|k⟩" for k in range(N)])


def create_localized_observables(
    n_vars: int,
    window_size: int = 5,
    window_center: int = None
) -> Tuple[List[Observable], int, int]:
    """
    创建局部化的可观测量算子
    
    对应经典DA中的局部化窗口
    
    参数:
        n_vars: 总变量数
        window_size: 局部窗口大小
        window_center: 窗口中心位置，默认中间
    
    返回:
        (可观测量列表, 窗口起始索引, 窗口结束索引)
    """
    if window_center is None:
        window_center = n_vars // 2
    
    # 确定窗口范围
    half_window = window_size // 2
    start = max(0, window_center - half_window)
    end = min(n_vars, window_center + half_window + 1)
    
    observables = []
    
    # 创建位置算子（对应经典DA中的状态变量）
    for i in range(start, end):
        # 位置算子 |i⟩⟨i|
        op = np.zeros((n_vars, n_vars), dtype=complex)
        op[i, i] = 1.0
        observables.append(Observable(operator=op, name=f"X_{i}"))
    
    # 创建动量算子（量子特有，对应经典DA中没有的概念）
    for i in range(start, min(end - 1, n_vars - 1)):
        # 动量算子（有限差分）
        op = np.zeros((n_vars, n_vars), dtype=complex)
        op[i, i+1] = 1j
        op[i+1, i] = -1j
        observables.append(Observable(operator=op, name=f"P_{i}"))
    
    return observables, start, end


def compare_quantum_classical_covariance(
    ensemble_states: List[np.ndarray],
    n_vars: int,
    window_size: int = 5
) -> dict:
    """
    对比量子协方差与经典协方差
    
    参数:
        ensemble_states: 系综状态列表
        n_vars: 总变量数
        window_size: 局部窗口大小
    
    返回:
        对比结果字典
    """
    # 构建密度矩阵
    rho = create_ensemble_density_matrix(ensemble_states)
    
    # 创建局部化可观测量（仅位置算子，与经典协方差对应）
    observables, obs_start, obs_end = create_localized_observables(n_vars, window_size)
    
    # 量子协方差估计器
    estimator = QuantumCovarianceEstimator(observables)
    
    # 计算量子协方差
    quantum_cov = estimator.compute_covariance(rho)
    quantum_sym = estimator.compute_symmetric_part(rho)
    quantum_anti = estimator.compute_anticommutator_part(rho)
    
    # 经典协方差（直接从系综计算）
    states_array = np.array(ensemble_states)
    mean_state = np.mean(states_array, axis=0)
    centered = states_array - mean_state
    classical_cov = np.cov(centered, rowvar=False)
    
    # 量子可观测量数（位置+动量）
    n_quantum_obs = len(observables)
    n_position_obs = obs_end - obs_start  # 位置算子数量 = window_size
    
    # 提取位置算子对应的经典协方差部分
    classical_cov_local = classical_cov[obs_start:obs_end, obs_start:obs_end]
    
    # 量子协方差矩阵中位置算子部分（前n_position_obs个）
    quantum_sym_position = quantum_sym[:n_position_obs, :n_position_obs]
    
    # 计算差异度量
    diff_sym = np.linalg.norm(quantum_sym_position.real - classical_cov_local, 'fro')
    diff_anti = np.linalg.norm(quantum_anti, 'fro')
    
    return {
        'quantum_covariance': quantum_cov,
        'quantum_symmetric': quantum_sym,
        'quantum_anticommutator': quantum_anti,
        'classical_covariance': classical_cov_local,
        'difference_symmetric': diff_sym,
        'difference_anticommutator': diff_anti,
        'is_nonclassical': diff_anti > 1e-10,
        'n_observables': n_quantum_obs,
        'obs_start': obs_start,
        'obs_end': obs_end
    }


def main():
    """演示量子协方差估计"""
    print("=" * 60)
    print("量子协方差估计模块演示")
    print("=" * 60)
    
    # 示例1：简单的2-qubit系统
    print("\n【示例1】2-qubit系统")
    print("-" * 40)
    
    # 创建Bell态（纠缠态）
    bell_state = np.array([1, 0, 0, 1]) / np.sqrt(2)  # |00⟩ + |11⟩
    
    # 构建密度矩阵
    rho = create_ensemble_density_matrix([bell_state])
    
    # 创建Pauli算子作为可观测量
    pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
    pauli_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)
    
    # 对2-qubit系统，使用张量积
    observables = [
        Observable(np.kron(pauli_x, np.eye(2)), "X₁"),
        Observable(np.kron(np.eye(2), pauli_x), "X₂"),
        Observable(np.kron(pauli_z, np.eye(2)), "Z₁"),
        Observable(np.kron(np.eye(2), pauli_z), "Z₂"),
    ]
    
    estimator = QuantumCovarianceEstimator(observables)
    analysis = estimator.analyze_nonclassical_correlation(rho)
    
    print(f"可观测量: {analysis['observables_names']}")
    print(f"非对称范数: {analysis['non_symmetric_norm']:.6f}")
    print(f"反对易范数: {analysis['anticommutator_norm']:.6f}")
    print(f"是否经典: {analysis['is_classical']}")
    
    # 示例2：Lorenz96风格的系综
    print("\n【示例2】Lorenz96风格系综")
    print("-" * 40)
    
    n_vars = 40
    n_ensemble = 20
    
    # 生成随机系综（模拟LETKF的集合）
    np.random.seed(42)
    ensemble = []
    for _ in range(n_ensemble):
        state = np.random.randn(n_vars) * 0.1
        state += np.sin(np.linspace(0, 4*np.pi, n_vars))  # 添加周期性结构
        ensemble.append(state)
    
    # 对比量子与经典协方差
    result = compare_quantum_classical_covariance(ensemble, n_vars, window_size=10)
    
    print(f"变量数: {n_vars}")
    print(f"局部窗口大小: 10")
    print(f"可观测量数: {result['n_observables']}")
    print(f"对称部分差异: {result['difference_symmetric']:.6f}")
    print(f"反对易部分范数: {result['difference_anticommutator']:.6f}")
    print(f"是否非经典: {result['is_nonclassical']}")
    
    # 示例3：局部化敏感性分析
    print("\n【示例3】局部化敏感性分析")
    print("-" * 40)
    
    window_sizes = [5, 10, 15, 20]
    
    print(f"{'窗口大小':<10} {'对称差异':<15} {'反对易范数':<15} {'非经典':<10}")
    print("-" * 50)
    
    for ws in window_sizes:
        result = compare_quantum_classical_covariance(ensemble, n_vars, window_size=ws)
        print(f"{ws:<10} {result['difference_symmetric']:<15.6f} {result['difference_anticommutator']:<15.6f} {result['is_nonclassical']:<10}")
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
