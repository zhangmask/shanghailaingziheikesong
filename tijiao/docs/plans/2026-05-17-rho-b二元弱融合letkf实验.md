# rho-B 二元弱融合 LETKF 实验 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 围绕当前最强的 `rho` 主线与次强的 `B` 修正线，实现一条新的二元弱融合实验 `exp36`，验证 `rho + weak_B` 是否能以更低风险逼近或超过现有单线结果。

**Architecture:** 继续复用 `exp13_quantum_localization_letkf.py` 与 `exp17_quantum_B_correction_letkf.py` 已稳定的 Lorenz96 + 局部 LETKF 主骨架、量子相似度构造、结果导出和静默远端运行模式；`exp36` 只做 `rho_q + weak_B_q` 的二元分层融合，不叠加 `R`，不引入自适应规则。

**Tech Stack:** Python 3、NumPy、Qiskit 2.4、Markdown、远端 Ubuntu 运行环境

---

### Task 1: 固定 exp36 的命名和隔离规则

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp36_binary_rho_B_letkf.py`
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 固定远端输出目录**

- `exp36`: `/home/infra/qda_competition/experiments/binary_rho_B_letkf`

**Step 2: 固定实验对照**

- `fixed`
- `corr`
- `binary_rho_b`

**Step 3: 固定隔离规则**

- 不复用已有实验的远端目录
- 启动结果只写本地 `launch_status.txt`
- 不在终端直接回显远端结果内容

### Task 2: 创建 exp36 二元弱融合实验

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp36_binary_rho_B_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp13_quantum_localization_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp17_quantum_B_correction_letkf.py`

**Step 1: 复用基础骨架**

- 复制 `exp13` 的距离先验、状态-观测量子相似度构造
- 复制 `exp17` 的局部背景扰动方向修正逻辑
- 保持经典对角 `R`，不并入结构化 `R`

**Step 2: 写二元分层融合局部分析步**

```python
weights = normalize_weights(
    dist_prior * ((1.0 - lam_rho) + lam_rho * quantum_raw)
)
r_inv = np.diag(weights / obs_var)

pa_tilde = stable_inverse(((nens - 1) / infl) * np.eye(nens) + y_pert @ r_inv @ y_pert.T)
w_mean = pa_tilde @ y_pert @ r_inv @ innovation
w_pert = sym_sqrt((nens - 1) * pa_tilde)

corrected_signal = state_signal + lam_b * coupling * local_mode
x_mean_a = x_mean[i] + corrected_signal @ w_mean
x_pert_a = corrected_signal @ w_pert
```

**Step 3: 固定首轮参数**

- `lam_rho = [0.02, 0.03]`
- `lam_b = [0.003, 0.005]`

**Step 4: 固定首轮组合**

- `(0.02, 0.003)`
- `(0.02, 0.005)`
- `(0.03, 0.003)`
- `(0.03, 0.005)`

**Step 5: 固定融合原则**

- `lam_rho > lam_b`
- `rho` 主导
- `B` 末端弱修正

### Task 3: 输出融合统计

**Files:**
- Modify: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp36_binary_rho_B_letkf.py`

**Step 1: 固定输出字段**

- `lambda_rho`
- `lambda_b`
- `train_avg_b_correction_strength`
- `test_1_avg_b_correction_strength`

**Step 2: 固定 summary 输出**

- `summary.json`
- `summary.csv`
- `result.csv`

### Task 4: 本地检查

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp36_binary_rho_B_letkf.py`

**Step 1: 运行 `py_compile`**

Run:
- `python -m py_compile "d:\Desktop\laingzimuxi\气象海洋\shiyan\exp36_binary_rho_B_letkf.py"`

Expected:
- 退出码 `0`

**Step 2: 检查 diagnostics**

- 确认无新增语法级错误

### Task 5: 静默远端启动

**Files:**
- Modify local status files under:
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp36_binary_rho_B_outputs\`

**Step 1: 固定上传方式**

- 上传到 `/tmp/exp36_binary_rho_B_letkf.py`
- `nohup python3 ... > run.log 2>&1 < /dev/null &`
- 本地只保存 `launch_status.txt`

**Step 2: 固定异常规避**

- 若堡垒机首条命令对 `pkill` 敏感，则首轮启动不把 `pkill` 放在第一条
- 优先采用已验证可行的分块上传方式

### Task 6: 统一结果抓取与验收

**Files:**
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 只抓取三类结果**

- `summary.json`
- `summary.csv`
- `result.csv`

**Step 2: 加入统一排序**

- 与 `exp13`
- `exp17`
- `fixed`
  一起比较

**Step 3: 固定验收指标**

- `test_1 RMSE`
- 是否优于 `fixed`
- 是否优于 `exp17`
- 是否接近或超过 `exp13`
- 是否存在训练改善但测试退化

**Step 4: 每完成一阶段写入 jindu.md**

- 计划完成写一次
- 远端启动完成写一次
- 结果下载完成写一次

### Task 7: 止损规则

**Files:**
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 固定止损标准**

- 若所有组合都不优于 `exp17`，说明当前 `B` 与 `rho` 未形成有效互补
- 若 `lam_b` 略增就退化，回退到更弱 `lam_b`
- 若出现 `NaN` 或病态矩阵，先修数值稳定，不扩大参数范围

**Step 2: 固定可交付标准**

- 至少出现 `1` 条优于 `exp17` 的二元融合组合
- 或形成 `1` 条虽未超 `exp13` 但比三元融合更稳、更清晰的保守主线
