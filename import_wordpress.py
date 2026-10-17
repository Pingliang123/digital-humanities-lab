"""Import the owner's published Laozi research, with local media and provenance."""
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request

ROOT = Path(__file__).parent
API = 'https://public-api.wordpress.com/wp/v2/sites/dhchina.wordpress.com/'
PAGES = {1: 'abstract', 19: 'dataset', 26: 'methods', 28: 'results', 30: 'limitations'}
ALLOWED = set('p h2 h3 h4 ul ol li blockquote pre code strong em b i u s br hr div span section figure figcaption img a table thead tbody tr th td sup sub'.split())
VOID = {'img', 'br', 'hr'}

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'DH-Lab-Migration/1.0'}), timeout=60) as response:
        return response.read()

def collect(kind):
    rows, page = [], 1
    while True:
        batch = json.loads(fetch(API + kind + '?per_page=100&page=' + str(page)))
        rows.extend(batch)
        if len(batch) < 100:
            return rows
        page += 1

class Cleaner(HTMLParser):
    def __init__(self, links, asset):
        super().__init__(convert_charrefs=True)
        self.links, self.asset, self.output, self.skip = links, asset, [], 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'iframe', 'object'}:
            self.skip += 1
        if self.skip or tag not in ALLOWED:
            return
        attrs = dict(attrs)
        kept = {}
        if tag == 'a':
            url = attrs.get('href', '')
            if url.startswith(('https://', 'http://', '#')):
                kept['href'] = self.links.get(urllib.parse.unquote(url).rstrip('/'), self.asset(url))
            if 'download' in attrs:
                kept['download'] = ''
        if tag == 'img':
            url = attrs.get('src', '')
            if not url.startswith('https://'):
                return
            kept = {'src': self.asset(url), 'alt': attrs.get('alt', ''), 'loading': 'lazy'}
        for key in ['colspan', 'rowspan']:
            if attrs.get(key, '').isdigit():
                kept[key] = attrs[key]
        self.output.append('<' + tag + ''.join(' ' + k + '="' + html.escape(v, quote=True) + '"' for k, v in kept.items()) + '>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'iframe', 'object'}:
            self.skip = max(0, self.skip - 1)
        elif not self.skip and tag in ALLOWED and tag not in VOID:
            self.output.append('</' + tag + '>')

    def handle_data(self, value):
        if not self.skip:
            self.output.append(html.escape(value))

def main():
    pages, posts = collect('pages'), collect('posts')
    selected = [(p, 'laozi-' + PAGES[p['id']]) for p in pages if p['id'] in PAGES]
    if len(selected) != len(PAGES):
        raise ValueError('Missing one of the five Laozi research pages')
    selected += [(p, 'laozi-note-' + str(p['id'])) for p in posts if re.search('老子|BERT|bert', p['title']['rendered'] + p['content']['rendered'])]
    links = {urllib.parse.unquote(p['link']).rstrip('/'): slug + '.html' for p, slug in selected}
    resources = {}
    def asset(url):
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc != 'dhchina.wordpress.com' or not parsed.path.startswith('/wp-content/uploads/'):
            return url
        # Keep downloaded files independent of WordPress and use stable portable names.
        if url not in resources:
            suffix = Path(parsed.path).suffix.lower()
            if suffix not in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.pdf', '.docx', '.xlsx', '.zip', '.txt', '.csv'}:
                return url
            target = 'assets/laozi/' + hashlib.sha256(url.encode()).hexdigest()[:16] + suffix
            data = fetch(url)
            destination = ROOT / target
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            resources[url] = {'path': target, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        return resources[url]['path']
    nav = '<nav class="research-nav" aria-label="老子研究章節">' + ''.join('<a href="laozi-' + slug + '.html">' + label + '</a>' for slug, label in [('abstract','摘要'),('dataset','數據集'),('methods','分析方法'),('results','分析結果'),('limitations','研究限制')]) + '</nav>'
    for page, slug in selected:
        clean = Cleaner(links, asset)
        clean.feed(page['content']['rendered'])
        title = re.sub('<[^>]+>', '', html.unescape(page['title']['rendered']))
        markup = '<div class="topline"><span>LAOZI</span><a href="projects.html#laozi">研究項目 ↗</a></div><header class="page-heading"><p class="eyebrow">老子其人 / 文本分類研究</p><h1>' + html.escape(title) + '</h1></header>' + nav + '<article class="content research-article">' + ''.join(clean.output) + '</article><p class="caption">遷移來源：<a href="' + html.escape(page['link'], quote=True) + '">原 WordPress 頁面</a> · 原文最後更新：' + html.escape(page['modified_gmt']) + ' UTC</p>'
        (ROOT / 'content' / (slug + '.html')).write_text(markup, encoding='utf-8')
    snapshot = {'site': 'https://dhchina.wordpress.com/', 'pages': [{'id': p['id'], 'slug': slug, 'title': p['title']['rendered'], 'link': p['link'], 'modified_gmt': p['modified_gmt'], 'content': p['content']['rendered']} for p, slug in selected], 'resources': resources}
    (ROOT / 'wordpress-source.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'pages': len(selected), 'resources': len(resources)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
