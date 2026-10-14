# Objais Measurement and Attribution Research

**13 October 2026 | Portugal first, with expansion comparisons. Research and proposed design; no live results are implied.**

Measurement records what happened; attribution assigns credit to an acquisition route. Connect product, partner and finance records while preserving their meanings, counting each commercial event once and respecting the data uses the service promises.

Read [the central acquisition explanation](<Objais Acquisition Numerical Summary.md>) for the connected numerical example and the relationship to the revenue model.

For a short explanation of unfamiliar terms, use [the shared glossary](<Objais Glossary.md>). Detailed formulas and counting rules remain in this reference.

## Current product focus and optional future venues

The acquisition baseline is Objais's publicly described photo-based indicative premium estimates, collection management and specialist introductions for supported valuables, cars, boats and pets. This is marketed scope, not proof that every category can be fulfilled in both countries. Health/home availability is inconsistent across public pages and Business is forthcoming; exclude these from initial campaigns until confirmed. [Objais Insurance](https://objais.com/en/insurance), [Objais Select](https://objais.com/en/select), [Objais Family](https://objais.com/en/family), [Objais Business](https://objais.com/en/business)

TCG is an optional future acquisition venue. Card recognition, grading, transaction integrations, auction tools and locally placeable card insurance are not established current capabilities. The community material below is exploratory and does not add an active TCG pilot to the initial campaign. Start with a current, serviceable product and a matching destination.

[The current venue prices and requirements](<Objais Advertising Prices and Requirements.md>) distinguish outside-brand advertising, auction-house promotion, published list prices and quote-only inventory. The retained original sections provide the funnel and measurement baseline; the current focus and new inventory findings guide execution.


## Measurement architecture and attribution

Use three linked records: campaign delivery and cost, product or service events, and commercial outcomes. Campaign systems describe exposure and spend; operational systems establish requests and partner decisions; finance establishes earned fees, reversals and receipts. Reconcile them by opportunity and payable-event identity.

### Proposed event sequence

| Event group | Proposed events | Authoritative source |
| --- | --- | --- |
| Arrival and access | landing_view, store_outbound, first_open | Permitted web or app measurement; store reports separately |
| First value | photo_attempt_started, photo_attempt_failed, recognition_confirmed, estimate_viewed | Product events or aggregate operational counters |
| Enquiry | quote_request_started, quote_request_submitted, lead_qualified | Backend and CRM |
| Partner process | lead_delivered, partner_decision_recorded, quote_issued, policy_bound | Partner receipt, CRM and policy evidence |
| Commercial process | payable_event_confirmed, fee_earned, fee_reversed, cash_received | Contract-linked commercial record and finance |
| Continuing value | item_added, documentation_updated, coverage_update_requested, renewal_completed | Product, CRM or policy record as applicable |

These are proposed internal names, not a claim that the events already exist. Google Analytics recommends lead lifecycle events including generate_lead and qualify_lead, and close_convert_lead for a completed customer conversion. Map only matching meanings. A form start is not generate_lead; partner acceptance is not automatically a completed customer transaction. Keep explicit internal payable-event and fee records regardless of analytics naming. [Google Analytics event definitions](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference/events)

For internal records, keep event identity, UTC occurrence time, receipt time, schema version, observable journey identity, opportunity identity when known, category, eligibility country, route and outcome reason. Link cost and fee records using their own identifiers and currency. Do not send this entire internal record to every analytics vendor: define a minimal destination-specific export.

Use an idempotency key for each authoritative transition; retries and client/server copies must not create another lead or fee. Do not rely on a generic event_id field to deduplicate automatically in every vendor. Keep pending outcomes visible, and allow delayed decisions or reversals to revise earlier cohort reports.

### Feedback to advertising systems

Where permitted, feed qualified or converted outcomes back to the ad platform instead of relying only on installs or initial forms. Google documents enhanced conversions for leads, qualified or converted lead goals, consent fields, conversion values and transaction identifiers. Its current guidance flags the 2026 move of uploads toward Data Manager API; verify the supported route for the actual account before implementation. [Google enhanced conversions for leads](https://support.google.com/google-ads/answer/14274408?hl=en)

Choose one primary bidding milestone for a pilot. Keep preceding milestones diagnostic so that the same journey does not earn a full conversion value at form submission, qualification, acceptance and binding. If a shallow event is temporarily used because deeper outcomes are sparse, keep the commercial decision based on mature downstream outcomes. An expected value used for bidding remains separate from earned revenue.

Keep first-touch source, request source and platform-attributed conversions as different views. Declare click and view windows, timezone and maturity rules. A policy claimed by several platforms is still one policy and one contractual fee. Attribution describes assigned credit; a randomised or otherwise credible holdout is needed to estimate incremental effect. Small pilots may only support directional comparisons.

### Privacy requirements that change the design

Objais's published privacy policy says its mobile app uses no cookies or tracking tools, permits website cookie choices, and distinguishes personalised-request processing from commercial marketing consent. The FAQ describes consent more broadly. The actual implementation, notices and partner handoff must be reconciled before adding measurement tools. Operational aggregates may be a suitable starting point; they still need an assessed purpose, legal basis and retention policy. [Objais privacy policy](https://objais.com/en/privacy), [Objais FAQ](https://objais.com/en/faq)

Keep asset photos, detailed collection values, documents, addresses, free text and health information out of advertising pixels, analytics payloads and replay recordings. Mask sensitive forms and collection screens. Do not put personal information in campaign URLs. Hashing an email does not make it anonymous or override permission requirements.

Apple requires App Tracking Transparency permission for the tracking it defines across companies' apps, websites or offline properties; first-party analytics and advertising tracking must be assessed separately. A deferred deep link or SDK is not automatically exempt. Design an unlinked or aggregate measurement path when tracking is declined. [Apple privacy and data use](https://developer.apple.com/app-store/user-privacy-and-data-use/)

## Full proposed event dictionary

These 22 event definitions are internal proposals. The occurrence, authoritative record and deduplication identity must be implemented explicitly. Advertising exports need their own purpose and permission assessment.

### landing_view

**Occurs when:** Eligible destination becomes visible.

**Source:** Permitted web measurement. **Identity:** Session/page-view identity.

**Critical internal fields:** route; category; campaign source where permitted.

**Export treatment:** Only approved minimal fields. **Status:** Proposed; not implemented.

### store_outbound

**Occurs when:** User activates store destination.

**Source:** Permitted web measurement. **Identity:** Session plus navigation event.

**Critical internal fields:** OS; route; destination.

**Export treatment:** Diagnostic only. **Status:** Proposed; not implemented.

### first_open

**Occurs when:** Observable app instance opens for first time.

**Source:** Permitted app measurement or store aggregate. **Identity:** App instance where permitted; never owner.

**Critical internal fields:** OS; version; route when lawfully available.

**Export treatment:** Conditional on measurement/privacy assessment. **Status:** Proposed; not implemented.

### photo_attempt_started

**Occurs when:** Input attempt starts at documented UI point.

**Source:** Product. **Identity:** Journey plus attempt identity.

**Critical internal fields:** category; OS; start timestamp.

**Export treatment:** Aggregate preferred initially. **Status:** Proposed; not implemented.

### photo_attempt_failed

**Occurs when:** Attempt terminates or reaches declared timeout.

**Source:** Product/backend. **Identity:** Attempt identity plus terminal transition.

**Critical internal fields:** reason code; duration; version.

**Export treatment:** No sensitive data. **Status:** Proposed; not implemented.

### recognition_confirmed

**Occurs when:** User confirms or corrects recognised item.

**Source:** Product. **Identity:** Attempt/result plus transition.

**Critical internal fields:** correction indicator; category.

**Export treatment:** Do not export identity/photo/free text. **Status:** Proposed; not implemented.

### estimate_viewed

**Occurs when:** Usable indicative result is actually displayed.

**Source:** Product. **Identity:** Estimate identity plus first-view transition.

**Critical internal fields:** duration; category; indicative status.

**Export treatment:** Exclude asset and premium amounts by default. **Status:** Proposed; not implemented.

### quote_request_started

**Occurs when:** User begins personalised enquiry.

**Source:** Product. **Identity:** Journey plus form-start identity.

**Critical internal fields:** route; category.

**Export treatment:** Diagnostic; not generated lead. **Status:** Proposed; not implemented.

### quote_request_submitted

**Occurs when:** Backend accepts unique valid request.

**Source:** Backend/CRM. **Identity:** Request idempotency key and opportunity.

**Critical internal fields:** opportunity; category; eligibility country; contact availability.

**Export treatment:** Map to generate_lead only where permitted and meaningful. **Status:** Proposed; not implemented.

### lead_qualified

**Occurs when:** Request meets written service criteria.

**Source:** CRM. **Identity:** Opportunity plus qualification decision.

**Critical internal fields:** criteria version; reason; occurrence time.

**Export treatment:** Map to qualify_lead if exported. **Status:** Proposed; not implemented.

### lead_delivered

**Occurs when:** Partner acknowledges delivered request.

**Source:** Backend/partner. **Identity:** Opportunity-partner delivery key.

**Critical internal fields:** partner; timestamp; delivery status.

**Export treatment:** Internal unless justified. **Status:** Proposed; not implemented.

### partner_decision_recorded

**Occurs when:** Partner gives substantive accepted/rejected/pending decision.

**Source:** Partner/CRM. **Identity:** Opportunity plus partner decision version.

**Critical internal fields:** decision; reason; partner; occurrence time.

**Export treatment:** Minimal outcome only if permitted. **Status:** Proposed; not implemented.

### quote_issued

**Occurs when:** Formal personalised quote issued.

**Source:** Partner/CRM. **Identity:** Quote identity.

**Critical internal fields:** opportunity; insurer; issue time; status.

**Export treatment:** Do not assume fee earned. **Status:** Proposed; not implemented.

### policy_bound

**Occurs when:** Cover effective under contract evidence.

**Source:** Policy record. **Identity:** Policy identity plus bind transition.

**Critical internal fields:** opportunity; effective time; policy status.

**Export treatment:** Completed transaction mapping only if meaning fits. **Status:** Proposed; not implemented.

### payable_event_confirmed

**Occurs when:** Contractual fee condition satisfied.

**Source:** Commercial record. **Identity:** Agreement plus payable-event identity.

**Critical internal fields:** agreement; trigger; opportunity; occurrence time.

**Export treatment:** Candidate primary optimisation signal; consent assessed. **Status:** Proposed; not implemented.

### fee_earned

**Occurs when:** Fee recorded as earned under agreed convention.

**Source:** Finance. **Identity:** Fee identity linked to payable event.

**Critical internal fields:** fee amount; currency; earned date; split treatment.

**Export treatment:** Value only with defined nonduplicating convention. **Status:** Proposed; not implemented.

### fee_reversed

**Occurs when:** Earned fee partly or fully withdrawn.

**Source:** Finance. **Identity:** Reversal identity plus original fee.

**Critical internal fields:** amount; currency; reason; original fee.

**Export treatment:** Use platform-specific adjustment only if supported. **Status:** Proposed; not implemented.

### cash_received

**Occurs when:** Actual receipt allocated to earned fee.

**Source:** Finance. **Identity:** Receipt plus allocation identity.

**Critical internal fields:** amount; currency; fee/invoice; receipt date.

**Export treatment:** Internal; not a second conversion. **Status:** Proposed; not implemented.

### item_added

**Occurs when:** Owner saves an additional collection item.

**Source:** Product. **Identity:** Asset identity plus creation transition.

**Critical internal fields:** owner when known; category; timestamp.

**Export treatment:** Useful task signal; no automatic payable event. **Status:** Proposed; not implemented.

### documentation_updated

**Occurs when:** Owner completes a defined documentation task.

**Source:** Product/CRM. **Identity:** Task identity plus completed transition.

**Critical internal fields:** task type; asset; timestamp.

**Export treatment:** Internal task measurement preferred. **Status:** Proposed; not implemented.

### coverage_update_requested

**Occurs when:** Owner requests a real policy coverage review.

**Source:** CRM. **Identity:** Opportunity/request idempotency key.

**Critical internal fields:** owner; policy link; request timestamp.

**Export treatment:** Qualification and payment assessed separately. **Status:** Proposed; not implemented.

### renewal_completed

**Occurs when:** Eligible due policy renews.

**Source:** Policy record. **Identity:** Policy plus renewal-term identity.

**Critical internal fields:** due date; term; status; rights reference.

**Export treatment:** Fee only if renewal remuneration earned. **Status:** Proposed; not implemented.

## Context for current-product inventory

Record the country, product category, media owner, buying route, actual placement, campaign and device alongside the permitted acquisition context. Keep Mercado Only Off inventory separate from Mercado Livre native placements. An Uber or CustoJusto app placement should be distinguishable from mobile web. Reconcile media billing, product records, partner outcomes and earned fees separately.

Optional community research can later add operator and invitation context. Forwarded codes do not prove immediate exposure. No marketplace purchase, bid or card sale is an Objais payable event. The 22 event definitions remain the proposed baseline, without implying installed tracking.

## Established offers and category-specific acquisition

Preserve category, country, invitation moment, known owner, authorised representative and whether the owner is newly acquired. Link service/valuation records only where their actual relationship is established. A dealer warranty, veterinary plan, shipping guarantee and continuing insurance policy are separate records. Read [the established offers and category capture strategy](<Objais Established Offers and Category Capture Strategy.md>) and its four linked category plans.

## Related research

- [Objais Funnels Research](<Objais Funnels Research.md>)
- [Objais Advertising Platforms Research](<Objais Advertising Platforms Research.md>)
- [Objais Metrics Research](<Objais Metrics Research.md>)
- [Objais User Experience Research](<Objais User Experience Research.md>)
- [Objais Acquisition Experiments Research](<Objais Acquisition Experiments Research.md>)
- [External advertising inventory](<Objais External Advertising Inventory Research.md>)
- [Advertising prices and requirements](<Objais Advertising Prices and Requirements.md>)
- [Optional future networks and communities](<Objais Networks and Communities Research.md>)

The [measurement workbook](<Objais Acquisition Measurement Plan.xlsx>) contains blank observed-value fields, proposed responsibilities and an illustrative calculator. The [source register](<research/acquisition/sources.csv>) preserves the source status and claim limits from the original research.
