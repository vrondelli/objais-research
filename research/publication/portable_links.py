"""Convert generated workspace links to repository-relative links."""
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[2]


def normalise():
    for p in ROOT.rglob('*.md'):
        if any(x in p.parts for x in ['node_modules', '.git']):
            continue
        text = p.read_text()
        def convert(match):
            target = match.group(1)
            base, separator, anchor = target.partition('#')
            if base.startswith(str(ROOT) + '/'):
                base = os.path.relpath(base, p.parent).replace(os.sep, '/')
            return '](<' + base + (separator + anchor if separator else '') + '>)'
        text = re.sub(r'\]\(<([^>]+)>\)', convert, text)
        p.write_text(text.replace(str(ROOT) + '/', ''))
    for p in ROOT.rglob('*.json'):
        if any(x in p.parts for x in ['node_modules', '.git']):
            continue
        p.write_text(p.read_text().replace(str(ROOT) + '/', ''))
