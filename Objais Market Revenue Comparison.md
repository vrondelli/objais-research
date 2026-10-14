# Objais Market Revenue Comparison

**13 October 2026 | Global scope with Brazil and Europe highlighted**

Collectibles can improve the frequency of useful product activity, but changing category does not by itself change insurance remuneration. A retained collector becomes economically valuable when retention increases first paid conversion, creates genuinely new paid events, supports paid software or earns renewal income. With one payable lead per owner and no later remuneration, post-sale engagement adds costs without additional lead revenue.

The current markets also contain collection workflows: watches, jewellery, art and antiques. Testing one of those existing categories may establish the commercial mechanism with less new catalogue work than a broad TCG launch. A large collector audience is financially attractive only if its insurable or paying fraction supports the cost of the free users.

All numerical inputs below are synthetic controlled assumptions, not measured market rates, Objais prices or forecasts. The researched evidence informs the tasks and commercial hypotheses; it cannot populate CAC, fees, paid conversion or continuation. Actual market economics inputs remain blank in the workbook.

# Resolve what Objais is paid for

The team reportedly described selling leads. Objais's public FAQ describes insurer commissions and separate service-referral fees. These descriptions may be compatible, but they do not establish the actual payment trigger or renewal rights. The model keeps accepted-lead and bound-policy remuneration as alternative architectures until contracts and invoices settle this. A submitted request, accepted lead and bound policy are distinct events. [Objais FAQ](https://www.objais.com/en/faq)

The FAQ also distinguishes an app estimate update from a change to policy coverage. An inventory addition or price update therefore cannot automatically be counted as another lead, paid endorsement or renewal. A repeat fee requires an actual paid event. [Objais FAQ](https://www.objais.com/en/faq)

The existing research identifies advertised fine art, watches, jewellery, luxury handbags, yachts, supercars, everyday cars, leisure boats and pets, with broader antiques and collections wording. Advertising establishes scope, not revenue-producing operation in every country. Decorative antiques overlap the expansion idea; archaeological antiquities are a separate specialist case. Wine and instruments need rollout confirmation. Home, health and planned Business products are excluded from the current comparison. [Current market research](Objais Current Markets Research.md)

# Mathematical viability conditions

Define a lane by country, category, owner segment, acquisition channel and payment contract. Let A denote acquired owners, p qualified-request probability, alpha paid acceptance conditional on a request, q = p × alpha, f payment per accepted lead before reversals, omega reversed fraction, h processing cost per paid event, vE cost per acquired eligible owner and k CAC per acquired owner.

For one-visit leads, revenue is R = A × q × f × (1 − omega). Customer contribution before fixed costs is u = q × [f × (1 − omega) − h] − vE − k. Unit viability requires u > 0. Object value increases revenue only if the actual fee contract or paid conversion responds to it.

The maximum affordable CAC is k_max = q × [f × (1 − omega) − h] − vE. For q > 0 and omega < 1, break-even payment is f_min = [h + (k + vE)/q] / (1 − omega). For positive event margin m = f × (1 − omega) − h, q_min = (k + vE)/m. A required q above 1 is infeasible. Nonpositive event margin cannot be fixed by more volume. Fixed costs are excluded from these unit thresholds.

The retained-cohort model has E owners with one unexhausted opportunity and M retained owners whose opportunity has already monetised. Its equations are L = qE; E_next = rhoE(E − L) + rhoM × lambda × (M + L); M_next = rhoM(1 − lambda)(M + L). Lambda is a genuine new payable episode conditional on retained post-event state, not another scan, visit or collection edit.

With lambda = 0, expected lifetime paid leads per acquired owner equal q / [1 − rhoE(1 − q)] and cannot exceed one. Post-event continuation rhoM does not enter that expression. Retention before first payment can improve eventual conversion, while its additional costs must still be funded.

For H months the model computes discounted customer contribution V_H before CAC and fixed costs. Unit viability requires V_H > k. Using the transition matrix T in the mathematical specification, the opportunity contribution is w^T × sum from a = 0 to H − 1 of (delta T)^a × eE, with w = (mq − vE, −vM), discount factor delta and initial state eE = (1, 0). Renewals, paid software and earned service fees use separate event and continuation rules.

The inverse fee threshold uses discounted payable events N_H, discounted variable costs C_H and discounted other revenue O_H: f_min = max(0, [k + C_H − O_H] / [(1 − omega)N_H]). This holds event rates, continuation, other prices and costs fixed. If the denominator is zero, no initial fee can generate revenue. The workbook derives these quantities from its cohort formulas.

For software let kappa be paid starts per acquired owner, eta billed monthly continuation and b − vS contribution per billed month after applicable fees and incremental costs. Let G_H = (b − vS) × sum from a = 0 to H − 1 of (delta eta)^a. If G_H > 0, kappa_min = max(0, [k − V_H_without_software]/G_H). A threshold above 100% is infeasible. The denominator is all acquired owners, not just enthusiastic interviewees or users offered a paywall.

For a commission architecture, q means policy-binding probability and initial payment equals eligible premium × commission rate × retained share. Earned annual renewals start at policy age 12 months and depend on survival and actual remuneration rights. App continuation does not replace policy survival. Lead and binding payments are additive only if an agreement explicitly grants both incrementally.

Company viability additionally requires revenue to cover acquisition, variable and fixed costs, and cash to bridge payment delays. A positive 36-month customer contribution can coexist with a negative 36-month company result: recently acquired cohorts have not matured. Customer, insurer, distribution-partner, policy and subscription retention must be measured separately.

# Controlled numerical comparison

The common illustration assumes EUR 20 per accepted lead, 5% reversals, EUR 1 cost per paid event, EUR 0.20 eligible-owner monthly cost, EUR 0.30 completed-owner monthly cost, EUR 4 CAC, q = 10% per eligible owner-month, 1% monthly discount rate and a 36-month horizon. These are chosen inputs, not market estimates.

C1 is a one-visit baseline. C2 changes only CAC to EUR 1. C3 changes only post-event continuation to 80%. C4 sets pre- and post-event continuation to 80%. C5 adds a 10% eligibility reset conditional on retained post-event state; this requires documented repeat remuneration.

C6–C9 stress a collector audience with low insurance intent: q = 2%, pre-event continuation 90%, post-event continuation 95%, eligible monthly cost EUR 0.30 and completed monthly cost EUR 0.50. Fee, CAC and processing cost stay the same. C7 adds a 10% eligibility reset. C8 and C9 instead add software with EUR 3 billed-month payment, EUR 0.50 incremental billed-month cost, 95% billed continuation and paid starts of 5% and 15%. These combinations are not measured TCG or figure behaviour.

C10 is an alternative bound-policy architecture with 10% binding, EUR 30 initial payment, no reversal, EUR 15 earned annual renewal fee, 98% monthly policy survival and EUR 0.10 monthly policy cost. There is no app continuation or repeat episode. Matching the lead and binding rates numerically is only a controlled assumption; their empirical rates are not interchangeable.

| Controlled case | Maximum CAC over 36 months | Contribution after assumed CAC |
| --- | --- | --- |
| C1 One-visit lead baseline | EUR 1.60 | EUR -2.40 |
| C2 Same lead, cheaper acquisition | EUR 1.60 | EUR +0.60 |
| C3 Post-sale retention only | EUR 1.49 | EUR -2.51 |
| C4 Retention before first paid lead | EUR 5.17 | EUR +1.17 |
| C5 New payable opportunities | EUR 5.88 | EUR +1.88 |
| C6 Collector tool with low insurance intent | EUR -0.53 | EUR -4.53 |
| C7 Low-intent collector plus repeat leads | EUR 0.06 | EUR -3.94 |
| C8 Low-intent collector plus 5% paid tools | EUR 1.34 | EUR -2.66 |
| C9 Low-intent collector plus 15% paid tools | EUR 5.09 | EUR +1.09 |
| C10 Binding commission and renewal rights | EUR 4.25 | EUR +0.25 |

C2 proves that a one-off lead model can be unit-positive through cheaper acquisition without retention. C3 shows that post-sale retention alone worsens economics. C4 shows the benefit of continuation before conversion. C5 improves contribution through another paid opportunity. C6 and C7 fail despite high continuation and some repeat eligibility. C9 succeeds at customer level only because the assumed paid conversion funds retained service.

At C1 assumptions, unit break-even requires CAC no greater than EUR 1.60, payment at least EUR 45.26 at 10% conversion, or paid-event probability at least 23.33% at EUR 20 payment. These are alternative one-variable changes holding the other inputs fixed. With EUR 1,000 monthly fixed expense and 1,000 new owners monthly in a one-visit business, another EUR 1 per acquired owner must be covered: the limits become CAC EUR 0.60, fee EUR 55.79 or conversion 28.89%. Equality is break-even, not a safety margin.

For C6, maximum CAC is negative: zero acquisition spend still fails to cover retained service costs. The minimum initial fee is EUR 50.44. Adding C7's reset reduces it to EUR 44.25, above the assumed EUR 20. Even resetting every retained completed opportunity every month leaves contribution after CAC negative, approximately EUR −3.45. Purchase frequency cannot compensate for too little paid demand in this controlled case.

C6 plus the illustrated software needs approximately 12.1% paid starts among all acquired owners to break even over 36 discounted months before fixed costs. At 5% it loses EUR 2.66 per acquired owner; at 15% it contributes EUR 1.09. This assumes incremental software revenue, the stated billed continuation and no double-counting of free/paid service costs. It does not establish that Objais can achieve that offer or conversion.

Collectr advertises USD 59.99 annual PRO billing; Pop Price Guide advertises USD 29.99 annually. Both offer free alternatives. These are functionality and price precedents, not evidence of Objais willingness to pay, conversion, local net price or competitive advantage. The EUR 3 monthly assumption is independently synthetic. [Collectr PRO](https://www.getcollectr.com/pro), [Pop Price Guide](https://www.hobbydb.com/marketplaces/poppriceguide/subs/pop-price-guide-landing-page)

## Company profit and cash need a separate test

The calendar illustration acquires 1,000 new owners every month for 36 months, incurs EUR 1,000 fixed expense monthly, receives invoiced revenue one month later and pays modeled costs immediately. It starts without an installed customer or policy base. It excludes startup build spend, tax, bad debt and late credits.

| Case | Operating result over 36 months | Cash surplus over 36 months |
| --- | --- | --- |
| C2 Same lead, cheaper acquisition | EUR -14,400 | EUR -16,300 |
| C4 Retention before first paid lead | EUR -1,165 | EUR -7,951 |
| C5 New payable opportunities | EUR 19,343 | EUR 11,788 |
| C9 Low-intent collector plus 15% paid tools | EUR -37,478 | EUR -48,243 |
| C10 Binding commission and renewal rights | EUR -48,805 | EUR -53,906 |

C2's EUR 0.60 unit contribution cannot cover EUR 1,000 fixed expense with 1,000 monthly acquisitions: more than about 1,667 acquisitions at unchanged economics are needed for operating profit. C4 is customer-positive but remains slightly negative over the 36-month calendar. C9's 15% software conversion also has positive customer value and a substantial calendar loss. C10 illustrates how renewal remuneration arrives slowly in a newly built policy book.

Under C6's calendar assumptions, paid starts need approximately 18.75% for the 36-month operating result to break even and 20.08% for cumulative cash to break even by month 36. Both exceed the 12.1% customer-value threshold. End-of-horizon cash break-even does not eliminate initial funding needs: use the minimum cumulative cash balance, build costs and a funding buffer to size the bridge.

# Apply the model to the researched markets

The market evidence identifies recurring tasks and product precedents. It does not establish Objais paid-event rates. The conditions below are hypotheses to validate, not a ranking of measured profitability. Separate high-value collectors and professional users from one-object owners and casual hobbyists. [Current markets research](Objais Current Markets Research.md), [Collectibles research](Collectibles Market Research.md)

## Existing markets

### Watches

**Target:** Single owner vs multi-watch collector. **Recurring task:** Serials, invoices, purchases, service, disposal and coverage records.

**Potential remuneration:** Accepted initial lead; renewal only with rights; paid dealer workflow if contracted. **Viability condition:** Dealer/service distribution lowers CAC or documentation raises q; repeat episodes must be payable. **Team data:** Reference and authenticity requirements, net fee, multi-piece share, dealer CAC.

### Jewellery

**Target:** One-piece owner vs growing collection. **Recurring task:** Appraisal, gifts, repair and insured-value changes.

**Potential remuneration:** Initial lead or binding commission; policy renewal with rights. **Viability condition:** Actual payment and conversion cover acquisition and appraisal/support costs. **Team data:** Premium basis, broker share, net fee, appraisals, renewal ownership.

### Luxury handbags

**Target:** User of one bag vs valuable resale collection. **Recurring task:** Model, variant, receipts, condition and ownership changes.

**Potential remuneration:** Initial placement; contracted service or paid inventory tool. **Viability condition:** Insurable collection and reliable variants produce paid demand; monitoring alone earns nothing. **Team data:** Insurer appetite, collection value distribution, matching accuracy and verification cost.

### Fine art

**Target:** Private collector vs professional managing clients. **Recurring task:** Provenance, location, loan, transit, restoration and estate records.

**Potential remuneration:** Placement; contracted expert referrals; professional subscription. **Viability condition:** Larger contribution survives specialist costs, or professionals pay for repeated work. **Team data:** Expert minutes, placement yield, referral ledger, payer and documentation acceptance.

### Decorative antiques

**Target:** Documented collection vs isolated inherited object. **Recurring task:** Appraisal, restoration, provenance, estate and movement records.

**Potential remuneration:** Placement and separately contracted services. **Viability condition:** Accepted documented niche, trusted partner access and adequate net fee. **Team data:** Category acceptance, provenance cost, expert turnaround, completed referrals.

### Yachts and superyachts

**Target:** Owner, yacht manager or specialist broker. **Recurring task:** Surveys, cruising/use changes and renewal submissions.

**Potential remuneration:** Specialist placement or paid partner workflow. **Viability condition:** Net fee exceeds long sales-cycle and specialist work; partner relationship can recur. **Team data:** Decision maker, premium/fee share, acquisition hours, survey costs and payment lag.

### Leisure boats

**Target:** Private leisure owner vs marina-led channel. **Recurring task:** Mooring, use, records and renewal preparation.

**Potential remuneration:** Placement; earned renewal or marina workflow. **Viability condition:** Partner-sourced contribution positive after servicing; eligibility follows actual cover. **Team data:** Marina sourcing CAC, acceptance, usage rules, support and renewal rights.

### Supercars

**Target:** Single-car owner vs collectible fleet. **Recurring task:** Provenance, agreed value, mileage, storage and transfers.

**Potential remuneration:** Specialist placement and documented renewal rights. **Viability condition:** Specialist net remuneration covers verification and distribution; no premium-to-fee shortcut. **Team data:** Rollout status, collector/fleet mix, lead value, specialist effort and policy terms.

### Everyday cars

**Target:** Owner shopping at purchase or renewal. **Recurring task:** Quote, renewal and claims documentation.

**Potential remuneration:** Paid lead or binding/renewal commission. **Viability condition:** One-off contribution positive or later renewal payment actually belongs to Objais. **Team data:** Channel CAC, duplicate rejection, binding yield, commissions, renewal attribution.

### Pets

**Target:** Caregiving household vs occasional insurance shopper. **Recurring task:** Veterinary evidence, benefits and claims records.

**Potential remuneration:** Placement; contracted renewal or paid care/document service. **Viability condition:** Revenue funds recurring support; insurer integration makes workflow useful. **Team data:** Insurance vs assistance scope, support minutes, access to insurer systems and payer.

## Collectibles expansion

### TCGs and sports cards

**Target:** Casual player/bulk owner vs valuable adult collection. **Recurring task:** Batch additions, variants, trades, grading certificates and inventory.

**Potential remuneration:** Collection placement; genuinely paid repeat service; optional subscription. **Viability condition:** Insurable fraction and conversion sufficient, or paid-tool margin supports free usage. **Team data:** Collection values, insurable fraction, paid conversion, billed churn, scans and data licence cost.

### Action figures and designer toys

**Target:** Mass-market pieces vs boxed limited editions/statues. **Recurring task:** Edition, completeness, box condition, wish lists and inventory.

**Potential remuneration:** Collection placement; paid inventory or documented referral. **Viability condition:** Catalogue-defined niche and paid demand exceed matching/storage/licence costs. **Team data:** Exact variant coverage, collection value, cost per item and willingness to pay.

### Modern or certified coins

**Target:** Numismatic collection; bullion separate. **Recurring task:** Mint/date, certification, grade, provenance and swaps.

**Potential remuneration:** Specialist placement; appraisal referrals; paid documentation. **Viability condition:** Accepted specialist coverage and accurate documentation with controlled verification cost. **Team data:** Numismatic/bullion split, accepted grades, partner yield, certificate and appraisal costs.

### Archaeological antiquities and ancient coins

**Target:** Objects with documented provenance and lawful title. **Recurring task:** Provenance, title, expert attribution and movement records.

**Potential remuneration:** Specialist placement or paid expert documentation. **Viability condition:** Specialist acceptance and full costs proven before an automated mass-market offer. **Team data:** Title/provenance requirements by country, insurer acceptance, expert cost and responsibility.


Watch and jewellery collections provide a useful comparison with new collectibles because the documentation task is already plausible within advertised scope. Art and decorative antiques may support professional tools or completed expert referrals, but specialist labour can dominate costs. Yachts and supercars need net placement margin and repeated partner submissions measured explicitly. Cars and pets create recurring protection or care needs while the insurer may already own the servicing interface.

For TCGs the insurance unit is the owner and insurable collection or policy episode, not each inexpensive card. New cards can be absorbed into a collection policy. A US specialist offers additions and optional automatic collection growth alongside inventory requirements. This demonstrates why purchases need not create another paid lead. It is a product precedent, not Brazil or European availability. [Collectibles Insurance Services](https://collectinsure.com/pokemon-insurance/)

Figures need exact edition, condition and completeness records. Modern or certified coins can fit specialist documentation; bullion and ancient coins require separate treatment. Decorative antiques overlap current scope. Archaeological antiquities should not be the first mass-market retention test because specialist provenance and acceptance work materially change the cost structure.

## Segment the funnel rather than assign one market rate

For a collector insurance pathway, a diagnostic factorisation is q = s × d × alpha: s is the share of eligible acquired owners with an insurable collection, d request probability conditional on that segment, and alpha paid acceptance conditional on request. Multiple pathways require disjoint segments or an event ledger. More releases can raise visits without raising s or d. Use the correct time exposure for each rate.

For disjoint segments within a country/channel, acquired-owner weights pi_j give V_mix = sum_j pi_j V_j and CAC_mix = sum_j pi_j CAC_j. Valuable collectors subsidise casual free users only if the measured mix clears V_mix > CAC_mix after all casual-user costs. Owners with multiple asset classes must not be counted as newly acquired in every category: acquisition is charged once and distinct documented revenue events are attributed afterward.

# Brazil and Europe

Country, category, channel and contract require separate calibration in native currency. EUR examples are controlled comparisons and imply no Brazilian fee level. Do not add BRL, EUR and USD amounts. Manufacturer revenue, auction turnover, GMV, collection stock and premiums are different measures, none equal to Objais revenue. Market growth can inform a pilot audience; it cannot supply q, fee or acquisition cost.

For Brazil, obtain the local intermediary, insurer, category wording, accepted valuation basis, fees and channel history. The prior research found exclusions for some collectibles in one residential product; it does not establish the whole specialist market's availability. A coverage gap may create demand and reduce paid acceptance simultaneously. Obtain the actual offered product instead of assuming ordinary home coverage accepts a collection. [Brazil evidence in the collectibles research](Collectibles Market Research.md)

For Europe, start with a named country and verified partner. Portugal's specialist fine-art and valuable-goods offering is a useful precedent but establishes no Objais agreement or pan-European collector tariff. Separate UK and EU products. Each other-European-country template in the workbook must be named and split by actual contract/channel before commercial use. [Howden Portugal](https://www.howdengroup.com/pt-en/sector/fine-art-and-specie)

For older objects ask what provenance and movement documentation the actual jurisdiction, insurer and partner need and what it costs. For all categories, local replacement value, data licences, referral consent and insurer-accepted records are commercial dependencies. Their economic effects enter acceptance, costs, payment delays and the availability gate.

# Data to request from the team

P0 establishes current unit economics and the actual payment architecture. P1 establishes whether expansion or retention improves it. Ask for anonymised extracts tied by stable owner, event and policy keys; aggregates hide unpaid events, rejected leads and repeat users. No requests have been sent to the team.

## P0 Payment trigger and contract

**Suggested owner:** Commercial / finance. **Fields:** Counterparty, country, category, event basis, fee schedule, acceptance definition, payout split, reversal rules, renewal/service rights and attribution window. **Evidence:** Signed agreement and anonymised invoice examples. **Model use:** Architecture, f, omega, renewal-rights mask.

## P0 Actual operating scope

**Suggested owner:** Product / commercial. **Fields:** Live vs waitlist, supported country, local intermediary, insurer, category, accepted value range, required ownership/valuation documents. **Evidence:** Category-country availability matrix and acceptance record. **Model use:** Whether a modeled revenue stream is available.

## P0 Acquisition denominator and cost

**Suggested owner:** Growth / finance. **Fields:** Channel spend, attributable labour, partner fees, unique acquired owners, acquisition date, country, category and referral source. **Evidence:** Monthly channel exports, invoices and owner-level acquisition keys. **Model use:** CAC; avoid using CAC per paid lead with q a second time.

## P0 First payment funnel

**Suggested owner:** Product / commercial. **Fields:** Unique eligible owners, qualified requests, submission, acceptance/rejection reason, policy binding if relevant, dates and paid amount. **Evidence:** Owner/event-level anonymised funnel for all available history, ideally 12-24 months. **Model use:** p, alpha, q and paid-event delay.

## P0 Variable cost and servicing

**Suggested owner:** Finance / operations. **Fields:** AI/OCR calls, images/items, licensed-data charges, storage, payment/platform fees, support/expert minutes and wage rates, per policy costs. **Evidence:** Usage invoices, operational time samples and allocation rules. **Model use:** h, vE, vM, vS, vPolicy; costs of free users.

## P0 Invoices and collections

**Suggested owner:** Finance. **Fields:** Event ID, invoice date/amount, credits, due date, actual receipts, writeoffs, insurer share and currency. **Evidence:** Anonymised receivables and receipts ledger tied to event IDs. **Model use:** Net fees, cash lag, bad debt and working capital.

## P1 Continuation before and after payment

**Suggested owner:** Product / data. **Fields:** Cohort, first payment date, eligible state, post-payment state, meaningful task timestamps, deletion/contactability and exposure months. **Evidence:** Anonymised monthly owner/event panel with observation end. **Model use:** rhoE/rhoM with censoring; app visit frequency measured separately.

## P1 Genuine repeat eligibility

**Suggested owner:** Commercial / data. **Fields:** New asset/contract episode, relationship to first lead, consent, duplicate disposition, incremental accepted fee and date. **Evidence:** Repeat-event ledger plus explicit contract clause. **Model use:** lambda; never infer from scans or portfolio additions.

## P1 Renewals and revenue rights

**Suggested owner:** Insurance / finance. **Fields:** Policy births, term, premium, cancellation, renewal due/observed dates, surviving policies, actual renewal fees, service costs and ownership of book. **Evidence:** Mature policy cohorts and counterparty renewal statements. **Model use:** Policy survival and phiRenewal; young cohorts are censored.

## P1 Collector fit and willingness to pay

**Suggested owner:** Product / research. **Fields:** Category, owner vs dealer, collection-value bands, items, changes per month, existing tools, insured status, locale and completed protection need. **Evidence:** Consented targeted interviews plus paid pilot outcomes. **Model use:** Insurable fraction, q by segment, substitution and differentiation.

## P1 Paid tools and service referrals

**Suggested owner:** Product / finance. **Fields:** Offer exposure, actual payer, starts, billed renewal, cancellations/refunds, net recurring price, app-store/payment costs, completed referral fee. **Evidence:** Paid pilot or existing billing ledger; signed service terms. **Model use:** kappa, eta, b-vS and event-level referral margin.

## P1 Operating scale and concentration

**Suggested owner:** Finance / leadership. **Fields:** Actual fixed spend, incremental build/licence/integration cost, channel capacity, signed distribution reach, insurer concentration and currencies. **Evidence:** Management accounts, pipeline and partner channel history. **Model use:** Company profit, startup funding, concentration and obtainable volume.


Join owner acquisition date, category, country, segment and channel to qualified requests, submission, acceptance/rejection, binding, earned amount, credits and receipt dates. Join renewals by policy key and meaningful tasks/costs by owner and month. Request all available history, ideally 12–24 months, with observation-end dates. Recently acquired policies may not yet have had the chance to renew.

Estimate conversion by cohort and elapsed time. This month's paid leads divided by this month's new users is misleading when the funnel spans months. Treat incomplete cohorts as censored observations rather than failures. Meaningful task continuation, reachability, policy survival and paid subscription continuation are distinct: not logging in every month does not establish policy churn. Generic daily-active-user metrics cannot calibrate opportunity-state continuation by themselves.

Include partner labour, commissions and manual onboarding in total CAC. Include support, expert minutes, valuation licences, storage and inference in costs. Report fees by country/category/payer/channel. A verified absence of rights means zero renewal revenue; unknown contract terms remain unknown.

# Decision sequence

**Calibrate the current business first.** Populate P0 inputs and reconcile earned fees with invoices and cash. A low-frequency model is viable if first-event contribution covers acquisition and the obtainable volume covers operating costs. If contribution is negative, identify the exact fee, conversion or CAC gap before treating more visits as the remedy.

**Compare an existing collector lane with a new one.** Test watch/jewellery documentation against a targeted valuable adult TCG collection, using the same acquired-owner denominator. Log insurer-accepted records, time saved, actual payments and full service costs. Select the country only after verifying a counterparty; no Brazil or European coverage is assumed.

**Test a specific recurring payment.** A real paid-tool offer, earned renewal agreement, completed referral or paid professional workflow can convert usefulness into revenue. Repeat leads need an additional episode that is accepted and paid. Interviews measure needs; paid billing and fee ledgers measure revenue. A dealer/managing-professional workflow uses a different payer and acquisition unit and needs its own account-level model before B2B extrapolation.

**Scale against measured profit and cash.** Require contribution headroom after servicing, actual fixed/build costs, sales-cycle delays and obtainable channel capacity. Stress fee reductions, rejection, support and insurer concentration. The 360-combination grid varies q, payment, CAC, reset and paid conversion without assigning probabilities to those assumptions.

The strongest current hypothesis is a paid collection-protection/documentation relationship for a narrow valuable audience or a professional partner. TCGs are a useful test of recurring utility; their financial advantage remains conditional on paid demand and earned recurring remuneration. High app use is a product signal. The event and billing ledgers establish whether it creates revenue.

# Deliverables and validation

The workbook contains ten editable synthetic cohort/calendar cases, inverse thresholds, a 14-market mechanism matrix, 56 category-country input templates, the 360-combination static stress grid, sources and the team-data request. Actual economics inputs begin blank. Other-European and other-global templates require named countries and channels; the templates do not establish operating coverage.

The mathematical specification and Python reference remain model authority. This application checks inverse fee and paid-conversion thresholds against that reference and evaluates spreadsheet formulas independently. Native Excel recalculation, empirical forecasts and completed customer experiments are not claimed.

The PDF and Word document preserve the comparison. The data request is also available as research/market-model/Team Data Request.csv. Existing market reports retain the broader quantitative evidence and original source registers.
