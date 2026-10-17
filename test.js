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
const imported=JSON.parse(fs.readFileSync(path.join(__dirname,'wordpress-source.json'),'utf8'));
assert(imported.pages.length>=5);
for(const page of imported.pages){
  const html=fs.readFileSync(path.join(__dirname,'dist',page.slug+'.html'),'utf8');
  assert(html.includes('research-nav'));assert(!/<(?:script|iframe|object)\b/i.test(html));
  assert(!/https:\/\/dhchina\.wordpress\.com\/wp-content\/uploads\//.test(html),'Media must be local');
  for(const match of html.matchAll(/(?:href|src)="([^"#]+)"/g)){
    if(!/^https?:/.test(match[1]))assert(fs.existsSync(path.join(__dirname,'dist',match[1].split('#')[0])),'Broken local link: '+match[1]);
  }
}
for(const record of Object.values(imported.resources)){
  const bytes=fs.readFileSync(path.join(__dirname,'dist',record.path));
  assert.equal(require('node:crypto').createHash('sha256').update(bytes).digest('hex'),record.sha256);
}
console.log('Lab site build and navigation tests passed.');
