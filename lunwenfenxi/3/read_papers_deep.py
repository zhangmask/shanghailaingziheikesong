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

for paper_file, chinese_name in papers:
    paper_path = os.path.join(papers_dir, paper_file)
    if not os.path.exists(paper_path):
        print(f"❌ 文件不存在: {paper_file}")
        continue
    
    print(f"\n{'='*80}")
    print(f"📄 {chinese_name} ({paper_file})")
    print(f"{'='*80}")
    
    try:
        reader = PdfReader(paper_path)
        print(f"总页数: {len(reader.pages)}")
        
        # 读取全文，提取关键公式和概念
        full_text = ""
        for i in range(len(reader.pages)):
            text = reader.pages[i].extract_text()
            full_text += text + "\n"
        
        # 提取公式相关段落
        print("\n--- 核心公式 ---")
        lines = full_text.split('\n')
        formula_lines = []
        for line in lines:
            # 查找包含数学符号的行
            if any(s in line for s in ['ρ', '∂', '∫', '∑', '∏', '∈', '∀', '∃', '→', '⇒', '≈', '≠', '≤', '≥', 
                                       'Tr', 'H[', 'D[', 'E[', 'M(', '⟨', '⟩', '†', '∞', '∇', 'Δ', '∂',
                                       'dρ', 'dt', 'dW', 'L(', 'H(', 'c)', 'H', 'SME', 'master equation']):
                formula_lines.append(line.strip())
        
        # 去重并打印
        seen = set()
        for line in formula_lines:
            if line and line not in seen and len(line) > 10:
                seen.add(line)
                print(f"  {line[:200]}")
        
        # 提取关键概念
        print("\n--- 关键概念 ---")
        concepts = ['filtering', 'smoothing', 'trajectory', 'master equation', 'Lindblad', 
                    'measurement', 'Bayesian', 'ensemble', 'Kalman', 'covariance',
                    'localization', 'reduced-order', 'projection', 'quantum']
        for concept in concepts:
            count = full_text.lower().count(concept.lower())
            if count > 0:
                print(f"  {concept}: 出现 {count} 次")
                
    except Exception as e:
        print(f"❌ 读取错误: {e}")

print("\n\n✅ 读取完成")
