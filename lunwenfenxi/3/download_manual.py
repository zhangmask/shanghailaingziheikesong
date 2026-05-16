import urllib.request
import os

os.makedirs("d:\\Desktop\\laingzimuxi\\lunwenfenxi\\3", exist_ok=True)

# 逐个下载，带重试
papers = [
    ("https://arxiv.org/pdf/2510.11744", "arxiv_quantum_kernel_convergence_2025.pdf"),
]

for url, name in papers:
    filepath = os.path.join("d:\\Desktop\\laingzimuxi\\lunwenfenxi\\3", name)
    print(f"Downloading {name}...")
    try:
        urllib.request.urlretrieve(url, filepath)
        size = os.path.getsize(filepath)
        print(f"  Done: {size/1024:.1f} KB")
    except Exception as e:
        print(f"  Error: {e}")

print("Done!")
