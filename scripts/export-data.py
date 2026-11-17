import json
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
products=json.loads((R/'data/products.json').read_text(encoding='utf-8'))
specs=[];sections=[];assets=[]
for p in products:
 s=BeautifulSoup((R/'data/pages'/('products__'+p['handle']+'.html')).read_text(encoding='utf-8'),'html.parser')
 for n,section in enumerate(s.select('main > .shopify-section')):
  key=p['handle']+':section:'+str(n)
  sections.append({'id':key,'product_id':p['id'],'source_id':section.get('id'),'order':n,'type':section.get('class'),'headings':[h.get_text(' ',strip=True) for h in section.select('h1,h2,h3')],'content_html':str(section)})
  for i,e in enumerate(section.select('img,video,audio,source')):
   assets.append({'owner_id':key,'order':i,'type':e.name,'src':e.get('src'),'srcset':e.get('srcset'),'poster':e.get('poster'),'alt':e.get('alt')})
 for tab,panel in enumerate(s.select('[role=tabpanel]')):
  button=s.find(id=panel.get('aria-labelledby'))
  for i,row in enumerate(panel.select('dl > div')):
   if row.dt and row.dd:specs.append({'product_id':p['id'],'group_order':tab,'group':button.get_text(' ',strip=True) if button else str(tab),'order':i,'label':row.dt.get_text(' ',strip=True),'value':row.dd.get_text('\n',strip=True),'locale':'vi','source_url':p['source_url']})
for name,records in [('sections',sections),('specifications',specs),('asset-usages',assets)]:
 (R/'data'/f'{name}.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');print(name,len(records))
s=BeautifulSoup((R/'data/pages/pages__where-to-buy.html').read_text(encoding='utf-8'),'html.parser')
partners=[];locations=[]
for i,card in enumerate(s.select('.vwtb__card')):
 partner_id='partner:'+str(i)
 partners.append({'id':partner_id,'name':card.h3.get_text(' ',strip=True),'country':card.get('data-country'),'types':card.get('data-type'),'links':[{'label':a.get_text(' ',strip=True),'url':a.get('href')}for a in card.select('a[href]')]})
 for n,address in enumerate(card.select('[data-location]')):
  locations.append({'id':partner_id+':'+str(n),'partner_id':partner_id,'name':address.get('data-branch-name'),'address':address.get_text(' ',strip=True),'lat':address.get('data-lat'),'lon':address.get('data-lon')})
for name,records in [('partners',partners),('locations',locations)]:
 (R/'data'/f'{name}.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');print(name,len(records))
