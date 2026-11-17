import json,re,csv
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];D=R/'docs/voicsky-clone';D.mkdir(exist_ok=True)
products=json.loads((R/'data/products.json').read_text(encoding='utf-8'))
translations=json.loads((R/'data/translations.json').read_text(encoding='utf-8'))
comment_values={v for k,v in translations.items() if any(x in k for x in ['BEGIN sections:','END sections:','Google Material Icons:'])}
for f in (R/'data/pages').glob('*.html'):
 text=f.read_text(encoding='utf-8')
 text=text.replace('this.track.querySelectorAll(\'.voicsky-liquid-row__card:not([data-vlr-clone])\')',"(this.track?.querySelectorAll('.voicsky-liquid-row__card:not([data-vlr-clone])') || [])")
 text=re.sub(r'^\s*html\s*(?=<html)', '<!DOCTYPE html>\n', text)
 s=BeautifulSoup(text,'html.parser')
 for node in list(s.find_all(string=True)):
  if node.parent.name not in ['script','style'] and (str(node).strip() in comment_values or any(k in str(node) for k in ['Apache 2.0','Google Material','Liquid output','BEGIN sections','END sections'])):node.extract()
 for e in s.select('script[data-source-attribution]'):e.decompose()
 for e in s.select('#shopify-features,#shop-js-analytics'):e.decompose()
 corrections={'MÀN HÌNH HỒNG + ĐEN + PIXDOT.':'HỒNG + ĐEN + MÀN HÌNH PIXDOT.','1 triệu. SIÊU DÀY.':'SIÊU MỎNG CHỈ 1 MM.','ĐÓNG GÓP.':'MÀN HÌNH PIXEL.','BƯỚM THẤP, HIỆU SUẤT CAO.':'LƯNG THẤP, HIỆU NĂNG CAO.','CÓ PIXDOT.':'TÍCH HỢP PIXDOT.'}
 for node in s.find_all(string=True):
  if node.parent.name not in ['script','style'] and str(node).strip() in corrections:node.replace_with(corrections[str(node).strip()])
 for e in s.select('script'):
  if any(t in (e.string or '') for t in ['shop.app','shopifycloud/shop-js','shopify-features','Shopify.PaymentButton']):e.decompose()
 # SEO and locale are owned by the clone.
 for a in s.select('a[href]'):
  href=a['href'];href=href.replace('https://voicsky.com/en-my','').replace('https://voicsky.com/','/');href=re.sub(r'^/en-my(?=/|$)','',href) or '/';a['href']=href
 for e in s.select('script[type="application/ld+json"]'):
  if e.string:e.string=e.string.replace('https:\\/\\/voicsky.com','http:\\/\\/localhost:3000').replace('https://voicsky.com','http://localhost:3000')
 f.write_text(str(s),encoding='utf-8')
routes=json.loads((R/'data/routes.json').read_text())
with (D/'route-matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['source_url','route','provenance','locale']);w.writerows([['https://voicsky.com/en-my'+r,r,'observed','vi'] for r in routes]);w.writerows([['',r,'new','vi'] for r in ['/pages/about','/cart','/checkout','/order-complete','/blogs/news/demo','/search']])
(D/'design-tokens.json').write_text(json.dumps({'accent':'#67c9ff','light':'#f5f5f7','dark':'#161616','ink':'#1d1d1f','radius':[20,24],'mobileBreakpoint':750,'font':'Be Vietnam Pro','modelFont':'Gridular','heroDurationMs':14000},indent=2))
with (D/'interaction-matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['component','trigger','result']);w.writerows([['hero','thumbnail / next / previous','active slide changes'],['product','discover','hero changes to information'],['structure','accordion','image and description change'],['specification','tab','active specification panel'],['cart','quantity','line and total update'],['checkout','valid submit','session receipt and cart clear'],['search','submit','local catalog search'],['audio','play / seek','single active audio']])
print('Finalized',len(routes),'routes; products',len(products),'variants',sum(len(p['variants']) for p in products))
