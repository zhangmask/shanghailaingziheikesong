from pypdf import PdfReader
import os

os.chdir(r'd:\Desktop\laingzimuxi\lunwenfenxi')

# Read NPG 2024 paper - focus on QUBO formulation
print('='*80)
print('PAPER 1: NPG 2024 - QUBO FORMULATION (核心数学)')
print('='*80)
reader = PdfReader('npg_quantum_da.pdf')
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        # Look for mathematical content
        if any(kw in text.lower() for kw in ['cost function', 'objective', 'qubo', 'quadratic', 'hamiltonian', 'equation', 'formula', 'minimize', 'optimization']):
            print(f'\n--- Page {i+1} ---')
            print(text[:3000])

print('\n\n')

# Read operator algebras paper - focus on mathematical structure
print('='*80)
print('PAPER 4: arXiv 2206.13659 - OPERATOR ALGEBRA STRUCTURE (核心数学)')
print('='*80)
reader2 = PdfReader('da_operator_algebras_2206.pdf')
for i, page in enumerate(reader2.pages[10:20]):
    text = page.extract_text()
    if text:
        print(f'\n--- Page {i+11} ---')
        print(text[:3000])
