"""Render complete, crawlable HTML pages; JS is only used for opt-in video playback."""
from pathlib import Path
import os, re, json
from html import escape
from urllib.parse import urlparse
from datetime import date
import markdown
from bs4 import BeautifulSoup
from make_images import SPECS

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-15'
BASE=os.environ.get('SITE_URL','https://example.com').rstrip('/')
parsed=urlparse(BASE)
if parsed.scheme!='https' or not parsed.netloc or parsed.query or parsed.fragment or parsed.username or parsed.password:
    raise SystemExit('SITE_URL must be an HTTPS URL, optionally with a project path')
BASE_PATH=parsed.path.rstrip('/')
if BASE_PATH and not re.fullmatch(r'(?:/[A-Za-z0-9_-]+)+',BASE_PATH):
    raise SystemExit('SITE_URL project path contains unsupported characters')

PAGES=[
 dict(key='home',path='/',title='Strip Chat Free: What Is Actually Free? | OpenRoom',description='A practical guide to free public rooms, guest and registered accounts, token costs and safer browsing. No hacks or guaranteed bonus claims.',h1='Strip chat free: the free part, and the fine print.',category='THE FREE-ACCESS GUIDE',number='01',deck='Public rooms. Real boundaries. No invented rewards.',short='Free access',primary='strip chat free',hero='Free to watch.\nNot free of boundaries.'),
 dict(key='generator',path='/stripchat-token-generator/',title='Stripchat Token Generator: Why It Is a Scam | OpenRoom',description='Token generators, hacks and modified apps do not create real credit. Learn the warning signs, recovery steps and verified official giveaway rules.',h1='Stripchat token generator: a promise that does not pay.',category='THE SAFETY INVESTIGATION',number='02',deck='A fake counter is not a credit. Here is what to trust instead.',short='Token safety',primary='stripchat token generator',hero='A bigger number.\nNot a real balance.'),
 dict(key='live',path='/stripchat-live/',title='Stripchat Live: Shows, Costs & Privacy | OpenRoom',description='Understand public, private, spy and ticket shows, cam2cam privacy, tipping, interactive features and mobile controls before spending tokens.',h1='Stripchat live: know the room before you join.',category='THE LIVE-ROOM HANDBOOK',number='03',deck='Who can watch, what it costs, and where your privacy begins.',short='Live rooms',primary='stripchat live',hero='Know the format.\nKeep your boundaries.'),
 dict(key='sites',path='/strip-chat-sites/',title='Strip Chat Sites Compared: Three Platforms | OpenRoom',description='Compare Stripchat, Chaturbate and BongaCams on public access, token value, payments, privacy and adult-only rules. Free first, paid only by choice.',h1='Strip chat sites: compare the terms, not the hype.',category='THE PLATFORM COMPARISON',number='04',deck='Three platforms. One fair way to judge cost, fit and privacy.',short='Compare sites',primary='strip chat sites',hero='Compare the outcome.\nNot the token count.'),
]
CTA={
'home-how':('https://striptks.live/how-stripchat-works/','See how Stripchat works','For another overview of the interface, this external guide separates public rooms from paid actions. Treat the live platform as the authority if a feature has changed.'),
'home-safe':('https://striptks.live/blog/is-stripchat-safe/','Is Stripchat safe? Full check','This external safety checklist covers account, device and payment exposure in more depth. Its publisher is commercial; check current official rules rather than relying on promotional claims.'),
'generator-apk':('https://striptokens.live/blog/stripchat-mod-apk-danger/','Why mod APKs are dangerous','This external explainer expands on modified-app risks. We link for the security explanation, not its unverified bonus claims or predictions about automatic bans.'),
'generator-giveaway':('https://striptks.live/blog/how-stripchat-hourly-giveaway-works/','How the official hourly giveaway works','This independent explainer separates eligibility, selection and claiming. It is not the official platform; compare it with the official support article cited below.'),
'generator-missing':('https://striptks.live/blog/why-i-didnt-get-my-hourly-draw-tokens-on-stripchat/',"Didn't get your draw tokens? Fixes",'If you have evidence of a missing official credit, this troubleshooting article can help organize a support request. Do not treat its assumptions about participation or eligibility as official rules.'),
'generator-packages':('https://striptks.live/blog/stripchat-token-prices-best-packages/','Cheapest legit token packages','Use this external guide for package arithmetic, not a guaranteed cheapest offer. Compare the final checkout total with your existing cash limit before making any purchase.'),

'live-toys':('https://striptks.live/blog/stripchat-lovense-interactive-toys/','How interactive toys work','This external feature guide discusses enabled controls, durations and queues. Ignore promotional urgency and verify the current settings in the official room before spending.'),
'sites-chaturbate':('https://striptks.live/stripchat-vs-chaturbate/','Stripchat vs Chaturbate','For a narrower comparison, this external article considers the two interfaces and feature costs. Its preference is editorial, not proof of a universal cheapest or safest platform.'),
'sites-bonga':('https://striptks.live/stripchat-vs-bongacams/','Stripchat vs BongaCams','This external comparison gives another perspective on the two services. Verify the room and checkout details yourself; a promotional advantage is not a guaranteed personal benefit.'),
'sites-payments':('https://striptks.live/blog/stripchat-payment-methods/','Payment methods compared','This external guide explains provider handoffs and local availability. It does not replace the methods, conditions and final total shown in your own official checkout.'),
'sites-crypto':('https://striptks.live/blog/stripchat-crypto-payments/','Paying with crypto','If you already understand cryptocurrency, this external checklist highlights irreversible-payment details. It is informational, not a recommendation to acquire crypto or a promise of anonymity.'),
}
SUPPORT='https://support.stripchat.com/hc/en-us/articles/4410727906577-I-did-not-receive-free-tokens-token-giveaway-when-I-signed-up'
SOURCES=[('Stripchat Terms and Conditions','https://stripchat.com/terms','Eligibility, account security, prohibited uses, payments, refunds and room formats.'),('Stripchat official giveaway help',SUPPORT,'The published hourly giveaway, eligibility and ten-minute claim requirement.')]
LEGAL={
'about': ('About OpenRoom', 'Our purpose, evidence standards and limits as an independent adult-platform information site.', '''OpenRoom is an independent, non-explicit information site for adults. It explains public access, paid live-room formats, token scams and platform comparisons. It is not Stripchat, Chaturbate, BongaCams or any of their support teams.

## What we publish

We aim to make decisions easier to understand, not encourage a purchase. A reader should leave knowing what is free, which action costs money and what remains uncertain. A no-purchase visit is a valid outcome. We do not provide explicit imagery, modified software, balance tools or ways around age and access rules.

The OpenRoom Editorial Desk is a publication byline, not a claimed individual expert. We have not invented a biography, professional credential or testing history. Drafting, implementation and structural checks for this version were AI-assisted. There has been no firsthand paid-account testing, malware analysis, controlled performance benchmark or independent security audit.

## Evidence and corrections

The four main guides cite the official rules used to support factual claims. The last-updated date identifies this edition, not a promise of continuous monitoring. Prices, promotions and local requirements can change afterward. Fictional arithmetic examples are labeled as illustrations and should not be mistaken for checkout quotes.

We distinguish official documentation from third-party commentary. External resource buttons lead to commercial publishers and are marked sponsored and nofollow conservatively. A linked article can have useful explanatory material without every promotion or factual assertion being endorsed. Two supplied articles were excluded for misleading promotional claims; details are in the repository's link audit.

## Editorial boundaries

We do not publish fabricated testimonials, statistics, star ratings, traffic counts or quotations. No external site can choose promotion winners through this publication. We cannot inspect balances, recover credentials, accept payment for platform services or resolve account disputes.

All diagrams are original editorial illustrations, not screenshots of a live platform or evidence of an actual transaction. The supplied video is labeled as a promotional claim under critical review, with a warning before opt-in playback. Its unlimited-token framing is not endorsed.

## Reach the editorial desk

Use the [contact page](/contact/) for a public correction route. Do not send personal documents, payment information, passwords or private account material. For account or billing help, use the relevant official platform or payment provider instead.'''),
'contact': ('Contact and corrections', 'How to report an editorial problem without sharing private account or payment information.', '''This site has no account-support service, payment desk or private message form. We cannot issue tokens, restore access, choose winners or reverse charges. Never send us a password, one-time code, reset link, identity document, card number or wallet recovery phrase.

## Report an editorial error

The repository has GitHub issues enabled. You can [open a public editorial issue](https://github.com/MaryamKrol444/strip-mod-token/issues/new) about a broken link, unclear passage or factual correction. GitHub may require an account. This is a public channel operated under GitHub's own terms and privacy policy, not a confidential support inbox.

Include the page address, section heading, the statement you believe is wrong and an official source supporting a correction. A short description is enough. Do not attach screenshots of private rooms, account history, messages, identity checks or financial records. Publication of a report does not guarantee a response time or a particular editorial outcome.

## Account and billing questions

Navigate to support from the official platform you use. For an unrecognized charge, contact the payment provider or issuer through a verified route. If you suspect account compromise, use a trusted device, secure the recovery email and change reused passwords before discussing details publicly.

If a person contacts you claiming to be this site's recovery agent, do not provide credentials or money. OpenRoom has no such role. A public issue is suitable for a typo or link correction, not incident response or a private account dispute.

## Private matters

No verified private editorial inbox has been configured for this edition. Do not submit a privacy-sensitive complaint through a public issue. The publisher must supply an appropriate private contact and legal identity before a production launch that requires them. Consult the [Privacy Policy](/privacy-policy/) for the current site's limited data behavior.'''),
'privacy-policy': ('Privacy Policy', 'What this static site loads, what external video playback changes and what it does not collect.', '''This policy describes the supplied static OpenRoom implementation as of 15 October 2026. It does not describe the privacy practices of adult platforms, linked commercial publishers, GitHub or YouTube. Their services have separate policies and controls.

## Data collected by the site

This implementation has no visitor accounts, contact form, analytics script, advertising pixel or embedded payment system. It does not set application cookies or use local storage. Reading an article or its contents menu does not require submitting information.

The hosting provider necessarily receives requests when a page or asset is served and may log technical information such as an IP address, request path, browser information and time. Actual retention and access depend on the selected host. No host-specific retention period, controller identity or legal basis has been verified for this undeployed edition.

## Video playback is optional

The supplied YouTube player is stored in an inactive HTML template. It is not connected until you select the clearly labeled load control. Loading it creates a third-party connection to YouTube's privacy-enhanced embed domain. Google/YouTube may process network and device information under its own policies and may use storage when you interact.

Privacy-enhanced embedding is not a guarantee of anonymity or zero data processing. Do not load the video if you do not want that connection. The article, captions for editorial diagrams and navigation remain available without loading the player or enabling JavaScript.

## External links

Following a resource or source link sends you to another service. External commercial resource buttons open a new tab and carry sponsored, nofollow and noopener attributes. No embedded third-party tracker is added to these links by this implementation. Destination sites can have their own referral tracking, cookies and commercial relationships.

The correction route uses public GitHub issues. Do not submit private account or financial information there. You control whether you follow that link; no GitHub widget is embedded here.

## Rights and production information

Depending on your jurisdiction, data-protection rights may include access, correction, deletion and complaint rights in relation to a controller's processing. This static implementation does not maintain an application account database. Hosting logs and third-party records must be addressed with the relevant responsible party.

Before production publication, the publisher must add its verified identity, private contact route, hosting practices and any applicable consent arrangements. Those details must not be invented. If analytics, forms, advertising or other data processing is introduced later, update this policy before enabling it.'''),
'terms': ('Terms of use', 'Adult-only informational use, external services and the limits of this publication.', '''These terms describe use of OpenRoom's informational pages. They do not replace the rules of any external platform. If you do not meet the age and legal access requirements for adult-industry information in your location, do not use this site.

## Adult-only scope

Readers must be at least eighteen and meet any higher applicable age-of-majority requirement. The site contains non-explicit educational material about adult services. Its adult notice is not identity verification or permission to access a separate platform. Do not use this information to evade age assurance, geographic restrictions or another service's rules.

## Information, not account services

Articles are general information, not individualized legal, financial, cybersecurity or medical advice. We do not operate live rooms, hold token balances or accept platform payments. We cannot guarantee a particular price, promotion, performer availability, support outcome or account status.

Facts are limited to the sources and scope described in each article. Changing features must be checked with the official service. Examples using fictional cash and token quantities explain arithmetic only. They are not offers to sell anything or promises of an obtainable package.

## Responsible use

Do not use this site to distribute malware, steal credentials, bypass controls, harass people or infringe privacy or intellectual-property rights. Public correction reports must not include sensitive account information or unauthorized content. Follow the rules of the external service hosting any report.

You are responsible for your decision to visit an external service or authorize a purchase. Nothing here overrides mandatory consumer rights or excludes liabilities that cannot legally be excluded. If an interaction seems unsafe or unclear, stop rather than relying on a general article as permission to continue.

## Ownership and external material

Platform and hardware names are trademarks of their respective owners. Their use identifies the subjects of commentary and does not imply endorsement. OpenRoom's diagrams are editorial illustrations, not copied platform screenshots. The external video is shown for critical review and remains its publisher's material.

## Updates and limitations

These terms apply to this edition dated 15 October 2026. The publisher must add any production-specific identity, jurisdiction and contact information required by applicable law before launch. No fictitious governing jurisdiction, business address or private inbox has been inserted. Use the [contact page](/contact/) for non-sensitive editorial corrections only.'''),
'disclaimer': ('Editorial and affiliate disclaimer', 'Our independence, conservative link labeling and the limits of platform and promotional information.', '''OpenRoom is an independent informational publication for adults. It is not affiliated with or endorsed by Stripchat, Chaturbate, BongaCams, Lovense, Google or YouTube. Mentioning a company identifies the subject of discussion, not a business partnership.

## Affiliate and commercial links

External resource buttons lead to commercial third-party publishers. We conservatively mark them sponsored and nofollow, alongside noopener for new tabs. No affiliate account, commission arrangement or payout has been verified for this build. Do not interpret a Partner site label on another website as a guarantee from this publication.

If the publisher later introduces a direct affiliate arrangement, it must update this disclosure to explain who may pay it and under what broad circumstances. A commercial relationship must not determine factual claims, disguise a paid placement as an official source or create promises about promotion eligibility.

## Promotional claims

Token generators, hacks, modified apps and bypass extensions do not provide an authorized way to create spendable credit. We publish no downloads or instructions for them. The official giveaway cited in the guides is chance-based and subject to current platform terms; it is not a guaranteed signup payment.

The supplied video has misleading unlimited-token framing. It is available only behind an explicit warning and opt-in load control as an example for critical review. We do not endorse its headline, off-site offers or unsupported claims about turning small awards into unlimited balances.

Some requested resource links were excluded because they promoted unverified prizes and unsupported assurances. Other linked articles can contain promotions we do not substantiate. Their explanatory content is not a substitute for official account and checkout conditions.

## No invented experience

We do not claim firsthand testing, private system access or expert credentials. The publication byline is an editorial desk, not an invented person. AI-assisted writing and development were used for this edition. We provide dated sources, explicit limits and illustrative diagrams so readers can assess the basis of the advice.

## Financial and safety decisions

There is no obligation to purchase tokens after reading. Set a limit you can afford, never borrow for entertainment and stop if spending becomes difficult to control. For account incidents, use official platform support; for unauthorized payments, use your provider's verified route. This site cannot resolve either on your behalf.'''),
}

def slug(text):
    return re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-')

def cta(match):
    url,label,explanation=CTA[match.group(1)]
    if re.search(r'hack|generator|bypass|unlimited|premium-free|free-coins|get-tokens',url) or ('mod' in url and 'mod-apk-danger' not in url):
        raise ValueError('Disallowed external resource URL')
    return f'<aside class="resource" aria-label="Related commercial resource"><span class="eyebrow">Related resource · External commercial publisher</span><p>{escape(explanation)}</p><a class="cta-btn" href="{escape(url)}" target="_blank" rel="sponsored nofollow noopener">{escape(label)} <span aria-hidden="true">↗</span><span class="visually-hidden"> (opens in a new tab)</span></a></aside>'

def image(match):
    key=match.group(1); title,subtitle,cards=SPECS[key]
    context=next(p['primary'] for p in PAGES if key.startswith(p['key']+'-'))
    alt=f'{context.capitalize()} diagram: '+ '; '.join(f'{a.lower()} — {b.lower()}' for a,b,c in cards)
    return f'<figure><img src="/assets/images/{key}.webp" width="1200" height="650" loading="lazy" decoding="async" alt="{escape(alt)}"><figcaption>{escape(subtitle)} <span>Editorial illustration, not a platform screenshot.</span></figcaption></figure>'

VIDEO='''<div class="video-review">
<span class="eyebrow">Critical review · Not a recommendation</span>
<p><strong>The supplied video's “unlimited tokens” headline is misleading.</strong> No unlimited-credit method is verified here. A genuine promotion is conditional; a generator does not create authorized tokens. Do not follow off-site offers or provide credentials based on this video.</p>
<p>This promotional video was supplied for inclusion, not selected as evidence. Loading it connects to YouTube, which may process device and network data. It does not autoplay.</p>
<div class="video-slot" data-video-slot><span aria-hidden="true" class="play-mark">▷</span><p>External video held until you choose to load it.</p><button class="video-load" type="button">Load supplied video for critical review</button></div>
<template class="video-template"><iframe width="960" height="540" loading="lazy" src="https://www.youtube-nocookie.com/embed/gDtkB1YmXew" title="Supplied promotional video for critical review; unlimited-token claim is not endorsed" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></template>
<noscript><p>Video loading needs JavaScript. You can <a href="https://www.youtube.com/watch?v=gDtkB1YmXew" rel="nofollow noopener" target="_blank">view the supplied video on YouTube<span class="visually-hidden"> (opens in a new tab)</span></a>. The same warning applies: its unlimited-token framing is not advice.</p></noscript>
<p class="small">The written guide is complete without this video. No purchase, installation or verification task is needed to read it.</p></div>'''

def nav(path):
    return ''.join(f'<a href="{p["path"]}"'+(' aria-current="page"' if path==p['path'] else '')+f'>{p["short"]}</a>' for p in PAGES)

def header(path):
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<div class="adult-bar"><div><strong>18+ only.</strong> Independent information for adults. No explicit imagery. <a href="/disclaimer/">Editorial & affiliate disclosure <span aria-hidden="true">↗</span></a></div></div>
<header class="site-header"><a class="brand" href="/" aria-label="OpenRoom home"><span class="brand-icon" aria-hidden="true">o<span></span></span><span>openroom<span class="brand-sub">INDEPENDENT FIELD NOTES</span></span></a><nav aria-label="Main navigation">{nav(path)}</nav><span class="header-note">Clear advice.<br>No false promises.</span></header>'''

def footer(path):
    links=''.join(f'<a href="/{key}/">{title}</a>' for key,(title,_,__) in LEGAL.items())
    return f'''<footer class="site-footer"><div class="footer-top"><a class="brand" href="/">openroom<span class="brand-sub">INDEPENDENT FIELD NOTES</span></a><p>Read the terms.<br>Keep your boundaries.</p><a href="#top" class="back-top">Back to top ↑</a></div><div class="footer-links"><nav aria-label="Footer guides">{nav(path)}</nav><nav aria-label="Publication information">{links}</nav></div><div class="footer-bottom"><span>© 2026 OpenRoom · 18+ only</span><p>Independent commentary. Not an official platform or support service. External commercial resource links are marked sponsored/nofollow. Prices and access rules can change.</p></div></footer>'''

DISCLOSURE='''<aside class="disclosure" aria-label="Adult notice and affiliate disclosure"><p><strong>18+ notice.</strong> For adults who meet the legal age and access rules in their location. No explicit imagery is published here.</p><p><strong>Affiliate disclosure.</strong> External resource buttons lead to commercial publishers and are marked sponsored/nofollow conservatively. No affiliate commission arrangement has been verified for this build. They are not official support. <a href="/disclaimer/">Read the full disclosure</a>.</p></aside>'''

def render_content(raw):
    raw=re.sub(r'\[\[image:([\w-]+)\]\]',image,raw)
    raw=re.sub(r'\[\[cta:([\w-]+)\]\]',cta,raw)
    raw=raw.replace('[[video]]',VIDEO)
    html=markdown.markdown(raw,extensions=['tables','sane_lists'])
    soup=BeautifulSoup(html,'html.parser')
    # Make all tables keyboard scrollable and preserve semantic headers.
    for table in soup.find_all('table'):
        caption=soup.new_tag('caption'); caption.string='Comparison details — check current official conditions'
        table.insert(0,caption)
        for th in table.find_all('th'): th['scope']='col'
        wrapper=soup.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','role':'region','aria-label':'Scrollable comparison table'})
        table.wrap(wrapper)
    used=set()
    for h in soup.find_all(['h2','h3']):
        anchor=slug(h.get_text()); original=anchor; n=2
        while anchor in used: anchor=f'{original}-{n}'; n+=1
        used.add(anchor); h['id']=anchor
    return soup

def author():
    return '''<aside class="author-box" aria-label="About the author"><div class="author-avatar" aria-hidden="true">OR</div><div><span class="eyebrow">Written by</span><p class="author-name"><a href="/about/">OpenRoom Editorial Desk</a></p><p>An independent publication byline focused on adult-platform costs, privacy and consumer safety. Source-based and AI-assisted; no firsthand platform testing or professional credentials are claimed. <a href="/about/">Our methods and limitations</a>.</p></div></aside>'''

def source_section(page):
    sources=list(SOURCES)
    if page['key']=='sites':
        sources += [('Chaturbate Terms & Conditions','https://chaturbate.com/terms/','Adult eligibility and the independent broadcaster platform.'),('BongaCams Terms and Conditions','https://bongacams.com/terms','Age-of-majority definition and service conditions.')]
    items=''.join(f'<li><a href="{escape(u)}">{escape(t)}</a><p>{escape(d)}</p></li>' for t,u,d in sources)
    return f'''<h2 id="sources-and-editorial-notes">Sources and editorial notes</h2><p>Official documents checked on <time datetime="{DATE}">15 October 2026</time>. We cite published rules, not access to private platform systems. Live checkout and local requirements must be verified separately.</p><ol class="sources">{items}</ol><p>External resources are secondary commentary, not verification of every claim they contain. No automatic welcome balance, universal first-purchase bonus, permanent crypto bonus or authenticated three-platform price list was verified. All numeric cost examples are fictional illustrations.</p><p>All diagrams are original, non-explicit editorial illustrations. The supplied promotional video is included for critical review only; its unlimited-token framing is not endorsed. <a href="/contact/">Report an editorial correction</a>.</p>'''

def toc(soup):
    items=''.join(f'<li class="toc-{h.name}"><a href="#{h["id"]}">{escape(h.get_text())}</a></li>' for h in soup.find_all(['h2','h3']))
    return f'<nav class="toc" aria-label="Table of contents"><span class="eyebrow">IN THIS GUIDE</span><ol>{items}</ol><a class="toc-return" href="#top">Back to overview ↑</a></nav>'

def faq_schema(soup):
    faq=soup.find('h2',id='frequently-asked-questions'); questions=[]
    if not faq:return questions
    node=faq.find_next_sibling()
    while node and node.name!='h2':
        if node.name=='h3':
            p=node.find_next_sibling('p')
            questions.append({'@type':'Question','name':node.get_text(),'acceptedAnswer':{'@type':'Answer','text':p.get_text(' ',strip=True)}})
        node=node.find_next_sibling()
    return questions

def schema(page,soup):
    url=BASE+page['path']; questions=faq_schema(soup)
    article={'@context':'https://schema.org','@type':'Article','headline':page['h1'],'description':page['description'],'datePublished':DATE,'dateModified':DATE,'inLanguage':'en','isAccessibleForFree':True,'author':{'@type':'Organization','name':'OpenRoom Editorial Desk','url':BASE+'/about/'},'publisher':{'@type':'Organization','name':'OpenRoom','url':BASE+'/'},'mainEntityOfPage':{'@type':'WebPage','@id':url},'image':[BASE+'/assets/images/social.webp'],'citation':[u for t,u,d in SOURCES]}
    blocks=[article]
    if questions: blocks.append({'@context':'https://schema.org','@type':'FAQPage','mainEntity':questions})
    return ''.join('<script type="application/ld+json">'+json.dumps(block,ensure_ascii=False).replace('<','\\u003c')+'</script>' for block in blocks)

def shell(page,body,structured=''):
    title=escape(page['title']); desc=escape(page['description']); url=escape(BASE+page['path'])
    document=f'''<!doctype html>
<html lang="en" id="top"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow"><meta name="theme-color" content="#f6f4ed"><meta name="referrer" content="strict-origin-when-cross-origin"><link rel="canonical" href="{url}"><meta property="og:type" content="article"><meta property="og:site_name" content="OpenRoom"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{escape(BASE)}/assets/images/social.webp"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="OpenRoom: clear guides, no false promises"><meta property="og:locale" content="en_GB"><meta property="article:modified_time" content="{DATE}T00:00:00Z"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/styles.css">{structured}<script src="/assets/video.js" defer></script></head><body>{header(page['path'])}{body}{footer(page['path'])}</body></html>'''
    # Project Pages uses /repository-name/ rather than the domain root.
    # Only root-relative HTML href/src attributes are rewritten; external URLs,
    # fragments and canonical/structured-data URLs remain intact.
    if BASE_PATH:
        document=re.sub(r'(\b(?:href|src)=")/(?!/)',lambda m:m.group(1)+BASE_PATH+'/',document)
    return document

def visual(page):
    if page['key']=='home':
        top=('PUBLIC ROOM','Free to watch','No purchase required'); bottom=('PAID FEATURES','Your choice. Your limit.','Tips · Private · Ticketed access')
    elif page['key']=='generator':
        top=('LOCAL DISPLAY','A fake counter ≠ credit','An animation is not a transaction'); bottom=('THE REAL REFERENCE','Official account history','No downloads. No passwords. No surveys.')
    elif page['key']=='live':
        top=('ROOM FORMAT','Watch or participate?','Public · Private · Spectator · Ticket'); bottom=('BEFORE YOU JOIN','Check rate + permissions','Know the audience. Find the exit.')
    else:
        top=('THE SAME QUESTION','What does it really cost?','Stripchat · Chaturbate · BongaCams'); bottom=('A FAIR COMPARISON','Price × purpose','Compare the outcome, not the units.')
    return f'''<aside class="hero-visual" aria-label="Guide at a glance"><div class="mock-top"><span class="mock-dots" aria-hidden="true">● ● ●</span><span>OPENROOM / READER NOTES</span><span>18+</span></div><div class="mock-main"><span class="eyebrow">{top[0]}</span><p>{top[1]}</p><span class="mock-small">{top[2]}</span><div class="signal-bars" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><span class="mock-status">● &nbsp; Information, not a live feed</span></div><div class="mock-bottom"><span class="eyebrow">{bottom[0]}</span><p>{bottom[1]}</p><span>{bottom[2]}</span></div><div class="mock-caption"><span>Independent. Non-explicit.</span><span aria-hidden="true">↗</span></div></aside>'''

def main():
    manifest={}
    for page in PAGES:
        raw=(ROOT/'content'/f'{page["key"]}.md').read_text()
        soup=render_content(raw)
        # Intro lives beside the visual; all remaining sections follow the contents.
        intro=[]
        while soup.contents and not (getattr(soup.contents[0],'name',None)=='h2'):
            intro.append(str(soup.contents[0].extract()))
        source=BeautifulSoup(source_section(page),'html.parser')
        for child in list(source.contents):soup.append(child.extract())
        count=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",BeautifulSoup(''.join(intro)+str(soup),'html.parser').get_text(' ',strip=True)))
        read=max(1,round(count/230))
        hero=f'''<main id="main"><section class="hero" aria-labelledby="page-title"><div class="hero-copy"><div class="edition"><span class="eyebrow">{page['category']}</span><span class="issue">FIELD NOTE / {page['number']}</span></div><h1 id="page-title">{escape(page['h1'])}</h1><p class="deck">{escape(page['deck'])}</p><div class="byline"><a href="/about/">OpenRoom Editorial Desk</a><span>Last updated <time datetime="{DATE}">15 October 2026</time> · {read} min read</span></div></div>{visual(page)}</section><section class="quick-take" aria-label="Key takeaways"><div><span>01 / ACCESS</span><p>Free public viewing is not free paid access.</p></div><div><span>02 / COST</span><p>Read the live price. Keep a cash limit.</p></div><div><span>03 / TRUST</span><p>Official records beat promotional promises.</p></div></section><div class="article-layout">{toc(soup)}<article class="article" aria-labelledby="page-title"><div class="article-intro">{''.join(intro)}</div>{DISCLOSURE}{str(soup)}{author()}<a class="end-link" href="#top">Back to the top of this guide ↑</a></article></div></main>'''
        output=shell(page,hero,schema(page,soup))
        dest=ROOT / (page['path'].strip('/')+'/index.html' if page['path']!='/' else 'index.html')
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(output)
        manifest[page['path']]={'words':count,'images':len(soup.find_all('img')),'faqs':len(faq_schema(soup)),'ctas':len(soup.select('.cta-btn'))}
    for key,(title,description,text) in LEGAL.items():
        page={'path':f'/{key}/','title':title+' | OpenRoom','description':description}
        soup=render_content(text)
        body=f'''<main id="main" class="legal-main"><div class="edition"><span class="eyebrow">THE PUBLICATION</span><span>UPDATED 15 OCTOBER 2026</span></div><h1>{escape(title)}</h1><p class="deck">{escape(description)}</p>{DISCLOSURE}<div class="legal-layout">{toc(soup)}<article class="article">{soup}{author()}</article></div></main>'''
        dest=ROOT/key/'index.html';dest.parent.mkdir(exist_ok=True);dest.write_text(shell(page,body))
    paths=[p['path'] for p in PAGES]+[f'/{k}/' for k in LEGAL]
    xml='\n'.join(f'  <url><loc>{escape(BASE+p)}</loc><lastmod>{DATE}</lastmod></url>' for p in paths)
    (ROOT/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{xml}\n</urlset>\n')
    (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
    (ROOT/'content-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for path,result in manifest.items():print(path,result)
    if BASE=='https://example.com':print('PRE-LAUNCH: set SITE_URL to the real HTTPS origin and rebuild.')

if __name__=='__main__':main()
