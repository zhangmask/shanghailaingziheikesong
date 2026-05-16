from pypdf import PdfReader
import os

os.chdir(r'd:\Desktop\laingzimuxi\lunwenfenxi')

# Read NPG 2024 paper - remaining pages
print('='*80)
print('PAPER 1: NPG 2024 - Quantum data assimilation (Kotsuki et al.) - CONTINUED')
print('='*80)
reader = PdfReader('npg_quantum_da.pdf')
for i, page in enumerate(reader.pages[8:]):
    text = page.extract_text()
    if text:
        print(f'\n--- Page {i+9} ---')
        print(text[:2500])

print('\n\n')

# Read QML bibliometric paper
print('='*80)
print('PAPER 2: arXiv 2504.07726 - QML Bibliometric Analysis')
print('='*80)
reader2 = PdfReader('qml_bibliometric.pdf')
for i, page in enumerate(reader2.pages[:8]):
    text = page.extract_text()
    if text:
        print(f'\n--- Page {i+1} ---')
        print(text[:2500])
