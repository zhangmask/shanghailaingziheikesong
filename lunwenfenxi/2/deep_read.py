#!/usr/bin/env python3
"""
深度阅读论文本质公式和理论框架
"""

from pypdf import PdfReader
import os

PAPERS = [
    ("acta_numerica_enkf_2025.pdf", "Acta Numerica 2025 - 均值场理论", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]),
    ("nature_comp_science_qml_2025.pdf", "Nature Comp Sci 2025 - QML陷阱", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]),
    ("npj_lindblad_tomography_2025.pdf", "npj Quantum Info 2025 - 非马尔可夫", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]),
    ("arxiv_nmr_quantum_kernels_2024.pdf", "arXiv 2024 - 量子核方法", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]),
    ("arxiv_quantum_reduction_2025.pdf", "arXiv 2025 - 量子降阶", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]),
    ("arxiv_mllenkb_2025.pdf", "arXiv 2025 - 多层局部EnKBF", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]),
    ("npg_quantum_da_2024.pdf", "NPG 2024 - 量子退火DA", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]),
]

def read_pages(filename, pages, dir_path):
    """读取指定页面"""
    filepath = os.path.join(dir_path, filename)
    reader = PdfReader(filepath)
    
    results = []
    for page_num in pages:
        if page_num <= len(reader.pages):
            text = reader.pages[page_num - 1].extract_text()
            results.append(f"=== Page {page_num} ===\n{text[:3000]}\n")
    
    return "\n".join(results)

def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    for filename, title, pages in PAPERS:
        print(f"\n{'='*60}")
        print(f"正在深度阅读: {title}")
        print(f"{'='*60}\n")
        
        content = read_pages(filename, pages, dir_path)
        
        # 保存到文件
        safe_title = title.split(" - ")[0].replace(" ", "_").replace("/", "_")
        output_file = os.path.join(dir_path, f"deep_read_{safe_title}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"已保存到: {output_file}")
        print(f"共 {len(pages)} 页\n")

if __name__ == "__main__":
    main()
