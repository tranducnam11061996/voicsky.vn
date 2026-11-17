import { catalogRepository, contentRepository } from '../../lib/repositories';
export const dynamic='force-dynamic';
export async function GET(request:Request) {
 const url=new URL(request.url); const route=url.pathname.replace(/\/$/,'')||'/';
 if(route==='/api/catalog')return Response.json(catalogRepository.list().map(({id,handle,name,category,image,variants})=>({id,handle,name,category,image,variants})));
 let html=contentRepository.get(route);
 if(!html) {
  const shell=contentRepository.get('/blogs/news')!;
  const known=['/cart','/checkout','/order-complete','/pages/about','/blogs/news/demo','/search'];
  html=shell.replace(/<main\b[\s\S]*?<\/main>/,'<main id="MainContent"><div id="custom-page"></div></main>');
  if(!known.includes(route))return new Response(html.replace('id="custom-page"','id="custom-page" data-not-found="true"'),{status:404,headers:{'Content-Type':'text/html; charset=utf-8'}});
 }
 return new Response(html,{headers:{'Content-Type':'text/html; charset=utf-8'}});
}
