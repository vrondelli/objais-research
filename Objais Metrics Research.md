# Objais Metrics Research

**13 October 2026 | Portugal first, with expansion comparisons. Research and proposed design; no live results are implied.**

Metrics connect the work to the decision. The primary dashboard explains commercial value and the customer task; diagnostic metrics explain where a result improves or deteriorates. Each measure needs an explicit counting unit, denominator, window and source.

Read [the central acquisition explanation](<Objais Acquisition Numerical Summary.md>) for the connected numerical example and the relationship to the revenue model.

For a short explanation of unfamiliar terms, use [the shared glossary](<Objais Glossary.md>). Detailed formulas and counting rules remain in this reference.

## Current product focus and optional future venues

The acquisition baseline is Objais's publicly described photo-based indicative premium estimates, collection management and specialist introductions for supported valuables, cars, boats and pets. This is marketed scope, not proof that every category can be fulfilled in both countries. Health/home availability is inconsistent across public pages and Business is forthcoming; exclude these from initial campaigns until confirmed. [Objais Insurance](https://objais.com/en/insurance), [Objais Select](https://objais.com/en/select), [Objais Family](https://objais.com/en/family), [Objais Business](https://objais.com/en/business)

TCG is an optional future acquisition venue. Card recognition, grading, transaction integrations, auction tools and locally placeable card insurance are not established current capabilities. The community material below is exploratory and does not add an active TCG pilot to the initial campaign. Start with a current, serviceable product and a matching destination.

[The current venue prices and requirements](<Objais Advertising Prices and Requirements.md>) distinguish outside-brand advertising, auction-house promotion, published list prices and quote-only inventory. The retained original sections provide the funnel and measurement baseline; the current focus and new inventory findings guide execution.


## Metrics to track

Use a small decision dashboard backed by a fuller metric dictionary. Each rate needs a defined numerator, denominator, time window and source. Segment by country, asset category, channel, creative or referral partner, device, app version and acquisition cohort where counts permit. Keep EUR and BRL separate.

### The primary dashboard

| Metric | Definition | Why it matters |
| --- | --- | --- |
| Cost per qualified request | Attributable acquisition cost divided by unique qualified opportunities | Captures lead quality before payment |
| Cost per payable event | Attributable acquisition cost divided by unique events meeting the payment agreement | Connects acquisition to monetisation |
| Payable yield | Opportunities with a first payable event divided by submitted opportunities in a matured cohort | Exposes acceptance and payment-condition losses |
| Contribution after acquisition | Net earned Objais fees less delivery variable costs and attributable acquisition cost | Primary commercial decision measure |
| Cash receipts and collection delay | Collected amounts and elapsed time from fee earning to allocated receipt | Shows financing needs and payer performance |
| First usable estimate rate | Observable first-use journeys with a usable result divided by first-use journeys starting a photo attempt | Indicates whether the entry experience delivers value |
| Estimate to request rate | Journeys submitting an enquiry divided by journeys receiving a usable estimate | Distinguishes interest from curiosity |
| Partner response time and unresolved backlog | Time from delivered request to first substantive response; requests still awaiting an outcome | Exposes service bottlenecks and incomplete cohorts |
| Useful task return | Activated owners completing a defined later task in a stated window divided by owners eligible for that window | Tests continuing product value |

A payable event can precede a cash receipt. Show pending, rejected, payable, invoiced, reversed and collected states separately. Preserve the rejection reason, payment condition and time to decision. Show contribution before fixed overhead alongside operating costs when assessing company profitability.

### Diagnostic metrics

Track impressions, outbound CTR, CPC, CPM, landing sessions, measured click-to-landing arrivals, store exits, first opens, photo-attempt success, time to usable estimate, recognition corrections, request completion, qualification rate, partner delivery failures, quotation rate, binding rate and reversals. These explain where contribution changes; they do not replace it.

Define clicks consistently: a platform's “all clicks” and outbound link clicks answer different questions. Platform impressions can repeat for the same person and should not become unique prospects. Clicks, sessions and installs are different counting units; a ratio between them is a diagnostic ratio rather than a person-level conversion unless linkage is established.

Measure estimate latency at median and 95th percentile, including failures and timeouts in a separate rate. Record the share of started attempts producing a usable result within the advertised time, with a precise start and end definition. AI confidence is not accuracy; validate matches against a reference set. User corrections are a diagnostic signal, not a complete error benchmark.

CAC here means all attributable acquisition cost per newly identified owner. Media-only cost per install, request or payable event is a separately labelled CPA. When distinct owners cannot be identified, report the observable unit and leave owner CAC unavailable.

Objais revenue ROAS equals attributable net earned Objais fees divided by ad spend. Insurer premiums and asset valuations do not enter its numerator. A ROAS above one can still lose money after processing, support, data and referral costs. Evaluate lifetime contribution only with supported future payment rights, matured cohorts and continuing delivery costs; daily app engagement cannot establish renewal income.

## Full metric dictionary

The following 38 definitions expand the dashboard. Observed values remain blank in the measurement workbook. Owner assignments are proposed responsibilities, not confirmed team appointments.

### Outbound CTR

**Purpose:** Diagnose message and destination interest.

**Definition:** Outbound link clicks / platform impressions.

**Counting and window:** Click and impression. Same platform and reporting window; do not substitute all clicks.

**Source and proposed owner:** Ad platform; Acquisition. **Dashboard role:** Diagnostic.

### Media CPC

**Purpose:** Compare with contribution ceiling.

**Definition:** Media spend / outbound clicks.

**Counting and window:** Currency per click. Same campaign; EUR and BRL separate.

**Source and proposed owner:** Ad cost export; Acquisition. **Dashboard role:** Diagnostic.

### Media CPM

**Purpose:** Explain auction cost changes.

**Definition:** 1000 * media spend / impressions.

**Counting and window:** Currency per 1000 impressions. Same inventory and period.

**Source and proposed owner:** Ad cost export; Acquisition. **Dashboard role:** Diagnostic.

### Measured click to landing ratio

**Purpose:** Detect destination or measurement loss.

**Definition:** Measured arriving landing sessions / outbound clicks.

**Counting and window:** Session and click. Diagnostic ratio; no assumed identity match; consent coverage shown.

**Source and proposed owner:** Ad export and web measurement; Data. **Dashboard role:** Diagnostic.

### Store outbound rate

**Purpose:** Diagnose installation transition.

**Definition:** Eligible landing sessions opening store link / eligible landing sessions.

**Counting and window:** Session. Session counted once; returning installed users separately.

**Source and proposed owner:** Permitted web measurement; Product. **Dashboard role:** Diagnostic.

### New installs and redownloads

**Purpose:** Explain app entry volume.

**Definition:** Store-reported new installs and redownloads kept separate.

**Counting and window:** Store acquisition. Store attribution definitions preserved; do not infer unique owners.

**Source and proposed owner:** Store reporting; Product. **Dashboard role:** Diagnostic.

### First usable estimate rate

**Purpose:** Judge delivery of initial value.

**Definition:** First-use journeys with first usable estimate / first-use journeys starting photo attempt.

**Counting and window:** Observable journey. Deduplicate journey; cohort has full selected completion window; show unlinked share.

**Source and proposed owner:** Product measurement or operational aggregates; Product. **Dashboard role:** Primary.

### First attempt success

**Purpose:** Prioritise capture and processing reliability.

**Definition:** First photo attempts ending in usable estimate / started first photo attempts.

**Counting and window:** Attempt. Timeout and failure count against success; distinguish retry success.

**Source and proposed owner:** Product backend; Product. **Dashboard role:** Diagnostic.

### Photo failure rate

**Purpose:** Locate technical and input failures.

**Definition:** Failed or timed out photo attempts / started photo attempts.

**Counting and window:** Attempt. By failure reason; include abandoned attempts under declared timeout.

**Source and proposed owner:** Product backend; Product. **Dashboard role:** Diagnostic.

### Estimate latency

**Purpose:** Check actual waiting experience.

**Definition:** Elapsed time from agreed input-start point to usable estimate displayed.

**Counting and window:** Seconds; p50 and p95. Completed estimates; report failed and timed out attempts alongside.

**Source and proposed owner:** Product events; Product. **Dashboard role:** Diagnostic.

### Result within advertised time

**Purpose:** Assess marketing promise delivery.

**Definition:** Started attempts with usable result within stated promise / all started attempts.

**Counting and window:** Attempt. Start/end fixed; include failures; do not silently start clock after upload.

**Source and proposed owner:** Product events; Product. **Dashboard role:** Diagnostic.

### Recognition correction rate

**Purpose:** Find confusing matches and category gaps.

**Definition:** Recognised results corrected by user / reviewed recognised results.

**Counting and window:** Reviewed result. Correction is a signal; not complete model accuracy.

**Source and proposed owner:** Product events; Product. **Dashboard role:** Diagnostic.

### Estimate to request rate

**Purpose:** Measure intent after first value.

**Definition:** Estimate journeys submitting unique enquiry / journeys with usable estimate.

**Counting and window:** Journey. Same linked path and maturity window; referral bypass analysed separately.

**Source and proposed owner:** Product and CRM; Product. **Dashboard role:** Primary.

### Request form completion

**Purpose:** Diagnose unnecessary form loss.

**Definition:** Unique successful submitted opportunities / journeys starting request form.

**Counting and window:** Journey and opportunity. Declared window; repeated submission does not add opportunity.

**Source and proposed owner:** Backend and CRM; Product. **Dashboard role:** Diagnostic.

### Qualification rate

**Purpose:** Assess eligibility and lead quality.

**Definition:** Qualified opportunities / submitted opportunities.

**Counting and window:** Opportunity. Written criteria; pending and unresolved separately; mature cohort.

**Source and proposed owner:** CRM; Operations. **Dashboard role:** Diagnostic.

### Delivery success

**Purpose:** Check request transport.

**Definition:** Partner-acknowledged deliveries / intended deliveries.

**Counting and window:** Opportunity-partner delivery. Retry deduplication; distinguish fan-out across partners.

**Source and proposed owner:** Backend and partner acknowledgement; Operations. **Dashboard role:** Diagnostic.

### Partner response time

**Purpose:** Assess service capacity and owner uncertainty.

**Definition:** Elapsed time from delivery to first substantive response.

**Counting and window:** Hours; p50 and p95. Responded subset with unresolved age and count shown separately.

**Source and proposed owner:** CRM and partner record; Operations. **Dashboard role:** Primary.

### Partner decision backlog

**Purpose:** Expose incomplete cohorts and bottlenecks.

**Definition:** Delivered opportunities without substantive decision and their age.

**Counting and window:** Opportunity count and hours. As-of snapshot; pending is not rejection or success.

**Source and proposed owner:** CRM; Operations. **Dashboard role:** Primary.

### Quote rate

**Purpose:** Assess underwriting and handoff.

**Definition:** Opportunities with formal quote / eligible delivered opportunities.

**Counting and window:** Opportunity. Full quotation window; unsupported routes excluded explicitly.

**Source and proposed owner:** Partner and CRM; Operations. **Dashboard role:** Diagnostic.

### Binding rate

**Purpose:** Measure contract completion.

**Definition:** Opportunities with policy bound / opportunities receiving formal quote.

**Counting and window:** Opportunity. Actual effective cover evidence; cohort maturity and cancellations tracked.

**Source and proposed owner:** Policy record; Operations. **Dashboard role:** Diagnostic.

### Payable yield

**Purpose:** Connect intent to payment rights.

**Definition:** Submitted opportunities with first contractual payable event / submitted opportunities.

**Counting and window:** Opportunity. Mature cohort; pending and reasons shown; first event avoids repeat double count.

**Source and proposed owner:** Contract-linked CRM; Commercial. **Dashboard role:** Primary.

### Cost per qualified request

**Purpose:** Compare route quality economics.

**Definition:** Attributable acquisition cost / unique qualified opportunities.

**Counting and window:** Currency per opportunity. Cohort-aligned; costs include attributable referral and onboarding work.

**Source and proposed owner:** Cost ledger and CRM; Finance. **Dashboard role:** Primary.

### Cost per payable event

**Purpose:** Compare acquisition against fee contribution.

**Definition:** Attributable acquisition cost / unique payable events.

**Counting and window:** Currency per event. Cohort-aligned; media-only CPA reported separately.

**Source and proposed owner:** Cost ledger and payable register; Finance. **Dashboard role:** Primary.

### Owner CAC

**Purpose:** Connect acquisition to existing owner model.

**Definition:** All attributable acquisition cost / newly identified distinct owners.

**Counting and window:** Currency per owner. Never infer owners from anonymous sessions; reactivation separately.

**Source and proposed owner:** Identity-linked CRM and cost ledger; Finance. **Dashboard role:** Diagnostic.

### Net earned Objais fees

**Purpose:** Establish revenue numerator.

**Definition:** Earned contractual fees less fee reversals under finance convention.

**Counting and window:** Currency. Net retained share; premium and insured value excluded; currency separate.

**Source and proposed owner:** Fee ledger and contracts; Finance. **Dashboard role:** Primary.

### Objais revenue ROAS

**Purpose:** Revenue efficiency before other costs.

**Definition:** Attributable net earned Objais fees / media spend.

**Counting and window:** Ratio. Cohort and attribution window declared; never use insurer premium.

**Source and proposed owner:** Fee ledger and media export; Finance. **Dashboard role:** Diagnostic.

### Contribution after acquisition

**Purpose:** Primary lane decision.

**Definition:** Net earned fees - delivery variable costs - attributable acquisition costs.

**Counting and window:** Currency and currency per entry. Include free and failed use costs; fixed overhead separate.

**Source and proposed owner:** Finance and cost-driver ledger; Finance. **Dashboard role:** Primary.

### Fee reversal rate

**Purpose:** Check quality and contractual risk.

**Definition:** Value of fees reversed / gross earned fees in matched earned cohort.

**Counting and window:** Currency proportion. Report event-count rate separately; adequate reversal maturity.

**Source and proposed owner:** Fee ledger; Finance. **Dashboard role:** Diagnostic.

### Cash receipts

**Purpose:** Assess cash available.

**Definition:** Actual money received allocated to fee/invoice.

**Counting and window:** Currency. Receipts are collections of fees; not additional earned revenue.

**Source and proposed owner:** Bank/finance receipt ledger; Finance. **Dashboard role:** Primary.

### Collection delay

**Purpose:** Assess working capital.

**Definition:** Time from fee earning to allocated collection.

**Counting and window:** Days; p50 and p95. Collected subset plus unpaid balance/age shown; partial payments retained.

**Source and proposed owner:** Fee and receipt ledgers; Finance. **Dashboard role:** Primary.

### Useful task return

**Purpose:** Test continuing value.

**Definition:** Activated identified owners with defined later task in window / activated owners eligible for window.

**Counting and window:** Owner. Suggested D30 window days 21-30; label definition; login alone excluded.

**Source and proposed owner:** Permitted product/CRM records; Product. **Dashboard role:** Primary.

### New payable opportunity rate

**Purpose:** Test repeat economics.

**Definition:** Owners with genuinely new payable opportunity / eligible acquired owners.

**Counting and window:** Owner. Contract-defined new opportunity; visit or scan is not reset.

**Source and proposed owner:** CRM and contracts; Commercial. **Dashboard role:** Diagnostic.

### Policy renewal rate

**Purpose:** Evaluate renewal relationship.

**Definition:** Eligible due policies renewed / eligible policies reaching renewal due date.

**Counting and window:** Policy. Mature due cohort; separate contractual remuneration rights.

**Source and proposed owner:** Policy records; Commercial. **Dashboard role:** Conditional.

### Estimate comprehension

**Purpose:** Detect harmful misunderstanding.

**Definition:** Participants correctly explaining estimate and cover status / assessed participants.

**Counting and window:** Participant. Qualitative task sample; denominator and question recorded; no population estimate.

**Source and proposed owner:** Usability observation; Research. **Dashboard role:** Primary UX.

### Independent task success

**Purpose:** Prioritise product repairs.

**Definition:** Task attempts completed correctly without help / assessed task attempts.

**Counting and window:** Task attempt. Per task and participant; retain assist/failure reason.

**Source and proposed owner:** Usability observation; Research. **Dashboard role:** Primary UX.

### Web Core Vitals

**Purpose:** Improve loading responsiveness and stability.

**Definition:** LCP <=2.5s; INP <=200ms; CLS <=0.1 at p75.

**Counting and window:** Web page-load distribution. Field evidence; mobile/desktop separate; native app excluded.

**Source and proposed owner:** Web field performance; Engineering. **Dashboard role:** Diagnostic.

### Unlinked outcome share

**Purpose:** Show attribution coverage.

**Definition:** Outcomes lacking permitted upstream linkage / all outcomes.

**Counting and window:** Outcome. By outcome type and route; no identity guessing.

**Source and proposed owner:** CRM and measurement reconciliation; Data. **Dashboard role:** Primary data.

### Outcome reconciliation residual

**Purpose:** Ensure decisions use correct data.

**Definition:** Operational or finance outcomes not reconciled to canonical records.

**Counting and window:** Event count and currency. Daily and mature cohort; record causes; avoid hiding vendor modelling difference.

**Source and proposed owner:** CRM fee ledger and exports; Data. **Dashboard role:** Primary data.

## Measures for external placements and later community research

Segment the baseline metrics by country, current product, venue, named placement and device. Track delivered impressions, permitted viewability measures, outbound clicks, usable results, qualified requests, payable events and full attributable cost. Separate published CPM, negotiated invoice price and observed effective CPC. Compare app inventory with app inventory rather than silently grouping mobile web under the same label.

The communities reference retains ten optional measures for operator activation, relationships, commerce events, invitations, task completion, evidence completeness, owner CAC, commercial yield, workload and concentration. They are future research additions outside the original 38 metrics. Group membership is not an owner-conversion denominator.

## Established offers and category-specific acquisition

Segment by pet/boat/jewellery/watch category, country, owner situation and invitation moment. An existing policy update, new collection item and new owner are different outcomes. Include partner onboarding, staff coordination and ongoing support in cost; the category plans propose diagnostics without changing the original 38-definition dictionary. Read [the established offers and category capture strategy](<Objais Established Offers and Category Capture Strategy.md>) and its four linked category plans.

## Related research

- [Objais Funnels Research](<Objais Funnels Research.md>)
- [Objais Advertising Platforms Research](<Objais Advertising Platforms Research.md>)
- [Objais Measurement and Attribution Research](<Objais Measurement and Attribution Research.md>)
- [Objais User Experience Research](<Objais User Experience Research.md>)
- [Objais Acquisition Experiments Research](<Objais Acquisition Experiments Research.md>)
- [External advertising inventory](<Objais External Advertising Inventory Research.md>)
- [Advertising prices and requirements](<Objais Advertising Prices and Requirements.md>)
- [Optional future networks and communities](<Objais Networks and Communities Research.md>)

The [measurement workbook](<Objais Acquisition Measurement Plan.xlsx>) contains blank observed-value fields, proposed responsibilities and an illustrative calculator. The [source register](<research/acquisition/sources.csv>) preserves the source status and claim limits from the original research.
