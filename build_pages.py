#!/usr/bin/env python3
"""Generate the per-shop landing pages (laundromats.html, dry-cleaners.html,
alterations.html) from index.html, so there is one source of truth.

Run after editing index.html:  python3 build_pages.py
"""
import re
from bs4 import BeautifulSoup

SHOPS = {
    'laundromat': dict(
        file='laundromats.html', name='Laundromat', noun='laundromat', others=[('dry-cleaners', 'For dry cleaners'), ('alterations', 'For tailors')],
        title='Laundromat POS — Fold POS', canonical='https://foldpos.com/laundromats',
        desc='Point of sale for laundromats: wash & fold by the pound, a live floor map of every washer and dryer, machines, supplies, pickup & delivery and staff shifts. 14-day free trial, no card.',
        eyebrow='Point of sale for laundromats', h1='Point of sale for <em>laundromats</em>, not retail.',
        lede='Wash &amp; fold by the pound at the counter, a live map of every washer and dryer on the floor, and every order followed from drop-off to pickup.',
        og='Fold POS for laundromats', md='/laundromats.md', crumb='For laundromats'),
    'drycleaner': dict(
        file='dry-cleaners.html', name='Dry cleaner', noun='dry cleaner', others=[('laundromats', 'For laundromats'), ('alterations', 'For tailors')],
        title='Dry cleaner POS — Fold POS', canonical='https://foldpos.com/dry-cleaners',
        desc='Point of sale for dry cleaners: per-piece tickets, heat-seal garment tags, conveyor slots, alterations on the same ticket, wash & fold and pickup & delivery. 14-day free trial, no card.',
        eyebrow='Point of sale for dry cleaners', h1='Point of sale for <em>dry cleaners</em>, not retail.',
        lede='Garment tags, conveyor slots and per-piece tickets — with wash &amp; fold and pickup &amp; delivery on the same counter when you offer them.',
        og='Fold POS for dry cleaners', md='/dry-cleaners.md', crumb='For dry cleaners'),
    'tailor': dict(
        file='alterations.html', name='Alterations', noun='alterations shop', others=[('laundromats', 'For laundromats'), ('dry-cleaners', 'For dry cleaners')],
        title='Alterations & tailoring POS — Fold POS', canonical='https://foldpos.com/alterations',
        desc='Point of sale for alterations and tailoring shops: per-task pricing, measurements, photos and notes on every ticket, due-date reminders, customers and staff. 14-day free trial, no card.',
        eyebrow='Point of sale for alterations &amp; tailoring', h1='Point of sale for <em>tailors</em>, not retail.',
        lede='Per-task pricing, measurements and photos on every ticket, due-date reminders — and none of the laundry screens in the way.',
        og='Fold POS for tailors', md='/alterations.md', crumb='For tailors'),
}


def jsonld(sh):
    """Per-shop structured data: the home page's SoftwareApplication and FAQPage
    belong to the home page, so a landing page carries a WebPage, the shared
    Organization and a breadcrumb back to the home page instead."""
    url = sh['canonical']
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://foldpos.com/#organization",
  "name": "Fold POS",
  "url": "https://foldpos.com/",
  "logo": "https://foldpos.com/assets/img/og.png",
  "description": "Point of sale and operations software for laundromats, dry cleaners and tailors. Built by Fold Laundry.",
  "parentOrganization": {{ "@type": "Organization", "name": "Fold Laundry LLC" }},
  "contactPoint": [{{
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "contact@foldpos.com",
    "availableLanguage": "English"
  }}]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "{url}#webpage",
  "url": "{url}",
  "name": "{sh['title']}",
  "description": "{sh['desc']}",
  "inLanguage": "en-US",
  "isPartOf": {{ "@id": "https://foldpos.com/#website" }},
  "about": {{ "@id": "https://foldpos.com/#software" }},
  "primaryImageOfPage": "https://foldpos.com/assets/img/og.png",
  "publisher": {{ "@id": "https://foldpos.com/#organization" }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Fold POS", "item": "https://foldpos.com/" }},
    {{ "@type": "ListItem", "position": 2, "name": "{sh['crumb']}", "item": "{url}" }}
  ]
}}
</script>'''

def art(noun):
    """'a laundromat', but 'an alterations shop'."""
    return 'an' if noun[0] in 'aeiou' else 'a'


src = open('index.html', encoding='utf-8').read()

for key, sh in SHOPS.items():
    s = src
    s = s.replace('<html lang="en">', f'<html lang="en" data-shop="{key}">', 1)
    s = re.sub(r'<title>.*?</title>', f'<title>{sh["title"]}</title>', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{sh["desc"]}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{sh["canonical"]}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{sh["og"]}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{sh["desc"]}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{sh["canonical"]}">', s, count=1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{sh["og"]}">', s, count=1)
    s = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{sh["desc"]}">', s, count=1)
    s = re.sub(r'<link rel="alternate" type="text/markdown" href="[^"]*">', f'<link rel="alternate" type="text/markdown" href="{sh["md"]}">', s, count=1)
    # structured data: swap the home page's graph for this page's
    s = re.sub(r'<!--JSONLD-->.*?<!--/JSONLD-->', lambda m: jsonld(sh), s, count=1, flags=re.S)
    # hero
    s = re.sub(r'<span class="eyebrow" id="heroEyebrow">.*?</span>', f'<span class="eyebrow" id="heroEyebrow">{sh["eyebrow"]}</span>', s, count=1)
    s = re.sub(r'<h1 id="heroTitle">.*?</h1>', f'<h1 id="heroTitle">{sh["h1"]}</h1>', s, count=1)
    s = re.sub(r'<p class="lede" id="heroLede">.*?</p>', f'<p class="lede" id="heroLede">{sh["lede"]}</p>', s, count=1)
    # links between pages are relative to the site root; anchors stay on this page
    s = s.replace('href="#shops"', 'href="#intro"')
    # the FAQ section is dropped below, so the footer's FAQ link goes home
    s = s.replace('href="#faq"', 'href="/#faq"')

    soup = BeautifulSoup(s, 'html.parser')
    # switcher head → "not a X?" row; keep only this shop's intro panel
    head = soup.select_one('.switch-head')
    others = ' '.join(f'<a href="{href}">{label}</a>' for href, label in sh['others'])
    head.clear()
    head.append(BeautifulSoup(
        f'<span class="eyebrow">Built for how your shop works</span>'
        f'<h2>What {art(sh["noun"])} {sh["noun"]} gets on day one.</h2>'
        f'<p class="lede">Choose “{sh["name"]}” at sign-up and this is the POS you see — the tools below and nothing that gets in the way. Change it any time in Settings.</p>'
        f'<div class="shops-row"><span style="align-self:center;color:var(--ink-3);font-size:.9rem">Not {art(sh["noun"])} {sh["noun"]}?</span>{others}</div>', 'html.parser'))
    # the landing page's chapters already say all this; drop the preview panels and the note
    for p in soup.select('.switch-panel'):
        p.decompose()
    n = soup.select_one('.switch-note')
    if n: n.decompose()
    sw = soup.select_one('.switch'); sw['id'] = 'intro'
    # prerender: drop what this shop doesn't see, sort chapters
    for el in list(soup.select('[data-for]')):
        if el.decomposed or el.get('data-for') is None:
            continue
        if key not in el['data-for'].split():
            el.decompose()
    ch = soup.select_one('.chapters .wrap')
    chapters = ch.select('.chapter')
    def order(c):
        m = re.search(key + r':(\d+)', c.get('data-order', ''))
        return int(m.group(1)) if m else 99
    for c in sorted(chapters, key=order):
        ch.append(c.extract())
    # the viewing pill is a home-page thing
    v = soup.select_one('#viewing')
    if v: v.decompose()
    # Shop pages are a pitch, not the whole catalogue: a visitor who picked
    # "dry cleaner" wants the three things that matter to them, pricing and a
    # way in. The overview strip, platform list and FAQ stay on the home page;
    # the "every shop gets" section keeps its words but not its screenshots;
    # only this shop's first three chapters survive.
    for sel in ('.strip', '#platforms', '#faq'):
        el = soup.select_one(sel)
        if el: el.decompose()
    for shot in soup.select('#shared .shot, #shared img, #shared picture'):
        shot.decompose()
    for c in soup.select('.chapters .chapter'):
        if order(c) > 3:
            c.decompose()
    out = str(soup)
    open(sh['file'], 'w', encoding='utf-8').write(out)
    print('wrote', sh['file'], len(out))
