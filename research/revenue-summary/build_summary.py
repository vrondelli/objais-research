"""Reproducible plain-language, one-factor sensitivity summary.

All example inputs are synthetic. The original model and market comparison
are read, not modified. Each experiment changes only its named parameter.
"""
from pathlib import Path
from dataclasses import replace,asdict
import sys,json,csv,math
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/revenue-model'))
from revenue_model import Parameters,finite_value,simulate

prior=json.loads((ROOT/'research/market-model/cases.json').read_text())
lead=replace(Parameters(**prior[0]['parameters']),name='One-off paid-lead arrangement')
free=replace(Parameters(**prior[5]['parameters']),name='Retained service without software payment')
paid=replace(Parameters(**prior[8]['parameters']),name='Lead plus optional paid-tool arrangement')
placement=replace(Parameters(**prior[9]['parameters']),name='Policy binding with renewal rights')
retained=replace(lead,name='Retained paid-lead arrangement',rho_e=.8,rho_m=.8)
unit=lambda p:finite_value(p)-p.cac
money=lambda v:f'€{abs(v):,.2f}'
signed=lambda v:('+' if v>=0 else '−')+money(v)
records=[]

def case(label,base,changes):
 p=replace(base,**changes);r=dict(label=label,baseline=base.name,changes=changes,parameters=asdict(p),unit_before=unit(base),unit_after=unit(p),unit_change=unit(p)-unit(base))
 records.append(r);return r

common=[
 ('Acquisition cost','20% lower CAC','cac',.8),
 ('Paid-event probability','20% higher paid-event probability','q',1.2),
 ('Initial payment','20% higher initial payment','initial_payment',1.2),
 ('Eligible-user cost','20% lower cost before monetisation','eligible_month_cost',.8),
 ('Post-event user cost','20% lower cost after monetisation','completed_month_cost',.8),
 ('Processing cost','20% lower cost per paid event','event_cost',.8),
 ('Payment reversals','20% lower reversal fraction','reversal_fraction',.8),
]
common_rows=[]
for factor,label,key,mult in common:
 comparisons=[case(label,p,{key:getattr(p,key)*mult}) for p in [lead,retained,placement,paid]]
 common_rows.append((factor,label,*comparisons))
software=[]
for label,key,new in [('Paid starts: 15% to 18%','software_conversion',.18),('Monthly net payment: €3 to €3.60','software_month_payment',3.6),('Billed monthly continuation: 95% to 96%','software_survival',.96),('Billed monthly cost: €0.50 to €0.40','software_month_cost',.4)]:
 software.append(case(label,paid,{key:new}))
pre=case('Pre-event continuation: 0% to 80%',lead,{'rho_e':.8})
post=case('Post-event continuation: 0% to 80%',lead,{'rho_m':.8})
paid_pre=case('Paid-tool example pre-event continuation: 90% to 92%',paid,{'rho_e':.92})
paid_post=case('Paid-tool example post-event continuation: 95% to 96%',paid,{'rho_m':.96})
paid_bill=case('Billed monthly continuation: 95% to 90%',paid,{'software_survival':.9})
repeat_lead=case('New paid eligibility: 0% to 10%',retained,{'reset_probability':.1})
repeat_free=case('New paid eligibility: 0% to 10%',free,{'reset_probability':.1})
conversion_rows=[case(f'Paid-tool starts: {k:.0%}',free,{'software_conversion':k}) for k in [0,.05,.10,.15]]
without_renewal=case('Binding without renewal rights',placement,{'renewal_rights':False})
better_survival=case('Policy monthly survival: 98% to 99%',placement,{'policy_month_survival':.99})
double_renewal=case('Renewal payment: €15 to €30',placement,{'renewal_payment':30})
horizons=[case(f'Horizon: {h} months',paid,{'horizon':h}) for h in [12,24,36]]
discounts=[case(f'Monthly discount: {i:.0%}',paid,{'monthly_discount_rate':i}) for i in [0,.01,.02]]
cash_rows=[]
for lag in [0,1,3]:
 p=replace(paid,cash_lag=lag);rows=simulate(p)
 cash_rows.append(dict(lag=lag,operating36=sum(r['operating_result'] for r in rows),cash36=rows[-1]['cumulative_cash'],receivables36=rows[-1]['receivables'],unit=unit(p)))

base_sub_gain=unit(replace(free,software_conversion=1))-unit(free)
required_k=-unit(free)/base_sub_gain
cal0=simulate(free);cal1=simulate(replace(free,software_conversion=1))
op0=sum(r['operating_result'] for r in cal0);op1=sum(r['operating_result'] for r in cal1)
op_k=-op0/(op1-op0);cash_k=-cal0[-1]['cumulative_cash']/(cal1[-1]['cumulative_cash']-cal0[-1]['cumulative_cash'])
checks=[]
for p,index in [(lead,0),(free,5),(paid,8),(placement,9)]:checks.append(math.isclose(unit(p),prior[index]['unit_net'],abs_tol=1e-10))
checks.append(math.isclose(unit(retained),prior[3]['unit_net'],abs_tol=1e-10))
for r in records:
 changed={k for k in asdict(Parameters(**r['parameters'])) if asdict(Parameters(**r['parameters']))[k]!=asdict(next(p for p in [lead,paid,free,placement,retained] if p.name==r['baseline'] and math.isclose(unit(p),r['unit_before'],abs_tol=1e-10)))[k]}
 checks.append(changed.issubset(set(r['changes'])))
checks.append(math.isclose(common_rows[0][2]['unit_change'],.8,abs_tol=1e-10))
checks.append(math.isclose(common_rows[1][2]['unit_change'],.36,abs_tol=1e-10))
checks.append(math.isclose(common_rows[2][2]['unit_change'],.38,abs_tol=1e-10))
checks.append(math.isclose(unit(replace(free,software_conversion=required_k)),0,abs_tol=1e-9))
checks.append(math.isclose(unit(replace(lead,initial_payment=(1+(4+.2)/.1)/.95)),0,abs_tol=1e-9))
checks.append(all(math.isclose(r['operating36']-r['cash36'],r['receivables36'],abs_tol=1e-7) for r in cash_rows))
checks.append(all(math.isclose(r['unit'],unit(paid),abs_tol=1e-10) for r in cash_rows))
assert all(checks)

# Follow one cohort through two months so the explanation shows the mechanism.
walkthrough_parameters=replace(lead,rho_e=.8,rho_m=.8,fixed_month_cost=0)
walkthrough=simulate(walkthrough_parameters,[1000]+[0]*35)
assert math.isclose(walkthrough[0]['revenue'],1900,abs_tol=1e-9)
assert math.isclose(walkthrough[0]['contribution'],-2400,abs_tol=1e-9)
assert math.isclose(walkthrough[1]['eligible'],720,abs_tol=1e-9)
assert math.isclose(walkthrough[1]['completed_active'],80,abs_tol=1e-9)
assert math.isclose(walkthrough[1]['monetary_events'],72,abs_tol=1e-9)
assert math.isclose(walkthrough[1]['variable_cost'],240,abs_tol=1e-9)
assert math.isclose(walkthrough[1]['contribution'],1128,abs_tol=1e-9)

from concise_summary import compose
from diagrams import export_diagrams
body=compose(globals())
export_diagrams(D/'diagrams')
(ROOT/'Objais Revenue Model Numerical Summary.md').write_text(body,encoding='utf-8')
(D/'numerical-examples.json').write_text(json.dumps({'evidence':'All inputs synthetic; one-factor effects hold all other parameters fixed','scope':'Current Objais categories and contracts, improvements within existing scope, and optional future services/categories/countries. Examples represent payment arrangements, not calibrated markets. Professional accounts need adapted units and event counts.','baselines':{'lead':asdict(lead),'retained_lead':asdict(retained),'retained_without_paid_service':asdict(free),'lead_plus_paid_service':asdict(paid),'policy_placement':asdict(placement)},'model_walkthrough':{'parameters':asdict(walkthrough_parameters),'first_two_months':walkthrough[:2],'unit_net36':unit(walkthrough_parameters)},'experiments':records,'cash_comparisons':cash_rows,'break_even':{'customer_paid_starts':required_k,'calendar_operating_paid_starts':op_k,'calendar_cash_paid_starts':cash_k}},indent=2))
with (D/'factor-changes.csv').open('w',newline='',encoding='utf-8-sig') as f:
 keys=['label','baseline','changes','unit_before','unit_after','unit_change'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
 for r in records:w.writerow({k:json.dumps(r[k]) if k=='changes' else r[k] for k in keys})
(D/'validation.json').write_text(json.dumps({'status':'pass','checks':len(checks),'walkthrough_checks':7,'one_factor_experiments':len(records),'cash_comparisons':len(cash_rows),'empirical_calibration':False},indent=2))
print(json.dumps({'file':str(ROOT/'Objais Revenue Model Numerical Summary.md'),'words':len(body.split()),'experiments':len(records),'checks':len(checks)},indent=2))
