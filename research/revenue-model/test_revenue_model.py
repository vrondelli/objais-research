import unittest,random,math
from dataclasses import replace
from revenue_model import Parameters,simulate,finite_value,infinite_value,scenarios

class FormalModelTests(unittest.TestCase):
 def close(self,a,b,tol=1e-8):self.assertTrue(math.isclose(a,b,rel_tol=tol,abs_tol=tol),(a,b))
 def test_single_visit_closed_identity(self):
  p=Parameters();self.close(finite_value(p),p.q*p.event_margin-p.eligible_month_cost)
 def test_post_event_retention_no_extra_leads(self):
  a=Parameters();b=replace(a,rho_m=.95)
  ra=simulate(a,[100]+[0]*35);rb=simulate(b,[100]+[0]*35)
  self.close(sum(r['monetary_events'] for r in ra),sum(r['monetary_events'] for r in rb))
  self.assertLess(finite_value(b),finite_value(a))
 def test_one_episode_ceiling_and_exact_probability(self):
  p=replace(Parameters(),horizon=2000,rho_e=.9,rho_m=.8)
  rs=simulate(p,[1]+[0]*1999);total=sum(r['monetary_events'] for r in rs)
  self.close(total,p.q/(1-p.rho_e*(1-p.q)));self.assertLessEqual(total,1+1e-10)
 def test_pre_event_retention_changes_conversion(self):
  a=Parameters();b=replace(a,rho_e=.8)
  self.assertGreater(sum(x['monetary_events'] for x in simulate(b)),sum(x['monetary_events'] for x in simulate(a)))
 def test_recurrence_conservation_and_nonnegative_states(self):
  rng=random.Random(41)
  for _ in range(30):
   p=replace(Parameters(),q=rng.random(),rho_e=rng.random(),rho_m=rng.random(),reset_probability=rng.random())
   rs=simulate(p)
   for r in rs:
    self.close(r['eligible']+r['completed_active']-r['churned'],r['next_active'])
    self.assertGreaterEqual(r['eligible'],0);self.assertGreaterEqual(r['completed_active'],0)
    self.assertLessEqual(r['monetary_events'],r['eligible']+1e-9)
 def test_closed_resolvent_matches_cohort_sum(self):
  rng=random.Random(13)
  for _ in range(25):
   p=replace(Parameters(),q=rng.uniform(.01,.8),rho_e=rng.uniform(0,.9),rho_m=rng.uniform(0,.9),reset_probability=rng.random(),eligible_month_cost=rng.random(),completed_month_cost=rng.random())
   self.close(finite_value(p,600),infinite_value(p))
 def test_closed_one_lead_formula(self):
  p=replace(Parameters(),rho_e=.8,rho_m=.75);d=p.delta;den=1-d*p.rho_e*(1-p.q)
  expected=(p.event_margin*p.q-p.eligible_month_cost-p.completed_month_cost*d*p.rho_m*p.q/(1-d*p.rho_m))/den
  self.close(expected,infinite_value(p))
 def test_derivative_post_event_retention(self):
  p=replace(Parameters(),rho_e=.8,rho_m=.7);h=1e-5
  actual=(infinite_value(replace(p,rho_m=p.rho_m+h))-infinite_value(replace(p,rho_m=p.rho_m-h)))/(2*h)
  d=p.delta;expected=-p.completed_month_cost*d*p.q/((1-d*p.rho_m)**2*(1-d*p.rho_e*(1-p.q)))
  self.close(actual,expected,tol=1e-7)
 def test_zero_post_event_cost_retention_neutral(self):
  p=replace(Parameters(),completed_month_cost=0,rho_e=.8)
  self.close(infinite_value(replace(p,rho_m=.1)),infinite_value(replace(p,rho_m=.9)))
 def test_genuine_reset_can_enable_another_event(self):
  p=replace(Parameters(),horizon=4,q=1,rho_e=1,rho_m=1,reset_probability=1)
  r=simulate(p,[1,0,0,0]);self.close(sum(x['monetary_events'] for x in r),4)
 def test_zero_conversion_no_new_event_revenue(self):
  p=replace(Parameters(),q=0,rho_e=.8,rho_m=.8)
  r=simulate(p);self.close(sum(x['initial_revenue'] for x in r),0)
 def test_no_acquisition_no_population_or_revenue(self):
  p=Parameters();r=simulate(p,[0]*36)
  self.close(sum(x['revenue'] for x in r),0);self.close(sum(x['acquisition_cost'] for x in r),0)
 def test_stop_acquisition_keeps_existing_cohort_cash_and_events(self):
  p=replace(Parameters(),rho_e=.8,rho_m=.8)
  r=simulate(p,[100]+[0]*35)
  self.assertGreater(r[1]['monetary_events'],0);self.assertGreater(r[1]['cash_receipts'],0);self.close(r[1]['acquisition_cost'],0)
 def test_renewals_begin_at_month_13(self):
  p=replace(Parameters(),event_basis='bound_policy',q=1,renewal_rights=True,policy_month_survival=1,initial_payment=30)
  r=simulate(p,[1]+[0]*35)
  self.assertEqual([x['month'] for x in r if x['renewal_revenue']>0],[13,25]);self.close(r[12]['renewal_revenue'],15)
 def test_no_renewal_rights_zero_renewal_revenue(self):
  p=replace(Parameters(),event_basis='bound_policy',q=1,renewal_rights=False)
  self.close(sum(x['renewal_revenue'] for x in simulate(p)),0)
 def test_policy_count_renewal_not_an_extra_policy(self):
  p=replace(Parameters(),event_basis='bound_policy',q=1,renewal_rights=True,policy_month_survival=1)
  r=simulate(p,[1]+[0]*35)
  self.assertTrue(all(x['active_policies']==1 for x in r))
 def test_policy_and_subscription_resolvents(self):
  for p in scenarios():self.close(finite_value(p,1200),infinite_value(p))
 def test_receivable_and_cash_identity(self):
  for lag in [0,1,7,50]:
   p=replace(Parameters(),cash_lag=lag);rs=simulate(p);previous=0
   for r in rs:self.close(r['receivables'],previous+r['revenue']-r['cash_receipts']);previous=r['receivables']
   self.close(sum(x['revenue'] for x in rs)-sum(x['cash_receipts'] for x in rs),rs[-1]['receivables'])
 def test_cac_charged_once_across_streams(self):
  p=replace(Parameters(),software_conversion=.05,event_basis='bound_policy',renewal_rights=True)
  rs=simulate(p,[1]+[0]*35);self.close(sum(x['acquisition_cost'] for x in rs),p.cac)
 def test_cash_delay_preserves_earned_revenue(self):
  a=Parameters();b=replace(a,cash_lag=12)
  self.close(sum(x['revenue'] for x in simulate(a)),sum(x['revenue'] for x in simulate(b)))
  self.assertNotEqual(sum(x['cash_surplus'] for x in simulate(a)),sum(x['cash_surplus'] for x in simulate(b)))
 def test_invalid_inputs_and_rights_rejected(self):
  for change in [{'q':1.1},{'rho_e':-.1},{'initial_payment':-1},{'cash_lag':-1},{'renewal_rights':True}]:
   with self.assertRaises(ValueError):simulate(replace(Parameters(),**change))
 def test_divergent_boundary_is_explicit(self):
  p=replace(Parameters(),rho_e=1,rho_m=1,q=.1,monthly_discount_rate=0)
  with self.assertRaises(ValueError):infinite_value(p)
  self.assertTrue(math.isfinite(finite_value(p)))

if __name__=='__main__':unittest.main(verbosity=2)
