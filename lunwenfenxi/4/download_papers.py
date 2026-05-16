#!/usr/bin/env python3
"""
下载与量子数据同化相关的顶会顶刊论文
"""
import os
import urllib.request
import ssl

# 创建目录
output_dir = r"d:\Desktop\laingzimuxi\lunwenfenxi\4"
os.makedirs(output_dir, exist_ok=True)

# 论文列表 (URL, 文件名, 来源)
papers = [
    # 量子数据同化 - 顶刊
    ("https://npg.copernicus.org/articles/31/237/2024/npg-31-237-2024.pdf", 
     "01_quantum_data_assimilation_NPG_2024.pdf", "Nonlin. Processes Geophys. 2024"),
    
    # 量子数据同化 - Science Advances 顶刊
    ("https://www.science.org/doi/pdf/10.1126/sciadv.aea4248", 
     "02_physically_consistent_da_ScienceAdv_2026.pdf", "Science Advances 2026"),
    
    # 量子机器学习天气预测
    ("https://arxiv.org/pdf/2509.01422", 
     "03_quantum_ml_weather_forecasting_arxiv_2025.pdf", "arXiv 2025"),
    
    # 量子平滑
    ("https://arxiv.org/pdf/2506.15951", 
     "04_quantum_smoothing_arxiv_2025.pdf", "arXiv 2025"),
    
    # 量子降阶滤波
    ("https://arxiv.org/pdf/2511.07949", 
     "05_quantum_reduced_filters_arxiv_2025.pdf", "arXiv 2025"),
    
    # 量子轨迹
    ("https://arxiv.org/pdf/2510.16754", 
     "06_quantum_state_trajectories_arxiv_2025.pdf", "arXiv 2025"),
    
    # 物理驱动局部化
    ("https://arxiv.org/pdf/2511.08845", 
     "07_physics_based_localization_arxiv_2025.pdf", "arXiv 2025"),
    
    # 量子校准
    ("https://arxiv.org/pdf/2507.06941", 
     "08_quantum_calibration_arxiv_2025.pdf", "arXiv 2025"),
    
    # 量子幅度估计
    ("https://arxiv.org/pdf/2412.04394", 
     "09_quantum_amplitude_estimation_arxiv_2024.pdf", "arXiv 2024"),
    
    # 贝叶斯量子态估计
    ("https://arxiv.org/pdf/2501.17334", 
     "10_bayesian_qst_arxiv_2025.pdf", "arXiv 2025"),
    
    # 气候预测与机器学习
    ("https://npg.copernicus.org/articles/32/397/2025/npg-32-397-2025.pdf", 
     "11_hybrid_climate_prediction_NPG_2025.pdf", "Nonlin. Processes Geophys. 2025"),
    
    # 量子退火 4D-Var (JMSJ)
    ("https://jmsj.jstage.jst.go.jp/article/jmsj/103/5/103_2025-032/_pdf", 
     "12_quantum_annealing_4dvar_JMSJ_2025.pdf", "J. Meteor. Soc. Jpn. 2025"),
]

# 创建 SSL 上下文（绕过证书验证，用于某些下载）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download_paper(url, filename, source):
    """下载单篇论文"""
    filepath = os.path.join(output_dir, filename)
    if os.path.exists(filepath):
        print(f"⏭️  已存在: {filename}")
        return filepath
    
    print(f"⬇️  下载: {filename} ({source})")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as response:
            with open(filepath, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        size = os.path.getsize(filepath)
        print(f"✅ 下载成功: {size/1024/1024:.1f} MB")
        return filepath
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("下载量子数据同化相关顶会顶刊论文")
    print("=" * 60)
    
    for url, filename, source in papers:
        download_paper(url, filename, source)
    
    # 列出已下载的论文
    print("\n" + "=" * 60)
    print("已下载论文列表:")
    print("=" * 60)
    for f in sorted(os.listdir(output_dir)):
        if f.endswith('.pdf'):
            size = os.path.getsize(os.path.join(output_dir, f))
            print(f"  {f} ({size/1024/1024:.1f} MB)")
