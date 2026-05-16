#!/usr/bin/env python3
"""深度读取量子贝叶斯滤波论文 - 提取核心公式和思想 v5"""

import os

try:
    from pypdf import PdfReader
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "pypdf", "-q"])
    from pypdf import PdfReader

papers_dir = "papers"
papers = [
    ("arxiv_quantum_calibration_2507.pdf", "量子设备校准"),
    ("arxiv_quantum_amplitude_estimation_2412.pdf", "贝叶斯量子幅度估计"),
    ("arxiv_quantum_bayesian_filter_2025.pdf", "量子贝叶斯滤波"),
]

for paper_file, chinese_name in papers:
    paper_path = os.path.join(papers_dir, paper_file)
    if not os.path.exists(paper_path):
        print(f"❌ 文件不存在: {paper_file}")
        continue
    
    print(f"\n{'='*80}")
    print(f"📄 {chinese_name} ({paper_file})")
    print(f"{'='*80}")
    
    reader = PdfReader(paper_path)
    full_text = ""
    for i in range(len(reader.pages)):
        text = reader.pages[i].extract_text()
        full_text += text + "\n"
    
    # 提取引言部分 - 了解作者的问题意识
    print("\n--- 作者的问题意识（引言）---")
    intro_found = False
    for line in full_text.split('\n'):
        line = line.strip()
        if any(kw in line.lower() for kw in ['we propose', 'we introduce', 'we present', 'in this work', 'this paper']):
            print(f"  ★ {line[:300]}")
            intro_found = True
        if intro_found and any(kw in line.lower() for kw in ['method', 'results', 'section']):
            break
    
    # 提取核心公式 - 逐页扫描
    print("\n--- 核心公式（逐页提取）---")
    for i in range(min(15, len(reader.pages))):
        text = reader.pages[i].extract_text()
        # 查找包含数学符号的段落
        for line in text.split('\n'):
            line = line.strip()
            if any(s in line for s in ['dρ', '∂ρ', 'Tr(', '⟨', '⟩', '†', 'H[', 'D[', 'E[', 'M(',
                                       'Bayes', 'posterior', 'likelihood', 'prior', 'smoothing',
                                       'filtering', 'trajectory', 'master equation', 'SMC',
                                       'particle', 'ensemble', 'Kalman', 'covariance']):
                if len(line) > 20 and len(line) < 400:
                    print(f"  [P{i+1}] {line[:350]}")

print("\n\n✅ 深度读取完成")
