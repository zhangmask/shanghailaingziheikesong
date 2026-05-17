# rho-R 联合自适应三线 LETKF 实验 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 围绕当前最有效的两条公式主线 `rho` 与 `R`，实现三条深化实验 `exp32-34`，验证联合接入与局部自适应强度是否优于现有单线结果。

**Architecture:** 继续复用 `exp10_quantum_structured_R_letkf.py` 与 `exp13_quantum_localization_letkf.py` 已稳定的 Lorenz96 + 局部 LETKF 主骨架、量子相似度构造、结果导出和静默远端运行模式；`exp32` 只做 `rho_q + R_q` 联合，`exp33` 只把 `exp13` 的固定 `lambda` 改成局部自适应，`exp34` 只把 `exp10` 的固定 `lambda` 改成局部自适应，不混入第三个公式对象。

**Tech Stack:** Python 3、NumPy、Qiskit 2.4、Markdown、远端 Ubuntu 运行环境

---

### Task 1: 固定 exp32-34 的命名和隔离规则

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp32_joint_quantum_rho_R_letkf.py`
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp33_adaptive_lambda_localization_letkf.py`
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp34_adaptive_lambda_structured_R_letkf.py`
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 固定远端输出目录**

- `exp32`: `/home/infra/qda_competition/experiments/joint_quantum_rho_R_letkf`
- `exp33`: `/home/infra/qda_competition/experiments/adaptive_lambda_localization_letkf`
- `exp34`: `/home/infra/qda_competition/experiments/adaptive_lambda_structured_R_letkf`

**Step 2: 固定实验对照**

- `fixed`
- `corr`
- `exp32`: `joint_quantum_rho_r`
- `exp33`: `adaptive_quantum_localization`
- `exp34`: `adaptive_structured_r`

**Step 3: 固定隔离规则**

- 不复用已有实验的远端目录
- 只对当前实验脚本执行 `pkill -f`
- 启动结果只写本地 `launch_status.txt`
- 不在终端回显远端结果内容

### Task 2: 创建 exp32 联合 rho + R 实验

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp32_joint_quantum_rho_R_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp10_quantum_structured_R_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp13_quantum_localization_letkf.py`

**Step 1: 复用基础骨架**

- 复制 `exp13` 的局部窗口、距离先验、量子相似度构造
- 复制 `exp10` 的结构化 `R` 投影与 SPD 修正

**Step 2: 写联合局部分析步**

```python
weights = normalize_weights((1.0 - lam_rho) * dist_prior + lam_rho * dist_prior * quantum_raw)
r_scale = np.diag(weights)
structured_r = obs_var * ((1.0 - lam_r) * np.eye(m) + lam_r * corr_q)
structured_r = r_scale @ structured_r @ r_scale
r_inv = stable_inverse(structured_r + 1e-6 * obs_var * np.eye(m))
```

**Step 3: 固定首轮参数**

- `lam_rho = [0.02, 0.05]`
- `lam_r = [0.02, 0.05]`
- 不扩到 `0.10`

**Step 4: 固定第一轮验收目标**

- 是否超过 `exp10` 或 `exp13`
- 是否比单线更稳

### Task 3: 创建 exp33 局地化自适应 lambda 实验

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp33_adaptive_lambda_localization_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp13_quantum_localization_letkf.py`

**Step 1: 固定局部自适应信号**

- `quantum_signal = mean(quantum_raw)`
- `innovation_signal = tanh(mean(abs(innovation)) / (OBS_STD + EPS))`
- `spread_signal = tanh(mean(std(y_pert)) / (OBS_STD + EPS))`

**Step 2: 写最小自适应规则**

```python
def compute_local_lambda(quantum_signal, innovation_signal, spread_signal):
    lam = 0.015 + 0.03 * quantum_signal + 0.02 * innovation_signal - 0.015 * spread_signal
    return float(np.clip(lam, 0.01, 0.08))
```

**Step 3: 接入局地化权重**

```python
lam_i = compute_local_lambda(quantum_signal, innovation_signal, spread_signal)
weights = normalize_weights(dist_prior * ((1.0 - lam_i) + lam_i * quantum_raw))
```

**Step 4: 固定首轮限制**

- 只做一套自适应规则
- 不再额外扫 `lambda`
- 输出平均 `lambda_i` 统计

### Task 4: 创建 exp34 结构化 R 自适应 lambda 实验

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp34_adaptive_lambda_structured_R_letkf.py`
- Reference: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp10_quantum_structured_R_letkf.py`

**Step 1: 固定局部一致性信号**

- `corr_strength = mean(abs(corr_q - I))`
- `quantum_consistency = mean(corr_q)`
- 可选记录 `innovation_signal`

**Step 2: 写最小自适应规则**

```python
def compute_r_lambda(corr_strength, quantum_consistency):
    lam = 0.015 + 0.03 * corr_strength + 0.02 * quantum_consistency
    return float(np.clip(lam, 0.01, 0.08))
```

**Step 3: 接入结构化 R**

```python
lam_i = compute_r_lambda(corr_strength, quantum_consistency)
structured_r = obs_var * ((1.0 - lam_i) * np.eye(m) + lam_i * corr_q)
structured_r = 0.5 * (structured_r + structured_r.T) + 1e-6 * obs_var * np.eye(m)
```

**Step 4: 固定首轮限制**

- 保持 `exp10` 的 SPD 投影
- 只做一套自适应规则
- 输出平均 `lam_i` 和窗口统计

### Task 5: 本地检查

**Files:**
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp32_joint_quantum_rho_R_letkf.py`
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp33_adaptive_lambda_localization_letkf.py`
- Create: `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp34_adaptive_lambda_structured_R_letkf.py`

**Step 1: 逐条运行 `py_compile`**

Run:
- `python -m py_compile "d:\Desktop\laingzimuxi\气象海洋\shiyan\exp32_joint_quantum_rho_R_letkf.py"`
- `python -m py_compile "d:\Desktop\laingzimuxi\气象海洋\shiyan\exp33_adaptive_lambda_localization_letkf.py"`
- `python -m py_compile "d:\Desktop\laingzimuxi\气象海洋\shiyan\exp34_adaptive_lambda_structured_R_letkf.py"`

Expected:
- 三条都退出码 `0`

**Step 2: 检查 diagnostics**

- 确认无新增语法级错误

### Task 6: 静默远端启动

**Files:**
- Modify local status files under:
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp32_joint_quantum_rho_R_outputs\`
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp33_adaptive_lambda_localization_outputs\`
  - `d:\Desktop\laingzimuxi\气象海洋\shiyan\exp34_adaptive_lambda_structured_R_outputs\`

**Step 1: 按顺序启动**

- 先 `exp32`
- 再 `exp33`
- 最后 `exp34`

**Step 2: 固定上传方式**

- 上传到 `/tmp/<script>.py`
- `nohup python3 ... > run.log 2>&1 < /dev/null &`
- 本地只保存 `launch_status.txt`

### Task 7: 统一结果抓取与验收

**Files:**
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 只抓取三类结果**

- `summary.json`
- `summary.csv`
- `result.csv`

**Step 2: 加入统一排序**

- 与 `exp10`
- `exp13`
- `exp14`
- `exp11`
  一起比较

**Step 3: 固定验收指标**

- `test_1 RMSE`
- 是否优于 `fixed`
- 是否优于单线 `exp10` 或 `exp13`
- 是否存在训练改善但测试退化

**Step 4: 每完成一阶段写入 jindu.md**

- 计划完成写一次
- 远端启动完成写一次
- 结果下载完成写一次

### Task 8: 止损规则

**Files:**
- Modify: `d:\Desktop\laingzimuxi\jindu.md`

**Step 1: 固定止损标准**

- 若 `exp32` 全部组合都明显差于 `exp10/13`，判定“当前 `rho` 与 `R` 不宜直接联用”
- 若 `exp33/34` 自适应规则普遍差于固定小 `lambda`，回退到更保守公式
- 若出现 `NaN` 或矩阵病态，先修数值稳定，不扩大参数范围

**Step 2: 固定可交付标准**

- 至少出现 `1` 条优于当前单线最优的实验
- 或形成 `1` 条虽未超最优但解释更完整、可继续深化的主线
