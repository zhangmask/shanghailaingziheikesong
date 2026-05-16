#!/usr/bin/env python3
"""深度读取量子贝叶斯滤波论文 - 提取核心公式和思想"""

import os

try:
    from pypdf import PdfReader
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "pypdf", "-q"])
    from pypdf import PdfReader

papers_dir = "papers"
papers = [
    ("arxiv_quantum_state_trajectories_2510.pdf", "量子态轨迹估计"),
    ("arxiv_quantum_reduced_filters_2511.pdf", "量子系统降阶滤波"),
    ("arxiv_quantum_smoothing_2506.pdf", "量子态平滑"),
    ("arxiv_quantum_calibration_2507.pdf", "量子设备校准"),
    ("arxiv_quantum_amplitude_estimation_2412.pdf", "贝叶斯量子幅度估计"),
]

output_lines = []

for paper_file, chinese_name in papers:
    paper_path = os.path.join(papers_dir, paper_file)
    if not os.path.exists(paper_path):
        continue
    
    print(f"\n{'='*80}")
    print(f"📄 {chinese_name} ({paper_file})")
    print(f"{'='*80}")
    
    reader = PdfReader(paper_path)
    full_text = ""
    for i in range(len(reader.pages)):
        text = reader.pages[i].extract_text()
        full_text += text + "\n"
    
    # 提取引言/摘要部分
    print("\n--- 引言/摘要 ---")
    intro_lines = []
    in_intro = False
    for line in full_text.split('\n'):
        line = line.strip()
        if any(kw in line.lower() for kw in ['abstract', 'introduction', '摘要', '引言']):
            in_intro = True
            continue
        if in_intro:
            if any(kw in line.lower() for kw in ['method', 'approach', 'results', 'conclusion', '结论', '方法']):
                break
            if line and len(line) > 20:
                intro_lines.append(line)
                print(f"  {line[:200]}")
    
    # 提取核心公式
    print("\n--- 核心公式 ---")
    formula_lines = []
    for line in full_text.split('\n'):
        line = line.strip()
        if any(s in line for s in ['ρ', '∂', '∫', '∑', '∏', '∈', '∀', '∃', '→', '⇒', '≈', '≠', '≤', '≥', 
                                   'Tr', 'H[', 'D[', 'E[', 'M(', '⟨', '⟩', '†', '∞', '∇', 'Δ',
                                   'dρ', 'dt', 'dW', 'L(', 'H(', 'c)', 'master equation', 'SME',
                                   'Bayes', 'likelihood', 'posterior', 'prior']):
            if len(line) > 15 and len(line) < 500:
                formula_lines.append(line)
    
    seen = set()
    for line in formula_lines:
        if line not in seen:
            seen.add(line)
            print(f"  {line[:300]}")
    
    # 提取关键概念
    print("\n--- 关键概念 ---")
    concepts = [
        ('filtering', '滤波'),
        ('smoothing', '平滑'),
        ('trajectory', '轨迹'),
        ('master equation', '主方程'),
        ('Lindblad', 'Lindblad'),
        ('measurement', '测量'),
        ('Bayesian', '贝叶斯'),
        ('ensemble', '集合/系综'),
        ('Kalman', '卡尔曼'),
        ('covariance', '协方差'),
        ('localization', '局部化'),
        ('reduced-order', '降阶'),
        ('projection', '投影'),
        ('quantum', '量子'),
        ('density matrix', '密度矩阵'),
        ('state estimation', '状态估计'),
    ]
    for eng, chn in concepts:
        count = full_text.lower().count(eng.lower())
        if count > 0:
            print(f"  {chn} ({eng}): 出现 {count} 次")

print("\n\n✅ 读取完成")
