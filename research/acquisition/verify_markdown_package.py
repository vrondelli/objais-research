"""Check deliverable coverage, local links and the central guide's arithmetic."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
DATA=Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'research/glossary'))
from linking import validate_local_target
manifest=json.loads((DATA/'markdown-package.json').read_text(encoding='utf-8'))
source=Path(manifest['source'])
if not source.is_absolute():
    source=ROOT/source
assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['source_sha256']

base={'impressions':20000,'clicks':1000,'photo_journeys_started':600,'usable_estimate_journeys':400,'request_share_of_estimates':.125,'qualification_share_of_requests':.8,'payable_share_of_requests':.5,'fee_eur':20,'reversal_share':.05,'processing_per_payable_event_eur':1,'other_variable_cost_per_click_eur':.1,'media_cpc_eur':.5}

def outcome(p):
    requests=p['usable_estimate_journeys']*p['request_share_of_estimates']
    qualified=requests*p['qualification_share_of_requests']
    payable=requests*p['payable_share_of_requests']
    gross=payable*p['fee_eur']
    net=gross*(1-p['reversal_share'])
    processing=payable*p['processing_per_payable_event_eur']
    other=p['clicks']*p['other_variable_cost_per_click_eur']
    media=p['clicks']*p['media_cpc_eur']
    per_payable=p['fee_eur']*(1-p['reversal_share'])-p['processing_per_payable_event_eur']
    click_payable_share=payable/p['clicks']
    ceiling=click_payable_share*per_payable-p['other_variable_cost_per_click_eur']
    return {'requests':requests,'qualified':qualified,'payable_events':payable,'ctr':p['clicks']/p['impressions'],'cpm_eur':media/p['impressions']*1000,'first_usable_estimate_rate':p['usable_estimate_journeys']/p['photo_journeys_started'],'gross_fees_eur':gross,'net_fees_eur':net,'processing_eur':processing,'other_variable_cost_eur':other,'media_eur':media,'contribution_eur':net-processing-other-media,'per_payable_contribution_eur':per_payable,'media_cost_per_request_eur':media/requests,'media_cost_per_qualified_eur':media/qualified,'media_cost_per_payable_eur':media/payable,'media_cpc_ceiling_eur':ceiling,'media_cpa_ceiling_eur':ceiling/click_payable_share,'revenue_roas':net/media}

scenarios=[('base',{}),('more_usable_estimates',{'usable_estimate_journeys':500}),('more_intent',{'request_share_of_estimates':.2}),('higher_payable_share',{'payable_share_of_requests':.7}),('lower_cpc',{'media_cpc_eur':.35}),('more_expensive_route_with_more_intent',{'media_cpc_eur':.8,'request_share_of_estimates':.3})]
examples=[]
for name,changes in scenarios:
    inputs={**base,**changes};results=outcome(inputs)
    examples.append({'name':name,'evidence_status':'Illustrative assumptions; expected counts, not observed people','inputs':inputs,'results':results})
expected_contribution=[-150,-37.5,120,30,0,180]
expected_payable=[25,31.25,40,35,25,60]
for r,c,p in zip(examples,expected_contribution,expected_payable):
    assert abs(r['results']['contribution_eur']-c)<1e-9
    assert abs(r['results']['payable_events']-p)<1e-9
assert abs(examples[0]['results']['media_cpc_ceiling_eur']-.35)<1e-9
assert abs(examples[0]['results']['media_cpa_ceiling_eur']-14)<1e-9
assert abs(examples[0]['results']['revenue_roas']-.95)<1e-9
cash={'assumptions':'All entry/processing/acquisition costs paid in month 1; net fees collected in month 2; no additional cohort cost; fixed overhead excluded','month_1_receipts_eur':0,'month_1_costs_paid_eur':625,'month_1_cash_eur':-625,'month_2_receipts_eur':475,'month_2_costs_paid_eur':0,'month_2_cash_eur':475,'cumulative_cash_eur':-150}
assert cash['month_1_cash_eur']+cash['month_2_cash_eur']==examples[0]['results']['contribution_eur']
community={'evidence_status':'Illustrative assumptions; no observed community conversion','operator_recruitment_and_onboarding_brl':200,'promotion_brl':100,'coordination_brl':100,'new_identified_owners':40,'total_acquisition_cost_brl':400,'owner_cac_brl':10}
assert sum(community[k] for k in ['operator_recruitment_and_onboarding_brl','promotion_brl','coordination_brl'])==community['total_acquisition_cost_brl']
assert community['total_acquisition_cost_brl']/community['new_identified_owners']==community['owner_cac_brl']
(DATA/'central-examples.json').write_text(json.dumps({'scope':'Simplified linked entry cohorts; no unique owner count inferred; independent sensitivity comparisons; common costs held fixed','scenarios':examples,'cash_timing':cash,'community_acquisition':community},indent=2)+'\n',encoding='utf-8')

files=[ROOT/manifest['central'],*[ROOT/n for n in manifest['topic_files']]]
link_count=0
for path in files:
    text=path.read_text(encoding='utf-8')
    assert len(re.findall(r'^# ',text,re.M))==1, path.name
    assert text.count('```')%2==0, path.name
    assert '\ufffd' not in text, path.name
    for target in re.findall(r'\]\(<([^>]+)>\)',text):
        validate_local_target(target)
        link_count+=1
    for target in re.findall(r'\]\((/[^)]+)\)',text):
        validate_local_target(target)
        link_count+=1
    lines=text.splitlines()
    widths=[]
    for line in lines+['']:
        if line.startswith('|'):
            widths.append(len(line.strip('|').split('|')))
        elif widths:
            assert len(set(widths))==1, (path.name,widths)
            widths=[]
central=files[0].read_text(encoding='utf-8')
assert all(n in central for n in manifest['topic_files'])
metric_dictionary=(ROOT/'Objais Metrics Research.md').read_text().split('## Full metric dictionary\n',1)[1]
event_dictionary=(ROOT/'Objais Measurement and Attribution Research.md').read_text().split('## Full proposed event dictionary\n',1)[1]
assert len(re.findall(r'^### ',metric_dictionary,re.M))==38
assert len(re.findall(r'^### ',event_dictionary,re.M))==22
source_text=source.read_text(encoding='utf-8')
original_matches=list(re.finditer(r'^# (.+)$',source_text,re.M))[1:]
for i,m in enumerate(original_matches):
    section=source_text[m.start():original_matches[i+1].start() if i+1<len(original_matches) else len(source_text)].strip()
    shifted=re.sub(r'^(#{1,5}) ',lambda x:'#'+x.group(1)+' ',section,flags=re.M)
    assert any(shifted in p.read_text(encoding='utf-8') for p in files[1:]),m.group(1)
result={'status':'pass','scope':'Markdown coverage, local links, structure and illustrative arithmetic; no live research or measurement validation','central_file':manifest['central'],'focused_files':len(manifest['topic_files']),'original_sections_preserved':len(original_matches),'local_links_checked':link_count,'metrics':38,'supplemental_community_metrics':manifest.get('supplemental_community_metrics',0),'events':22,'example_scenarios':len(examples),'community_acquisition_example':'pass','original_report_sha256_unchanged':manifest['source_sha256'],'word_counts':{p.name:len(p.read_text(encoding='utf-8').split()) for p in files}}
(DATA/'markdown-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
manifest['status']='Complete; central guide and focused references checked'
(DATA/'markdown-package.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
