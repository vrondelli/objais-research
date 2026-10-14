# Objais research and revenue model

Independent research to help assess how Objais can earn enough from its current service, and what would have to change for future options to work. Start with the two reader guides; they connect the people, service events, formulas and numerical examples.

1. [Revenue guide](<Objais Revenue Model Numerical Summary.md>) — acquisition, first fees, retention, repeat eligibility, renewals, paid software and cash.
2. [Acquisition guide](<Objais Acquisition Numerical Summary.md>) — how attention becomes a serviceable enquiry, what advertising can afford and where current products could reach owners.
3. [Shared glossary](<Objais Glossary.md>) — definitions when needed, without interrupting the examples.
4. [Review notes and evidence needed](<Review Notes.md>) — what is established, what remains assumed and what the team needs to supply.

**The economic examples are synthetic, not Objais performance or forecasts.** Lead selling is a working assumption. Objais's [public FAQ](https://objais.com/en/faq) describes insurance-company commissions and specialist referrals; contracts, earning conditions, renewal rights and observed retention were not supplied. Current advertised products and optional future offers are kept separate. The research covers global evidence, with Brazil and European countries highlighted; the acquisition examples start with Portugal.

## Supporting research

| Question | Read |
| --- | --- |
| What does the company advertise? | [Company and product report](<Objais Research Report.md>), [current markets](<Objais Current Markets Research.md>) |
| Could collectibles change the economics? | [Collectibles markets](<Collectibles Market Research.md>), [market revenue comparison](<Objais Market Revenue Comparison.md>) |
| Where could current categories reach owners? | [Established offers and category strategy](<Objais Established Offers and Category Capture Strategy.md>), [pets](<Objais Pets Market Capture Research.md>), [boats](<Objais Boats Market Capture Research.md>), [jewellery](<Objais Jewellery Market Capture Research.md>), [watches](<Objais Watches Market Capture Research.md>) |
| What exposure can be bought? | [Platforms](<Objais Advertising Platforms Research.md>), [outside advertising inventory](<Objais External Advertising Inventory Research.md>), [prices and requirements](<Objais Advertising Prices and Requirements.md>) |
| How would the team measure it? | [Funnels](<Objais Funnels Research.md>), [metrics](<Objais Metrics Research.md>), [measurement and attribution](<Objais Measurement and Attribution Research.md>), [UX](<Objais User Experience Research.md>), [experiments](<Objais Acquisition Experiments Research.md>) |
| What is the full mathematical specification? | [Formal model](<Objais Revenue Model.tex>), [calculator notes](research/revenue-model/README.md) |

The guides show diagrams directly in GitHub and include compact formula images. The [HTML diagram gallery](<Objais Revenue Model Diagrams.html>) can also be downloaded and opened locally. Markdown is the reviewed reading version; older PDF and Word exports are omitted.

The model workbook has live formulas for its stationary benchmarks and acquisition curve. Advanced cohort sheets are Python-generated snapshots: changing their cells does not recalculate those forecasts. The measurement workbook contains blank observed-value fields and illustrative calculations.

## Reproduce the examples

Clone the repository, enter its directory, then run with Python 3.10 or newer. The calculations and checks use the standard library:

```bash
python3 -m unittest discover -s research/revenue-model -p 'test_*model.py'
python3 research/publication/rebuild.py
python3 research/publication/check_package.py
```

The rebuild regenerates the 15 extended scenarios, 52 benchmark sensitivity experiments, revenue guide, glossary and SVG formula sources. It preserves the manually edited acquisition guide. It converts generated links to relative paths and runs the existing arithmetic and terminology checks. PNGs are committed so readers need no rendering tools. Rebuilding PNGs after changing panel geometry requires Node.js and Playwright:

```bash
npm install
npx playwright install chromium
npm run render:formulas
python3 research/formulas/validate_formula_figures.py
```

Use the SVG and PNG together after a panel edit. Browser fonts can change image pixels without changing the calculation. The revenue diagrams are also available as Mermaid sources in `research/revenue-summary/diagrams/`.

Public-source registers retain dates, scopes and limitations. Most market research was collected on 13 October 2026; selected core company pages were checked again on 14 October. Publisher list prices are dated observations, not campaign quotes. The package contains research, synthetic scenarios and templates; it does not contain customer records, contracts, credentials or downloaded third-party source archives.

Anyone with this public repository link can read the material without joining the repository. Team members can use GitHub issues to provide corrections or discuss assumptions; confidential contracts or customer data should be supplied through the team's existing private channel.
