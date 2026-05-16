from pypdf import PdfReader
import os

os.chdir(r'd:\Desktop\laingzimuxi\lunwenfenxi')

# Read quantum reservoir paper - first 15 pages
print('='*80)
print('PAPER 3: arXiv 2405.03390 - Quantum Reservoir Computing')
print('='*80)
reader = PdfReader('quantum_reservoir_2405.pdf')
for i, page in enumerate(reader.pages[:15]):
    text = page.extract_text()
    if text:
        print(f'\n--- Page {i+1} ---')
        print(text[:3000])
