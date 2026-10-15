"""Deterministic checks against the generated public files (no network needed)."""
from pathlib import Path
import json, re, sys
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import PAGES, LEGAL, BASE, BASE_PATH
errors=[]
def check(value,message):
    if not value:errors.append(message)
def local_path(path):
    if BASE_PATH and (path==BASE_PATH or path.startswith(BASE_PATH+'/')):
        return path[len(BASE_PATH):] or '/'
    return path
def public_file(path):
    path=local_path(path)
    return ROOT / (path.lstrip('/')+'index.html' if path.endswith('/') else path.lstrip('/'))
def text_words(text): return len(re.findall(r"\b\w+(?:['’-]\w+)*\b",text))

def validate(path,core=False):
    file=public_file(path);soup=BeautifulSoup(file.read_text(),'html.parser')
    name=path
    check(len(soup.find_all('h1'))==1,name+' exactly one H1')
    check(soup.html.get('lang')=='en',name+' language')
    check(bool(soup.select_one('a.skip-link[href="#main"]')),name+' skip link')
    check(bool(soup.select_one('main#main')),name+' main landmark')
    check(len(soup.title.get_text())<=60,name+' title <=60')
    check(len(soup.select_one('meta[name="description"]')['content'])<=155,name+' description <=155')
    check(soup.select_one('link[rel="canonical"]')['href']==BASE+path,name+' canonical')
    check(soup.select_one('meta[property="og:url"]')['content']==BASE+path,name+' OG URL')
    ids=[el['id'] for el in soup.select('[id]')]
    check(len(ids)==len(set(ids)),name+' unique IDs')
    level=0
    for h in soup.find_all(re.compile('^h[1-6]$')):
        new=int(h.name[1]);check(new<=level+1,name+' heading hierarchy: '+h.get_text());level=new
    headings=soup.find_all(['h2','h3'])
    toc=soup.select_one('nav[aria-label="Table of contents"]')
    check(bool(toc),name+' TOC')
    if toc:
        anchors={a['href'] for a in toc.find_all('a',href=True)}
        check(all('#'+h.get('id','') in anchors for h in headings),name+' TOC covers all H2/H3')
    for a in soup.find_all('a',href=True):
        href=a['href']; parsed=urlsplit(href)
        if not parsed.netloc and not parsed.scheme:
            target=public_file(unquote(parsed.path)) if parsed.path else file
            check(target.exists(),name+' local target '+href)
            if parsed.fragment and target.exists():
                dest=BeautifulSoup(target.read_text(),'html.parser')
                check(bool(dest.find(id=parsed.fragment)),name+' fragment '+href)
        if a.get('target')=='_blank':
            check('noopener' in a.get('rel',[]),name+' safe new tab '+href)
            check('(opens in a new tab)' in a.get_text(),name+' new tab announcement '+href)
    for a in soup.select('.cta-btn'):
        href=a['href'];check(all(x in a.get('rel',[]) for x in ('sponsored','nofollow','noopener')),name+' CTA rel')
        banned=re.search(r'hack|generator|bypass|unlimited|premium-free|free-coins|get-tokens',href) or ('mod' in href and 'mod-apk-danger' not in href)
        check(not banned,name+' CTA URL keyword rule')
        check(bool(a.find_previous_sibling('p')),name+' contextual CTA explanation')
    for img in soup.find_all('img'):
        check(img.get('loading')=='lazy',name+' lazy image')
        check(bool(img.get('alt')),name+' alt')
        check(bool(img.get('width')) and bool(img.get('height')),name+' dimensions')
        check(img['src'].endswith('.webp'),name+' WebP')
        fileimg=public_file(img['src'])
        check(fileimg.exists(),name+' image file')
        if fileimg.exists():
            with Image.open(fileimg) as im:check(im.size==(int(img['width']),int(img['height'])),name+' actual image dimensions')
    check(bool(soup.select_one('.disclosure')),name+' 18+ and affiliate notice')
    check(bool(soup.select_one('.author-box')),name+' author box')
    if not core:return
    page=next(p for p in PAGES if p['path']==path)
    check(page['primary'] in soup.h1.get_text().lower(),name+' primary keyword in H1')
    content=(ROOT/'content'/f'{page["key"]}.md').read_text()
    content=re.sub(r'\[\[.*?\]\]','',content)
    # Counts only original source content, not common source notes or video boilerplate.
    wc=text_words(content)
    check(wc>=3000,name+f' original content >=3000 ({wc})')
    check(len(soup.select('article img'))>=5,name+' >=5 images')
    check(len(soup.select('.cta-btn'))=={'home':2,'generator':4,'live':1,'sites':4}[page['key']],name+' approved CTA count (documented exclusions)')
    article=soup.find('article')
    bodylinks={local_path(a['href']) for a in article.select('p a[href]')}
    for other in PAGES:
        if other['path']!=path:check(other['path'] in bodylinks,name+' contextual in-body link to '+other['path'])
    schemas=[json.loads(s.string) for s in soup.select('script[type="application/ld+json"]')]
    art=next((s for s in schemas if s.get('@type')=='Article'),{})
    faq=next((s for s in schemas if s.get('@type')=='FAQPage'),{})
    check(bool(art.get('author')) and bool(art.get('dateModified')),name+' Article author/date')
    questions=faq.get('mainEntity',[]);check(6<=len(questions)<=10,name+' 6–10 FAQs')
    for q in questions:
        heading=next((h for h in soup.find_all('h3') if h.get_text()==q['name']),None)
        check(bool(heading),name+' FAQ question visible')
        if heading:check(heading.find_next_sibling('p').get_text(' ',strip=True)==q['acceptedAnswer']['text'],name+' FAQ answer matches JSON-LD')
    check(bool(soup.select_one('template.video-template iframe[src$="gDtkB1YmXew"]')),name+' supplied video template')
    check(not soup.select_one('.video-slot iframe'),name+' video not connected until opt-in')
    print(f'PASS {name}: {wc} source words, 5 WebPs, {len(questions)} FAQs')

for page in PAGES:validate(page['path'],True)
for key in LEGAL:validate('/'+key+'/')
root=ElementTree.parse(ROOT/'sitemap.xml').getroot()
check(len(root)==9,'sitemap has nine pages')
check('Allow: /' in (ROOT/'robots.txt').read_text(),'robots allows indexing')
all_soups=[BeautifulSoup(public_file(p['path']).read_text(),'html.parser') for p in PAGES]
check(len({s.title.get_text() for s in all_soups})==4,'unique core titles')
if errors:
    print('\nFAILURES:\n'+'\n'.join(errors));sys.exit(1)
print('PASS: headings, links, fragments, metadata, FAQ parity, image dimensions, video consent, robots and sitemap')
