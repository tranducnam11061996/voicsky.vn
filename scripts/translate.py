from pathlib import Path
import json,requests,time,re
from bs4 import BeautifulSoup, Comment, Doctype
ROOT=Path(__file__).resolve().parents[1]
files=list((ROOT/'data/pages').glob('*.html'))
skip={'script','style','svg','title','noscript'}
texts=[]
for file in files:
 s=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 for t in s.find_all(string=True):
  value=str(t).strip()
  if t.parent.name not in skip and not any(p.name in skip for p in t.parents) and re.search('[a-zA-Z]{3}',value) and '<' not in value and len(value)<5000 and value not in texts:texts.append(value)
cachefile=ROOT/'data/translations.json'
cache=json.loads(cachefile.read_text(encoding='utf-8')) if cachefile.exists() else {}
pending=[t for t in texts if t not in cache]
for index in range(0,len(pending),25):
 batch=pending[index:index+25]
 try:
  response=requests.post('https://translate.googleapis.com/translate_a/single',params={'client':'gtx','sl':'en','tl':'vi','dt':'t'},data={'q':'\n'.join(t.replace('\n',' ') for t in batch)},timeout=60)
  if response.status_code!=200:
   response=requests.get('https://translate.googleapis.com/translate_a/single',params={'client':'gtx','sl':'en','tl':'vi','dt':'t','q':'\n'.join(t.replace('\n',' ') for t in batch)},timeout=60)
  translated=''.join(x[0] for x in response.json()[0]).split('\n')
  if len(translated)==len(batch):cache.update(zip(batch,translated))
  else:
   for t in batch:
    r=requests.get('https://translate.googleapis.com/translate_a/single',params={'client':'gtx','sl':'en','tl':'vi','dt':'t','q':t},timeout=30)
    cache[t]=''.join(x[0] for x in r.json()[0])
 except Exception as e: print('TRANSLATE ERROR',str(e)[:150],flush=True)
 cachefile.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding='utf-8')
 print('TRANSLATED',len(cache),'/',len(texts),flush=True)
for file in files:
 s=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 for t in s.find_all(string=True):
  value=str(t).strip()
  if not isinstance(t,(Comment,Doctype)) and value in cache and not any(p.name in skip for p in t.parents):
   # Preserve product model typography and brand names.
   if re.fullmatch(r'(VOICSKY )?(APEX|ATMOS|ECHO|PULSE|TUNE|NIMBUS|SKY|CLOUD|AEROS)[A-Z 0-9.%-]*',value):continue
   t.replace_with(str(t).replace(value,cache[value]))
 file.write_text(str(s),encoding='utf-8')
print('DONE',flush=True)
