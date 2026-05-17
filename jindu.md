# 项目进度

### 2026-05-17：exp37 最高分方案解释性可视化补全

- 已围绕当前最高分方案 `exp37 rho + J weak fusion` 补充一套更偏“方案解析”的图组，输出目录：
  - `d:\Desktop\laingzimuxi\tijiao\figures`
- 为保证解释图基于真实最优输出，已通过 `ssh -tt jump + base64` 从远端抓回以下分析素材到本地：
  - `tijiao/results/exp37_analysis/lorenz96_test_1.csv`
  - `tijiao/results/exp37_analysis/exp37_result.csv`
  - `tijiao/results/exp37_analysis/exp37_test_fixed.csv`
  - `tijiao/results/exp37_analysis/exp37_test_corr.csv`
  - `tijiao/results/exp37_analysis/exp37_summary.csv`
- 已新增图：
  - `exp37_error_distribution.png`
  - `exp37_error_improvement_heatmap.png`
  - `exp37_parameter_profiles.png`
  - `exp37_prediction_scatter.png`
  - `exp37_dimension_gain.png`
  - `exp37_time_rmse_trend.png`
  - `exp37_case_slices.png`
  - `exp37_timestep_distribution.png`
  - `exp37_method_schematic.png`
  - `exp37_observed_truth_fixed_best_slice.png`
  - `exp37_local_window_explanation.png`
  - `exp37_quantum_similarity_matrix.png`
  - `exp37_rho_vs_corr_weights.png`
- 图组用途：
  - 误差分布对比：说明 `exp37` 相对 `fixed` 的整体误差收缩
  - 误差改善热力图：说明不同时间步、不同维度上的改善位置
  - 参数剖面：说明 `lambda_rho` 与 `lambda_j` 的敏感性关系
  - 真值-预测散点：说明 `exp37` 相比 `fixed` 更贴近理想对角线
  - 分维度增益：说明收益并非只集中在少数维度
  - 时间趋势图：说明 `exp37` 的优势并非只来自个别时间点
  - 案例切片图：说明在具体状态截面上 `exp37` 对真值的拟合更贴近
  - 时间步分布图：说明逐时间步收益分布及波动范围
  - 方法结构图：说明 `rho` 主导、`J` 弱修正的接入逻辑
  - 四线切片图：把 `truth / observed / fixed / exp37` 放到同一时间片下直接对照，便于在文档中解释“最优结果如何同时贴近真值并纠正观测噪声”
  - 局部窗口解释图：说明 `exp37` 的量子窗口匹配不是抽象概念，而是可在一个具体局地窗口里看到“状态模式 vs 观测模式”的对应关系，同时展示 `J` 只做弱方向微调
  - 量子相似度矩阵图：说明局地状态窗口与多个观测窗口之间存在结构化相似度，而不是均匀权重
  - `rho` vs `corr` 权重图：直接展示当前主线为何不是简单相关性加权，而是“距离先验 + 量子相似度”的融合权重
- 已新增复现脚本：
  - `d:\Desktop\laingzimuxi\tijiao\tools\generate_exp37_interpretability_figures.py`
- 新脚本已补充本地 `qiskit` 缺失时的轻量回退实现：
  - 在不改 `exp37` 原实验文件的前提下，本地用同参数的 4-qubit 特征映射和 LETKF 公式重建代表性样本机制图，避免因为本地环境无 `qiskit` 而无法出图
- 本轮代表性解释样本：
  - 选取高收益时间步中的最早样本 `time_step=4`
  - 焦点维度为 `dimension=18`
  - 这样可以保留“收益明显”的解释性，同时避免为绘图重跑过长前序时间步
- 已继续补充“提交级附加说明图”：
  - `exp37_quantum_circuit_schematic.png`
  - `exp37_method_flowchart.png`
  - `exp37_residual_distribution.png`
  - `exp37_bias_variance_analysis.png`
  - `exp37_topk_dimension_gain.png`
  - `quantum_ablation_logic.png`
  - `quantum_qubit_compliance.png`
- 新增附加图复现脚本：
  - `d:\Desktop\laingzimuxi\tijiao\tools\generate_submission_extra_figures.py`
- 当前判断：
  - `exp37` 的优势不是来自强修正，而是来自“弱而稳定”的 `J` 几何修正；
  - 最优点仍然落在较小 `lambda_j`，支持“量子结构做弱控制”这一主线判断。
  - 当前提交材料层面，方法说明、量子电路、消融逻辑、误差解释和合规说明图已基本齐全。

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
```

### 2026-05-17：项目结构与主线梳理

- 已完成对仓库整体结构的重新梳理，当前仓库可视为三层并行体系：
  - `气象海洋/`：主实验与主代码区，承载 `LETKF + 量子增强` 的真实实验脚本
  - `tijiao/`：提交与汇报打包区，集中代码副本、图表、结果状态和文档材料
  - `lunwenfenxi/`：文献调研与方法库，用于支撑后续新方案设计而非直接替换主线
- 已确认赛题面向 `40` 维 `Lorenz96` 数据同化，硬约束是必须包含真实量子模块、单次量子线路不超过 `30` qubits、结果与文档可复现。
- 已确认对外交付主线仍是 `LETKF + 量子参数调优`：
  - 经典主骨架负责稳定同化
  - 量子模块负责小规模候选超参数选择
  - 当前公开对比文档显示该路线相对经典强基线有小幅提升，适合提交叙事与复现
- 已确认 `气象海洋/shiyan/` 是研究主线目录，实验链从 `exp2` 持续推进到 `exp42`：
  - `exp2-exp5`：量子核结构与最小接入验证
  - `exp6-exp21`：分组、结构化算子、公式层接入与迭代扩展
  - `exp32-exp42`：多源弱融合、自适应和门控版本
- 已确认当前最新实验主线集中在 `exp37-exp42`：
  - `exp37`：`rho + J` 弱融合
  - `exp39`：`rho + adaptive_B`
  - `exp41`：`rho + J` 置信门控
  - `exp42`：`rho + J + adaptive_B` 双门控
- 已确认 `exp41` 与 `exp42` 的共同模式是：
  - 用 `4` qubits 的局地窗口特征映射计算量子相似度
  - 将量子相似度以弱融合形式接入 `rho`
  - 再用门控/自适应机制决定 `J` 或 `B` 修正强度
  - 与 `fixed/corr` 基线一起输出 `summary.json`、`summary.csv`、`result.csv`
- 已确认 `tijiao/figures/` 和 `tijiao/results/status/` 已形成较完整提交材料：
  - `exp37` 解释图组较完整，适合作为当前最好方案的展示材料
  - `results/status/` 保留了远端日志、摘要和资源状态，适合作为运行佐证

### 2026-05-17：评委结构版 LaTeX 报告与扩图

- 已在 `tijiao/paper_cvpr_report.tex` 中重写正式报告，严格对齐评委要求的 9 节结构：
  - 摘要
  - 问题分析
  - 建模过程
  - 量子算法设计
  - 量子线路实现
  - 实验结果与展示
  - 创新点描述
  - 算法对比分析
  - 总结
- 已按规范调整版式：
  - `A4` 单栏
  - 四边页边距 `2.5cm`
  - 正文 `12pt`，满足“不小于小四号”
- 已将文档从“最小可编译版”扩展为“均衡版正文展示”，把前期分析图真正嵌入章节叙事，而不是只保留少量示意图。
- 当前正文已纳入的关键图包括：
  - `quantum_ablation_logic.png`
  - `exp37_method_flowchart.png`
  - `exp37_quantum_circuit_schematic.png`
  - `best_model_rmse_comparison.png`
  - `exp37_error_distribution.png`
  - `exp37_time_rmse_trend.png`
  - `exp37_error_improvement_heatmap.png`
  - `exp37_local_window_explanation.png`
  - `exp37_rho_vs_corr_weights.png`
- 当前写法已从“少图摘要版”切换为“正文主图 + 结果解释 + 机制说明”的正式报告风格：
  - 结果图负责证明方法有效
  - 机制图负责说明量子信息为何不是装饰
  - 对比图负责解释为什么当前主线不是普通 `corr` 加权，而是“距离先验 + 量子相似度”的弱融合
- 已在空闲 `PowerShell` 终端中使用 `xelatex` 两遍完成新版编译，生成：
  - `tijiao/paper_cvpr_report.pdf`
- 当前 `PDF` 已扩展为 `8` 页，可正常打开；剩余仅有中文字体粗体替代类警告，不影响交付阅读。

### 2026-05-17：LaTeX 报告拆分为主文件加章节文件

- 已将原先单文件 `tijiao/paper_cvpr_report.tex` 重构为“主控文件 + 章节子文件”结构，提升后续定位和分节修改效率。
- 当前主控文件仍为：
  - `tijiao/paper_cvpr_report.tex`
- 当前章节文件目录为：
  - `tijiao/paper_sections/00_abstract.tex`
  - `tijiao/paper_sections/01_problem_analysis.tex`
  - `tijiao/paper_sections/02_modeling.tex`
  - `tijiao/paper_sections/03_quantum_algorithm.tex`
  - `tijiao/paper_sections/04_circuit.tex`
  - `tijiao/paper_sections/05_results.tex`
  - `tijiao/paper_sections/06_innovations.tex`
  - `tijiao/paper_sections/07_comparison.tex`
  - `tijiao/paper_sections/08_summary.tex`
- 主文件当前只保留：
  - 文档类与版式设置
  - 宏包与字体配置
  - 标题信息
  - 按章节顺序的 `\\input`
- 当前拆分后的好处：
  - 修改摘要、实验结果、创新点时可直接进入对应章节文件
  - 插图和段落扩写可以按节推进，不必在长文件中来回查找
  - 更适合后续继续扩正文、压缩措辞或多人协作分节修改
- 已在 `PowerShell` 终端中对拆分后的版本重新执行两遍 `xelatex` 编译，生成新的：
  - `tijiao/paper_cvpr_report.pdf`
- 当前拆分后 `PDF` 已正常生成，并扩展为 `9` 页；交叉引用与图表路径均正常。

### 2026-05-17：实验结果章节改为逐图分析版

- 已重点扩写 `tijiao/paper_sections/05_results.tex`，不再只停留在“插图 + 一句结论”，而是把图作为正文论证证据来写。
- 本轮新增和强化的分析维度包括：
  - 总体 RMSE 对比后的结论承接
  - 误差分布为何说明不是偶然收益
  - 时间趋势为何说明优势具有持续性
  - 误差热力图为何说明改进是局地结构性的
  - 散点图为何说明重建结果更贴近真实值
  - 残差分布为何说明偏差中心与波动范围同步收缩
  - 代表性切片为何能直观看到峰谷和局地转折恢复更好
- 本轮在结果章节中新增使用的图包括：
  - `exp37_prediction_scatter.png`
  - `exp37_residual_distribution.png`
  - `exp37_case_slices.png`
- 当前结果章节已经从“指标汇总型写法”升级为“指标 + 分布 + 时间 + 空间 + 切片”的组合证据链，更适合论文报告和答辩展示。
- 已重新执行两遍 `xelatex` 编译，当前：
  - `tijiao/paper_cvpr_report.pdf`
  - 已扩展为 `10` 页
  - 编译通过，交叉引用正常

### 2026-05-17：建立报告修改问题清单文档

- 已根据最新人工审阅意见，新增独立问题清单文档：
  - `tijiao/report_revision_checklist.md`
- 当前文档用途：
  - 收敛报告存在的关键问题
  - 按“问题 -> 修改动作 -> 验收标准 -> 勾选状态”跟踪修订
  - 后续每完成一项，直接把对应复选框从 `[ ]` 改为 `[x]`
- 当前已纳入的问题类别包括：
  - 核心方法数学定义不足
  - 实验对比与系统性消融不充分
  - related work 缺失导致创新性表述悬空
  - 实验设置透明度不足
  - 图表分析缺少定量信息
  - 论文风格、模型层与比较章节需要继续收紧
- 当前推荐执行顺序也已写入清单：
  - 先补方法定义与最终公式
  - 再补实验设置与系统性消融
  - 再补 related work 与创新点重写
  - 再把图分析全部定量化
  - 最后统一收紧摘要、结论与标题

### 2026-05-17：按问题清单完成报告主干硬改

- 已围绕 `exp37` 当前受控实验脚本，完成报告主干的结构性修订，重点不再是“多加几段说明”，而是把可检验定义、实验透明度和定量证据真正补齐。
- 已完成的关键修改包括：
  - 将标题从偏方法论论文口径收紧为更符合证据规模的受控实验研究口径
  - 重写摘要，明确这是固定实验设定下的受控比较，弱化外推强度
  - 在 `02_modeling.tex` 中补入经典 LETKF 局地更新公式、局地逆观测协方差构造、量子弱融合权重、$J$ 修正项和最终分析公式
  - 在 `03_quantum_algorithm.tex` 中把 `J`、耦合系数和连续弱修正写成明确数学定义，并澄清当前 `exp37` 不含额外硬门控阈值
  - 在 `05_results.tex` 中新增实验设置说明、参数网格、系统性消融表，并把全部图分析改为带定量数字的写法
  - 在 `06_innovations.tex` 中补入 related-work 风格的相对定位，避免“自封式创新点”
  - 在 `07_comparison.tex` 中加入证据驱动的定量对比，说明本文与 `fixed`、`corr` 以及外层量子调参思路的差异
  - 在 `08_summary.tex` 中下调结论强度，明确当前证据仍局限于单一 Lorenz96 设定与有限参数网格
- 本轮还新增了一个本地统计文件：
  - `tijiao/results/exp37_analysis/exp37_quant_stats.json`
  - 用于支撑图表中的定量结论，如：
    - 相对 `fixed` 的 RMSE 改善比例
    - 时间步优于基线的比例
    - 改善维度数量
    - 误差尾部分位数下降
    - 代表性高收益时间片的单切片改善幅度
- 已重新使用 `xelatex` 两遍编译最新版本：
  - `tijiao/paper_cvpr_report.pdf`
  - 当前页数为 `21` 页
- 当前清单中大部分关键问题已打勾，剩余明确保留的一项是：
  - 全文进一步去重和压缩重复表述

### 2026-05-17：整篇报告升级为研究过程与可解释性厚版

- 已按“研究推进链条 + 可解释性证据链”两条主线，对整篇报告做系统性扩写，不再只是结果汇总型写法。
- 本轮重点加厚的章节包括：
  - `tijiao/paper_sections/01_problem_analysis.tex`
  - `tijiao/paper_sections/02_modeling.tex`
  - `tijiao/paper_sections/03_quantum_algorithm.tex`
  - `tijiao/paper_sections/04_circuit.tex`
  - `tijiao/paper_sections/05_results.tex`
  - `tijiao/paper_sections/06_innovations.tex`
  - `tijiao/paper_sections/07_comparison.tex`
- 本轮新增写法重点：
  - 在“问题分析”中补出完整研究形成过程：
    - 为什么不能走全量量子替代
    - 为什么要先做结构验证
    - 为什么直接强接入失败
    - 为什么最后收敛到弱融合与弱 `J` 修正
  - 在“建模过程”中补出局地窗口建模的理论动机，并加入量子相似度矩阵分析，说明量子结构不是随机噪声
  - 在“量子算法设计”中补出流程图和方法结构图的区别与联系，强调 `rho` 主调制、`J` 弱修正的双层控制逻辑
  - 在“量子线路实现”中补出线路层可解释性和量子比特合规分析，说明当前方案既能解释也能落地
  - 在“实验结果”中继续扩展为组合证据链，新增：
    - `exp37_dimension_gain.png`
    - `exp37_observed_truth_fixed_best_slice.png`
  - 在“创新点描述”中将创新从条目式表述升级为三条解释链：
    - 局地窗口解释链
    - 相似度解释链
    - 弱修正解释链
  - 在“算法对比分析”中加入更多支撑图，说明为什么本文不是普通 `corr` 加权、也不是外层量子调参：
    - `rmse_gain_over_fixed.png`
    - `train_test_rmse_grouped.png`
    - `exp37_j_strength_vs_rmse.png`
- 当前报告已形成“问题提出 -> 研究过程 -> 建模转化 -> 算法设计 -> 线路实现 -> 结果证据 -> 创新解释 -> 对比分析 -> 总结”的完整叙事链。
- 本轮编译结果：
  - `tijiao/paper_cvpr_report.pdf`
  - 已扩展为 `18` 页
  - `xelatex` 两遍编译通过
  - 交叉引用正常
  - 仅保留中文字体粗体替代警告，不影响阅读与交付
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

---

## 2026-05-17 新增推进记录

### exp41：rho + J + 置信门控 已实现并启动

- 本轮按“只新建文件、不修改现有实验源码”的方式推进
- 新增脚本：
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_letkf.py`
- 核心结构：
  - 保持 `rho` 作为主导局地化入口
  - 在 `J` 修正前加入 `j_confidence`
  - `j_confidence` 由 `coupling_strength`、`quantum_focus`、`innovation_strength` 共同决定
- 当前最小组合：
  - `(lambda_rho, lambda_j) = (0.02, 0.003), (0.02, 0.004), (0.03, 0.003)`
- 本地检查：
  - `py_compile` 通过
  - 诊断检查无报错
- 远端上传与启动方式：
  - `ssh -tt jump`
  - `base64` 上传到 `/tmp/exp41_rho_J_confidence_gated_letkf.py`
  - `nohup python3 ... > run.log 2>&1 < /dev/null &`
- 远端目录：
  - `/home/infra/qda_competition/experiments/rho_J_confidence_gated_letkf`
- 启动结果：
  - `STARTED:224617`
- 启动后短回查：
  - 进程仍在运行
  - `run.log` 已出现 `fixed` 的 `DONE {...}` 记录

### exp42：rho + J + adaptive_B + 双门控 已实现并启动

- 新增脚本：
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp42_rho_J_adaptive_B_gated_letkf.py`
- 核心结构：
  - 先做 `rho`
  - 再做 `J` 门控修正
  - 最后做 `adaptive_B` 门控补偿
- 新增门控量：
  - `j_confidence`
  - `b_confidence`
  - `alignment`
  - `spread_penalty`
- 本轮不再保留外层 `lambda_b` 扫描，`B` 只通过局部自适应 `lam_b_i` 控制
- 当前最小组合：
  - `(lambda_rho, lambda_j) = (0.02, 0.003), (0.02, 0.004), (0.03, 0.003)`
- 本地检查：
  - `py_compile` 通过
  - 诊断检查无报错
- 远端上传与启动方式：
  - `ssh -tt jump`
  - `base64` 上传到 `/tmp/exp42_rho_J_adaptive_B_gated_letkf.py`
  - `nohup python3 ... > run.log 2>&1 < /dev/null &`
- 远端目录：
  - `/home/infra/qda_competition/experiments/rho_J_adaptive_B_gated_letkf`
- 启动结果：
  - `STARTED:224681`
- 启动后短回查：
  - 进程仍在运行
  - `run.log` 已出现 `fixed` 的 `DONE {...}` 记录

### 本轮新增辅助脚本

- 为了稳定执行 `ssh -tt jump + base64 + nohup` 链路，新增本地上传器：
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\launch_remote_via_jump.py`
- 作用：
  - 统一把本地实验脚本经 `base64` 写入远端 `/tmp/*.py`
  - 远端先 `py_compile`
  - 再 `nohup` 启动
  - 本地落 `launch_status.txt` 与后续回查文件

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

### 实验8：量子 block 弱混合验证

- 已完成 `exp8_quantum_block_mix_letkf.py` 第一版实现，并在远端完成一轮运行：
  - 远程实验目录：
    - `/home/infra/qda_competition/experiments/quantum_block_mix_letkf/`
- 接入方式：
  - 复用 `exp5` 的 `LETKF` 主骨架
  - 不再使用单观测点量子权重
  - 改为先在局部 `block` 内聚合量子相似度，再回写到观测点层
  - 最终采用：
    - `distance_prior * weak block_quantum_signal`
- 固定参数：
  - `ens_size = 40`
  - `infl = 1.02`
  - `obs_std = 0.5`
  - `dt = 0.05`
  - `forcing = 8.0`
  - `seed = 2`
  - `support_radius = 20`
  - `window_size = 4`
  - `block_size = 4`
  - `n_qubits = 4`
- 扫描结果：
  - `fixed`
    - `train RMSE = 0.1211974487`
    - `test_1 RMSE = 0.1287279125`
  - `corr`
    - `train RMSE = 0.1414554889`
    - `test_1 RMSE = 0.1427945539`
  - `block_quantum_mix, lambda = 0.02`
    - `train RMSE = 0.1197131136`
    - `test_1 RMSE = 0.1292123375`
  - `block_quantum_mix, lambda = 0.05`
    - `train RMSE = 0.1196765303`
    - `test_1 RMSE = 0.1293390255`
  - `block_quantum_mix, lambda = 0.08`
    - `train RMSE = 0.1195522025`
    - `test_1 RMSE = 0.1296532903`
  - `block_quantum_mix, lambda = 0.10`
    - `train RMSE = 0.1194108322`
    - `test_1 RMSE = 0.1299600672`
- 当前判断：
  - `block` 级弱混合比此前更激进的量子权重接入稳定得多；
  - 但当前仍未超过经典 `fixed`；
  - 与 `exp5` 类似，量子调制对 `train` 有轻微改善，但未转化为 `test_1` 提升；
  - 且 `lambda` 增大时，`test_1` 持续变差，说明量子 block 信号仍应保持非常弱的参与度；
  - 当前最优测试结果仍然是经典 `fixed`。
- 下一步建议：
  - 继续推进 `exp9`，验证“表示层分组/降阶”是否比 `block` 弱调制更合理；
  - 暂不扩大 `exp8` 的 `lambda` 范围；
  - 如后续继续优化 `exp8`，优先考虑改 `block` 特征定义，而不是加大量子混合强度。

### 2026-05-16：公式层扩展实验第二批远端启动

- 在确认远端 `CPU + GPU + 内存` 基本空闲后，已继续按“本地写脚本、静默上传、最后统一下载结果”的方式补发未完成和新开的实验。
- 本地语法与诊断检查已通过：
  - `exp11_quantum_S_operator_letkf.py`
  - `exp13_quantum_localization_letkf.py`
  - `exp14_quantum_inflation_letkf.py`
  - `exp15_quantum_robust_innovation_letkf.py`
- 已确认远端启动并拿到 PID：
  - `exp11_quantum_S_operator_letkf.py`
    - `STARTED:215336`
  - `exp13_quantum_localization_letkf.py`
    - `STARTED:215402`
  - `exp14_quantum_inflation_letkf.py`
    - `STARTED:215604`
  - `exp15_quantum_robust_innovation_letkf.py`
    - `STARTED:215671`
- 约束保持不变：
  - 不复用当前其他实验的远端输出目录；
  - 不在终端直接回显结果；
  - 统一等远端产出 `summary.json / summary.csv / result.csv` 后再下载到本地验收。

### 2026-05-16：未完成公式层四线实施计划

- 已新增下一阶段实施计划：
  - `docs/plans/2026-05-16-量子未完成公式层四线letkf实验.md`
- 目标是补齐当前尚未系统完成的四类公式层改动：
  - `exp16_quantum_transform_letkf.py`
    - 只改集合变换矩阵 `T / w_pert`
  - `exp17_quantum_B_correction_letkf.py`
    - 只改背景协方差修正 `B_q`
  - `exp18_quantum_J_operator_letkf.py`
    - 直接改分析步代价函数 `J_q(w)`
  - `exp20_quantum_H_representation_letkf.py`
    - 用量子表示 `phi_q` 改观测表示空间
- 排序原则：
  - 先做 `T` 和 `B`，因为它们更接近现有 LETKF 骨架；
  - 再做 `J` 和 `H`，因为它们更理论、更可能重写解释体系。

### 2026-05-16：exp16 / exp17 / exp18 / exp20 已实现并静默发远端

- 已完成本地实现并通过语法检查：
  - `气象海洋/shiyan/exp16_quantum_transform_letkf.py`
  - `气象海洋/shiyan/exp17_quantum_B_correction_letkf.py`
  - `气象海洋/shiyan/exp18_quantum_J_operator_letkf.py`
  - `气象海洋/shiyan/exp20_quantum_H_representation_letkf.py`
- 四条线对应的公式位置：
  - `exp16`：只改集合变换矩阵 `T / w_pert`
  - `exp17`：只改背景协方差低秩修正 `B_q`
  - `exp18`：直接改分析步代价函数几何 `J_q(w)`
  - `exp20`：用量子表示 `phi_q` 改观测表示空间
- 已静默上传并启动远端：
  - `exp16`：`STARTED:216123`
  - `exp17`：`STARTED:216193`
  - `exp18`：`STARTED:216394`
  - `exp20`：`STARTED:216461`
- 约束保持不变：
  - 不在终端直接回显实验结果；
  - 后续统一只下载 `summary.json / summary.csv / result.csv` 到本地验收。

### 实验9：量子分组降阶表示验证

- 已完成 `exp9_quantum_reduced_group_letkf.py` 的首轮结果验收。
- 接入位置：
  - 不再直接在观测权重层引入量子信号；
  - 改为先做局部观测分组 / 降阶表示，再由经典更新完成组内分析。
- 固定参数：
  - `ens_size = 40`
  - `infl = 1.02`
  - `obs_std = 0.5`
  - `dt = 0.05`
  - `forcing = 8.0`
  - `seed = 2`
  - `support_radius = 20`
  - `group_threshold = 0.9`
  - `max_groups = 3`
  - `max_representatives = 2`
- 结果摘要：
  - `fixed`
    - `train RMSE = 0.1211974487`
    - `test_1 RMSE = 0.1287279125`
  - `corr`
    - `train RMSE = 0.1414554889`
    - `test_1 RMSE = 0.1427945539`
  - `quantum_reduced_group_update`
    - `train RMSE = 2.7047558869`
    - `test_1 RMSE = 2.6277235882`
    - `avg_group_count = 3.0`
    - `avg_group_size = 13.3333`
- 当前判断：
  - 这条“表示层分组 / 降阶”路线在当前版本明显退化；
  - 问题不在于是否形成了分组，而在于当前分组后的代表信息损失过大；
  - 因此 `exp9` 当前不适合作为可交付主线，应降级为失败对照实验。
- 本地结果文件：
  - `气象海洋/shiyan/formula_results_fetch/exp9_summary.json`

### 2026-05-16：exp19 / exp21 已实现并静默发远端

- 已新增实施计划文档：
  - `docs/plans/2026-05-16-量子增益迭代双线letkf实验.md`
- 已完成本地实现并通过检查：
  - `气象海洋/shiyan/exp19_quantum_gain_regularized_letkf.py`
  - `气象海洋/shiyan/exp21_iterative_quantum_letkf.py`
- 本地检查状态：
  - 两个脚本均已通过 `py_compile`
  - 编辑器诊断无报错
- 两条线对应的公式位置：
  - `exp19`
    - 增益 `K` 的结构化正则化
    - 用量子相似度矩阵构造图拉普拉斯，对局部增益行做平滑
  - `exp21`
    - 时间上的迭代更新
    - 用量子结构、innovation 与 spread 共同决定阻尼系数 `alpha_q`
- 已静默上传并启动远端：
  - `exp19`：`STARTED:216704`
  - `exp21`：`STARTED:216771`
- 结果验收策略保持不变：
  - 当前只确认远端已正常启动；

### 2026-05-16：rho-R 联合自适应三线 LETKF 已完成本地实现

- 已按 `docs/plans/2026-05-16-rho-r联合自适应三线letkf实验-design.md` 与 `docs/plans/2026-05-16-rho-r联合自适应三线letkf实验.md` 完成三条新实验脚本落地：
  - `气象海洋/shiyan/exp32_joint_quantum_rho_R_letkf.py`
  - `气象海洋/shiyan/exp33_adaptive_lambda_localization_letkf.py`
  - `气象海洋/shiyan/exp34_adaptive_lambda_structured_R_letkf.py`
- 三条线的职责固定为：
  - `exp32`
    - 联合 `rho_q + R_q`
    - 在同一局部分析步里同时使用量子局地化权重与结构化 `R`
  - `exp33`
    - 只把 `exp13` 的固定小 `lambda` 改成局部自适应 `lambda_i`
    - 自适应信号为 `quantum_signal + innovation_signal - spread_signal`
  - `exp34`
    - 只把 `exp10` 的固定 `lambda` 改成局部自适应 `lambda_i`
    - 自适应信号为 `corr_strength + quantum_consistency`
- 远端输出目录已固定隔离：
  - `exp32`
    - `/home/infra/qda_competition/experiments/joint_quantum_rho_R_letkf`
  - `exp33`
    - `/home/infra/qda_competition/experiments/adaptive_lambda_localization_letkf`
  - `exp34`
    - `/home/infra/qda_competition/experiments/adaptive_lambda_structured_R_letkf`
- 本地检查已通过：
  - `exp32 / exp33 / exp34` 均已通过 `py_compile`
  - 三个脚本在编辑器 `diagnostics` 中均无新增报错
- 当前阶段判断：
  - 这一轮没有再横向扩展新公式对象；
  - 而是把已有正信号最强的两条线 `rho` 与 `R` 推进到“联合化 + 自适应化”；
  - 下一步直接进入静默远端启动与结果验收。

### 2026-05-17：exp32-34 远端静默启动完成

- 三条实验已全部在远端启动：
  - `exp32`
    - 远端目录：`/home/infra/qda_competition/experiments/joint_quantum_rho_R_letkf`
    - 进程号：`220081`
  - `exp33`
    - 远端目录：`/home/infra/qda_competition/experiments/adaptive_lambda_localization_letkf`
    - 进程号：`219278`
  - `exp34`
    - 远端目录：`/home/infra/qda_competition/experiments/adaptive_lambda_structured_R_letkf`
    - 进程号：`219406`
- 本轮启动排查出的关键经验：
  - `exp32` 失败根因不在算法，而在远端启动链路；
  - 问题点集中在首条 `pkill` 触发了堡垒机会话异常中断；
  - 改为“跳过 `pkill`，先 `mkdir`，再分块 base64 上传脚本、远端解码、`py_compile`、`nohup` 启动”后恢复正常；
  - 说明后续遇到堡垒机终端对首条命令敏感时，优先采用分块上传并避免把清理命令放在首条。
- 下一步：
  - 等待三条线在远端生成 `summary.json / summary.csv / result.csv`；
  - 之后统一抓取并与 `exp10 / exp11 / exp13 / exp14` 做排序比较。

### 2026-05-17：rho-R-B 三元弱融合方案定稿

- 基于当前已下载的 `summary.json` 重新统一排序后，真正对 `fixed` 给出正增益的板块共有三条：
  - `exp13`
    - `rho_q` 量子局地化
    - 当前最强
  - `exp17`
    - `B_q` 背景扰动修正
    - 次强
  - `exp10`
    - `R_q` 结构化观测误差
    - 第三
- 当前判断更新：
  - 现在可以开始做“融合”，但不应把所有量子板块同权硬拼；
  - 最合理的结构是：
    - `rho` 主导
    - `R` 次级
    - `B` 弱修正
  - 即采用 `lam_rho > lam_r > lam_b` 的分层弱融合，而不是三者等强并入。
- 已新增设计文档：
  - `docs/plans/2026-05-17-rho-r-b三元弱融合letkf实验-design.md`
- 已新增实施计划：
  - `docs/plans/2026-05-17-rho-r-b三元弱融合letkf实验.md`
- 新主线实验命名固定为：
  - `exp35_triply_fused_rho_R_B_letkf.py`
- 首轮目标：
  - 先验证 `rho + R + weak_B` 是否至少优于 `exp10` 与 `exp17`
  - 再看是否能够接近或超过当前最强的 `exp13`

### 2026-05-17：exp35 三元弱融合脚本已完成本地实现

- 已创建：
  - `气象海洋/shiyan/exp35_triply_fused_rho_R_B_letkf.py`
- 当前实现遵循分层弱融合原则：
  - `rho` 主导局部观测参与
  - `R` 次级控制局部观测误差结构
  - `B` 仅做最弱背景扰动方向修正
- 当前脚本已固定首轮 4 组保守参数组合：
  - `(0.02, 0.01, 0.005)`
  - `(0.02, 0.02, 0.005)`
  - `(0.03, 0.01, 0.005)`
  - `(0.02, 0.01, 0.01)`
- 当前输出字段已补齐：
  - `lambda_rho`
  - `lambda_r`
  - `lambda_b`
  - `train_avg_b_correction_strength`
  - `test_1_avg_b_correction_strength`
- 本地检查已通过：
  - `exp35` 已通过 `py_compile`
  - 编辑器 `diagnostics` 无新增报错
- 下一步：
  - 按静默方式上传并远端启动 `exp35`
  - 后续与 `exp13 / exp17 / exp10 / fixed` 统一排序验收

### 2026-05-17：exp35 三元弱融合已远端启动

- `exp35` 已在远端启动：
  - 远端目录：`/home/infra/qda_competition/experiments/triply_fused_rho_R_B_letkf`
  - 进程号：`220223`
- 本轮启动方式继续采用已验证成功的稳妥链路：
  - 先 `mkdir`
  - 再分块 base64 上传
  - 远端解码写入 `/tmp/exp35_triply_fused_rho_R_B_letkf.py`
  - `py_compile`
  - `nohup` 后台启动
- 当前已确认：
  - 远端脚本写入成功
  - 远端 `py_compile` 通过
  - 后台任务已成功拿到 `STARTED`
- 下一步：
  - 等待 `summary.json / summary.csv / result.csv`
  - 与 `exp13 / exp17 / exp10 / fixed` 做统一排序验收

### 2026-05-17：rho-B 二元弱融合方案定稿

- 在等待 `exp32 / exp33 / exp35` 的同时，新增一条更保守的新方案线：
  - `rho + weak_B`
- 当前判断：
  - `rho` 仍是最强主线；
  - `B` 是次强修正项；
  - 若短期目标是“尽量稳地继续提升”，则先拿掉 `R`，只验证 `rho` 与 `weak_B` 的二元兼容性，更适合做低风险并行线。
- 新方案命名固定为：
  - `exp36_binary_rho_B_letkf.py`
- 设计原则固定为：
  - `rho` 主导局部观测参与
  - `B` 只做末端弱修正
  - `lam_rho > lam_b`
  - 不叠加 `R`
  - 不做自适应
- 已新增设计文档：
  - `docs/plans/2026-05-17-rho-b二元弱融合letkf实验-design.md`
- 已新增实施计划：
  - `docs/plans/2026-05-17-rho-b二元弱融合letkf实验.md`
- 首轮参数固定为：
  - `lam_rho = [0.02, 0.03]`
  - `lam_b = [0.003, 0.005]`
- 首轮目标：
  - 至少优于 `exp17`
  - 尽量逼近 `exp13`
  - 同时观察该二元线是否比三元融合更稳

### 2026-05-17：exp36 二元弱融合脚本已完成本地实现

- 已创建：
  - `气象海洋/shiyan/exp36_binary_rho_B_letkf.py`
- 当前实现遵循二元弱融合原则：
  - `rho` 主导局部观测参与
  - `B` 仅做末端弱修正
  - 不叠加 `R`
- 当前脚本已固定首轮 4 组保守参数组合：
  - `(0.02, 0.003)`
  - `(0.02, 0.005)`
  - `(0.03, 0.003)`
  - `(0.03, 0.005)`
- 当前输出字段已补齐：
  - `lambda_rho`
  - `lambda_b`
  - `train_avg_b_correction_strength`
  - `test_1_avg_b_correction_strength`
- 本地检查已通过：
  - `exp36` 已通过 `py_compile`
  - 编辑器 `diagnostics` 无新增报错
- 下一步：
  - 按静默方式上传并远端启动 `exp36`
  - 后续与 `exp13 / exp17 / fixed` 统一排序验收

### 2026-05-17：exp36 二元弱融合已远端启动

- `exp36` 已在远端启动：
  - 远端目录：`/home/infra/qda_competition/experiments/binary_rho_B_letkf`
  - 进程号：`220523`
- 本轮启动方式继续采用已验证成功的稳妥链路：
  - 先 `mkdir`
  - 再分块 base64 上传
  - 远端解码写入 `/tmp/exp36_binary_rho_B_letkf.py`
  - `py_compile`
  - `nohup` 后台启动
- 当前已确认：
  - 远端脚本写入成功
  - 远端 `py_compile` 通过
  - 后台任务已成功拿到 `STARTED`
- 下一步：
  - 等待 `summary.json / summary.csv / result.csv`
  - 与 `exp13 / exp17 / fixed` 做统一排序验收

### 2026-05-17：四条新融合线方案定稿

- 为了不在等待 `exp32-36` 期间空转，决定继续并行开 4 条新的最小弱融合线：
  - `exp37_rho_J_weak_fusion_letkf.py`
  - `exp38_rho_inflation_weak_fusion_letkf.py`
  - `exp39_rho_adaptive_B_letkf.py`
  - `exp40_R_B_weak_fusion_letkf.py`
- 当前统一策略：
  - 四条都做最小弱融合版
  - 除 `exp39` 外，其余不做自适应
  - 全部保留 `fixed / corr` 对照
  - 全部静默挂远端
- 新增总设计文档：
  - `docs/plans/2026-05-17-四条新融合letkf实验-design.md`
- 新增总实施计划：
  - `docs/plans/2026-05-17-四条新融合letkf实验.md`
- 当前判断目标：
  - `exp37` 看 `rho + J` 是否比单独 `J` 稳
  - `exp38` 看 `rho + inflation` 是否改善泛化
  - `exp39` 看 `rho + adaptive_B` 是否优于 `exp36`
  - `exp40` 看 `R + B` 两个次级正信号能否互补
  - 不在终端直接回显结果；
  - 后续统一下载 `summary.json / summary.csv / result.csv` 到本地验收。

### 2026-05-17：exp37-40 已修复并按 base64 链路重新远端启动

- 已完成本地修复：
  - `exp37_rho_J_weak_fusion_letkf.py`
    - 修正 `lam_j` 相关命名残留
    - 修正实验构造与结果文件名中的 `lam_b` 残留
  - `exp38_rho_inflation_weak_fusion_letkf.py`
    - 修正 `lam_infl` 相关命名残留
    - 修正 `summary.csv` 字段名从 `lambda_b` 到 `lambda_infl`
  - `exp40_R_B_weak_fusion_letkf.py`
    - 修正 `build_experiments()` 中 `fixed / corr` 的元组长度错误
- 本地校验已通过：
  - `exp37`
  - `exp38`
  - `exp39`
  - `exp40`
  - 四条脚本均已通过 `py_compile`
- 本轮远端启动方式：
  - 使用 `ssh -tt jump`
  - 本地脚本转 `base64`
  - 远端写入 `/tmp/*.py`
  - 远端 `python3 -m py_compile`
  - `nohup python3 ... > run.log 2>&1 < /dev/null &`
- 当前已拿到新的后台进程号：
  - `exp37`：`STARTED:222654`
  - `exp38`：`STARTED:222792`
  - `exp39`：`STARTED:222920`
  - `exp40`：`STARTED:223048`
- 启动后短回查结果：
  - 四条进程都仍在运行
  - 四个远端目录均已开始产出 `fixed / corr` 的 `train` 与 `test_1` 预测 CSV
  - `run.log` 已开始写入 `DONE {...}` 记录，说明实验已进入正式计算阶段而非秒退
- 当前远端目录：
  - `exp37`：`/home/infra/qda_competition/experiments/rho_J_weak_fusion_letkf`
  - `exp38`：`/home/infra/qda_competition/experiments/rho_inflation_weak_fusion_letkf`
  - `exp39`：`/home/infra/qda_competition/experiments/rho_adaptive_B_letkf`
  - `exp40`：`/home/infra/qda_competition/experiments/R_B_weak_fusion_letkf`

### 2026-05-17：exp37-40 结果已回查完成

- 四条新融合实验均已完成并生成 `summary.json`
- 相对 `fixed` 基线 `test_1 RMSE = 0.1287279125` 的结果：
  - `exp37 rho + J` 最优：`0.1269847690`
  - `exp38 rho + inflation` 最优：`0.1272991074`
  - `exp39 rho + adaptive_B` 最优：`0.1272579609`
  - `exp40 R + B` 最优：`0.1281659187`
- 当前四条新融合线内部排序：
  - 第 1：`exp37 rho + J`
  - 第 2：`exp39 rho + adaptive_B`
  - 第 3：`exp38 rho + inflation`
  - 第 4：`exp40 R + B`
- 与此前已下载主线结果对比：
  - `exp13` 最优 `test_1 RMSE = 0.1276904682`
  - `exp17` 最优 `test_1 RMSE = 0.1279326778`
  - `exp10` 最优 `test_1 RMSE = 0.1282514861`
- 当前阶段结论更新：
  - `exp37` 已超过 `exp13`，成为当前已知最优结果
  - `exp39` 与 `exp38` 也都超过 `exp13`
  - `exp40` 虽优于 `fixed` 与 `corr`，但未超过 `exp13`
- 当前最值得继续深化的融合方向：
  - 首推 `rho + J`
  - 次推 `rho + adaptive_B`
  - `R + B` 暂不适合作为主融合线

### 2026-05-17：rho+J 门控与三元弱融合双线设计已定稿

- 根据 `exp37` 与 `exp39` 的结果，当前决定不做大范围扫参，改做结构优化
- 新一轮双线主攻方向已固定：
  - `exp41_rho_J_confidence_gated_letkf.py`
  - `exp42_rho_J_adaptive_B_gated_letkf.py`
- 当前核心结构判断：
  - `exp41` 用 `j_confidence` 优化 `rho + J`
  - `exp42` 在 `exp41` 基础上增加 `adaptive_B` 第二层弱补强
  - 两条都坚持 `rho` 主导，不回到 `R` 主线
- 已新增设计文档：
  - `docs/plans/2026-05-17-rho-j门控与三元弱融合letkf实验-design.md`
- 已新增实施计划：
  - `docs/plans/2026-05-17-rho-j门控与三元弱融合letkf实验.md`
- 当前执行原则：
  - 不改 `exp37-40`
  - 新增独立脚本
  - 继续采用 `ssh -tt jump + base64 + /tmp + nohup`
  - 结果统一和 `exp37 / exp39 / exp13 / fixed` 比较

### 2026-05-16：exp22-31 量子基线公式扩展十线总计划

- 已按“全都试试”的要求整理出下一阶段独立实施计划：
  - `docs/plans/2026-05-16-量子基线公式扩展十线letkf实验.md`
- 这轮计划对应 10 条尚未系统实现的基线公式扩展线：
  - `exp22_hierarchical_hyperprior_letkf.py`
  - `exp23_structured_prior_metric_letkf.py`
  - `exp24_student_t_letkf.py`
  - `exp25_constraint_kkt_letkf.py`
  - `exp26_trust_region_iterative_letkf.py`
  - `exp27_lowrank_sparse_B_letkf.py`
  - `exp28_risk_sensitive_letkf.py`
  - `exp29_time_correlated_R_letkf.py`
  - `exp30_transport_geometry_letkf.py`
  - `exp31_em_hyperparameter_letkf.py`
- 当前分批顺序：
  - A 批：`exp22 + exp23 + exp24`
  - B 批：`exp25 + exp26 + exp27`
  - C 批：`exp28 + exp29 + exp30 + exp31`
- 当前优先级判断：
  - 第一梯队：层次贝叶斯、结构化先验几何、Student-t 重尾
  - 第二梯队：约束 KKT、信赖域迭代、低秩稀疏背景协方差
  - 第三梯队：风险敏感、时序相关观测误差、传输几何、EM 联合估计
- 执行约束保持不变：
  - 继续采用“本地写脚本、静默上传远端、最后统一下载结果验收”
  - 每条实验独立输出目录
  - 不在终端直接回显远端结果内容

### 2026-05-16：rho / R 联合自适应三线计划定稿

- 基于当前已下载并整理的结果，最新排序已经明确：
  - `exp13` 量子局地化核 `rho_q` 当前最强
  - `exp10` 结构化观测误差 `R_q` 次强
  - `exp11` 接近但未超
  - `exp14` 轻微退化
- 当前阶段判断更新：
  - 不再优先横向扩更多公式对象；
  - 先沿着已经证明有效的两条主线 `rho` 与 `R` 继续深化；
  - 重点从“固定小 lambda”推进到“联合接入 + 局部自适应”。
- 已新增设计文档：
  - `docs/plans/2026-05-16-rho-r联合自适应三线letkf实验-design.md`
- 已新增实施计划：
  - `docs/plans/2026-05-16-rho-r联合自适应三线letkf实验.md`
- 本轮拟实现三条新实验：
  - `exp32_joint_quantum_rho_R_letkf.py`
    - 联合 `rho_q + R_q`
  - `exp33_adaptive_lambda_localization_letkf.py`
    - 把 `exp13` 的固定 `lambda` 改成局部自适应 `lambda_i`
  - `exp34_adaptive_lambda_structured_R_letkf.py`
    - 把 `exp10` 的固定 `lambda` 改成局部自适应 `lambda_i`
- 当前执行顺序：
  - 先 `exp32`
  - 再 `exp33`
  - 最后 `exp34`
- 当前止损规则：
  - 若 `exp32` 全部组合都明显差于 `exp10/13`，说明当前 `rho` 与 `R` 不宜直接联用；
  - 若 `exp33/34` 的自适应规则普遍差于固定小 `lambda`，优先回退到更保守的自适应公式；
  - 若出现 `NaN` 或病态矩阵，先修数值稳定，不扩大参数范围。

### 2026-05-17：提交目录 `tijiao` 已整理完成

- 已按“代码 / 文档 / 结果”三类，把当前项目中重要的实验相关文件复制到 `d:\Desktop\laingzimuxi\tijiao`
- 已复制的代码范围：
  - `气象海洋` 下核心 Python 脚本
  - `气象海洋/shiyan` 下实验脚本 `exp2` 到 `exp42`
- 已复制的文档范围：
  - 根目录重要 Markdown 文档
  - `docs/plans` 下实验设计与实施计划
  - `lunwenfenxi` 及其 `2 / 3 / 4` 子目录中的分析文档
- 已复制的结果范围：
  - `formula_results_fetch/downloaded_results` 下已有 `result.csv / summary.csv / summary.json / manifest.json`
  - `shiyan` 根目录中保存的远端状态检查、运行日志和结果摘要文件
- 已新增：
  - `tijiao/README.md`
    - 用于说明提交目录结构与当前打包内容

### 2026-05-17：当前最高分方案可视化已生成

- 已围绕当前最高分主线 `exp37 rho + J` 生成提交可用图，输出目录：
  - `d:\Desktop\laingzimuxi\tijiao\figures`
- 已生成图片：
  - `best_model_rmse_comparison.png`
    - 当前主线与高分候选的 `test_1 RMSE` 对比图
  - `exp37_param_heatmap.png`
    - `exp37` 在不同 `lambda_rho / lambda_j` 组合下的 `test_1 RMSE` 热图
  - `exp37_j_strength_vs_rmse.png`
    - `exp37` 的平均 `J` 修正强度与 `test_1 RMSE` 关系图
- 已补充：
  - `tijiao/figures/README.md`
    - 说明每张图的用途，便于后续写算法说明文档

### 2026-05-17：补充高分方案说明图完成

- 在 `tijiao/figures` 下继续补充了更适合写算法说明文档的对比图：
  - `rmse_gain_over_fixed.png`
    - 各高分方法相对 `fixed` 基线的 `test_1 RMSE` 提升幅度
  - `train_test_rmse_grouped.png`
    - 高分方法的 `train / test` 双指标分组柱状图
  - `train_test_scatter_best_models.png`
    - 高分方法的 `train / test RMSE` 散点分布
- 已同步更新：
  - `tijiao/figures/README.md`
    - 追加新图的用途说明

### 2026-05-17：提交版 README 按官方要求重写

- 已按官方提交要求重写：
  - `d:\Desktop\laingzimuxi\tijiao\README.md`
- 当前 README 已补齐以下内容：
  - 开发环境与依赖版本
  - 环境配置文件位置
  - 代码目录结构与各文件功能
  - 所有可运行源代码文件清单
  - 一键运行命令与参数说明
  - 输入输出文件格式
  - 预期运行时间与硬件要求
  - 相关运行结果与结果呈现代码位置
- 已新增环境配置文件：
  - `d:\Desktop\laingzimuxi\tijiao\requirements.txt`
- 当前 README 重点把提交主线明确为：
  - `code/qixianghaiyang/shiyan/exp37_rho_J_weak_fusion_letkf.py`
  - `tools/day2_exp37_remote_runner.py`
  - `tools/generate_exp37_interpretability_figures.py`
  - `tools/generate_submission_extra_figures.py`
- 当前写法已把“主实验验证环境”和“本地整理出图环境”分开说明，避免只写一种环境导致官方复现时信息不完整。
