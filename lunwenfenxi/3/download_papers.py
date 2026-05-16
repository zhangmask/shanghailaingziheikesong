import urllib.request
import os

papers = [
    {
        "url": "https://www.nature.com/articles/s41566-025-01682-5.pdf",
        "name": "nature_photonics_quantum_kernel_2025.pdf",
        "title": "Experimental quantum-enhanced kernel-based machine learning on a photonic processor"
    },
    {
        "url": "https://openreview.net/pdf?id=RbUe1cLXrJ",
        "name": "iclr2026_quantum_generator_kernels.pdf",
        "title": "Quantum Generator Kernels"
    },
    {
        "url": "https://journals.aps.org/prresearch/pdf/10.1103/PhysRevResearch.6.033179",
        "name": "prresearch_quantum_tangent_kernel_2024.pdf",
        "title": "Quantum tangent kernel"
    },
    {
        "url": "https://arxiv.org/pdf/2510.11744",
        "name": "arxiv_quantum_kernel_convergence_2025.pdf",
        "title": "Quantum Kernel Methods: Convergence Theory, Separation Bounds"
    }
]

os.makedirs("d:\\Desktop\\laingzimuxi\\lunwenfenxi\\3", exist_ok=True)

for paper in papers:
    filepath = os.path.join("d:\\Desktop\\laingzimuxi\\lunwenfenxi\\3", paper["name"])
    print(f"Downloading: {paper['title']}")
    try:
        urllib.request.urlretrieve(paper["url"], filepath)
        size = os.path.getsize(filepath)
        print(f"  ✓ Saved: {size/1024:.1f} KB")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

print("\n下载完成！")
