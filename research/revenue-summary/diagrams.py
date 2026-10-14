"""Editable Mermaid explanations for the current/future revenue framework."""
from pathlib import Path
import json

DIAGRAMS=[
 dict(id='actors',title='Who helps and who pays',source='''flowchart TB
    subgraph Service["Service relationships"]
      direction TB
      Owner["Asset owner<br/>or representative"] -->|"Records and request"| Objais["Objais"]
      Acquisition["Acquisition partner"] -->|"Introduces owners"| Objais
      Objais -->|"Enquiry"| Partner["Insurer or broker partner"]
      Objais -.->|"Optional introduction"| Expert["Independent service provider"]
    end
    subgraph Economics["Fees and costs"]
      direction TB
      FeePartner["Insurer or broker partner"] -->|"Fee if earned"| Fees["Objais"]
      FeeOwner["Asset owner"] -.->|"Optional service fee"| Fees
      FeeExpert["Service provider"] -.->|"Referral fee if earned"| Fees
      Fees -->|"Software and data cost"| Supplier["Technology supplier"]
      Fees -->|"Acquisition cost if incurred"| CostPartner["Acquisition partner"]
    end
    Service ~~~ Economics
    classDef platform fill:#173247,color:#fff,stroke:#173247;
    classDef party fill:#eaf3f5,color:#173247,stroke:#007d89;
    class Objais,Fees platform;
    class Owner,Partner,Acquisition,Supplier,Expert,FeePartner,FeeOwner,FeeExpert,CostPartner party;''',
  caption='The top half shows the service; the bottom half shows the money. The same people appear in both. Dashed lines show possible arrangements, and a fee owed may arrive later. Actual partners and payment terms still need confirmation.'),
 dict(id='opportunity-states',title='A customer can return without starting over',source='''flowchart TB
    New["New owner<br/>Acquisition charged once"] --> E["E: active unpaid opportunity"]
    DE["D_E: dormant unpaid"] -->|"Returns; reactivation cost"| E
    DM["D_M: dormant after payment"] -->|"Returns without new eligibility"| M["M: active completed opportunity"]
    DM -.->|"Return with genuine new eligibility"| E
    E --> Gate{"Need, request and acceptance;<br/>history permits payment?"}
    Gate -->|"Paid event within capacity"| M
    Gate -->|"No payment; continues"| EN["E next month"]
    M -->|"Continues; no new eligibility"| MN["M next month"]
    M -.->|"Genuine new eligibility"| EN
    E -->|"Becomes dormant"| DEN["D_E next month"]
    M -->|"Becomes dormant"| DMN["D_M next month"]
    E -->|"Leaves permanently"| X["X: permanent exit"]
    M -->|"Leaves permanently"| X
    DE -->|"Leaves permanently"| X
    DM -->|"Leaves permanently"| X
    classDef active fill:#eaf3f5,color:#173247,stroke:#007d89;
    classDef sleeping fill:#fff4df,color:#173247,stroke:#b88b67;
    class New,E,M,EN,MN active;
    class DE,DM,DEN,DMN sleeping;''',
  caption='Someone can go quiet and return with the same customer record and payment history. The dashed paths need a genuinely new payable opportunity; returning does not clear payment limits. Insurance cover and software billing can continue separately.'),
 dict(id='independent-clocks',title='Three relationships that can last different lengths of time',source='''flowchart TB
    subgraph Opportunity["Opportunity relationship"]
      direction LR
      E["Eligible opportunity"] -->|"First paid event"| M["Completed opportunity"]
      M -->|"Continued app relationship alone"| M
    end
    subgraph Software["Optional paid software"]
      direction LR
      Start["Owner starts paying"] --> Bill["Billed month"]
      Bill -->|"Billed continuation and next month"| Bill
      Bill -->|"Billing stops"| Stop["No further software fee"]
    end
    subgraph Insurance["Insurance policy"]
      direction LR
      Bind["Policy bound"] --> Active["Policy remains in force"]
      Active -->|"Survives to renewal date"| Renew["Renewed policy term"]
      Renew --> Active
      Renew -.->|"Only with renewal payment rights"| Fee["Earned renewal fee"]
    end
    Opportunity ~~~ Software
    Software ~~~ Insurance''',
  caption='The same person can have all three relationships. One may end while another continues. Software billing and policy renewal do not require a monthly app visit.'),
 dict(id='events',title='From an enquiry to an earned fee',source='''flowchart TB
    Use["Owner uses the service"] --> Record["Record or estimate updated<br/>Usage cost; no automatic fee"]
    Record -->|"Owner requests insurance"| Request["Qualified enquiry submitted"]
    Record -->|"No request"| Continue["Continue or leave<br/>No insurance fee"]
    Request --> Agreement{"Which event does<br/>the agreement pay for?"}
    Agreement --> Lead["Partner accepts a payable lead"]
    Agreement --> Bind["Policy bound under<br/>a commission arrangement"]
    Agreement --> Unpaid["Rejected, pending or not payable<br/>No earned fee yet"]
    Lead --> Earn["Unique event earns its agreed fee"]
    Bind --> Earn
    Earn --> Invoice["Invoice or payment statement<br/>Same earned fee"]
    Invoice --> Receipt["Cash received later<br/>Same fee collected"]''',
  caption='The agreement decides whether the fee is earned when a lead is accepted or cover starts. Both payments belong together only with separate contractual rights. Invoicing and collection follow the fee already earned.'),
 dict(id='cash',title='Earning the fee and receiving the money',source='''flowchart TB
    Event["Payable event occurs"] --> Revenue["Earned revenue"]
    Revenue --> Profit["Operating result<br/>Revenue less variable,<br/>acquisition and fixed costs"]
    Event --> Invoice["Invoice or payment statement"]
    Invoice --> Due["Receivable<br/>Amount awaiting collection"]
    Due -->|"Payment received"| Receipts["Cash receipts"]
    Receipts --> Balance["Cash result<br/>Receipts less expenses paid"]
    Costs["Costs and expenses"] -->|"Cost incurred"| Profit
    Costs -->|"Expense paid"| Balance
    classDef earned fill:#eaf3f5,color:#173247,stroke:#007d89;
    classDef waiting fill:#fff4df,color:#173247,stroke:#b88b67;
    class Revenue,Profit,Receipts,Balance earned;
    class Due waiting;''',
  caption='A fee can be earned before it is paid. That difference matters when bills are due in the meantime. Receiving the money settles what was owed; it does not earn another fee.'),
 dict(id='scope',title='The same questions for existing and future offers',source='''flowchart TB
    Current["Current researched categories<br/>Art, valuables, vehicles,<br/>boats and pets"] --> Inputs["Inputs for each segment<br/>Category, country, channel,<br/>payment agreement, timing<br/>and acquisition cost curve"]
    Existing["Changes within existing scope<br/>Better acquisition or conversion;<br/>earned renewals or paid services"] --> Inputs
    Future["Optional future categories<br/>or countries"] -.->|"Measure local inputs"| Inputs
    Business["Optional professional offers"] -.->|"Adapt account unit<br/>and event counts first"| Inputs
    Inputs --> Model["Cohorts, paid events,<br/>continuation, costs and collections"]
    Model --> Unit["Customer contribution<br/>and break-even thresholds"]
    Model --> Profit["Company operating result"]
    Model --> Cash["Cash result and funding needs"]
    classDef core fill:#173247,color:#fff,stroke:#173247;
    classDef option fill:#eaf3f5,color:#173247,stroke:#007d89;
    class Model core;
    class Current,Existing,Future,Business,Inputs,Unit,Profit,Cash option;''',
  caption='Whatever the asset, the business still needs a payer, a reason for payment and costs it can cover. A new category changes those assumptions; it does not guarantee a better result.'),
]

_ORDER=['actors','events','opportunity-states','independent-clocks','cash','scope']
DIAGRAMS.sort(key=lambda d:_ORDER.index(d['id']))

def diagram(key):
 d=next(d for d in DIAGRAMS if d['id']==key)
 return '\n\n```mermaid\n'+d['source']+'\n```\n\n'+d['caption']+'\n'

def export_diagrams(output_dir):
 output_dir.mkdir(parents=True,exist_ok=True)
 for d in DIAGRAMS:
  (output_dir/(d['id']+'.mmd')).write_text(d['source']+'\n',encoding='utf-8')
 (output_dir/'diagrams.json').write_text(json.dumps(DIAGRAMS,indent=2),encoding='utf-8')
