#!/usr/bin/env python3
"""深度读取量子贝叶斯滤波论文"""

import os

try:
    from pypdf import PdfReader
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "pypdf", "-q"])
    from pypdf import PdfReader

papers_dir = "papers"
papers = [
    "arxiv_quantum_state_trajectories_2510.pdf",
    "arxiv_quantum_reduced_filters_2511.pdf",
    "arxiv_quantum_smoothing_2506.pdf",
    "arxiv_quantum_calibration_2507.pdf",
    "arxiv_quantum_amplitude_estimation_2412.pdf",
]

for paper_file in papers:
    paper_path = os.path.join(papers_dir, paper_file)
    if not os.path.exists(paper_path):
        print(f"❌ 文件不存在: {paper_file}")
        continue
    
    print(f"\n{'='*60}")
    print(f"📄 {paper_file}")
    print(f"{'='*60}")
    
    try:
        reader = PdfReader(paper_path)
        print(f"总页数: {len(reader.pages)}")
        
        # 读取摘要（前2页）
        print("\n--- 摘要/引言 ---")
        for i in range(min(3, len(reader.pages))):
            text = reader.pages[i].extract_text()
            # 只保留前1000字符
            text = text[:1500].replace('\n', ' ')
            print(text[:1000])
        
        # 读取核心公式部分（通常在第3-8页）
        if len(reader.pages) > 3:
            print("\n--- 核心公式/方法 ---")
            for i in range(3, min(8, len(reader.pages))):
                text = reader.pages[i].extract_text()
                text = text[:1000].replace('\n', ' ')
                print(f"[第{i+1}页] {text[:800]}")
                
    except Exception as e:
        print(f"❌ 读取错误: {e}")

print("\n\n✅ 读取完成")
