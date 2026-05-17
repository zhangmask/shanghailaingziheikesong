# rho+J 门控与三元弱融合 LETKF 实验 Design

## 目标

当前结果已经明确：

- `exp37 rho + J` 是现阶段最优线，`test_1 RMSE = 0.1269847690`
- `exp39 rho + adaptive_B` 与 `exp38 rho + inflation` 也优于 `exp13`
- `R + B` 只带来弱改善，不适合继续作为主线

因此下一步不再做纯参数扫描，而是做结构优化，回答两个问题：

- `rho + J` 的正收益，是否来自“只在可信局部模式上发力”，而不是固定强度硬修正
- `adaptive_B` 能否作为 `J` 之后的第二层弱补强，在不破坏当前最优主线的前提下继续抬升

## 总体策略

本轮新增两条实验线：

- `exp41_rho_J_confidence_gated_letkf.py`
- `exp42_rho_J_adaptive_B_gated_letkf.py`

统一思路不是扩大搜索空间，而是把“什么时候信量子修正”写进算法结构里。

## 实验一：exp41 rho + J + 置信门控

### 定位

- `rho` 继续作为主入口，控制局部观测参与
- `J` 继续只做末端几何修正
- 新增 `j_confidence`，把弱耦合和弱信号位置自动压小

### 现有问题

`exp37` 当前做法本质上是：

1. 用 `rho` 权重做分析
2. 构造 `j_mode`
3. 直接用 `lam_j * j_mode` 修正状态扰动方向

这条线虽然已经有效，但还存在一个结构缺口：

- `J` 修正只取决于固定 `lam_j`
- 没有显式判断当前位置的几何模式是否可信
- 弱耦合区和强耦合区被同样处理

### 结构优化

新增：

- `coupling_strength`
- `quantum_focus`
- `innovation_strength`
- `j_confidence`

建议定义思路：

- `coupling_strength`：`state_signal` 与 `local_mode` 的归一化耦合强度
- `quantum_focus`：量子权重的集中度，集中则更可信
- `innovation_strength`：当前创新的相对强度，过弱时不应强修正
- `j_confidence`：上面三者的保守组合，并裁剪到小范围

最终形式：

```python
corrected = state_signal + lam_j * j_confidence * j_mode
```

### 预期收益

- 保留 `exp37` 当前的主收益来源
- 减少弱信号区的误修正
- 提高 train/test 同步改善的稳定性

## 实验二：exp42 rho + J + adaptive_B + 双门控

### 定位

- `rho` 继续负责观测参与
- `J` 负责几何方向增强
- `adaptive_B` 作为 `J` 之后的第二层最弱补偿

### 现有问题

`exp39` 当前已经优于 `exp13`，但还不够“结构自适应”：

- `lambda_b_i` 只看 `quantum_signal + innovation_signal`
- 没有判断 `local_mode` 与 `state_signal` 是否真的同向
- 没有显式惩罚集合过散位置
- 外层 `lambda_b` 现在基本是空参数，不构成真正的控制量

### 结构优化

新增：

- `alignment`
- `spread_penalty`
- `b_confidence`

建议定义思路：

- `alignment`：状态扰动和局部修正方向的一致性
- `spread_penalty`：集合过散时减弱修正
- `b_confidence`：结合 `alignment`、`quantum_signal`、`innovation_signal`、`spread_penalty` 的保守门控

并按以下顺序作用：

1. `rho` 权重分析
2. `J` 门控修正
3. `adaptive_B` 门控补偿

最终形式：

```python
j_corrected = state_signal + lam_j * j_confidence * j_mode
final_corrected = j_corrected + lam_b_i * b_confidence * b_mode
```

### 预期收益

- 不让 `J` 与 `B` 无条件叠加
- 让 `B` 只在 `J` 后仍存在稳定残差信号时参与
- 验证两个正信号是否能做保守互补

## 统一原则

- 不改 `exp37-40` 已有脚本
- 新增独立脚本，避免污染已跑完结果
- 继续保留 `fixed / corr` 对照
- 继续使用小强度弱融合，不做激进接入
- 不做大范围参数扫描，首轮只给极小组合保证结构验真

## 首轮参数原则

### exp41

- 围绕当前最优 `exp37` 附近，只保留极小固定组合
- 重点看门控前后是否带来稳定提升，而不是做密集扫描

### exp42

- `rho` 与 `J` 只保留小强度
- `adaptive_B` 不再额外做外层扫描
- 重点验证“双门控串联”是否优于单独 `exp37` 或 `exp39`

## 验收标准

- `exp41` 是否低于当前最优 `0.1269847690`
- `exp42` 是否至少优于 `exp39`
- 若 `exp42` 未超过 `exp41`，但稳定优于 `exp39`，仍视为有效补强结构
- 若任一新线训练改善而测试退化，则视为门控设计不足

## 风险与止损

- 若门控写得过强，可能把有效修正过度抑制，退回接近 `fixed`
- 若门控写得过弱，本质上就退化回已有 `exp37/39`
- 若三元串联过多耦合，可能重新引入多对象叠加退化

止损原则：

- 保持 `rho` 主导地位不变
- 保持 `J` 与 `B` 都是末端弱修正
- 一旦 `exp42` 整体不如 `exp41`，优先保留 `exp41` 主线

## 一句话结论

这轮不再靠扫参找偶然最优，  
而是：

> 用“门控置信度”把 `rho + J` 做稳，再用“双门控串联”验证 `adaptive_B` 是否能成为 `J` 后的第二层弱补强。
