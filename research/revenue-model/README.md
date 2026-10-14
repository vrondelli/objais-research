# Updated Objais revenue model

Version 2 implements the timing, dormant-return, adoption and acquisition mechanisms identified in the problem review. Inputs remain hypothetical; the model does not establish Objais demand or contractual rights.

`revenue_model.py` exposes the public functions. `Parameters`, `simulate` and the stationary closed forms preserve the original benchmarks. `Segment`, `simulate_segment`, `simulate_market` and `cohort_value` expose the updated finite model in `episodic_model.py`.

Each segment is a mutually exclusive consumer-owner group with a category, country/channel context and direct or delegated workflow. Representatives are not extra owners. Do not mix native currencies or apply the consumer unit unchanged to professional multi-client accounts.

The updated flow is:

**Distinct prospects → adoption → active or dormant owner → need → qualified request → payable event allowed by history and capacity → revenue, cost and collection.**

Dormant returns preserve acquisition identity and paid-event history. Software billing and policy renewal survive or stop on their own clocks. Optional caps count initial paid events, not renewals or monthly software charges.

```python
from dataclasses import replace
from revenue_model import Parameters, Segment, simulate_market, cohort_value

economics = Parameters()  # synthetic fee, service, policy/billing and cash inputs
twice_yearly = (1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
segment = Segment(
    'Illustrative direct workflow', economics,
    contacts_per_month=2000, adoption=.5, contact_cost=2,
    qualified_request_probability=.5, paid_acceptance=.2,
    need_age_profile=twice_yearly, return_age_profile=twice_yearly,
    dormant_fraction_e=1, dormant_fraction_m=1,
    dormant_month_cost=.01, reactivation_cost=.2,
    paid_event_cap=2, cooldown_months=6,
)
company = simulate_market([segment], horizon=36, fixed_month_cost=1000)
standalone_owner_value = cohort_value(segment, contacts=2000, horizon=36)
```

This example assumes complete return at each scheduled date and only one lifetime payable enquiry because no repeat reset is specified. Neither assumption is established for Objais. A positive standalone owner value excludes fixed costs and may coexist with a calendar company loss.

Rate profiles repeat at their supplied length. `need_age_profile` uses months since each cohort's acquisition; `need_calendar_profile` gates or modifies that probability by calendar month. The product is a specified need probability, not two independent empirical estimates. Explicit `contacts_by_month` or `budgets_by_month` schedules instead match the forecast horizon exactly. Select one of these schedules. A contact capacity or reachable pool can leave budget unspent.

The new model derives acquisition spend from `Segment.contact_cost`, adoption, curvature, competition pressure and onboarding cost. It does not also charge `economics.cac`, use `economics.acquired_per_month`, or subtract `economics.fixed_month_cost`. Fixed costs are passed once to `simulate_market`. If no explicit qualified-request probability is supplied, `economics.q` supplies it, with need and acceptance applied separately. Set all three explicitly when calibrating the new funnel.

The capacity parameter is an independently allocated segment limit. It scales candidate paid events proportionally; qualified requests still incur request cost. It does not represent a service backlog. Allocate any shared partner capacity across segments before running the model. Under binding multi-cohort capacity, a standalone cohort projection is not an additive customer-value estimate for the whole business.

Reproduce the calculations from the workspace root:

```bash
python3 -m unittest discover -s research/revenue-model -p 'test_*model.py'
python3 research/publication/rebuild.py
```

`extension-examples.json` contains the complete inputs and outputs for 15 cases; CSV files contain results and monthly histories. The original 52 sensitivity experiments remain unchanged in `research/revenue-summary/`.

The committed workbook has live formulas for stationary benchmark sheets and Acquisition Curve. Advanced Inputs, Results and Monthly are labelled snapshots generated from Python; editing them does not recalculate the expanded model. The packaged rebuild updates the JSON/CSV examples and reader documents, not the workbooks. Workbook snapshots need a separate regeneration and verification before using changed inputs. The `.tex` file is the authoritative full specification.

Remaining commercial inputs include observed need/return dates, actual adoption by task performer, payment rights, cost/spend curves, acceptance, service costs, capacities and cash dates. Professional account units, later software upgrades, request backlogs, explicit currency consolidation and detailed bad-debt/late-credit handling remain extensions.
