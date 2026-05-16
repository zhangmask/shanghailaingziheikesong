#!/usr/bin/env python3
"""
批量下载2023年后顶会顶刊优秀论文
"""

import os
import urllib.request
import ssl

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 论文列表：(标题, PDF URL, 来源)
PAPERS = [
    # ===== NPG 2024: Quantum data assimilation (千叶大学) =====
    (
        "npg_quantum_da_2024.pdf",
        "https://npg.copernicus.org/articles/31/237/2024/npg-31-237-2024.pdf",
        "NPG 2024, Kotsuki et al. - 量子退火DA"
    ),
    
    # ===== NPG 2025: Coupled data assimilation =====
    (
        "npg_coupled_da_2025.pdf",
        "https://npg.copernicus.org/articles/32/439/2025/npg-32-439-2025.pdf",
        "NPG 2025, Garcia-Oliva et al. - 时空尺度耦合DA"
    ),
    
    # ===== JMSJ 2025: 4DVar + Quantum Annealing =====
    (
        "jmsj_4dvar_qa_2025.pdf",
        "https://metsoc.jp/jmsj/EOR/2025-032.pdf",
        "JMSJ 2025 - 二阶增量+量子退火4DVar"
    ),
    
    # ===== Optics Express 2025: ML for QST covariance =====
    (
        "oe_ml_covariance_2025.pdf",
        "https://mx.nthu.edu.tw/~rklee/files/OE-25-covariance.pdf",
        "Optics Express 2025 - ML量子态层析协方差估计"
    ),
    
    # ===== npj Quantum Information 2025: Lindblad-like tomography =====
    (
        "npj_lindblad_tomography_2025.pdf",
        "https://www.nature.com/articles/s41534-025-01044-7.pdf",
        "npj Quantum Information 2025 - 非马尔可夫量子层析"
    ),
    
    # ===== arXiv 2025: Multilevel Localized EnKBF =====
    (
        "arxiv_mllenkb_2025.pdf",
        "https://arxiv.org/pdf/2502.16808",
        "arXiv:2502.16808 - 多层局部EnKBF"
    ),
    
    # ===== arXiv 2025: Quantum model reduction for filters =====
    (
        "arxiv_quantum_reduction_2025.pdf",
        "https://arxiv.org/pdf/2501.13885",
        "arXiv:2501.13885 - 量子滤波器降阶"
    ),
    
    # ===== arXiv 2024: NMR Quantum Kernels =====
    (
        "arxiv_nmr_quantum_kernels_2024.pdf",
        "https://arxiv.org/pdf/2412.09557",
        "arXiv:2412.09557 - NMR量子核方法实验"
    ),
    
    # ===== Acta Numerica 2025: Ensemble Kalman mean field =====
    (
        "acta_numerica_enkf_2025.pdf",
        "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/123-291/S0962492924000060.pdf",
        "Acta Numerica 2025, Calvello et al. - 集合卡尔曼均值场"
    ),
    
    # ===== Nature Computational Science 2025: QML pitfalls =====
    (
        "nature_comp_science_qml_2025.pdf",
        "https://www.nature.com/articles/s41567-025-02844-1.pdf",
        "Nature Computational Science 2025 - QML陷阱与前景"
    ),
]

def download_paper(filename, url, description):
    """下载单篇论文"""
    output_path = os.path.join(os.path.dirname(__file__), filename)
    
    if os.path.exists(output_path):
        print(f"  [跳过] {filename} 已存在")
        return True
    
    print(f"  下载: {filename}")
    print(f"        URL: {url}")
    print(f"        说明: {description}")
    
    try:
        urllib.request.urlretrieve(url, output_path)
        size = os.path.getsize(output_path)
        print(f"  [成功] {filename} ({size/1024:.1f} KB)")
        return True
    except Exception as e:
        print(f"  [失败] {filename}: {e}")
        return False

def main():
    print("=" * 60)
    print("下载2023年后顶会顶刊优秀论文")
    print("=" * 60)
    print()
    
    success_count = 0
    fail_count = 0
    
    for filename, url, description in PAPERS:
        if download_paper(filename, url, description):
            success_count += 1
        else:
            fail_count += 1
        print()
    
    print("=" * 60)
    print(f"下载完成: 成功 {success_count} 篇, 失败 {fail_count} 篇")
    print("=" * 60)

if __name__ == "__main__":
    main()
