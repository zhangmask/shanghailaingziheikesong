#!/usr/bin/env python3
"""
深度提取核心论文的文本内容，用于进一步分析
"""
import os
import subprocess

output_dir = r"d:\Desktop\laingzimuxi\lunwenfenxi\4"

# 核心论文列表
core_papers = [
    ("04_quantum_smoothing_arxiv_2025.pdf", "量子平滑与错误假设"),
    ("05_quantum_reduced_filters_arxiv_2025.pdf", "量子降阶滤波"),
    ("06_quantum_state_trajectories_arxiv_2025.pdf", "量子态轨迹估计"),
    ("07_physics_based_localization_arxiv_2025.pdf", "物理驱动局部化"),
]

def extract_text_from_pdf(pdf_path, max_pages=20):
    """使用pdftotext提取PDF文本"""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", "-f", "1", "-l", str(max_pages), pdf_path, "-"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout[:10000]
        else:
            return f"Error: {result.stderr}"
    except FileNotFoundError:
        try:
            import fitz
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(min(max_pages, len(doc))):
                page = doc[page_num]
                text += page.get_text()
            doc.close()
            return text[:10000]
        except ImportError:
            return "Error: Neither pdftotext nor PyMuPDF available"
    except Exception as e:
        return f"Error: {str(e)}"

def extract_key_sections(text, keywords):
    """提取包含关键词的段落"""
    lines = text.split('\n')
    key_sections = []
    for i, line in enumerate(lines):
        for kw in keywords:
            if kw.lower() in line.lower():
                # 提取前后5行
                start = max(0, i-3)
                end = min(len(lines), i+8)
                section = '\n'.join(lines[start:end])
                key_sections.append(f"[Line {i}: {kw}]")
                key_sections.append(section)
                key_sections.append("---")
                break
    return '\n'.join(key_sections[:3000])

if __name__ == "__main__":
    results = {}
    for pdf_name, desc in core_papers:
        pdf_path = os.path.join(output_dir, pdf_name)
        print(f"\n{'='*80}")
        print(f"论文: {pdf_name}")
        print(f"主题: {desc}")
        print(f"{'='*80}")
        
        if not os.path.exists(pdf_path):
            print(f"⚠️ 文件不存在: {pdf_path}")
            continue
        
        text = extract_text_from_pdf(pdf_path)
        print(text[:2000])
        results[pdf_name] = text
    
    # 保存提取结果
    output_path = os.path.join(output_dir, "core_papers_text_extract.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 核心论文文本深度提取\n\n")
        for pdf_name, desc in core_papers:
            f.write(f"## {desc} ({pdf_name})\n\n")
            if pdf_name in results and results[pdf_name]:
                f.write(f"```\n{results[pdf_name][:5000]}\n```\n\n")
            else:
                f.write("⚠️ 提取失败\n\n")
    print(f"\n✅ 文本已保存到: {output_path}")
