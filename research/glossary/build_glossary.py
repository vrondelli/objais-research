"""Render the shared reader glossary from source-linked term records."""
from pathlib import Path
import json
from linking import heading_anchor, validate_local_target

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parent
registry = json.loads((DATA / 'terms.json').read_text())
terms = registry['terms']


def link(label, filename, anchor=None):
    target = str(ROOT / filename) + ('#' + anchor if anchor else '')
    validate_local_target(target)
    return f'[{label}](<{target}>)'


parts = [
    '# Objais Glossary',
    'Shared terms for the revenue and acquisition guides, covering the current business and future options. Open a definition when you need it; the guides explain their examples without requiring a glossary read-through.',
    'Start with ' + link('the revenue guide', 'Objais Revenue Model Numerical Summary.md')
    + ' or ' + link('the acquisition guide', 'Objais Acquisition Numerical Summary.md') + '.',
    'Terms describe how these documents count people, tasks and money. Their source links lead to the underlying model or research. They do not establish that Objais has a particular contract, capability or measured result.',
    ' · '.join(f'[{group}](#{heading_anchor(group)})' for group in registry['groups']),
    '## Distinctions that change the numbers',
    '- **Owner, interaction and opportunity:** one person can click several times, own several items and make several requests. Each needs its own counting unit.\n'
    '- **Paid event and payable event:** these are two names for the same contractual earning condition here. A product event or card sale is not automatically one.\n'
    '- **CAC, CPA and CPC:** owner CAC counts distinct new owners and full acquisition costs. CPA names another outcome and its cost scope; CPC counts advertising clicks.\n'
    '- **Conversion rates:** the owner model’s q, the share of requests accepted and the share of clicks producing a fee begin with different groups. Always keep the denominator.\n'
    '- **Fee, premium and cash:** the insurance premium is not Objais’s fee. Earning the fee, invoicing it and receiving the money are stages of the same amount.\n'
    '- **Retention and renewal:** app use, opportunity continuation, cover and software payments follow different clocks. A return earns another fee only when the agreement permits it.',
]
for group in registry['groups']:
    parts.append(f'## {group}')
    for term in sorted((t for t in terms if t['category'] == group),
                       key=lambda t: (t['kind'] != 'plain-language', t['term'].lower())):
        assert heading_anchor(term['term']) == term['anchor'], term['term']
        source_anchor = heading_anchor(term['source_heading']) if 'source_heading' in term else None
        source = link('Source', term['source'], source_anchor)
        # State aliases that help readers search, omitting single-letter symbols explained in prose.
        aliases = [a for a in term['aliases'] if len(a) > 2 and a.lower() != term['term'].lower()]
        alias_note = (' Also used: ' + ', '.join(aliases) + '.') if aliases else ''
        parts.append(f"### {term['term']}\n\n{term['definition']}{alias_note} {source}")
parts.extend([
    '## What still needs confirmation',
    'The vocabulary is consistent across the guides. The team still needs to supply the contractual payment conditions, observed behaviour, full costs and collection dates. Future paid demand, professional account units and availability in each country remain open commercial questions.',
    'The ' + link('metric dictionary', 'Objais Metrics Research.md', 'full-metric-dictionary')
    + ' retains the detailed formulas, counting rules and observation windows. The '
    + link('event dictionary', 'Objais Measurement and Attribution Research.md', 'full-proposed-event-dictionary')
    + ' retains the proposed occurrence and identity rules. This glossary explains their terms; the dictionaries and model hold the operational detail.',
])
(ROOT / 'Objais Glossary.md').write_text('\n\n'.join(parts) + '\n')
counts = {kind: sum(t['kind'] == kind for t in terms) for kind in ['plain-language', 'formal']}
report = f"""## Feature Glossary Result

- Scope: {registry['scope']}
- Output: {ROOT / 'Objais Glossary.md'}
- Plain-language terms: {counts['plain-language']}
- Formal concepts: {counts['formal']}
- Cross-scope terms: {sum(t['cross_scope'] for t in terms)} (included in the counts above)
- Unresolved terms: {len(registry['unresolved_vocabulary'])}
- Validation: Source files and heading anchors checked during generation; guide integration and unchanged numerical inputs checked by validate_glossary.py.
- Follow-up: Actual payment conditions, observed rates, full costs, future demand and country availability need team evidence. No commercial behaviour has been added by the glossary.
"""
(DATA / 'Feature Glossary Result.md').write_text(report)
print(f'Created glossary: {len(terms)} entries; source links checked.')
