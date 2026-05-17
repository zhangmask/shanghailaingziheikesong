# rho-B 二元弱融合 LETKF 实验 Design

## 目标

当前已验证的正增益板块中：

- `exp13` 的量子局地化 `rho_q` 最强
- `exp17` 的背景扰动修正 `B_q` 次强

这轮设计的目标不是继续叠加第三个对象，而是先做一条更保守的二元融合线，验证：

- `rho_q` 主导时，`weak_B_q` 能否在不破坏稳定性的前提下带来额外增益
- `B_q` 是否更适合作为 `rho` 主线后的末端弱修正，而不是独立主线
- 二元弱融合是否比当前三元融合更容易兼顾稳定性与提升

## 背景

- `exp13` 已经证明：量子结构最适合优先进入“哪些观测应该参与”的局地化层。
- `exp17` 已经证明：量子结构对局部背景扰动方向有修正价值，但强度不宜过大。
- `exp10` 虽然也有提升，但当前 `exp34` 刚验证出自适应 `R` 的增益还比较弱，说明 `R` 这条线短期内不一定要继续叠加到所有新方案中。

这说明当前阶段最合理的新问题是：

> 如果暂时拿掉 `R`，只保留最强的 `rho` 和次强的 `weak_B`，能否形成一条更轻、更稳的二元融合线。

## 核心判断

当前最值得新增的是：

- `exp36_binary_rho_B_letkf.py`

不建议这一步同时叠加：

- `R`
- 自适应 `lambda`
- 第四个公式对象

第一轮只回答一个更基础的问题：

> `rho + weak_B` 的最小二元弱融合，是否至少优于 `exp17`，并尽量逼近 `exp13`。

## 总体架构

继续复用现有稳定骨架：

- `Lorenz96 + RK4`
- 局部 `LETKF`
- `stable_inverse`
- `sym_sqrt`
- 量子窗口特征映射与相似度构造
- `summary.json / summary.csv / result.csv`

本轮只新增一条实验脚本，不拆公共库，不改数据接口。

## 板块分工

### rho_q：主入口

- 负责“局部观测参与结构”
- 继续沿用 `exp13` 的距离先验主导方案
- 保留量子信号为弱调制

最小形式：

```python
weights = normalize_weights(
    dist_prior * ((1.0 - lam_rho) + lam_rho * quantum_raw)
)
```

### weak_B_q：末端弱修正

- 负责“局部背景扰动方向修正”
- 沿用 `exp17` 的局部模式构造逻辑
- 只在分析权重已计算完成后，对 `state_signal` 做小幅修正

最小形式：

```python
corrected_signal = state_signal + lam_b * coupling * local_mode
x_mean_a = x_mean[i] + corrected_signal @ w_mean
x_pert_a = corrected_signal @ w_pert
```

## 融合顺序

二元融合采用固定主次顺序：

1. 先用 `rho_q` 形成局部观测参与权重
2. 再用经典 LETKF 结构计算 `w_mean / w_pert`
3. 最后用 `weak_B_q` 修正局部背景扰动方向

对应原则：

- `lam_rho > lam_b`
- `rho` 主导
- `B` 只做末端弱修正

## 最小公式链

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

## 参数原则

第一轮只扫非常保守的小范围：

- `lam_rho = [0.02, 0.03]`
- `lam_b = [0.003, 0.005]`

建议首轮只做 4 组：

- `(0.02, 0.003)`
- `(0.02, 0.005)`
- `(0.03, 0.003)`
- `(0.03, 0.005)`

约束原则：

- 不扩到 `0.01` 以上的 `lam_b`
- 不让 `lam_b` 接近 `lam_rho`
- 不引入第二层自适应

## 数据流

1. 构造局部观测集合
2. 生成距离先验与状态-观测量子相似度 `quantum_raw`
3. 用 `rho_q` 得到局地化权重 `weights`
4. 用经典 LETKF 结构得到 `w_mean / w_pert`
5. 用 `weak_B_q` 修正局部状态扰动方向
6. 输出 `summary.json / summary.csv / result.csv`

## 验收标准

- 至少优于 `exp17`
- 若接近 `exp13`，说明二元弱融合值得继续深化
- 若明显优于 `exp17` 且比三元融合更稳，说明 `rho+B` 可能比 `rho+R+B` 更适合作为短期主线

## 止损条件

- 若所有组合都差于 `exp13` 且不优于 `exp17`，说明 `B_q` 当前加入 `rho` 主线没有形成互补
- 若 `lam_b` 略增就普遍退化，说明 `B_q` 只能保持极弱接入
- 若训练误差明显恶化而测试不增益，说明该修正更像噪声放大而非有效结构信号

## 一句话结论

这轮设计的核心不是继续加对象，  
而是：

> 先拿最强的 `rho_q` 和次强的 `weak_B_q` 组成一条更轻的二元弱融合线，验证“少即是多”的保守融合是否比三元方案更稳。
