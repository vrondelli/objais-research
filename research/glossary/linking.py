"""Shared first-use links and local Markdown anchor validation."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]


def heading_anchor(text):
    text = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'\s', '-', text)


def link_first_uses(text, glossary_path=None):
    """Link each concept once; leave headings, diagrams and existing links intact."""
    terms = json.loads((Path(__file__).parent / 'terms.json').read_text())['terms']
    glossary_path = glossary_path or str(ROOT / 'Objais Glossary.md')
    labels = {}
    for term in terms:
        for label in [term['term'], *term['aliases']]:
            if len(label) > 2:
                labels[label.lower()] = term['anchor']
    labels.update({'asset owners': 'asset-owner', 'opportunities': 'opportunity',
                   'prospects': 'prospect', 'impressions': 'impression',
                   'paid events': 'paid-event', 'payable events': 'paid-event',
                   'payment reversals': 'payment-reversal',
                   'paid accounts': 'paid-account', 'renewal fees': 'renewal',
                   'acquisition channel': 'channel', 'customer contribution':
                   'customer-contribution-over-a-stated-horizon',
                   'cost curve': 'cost-curve', 'billing continuation': 'billed-continuation'})
    pattern = re.compile(r'(?<![\w-])(' + '|'.join(
        re.escape(label) for label in sorted(labels, key=len, reverse=True)
    ) + r')(?![\w-])', re.I)
    # Links may be bold; protecting just the link leaves the surrounding style intact.
    protected = re.compile(r'(\[[^\]]*\]\((?:<[^>]*>|[^)]*)\)|`[^`]*`)')
    seen = set(re.findall(re.escape(glossary_path) + r'#([a-z0-9_-]+)', text))
    result = []
    in_fence = False
    for line_number, line in enumerate(text.splitlines(keepends=True)):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            result.append(line)
            continue
        if in_fence or line.startswith('#') or line_number < 4:
            result.append(line)
            continue
        def replace(match):
            anchor = labels[match.group(0).lower()]
            # "Lead to" is a verb, and evidence labels need their explicit status context.
            if anchor == 'lead' and re.match(r'\s+to\b', match.string[match.end():], re.I):
                return match.group(0)
            if anchor == 'revenue' and re.match(r'\s+(guide|model|summary)\b', match.string[match.end():], re.I):
                return match.group(0)
            if anchor == 'activation' and re.match(r'\s+of\s+cover\b', match.string[match.end():], re.I):
                return match.group(0)
            if anchor in {'measured', 'documented', 'assumed', 'unknown'}:
                return match.group(0)
            if anchor in seen:
                return match.group(0)
            seen.add(anchor)
            return f'[{match.group(0)}](<{glossary_path}#{anchor}>)'
        pieces = protected.split(line)
        result.append(''.join(pattern.sub(replace, p) if i % 2 == 0 else p
                              for i, p in enumerate(pieces)))
    return ''.join(result)


def validate_local_target(target):
    if target.startswith(('https:', 'http:')):
        return  # Dated external sources; this checker verifies local targets only.
    path_text, _, anchor = target.partition('#')
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    assert path.exists(), target
    if anchor:
        assert path.suffix == '.md', target
        anchors = {heading_anchor(m.group(1)) for m in re.finditer(
            r'^#{1,6} (.+)$', path.read_text(), re.M)}
        assert anchor in anchors, (target, 'Missing heading anchor')
