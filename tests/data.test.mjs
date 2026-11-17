import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=name=>JSON.parse(fs.readFileSync(new URL('../data/'+name,import.meta.url),'utf8'));
test('catalog has 12 source products and 43 actual variants without duplicate IDs',()=>{const p=read('products.json');assert.equal(p.length,12);const v=p.flatMap(x=>x.variants);assert.equal(v.length,43);assert.equal(new Set(v.map(x=>String(x.id))).size,43);assert.ok(p.every(x=>x.price===null));});
test('every downloaded manifest entry exists locally',()=>{for(const a of read('asset-manifest.json')){if(a.status.startsWith('excluded'))continue;assert.equal(a.status,'downloaded',a.source_url);assert.ok(fs.existsSync(new URL('../public'+a.local_path,import.meta.url)),a.local_path)}});
