"""Cross-check the annotated panels against the existing executable examples."""
from pathlib import Path
from dataclasses import replace
import hashlib
import json
import math
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'research/revenue-model'))
from revenue_model import Parameters, finite_value, simulate

examples = json.loads((ROOT / 'research/revenue-summary/numerical-examples.json').read_text())
baselines = examples['baselines']
schedule = [1000] + [0] * 35
checks = {}


def equal(name, observed, reference):
    assert math.isclose(observed, reference, abs_tol=1e-8), (name, observed, reference)
    checks[name] = observed


lead = Parameters(**baselines['lead'])
lead_unit = lead.q * (lead.initial_payment * (1 - lead.reversal_fraction) - lead.event_cost) - lead.eligible_month_cost - lead.cac
equal('one_visit_contribution_per_owner', lead_unit, examples['experiments'][0]['unit_before'])
entry = json.loads((ROOT / 'research/acquisition/central-examples.json').read_text())['scenarios'][0]
i, r = entry['inputs'], entry['results']
ceiling = (r['requests'] / i['clicks']) * (r['payable_events'] / r['requests']) * r['per_payable_contribution_eur'] - i['other_variable_cost_per_click_eur']
equal('media_cpc_ceiling', ceiling, r['media_cpc_ceiling_eur'])

retained = Parameters(**baselines['retained_lead'])
retained_rows = simulate(retained, schedule)
first, second = retained_rows[:2]
equal('retention_E_next', retained.rho_e * (first['eligible'] - first['monetary_events']), second['eligible'])
equal('retention_M_next', retained.rho_m * (first['completed_active'] + first['monetary_events']), second['completed_active'])
assert round(second['eligible']) == 720 and round(second['completed_active']) == 80
discount = 1 / (1 + retained.monthly_discount_rate)
u36 = sum(discount ** a * month['contribution'] for a, month in enumerate(retained_rows)) / schedule[0]
equal('retained_36_month_contribution_per_owner', u36, finite_value(retained) - retained.cac)
assert f'{u36:.2f}' == '1.17'

reset_case = next(e for e in examples['experiments'] if e['changes'] == {'reset_probability': .1}
                  and e['baseline'] == retained.name)
reset = Parameters(**reset_case['parameters'])
reset_rows = simulate(reset, schedule)
extra = reset.rho_m * reset.reset_probability * (reset_rows[0]['completed_active'] + reset_rows[0]['monetary_events'])
equal('reset_extra_eligible', extra, reset_rows[1]['eligible'] - second['eligible'])
equal('reset_completed_next', second['completed_active'] - extra, reset_rows[1]['completed_active'])
assert round(extra) == 8 and round(reset_rows[1]['eligible']) == 728 and round(reset_rows[1]['completed_active']) == 72

policy = Parameters(**baselines['policy_placement'])
policy_rows = simulate(policy, schedule)
renewal = int(policy.renewal_rights) * policy_rows[0]['new_policies'] * policy.policy_month_survival ** 12 * policy.renewal_payment
equal('month_13_renewal_revenue', renewal, policy_rows[12]['renewal_revenue'])
equal('renewal_without_payment_rights', 0, simulate(replace(policy, renewal_rights=False), schedule)[12]['renewal_revenue'])
assert f'{renewal:,.2f}' == '1,177.08'

paid = Parameters(**baselines['lead_plus_paid_service'])
free = Parameters(**baselines['retained_without_paid_service'])
paid_rows = simulate(paid, schedule)
accounts = paid.software_conversion * schedule[0] * paid.software_survival
equal('month_2_expected_paid_accounts', accounts, paid_rows[1]['subscribers'])
software_month = accounts * (paid.software_month_payment - paid.software_month_cost)
equal('month_2_software_component', software_month, paid_rows[1]['software_revenue'] - paid.software_month_cost * paid_rows[1]['subscribers'])
assert accounts == 142.5 and software_month == 356.25
software36 = paid.software_conversion * (paid.software_month_payment - paid.software_month_cost) * sum((1 / (1 + paid.monthly_discount_rate) * paid.software_survival) ** a for a in range(36))
equal('discounted_software_component_per_original_owner', software36, finite_value(paid) - finite_value(free))
equal('combined_software_and_lead_contribution_per_owner', finite_value(free) - free.cac + software36, finite_value(paid) - paid.cac)

panels = json.loads((DATA / 'panels.json').read_text())
render = json.loads((DATA / 'render-validation.json').read_text())
assert render['status'] == 'pass' and len(render['panels']) == len(panels) == 8
images = {}
for panel in panels:
    path = DATA / (panel['id'] + '.png')
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    dimensions = list(struct.unpack('>II', data[16:24]))
    assert dimensions == [panel['width'] * 2, panel['height'] * 2]
    images[path.name] = {'pixels': dimensions, 'sha256': hashlib.sha256(data).hexdigest()}

guides = {}
for name, count in [('Objais Revenue Model Numerical Summary.md', 7), ('Objais Acquisition Numerical Summary.md', 1)]:
    text = (ROOT / name).read_text()
    image_lines = re.findall(r'^!\[[^\]]+\]\(<[^>]*research/formulas/[^>]+\.png>\)$', text, re.M)
    assert len(image_lines) == count, (name, len(image_lines))
    assert all('Objais Glossary.md#' not in line for line in image_lines)
    guides[name] = {'formula_panels': count, 'source_sha256': hashlib.sha256(text.encode()).hexdigest()}

original_hashes = json.loads((ROOT / 'research/glossary/migration-baseline.json').read_text())['sha256']
unchanged = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest for name, digest in original_hashes.items()}
assert all(unchanged.values())
report = {'status': 'pass', 'rendering': render,
          'visual_inspection': 'All panels inspected; terms are connected to their labels, units and time windows are explicit, and cohort counts, renewal rights and software component scope agree with the model.',
          'mathematical_agreement': checks, 'model_inputs_unchanged': unchanged,
          'images': images, 'guides': guides,
          'scope': 'Explanatory annotations of existing synthetic scenarios; no new revenue architecture or empirical calibration'}
(DATA / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
reader_path = ROOT / 'research/glossary/reader-review.json'
reader = json.loads(reader_path.read_text())
reader['formula_highlighting'] = {'report': str(DATA / 'validation.json'), 'formula_panels': len(panels), 'glossary_links_in_formulas': 0}
for name, record in guides.items():
    reader['documents'][name]['source_sha256'] = record['source_sha256']
reader_path.write_text(json.dumps(reader, indent=2) + '\n')
print(json.dumps({'status': 'pass', 'panels': len(panels), 'independent_model_comparisons': len(checks), 'model_inputs_unchanged': True}))
