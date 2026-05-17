# rho-R 联合自适应三线 LETKF 实验 Design

## 目标

在现有公式层实验中，`exp13` 的量子局地化 `rho_q` 与 `exp10` 的结构化观测误差 `R_q` 已经分别给出正信号。  
这轮设计的目标不是继续横向扩展新的公式对象，而是沿着这两条最有效的主线继续深化，验证：

- 单独有效的 `rho_q` 与 `R_q` 能否联合后进一步提升
- 固定小 `lambda` 能否升级为局部自适应 `lambda_i`
- 量子结构信号是否更适合做“弱结构控制”，而不是做全局强控制

## 背景

- `exp13` 当前最强，说明量子结构最适合先进入“哪些观测应该参与”的局地化层。
- `exp10` 次强，说明量子结构也适合进入“参与后如何解释观测误差”的结构化 `R` 层。
- `exp11` 接近但未超，`exp14` 轻微退化，说明量子信号一旦进入更深层或更强的控制对象，数值敏感性明显上升。

这说明当前阶段最合理的问题不是“还有没有更多公式对象能改”，而是：

> 能否把已经证明有效的两个对象 `rho` 与 `R` 联合起来，并把固定混合强度改成更合理的局部自适应规则。

## 核心判断

这轮最值得推进的是三条线：

- `exp32_joint_quantum_rho_R_letkf.py`
- `exp33_adaptive_lambda_localization_letkf.py`
- `exp34_adaptive_lambda_structured_R_letkf.py`

不建议当前优先继续横向铺开 `S / T / K / H / J / inflation` 的新变体，因为现有结果已经表明，这些位置要么更敏感，要么尚未给出比 `rho / R` 更强的证据。

## 总体架构

继续复用现有稳定骨架：

- `Lorenz96 + RK4`
- 局部 `LETKF` 分析更新
- `stable_inverse`
- `sym_sqrt`
- 量子窗口特征映射与相似度构造
- `summary.json / summary.csv / result.csv`

本轮只新增三条实验脚本，不拆公共库，不改数据接口。

## 三条实验的职责

### exp32：联合 rho + R

#### 脚本

`exp32_joint_quantum_rho_R_letkf.py`

#### 目标

把 `exp13` 的局地化优势与 `exp10` 的结构化 `R` 优势合并起来，验证两种正信号是否互补。

#### 接入方式

- `rho_q` 负责“局部观测参与结构”
- `R_q` 负责“局部观测误差耦合结构”

最小公式形式：

```python
weights = normalize_weights((1.0 - lam_rho) * dist_prior + lam_rho * dist_prior * quantum_raw)
structured_r = obs_var * ((1.0 - lam_R) * np.eye(m) + lam_R * corr_q)
```

#### 设计原则

- 不额外引入第三个公式对象
- 首轮只扫小范围组合
- 优先验证“联合是否优于单条最佳线”

### exp33：局地化自适应 lambda

#### 脚本

`exp33_adaptive_lambda_localization_letkf.py`

#### 目标

把 `exp13` 中固定小 `lambda` 升级成局部自适应 `lambda_i`，让量子局地化强度由局部结构自己决定。

#### 接入方式

由局部三个量构造 `lambda_i`：

- `quantum_signal`
- `innovation_signal`
- `spread_signal`

最小公式形式：

```python
lambda_i = clip(
    base + a * quantum_signal + b * innovation_signal - c * spread_signal,
    0.01, 0.08,
)
```

#### 设计原则

- 仍保持距离先验为主
- 量子只负责调节参与强度
- 上界保持保守，避免重蹈 `lambda=0.1` 退化的覆辙

### exp34：结构化 R 自适应 lambda

#### 脚本

`exp34_adaptive_lambda_structured_R_letkf.py`

#### 目标

把 `exp10` 中固定 `lambda` 的结构化 `R` 改成局部自适应 `lambda_i`，只在结构稳定的窗口中增强量子相关。

#### 接入方式

用局部结构一致性信号控制 `lambda_i`：

- `corr_strength`
- `quantum_consistency`
- 可选的 innovation 稳定指标

最小公式形式：

```python
lambda_i = clip(
    base + a * corr_strength + b * quantum_consistency,
    0.01, 0.08,
)
structured_r = obs_var * ((1.0 - lambda_i) * np.eye(m) + lambda_i * corr_q)
```

#### 设计原则

- 保留 `R_q` 的 SPD 投影和 `jitter`
- 不把自适应强度放大到激进区间
- 先做最小单规则，不叠加多套评分器

## 数据流

### exp32

1. 构造局部观测集合
2. 生成距离先验与量子相似度
3. 计算局地化权重 `weights`
4. 构造局部结构化 `R_q`
5. 在同一局部分析步中同时使用 `weights` 与 `R_q`

### exp33

1. 构造局部量子相似度
2. 从量子强度、innovation、spread 估计 `lambda_i`
3. 用 `lambda_i` 调节局地化权重
4. 其余分析步保持经典

### exp34

1. 构造局部观测相似度矩阵
2. 从结构一致性信号估计 `lambda_i`
3. 用 `lambda_i` 生成结构化 `R_q`
4. 其余分析步保持经典

## 实验顺序

### 第一阶段

- 先做 `exp32`
- 目标：验证联合线是否值得继续

### 第二阶段

- 再做 `exp33`
- 目标：验证 `exp13` 的固定最优点能否提升成局部自适应

### 第三阶段

- 最后做 `exp34`
- 目标：验证 `exp10` 的正信号能否变得更稳、更广泛

## 通过标准

- `exp32` 至少接近或超过 `exp13`
- `exp33` 至少在不失稳前提下接近 `exp13` 固定最优点
- `exp34` 至少不明显差于 `exp10` 固定最优点

## 止损条件

- 若 `exp32` 全部组合都明显差于 `exp13` 与 `exp10`，说明当前 `rho` 与 `R` 不能简单联用
- 若 `exp33/34` 的自适应版本普遍差于固定小 `lambda`，说明当前自适应规则过于激进，应先回到更保守公式
- 若出现 `NaN` 或矩阵病态，优先修数值稳定，不扩扫描

## 一句话结论

这轮设计的核心不是继续横向找新对象，而是：

> 围绕已经证明有效的 `rho` 与 `R` 两条主线，做联合化与自适应化，把“量子结构是弱结构信号”这件事推进成更完整的公式实验链。
