#!/usr/bin/env python3
"""下载量子滤波/量子贝叶斯滤波相关论文"""

import requests
import os

os.makedirs("papers", exist_ok=True)

papers = [
    {
        "name": "arxiv_quantum_state_trajectories_2510.pdf",
        "url": "https://arxiv.org/pdf/2510.16754",
        "title": "Post-processed estimation of quantum state trajectories"
    },
    {
        "name": "arxiv_quantum_reduced_filters_2511.pdf",
        "url": "https://arxiv.org/pdf/2511.07949",
        "title": "Stabilization of Time-Varying Perturbed Quantum Systems via Reduced Filters"
    },
    {
        "name": "arxiv_quantum_smoothing_2506.pdf",
        "url": "https://arxiv.org/pdf/2506.15951",
        "title": "Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob"
    },
    {
        "name": "arxiv_quantum_calibration_2507.pdf",
        "url": "https://arxiv.org/pdf/2507.06941",
        "title": "Calibration of Quantum Devices via Robust Statistical Methods"
    },
    {
        "name": "arxiv_quantum_amplitude_estimation_2412.pdf",
        "url": "https://arxiv.org/pdf/2412.04394",
        "title": "Bayesian Quantum Amplitude Estimation"
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
