"""Finite expected-value model of episodic demand and segmented acquisition.

States preserve the original owner/cohort and paid-event history. All example
inputs are hypothetical. Profiles repeat at their explicit supplied length.
"""
from dataclasses import dataclass, replace
from collections import defaultdict
from math import isfinite, sqrt
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from revenue_model import Parameters


@dataclass(frozen=True)
class Segment:
    name: str
    economics: 'Parameters'
    workflow: str = 'direct'
    contacts_per_month: float = 1000
    contacts_by_month: tuple[float, ...] = ()
    budgets_by_month: tuple[float, ...] = ()
    adoption: float = 1
    adoption_profile: tuple[float, ...] = ()
    contact_cost: float = 4
    onboarding_cost: float = 0
    acquisition_curvature: float = 0
    reference_contacts: float = 1000
    competition_profile: tuple[float, ...] = ()
    monthly_contact_limit: float | None = None
    reachable_contact_pool: float | None = None
    need_probability: float = 1
    need_age_profile: tuple[float, ...] = ()
    need_calendar_profile: tuple[float, ...] = ()
    qualified_request_probability: float | None = None
    paid_acceptance: float = 1
    acceptance_profile: tuple[float, ...] = ()
    fee_profile: tuple[float, ...] = ()
    request_cost: float = 0
    initial_active_fraction: float = 1
    dormant_fraction_e: float = 0
    dormant_fraction_m: float = 0
    return_probability: float = 0
    return_age_profile: tuple[float, ...] = ()
    return_reset_probability: float = 0
    dormant_exit_probability: float = 0
    dormant_month_cost: float = 0
    reactivation_cost: float = 0
    paid_event_cap: int | None = None
    cap_window_months: int = 12
    cooldown_months: int = 0
    monthly_event_capacity: float | None = None

    def validate(self, horizon):
        self.economics.validate()
        if type(horizon) is not int or horizon < 1:
            raise ValueError('Positive integer horizon required')
        if not self.name or self.workflow not in ('direct', 'delegated'):
            raise ValueError('Name and direct/delegated workflow required')
        probabilities = ['adoption', 'need_probability', 'paid_acceptance',
                         'initial_active_fraction', 'dormant_fraction_e',
                         'dormant_fraction_m', 'return_probability',
                         'return_reset_probability', 'dormant_exit_probability']
        for k in probabilities:
            v = getattr(self, k)
            if not isfinite(v) or not 0 <= v <= 1:
                raise ValueError(k + ' must be in [0,1]')
        p = self.qualified_request_probability
        if p is not None and (not isfinite(p) or not 0 <= p <= 1):
            raise ValueError('Request probability must be in [0,1]')
        for k in ['contacts_per_month', 'contact_cost', 'onboarding_cost',
                  'acquisition_curvature', 'request_cost', 'dormant_month_cost',
                  'reactivation_cost']:
            v = getattr(self, k)
            if not isfinite(v) or v < 0:
                raise ValueError(k + ' must be finite and nonnegative')
        if not isfinite(self.reference_contacts) or self.reference_contacts <= 0:
            raise ValueError('Positive reference contact volume required')
        for k in ['monthly_contact_limit', 'reachable_contact_pool', 'monthly_event_capacity']:
            v = getattr(self, k)
            if v is not None and (not isfinite(v) or v < 0):
                raise ValueError(k + ' must be nonnegative or None')
        for k, minimum in [('cap_window_months', 1), ('cooldown_months', 0)]:
            v = getattr(self, k)
            if type(v) is not int or v < minimum:
                raise ValueError('Invalid ' + k)
        if self.paid_event_cap is not None and (type(self.paid_event_cap) is not int or self.paid_event_cap < 0):
            raise ValueError('Paid-event cap must be a nonnegative integer or None')
        for k in ['adoption_profile', 'need_age_profile', 'need_calendar_profile',
                  'acceptance_profile', 'return_age_profile']:
            if any(not isfinite(x) or not 0 <= x <= 1 for x in getattr(self, k)):
                raise ValueError('Invalid probability profile: ' + k)
        for k in ['competition_profile', 'fee_profile', 'contacts_by_month', 'budgets_by_month']:
            if any(not isfinite(x) or x < 0 for x in getattr(self, k)):
                raise ValueError('Invalid nonnegative profile: ' + k)
        for k in ['contacts_by_month', 'budgets_by_month']:
            if getattr(self, k) and len(getattr(self, k)) != horizon:
                raise ValueError(k + ' must match horizon exactly')
        if self.contacts_by_month and self.budgets_by_month:
            raise ValueError('Choose contacts or budget schedule, not both')


def profile(values, index, default):
    return values[index % len(values)] if values else default


def acquisition_cost(s, contacts, adoption, multiplier=1):
    return (s.contact_cost * multiplier * contacts *
            (1 + s.acquisition_curvature * contacts / s.reference_contacts)
            + s.onboarding_cost * contacts * adoption)


def contacts_from_budget(s, budget, adoption, multiplier=1):
    """Invert total acquisition spend; capacity/pool limits are applied later."""
    linear = s.contact_cost * multiplier + s.onboarding_cost * adoption
    quadratic = s.contact_cost * multiplier * s.acquisition_curvature / s.reference_contacts
    if quadratic:
        return 2 * budget / (linear + sqrt(linear * linear + 4 * quadratic * budget))
    if linear:
        return budget / linear
    if budget:
        raise ValueError('A positive budget cannot define volume with zero acquisition costs')
    return 0


def simulate_segment(s: Segment, horizon=36):
    s.validate(horizon)
    p = s.economics
    # Each bucket is (E/M/DE/DM/X, last paid calendar month, recent paid months).
    cohorts = []
    policy_births = []
    subscribers = active_policies = used_contacts = receivable = cumulative_cash = 0.
    rows = []
    track_last = s.cooldown_months > 0

    for t in range(horizon):
        adoption = profile(s.adoption_profile, t, s.adoption)
        multiplier = profile(s.competition_profile, t, 1)
        requested_contacts = (contacts_from_budget(s, s.budgets_by_month[t], adoption, multiplier)
                              if s.budgets_by_month else
                              (s.contacts_by_month[t] if s.contacts_by_month else s.contacts_per_month))
        contacts = requested_contacts
        if s.monthly_contact_limit is not None:
            contacts = min(contacts, s.monthly_contact_limit)
        if s.reachable_contact_pool is not None:
            contacts = min(contacts, max(0, s.reachable_contact_pool - used_contacts))
        used_contacts += contacts
        acquired = contacts * adoption
        spend = acquisition_cost(s, contacts, adoption, multiplier)
        if acquired:
            cohorts.append({'birth': t, 'n': acquired, 'buckets': {
                ('E', -1, ()): acquired * s.initial_active_fraction,
                ('DE', -1, ()): acquired * (1 - s.initial_active_fraction)}})

        starts = defaultdict(float)
        returned = dormant_exits = requests = candidates = eligible_for_payment = blocked = 0.
        work = []
        for c in cohorts:
            age = t - c['birth']
            active = defaultdict(float)
            return_rate = profile(s.return_age_profile, age, s.return_probability)
            for (state, last, history), count in c['buckets'].items():
                recent = tuple(m for m in history if m > t - s.cap_window_months)
                key = (state, last, recent)
                if state in ('DE', 'DM') and age > 0:
                    loss = count * s.dormant_exit_probability
                    back = (count - loss) * return_rate
                    dormant_exits += loss
                    returned += back
                    active[('X', -1, ())] += loss
                    active[key] += count - loss - back
                    if state == 'DE':
                        active[('E', last, recent)] += back
                    else:
                        active[('E', last, recent)] += back * s.return_reset_probability
                        active[('M', last, recent)] += back * (1 - s.return_reset_probability)
                else:
                    active[key] += count
            need = (profile(s.need_age_profile, age, s.need_probability) *
                    profile(s.need_calendar_profile, t, 1))
            request_p = p.q if s.qualified_request_probability is None else s.qualified_request_probability
            alpha = profile(s.acceptance_profile, t, s.paid_acceptance)
            for (state, last, history), count in active.items():
                starts[state] += count
                allowed = (state == 'E' and
                           (s.paid_event_cap is None or len(history) < s.paid_event_cap) and
                           (last < 0 or t - last >= s.cooldown_months))
                if allowed:
                    eligible_for_payment += count
                    requests += count * need * request_p
                    candidates += count * need * request_p * alpha
                elif state == 'E':
                    blocked += count
                work.append((c, (state, last, history), count, need * request_p * alpha if allowed else 0))
            c['next'] = defaultdict(float)
        scale = (min(1, s.monthly_event_capacity / candidates)
                 if s.monthly_event_capacity is not None and candidates else 1)
        events = 0.

        def transition(c, key, count):
            if not count:
                return
            state, last, history = key
            if state in ('DE', 'DM', 'X'):
                c['next'][key] += count
                return
            rho = p.rho_e if state == 'E' else p.rho_m
            dormant_fraction = s.dormant_fraction_e if state == 'E' else s.dormant_fraction_m
            continuing = count * rho
            noncontinuing = count - continuing
            if state == 'M':
                c['next'][('E', last, history)] += continuing * p.reset_probability
                c['next'][key] += continuing * (1 - p.reset_probability)
            else:
                c['next'][key] += continuing
            c['next'][('D' + state, last, history)] += noncontinuing * dormant_fraction
            c['next'][('X', -1, ())] += noncontinuing * (1 - dormant_fraction)

        for c, key, count, probability in work:
            state, last, history = key
            paid = count * probability * scale
            events += paid
            transition(c, key, count - paid)
            if paid:
                paid_history = history + (t,) if s.paid_event_cap is not None else ()
                transition(c, ('M', t if track_last else -1, paid_history), paid)
        ends = defaultdict(float)
        for c in cohorts:
            c['buckets'] = {k: v for k, v in c.pop('next').items() if v > 0}
            assert abs(sum(c['buckets'].values()) - c['n']) <= 1e-8 * max(1, c['n'])
            for (state, _, _), count in c['buckets'].items():
                ends[state] += count

        fee = profile(s.fee_profile, t, p.initial_payment)
        initial = events * fee * (1 - p.reversal_fraction)
        new_policies = events if p.event_basis == 'bound_policy' else 0.
        policy_births.append(new_policies)
        active_policies = p.policy_month_survival * active_policies + new_policies
        renewal_count = sum(b * p.policy_month_survival ** (t - birth)
                            for birth, b in enumerate(policy_births)
                            if t > birth and (t - birth) % p.renewal_interval == 0)
        renewal = renewal_count * p.renewal_payment if p.renewal_rights else 0.
        subscribers = p.software_survival * subscribers + acquired * p.software_conversion
        software = subscribers * p.software_month_payment
        revenue = initial + renewal + software
        dormant = starts['DE'] + starts['DM']
        variable = (starts['E'] * p.eligible_month_cost + starts['M'] * p.completed_month_cost
                    + dormant * s.dormant_month_cost + returned * s.reactivation_cost
                    + requests * s.request_cost + events * p.event_cost
                    + subscribers * p.software_month_cost + active_policies * p.policy_month_cost)
        contribution = revenue - variable - spend
        receipts = revenue if p.cash_lag == 0 else (rows[t-p.cash_lag]['revenue'] if t >= p.cash_lag else 0.)
        receivable += revenue - receipts
        cash = receipts - variable - spend
        cumulative_cash += cash
        rows.append(dict(month=t+1,segment=s.name,workflow=s.workflow,
                         requested_contacts=requested_contacts,contacts=contacts,acquired=acquired,
                         adoption=adoption,acquisition_cost=spend,cac=spend/acquired if acquired else None,
                         unused_budget=max(0,s.budgets_by_month[t]-spend) if s.budgets_by_month else 0,
                         eligible=starts['E'],completed_active=starts['M'],dormant=dormant,
                         returned=returned,dormant_exits=dormant_exits,
                         eligible_for_payment=eligible_for_payment,blocked_eligible=blocked,
                         qualified_requests=requests,monetary_events=events,
                         capacity_unfilled_events=candidates-events,new_policies=new_policies,
                         active_policies=active_policies,renewal_events=renewal_count if p.renewal_rights else 0,
                         subscribers=subscribers,initial_revenue=initial,renewal_revenue=renewal,
                         software_revenue=software,revenue=revenue,variable_cost=variable,
                         contribution=contribution,cash_receipts=receipts,receivables=receivable,
                         cash_surplus=cash,cumulative_cash=cumulative_cash,
                         next_e=ends['E'],next_m=ends['M'],next_dormant=ends['DE']+ends['DM'],
                         permanently_exited=ends['X'],next_relationship=ends['E']+ends['M']+ends['DE']+ends['DM'],
                         cumulative_acquired=sum(c['n'] for c in cohorts)))
    return rows


def simulate_market(segments, horizon=36, fixed_month_cost=0):
    if not segments or len({s.name for s in segments}) != len(segments):
        raise ValueError('Nonempty, uniquely named, mutually exclusive segments required')
    if len({s.economics.currency for s in segments}) != 1:
        raise ValueError('Run native currencies separately; explicit FX required to consolidate')
    if not isfinite(fixed_month_cost) or fixed_month_cost < 0:
        raise ValueError('Fixed cost must be finite and nonnegative')
    by_segment = {s.name: simulate_segment(s,horizon) for s in segments}
    keys = ['contacts','acquired','eligible','completed_active','dormant','returned',
            'qualified_requests','monetary_events','revenue','variable_cost','acquisition_cost',
            'contribution','cash_receipts','receivables','next_relationship','permanently_exited']
    months = []
    cumulative_cash = 0.
    for t in range(horizon):
        r = {k:sum(rows[t][k] for rows in by_segment.values()) for k in keys}
        r.update(month=t+1,currency=segments[0].economics.currency,fixed_cost=fixed_month_cost)
        r['operating_result'] = r['contribution'] - fixed_month_cost
        r['cash_surplus'] = r['cash_receipts'] - r['variable_cost'] - r['acquisition_cost'] - fixed_month_cost
        cumulative_cash += r['cash_surplus']
        r['cumulative_cash'] = cumulative_cash
        months.append(r)
    return {'segments':by_segment,'months':months}


def cohort_value(s, contacts, horizon=36):
    """Standalone cohort at stated acquisition volume; excludes fixed costs.

    A binding capacity constraint across cohorts makes this standalone value
    different from a cohort's actual contribution inside a larger forecast.
    """
    if s.budgets_by_month:
        s = replace(s,budgets_by_month=())
    rows = simulate_segment(replace(s,contacts_by_month=(contacts,)+(0,)*(horizon-1)),horizon)
    n = rows[0]['acquired']
    return (sum(s.economics.delta**t*r['contribution'] for t,r in enumerate(rows))/n
            if n else None)
