import {test} from 'node:test';
import assert from 'node:assert/strict';
import {price,total,add,normalize} from '../public/runtime/commerce.js';
test('same variant merges, different variants remain separate, quantity capped',()=>{let c=add([],{variantId:'a',quantity:7,price:1490000});c=add(c,{variantId:'a',quantity:8,price:1490000});assert.equal(c[0].quantity,10);c=add(c,{variantId:'b',quantity:1,price:790000});assert.equal(c.length,2);assert.equal(total(c),15690000)});
test('VND fixture and Vietnamese normalization',()=>{assert.equal(price('keyboard'),1490000);assert.equal(price('mouse'),790000);assert.equal(price('mouse-pad'),990000);assert.equal(normalize('BÀN PHÍM Đẹp'),'ban phim dep')});
