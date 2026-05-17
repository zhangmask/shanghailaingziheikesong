# rho+J 门控与三元弱融合 LETKF 实验 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 新增 `exp41` 与 `exp42` 两条结构优化实验线，在不做大范围参数扫描的前提下验证 `J` 门控和 `J+B` 双门控是否优于当前最优融合线。

**Architecture:** 继续复用 `exp37` 的 `rho + J` 主骨架与 `exp39` 的 `adaptive_B` 思路，但把原先“固定强度修正”改成“保守置信门控修正”。`exp41` 只优化 `J` 的可信触发，`exp42` 在 `exp41` 基础上再串接 `adaptive_B` 的第二层弱补偿。

**Tech Stack:** Python 3、NumPy、Qiskit 2.4、Markdown、远端 Ubuntu、`ssh -tt jump`

---

### Task 1: 固定新实验命名与输出目录

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_letkf.py`
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp42_rho_J_adaptive_B_gated_letkf.py`
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 固定脚本命名**

- `exp41_rho_J_confidence_gated_letkf.py`
- `exp42_rho_J_adaptive_B_gated_letkf.py`

**Step 2: 固定远端输出目录**

- `exp41`: `/home/infra/qda_competition/experiments/rho_J_confidence_gated_letkf`
- `exp42`: `/home/infra/qda_competition/experiments/rho_J_adaptive_B_gated_letkf`

**Step 3: 固定对照组**

- `fixed`
- `corr`
- `exp41` 新方法
- `exp42` 新方法

### Task 2: 基于 exp37 抽出 J 门控结构

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp37_rho_J_weak_fusion_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp18_quantum_J_operator_letkf.py`

**Step 1: 复制 `exp37` 主骨架**

- 保留 `rho` 主导观测参与
- 保留 `fixed / corr` 对照
- 保留结果输出格式与 `summary.json / summary.csv / result.csv`

**Step 2: 新增 J 门控辅助函数**

- 新增 `compute_quantum_focus()`
- 新增 `compute_innovation_strength()`
- 新增 `compute_j_confidence()`

**Step 3: 修改 J 修正公式**

把：

```python
corrected = state_signal + lam_j * j_mode
```

改成：

```python
corrected = state_signal + lam_j * j_confidence * j_mode
```

**Step 4: 记录统计量**

- `avg_j_correction_strength`
- `avg_j_confidence`

### Task 3: 固定 exp41 的最小参数组合

**Files:**
- Modify: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_letkf.py`

**Step 1: 只保留当前最优附近的小组合**

- `LAMBDA_COMBOS = [(0.02, 0.003), (0.02, 0.004), (0.03, 0.003)]`

**Step 2: 不扩大搜索空间**

- 不加入额外扫描循环
- 不引入第二套门控公式

### Task 4: 基于 exp41 与 exp39 组装 exp42

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp42_rho_J_adaptive_B_gated_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp39_rho_adaptive_B_letkf.py`

**Step 1: 复用 exp41 的 `rho + J` 骨架**

- 先得到 `j_corrected`

**Step 2: 从 exp39 引入 `adaptive_B` 思路**

- 复用局部量子窗口构造
- 复用 `B` 修正方向构造

**Step 3: 新增 B 门控辅助函数**

- 新增 `compute_alignment()`
- 新增 `compute_spread_penalty()`
- 新增 `compute_b_confidence()`

**Step 4: 串联双门控修正**

```python
j_corrected = state_signal + lam_j * j_confidence * j_mode
final_corrected = j_corrected + lam_b_i * b_confidence * b_mode
```

### Task 5: 修正 exp39 的结构经验在 exp42 中的空参数问题

**Files:**
- Modify: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp42_rho_J_adaptive_B_gated_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp39_rho_adaptive_B_letkf.py`

**Step 1: 不再保留无实际作用的外层 `lambda_b` 扫描**

- `adaptive_B` 仅通过局部自适应 `lam_b_i` 控制

**Step 2: 让 `lam_b_i` 受更多结构量约束**

- `quantum_signal`
- `innovation_signal`
- `alignment`
- `spread_penalty`

**Step 3: 固定保守裁剪区间**

- `lam_b_i = clip(..., 0.0015, 0.006)`

### Task 6: 统一输出字段

**Files:**
- Modify: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_letkf.py`
- Modify: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp42_rho_J_adaptive_B_gated_letkf.py`

**Step 1: exp41 输出字段**

- `lambda_rho`
- `lambda_j`
- `train_avg_j_correction_strength`
- `test_1_avg_j_correction_strength`
- `train_avg_j_confidence`
- `test_1_avg_j_confidence`

**Step 2: exp42 输出字段**

- `lambda_rho`
- `lambda_j`
- `train_avg_j_correction_strength`
- `test_1_avg_j_correction_strength`
- `train_avg_j_confidence`
- `test_1_avg_j_confidence`
- `train_avg_b_correction_strength`
- `test_1_avg_b_correction_strength`
- `train_avg_b_confidence`
- `test_1_avg_b_confidence`

### Task 7: 本地语法校验

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_letkf.py`
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp42_rho_J_adaptive_B_gated_letkf.py`

**Step 1: 运行 `py_compile`**

Run:

- `python -m py_compile "d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_letkf.py"`
- `python -m py_compile "d:\Desktop\laingzimuxi\气象海洋\shiyan\exp42_rho_J_adaptive_B_gated_letkf.py"`

Expected:

- 两条都退出码 `0`

**Step 2: 检查诊断**

- 只修本次新增脚本的明确报错

### Task 8: 远端静默上传与启动

**Files:**
- Modify local status files under:
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp41_rho_J_confidence_gated_outputs\`
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp42_rho_J_adaptive_B_gated_outputs\`

**Step 1: 固定上传链路**

- `ssh -tt jump`
- 本地 `base64`
- 远端写入 `/tmp/exp41_*.py` 与 `/tmp/exp42_*.py`
- `python3 -m py_compile`
- `nohup python3 ... > run.log 2>&1 < /dev/null &`

**Step 2: 固定本地回执文件**

- `launch_status.txt`
- `post_launch_check.txt`

### Task 9: 统一结果验收

**Files:**
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 只抓取核心产物**

- `summary.json`
- `summary.csv`
- `result.csv`

**Step 2: 统一比较对象**

- `exp41`
- `exp42`
- `exp37`
- `exp39`
- `exp13`
- `fixed`

**Step 3: 固定验收结论**

- 若 `exp41 < exp37`，则 `J` 门控主线成立
- 若 `exp42 < exp39` 且接近或优于 `exp41`，则三元弱补强成立
- 若 `exp42` 明显不如 `exp41`，则保留 `exp41` 为主线，放弃三元串联

### Task 10: 阶段性记录

**Files:**
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 设计完成写一次**

- 记录 `exp41 / exp42` 的目标与结构

**Step 2: 实现完成写一次**

- 记录本地校验通过

**Step 3: 远端启动完成写一次**

- 记录远端目录与进程号

**Step 4: 结果完成写一次**

- 记录是否超过 `exp37`
