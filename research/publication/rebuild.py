"""Rebuild synthetic examples and reader documents with portable public links."""
from pathlib import Path
import subprocess
import sys
from portable_links import normalise

ROOT = Path(__file__).resolve().parents[2]
for script in ['research/revenue-model/build_extension_examples.py',
               'research/revenue-summary/build_summary.py',
               'research/glossary/build_glossary.py',
               'research/formulas/build_formula_figures.py']:
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)
normalise()
for script in ['research/acquisition/verify_markdown_package.py',
               'research/glossary/validate_glossary.py',
               'research/formulas/validate_formula_figures.py']:
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)
normalise()
subprocess.run([sys.executable, 'research/publication/check_package.py'], cwd=ROOT, check=True)
