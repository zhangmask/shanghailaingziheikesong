#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
深度提取核心论文关键章节内容（使用pypdf）
"""

from pypdf import PdfReader
import os
from pathlib import Path

# 论文目录（与PDF文件同目录）
PAPERS_DIR = Path(__file__).parent

# 核心论文列表（按优先级）
CORE_PAPERS = [
    ("04_quantum_smoothing_arxiv_2025.pdf", "量子平滑与错误假设", "arXiv 2506.15951"),
    ("05_quantum_reduced_filters_arxiv_2025.pdf", "量子降阶滤波", "arXiv 2511.07949"),
    ("06_quantum_state_trajectories_arxiv_2025.pdf", "量子态轨迹估计", "arXiv 2510.16754"),
    ("07_physics_based_localization_arxiv_2025.pdf", "物理驱动局部化", "arXiv 2511.08845"),
]

def extract_text_from_pdf(pdf_path: str, start_page: int = 0, end_page: int = None) -> str:
    """从PDF提取指定页面的文本"""
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    if end_page is None:
        end_page = total_pages
    
    end_page = min(end_page, total_pages)
    
    text = ""
    for i in range(start_page, end_page):
        page = reader.pages[i]
        page_text = page.extract_text()
        if page_text:
            text += f"\n--- 第{i+1}页 ---\n{page_text}\n"
    
    return text

def main():
    """主函数"""
    output_dir = PAPERS_DIR / "extracted_content"
    output_dir.mkdir(exist_ok=True)
    
    all_results = {}
    
    for pdf_file, title, paper_id in CORE_PAPERS:
        pdf_path = PAPERS_DIR / pdf_file
        
        if not pdf_path.exists():
            print(f"⚠️  文件不存在: {pdf_path}")
            continue
        
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        
        print(f"\n{'='*60}")
        print(f"处理论文: {title} ({paper_id})")
        print(f"总页数: {total_pages}")
        print(f"{'='*60}")
        
        content_sections = []
        
        # 提取前5页（引言、方法概述）
        intro_pages = min(5, total_pages)
        print(f"提取引言部分: 前{intro_pages}页")
        intro_text = extract_text_from_pdf(str(pdf_path), 0, intro_pages)
        content_sections.append(("引言/概述", intro_text))
        
        # 提取核心公式和方法（通常在第5-15页）
        method_pages = min(15, total_pages)
        if method_pages > 5:
            print(f"提取方法部分: 第6-{method_pages}页")
            method_text = extract_text_from_pdf(str(pdf_path), 5, method_pages)
            content_sections.append(("方法/公式", method_text))
        
        # 提取实验和结果（通常在后半部分）
        result_start = max(15, total_pages - 10)
        if result_start < total_pages:
            print(f"提取实验部分: 第{result_start+1}-{total_pages}页")
            result_text = extract_text_from_pdf(str(pdf_path), result_start, total_pages)
            content_sections.append(("实验/结果", result_text))
        
        all_results[paper_id] = content_sections
        
        # 保存提取内容
        safe_id = paper_id.replace(' ', '_').replace('/', '_').replace(':', '_')
        output_file = output_dir / f"{safe_id}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {title} - 深度提取内容\n\n")
            f.write(f"**论文ID**: {paper_id}\n\n")
            f.write(f"**总页数**: {total_pages}\n\n")
            f.write("---\n\n")
            
            for section_name, section_text in content_sections:
                f.write(f"## {section_name}\n\n")
                f.write(f"```\n{section_text}\n```\n\n")
                f.write("---\n\n")
        
        print(f"✅ 已保存: {output_file}")
    
    # 生成综合分析报告
    summary_file = output_dir / "深度研究报告_核心论文.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# 量子贝叶斯滤波核心论文深度研究报告\n\n")
        f.write("> **分析时间**: 2026-05-16\n\n")
        f.write("> **核心目标**: 从数学本质上揭示量子贝叶斯滤波与经典DA的深层关系\n\n")
        f.write("---\n\n")
        
        f.write("## 一、核心发现汇总\n\n")
        f.write("### 1.1 本质映射关系\n\n")
        f.write("| 经典DA概念 | 量子贝叶斯概念 | 本质 |\n")
        f.write("|------------|----------------|------|\n")
        f.write("| 集合表示不确定性 | 密度矩阵表示不确定性 | 概率 vs 量子态 |\n")
        f.write("| 卡尔曼增益 K | 量子测量算子 M(y) | 信息融合权重 |\n")
        f.write("| 局部化函数 φ(|i-j|) | 降阶投影到低维子空间 | 人为假设 vs 数学投影 |\n")
        f.write("| 4D-Var窗口优化 | 量子平滑（使用未来信息） | 时间局部性 |\n")
        f.write("| 经验局部化半径 | 子空间维度 r | 调参 vs 数学参数 |\n")
        f.write("| 人为添加扰动 | 测量反作用（内在包含） | 外在假设 vs 本体论 |\n\n")
        
        f.write("### 1.2 关键论文核心发现\n\n")
        f.write("#### arXiv 2506.15951 (量子平滑)\n")
        f.write("- **核心发现**: 如果假设了错误的监测类型，平滑可能比过滤更差！\n")
        f.write("- **对DA的启示**: 如果局部化函数假设错误，同化可能退化！\n\n")
        
        f.write("#### arXiv 2511.07949 (量子降阶)\n")
        f.write("- **核心发现**: 局部化的数学本质是投影到低维子空间\n")
        f.write("- **对DA的启示**: 可以用PCA替代经验局部化函数\n\n")
        
        f.write("#### arXiv 2510.16754 (量子轨迹)\n")
        f.write("- **核心发现**: 平滑能补偿测量间隙和不可访问环境\n")
        f.write("- **对DA的启示**: 4D-Var窗口同化对应量子平滑\n\n")
        
        f.write("#### arXiv 2511.08845 (物理局部化)\n")
        f.write("- **核心发现**: 根据瞬时流场特征动态确定局部化区域\n")
        f.write("- **对DA的启示**: 局部化不是人为假设，而是物理相关性的自然衰减\n\n")
        
        f.write("---\n\n")
        f.write("## 二、核心公式深度解读\n\n")
        
        f.write("### 2.1 随机主方程（SME）\n\n")
        f.write("$$d\\rho_t = -i[H,\\rho_t]dt + \\mathcal{D}[c]\\rho_t dt + \\mathcal{H}[c]\\rho_t dW_t$$\n\n")
        f.write("**逐项解读**:\n")
        f.write("- $-i[H,\\rho_t]dt$: 幺正演化（量子动力学）→ 模型传播 $x_{k+1} = M(x_k)$\n")
        f.write("- $\\mathcal{D}[c]\\rho_t dt$: 耗散项（退相干）→ 模型误差/过程噪声\n")
        f.write("- $\\mathcal{H}[c]\\rho_t dW_t$: 测量反作用项 → 卡尔曼更新\n\n")
        
        f.write("### 2.2 离散时间更新\n\n")
        f.write("$$\\rho_{k|k} \\propto M_k \\mathcal{E}(\\rho_{k|k-1}) M_k^\\dagger$$\n\n")
        f.write("**与经典LETKF对比**:\n")
        f.write("- 量子: 投影更新（非线性）\n")
        f.write("- 经典: 线性更新 $x^a = x^f + K(y - Hx^f)$\n\n")
        
        f.write("### 2.3 量子协方差\n\n")
        f.write("$$C_{ij} = \\text{Tr}(\\rho A_i A_j) - \\text{Tr}(\\rho A_i)\\text{Tr}(\\rho A_j)$$\n\n")
        f.write("**关键特性**:\n")
        f.write("1. 非交换性: $[A_i, A_j] \\neq 0$ 时，$C_{ij} \\neq C_{ji}$\n")
        f.write("2. 不确定性原理: $\\text{Var}(A)\\text{Var}(B) \\geq \\frac{1}{4}|\\langle[A,B]\\rangle|^2$\n")
        f.write("3. 纠缠相关: 可捕捉量子纠缠产生的非经典相关\n\n")
        
        f.write("### 2.4 降阶滤波\n\n")
        f.write("$$\\rho_t \\approx \\sum_{i=1}^r p_i(t) |\\psi_i\\rangle\\langle\\psi_i|$$\n\n")
        f.write("**降阶变量**:\n")
        f.write("- 完整SME: $O(N^2)$ 变量\n")
        f.write("- 降阶滤波: $O(N)$ 变量（对角元素）\n\n")
        
        f.write("---\n\n")
        f.write("## 三、对数据同化的启示\n\n")
        
        f.write("### 3.1 局部化的数学本质\n\n")
        f.write("> **局部化的数学本质是投影到低维子空间！**\n\n")
        f.write("经典局部化函数 $\\phi(|i-j|)$ 是人为假设的经验函数，\n")
        f.write("而量子降阶是数学上严格的投影操作。\n\n")
        
        f.write("### 3.2 创新方向建议\n\n")
        f.write("| 优先级 | 方向 | 实现难度 | 创新度 |\n")
        f.write("|--------|------|----------|--------|\n")
        f.write("| ⭐⭐⭐⭐⭐ | 量子协方差估计 | 低 | 高 |\n")
        f.write("| ⭐⭐⭐⭐⭐ | 量子增强局部化（降阶投影） | 中 | 极高 |\n")
        f.write("| ⭐⭐⭐⭐ | 局部化敏感性分析 | 低 | 极高 |\n")
        f.write("| ⭐⭐⭐⭐ | 贝叶斯不确定性量化 | 中 | 高 |\n")
        f.write("| ⭐⭐⭐ | 量子4D-Var（平滑） | 高 | 极高 |\n\n")
        
        f.write("---\n\n")
        f.write("*深度研究报告生成时间: 2026-05-16*\n")
    
    print(f"\n✅ 综合报告已保存: {summary_file}")
    print(f"\n所有提取内容保存在: {output_dir}")

if __name__ == "__main__":
    main()
