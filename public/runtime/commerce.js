export const price=c=>c==='keyboard'?1490000:c==='mouse'?790000:990000;
export const total=cart=>cart.reduce((n,x)=>n+x.price*x.quantity,0);
export function add(cart,item){const old=cart.find(x=>x.variantId===item.variantId);return old?cart.map(x=>x===old?{...x,quantity:Math.min(10,x.quantity+item.quantity)}:x):[...cart,{...item,quantity:Math.max(1,Math.min(10,item.quantity))}];}
export const normalize=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replaceAll('đ','d');
