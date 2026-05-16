#!/usr/bin/env python3
"""下载直接相关的量子数据同化/卡尔曼滤波论文"""

import requests
import os

os.makedirs("papers", exist_ok=True)

papers = [
    {
        "name": "prx_quantum_kalman_filter_2025.pdf",
        "url": "https://arxiv.org/pdf/2403.14764",
        "title": "Noisy atomic magnetometry with Kalman filtering and measurement-based feedback (PRX Quantum 2025)"
    },
    {
        "name": "arxiv_physical_localization_2025.pdf",
        "url": "https://arxiv.org/pdf/2511.08845",
        "title": "Physics-based localization methodology for Data Assimilation by Ensemble Kalman Filter"
    },
    {
        "name": "arxiv_bayesian_quantum_state_2025.pdf",
        "url": "https://arxiv.org/pdf/2501.17334",
        "title": "Unorthodox parallelization for Bayesian quantum state estimation"
    },
    {
        "name": "arxiv_quantum_bayesian_filter_2025.pdf",
        "url": "https://arxiv.org/pdf/2512.05265",
        "title": "Quantum Bayesian filtering (continuous monitoring)"
    },
]

for paper in papers:
    try:
        print(f"Downloading: {paper['title']}")
        response = requests.get(paper['url'], timeout=60)
        if response.status_code == 200 and len(response.content) > 100000:
            with open(f"papers/{paper['name']}", "wb") as f:
                f.write(response.content)
            print(f"  ✅ 成功: {len(response.content)} bytes")
        else:
            print(f"  ❌ 失败: status={response.status_code}, size={len(response.content)}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

print("\n下载完成")
