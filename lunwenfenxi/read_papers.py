from pypdf import PdfReader
import os

os.chdir(r'd:\Desktop\laingzimuxi\lunwenfenxi')

# Read NPG 2024 paper
print('='*80)
print('PAPER 1: NPG 2024 - Quantum data assimilation (Kotsuki et al.)')
print('='*80)
reader = PdfReader('npg_quantum_da.pdf')
for i, page in enumerate(reader.pages[:8]):
    text = page.extract_text()
    if text:
        print(f'\n--- Page {i+1} ---')
        print(text[:2500])

print('\n\n')

# Read quantum reservoir paper
print('='*80)
print('PAPER 3: arXiv 2405.03390 - Quantum Reservoir Computing')
print('='*80)
reader2 = PdfReader('quantum_reservoir_2405.pdf')
for i, page in enumerate(reader2.pages[:12]):
    text = page.extract_text()
    if text:
        print(f'\n--- Page {i+1} ---')
        print(text[:2500])

print('\n\n')

# Read operator algebras paper
print('='*80)
print('PAPER 4: arXiv 2206.13659 - DA in Operator Algebras')
print('='*80)
reader3 = PdfReader('da_operator_algebras_2206.pdf')
for i, page in enumerate(reader3.pages[:10]):
    text = page.extract_text()
    if text:
        print(f'\n--- Page {i+1} ---')
        print(text[:2500])
