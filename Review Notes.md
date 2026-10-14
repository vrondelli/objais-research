# Review notes and evidence needed

Reviewed 14 October 2026. The two guides explain the same model from different starting points: the revenue guide follows distinct owners over time; the acquisition guide follows observable interactions until owners and payment outcomes can be identified. Their counting units are deliberately different.

## What changed in this review

The eight formula panels now use short arrow labels and one numerical example each. Their combined height fell from 3,150 to 2,120 pixels, about 33%, at the same 900-pixel width. Repeated values and explanations were removed; the worked steps needed to understand the first contribution calculation remain. Definitions stay in the shared glossary and links appear at selected first uses.

The review corrected or qualified these assumptions:

| Assumption that could mislead | How to read the model |
| --- | --- |
| Objais has no retention | No observed retention data was supplied. Advertised updates and notifications do not establish return rates. Occasional need and dormancy are scenarios to test. |
| Objais earns a fee whenever a lead is accepted | The agreement must specify the earning condition. The public FAQ describes commissions and specialist referrals, without verifying lead-sale terms. |
| App retention produces repeat revenue | Further first conversions, genuinely new payable opportunities, policy renewals and software billing are separate mechanisms. Continued use can also add costs. |
| Collectors use services frequently, so they will pay Objais | Activity is not paid demand. Card tools, local insurance availability, paid starts and billing continuation need separate evidence. |
| Higher request yield proves stronger intent | It improves the synthetic example. The cause could be targeting, interface, qualification or partner fulfilment; the rate alone does not identify it. |
| Every click, asset or representative is another owner | Owner identity must be preserved. The acquisition example does not infer a distinct-owner count from 1,000 clicks. |
| A positive customer contribution means company profit | Customer examples exclude fixed costs. Company forecasts also have younger cohorts, overhead and collection delays. |
| Global market size is Objais revenue potential | Market observations describe different products, countries, currencies and dates. They cannot be added into an Objais forecast without local conversion, fee and cost evidence. |

The stationary formal model writes `q = p × α`, absorbing need into its request probability. The expanded model and guides write `q = n × p × α`, with requests conditional on need. These are compatible conventions, not interchangeable input fields. The expanded Python model has a legacy fallback that uses `Parameters.q` as its qualified-request probability when no explicit value is given; supply need, qualified-request probability and paid acceptance explicitly when calibrating it.

The original formal-model software benchmark uses 5% paid starts. The guide's lead-plus-software arrangement uses 15% and compares other rates. They are different synthetic scenarios, not contradictory measured results.

## What the team needs to supply

| Evidence | What it resolves |
| --- | --- |
| Contracts, fee statements and credits | Payer, earning trigger, retained fee, reversal conditions, repeat-payment limits and renewal rights. |
| Acquisition spend and identified-owner records by date, category, country and channel | Full CAC, adoption, attribution, audience limits and how costs change with scale. |
| Task, request and return histories, including who performs the task | Need frequency, dormant return, delegated use, qualification and actual payment yield. |
| Policy and software billing histories | Independent renewal and billing continuation, paid demand, cancellations and eligibility. |
| Service costs, capacities, invoices and receipts | Active and dormant costs, reactivation, processing, overhead, delivery limits and collection delays. |

Keep EUR and BRL scenarios separate unless an explicit exchange-rate convention is chosen. Recent cohorts cannot establish annual renewal behaviour, and a small advertising test cannot establish acquisition costs at a much larger budget.

## Limits and validation

The model follows expected consumer-owner counts; fractional outputs represent averages. Direct and delegated groups must be mutually exclusive. Professional accounts serving several clients need a different counting unit. The examples assume constant fees or specified schedules, rather than predicting competitor behaviour.

Shared partner capacity must be allocated across segments before simulation. A standalone customer projection may differ from its contribution inside a capacity-constrained growing business. Later software upgrades, service backlogs and other referral fee types need additional rules. The simplified cash examples exclude development investment, tax, bad debt and late credits and use one collection delay per segment.

Validation passed: 48 existing model tests, 52 sensitivity experiments with 64 checks, 15 extended scenarios, 13 independent formula-to-model comparisons, eight browser-rendered panels and the glossary/acquisition link and arithmetic checks. Input files for the worked examples were unchanged by the editorial review. Public-package checks additionally verify relative document/image links and exclude machine paths and private session references. These checks establish internal consistency; they do not validate the commercial inputs.

Most supporting market and advertising research is a dated baseline from 13 October 2026. Selected official company pages were refreshed on 14 October: [FAQ](https://objais.com/en/faq), [how it works](https://objais.com/en/how-it-works), [insurance](https://objais.com/en/insurance), [privacy](https://objais.com/en/privacy) and [Business](https://objais.com/en/business). Advertised scope is not proof of successful fulfilment in each country. Sources, including public price observations, need checking again before a commercial decision.
