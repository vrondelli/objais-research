import unittest
import random
import math
from dataclasses import replace
from revenue_model import (Parameters, Segment, simulate, simulate_segment,
                          simulate_market, cohort_value, finite_value)
from episodic_model import acquisition_cost, contacts_from_budget


class EpisodicModelTests(unittest.TestCase):
    def close(self, a, b):
        self.assertTrue(math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9),(a,b))

    def base(self, **changes):
        return replace(Segment('test',Parameters()),**changes)

    def test_old_scenarios_are_exact_special_cases(self):
        from revenue_model import scenarios
        for p in scenarios():
            s=Segment(p.name,p,contact_cost=p.cac,contacts_per_month=p.acquired_per_month)
            new=simulate_segment(s);old=simulate(p)
            for a,b in zip(new,old):
                for k in ['eligible','completed_active','monetary_events','new_policies',
                          'active_policies','renewal_events','subscribers','initial_revenue',
                          'renewal_revenue','software_revenue','revenue','variable_cost',
                          'acquisition_cost','contribution','cash_receipts','receivables']:
                    self.close(a[k],b[k])
            self.close(cohort_value(s,1000),finite_value(p)-p.cac)

    def test_need_request_and_acceptance_are_conditional_factors(self):
        r=simulate_segment(self.base(need_probability=.5,qualified_request_probability=.4,paid_acceptance=.25),1)[0]
        self.close(r['qualified_requests'],200);self.close(r['monetary_events'],50)

    def test_request_cost_includes_failed_requests(self):
        r=simulate_segment(self.base(qualified_request_probability=.5,paid_acceptance=0,request_cost=2),1)[0]
        self.close(r['monetary_events'],0);self.close(r['variable_cost'],1200)

    def test_age_schedule_means_two_need_months_per_year(self):
        p=replace(Parameters(),q=1,rho_e=1,rho_m=1,reset_probability=1)
        s=Segment('scheduled',p,contacts_by_month=(1000,)+(0,)*23,
                  need_age_profile=(1,0,0,0,0,0,1,0,0,0,0,0),paid_event_cap=2)
        r=simulate_segment(s,24)
        self.assertEqual([x['month'] for x in r if x['monetary_events']],[1,7,13,19])
        self.close(sum(x['monetary_events'] for x in r),4000)

    def test_calendar_schedule_is_distinct_from_cohort_age(self):
        p=replace(Parameters(),q=1,rho_e=1,rho_m=1,reset_probability=1)
        r=simulate_segment(Segment('calendar',p,need_calendar_profile=(1,0,0,0,0,0)),8)
        self.assertEqual([x['month'] for x in r if x['monetary_events']],[1,7])
        self.close(r[6]['monetary_events'],7000)

    def test_rolling_cap_applies_to_paths_not_only_mean(self):
        p=replace(Parameters(),q=.3,rho_e=1,rho_m=1,reset_probability=1)
        s=Segment('cap',p,contacts_by_month=(1000,)+(0,)*23,paid_event_cap=2)
        r=simulate_segment(s,24)
        self.assertLessEqual(sum(x['monetary_events'] for x in r[:12]),2000+1e-8)
        self.assertLessEqual(sum(x['monetary_events'] for x in r[12:]),2000+1e-8)
        # Independent binomial identity before any first-year history expires.
        expected=2-2*(.7**12)-12*.3*(.7**11)
        self.close(sum(x['monetary_events'] for x in r[:12]),1000*expected)

    def test_cap_rolls_without_resetting_customer_identity(self):
        p=replace(Parameters(),q=1,rho_e=1,rho_m=1,reset_probability=1)
        r=simulate_segment(Segment('cap',p,contacts_by_month=(1,)+(0,)*23,paid_event_cap=2),24)
        self.assertEqual([x['month'] for x in r if x['monetary_events']],[1,2,13,14])
        self.close(sum(x['acquired'] for x in r),1)

    def test_cooldown_is_independent_of_cap(self):
        p=replace(Parameters(),q=1,rho_e=1,rho_m=1,reset_probability=1)
        r=simulate_segment(Segment('cooldown',p,contacts_by_month=(1,)+(0,)*12,cooldown_months=6),13)
        self.assertEqual([x['month'] for x in r if x['monetary_events']],[1,7,13])

    def test_zero_cap_prevents_all_initial_fees(self):
        r=simulate_segment(self.base(paid_event_cap=0),12)
        self.close(sum(x['monetary_events'] for x in r),0)

    def test_dormant_owner_returns_without_being_acquired_again(self):
        p=replace(Parameters(),q=1,rho_e=0,rho_m=0)
        s=Segment('return',p,contacts_by_month=(1000,)+(0,)*11,
                  dormant_fraction_e=1,dormant_fraction_m=1,return_reset_probability=1,
                  return_age_profile=(0,0,0,0,0,0,1,0,0,0,0,0))
        r=simulate_segment(s,12)
        self.close(r[6]['returned'],1000);self.close(r[6]['monetary_events'],1000)
        self.close(r[6]['acquisition_cost'],0);self.close(sum(x['acquired'] for x in r),1000)
        self.close(r[5]['dormant'],1000)

    def test_return_without_new_rights_does_not_repay_completed_lead(self):
        p=replace(Parameters(),q=1,rho_m=0)
        r=simulate_segment(Segment('return',p,contacts_by_month=(1,)+(0,)*6,
                                  dormant_fraction_m=1,return_probability=1),7)
        self.close(sum(x['monetary_events'] for x in r),1)

    def test_return_preserves_recent_paid_event_cap(self):
        p=replace(Parameters(),q=1,rho_m=0)
        r=simulate_segment(Segment('return',p,contacts_by_month=(1,)+(0,)*11,
                                  dormant_fraction_m=1,return_probability=1,
                                  return_reset_probability=1,paid_event_cap=1),12)
        self.close(sum(x['monetary_events'] for x in r),1)

    def test_permanent_exit_is_absorbing(self):
        p=replace(Parameters(),q=1,rho_m=0)
        r=simulate_segment(Segment('exit',p,contacts_by_month=(1,)+(0,)*5,return_probability=1),6)
        self.close(sum(x['returned'] for x in r),0)
        self.close(r[-1]['permanently_exited'],1)

    def test_dormant_exit_and_reactivation_costs(self):
        p=replace(Parameters(),q=0,rho_e=0)
        s=Segment('cost',p,contacts_by_month=(1000,0),dormant_fraction_e=1,
                  return_probability=.5,dormant_exit_probability=.2,
                  dormant_month_cost=.1,reactivation_cost=2)
        r=simulate_segment(s,2)
        self.close(r[1]['returned'],400)
        self.close(r[1]['variable_cost'],400*.2+400*.1+400*2)

    def test_billing_and_policy_continue_while_owner_dormant(self):
        p=replace(Parameters(),event_basis='bound_policy',q=1,rho_m=0,
                  renewal_rights=True,policy_month_survival=1,software_conversion=1,software_survival=1)
        r=simulate_segment(Segment('clocks',p,contacts_by_month=(1,)+(0,)*12,dormant_fraction_m=1),13)
        self.close(r[12]['dormant'],1);self.close(r[12]['renewal_revenue'],15)
        self.close(r[12]['software_revenue'],3)

    def test_workflow_adoption_changes_cac_not_owner_counting(self):
        a=simulate_segment(self.base(contact_cost=2,adoption=.5),1)[0]
        b=simulate_segment(self.base(workflow='delegated',contact_cost=2,adoption=.1),1)[0]
        self.close(a['cac'],4);self.close(b['cac'],20)
        self.close(b['acquired'],100)

    def test_acquisition_curve_and_budget_inverse(self):
        s=self.base(adoption=.5,contact_cost=2,onboarding_cost=1,acquisition_curvature=.5)
        for n in [1,100,1000,2000]:
            cost=acquisition_cost(s,n,.5,1.4)
            self.close(contacts_from_budget(s,cost,.5,1.4),n)
        self.assertGreater(acquisition_cost(s,2000,.5)/1000,acquisition_cost(s,1000,.5)/500)

    def test_budget_scales_volume_and_unused_capacity_is_not_spent(self):
        s=self.base(adoption=.5,contact_cost=2,budgets_by_month=(4000,),monthly_contact_limit=1000)
        r=simulate_segment(s,1)[0]
        self.close(r['acquired'],500);self.close(r['unused_budget'],2000)

    def test_reachable_pool_stops_new_contacts_not_existing_revenue(self):
        p=replace(Parameters(),q=.1,rho_e=1,rho_m=1)
        r=simulate_segment(Segment('pool',p,reachable_contact_pool=1500),3)
        self.close(r[2]['contacts'],0);self.assertGreater(r[2]['monetary_events'],0)

    def test_capacity_reduces_paid_events_but_failed_request_cost_remains(self):
        r=simulate_segment(self.base(qualified_request_probability=1,request_cost=1,monthly_event_capacity=100),1)[0]
        self.close(r['monetary_events'],100);self.close(r['qualified_requests'],1000)
        self.close(r['capacity_unfilled_events'],900)

    def test_time_varying_acceptance_fee_and_competition(self):
        p=replace(Parameters(),q=1)
        s=Segment('profiles',p,acceptance_profile=(1,.5),fee_profile=(20,10),competition_profile=(1,2))
        a,b=simulate_segment(s,2)
        self.close(b['monetary_events'],500);self.close(b['initial_revenue'],4750)
        self.close(b['acquisition_cost'],2*a['acquisition_cost'])

    def test_random_state_conservation(self):
        rng=random.Random(72)
        for _ in range(8):
            p=replace(Parameters(),rho_e=rng.random(),rho_m=rng.random(),reset_probability=rng.random())
            s=Segment('conservation',p,dormant_fraction_e=rng.random(),dormant_fraction_m=rng.random(),
                      return_probability=rng.random(),dormant_exit_probability=rng.random(),
                      return_reset_probability=rng.random(),paid_event_cap=2)
            for r in simulate_segment(s,18):
                self.close(r['next_relationship']+r['permanently_exited'],r['cumulative_acquired'])

    def test_market_fixed_cost_once_and_cash_identity(self):
        result=simulate_market([self.base(),replace(self.base(),name='delegate',workflow='delegated')],12,1000)
        r=result['months']
        self.close(r[0]['operating_result'],2*(-2400)-1000)
        self.close(sum(x['operating_result'] for x in r)-r[-1]['cumulative_cash'],r[-1]['receivables'])

    def test_incompatible_currencies_and_duplicate_segments_rejected(self):
        a=self.base();b=replace(a,name='BR',economics=replace(a.economics,currency='BRL'))
        for ss in [[a,a],[a,b],[]]:
            with self.assertRaises(ValueError):simulate_market(ss)

    def test_invalid_configuration_is_rejected(self):
        for changes in [{'paid_event_cap':-1},{'cap_window_months':0},{'cooldown_months':-1},
                        {'adoption':1.1},{'need_age_profile':(1,1.1)},
                        {'reference_contacts':0},{'workflow':'dealer'},
                        {'contacts_by_month':(1,2)},{'budgets_by_month':(1,2)},
                        {'contact_cost':float('nan')},{'monthly_event_capacity':-1}]:
            with self.assertRaises(ValueError):simulate_segment(self.base(**changes),36)

    def test_no_adoption_still_consumes_marketing_budget(self):
        r=simulate_segment(self.base(adoption=0),1)[0]
        self.close(r['acquired'],0);self.close(r['acquisition_cost'],4000)
        self.assertIsNone(r['cac']);self.assertIsNone(cohort_value(self.base(adoption=0),1000))


if __name__=='__main__':unittest.main()
