# 项目进度

## 2026量子计算应用大赛·数据同化赛道

---

## 已完成任务

### 1. 文献调研（lunwenfenxi 文件夹）

#### 第一批论文（lunwenfenxi/）
- 下载并分析了5篇arXiv论文
- 写了分析报告：`lunwenfenxi/lunwenfenxi.md`
- 写了创新点分析：`lunwenfenxi/kejisheng.md`
- 写了本质分析：`lunwenfenxi/本质分析_最终版.md`

#### 第二批论文（lunwenfenxi/2/）— 2023年后顶会顶刊
- 下载9篇优秀论文（NPG 2024, NPG 2025, npj Quantum Info 2025, Acta Numerica 2025, Nature Comp Sci 2025, arXiv 2024-2025）
- 深度分析报告：
  - `lunwenfenxi/2/本质深度分析.md` — 初步深度分析
  - `lunwenfenxi/2/本质深度分析_终极版.md` — 终极深度分析（非交换概率论视角）
  - `lunwenfenxi/2/本质深度分析_终极版_引用.md` — 带完整引用的本质分析
  - `lunwenfenxi/2/思想深度分析_续.md` — **新增：作者思考角度深度分析**
- **核心发现**：所有差异源于**交换代数 vs 非交换代数**

### 2. 技术路线确定
- 主攻方向：**量子增强局部化**（Quantum-Enhanced Localization）
- 核心数学本质：
  - 经典: P_{ij} = E[(x_i-μ_i)(x_j-μ_j)] （对称，二阶，可交换）
  - 量子: C_{ij} = Tr(ρ A_i A_j) - Tr(ρ A_i)Tr(ρ A_j) （可非对称，任意阶，不可交换）
- 关键创新：如果ρ是纠缠态，则C_{ij}捕捉非经典相关

### 3. 决策文档
- `sousuo.md`：评分权重分析、技术路线对比、主攻方向确定

### 4. 论文思想深度分析（2026-05-16 新增）
- 分析了6篇核心论文的作者思考角度
- 提取了每篇论文的本质公式和深层解读
- 评估了思想适配性矩阵
- **核心洞察**：
  - Acta Numerica 2025：EnKF是在高斯流形上的投影，精度上限由高斯假设决定
  - npj Quantum Info 2025：非马尔可夫性的代数刻画是 γ_n(t) < 0
  - arXiv 2024：量子核是算子空间的内积，核-Fisher信息关系是理论基础
  - arXiv 2025：降阶不是截断，是非交换条件期望的子代数投影

### 5. 论文思想深度分析（续2）（2026-05-16 新增）
- 跨论文思想融合：统一在**概率论的代数结构**框架下
- 更深层的数学本质：**非交换概率论**视角
- 量子局部化的非交换几何本质
- 量子协方差估计的深层结构
- 非马尔可夫性的DA应用
- 量子数据同化的完整数学框架（提案）
- **核心洞察**：
  - 经典DA建立在**交换代数** $C(\Omega)$ 上
  - 量子DA应该建立在**非交换代数** $B(\mathcal{H})$ 上
  - 量子优势的根本来源是**不可交换性**

### 6. 论文思想深度分析（续3）（2026-05-16 新增）
- 算子代数理论的深层结构（C*-代数、冯·诺依曼代数、Tomita-Takesaki理论）
- 非交换几何的深层结构（谱三元组、非交换中心极限定理）
- 量子信息理论的深层结构（量子熵、量子Fisher信息、量子Cramér-Rao界）
- 量子纠缠的深层结构（算子代数定义、纠缠度量）
- 量子核方法的深层结构（量子RKHS、核-Fisher信息关系）
- 量子数据同化的完整数学框架（代数层、态层、可观测量层、几何层、动力学层）
- **终极洞察**：
  - 量子DA的精度上限由**量子Fisher信息**决定
  - 量子优势来自**不可交换性**和**纠缠**
  - 量子局部化的本质是**非交换条件期望**（Tomiyama定理保证结构保持）

### 7. 量子贝叶斯滤波终极深度分析（2026-05-16 新增）
- 深度分析了6篇核心量子贝叶斯滤波论文：
  - PRX Quantum 2025: 量子卡尔曼滤波
  - arXiv 2510.16754: 量子态轨迹估计
  - arXiv 2511.07949: 量子系统降阶滤波
  - arXiv 2506.15951: 量子态平滑
  - arXiv 2512.05265: 量子贝叶斯滤波（连续监测）
  - New J. Physics 2025: 贝叶斯量子态估计
- 提取核心公式：**随机主方程（SME）**
  $$d\rho_t = \mathcal{L}(\rho_t)dt + \mathcal{H}[c]\rho_t dW_t$$
- 完成七层本质对比：
  1. 状态表示：经典集合 vs 量子密度矩阵
  2. 预测步：数值积分 vs Lindblad主方程
  3. 更新步：卡尔曼更新 vs 量子贝叶斯更新
  4. 局部化：经验函数 vs 降阶投影
  5. 协方差估计：二阶矩 vs 非交换协方差
  6. 测量反作用：外在假设 vs 内在特性
  7. 4D-Var：窗口优化 vs 量子平滑
- **核心洞察**：
  - 卡尔曼增益 $K$ ←→ 量子测量算子 $M(y)$
  - 局部化 = 降阶滤波（投影到低维子空间）
  - 4D-Var = 量子平滑（使用未来信息）
  - 测量反作用是量子同化的**内在特性**
- 分析报告：`lunwenfenxi/3/量子贝叶斯滤波终极深度分析.md`

---

## 待完成任务

### 1. 量子贝叶斯EnKF实现（新方向）
- [ ] 设计量子态编码线路（密度矩阵表示）
- [ ] 实现量子动力学演化 E(ρ)
- [ ] 实现量子测量更新 M(y)ρM(y)†
- [ ] 量子协方差提取 C_ij = Tr(ρ A_i A_j) - Tr(ρ A_i)Tr(ρ A_j)
- [ ] 在Lorenz96上验证

### 2. 与经典LETKF对比
- [ ] 实现经典LETKF基线
- [ ] 对比精度（RMSE）
- [ ] 对比计算复杂度

### 3. 算法说明文档
- [ ] 写量子贝叶斯EnKF的算法说明
- [ ] 为50分创新分做准备

---

## 关键发现

### 量子协方差的本质
```
经典协方差: P_{ij} = E[(x_i - μ_i)(x_j - μ_j)]
- 对称: P_{ij} = P_{ji}
- 半正定
- 只捕捉二阶相关
- 可交换: E[XY] = E[YX]

量子协方差: C_{ij} = Tr(ρ A_i A_j) - Tr(ρ A_i) Tr(ρ A_j)
- 可非对称: C_{ij} ≠ C_{ji} 当 [A_i, A_j] ≠ 0
- 可捕捉高阶相关（通过A_i的高阶多项式）
- 不可交换: Tr(ρ A_i A_j) ≠ Tr(ρ A_j A_i)
- 当ρ是纠缠态时，可捕捉非经典相关
```

### 量子局部化的本质
```
经典局部化: D ∘ P (Hadamard积)
- 截断远距离虚假相关

量子局部化: E[C] (非交换条件期望)
- 截断非经典纠缠
- 数学本质: E: B(H) → B(H_red) 是子代数投影
```

### 非马尔可夫性的本质
```
Lindblad主方程: dρ/dt = L(ρ)
- γ_n ≥ 0 (完全正定)

非马尔可夫: dρ/dt = L_t(ρ)
- γ_n(t) 可为负 ← 信息回流
- 对应经典DA中的反向传播效应
```

### 量子贝叶斯滤波（2026-05-16 新增）

**核心公式**：
```
经典贝叶斯: p(x_k|y_{1:k}) ∝ p(y_k|x_k) ∫ p(x_k|x_{k-1}) p(x_{k-1}|y_{1:k-1}) dx_{k-1}

量子贝叶斯: ρ_k ∝ M_k E(ρ_{k-1}) M_k†
```

**关键洞察**：
- 量子测量会**扰动**系统（backaction），而经典测量不会
- 测量反作用是量子同化的**内在特性**，不是额外引入的
- 纠缠是**不可分离性**，不是人为假设

**直接相关论文**：
- PRX Quantum 2025: 量子系统中的EKF（原子磁力计）
- arXiv 2512.05265: 量子贝叶斯滤波（连续监测）

---

## 文件清单

```
lunwenfenxi/
├── lunwenfenxi.md          # 论文分析报告
├── kejisheng.md            # 创新点深度分析
├── 本质分析_最终版.md      # 经典vs量子协方差本质
├── npg_quantum_da.pdf      # NPG 2024 量子退火DA
├── qml_bibliometric.pdf    # arXiv 文献计量
├── quantum_reservoir_2405.pdf # 量子储层
├── da_operator_algebras_2206.pdf # DA算子代数
└── tensor_var_2501.pdf     # Tensor-Var

lunwenfenxi/2/
├── npg_quantum_da_2024.pdf          # NPG 2024
├── npg_coupled_da_2025.pdf          # NPG 2025
├── npj_lindblad_tomography_2025.pdf # npj Quantum Info 2025
├── arxiv_mllenkb_2025.pdf           # arXiv 多层局部EnKBF
├── arxiv_quantum_reduction_2025.pdf # arXiv 量子降阶
├── arxiv_nmr_quantum_kernels_2024.pdf # arXiv 量子核
├── acta_numerica_enkf_2025.pdf      # Acta Numerica 2025 ⭐
├── nature_comp_science_qml_2025.pdf # Nature Comp Sci 2025 ⭐
├── paper_analysis.md                # 论文分析报告
├── 本质深度分析.md                   # 深度分析
└── 本质深度分析_终极版.md            # 终极深度分析（非交换概率论视角）

lunwenfenxi/3/
├── paper_relevance_assessment.md    # 论文相关性诚实评估
├── direct_papers_analysis.md        # 直接相关论文深度分析
├── quantum_filtering_deep_analysis.md # 量子贝叶斯滤波深度分析 ⭐⭐⭐⭐⭐
├── papers/
│   ├── prx_quantum_kalman_filter_2025.pdf      # PRX Quantum 2025 ⭐⭐⭐⭐
│   ├── arxiv_physical_localization_2025.pdf    # arXiv 2511.08845 ⭐⭐⭐
│   ├── arxiv_bayesian_quantum_state_2025.pdf   # New J. Physics 2025 ⭐⭐⭐
│   ├── arxiv_quantum_bayesian_filter_2025.pdf  # arXiv 2512.05265 ⭐⭐⭐⭐⭐
│   ├── arxiv_quantum_state_trajectories_2510.pdf # arXiv 2510.16754 ⭐⭐⭐⭐⭐
│   ├── arxiv_quantum_reduced_filters_2511.pdf  # arXiv 2511.07949 ⭐⭐⭐⭐
│   ├── arxiv_quantum_smoothing_2506.pdf        # arXiv 2506.15951 ⭐⭐⭐⭐⭐
│   ├── arxiv_quantum_calibration_2507.pdf      # arXiv 2507.06941 ⭐⭐⭐
│   └── arxiv_quantum_amplitude_estimation_2412.pdf # arXiv 2412.04394 ⭐⭐⭐
```

---

## 2026-05-16 新增实验记录

### 实验1：固定局部化敏感性实验

- 已执行 `LETKF` 固定局部化敏感性实验
- 远程实验目录：
  - `/home/infra/qda_competition/experiments/loc_sensitivity/`

- 固定参数：
  - `ens_size = 40`
  - `infl = 1.02`
  - `obs_std = 0.5`
  - `dt = 0.05`
  - `forcing = 8.0`
  - `seed = 2`

- 扫描范围：
  - `loc_radius = 4, 6, 8, 10, 15, 20, 25, 30`

- 关键结果：
  - `loc_radius = 4`
    - `train RMSE = 0.1478915312`
    - `test_1 RMSE = 0.1586104835`
  - `loc_radius = 15`
    - `train RMSE = 0.1239766742`
    - `test_1 RMSE = 0.1286062214`
  - `loc_radius = 20`
    - `train RMSE = 0.1211974487`
    - `test_1 RMSE = 0.1287279125`
  - `loc_radius = 25 / 30`
    - 与 `20` 基本一致，进入平台区

- 当前判断：
  - 固定局部化半径对误差影响显著；
  - 小半径局部化明显过强；
  - `train` 与 `test_1` 的最优半径不一致；
  - 支持“固定经验局部化值得被更自适应的权重结构替代”这一主线判断。

- 本地实验文档：
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\实验1_固定局部化敏感性实验.md`

### 实验2：经典代理核实验

- 已执行 `LETKF` 经典代理核实验，用最小替换方式测试“数据驱动权重”是否优于固定局部化
- 远程实验目录：
  - `/home/infra/qda_competition/experiments/classical_proxy/`

- 固定参数：
  - `ens_size = 40`
  - `infl = 1.02`
  - `obs_std = 0.5`
  - `dt = 0.05`
  - `forcing = 8.0`
  - `seed = 2`
  - `support_radius = 20`

- 测试代理核：
  - `fixed`：窗口内等权
  - `corr`：扰动相关性核
  - `innov`：innovation 衰减核
  - `hybrid`：相关性 + innovation + 软距离混合核

- 结果摘要：
  - `fixed`
    - `train RMSE = 0.1211974487`
    - `test_1 RMSE = 0.1287279125`
  - `corr`
    - `train RMSE = 0.1433489617`
    - `test_1 RMSE = 0.1436237481`
  - `innov`
    - `train RMSE = 0.1603852765`
    - `test_1 RMSE = 0.1820804562`
  - `hybrid`
    - `train RMSE = 0.1574433598`
    - `test_1 RMSE = 0.1879526914`

- 当前判断：
  - 这轮最朴素的数据驱动代理核未能优于固定局部化；
  - `corr` 相对最接近，但仍明显落后；
  - `innov` 与 `hybrid` 退化更明显；
  - 说明后续若继续推进量子核路线，不能只是把“相关性/innovation 权重”直接量子化，而必须从特征表示和相似度结构本身重新设计。

- 本地实验文档：
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\实验2_经典代理核实验.md`

- 本次续做补齐了实验 2 的结构性输出：
  - 新增脚本：
    - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp2_structure_analysis.py`
  - 新增结构分析目录：
    - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp2_structure_outputs`
  - 关键新增产物：
    - `实验2_权重热图_fixed_t500.png`
    - `实验2_权重热图_corr_t500.png`
    - `实验2_权重热图_innov_t500.png`
    - `实验2_权重热图_hybrid_t500.png`
    - `实验2_典型权重曲线.png`
    - `实验2_权重结构分析_summary.md`

- 结构性补充结论：
  - `fixed` 在 `t = 500` 仍为常数权重，结构最稳；
  - `corr` 已经出现明显结构，说明它不是没信息，而是单步相关性还不足以稳定替代等权；
  - `innov` 会更直接地压低大残差观测，容易误伤有价值的修正信息；
  - `hybrid` 波动最强，说明多个经验因子相乘会把偏好叠加成更尖锐的降权结构。

- 当前阶段判断更新：
  - `实验 2` 现在已经从“只有误差表”补成了“误差结果 + 权重结构证据”；
  - 因此后续若继续做 `实验 3`，应把重点放在量子特征映射和相似度几何本身，而不是直接量子化现有 `corr / innov / hybrid` 权重公式。

### 实验3：量子核结构实验

- 已执行 `实验 3`，先不接入 `LETKF` 主循环，只检验小规模量子特征映射构造出的核矩阵是否有结构
- 远程实验目录：
  - `/home/infra/qda_competition/experiments/quantum_kernel_structure/`

- 实验设置：
  - `n_qubits = 4`
  - `window_size = 4`
  - `sample_times = [0, 500, 998]`
  - `sample_centers = [0, 10, 20, 30]`
  - `sample_count = 12`
  - 对照组：经典 `RBF` 核

- 量子核统计结果：
  - `min = 0.0000758`
  - `max = 1.0000000`
  - `mean = 0.2843038`
  - `std = 0.3120827`
  - `min_eig = 0.0235493`
  - `neg_eig_count = 0`

- 经典 `RBF` 核统计结果：
  - `min = 0.0078729`
  - `max = 1.0000000`
  - `mean = 0.2997723`
  - `std = 0.3216289`
  - `min_eig = 0.0082141`
  - `neg_eig_count = 0`

- 当前判断：
  - 量子核不是常数矩阵，说明它是非平凡的；
  - 没有负特征值，说明这一轮量子核矩阵近似半正定且数值稳定；
  - 不同时间块均值明显不同，说明量子核对局部流型变化有反应；
  - 与经典 `RBF` 核总体接近但块结构不同，说明量子核已形成不同的相似度几何；
  - 因此 `实验 3` 支持假设 3，可以进入最小接入版 `实验 4`。

- 远程已生成产物：
  - `summary.json`
  - `summary.md`
  - `quantum_kernel.csv`
  - `rbf_kernel.csv`
  - `quantum_time_block.csv`
  - `rbf_time_block.csv`

- 本地文档与脚本：
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\实验3_量子核结构实验.md`
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp3_quantum_kernel_structure.py`
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp3_render_plots.py`
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp3_render_plots.py`

### 实验4：量子核接入 LETKF 最小验证

- 已按最小接入方式执行 `实验 4`
- 远程实验目录：
  - `/home/infra/qda_competition/experiments/quantum_weighted_letkf/`

- 接入方式：
  - 保留 `LETKF` 主骨架、`RK4` 预报、集合子空间更新与 `sym_sqrt`
  - 只替换观测加权项
  - 对照组：
    - `fixed`
    - `corr`
    - `quantum`

- 固定参数：
  - `ens_size = 40`
  - `infl = 1.02`
  - `obs_std = 0.5`
  - `dt = 0.05`
  - `forcing = 8.0`
  - `seed = 2`
  - `support_radius = 20`
  - `window_size = 4`
  - `n_qubits = 4`

- 结果摘要：
  - `fixed`
    - `train RMSE = 0.1211974487`
    - `test_1 RMSE = 0.1287279125`
  - `corr`
    - `train RMSE = 0.1414554889`
    - `test_1 RMSE = 0.1427945539`
  - `quantum`
    - `train RMSE = 2.6827042544`
    - `test_1 RMSE = 2.4399778777`

- 当前判断：
  - 实验 3 的“量子核结构成立”没有自动转化为“最终方法有效”
  - 当前这版“量子核直接做观测对角加权”的最小接入方案显著退化，应判定为无效
  - 问题重点不再是“量子核有没有结构”，而是“量子核能否以合适方式进入同化更新”
  - 若继续推进，更合理的方向应是：
    - 量子核与固定权重/距离核混合
    - 量子核做结构调制而不是完全替代
    - 量子核先用于表示层，再间接影响同化

- 本地实验文档：
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\实验4_量子核接入LETKF最小验证.md`
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp4_quantum_weighted_letkf.py`

### 实验5：量子核混合权重验证

- 已按“温和混合而非完全替代”的思路执行 `实验 5`
- 远程实验目录：
  - `/home/infra/qda_competition/experiments/quantum_mixed_weight_letkf/`

- 接入方式：
  - 保留 `LETKF` 主骨架、`RK4` 预报、集合子空间更新与 `sym_sqrt`
  - 不再让量子核直接替代观测对角权重
  - 改为两类混合方案：
    - `linear_quantum_mix`
    - `distance_quantum_mix`
  - 同时保留对照组：
    - `fixed`
    - `corr`

- 固定参数：
  - `ens_size = 40`
  - `infl = 1.02`
  - `obs_std = 0.5`
  - `dt = 0.05`
  - `forcing = 8.0`
  - `seed = 2`
  - `support_radius = 20`
  - `window_size = 4`
  - `n_qubits = 4`

- 混合强度扫描：
  - `lambda = 0.1, 0.2, 0.3, 0.5`

- 结果摘要：
  - `fixed`
    - `train RMSE = 0.1211974487`
    - `test_1 RMSE = 0.1287279125`
  - `corr`
    - `train RMSE = 0.1414554889`
    - `test_1 RMSE = 0.1427945539`
  - `linear_quantum_mix, lambda = 0.1`
    - `train RMSE = 0.1200722774`
    - `test_1 RMSE = 0.1287301380`
  - `distance_quantum_mix, lambda = 0.1`
    - `train RMSE = 0.1215842098`
    - `test_1 RMSE = 0.1312267077`
  - 更大 `lambda` 下两类混合方案都继续退化

- 实现过程中的关键修复：
  - 实验第一次运行时在部分混合组合中途退出
  - 已在局部分析矩阵求逆处加入 `stable_inverse`
  - 通过 `jitter + pinv` 兜底后，实验 5 已完整跑通

- 当前判断：
  - 量子核“温和混合”明显比“直接量子对角加权”更稳定
  - 但当前没有任何混合方案真正超过 `fixed`
  - 最接近基线的是 `linear_quantum_mix, lambda = 0.1`
  - 当前最强可交付方案仍然是经典 `fixed`
  - 量子核目前更适合作为结构调制或探索分支，而不是直接替代最终赛题主方案

- 赛题链路兼容输出：
  - 远程已生成 `best_test_prediction.csv`
  - 远程已生成 `result.csv`
  - 但当前最优结果仍对应 `fixed`

- 本地实验文档：
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\实验5_量子核混合权重验证.md`
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp5_quantum_mixed_weight_letkf.py`

### 2026-05-16：双线并行量子 LETKF 落地实施设计定稿

- 已完成对 `lunwenfenxi/2` 另一套方法的工程可落地评估。
- 当前判断：
  - 不适合整体替换当前主线；
  - 最值得吸收的是：
    - 量子核用于局部结构表达
    - 降阶 / 分组 / 子块组织
    - 稀疏量子结构信号交给经典稳健更新完成最终分析
- 已确定采用“双线并行”推进，而不是继续在单一脚本中叠加所有想法：
  - `exp8_quantum_block_mix_letkf.py`
    - 短期稳妥线
    - 基于 `exp5`
    - 目标是让量子核只做 `block` 级结构调制，不直接决定单观测点权重
  - `exp9_quantum_reduced_group_letkf.py`
    - 中期创新线
    - 基于 `exp7`
    - 目标是让量子核先做表示层分组 / 降阶，再由经典规则做稳健更新
  - `compare_quantum_variants.py`
    - 统一比较 `fixed`、`corr`、`exp5` 最优、`exp8` 最优、`exp9` 最优
- 已新增文档：
  - `d:\Desktop\laingzimuxi\docs\plans\2026-05-16-双线并行量子letkf落地实施-design.md`
  - `d:\Desktop\laingzimuxi\docs\plans\2026-05-16-双线并行量子letkf落地实施.md`
- 当前执行建议：
  - 先实现 `exp8`，验证 `block` 级弱调制是否比 `exp5` 更稳
  - 再实现 `exp9`，验证表示层分组是否比权重层量子接入更合理
  - 只有当 `exp8` 或 `exp9` 出现积极信号，才继续做“可信度特征 + 分组”的交叉版本
