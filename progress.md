# 进度日志

## 2026-05-16

- 恢复会话后先核对了 `实验执行清单.md`、`jindu.md`、`气象海洋/shiyan/实验2_经典代理核实验.md`
- 确认实验 2 的误差对比与主结论已落盘
- 确认本次续做重点是补实验 2 的结构性输出，而不是直接进入下一实验
- 通过远程目录核对，确认实验 2 只有 `summary` 和预测结果 CSV，没有现成的权重结构图
- 新建 `气象海洋/shiyan/exp2_structure_analysis.py`，在本地重建实验 2 的权重提取流程
- 生成了 `t=500` 的 4 类核权重热图、典型状态点权重曲线和结构统计摘要
- 已把结构性结论补写回 `气象海洋/shiyan/实验2_经典代理核实验.md` 和 `jindu.md`
- 已为实验 3 新建计划文档 `docs/plans/2026-05-16-实验3量子核结构实验.md`
- 新建 `气象海洋/shiyan/exp3_quantum_kernel_structure.py`，实现小规模量子特征映射核矩阵实验
- 远程确认 `qiskit 2.4.1` 和 `Statevector` 可用，但远程无 `matplotlib`
- 实验 3 已在远程生成 `summary.json`、`summary.md` 和 4 个矩阵 CSV
- 已把实验 3 的核心统计结果和结论写入 `气象海洋/shiyan/实验3_量子核结构实验.md` 与 `jindu.md`
- 新建实验 4 计划文档 `docs/plans/2026-05-16-实验4量子核最小接入验证.md`
- 新建 `气象海洋/shiyan/exp4_quantum_weighted_letkf.py`，实现 `fixed/corr/quantum` 三组最小接入版 LETKF 对照
- 通过 base64 方式将实验 4 脚本上传到远程并运行
- 远程结果表明：`fixed` 最优，`corr` 退化，`quantum` 严重退化
- 已将实验 4 的负结果写入 `气象海洋/shiyan/实验4_量子核接入LETKF最小验证.md` 与 `jindu.md`
- 已为实验 5 新建设计文档 `docs/plans/2026-05-16-实验5量子核混合权重验证-design.md`
- 已为实验 5 新建实现计划 `docs/plans/2026-05-16-实验5量子核混合权重验证.md`
- 新建 `气象海洋/shiyan/exp5_quantum_mixed_weight_letkf.py`，实现 `linear_quantum_mix` 与 `distance_quantum_mix` 两类混合权重方案
- 本地已完成 `exp5_quantum_mixed_weight_letkf.py` 的静态检查，脚本可正常编译
- 首次远程运行实验 5 时，`fixed/corr` 正常，部分混合结果 CSV 已生成，但完整汇总文件未落盘
- 已在局部分析矩阵求逆处加入 `stable_inverse`，用 `jitter + pinv` 兜底修复数值不稳定
- 修复后重新上传并完整重跑实验 5，已拿到全部 `train/test_1` 的 `RMSE/MAE`
- 实验 5 的最终结果表明：最佳方案仍为 `fixed`，`linear_quantum_mix, lambda = 0.1` 仅在训练集上略优，但 `test_1` 仍未超过基线
- 已新建 `气象海洋/shiyan/实验5_量子核混合权重验证.md`，正式记录混合权重实验设置、结果表和结论
- 已将实验 5 的重要信息回写到 `jindu.md`
