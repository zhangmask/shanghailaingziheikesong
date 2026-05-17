# rho-R-B 三元弱融合 LETKF 实验 Design

## 目标

当前已下载结果里，真正对 `fixed` 基线给出稳定正增益的量子板块有三条：

- `exp13` 的量子局地化 `rho_q`
- `exp10` 的结构化观测误差 `R_q`
- `exp17` 的背景扰动修正 `B_q`

这轮设计的目标不是再横向增加新公式对象，而是把这三条已经出现正信号的板块做一次有主次的弱融合，验证：

- `rho_q` 作为主入口时，`R_q` 与 `B_q` 能否提供额外增益
- 多个正信号板块能否在“小强度、分层次”的前提下兼容
- 当前量子结构更适合形成“主-次-弱”分层控制，而不是多对象同权叠加

## 背景

- `exp13` 当前最强，说明量子结构最适合优先进入“哪些观测应该参与”的局地化层。
- `exp10` 次强，说明量子结构也可以进入“观测误差如何耦合”的结构化 `R` 层，但强度不能太大。
- `exp17` 也优于 `fixed`，说明量子结构对局部背景扰动方向有补偿价值，但更像弱修正项，而不是主骨架。

这说明当前阶段最合理的问题已经从：

> 哪个单一对象最值得接入

转向：

> 能否把三个已验证有效的板块组织成 `rho` 主导、`R` 次级、`B` 弱修正的分层融合结构。

## 核心判断

当前最值得新增的是一条主融合实验：

- `exp35_triply_fused_rho_R_B_letkf.py`

不建议这一步同时再加自适应、多评分器或额外新对象。  
第一轮先回答一个更基础的问题：

> `rho + R + weak_B` 在保守小强度下，是否至少接近或超过当前单线最优 `exp13`。

## 总体架构

继续复用现有稳定骨架：

- `Lorenz96 + RK4`
- 局部 `LETKF` 分析更新
- `stable_inverse`
- `sym_sqrt`
- 量子窗口特征映射与相似度构造
- `summary.json / summary.csv / result.csv`

本轮只新增一条实验脚本，不拆公共库，不改数据接口。

## 板块分工

### rho_q：主入口

- 负责“局部观测参与结构”
- 继续保留距离先验为主
- 量子只做轻量调节

最小形式：

```python
weights = normalize_weights(
    dist_prior * ((1.0 - lam_rho) + lam_rho * quantum_raw)
)
```

### R_q：次级结构控制

- 负责“局部观测误差耦合结构”
- 使用局部观测窗口量子相似度构造 `corr_q`
- 保留 SPD 投影与 `jitter`

最小形式：

```python
structured_r = obs_var * ((1.0 - lam_r) * np.eye(m) + lam_r * corr_q)
structured_r = 0.5 * (structured_r + structured_r.T) + 1e-6 * obs_var * np.eye(m)
```

### weak_B：弱背景修正

- 负责“局部背景扰动方向修正”
- 不直接替换 LETKF 骨架
- 只在已有分析权重计算完成后，用小系数修正局部状态扰动方向

最小形式：

```python
corrected_signal = state_signal + lam_b * coupling * local_mode
```

## 融合顺序

三元融合不采用同权并入，而采用固定主次顺序：

1. 先用 `rho_q` 形成局部观测参与权重
2. 再用 `R_q` 形成局部结构化观测误差
3. 最后用 `weak_B` 对局部背景扰动方向做弱修正

对应原则：

- `lam_rho > lam_r > lam_b`
- `rho` 主导
- `R` 次级
- `B` 最弱

## 最小公式链

```python
weights = normalize_weights(
    dist_prior * ((1.0 - lam_rho) + lam_rho * quantum_raw)
)

r_scale = np.diag(weights)
structured_r = obs_var * ((1.0 - lam_r) * np.eye(m) + lam_r * corr_q)
structured_r = r_scale @ structured_r @ r_scale
structured_r = 0.5 * (structured_r + structured_r.T) + 1e-6 * obs_var * np.eye(m)
r_inv = stable_inverse(structured_r)

pa_tilde = stable_inverse(((nens - 1) / infl) * np.eye(nens) + y_pert @ r_inv @ y_pert.T)
w_mean = pa_tilde @ y_pert @ r_inv @ innovation
w_pert = sym_sqrt((nens - 1) * pa_tilde)

corrected_signal = state_signal + lam_b * coupling * local_mode
x_mean_a = x_mean[i] + corrected_signal @ w_mean
x_pert_a = corrected_signal @ w_pert
```

## 参数原则

第一轮只扫保守小范围：

- `lam_rho = [0.02, 0.03]`
- `lam_r = [0.01, 0.02]`
- `lam_b = [0.005, 0.01]`

约束原则：

- 不扩到 `0.05` 以上的 `lam_b`
- 不让 `lam_r` 与 `lam_rho` 同量级放大
- 不做全量网格爆炸扫描，只做少量组合

## 数据流

1. 构造局部观测集合
2. 生成距离先验与状态-观测量子相似度 `quantum_raw`
3. 生成观测-观测量子相似度 `corr_q`
4. 用 `rho_q` 得到局地化权重 `weights`
5. 用 `R_q` 得到结构化 `structured_r`
6. 用 `structured_r` 计算分析权重 `w_mean / w_pert`
7. 用 `weak_B` 修正局部状态扰动方向
8. 输出 `summary.json / summary.csv / result.csv`

## 验收标准

- 至少接近 `exp13`
- 若能超过 `exp13`，则说明三元分层融合成立
- 即使未超过 `exp13`，若稳定优于 `exp10` 与 `exp17`，也说明融合结构有继续深化价值

## 止损条件

- 若大多数组合都差于 `exp13`，说明 `R` 与 `B` 叠加后破坏了当前最强局地化主线
- 若只要加入 `lam_b` 就普遍退化，说明 `B_q` 暂时不适合并入主融合链
- 若出现 `NaN`、病态矩阵或显著放大训练误差，优先回退 `lam_r` 与 `lam_b`

## 一句话结论

这轮设计的核心不是把所有量子板块一起塞进 LETKF，  
而是：

> 以 `rho_q` 为主入口、`R_q` 为次级结构、`B_q` 为弱修正，验证三元弱融合是否能把多个小正信号整合成更强主线。
