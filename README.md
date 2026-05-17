# 量子数据同化项目提交说明

本目录按官方提交要求整理，覆盖以下四类内容：

1. 所有可运行的源代码文件
2. 环境配置文件
3. 详细 `README.md`
4. 相关运行结果与结果呈现代码

当前推荐的正式复现实验主线为：

- 主方法脚本：`code/qixianghaiyang/shiyan/exp37_rho_J_weak_fusion_letkf.py`
- 远端批量运行工具：`tools/day2_exp37_remote_runner.py`
- 图表生成脚本：
  - `tools/generate_exp37_interpretability_figures.py`
  - `tools/generate_submission_extra_figures.py`

## 1. 开发环境与依赖版本

本项目实际包含两类环境：

### 1.1 主实验验证环境

- 操作系统：`Ubuntu 22.04.5 LTS`
- Python：`3.10.12`
- 关键依赖：
  - `numpy 2.2.6`
  - `scipy 1.15.3`
  - `qiskit 2.4.0`
- 典型硬件：
  - CPU：`64` 核
  - 内存：约 `515 GB`
  - GPU：`4 x MetaX C500X 64GB`

说明：

- 当前最高分主线 `exp37` 使用 `qiskit.quantum_info.Statevector` 做 `4-qubit` 量子特征映射与态重叠计算。
- 当前主线脚本可在 CPU 上运行，GPU 不是必要条件；远端大内存/多核环境主要用于批量实验和多结果下载整理。

### 1.2 本地整理与出图环境

- 操作系统：`Windows`
- Python：当前本地整理环境可用 `Python 3.13`
- 本地已检测到的依赖版本：
  - `numpy 2.4.3`
  - `pandas 3.0.2`
  - `matplotlib 3.10.8`

### 1.3 环境配置文件

- 文件：`requirements.txt`
- 作用：给出本提交目录推荐的最小依赖集合，便于在新环境中快速安装

安装命令：

```bash
pip install -r requirements.txt
```

## 2. 代码目录结构与各文件功能

### 2.1 顶层目录

- `code/qixianghaiyang/`
  - 主代码区，包含参考 4D-Var 演示和 `shiyan/` 实验脚本
- `tools/`
  - 运行辅助和可视化生成脚本
- `results/`
  - 已下载实验结果、远端状态、图表分析输入
- `figures/`
  - 已生成的提交图表
- `paper_sections/`
  - 论文 LaTeX 分章节文件
- `docs/`
  - 方案文档、实验计划、赛题说明整理
- `analysis/`
  - 文献调研与理论分析副本

### 2.2 所有可运行的源代码文件

下列 `.py` 文件均为可直接运行的源码文件。

#### A. 正式提交主线与辅助入口

- `code/qixianghaiyang/shiyan/exp37_rho_J_weak_fusion_letkf.py`
  - 当前正式主线；实现 `rho + J` 弱融合 LETKF，并输出 `summary.json / summary.csv / result.csv`
- `tools/day2_exp37_remote_runner.py`
  - 通过 `ssh jump` 把 `exp37` 和比赛数据上传到远端，并依次执行 `test_1` 到 `test_5`
- `tools/generate_exp37_interpretability_figures.py`
  - 基于 `results/exp37_analysis/` 中的数据生成解释性图组
- `tools/generate_submission_extra_figures.py`
  - 生成电路图、流程图、偏差方差分析图、Top-K 维度收益图等提交附加图
- `code/qixianghaiyang/shiyan/launch_remote_via_jump.py`
  - 通用远端上传/启动辅助脚本，适用于通过堡垒机静默发实验

#### B. 早期结构验证实验

- `code/qixianghaiyang/shiyan/exp2_structure_analysis.py`
  - 经典代理核结构分析与可视化
- `code/qixianghaiyang/shiyan/exp3_quantum_kernel_structure.py`
  - 量子核矩阵结构验证
- `code/qixianghaiyang/shiyan/exp3_render_plots.py`
  - 将实验 3 的结构结果渲染成图片
- `code/qixianghaiyang/shiyan/exp4_quantum_weighted_letkf.py`
  - 量子核直接接入 LETKF 的最小验证
- `code/qixianghaiyang/shiyan/exp5_quantum_mixed_weight_letkf.py`
  - 量子核与经典距离先验的混合权重实验

#### C. 表示层/分组/公式层扩展实验

- `code/qixianghaiyang/shiyan/exp6_quantum_credibility_features.py`
  - 量子可信度特征实验
- `code/qixianghaiyang/shiyan/exp7_quantum_grouped_letkf.py`
  - 量子分组 LETKF 实验
- `code/qixianghaiyang/shiyan/exp8_quantum_block_mix_letkf.py`
  - 量子 block 弱混合实验
- `code/qixianghaiyang/shiyan/exp9_quantum_reduced_group_letkf.py`
  - 量子降阶/分组表示实验
- `code/qixianghaiyang/shiyan/exp10_quantum_structured_R_letkf.py`
  - 结构化 `R` 量子接入
- `code/qixianghaiyang/shiyan/exp11_quantum_S_operator_letkf.py`
  - `S` 算子量子化实验
- `code/qixianghaiyang/shiyan/exp12_quantum_reduced_analysis_space_letkf.py`
  - 降阶分析空间实验
- `code/qixianghaiyang/shiyan/exp13_quantum_localization_letkf.py`
  - `rho` 量子局地化实验
- `code/qixianghaiyang/shiyan/exp14_quantum_inflation_letkf.py`
  - 量子 inflation 实验
- `code/qixianghaiyang/shiyan/exp15_quantum_robust_innovation_letkf.py`
  - 量子 robust innovation 实验
- `code/qixianghaiyang/shiyan/exp16_quantum_transform_letkf.py`
  - 分析变换矩阵量子修正
- `code/qixianghaiyang/shiyan/exp17_quantum_B_correction_letkf.py`
  - 背景协方差 `B` 的量子修正
- `code/qixianghaiyang/shiyan/exp18_quantum_J_operator_letkf.py`
  - `J` 算子几何修正实验
- `code/qixianghaiyang/shiyan/exp19_quantum_gain_regularized_letkf.py`
  - 增益正则化实验
- `code/qixianghaiyang/shiyan/exp20_quantum_H_representation_letkf.py`
  - 观测表示空间实验
- `code/qixianghaiyang/shiyan/exp21_iterative_quantum_letkf.py`
  - 迭代量子 LETKF 实验

#### D. 融合、自适应与门控实验

- `code/qixianghaiyang/shiyan/exp32_joint_quantum_rho_R_letkf.py`
  - `rho + R` 联合实验
- `code/qixianghaiyang/shiyan/exp33_adaptive_lambda_localization_letkf.py`
  - `rho` 自适应 lambda 局地化实验
- `code/qixianghaiyang/shiyan/exp34_adaptive_lambda_structured_R_letkf.py`
  - `R` 自适应 lambda 实验
- `code/qixianghaiyang/shiyan/exp35_triply_fused_rho_R_B_letkf.py`
  - `rho + R + B` 三元弱融合实验
- `code/qixianghaiyang/shiyan/exp36_binary_rho_B_letkf.py`
  - `rho + B` 二元弱融合实验
- `code/qixianghaiyang/shiyan/exp38_rho_inflation_weak_fusion_letkf.py`
  - `rho + inflation` 弱融合实验
- `code/qixianghaiyang/shiyan/exp39_rho_adaptive_B_letkf.py`
  - `rho + adaptive_B` 自适应实验
- `code/qixianghaiyang/shiyan/exp40_R_B_weak_fusion_letkf.py`
  - `R + B` 弱融合实验
- `code/qixianghaiyang/shiyan/exp41_rho_J_confidence_gated_letkf.py`
  - `rho + J` 置信门控实验
- `code/qixianghaiyang/shiyan/exp42_rho_J_adaptive_B_gated_letkf.py`
  - `rho + J + adaptive_B` 双门控实验

#### E. 参考/演示脚本

- `code/qixianghaiyang/quantum_enhanced_4dvar.py`
  - 参考性量子增强 4D-Var 原型，含 `scipy.optimize`
- `code/qixianghaiyang/quantum_enhanced_4dvar_demo.py`
  - 简化演示版 4D-Var；更适合读思路，不是当前正式提交主线

说明：

- `shiyan/` 下多数实验脚本采用统一命令行风格，支持：
  - `--train-input`
  - `--test-input`
  - `--output-dir`
- 当前正式推荐复现实验只需要运行 `exp37` 与 `tools/` 下两个出图脚本。

## 3. 一键运行命令与参数说明

### 3.1 正式主线：本地单实验运行

命令：

```bash
python code/qixianghaiyang/shiyan/exp37_rho_J_weak_fusion_letkf.py ^
  --train-input <训练集CSV路径> ^
  --test-input <测试集CSV路径> ^
  --output-dir <输出目录>
```

参数说明：

- `--train-input`
  - 训练集 CSV 路径，通常为 `lorenz96_train.csv`
- `--test-input`
  - 测试集 CSV 路径，通常为 `lorenz96_test_1.csv`
- `--output-dir`
  - 输出目录；脚本会在该目录下写出预测文件和统计汇总

### 3.2 正式主线：远端批量五测试集运行

命令：

```bash
python tools/day2_exp37_remote_runner.py launch
python tools/day2_exp37_remote_runner.py check
```

说明：

- `launch`
  - 通过 `ssh -tt jump` 上传 `exp37` 脚本与 `lorenz96_train.csv`、`lorenz96_test_1.csv` 到 `lorenz96_test_5.csv`
  - 远端依次运行 5 个测试集
- `check`
  - 回查远端目录、进程、日志与结果状态

使用前提：

- 本机已配置可用的 `ssh jump`
- 远端有 Python 3 和 `qiskit`
- 当前脚本默认使用仓库中的固定本地绝对路径与远端目录

### 3.3 解释图与提交图生成

命令：

```bash
python tools/generate_exp37_interpretability_figures.py
python tools/generate_submission_extra_figures.py
```

输出目录：

- `figures/`

### 3.4 其他实验脚本

`code/qixianghaiyang/shiyan/` 下其他 `exp*.py` 脚本可按同类命令运行：

```bash
python code/qixianghaiyang/shiyan/<实验脚本名>.py ^
  --train-input <训练集CSV路径> ^
  --test-input <测试集CSV路径> ^
  --output-dir <输出目录>
```

若某脚本参数略有差异，请以该脚本中的 `parse_args()` 定义为准。

## 4. 输入输出文件格式

### 4.1 输入文件格式

比赛输入 CSV 采用如下字段：

```text
time_step,dimension,true_value,observed_value
```

字段说明：

- `time_step`
  - 时间步编号
- `dimension`
  - Lorenz96 状态维编号
- `true_value`
  - 真值；训练集和验证分析时可见
- `observed_value`
  - 带噪观测值

样例见：

- `results/exp37_analysis/lorenz96_test_1.csv`

### 4.2 主要输出文件格式

#### `result.csv` / `best_test_prediction.csv`

```text
time_step,dimension,predicted_value
```

说明：

- 每一行对应一个时间步、一个维度的最终预测值
- `result.csv` 为官方提交最需要的预测结果文件

#### `summary.csv`

典型字段包括：

```text
method,lambda_rho,lambda_j,support_radius,train_rmse,train_mae,train_count,test_1_rmse,test_1_mae,test_1_count
```

不同实验脚本会把特定参数替换为对应字段，例如：

- `lambda`
- `lambda_j`
- `lambda_b`
- `lambda_infl`
- `train_avg_j_correction_strength`
- `test_1_avg_b_correction_strength`

#### `summary.json`

结构通常包含三部分：

- `config`
  - 当前脚本固定超参数
- `results`
  - 全部组合的结果列表
- `best_test`
  - 当前脚本在测试集上的最佳组合

#### `manifest.json`

说明远端实验目录下是否成功写出：

- `summary.json`
- `summary.csv`
- `result.csv`

## 5. 预期运行时间与硬件要求

以下时间为提交复现时的建议预留时间，不同 CPU、磁盘和远端负载会影响实际用时。

### 5.1 推荐硬件

- 最低建议：
  - CPU：`8` 核
  - 内存：`16 GB`
  - Python：`3.10+`
- 推荐：
  - CPU：`32` 核以上
  - 内存：`64 GB` 以上
  - 已安装 `qiskit`

说明：

- 当前主线采用 `Statevector` 相似度计算，GPU 不是硬性要求。
- 若只做图表整理，普通笔记本 CPU 也可完成。

### 5.2 预期运行时间

- `exp37_rho_J_weak_fusion_letkf.py`
  - 单次 `train + test_1` 全部组合扫描，建议预留 `10` 到 `40` 分钟
- `day2_exp37_remote_runner.py launch`
  - 顺序跑 `test_1` 到 `test_5`，建议预留 `1` 到 `3` 小时
- `generate_exp37_interpretability_figures.py`
  - 通常 `1` 到 `5` 分钟
- `generate_submission_extra_figures.py`
  - 通常 `1` 到 `3` 分钟

## 6. 相关运行结果与呈现代码

### 6.1 已保存结果

- `results/downloaded_results/`
  - 已下载的实验结果目录，含 `exp9`、`exp10`、`exp11`、`exp12`、`exp13`、`exp14`、`exp16`、`exp17`、`exp19`、`exp20`、`exp21`
  - 每个子目录通常包含：
    - `manifest.json`
    - `summary.json`
    - `summary.csv`
    - `result.csv`
- `results/status/`
  - 远端状态检查、运行日志、摘要文本、CPU/GPU 状态
- `results/exp37_analysis/`
  - 当前最好方案 `exp37` 的分析数据与派生统计文件

### 6.2 结果呈现代码

- `tools/generate_exp37_interpretability_figures.py`
  - 生成 `exp37` 的误差分布图、热力图、时间趋势图、代表性切片图、局地窗口解释图等
- `tools/generate_submission_extra_figures.py`
  - 生成电路示意图、方法流程图、消融逻辑图、偏差方差图、Top-K 收益图和量子比特合规图
- `figures/README.md`
  - 对每张图的用途做了逐项说明

### 6.3 当前关键结果

当前正式主线 `exp37` 的核心结果为：

- `fixed`：`test_1 RMSE = 0.12872791254901936`
- `exp37 最优`：`test_1 RMSE = 0.12698476904637393`
- `corr`：`test_1 RMSE = 0.14279455390011997`

对应统计汇总可见：

- `results/exp37_analysis/exp37_quant_stats.json`

## 7. 文档与论文材料

- `paper_cvpr_report.tex`
  - 主论文 LaTeX 文件
- `tijiao/paper_cvpr_report.pdf`
  - 最终报告论文 PDF 文件
- `paper_sections/`
  - 分章节 LaTeX 文件
- `docs/root_md/`
  - 根目录重要说明文档副本
- `docs/plans/`
  - 实验设计和实施计划副本
- `docs/qixianghaiyang/`
  - 赛题说明整理

## 8. 使用建议

- 若官方只检查“可复现主结果”，优先运行：
  - `code/qixianghaiyang/shiyan/exp37_rho_J_weak_fusion_letkf.py`
  - `tools/generate_exp37_interpretability_figures.py`
  - `tools/generate_submission_extra_figures.py`
- 若官方需要检查“是否包含全部过程代码”，再查看：
  - `code/qixianghaiyang/shiyan/exp2` 到 `exp42`
- 若官方需要检查“环境配置文件”，直接使用：
  - `requirements.txt`

## 9. 备注

- 当前提交目录是“重要文件副本整理区”，核心目标是便于提交、复核和答辩展示。
- 当前主实验线统一使用 `4` qubits，满足“不超过 `30` qubits”的赛题限制。
- `quantum_enhanced_4dvar.py` 与 `quantum_enhanced_4dvar_demo.py` 更偏参考/演示性质，不是当前正式提交主线。
