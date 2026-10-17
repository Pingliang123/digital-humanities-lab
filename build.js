'use strict';
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname, out = path.join(root, 'dist');
const pages = [
  ['index','Home','首頁'], ['about','About','關於'], ['projects','Projects','項目'],
  ['publications','Publications','論著'], ['docs','Docs','文檔']
];
fs.mkdirSync(path.join(out,'assets'),{recursive:true});
for (const [id,label,zh] of pages) {
  const links=pages.map(([slug,name])=>`<a href="${slug}.html"${slug===id?' aria-current="page"':''}>${name}<span aria-hidden="true">↗</span></a>`).join('\n');
  const content=fs.readFileSync(path.join(root,'content',id+'.html'),'utf8');
  const html=`<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Digital Humanities Lab：中國古典文本、數據與空間研究"><title>${label} · Digital Humanities Lab</title><link rel="stylesheet" href="assets/site.css"></head><body><a class="skip" href="#main">跳至主要內容</a><div class="shell"><aside class="sidebar"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">☯</span><span><strong>Digital<br>Humanities Lab</strong><small>數字人文研究</small></span></a><p class="sidebar-caption">TEXTS · DATA · SPACES</p><nav aria-label="主要導覽">${links}</nav><p class="sidebar-footer">中國古典文本<br>與數字方法</p></aside><main id="main" class="main" aria-label="${zh}">${content}<footer class="footer"><span>Digital Humanities Lab</span><span>文本 · 資料 · 空間</span><a href="https://github.com/Pingliang123/liaozhai-text-map">GitHub ↗</a></footer></main></div></body></html>`;
  fs.writeFileSync(path.join(out,id+'.html'),html,'utf8');
}
for (const file of ['site.css','banner.png']) fs.copyFileSync(path.join(root,'assets',file),path.join(out,'assets',file));
console.log(`Built ${pages.length} pages in ${out}`);
