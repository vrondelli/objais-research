"""Render the concise guide from the existing validated numerical examples."""
from pathlib import Path
import re, json
from diagrams import diagram


def compose(c):
    unit, signed, money = c['unit'], c['signed'], c['money']
    root = c['ROOT']
    body = (Path(__file__).parent / 'summary-template.md').read_text(encoding='utf-8')
    values = {
        'GLOSSARY_PATH': (root / 'Objais Glossary.md').as_posix(),
        'PAYMENT_FORMULA_PATH': (root / 'research/formulas/payment-chance.png').as_posix(),
        'CONTRIBUTION_FORMULA_PATH': (root / 'research/formulas/owner-contribution.png').as_posix(),
        'RETENTION_FORMULA_PATH': (root / 'research/formulas/retention-states.png').as_posix(),
        'RETAINED_VALUE_FORMULA_PATH': (root / 'research/formulas/retained-contribution.png').as_posix(),
        'RESET_FORMULA_PATH': (root / 'research/formulas/repeat-eligibility.png').as_posix(),
        'RENEWAL_FORMULA_PATH': (root / 'research/formulas/policy-renewal.png').as_posix(),
        'SOFTWARE_FORMULA_PATH': (root / 'research/formulas/paid-software.png').as_posix(),
        'SOFTWARE_COMPONENT': signed(unit(c['paid']) - unit(c['free'])),
        'FREE_SERVICE_UNIT': signed(unit(c['free'])),
        'ACTORS': diagram('actors').strip(),
        'EVENTS': diagram('events').strip(),
        'STATES': diagram('opportunity-states').strip(),
        'CLOCKS': diagram('independent-clocks').strip(),
        'CASH': diagram('cash').strip(),
        'SCOPE': diagram('scope').strip(),
        'LEAD_UNIT': signed(unit(c['lead'])),
        'RETAINED_UNIT': signed(unit(c['retained'])),
        'POST_UNIT': signed(c['post']['unit_after']),
        'RESET_UNIT': signed(c['repeat_lead']['unit_after']),
        'POLICY_UNIT': signed(unit(c['placement'])),
        'PAID_UNIT': signed(unit(c['paid'])),
        'NO_RENEWAL_UNIT': signed(c['without_renewal']['unit_after']),
        'POLICY_SURVIVAL_UNIT': signed(c['better_survival']['unit_after']),
        'SOFTWARE_ROWS': '\n'.join(f"| {r['parameters']['software_conversion']:.0%} | **{signed(r['unit_after'])}** |" for r in c['conversion_rows']),
        'CUSTOMER_PAID_THRESHOLD': f"{c['required_k']:.1%}",
        'OPERATING_PAID_THRESHOLD': f"{c['op_k']:.2%}",
        'CASH_PAID_THRESHOLD': f"{c['cash_k']:.2%}",
        'PAID_START_GAIN': signed(c['software'][0]['unit_change']),
        'PRICE_GAIN': signed(c['software'][1]['unit_change']),
        'BILL_GAIN': signed(c['software'][2]['unit_change']),
        'BILL_DOWN_UNIT': signed(c['paid_bill']['unit_after']),
        'HORIZON_TWELVE': signed(c['horizons'][0]['unit_after']),
        'CASH_LAG_ONE': signed(c['cash_rows'][1]['cash36']),
        'CASH_LAG_THREE': signed(c['cash_rows'][2]['cash36']),
        'RECEIVABLES_THREE': money(c['cash_rows'][2]['receivables36']),
        'GALLERY_PATH': (root / 'Objais Revenue Model Diagrams.html').as_posix(),
        'FORMAL_PATH': (root / 'Objais Revenue Model.tex').as_posix(),
        'NUMERICAL_PATH': (root / 'research/revenue-summary/numerical-examples.json').as_posix(),
        'FACTORS_PATH': (root / 'research/revenue-summary/factor-changes.csv').as_posix(),
    }
    labels = [
        'CAC −20%', 'Paid-event probability +20%', 'Initial fee +20%',
        'E service cost −20%', 'M service cost −20%',
        'Processing cost −20%', 'Reversal fraction −20%',
    ]
    values['SENSITIVITY_ROWS'] = '\n'.join(
        '| ' + label + ' | ' + ' | '.join(signed(r['unit_change']) for r in row[2:]) + ' |'
        for label, row in zip(labels, c['common_rows'])
    )
    company = []
    for label, p in [('One-off lead', c['lead']), ('Retained lead', c['retained']),
                     ('Policy + renewals', c['placement']), ('Lead + software', c['paid'])]:
        rows = c['simulate'](p)
        company.append(f"| {label} | {signed(unit(p))} | "
                       f"{signed(sum(r['operating_result'] for r in rows))} | "
                       f"{signed(rows[-1]['cumulative_cash'])} |")
    values['COMPANY_ROWS'] = '\n'.join(company)
    advanced = json.loads((root / 'research/revenue-model/extension-examples.json').read_text())
    aliases = {'EPISODIC_FIRST':2,'EPISODIC_REPEAT':3,'EPISODIC_LOSS':4,
               'DIRECT_UNIT':5,'DELEGATED_UNIT':6,'EPISODIC_FREE':7,
               'EPISODIC_PAID15':8,'EPISODIC_PAID25':9}
    for key, case_id in aliases.items():
        values[key] = signed(advanced[case_id-1]['unit_net36'])
    values['EXTENSION_PATH'] = (root / 'research/revenue-model/extension-examples.json').as_posix()
    for key, value in values.items():
        body = body.replace('@' + key + '@', value)
    assert not re.search(r'@[A-Z_]+@', body), 'Unresolved template value'
    return body
