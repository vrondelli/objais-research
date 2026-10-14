"""Expected-value revenue model. All bundled numerical examples are synthetic.

Month starts: add newly acquired owners; compute one accepted monetary event
per eligible owner in expectation; bill software and policy fees; incur costs.
Month ends: retain owners and reset eligibility only for a genuine new event.
The two opportunity states are independent of policy and software continuation.
"""
from dataclasses import dataclass, replace, asdict
from math import isfinite
from typing import Sequence
import json, csv
from pathlib import Path
from episodic_model import Segment, simulate_segment, simulate_market, cohort_value

@dataclass(frozen=True)
class Parameters:
    name: str = 'Illustrative one-visit lead sales'
    currency: str = 'EUR'
    event_basis: str = 'accepted_lead'
    horizon: int = 36
    acquired_per_month: float = 1000
    cac: float = 4
    q: float = .10
    rho_e: float = 0
    rho_m: float = 0
    reset_probability: float = 0
    initial_payment: float = 20
    reversal_fraction: float = .05
    event_cost: float = 1
    eligible_month_cost: float = .20
    completed_month_cost: float = .30
    software_conversion: float = 0
    software_survival: float = .95
    software_month_payment: float = 3
    software_month_cost: float = .50
    renewal_rights: bool = False
    policy_month_survival: float = .98
    renewal_interval: int = 12
    renewal_payment: float = 15
    policy_month_cost: float = 0
    fixed_month_cost: float = 1000
    cash_lag: int = 1
    monthly_discount_rate: float = .01

    def validate(self):
        for k in ['q','rho_e','rho_m','reset_probability','reversal_fraction','software_conversion','software_survival','policy_month_survival']:
            v=getattr(self,k)
            if not isfinite(v) or not 0<=v<=1:raise ValueError(f'{k} must be a probability in [0,1]')
        for k in ['acquired_per_month','cac','initial_payment','event_cost','eligible_month_cost','completed_month_cost','software_month_payment','software_month_cost','renewal_payment','policy_month_cost','fixed_month_cost','monthly_discount_rate']:
            v=getattr(self,k)
            if not isfinite(v) or v<0:raise ValueError(f'{k} must be finite and nonnegative')
        if self.event_basis not in ['accepted_lead','bound_policy']:raise ValueError('Unsupported monetary trigger')
        if self.renewal_rights and self.event_basis!='bound_policy':raise ValueError('Lead-only events do not establish renewal rights')
        for k,lower in [('horizon',1),('cash_lag',0),('renewal_interval',1)]:
            v=getattr(self,k)
            if type(v) is not int or v<lower:raise ValueError(f'{k} must be an integer >= {lower}')

    @property
    def delta(self):return 1/(1+self.monthly_discount_rate)

    @property
    def event_margin(self):return self.initial_payment*(1-self.reversal_fraction)-self.event_cost

    def transition(self):
        r=self.reset_probability;q=self.q;re=self.rho_e;rm=self.rho_m
        return ((re*(1-q)+rm*r*q,rm*r),(rm*(1-r)*q,rm*(1-r)))


def simulate(p: Parameters, acquisitions: Sequence[float]|None=None):
    p.validate()
    arrivals=list(acquisitions) if acquisitions is not None else [p.acquired_per_month]*p.horizon
    if len(arrivals)!=p.horizon or any(not isfinite(x) or x<0 for x in arrivals):raise ValueError('Acquisitions must be nonnegative, finite and match the horizon')
    # State before new acquisition, by original acquired-owner cohort.
    cohorts=[];policy_births=[];subscribers=0.;active_policies=0.;rows=[];receivable=0.;cumulative_cash=0.
    T=p.transition()
    for t,n in enumerate(arrivals):
        if n>0:cohorts.append({'birth':t,'n':n,'e':n,'m':0.})
        e=sum(c['e'] for c in cohorts);m=sum(c['m'] for c in cohorts)
        event=sum(p.q*c['e'] for c in cohorts)
        initial=event*p.initial_payment*(1-p.reversal_fraction)
        new_policies=event if p.event_basis=='bound_policy' else 0.
        policy_births.append(new_policies)
        active_policies=p.policy_month_survival*active_policies+new_policies
        renewal_count=sum(b*p.policy_month_survival**(t-c) for c,b in enumerate(policy_births) if t>c and (t-c)%p.renewal_interval==0)
        renewal=renewal_count*p.renewal_payment if p.renewal_rights else 0.
        subscribers=p.software_survival*subscribers+n*p.software_conversion
        software=subscribers*p.software_month_payment
        revenue=initial+renewal+software
        variable=e*p.eligible_month_cost+m*p.completed_month_cost+event*p.event_cost+subscribers*p.software_month_cost+active_policies*p.policy_month_cost
        acquisition_cost=n*p.cac
        contribution=revenue-variable-acquisition_cost
        operating=contribution-p.fixed_month_cost
        receipts=revenue if p.cash_lag==0 else (rows[t-p.cash_lag]['revenue'] if t>=p.cash_lag else 0.)
        # Simplified example: immediate net invoicing, no bad debt or late credits,
        # one collection lag for all streams; costs paid in the month incurred.
        receivable+=revenue-receipts
        cash_surplus=receipts-variable-acquisition_cost-p.fixed_month_cost
        cumulative_cash+=cash_surplus
        churn=0.
        for c in cohorts:
            ce,cm=c['e'],c['m'];paid=p.q*ce
            churn+=(1-p.rho_e)*(ce-paid)+(1-p.rho_m)*(cm+paid)
            c['e'],c['m']=T[0][0]*ce+T[0][1]*cm,T[1][0]*ce+T[1][1]*cm
        rows.append(dict(month=t+1,acquired=n,eligible=e,completed_active=m,monetary_events=event,new_policies=new_policies,active_policies=active_policies,renewal_events=renewal_count if p.renewal_rights else 0.,subscribers=subscribers,initial_revenue=initial,renewal_revenue=renewal,software_revenue=software,revenue=revenue,variable_cost=variable,acquisition_cost=acquisition_cost,contribution=contribution,fixed_cost=p.fixed_month_cost,operating_result=operating,cash_receipts=receipts,receivables=receivable,cash_surplus=cash_surplus,cumulative_cash=cumulative_cash,churned=churn,next_active=sum(c['e']+c['m'] for c in cohorts)))
    return rows


def infinite_value(p: Parameters):
    """Discounted gross contribution per acquired owner, excluding CAC/fixed cost.

    The two-state resolvent plus independent subscription and policy cohorts.
    Conditions are explicitly checked; use finite_value at divergent boundaries.
    """
    p.validate();d=p.delta;T=p.transition()
    # Inverse of I-dT applied to the initial eligible state (1,0).
    a=1-d*T[0][0];b=-d*T[0][1];c=-d*T[1][0];z=1-d*T[1][1];det=a*z-b*c
    if det<=1e-12 or a<=0 or z<=0:raise ValueError('Opportunity-state discounted sum is not convergent')
    es=z/det;ms=-c/det
    value=p.event_margin*p.q*es-p.eligible_month_cost*es-p.completed_month_cost*ms
    if p.software_conversion:
        if 1-d*p.software_survival<=1e-12:raise ValueError('Subscription discounted sum is not convergent')
        value+=p.software_conversion*(p.software_month_payment-p.software_month_cost)/(1-d*p.software_survival)
    if p.event_basis=='bound_policy':
        ds=d*p.policy_month_survival
        if (p.policy_month_cost or (p.renewal_rights and p.renewal_payment)) and 1-ds<=1e-12:raise ValueError('Policy discounted sum is not convergent')
        policy_value=0.
        if p.policy_month_cost:policy_value-=p.policy_month_cost/(1-ds)
        if p.renewal_rights and p.renewal_payment:
            u=ds**p.renewal_interval;policy_value+=p.renewal_payment*u/(1-u)
        value+=p.q*es*policy_value
    return value


def finite_value(p: Parameters, horizon: int|None=None):
    h=horizon or p.horizon
    pp=replace(p,horizon=h,cac=0,fixed_month_cost=0)
    r=simulate(pp,[1]+[0]*(h-1))
    return sum(p.delta**i*(x['revenue']-x['variable_cost']) for i,x in enumerate(r))


def scenarios():
    b=Parameters()
    return [b,
      replace(b,name='Retain after first lead only',rho_m=.8),
      replace(b,name='Retain before and after first lead',rho_e=.8,rho_m=.8),
      replace(b,name='New eligible opportunities',rho_e=.8,rho_m=.8,reset_probability=.1),
      replace(b,name='Paid tools with post-lead retention',rho_m=.8,software_conversion=.05),
      replace(b,name='Policy commission and renewal hypothesis',event_basis='bound_policy',initial_payment=30,reversal_fraction=0,renewal_rights=True,policy_month_cost=.1)]


def export(out: Path):
    out.mkdir(exist_ok=True,parents=True);summary=[];allrows=[]
    for i,p in enumerate(scenarios(),1):
        rows=simulate(p)
        v=finite_value(p)
        inf=infinite_value(p)
        summary.append(dict(scenario_id=f'S{i}',name=p.name,currency=p.currency,evidence_status='ILLUSTRATIVE ASSUMPTIONS; NOT OBJAIS DATA',horizon=p.horizon,revenue_36=sum(r['revenue'] for r in rows),contribution_36=sum(r['contribution'] for r in rows),operating_result_36=sum(r['operating_result'] for r in rows),cash_surplus_36=sum(r['cash_surplus'] for r in rows),receivables_36=rows[-1]['receivables'],ltv_36_before_cac=v,ltv_infinite_before_cac=inf,unit_value_36_after_cac=v-p.cac,break_even_cac_36=v,parameters=asdict(p)))
        for r in rows:allrows.append(dict(scenario_id=f'S{i}',**r))
    (out/'scenarios.json').write_text(json.dumps(summary,indent=2))
    with (out/'monthly-results.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)
    with (out/'scenario-results.csv').open('w',newline='',encoding='utf-8-sig') as f:
        headers=[k for k in summary[0] if k!='parameters'];w=csv.DictWriter(f,fieldnames=headers);w.writeheader();w.writerows({k:v for k,v in r.items() if k!='parameters'} for r in summary)
    print(json.dumps([{k:r[k] for k in ['scenario_id','name','ltv_36_before_cac','ltv_infinite_before_cac','unit_value_36_after_cac']} for r in summary],indent=2))

if __name__=='__main__':export(Path(__file__).resolve().parent)
