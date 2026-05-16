#!/usr/bin/env python3
"""
下载剩余失败的论文
"""

import os
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

PAPERS = [
    # Acta Numerica 2025 - 正确URL
    (
        "acta_numerica_enkf_2025.pdf",
        "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/94C9B874BBD4F11B8D36DD42D9F01BC7/S0962492924000060a.pdf/ensemble_kalman_methods_a_meanfield_perspective.pdf",
        "Acta Numerica 2025, Calvello et al. - 集合卡尔曼均值场视角"
    ),
    
    # Nature Computational Science 2025 - 正确URL
    (
        "nature_comp_science_qml_2025.pdf",
        "https://www.nature.com/articles/s43588-025-00914-6.pdf",
        "Nature Computational Science 2025 - QML陷阱与前景"
    ),
    
    # Optics Express 2025 - 用arxiv版本
    (
        "oe_ml_covariance_2025.pdf",
        "https://arxiv.org/pdf/2509.21720",
        "Optics Express 2025 / arXiv:2509.21720 - ML量子态层析协方差估计"
    ),
]

def download_paper(filename, url, description):
    output_path = os.path.join(os.path.dirname(__file__), filename)
    
    if os.path.exists(output_path):
        print(f"  [跳过] {filename} 已存在")
        return True
    
    print(f"  下载: {filename}")
    print(f"        URL: {url}")
    
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
    print("下载剩余论文")
    print("=" * 60)
    
    for filename, url, description in PAPERS:
        download_paper(filename, url, description)
        print()

if __name__ == "__main__":
    main()
