import requests, json, re, hashlib, time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[1]
BASE='https://voicsky.com'
handles=['apex-75','atmos-87','echo','pulse','tune-65','nimbus-65','sky','sky-pro','cloud-s1-pro','cloud-s2-pro','aeros-pro','apex-75-reiko-edition']
routes=['/']+['/products/'+h for h in handles]+['/collections/'+h for h in ['all','keyboard','mouse','mouse-pad','frontpage']]+['/pages/'+h for h in ['contact','where-to-buy','global-sources-hong-kong-shows-2026','pre-order-apex-75-reiko-edition']]+['/blogs/news','/policies/privacy-policy','/policies/terms-of-service']
assets={}; pending=[]; pages={}; products=[]
def register(url):
    url=urljoin(BASE,url.replace('&amp;','&'))
    if not url.startswith(('https://voicsky.com/cdn/','https://cdn.shopify.com/s/files/')): return url
    # Preserve version and rendition identity. Hash exact URL to avoid basename collisions.
    ext=Path(urlparse(url).path).suffix or '.bin'
    if ext=='.m3u8': return url
    local='/assets/'+hashlib.sha256(url.encode()).hexdigest()[:20]+ext
    if url not in assets: assets[url]={'source_url':url,'local_path':local,'status':'pending'}; pending.append(url)
    return local
def rewrite(text):
    return re.sub(r'(?:https:)?//(?:voicsky\.com/cdn/|cdn\.shopify\.com/s/files/)[^\s\"\'<>\\)]+',lambda m:register(m.group()),text)
for route in routes:
    url=BASE+'/en-my'+('' if route=='/' else route)
    print('PAGE',route,flush=True)
    r=requests.get(url,timeout=60); r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser')
    if route.startswith('/products/'):
        variants=[]
        for tag in soup.select('script[type="application/json"]'):
            try:
                v=json.loads(tag.string or tag.get_text())
                if isinstance(v,list) and v and isinstance(v[0],dict) and 'options' in v[0] and 'id' in v[0]: variants=v;break
            except:pass
        main=soup.select_one('main'); image=main.select_one('img')
        products.append({'id':route.split('/')[-1],'handle':route.split('/')[-1],'name':soup.title.get_text().split(' – ')[0], 'category':'mouse-pad' if route.split('/')[-1] in ['sky','sky-pro'] else 'mouse' if any(t in route for t in ['cloud-','aeros']) else 'keyboard','source_url':url,'variants':variants,'image':register(urljoin(BASE,image.get('src'))) if image else '', 'sections':[{'id':s.get('id'),'html':str(s)} for s in main.select('.shopify-section')], 'source_price':0,'price':None})
    for tag in soup.select('script[src]'):
        src=urljoin(BASE,tag['src'])
        if '/cdn/shop/t/2/' not in src:tag.decompose()
    for tag in soup.select('script:not([src])'):
        txt=tag.string or ''
        if any(x in txt for x in ['webPixelsManager','GoogleAnalytics','gtag(', 'ShopifyAnalytics','monorail','trekkie','Shopify.loadFeatures']):tag.decompose()
    for a in soup.select('[href]'):
        href=a['href']
        if href.startswith(BASE):href=href[len(BASE):]
        href=re.sub(r'^/en-my(?=/|$)','',href) or '/'
        a['href']=href
    soup.html['lang']='vi'
    for e in soup.select('link[rel="canonical"]'):e['href']='http://localhost:3000'+route
    for e in soup.select('form'):
        if e.get('action') and '/localization' in e['action']:e['data-original-action']=e['action'];e['action']='#'
    style=soup.new_tag('link',rel='stylesheet',href='/runtime/clone.css');soup.head.append(style)
    script=soup.new_tag('script',src='/runtime/clone.js');script['defer']='';soup.head.append(script)
    html=rewrite(str(soup))
    html=html.replace('https://voicsky.com/en-my/','/').replace('https://voicsky.com/en-my','/').replace('"/en-my/','"/').replace("'/en-my/","'/")
    pages[route]=html
    (ROOT/'data/pages').mkdir(exist_ok=True)
    (ROOT/'data/pages'/((route.strip('/').replace('/','__') or 'home')+'.html')).write_text(html,encoding='utf-8')
(ROOT/'data/products.json').write_text(json.dumps(products,ensure_ascii=False),encoding='utf-8')
(ROOT/'data/routes.json').write_text(json.dumps(routes),encoding='utf-8')
def download(url):
    record=assets[url]; target=ROOT/'public'/record['local_path'].lstrip('/')
    if target.exists():record['status']='downloaded';return
    for attempt in range(3):
        try:
            r=requests.get(url,timeout=180);r.raise_for_status();content=r.content
            if target.suffix in ['.css','.js']:
                txt=rewrite(r.text)
                # Relative module imports and CSS url references resolve to original asset directory.
                txt=re.sub(r'([\"\'])(\./[^\"\']+\.js(?:\?[^\"\']*)?)\1',lambda m:m[1]+register(urljoin(url,m[2]))+m[1],txt)
                txt=re.sub(r'url\(([\"\']?)([^)\"\']+)\1\)',lambda m:'url("'+register(urljoin(url,m[2]))+'")' if not m[2].startswith(('data:','#','/assets/')) else m[0],txt)
                content=txt.encode()
            target.write_bytes(content);record.update(status='downloaded',bytes=len(content),sha256=hashlib.sha256(content).hexdigest(),mime=r.headers.get('Content-Type'))
            return
        except Exception as e:record.update(status='failed',error=str(e));time.sleep(attempt+1)
with ThreadPoolExecutor(max_workers=3) as pool:
    offset=0
    while offset<len(pending):
        batch=pending[offset:];offset=len(pending)
        list(pool.map(download,batch));print('ASSETS',offset,'/',len(pending),flush=True)
(ROOT/'data/asset-manifest.json').write_text(json.dumps(list(assets.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',len(pages),len(assets),flush=True)
