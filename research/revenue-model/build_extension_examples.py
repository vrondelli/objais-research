"""Reproducible hypothetical examples for the episodic, segmented model."""
from pathlib import Path
from dataclasses import replace, asdict
import json,csv
from revenue_model import Parameters,Segment,simulate_market,cohort_value

ROOT=Path(__file__).resolve().parents[2]
D=Path(__file__).resolve().parent
inputs=json.loads((ROOT/'research/revenue-summary/numerical-examples.json').read_text())['baselines']
lead=Parameters(**inputs['lead'])
free=Parameters(**inputs['retained_without_paid_service'])
paid=Parameters(**inputs['lead_plus_paid_service'])
policy=Parameters(**inputs['policy_placement'])
twice=(1,0,0,0,0,0,1,0,0,0,0,0)
annual=(1,)+(0,)*11
base=Segment('One-off lead benchmark',lead)
occasional=Segment('Occasional returns; first fee only',lead,
                   contacts_per_month=2000,adoption=.5,contact_cost=2,
                   qualified_request_probability=.5,paid_acceptance=.2,
                   need_age_profile=twice,return_age_profile=twice,
                   dormant_fraction_e=1,dormant_fraction_m=1,
                   dormant_month_cost=.01,reactivation_cost=.2,
                   paid_event_cap=2,cooldown_months=6)
repeat=replace(occasional,name='Occasional returns; new payable enquiries',return_reset_probability=1)
future=Segment('Frequent free service; occasional insurance',free,
               need_age_profile=twice,paid_event_cap=2,cooldown_months=6)
cheap=replace(base,name='Lower CAC; flat cost; 2000 contacts',
              economics=replace(lead,cac=1),contact_cost=1,contacts_per_month=2000)
cases=[base,
       occasional,
       repeat,
       replace(repeat,name='Occasional returns; 2% dormant exit',dormant_exit_probability=.02),
       Segment('Direct use; 50% adoption',lead,contacts_per_month=2000,adoption=.5,contact_cost=2),
       Segment('Delegated use; 10% adoption',lead,workflow='delegated',contacts_per_month=2000,adoption=.1,contact_cost=2),
       future,
       replace(future,name='Paid service; 15% paid starts',economics=paid),
       replace(future,name='Paid service; 25% paid starts',economics=replace(paid,software_conversion=.25)),
       cheap,
       replace(cheap,name='Lower CAC; curved cost; 1000 contacts',contacts_per_month=1000,acquisition_curvature=.5),
       replace(cheap,name='Lower CAC; curved cost; 2000 contacts',acquisition_curvature=.5),
       Segment('Annual return; binding and renewal rights',policy,
               need_age_profile=annual,return_age_profile=annual,
               dormant_fraction_e=1,dormant_fraction_m=1,
               dormant_month_cost=.01,reactivation_cost=.2,
               paid_event_cap=1,cooldown_months=12),
       replace(base,name='Capacity limit; failed request costs',qualified_request_probability=.5,
               paid_acceptance=.2,request_cost=.1,monthly_event_capacity=50),
       Segment('Fixed budget; curved acquisition cost',lead,contacts_per_month=0,
               budgets_by_month=(4000,)*36,adoption=.5,contact_cost=2,acquisition_curvature=.5)]
summaries=[];monthly=[]
for i,s in enumerate(cases,1):
    market=simulate_market([s],36,1000)
    rows=market['months'];detail=market['segments'][s.name]
    contacts=detail[0]['contacts']
    summaries.append(dict(id=f'E{i}',name=s.name,parameters=asdict(s),
                          evidence='SYNTHETIC; no calibrated market assignment',
                          contacts_month1=contacts,acquired_month1=detail[0]['acquired'],
                          cac_month1=detail[0]['cac'],unit_net36=cohort_value(s,contacts),
                          operating36=sum(r['operating_result'] for r in rows),
                          cash36=rows[-1]['cumulative_cash'],receivables36=rows[-1]['receivables']))
    for r in detail:monthly.append(dict(case_id=f'E{i}',**r))
(D/'extension-examples.json').write_text(json.dumps(summaries,indent=2))
with (D/'extension-monthly.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(monthly[0]));w.writeheader();w.writerows(monthly)
with (D/'extension-results.csv').open('w',newline='',encoding='utf-8-sig') as f:
    fields=[k for k in summaries[0] if k!='parameters']
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    w.writerows({k:r[k] for k in fields} for r in summaries)
print(json.dumps([{k:r[k] for k in ['id','name','cac_month1','unit_net36','operating36']} for r in summaries],indent=2))
