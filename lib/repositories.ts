import fs from 'node:fs';
import path from 'node:path';
export type Product = { id:string; handle:string; name:string; category:string; image:string; variants:{id:string;title:string;options:string[];featured_image?:{src:string}}[];source_url:string;price:null };
export const catalogRepository = {
  list():Product[] {
    const products:Product[]=JSON.parse(fs.readFileSync(path.join(process.cwd(),'data/products.json'),'utf8'));
    const manifestPath=path.join(process.cwd(),'data/asset-manifest.json');
    if(fs.existsSync(manifestPath)){
      const assets: {source_url:string;local_path:string}[]=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
      for(const p of products){for(const v of p.variants){if(v.featured_image?.src){const pathname=new URL(v.featured_image.src,'https://voicsky.com').pathname;const asset=assets.find(a=>new URL(a.source_url).pathname===pathname);if(asset)v.featured_image.src=asset.local_path;}}p.image=p.variants[0]?.featured_image?.src||p.image;}
    }
    return products;
  },
  get(handle:string) { return this.list().find(p=>p.handle===handle); }
};
export const contentRepository = {
  get(route:string):string|null { const file=path.join(process.cwd(),'data/pages',(route.replace(/^\//,'').replaceAll('/','__')||'home')+'.html'); return fs.existsSync(file)?fs.readFileSync(file,'utf8'):null; }
};
export const demoPrice = (category:string)=>category==='keyboard'?1490000:category==='mouse'?790000:990000;
