'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
cp.execFileSync(process.execPath,[path.join(__dirname,'build.js')]);
for(const [name,title] of [['index','Home'],['about','About'],['projects','Projects'],['publications','Publications'],['docs','Docs']]){
  const html=fs.readFileSync(path.join(__dirname,'dist',name+'.html'),'utf8');
  assert(html.includes('<html lang="zh-Hant">'));assert(html.includes(`>${title}<span aria-hidden="true">↗</span></a>`));
  assert(html.includes('aria-current="page"'));assert(html.includes('id="main"'));
  for(const slug of ['index','about','projects','publications','docs'])assert(html.includes(`href="${slug}.html"`));
}
const projects=fs.readFileSync(path.join(__dirname,'dist','projects.html'),'utf8');
assert(projects.includes('老子其人'));assert(projects.includes('聊齋文本地圖'));assert(projects.includes('pingliang123.github.io/liaozhai-text-map/'));
assert(fs.statSync(path.join(__dirname,'dist','assets','banner.png')).size>100000);
console.log('Lab site build and navigation tests passed.');
