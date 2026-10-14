"""Compact arrow-labelled panels for the existing synthetic model examples."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
NAVY, TEAL, GREY = '#173247', '#007d89', '#425966'
panels = []


def text(x, y, value, size=17, color=NAVY, weight=400):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(value)}</text>'


def term(x, y, value, sub=None, sup=None, size=36, result=False):
    s=f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{("#9be7dc" if result else "#ffffff")}" font-weight="700">{escape(value)}'
    if sub is not None:s+=f'<tspan baseline-shift="sub" font-size="{size*.58}">{escape(sub)}</tspan>'
    if sup is not None:s+=f'<tspan baseline-shift="super" font-size="{size*.58}">{escape(sup)}</tspan>'
    return s+'</text>'


def strip(y=44,height=58,x=20,width=860):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="9" fill="{NAVY}"/>'


def label(sx, cx, title, meaning, sy=105, y=140, width=172):
    # One symbol label and one short explanation; example values appear once below.
    return (f'<path d="M{sx},{sy} L{cx},{(y+27 if sy>y+30 else y-19)}" stroke="{TEAL}" stroke-width="1.6" marker-end="url(#arrow)"/>'
            f'<circle cx="{sx}" cy="{sy}" r="2.3" fill="{TEAL}"/>'
            f'<g class="annotation" data-min-x="{cx-width/2}" data-max-x="{cx+width/2}">'
            +text(cx,y,title,17,TEAL,700)+text(cx,y+21,meaning,16)+ '</g>')


def example(y, value, size=22):
    return f'<rect x="20" y="{y}" width="860" height="42" rx="8" fill="#fff1e9"/>'+text(450,y+29,value,size,'#913f20',700)


def save(identifier,title,height,content,formula,description,source):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc><defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5.5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="{TEAL}"/></marker></defs><rect x="1" y="1" width="898" height="{height-2}" rx="12" fill="white" stroke="#cbdce2"/><g font-family="Arial, sans-serif">{text(450,28,title,22,NAVY,700)}{content}</g></svg>'''
    (OUT/(identifier+'.svg')).write_text(svg+'\n')
    panels.append(dict(id=identifier,title=title,description=description,formula=formula,source=source,width=900,height=height))


c=strip()
for x,v in [(180,'q'),(270,'='),(360,'n'),(450,'×'),(535,'p'),(620,'×'),(715,'α')]:c+=term(x,85,v,size=42,result=v=='q')
for sx,cx,title,meaning in [(180,150,'q · First-fee chance','Per eligible owner-month'),(360,350,'n · Needs help','This month'),(535,550,'p · Qualified request','Given that need'),(715,750,'α · Objais earns','Given a qualified request')]:c+=label(sx,cx,title,meaning,width=195)
c+=text(450,193,'Conditional chances; payment-history limits and delivery capacity still apply.',15,GREY)
save('payment-chance','Chance of earning the first fee',211,c,'q = n × p × α','q: first-fee chance per eligible owner-month; n: need; p: qualified request given need; alpha: contractual fee earned given a qualified request.','Objais Revenue Model.tex; monthly need extension')

c=strip(y=100)
for x,v in [(89,'C / A'),(160,'='),(208,'q'),(245,'×'),(274,'['),(303,'f'),(338,'×'),(370,'('),(394,'1'),(428,'−'),(468,'ω'),(502,')'),(535,'−'),(570,'h'),(601,']'),(633,'−'),(730,'−'),(792,'k')]:c+=term(x,141,v,size=34,result=v=='C / A')
c+=term(680,141,'v',sub='E',size=34)
for sx,cx,title,meaning in [(89,95,'C / A · Result','Per acquired owner'),(303,305,'f · Fee','Per payable event'),(570,575,'h · Processing','Per payable event'),(792,795,'k · Acquisition','Per new owner')]:c+=label(sx,cx,title,meaning,sy=111,y=54,width=195)
for sx,cx,title,meaning in [(208,200,'q · Payment chance','Share earning a first fee'),(468,450,'ω · Reversals','Share of fees withdrawn'),(680,710,'v_E · Service cost','Per owner this month')]:c+=label(sx,cx,title,meaning,sy=161,y=194,width=225)
c+=example(232,'10% × [ €20 × (1 − 5%) − €1 ] − €0.20 − €4 = −€2.40')
c+=text(450,297,'One-visit example; fixed costs excluded. C is group contribution; A is original acquired owners.',15,GREY)
save('owner-contribution','One-visit contribution per acquired owner',315,c,'C / A = q × [f × (1 − ω) − h] − v_E − k','C/A is group contribution per acquired owner, with fee reversals and processing deducted before multiplying by payment chance, then owner service and acquisition deducted. Numerical result minus 2.40 euros, before overhead.','Objais Revenue Model.tex; minimal one-visit model')

c=strip()
for x,v in [(95,'5%'),(180,'×'),(280,'50%'),(365,'×'),(455,'€18'),(545,'−'),(635,'€0.10'),(720,'='),(810,'€0.35')]:c+=term(x,85,v,size=38,result=v=='€0.35')
for cx,title,meaning in [(95,'Requests / clicks','50 / 1,000'),(280,'Payable / requests','25 / 50'),(455,'Retained / paid lead','After fee deductions'),(635,'Other service cost','Per entry click'),(810,'Ad cost ceiling','Per click; no overhead')]:c+=label(cx,cx,title,meaning,y=140,width=174)
c+=text(450,193,'Extra introduction, setup or onboarding costs leave less available for advertising.',15,GREY)
save('click-cost-ceiling','Maximum advertising cost per click',211,c,'5% × 50% × €18 − €0.10 = €0.35','5 percent requests per entry click times 50 percent payable requests times 18 euros retained per paid lead, less 0.10 euros other cost per click, leaves 0.35 euros for advertising.','Objais Funnels Advertising Metrics and UX Research.md; acquisition limits')

c=strip(x=20,width=415)+strip(x=465,width=415)
for offset,state,sign in [(0,'E','−'),(445,'M','+')]:
    for x,v,sub in [(74,state,'next'),(143,'=',None),(205,'ρ',state),(254,'×',None),(280,'(',None),(305,state,None),(340,sign,None),(371,'L',None),(401,')',None)]:c+=term(x+offset,85,v,sub=sub,size=27,result=sub=='next')
    labels=[(74,67,'Next '+state,'Awaiting fee' if state=='E' else 'Fee earned'),(205,190,'ρ_'+state+' · Stay','Before fee' if state=='E' else 'After fee'),(305,295,state+' · Now','Awaiting fee' if state=='E' else 'Fee earned'),(371,393,'L · Leads','Payable now')]
    for sx,cx,title,meaning in labels:c+=label(sx+offset,cx+offset,title,meaning,y=138,width=106)
    c+=text(227+offset,198,'80% × (1,000 − 100) = 720' if state=='E' else '80% × (0 + 100) = 80',21,NAVY,700)
c+=text(450,230,'Fee earnings belong to Objais. This simple case has no dormant return and no eligibility reset (λ = 0).',15,GREY)
save('retention-states','Retention before and after the first fee',247,c,'E_next = ρ_E × (E − L); M_next = ρ_M × (M + L)','E waits for a first fee; M has already earned Objais a fee; L is new paid leads. At 80 percent continuation, next month has 720 waiting owners and 80 completed owners, without dormancy or reset.','Objais Revenue Model.tex; one-opportunity retention')

c=strip(height=82)
c+=term(92,99,'U',sub='36',result=True)+term(180,99,'=')+term(267,99,'Σ',size=43)+text(267,60,'35',16,'white',700)+text(267,119,'a = 0',14,'white',700)+term(435,99,'δ',sup='a')+term(532,99,'C',sub='a')+term(650,99,'/')+term(810,99,'A')
for sx,cx,title,meaning in [(92,92,'U36 · Per owner','36-month contribution'),(267,272,'Σ · Add months','a = 0 through 35'),(435,452,'δᵃ · Time weight','δ = 1 / 1.01'),(532,632,'C_a · Month result','Net group result'),(810,812,'A · Original group','All 1,000 acquired')]:c+=label(sx,cx,title,meaning,sy=129,y=164,width=174)
c+=example(201,'( −€2,400 + €1,128 / 1.01 + … ) / 1,000 = +€1.17')
c+=text(450,269,'Includes all 36 months. Acquisition charged once at joining; fixed overhead excluded.',15,GREY)
save('retained-contribution','From monthly results to contribution per owner',287,c,'U_36 = Σ(a=0..35) δ^a C_a / A','Sum all monthly group contributions at a one percent monthly discount, then divide by the original cohort. Acquisition is already included once in month 1. Result 1.17 euros before fixed costs.','Objais Revenue Model.tex; equivalent finite V_H minus k')

c=strip()
for x,v,sub in [(115,'ΔE',None),(220,'=',None),(305,'ρ','M'),(382,'×',None),(457,'λ',None),(532,'×',None),(590,'(',None),(645,'M',None),(705,'+',None),(765,'L',None),(822,')',None)]:c+=term(x,85,v,sub=sub,result=v=='ΔE')
for sx,cx,title,meaning in [(115,112,'ΔE · New eligibility','Existing owners return'),(305,338,'ρ_M · Continue','After first fee'),(457,550,'λ · Reset','Share gaining a new right'),(705,780,'M + L · Completed','Existing + newly completed')]:c+=label(sx,cx,title,meaning,y=141,width=208)
c+=example(182,'80% × 10% × ( 0 + 100 ) = 8 newly eligible owners')
c+=text(450,248,'Next month: E = 720 + 8 = 728; M = 80 − 8 = 72. Eligibility is not another earned fee.',15,GREY)
save('repeat-eligibility','A new opportunity needs a genuine payment right',267,c,'ΔE = ρ_M × λ × (M + L)','80 percent continuation and 10 percent reset applied to 100 completed owners gives 8 newly eligible owners. Existing owner identity remains; another fee needs its own valid payment condition.','Objais Revenue Model.tex; repeat-eligibility transition')

c=strip()
for x,v,sub,sup in [(92,'R',None,'π'),(184,'=',None,None),(277,'z','π',None),(365,'×',None,None),(452,'B',None,None),(545,'×',None,None),(635,'ζ','12',None),(718,'×',None,None),(810,'φ',None,'π')]:c+=term(x,85,v,sub=sub,sup=sup,result=v=='R')
for cx,title,meaning in [(92,'Rπ · Renewal fees','Original policy group'),(277,'zπ · Payment right','Granted = 1; else 0'),(452,'B · Policies started','100 from 1,000 owners'),(635,'ζ12 · Eligible','After 12 months'),(810,'φπ · Renewal fee','€15 per renewal')]:c+=label(cx,cx,title,meaning,y=141,width=173)
c+=example(183,'1 × 100 × 0.98¹² × €15 = €1,177.08 renewal revenue')
c+=text(450,249,'Month 13, before policy costs. No renewal payment right (zπ = 0) means €0 earned.',15,GREY)
save('policy-renewal','Renewal revenue at the first annual due date',267,c,'Rπ = zπ × B × ζ12 × φπ','For one original policy group at age 12 months: payment rights times 100 started policies times 98 percent monthly eligibility to power 12 times 15 euro renewal fee, earning 1177.08 euros before policy costs. Without rights, zero.','Objais Revenue Model.tex; one cohort annual renewal')

c=strip(y=100)
for x,v,sub,sup in [(100,'C',None,'S'),(193,'=',None,None),(252,'κ',None,None),(310,'×',None,None),(365,'A',None,None),(425,'×',None,None),(480,'η',None,'a'),(555,'×',None,None),(589,'(',None,None),(620,'b',None,None),(669,'−',None,None),(728,'v','S',None),(780,')',None,None)]:c+=term(x,141,v,sub=sub,sup=sup,result=v=='C')
for sx,cx,title,meaning in [(100,110,'Cˢ · Software part','This cohort-month'),(365,375,'A · Original owners','1,000 here'),(620,700,'b · Net monthly payment','€3 per paid account')]:c+=label(sx,cx,title,meaning,sy=112,y=54,width=255)
for sx,cx,title,meaning in [(252,210,'κ · Paid starts','Share of all new owners'),(480,465,'ηᵃ · Billing continuation','η = 95%/month; a = 1'),(728,730,'v_S · Extra account cost','€0.50 per paid month')]:c+=label(sx,cx,title,meaning,sy=161,y=194,width=250)
c+=example(232,'15% × 1,000 × 95%¹ × ( €3 − €0.50 ) = €356.25')
c+=text(450,297,'Month 2 software component; acquisition, shared work and fixed costs accounted for separately.',15,GREY)
save('paid-software','Paid software follows its own billing clock',315,c,'C^S_a = κ × A × η^a × (b − v_S)','Software monthly contribution is paid-start share times original owners times billing continuation to age a times net price less extra account cost. Month 2 gives 356.25 euros, before acquisition, shared costs and fixed overhead.','Objais Revenue Model.tex; software cohort billing and extra account cost')

(OUT/'panels.json').write_text(json.dumps(panels,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'svg_panels':len(panels),'combined_height':sum(p['height'] for p in panels)}))
