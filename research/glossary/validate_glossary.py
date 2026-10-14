"""Check reader links, terminology coverage and preservation of worked examples."""
from pathlib import Path
import hashlib
import json
import re
from linking import heading_anchor, validate_local_target

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parent
REGISTRY = json.loads((DATA / 'terms.json').read_text())
baseline = json.loads((DATA / 'migration-baseline.json').read_text())
terms = REGISTRY['terms']
glossary = ROOT / 'Objais Glossary.md'
revenue = ROOT / 'Objais Revenue Model Numerical Summary.md'
acquisition = ROOT / 'Objais Acquisition Numerical Summary.md'
sources = json.loads((ROOT / 'research/acquisition/markdown-package.json').read_text())
files = [glossary, revenue, acquisition, *[ROOT / f for f in sources['topic_files']]]

assert len({t['anchor'] for t in terms}) == len(terms)
assert sum('original_revenue_term' in t for t in terms) == 64
assert all(t['definition'] and t['source'] for t in terms)
links_checked = 0
for path in files:
    text = path.read_text()
    assert text.count('```') % 2 == 0, path.name
    assert '\ufffd' not in text, path.name
    assert len(re.findall(r'^# ', text, re.M)) == 1, path.name
    for target in re.findall(r'\]\(<([^>]+)>\)', text):
        validate_local_target(target)
        links_checked += 1
    for anchor in re.findall(r'\]\(#([^)]+)\)', text):
        validate_local_target(str(path) + '#' + anchor)
        links_checked += 1

unchanged = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == digest
             for p, digest in baseline['sha256'].items()}
assert all(unchanged.values()), unchanged
rev_text, acq_text = revenue.read_text(), acquisition.read_text()
assert 'Definition:' not in rev_text
assert 'shared glossary' in rev_text and 'shared glossary' in acq_text
assert not re.search(r'\[lead\]\(<[^>]+>\) to\b', rev_text + acq_text)
assert not re.search(r'\[measured\]\(<[^>]+>\)', acq_text)
for target in ['#conversion-probability', '#eligible-state-e', '#monetised-state-m']:
    assert target in rev_text, target
assert 'q = n × p × α' in rev_text
for needle in ['€20 − €1 − €1 = €18', '100 × €18 ÷ 1,000 = €1.80',
               '€1.80 − €0.20', '€1.60 − €4', '23.34%', '€45.27']:
    assert needle in rev_text, needle
for needle in ['5% request yield × 50% payable share × €18 − €0.10 = €0.35',
               '60 × €18 − €100 − €800 = +€180', 'R$10', '−€625', '−€150']:
    assert needle in acq_text, needle
assert len(re.findall(r'```mermaid\n', rev_text)) == 6
assert len(re.findall(r'```mermaid\n', acq_text)) >= 2
# First-use linking never alters the diagram source or surrounding fence.
diagram_names = ['actors', 'events', 'opportunity-states', 'independent-clocks', 'cash', 'scope']
embedded = re.findall(r'```mermaid\n(.*?)\n```', rev_text, re.S)
for name, source in zip(diagram_names, embedded):
    assert source.strip() == (ROOT / 'research/revenue-summary/diagrams' / (name + '.mmd')).read_text().strip()

def visible_words(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    text = re.sub(r'!\[[^]]*\]\((?:<[^>]+>|[^)]*)\)', '', text)
    text = re.sub(r'\[([^]]+)\]\((?:<[^>]+>|[^)]*)\)', r'\1', text)
    return len(text.split())

report = {
    'status': 'pass',
    'scope': 'Shared glossary and reader integration; no live research or empirical calibration',
    'terms': len(terms), 'previous_revenue_definitions_preserved': 64,
    'new_acquisition_terms': len(terms) - 64,
    'plain_language_terms': sum(t['kind'] == 'plain-language' for t in terms),
    'formal_concepts': sum(t['kind'] == 'formal' for t in terms),
    'cross_scope_terms': sum(t['cross_scope'] for t in terms),
    'unresolved_vocabulary': REGISTRY['unresolved_vocabulary'],
    'commercial_gaps': REGISTRY['commercial_gaps'],
    'local_links_and_anchors_checked': links_checked,
    'input_and_example_hashes_unchanged': unchanged,
    'standalone_revenue_definition_blocks': 0,
    'diagrams': {'revenue': 6, 'acquisition': len(re.findall(r'```mermaid\n', acq_text)), 'revenue_sources_match_exports': True},
    'guide_link_counts': {p.name: len(re.findall(r'Objais Glossary.md#', p.read_text()))
                         for p in [revenue, acquisition]},
    'word_counts': {p.name: {'before': baseline['guide_words'][p.name],
                            'after': len(p.read_text().split()),
                            'visible_prose_after': visible_words(p.read_text())}
                    for p in [revenue, acquisition]},
}
(DATA / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')

# Replace reports about the superseded inline-definition layout with current evidence.
rev_data = ROOT / 'research/revenue-summary'
source_hash = hashlib.sha256(rev_text.encode()).hexdigest()
registered = [dict(term=t['original_revenue_term'], glossary_term=t['term'],
                   glossary_anchor=t['anchor']) for t in terms if 'original_revenue_term' in t]
(rev_data / 'terminology-review.json').write_text(json.dumps({
    'status': 'pass', 'defined_terms': registered, 'definition_location': str(glossary),
    'review': '64 former inline definitions now resolve to the shared glossary; context and first-use links remain in the guide.',
    'source_sha256': source_hash,
    'numeric_results_sha256': baseline['sha256']['research/revenue-summary/numerical-examples.json']
}, indent=2) + '\n')
old = json.loads((rev_data / 'definition-formatting-review.json').read_text())
formatting = {k: old[k] for k in ['contribution_explanation_checks',
             'displayed_break_even_values', 'rounding']}
formatting.update(status='pass', definition_blocks=0,
                  format='Shared glossary with first-use links; contextual explanation stays with the examples',
                  glossary_terms=len(terms), numerical_input_files_unchanged=True,
                  source_sha256=source_hash, local_links_and_anchors_checked=links_checked)
(rev_data / 'definition-formatting-review.json').write_text(json.dumps(formatting, indent=2) + '\n')
editorial_path = rev_data / 'editorial-review.json'
editorial = json.loads(editorial_path.read_text())
editorial.update(total_words_after=len(rev_text.split()), prose_words_after=visible_words(rev_text),
                 source_sha256=source_hash, definition_blocks=0,
                 definition_format=formatting['format'], shared_glossary=str(glossary),
                 glossary_terms=len(terms), numerical_results_unchanged=True,
                 manual_review='Glossary links deliberately selected. Counting units, conditional chances, state labels, paid starts, acquisition ceilings and customer versus company time windows explained in context. Tables and calculation lines kept free of glossary links; numerical examples unchanged.',
                 glossary_migration_word_counts=report['word_counts'][revenue.name])
editorial['total_reduction_percent'] = round(100 * (1 - editorial['total_words_after']/editorial['total_words_before']), 1)
editorial['prose_reduction_percent'] = round(100 * (1 - editorial['prose_words_after']/editorial['prose_words_before']), 1)
editorial_path.write_text(json.dumps(editorial, indent=2) + '\n')
alignment_path = rev_data / 'problem-alignment-review.json'
alignment = json.loads(alignment_path.read_text())
alignment['coverage_review_line'] = rev_text.splitlines().index('## What would make the decision more grounded') + 1
alignment['source_sha256'] = source_hash
alignment_path.write_text(json.dumps(alignment, indent=2) + '\n')
diagram_review = rev_data / 'diagram-package-validation.json'
diagram_report = json.loads(diagram_review.read_text())
diagram_report['source_sha256'] = source_hash
diagram_report['glossary_migration_check'] = 'All six embedded sources match their exports; first-use links leave Mermaid blocks intact. No new browser inspection performed.'
diagram_review.write_text(json.dumps(diagram_report, indent=2) + '\n')
print(json.dumps(report, indent=2))
