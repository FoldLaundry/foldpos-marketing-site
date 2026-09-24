#!/usr/bin/env python3
"""Build the inner pages (pricing, FAQ, help, contact, about, printers) and put the shared
header and footer on every page of foldpos.com.

Run from the repository root after editing anything here, partials/ or
index.html (and after build_pages.py, which regenerates the shop pages):

    python3 build_pages.py && python3 build_site.py && python3 check_seo.py

The header and footer live in partials/header.html and partials/footer.html,
styled by assets/css/chrome.css and driven by assets/js/chrome.js. Each page
carries them between <!--fx:header--> / <!--fx:footer--> markers, so running
this again replaces them in place.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://foldpos.com'
os.chdir(ROOT)

HEADER = open('partials/header.html', encoding='utf-8').read().strip()
FOOTER = open('partials/footer.html', encoding='utf-8').read().strip()
# Spanish chrome for es/*.html. {{ALT}} in either is the same page in the other language.
HEADER_ES = open('partials/header.es.html', encoding='utf-8').read().strip()
FOOTER_ES = open('partials/footer.es.html', encoding='utf-8').read().strip()
LASTMOD = '2026-09-23'   # bump when the site content changes
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700'
         '&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">')
CHROME_CSS = '<link rel="stylesheet" href="/assets/css/chrome.css">'
CHROME_JS = '<script src="/assets/js/chrome.js" defer></script>'

# ─── icons: reuse the homepage sprite ───
_sprite = open('index.html', encoding='utf-8').read()
SYMBOLS = {k: v for v, k in re.findall(r'(<symbol id="i-([a-z]+)".*?</symbol>)', _sprite, re.S)}
EXTRA = {
    'search': '<symbol id="i-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4 4"/></symbol>',
    'mail': '<symbol id="i-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></symbol>',
    'import': '<symbol id="i-import" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 17v2.5A1.5 1.5 0 0 0 5.5 21h13a1.5 1.5 0 0 0 1.5-1.5V17"/></symbol>',
    'code': '<symbol id="i-code" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/></symbol>',
    'shield': '<symbol id="i-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 5 6v5.5c0 4.3 3 7.9 7 9.5 4-1.6 7-5.2 7-9.5V6l-7-3z"/><path d="m9 12 2.2 2.2L15.5 10"/></symbol>',
}
SYMBOLS.update(EXTRA)


def ic(name, cls='i'):
    assert name in SYMBOLS, name
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def sprite(body):
    used = sorted(set(re.findall(r'#i-([a-z]+)"', body)))
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
            + ''.join(SYMBOLS[u] for u in used) + '</svg>')


def esc(s):
    return html.escape(s, quote=True)


def md_text(s):
    """Like strip_tags, but keeps links as markdown links (site paths made absolute)."""
    s = re.sub(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
               lambda m: '[%s](%s)' % (re.sub(r'<[^>]+>', '', m.group(2)), (SITE + m.group(1)) if m.group(1).startswith('/') else m.group(1)), s, flags=re.S)
    return strip_tags(s)


def strip_tags(s):
    s = re.sub(r'</?(p|li|ol|ul|div|br|h[1-6])\b[^>]*>', ' ', s)   # block tags become spaces
    s = re.sub(r'<[^>]+>', '', s)                                   # inline tags just go
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


BAND = '''<section class="band"><div class="wrap"><div class="in">
  <div><h2>Try it on your own counter.</h2><p>14 days free. No card, no contract, no sales call.</p></div>
  <div class="acts"><a class="btn btn-primary" href="https://pos.foldpos.com/signup">Start free</a>
  <a class="btn btn-ghost" href="/contact">Talk to us</a></div>
</div></div></section>'''
BAND_CONTACT = BAND.replace('<a class="btn btn-ghost" href="/contact">Talk to us</a>', '<a class="btn btn-ghost" href="/faq">Read the FAQ</a>')


def page(slug, title, desc, og_title, crumb, body, extra_ld=(), script=''):
    url = f'{SITE}/{slug}'
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Fold POS", "item": SITE + '/'},
        {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]}
    lds = [crumbs] + list(extra_ld)
    ld = '\n'.join('<script type="application/ld+json">\n' + json.dumps(x, ensure_ascii=False, indent=1) + '\n</script>' for x in lds)
    band = BAND_CONTACT if slug == 'contact' else BAND
    main = f'<main id="top">\n{body}\n{band}\n</main>'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:title" content="{esc(og_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/assets/img/og-2026.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Fold POS">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(og_title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og-2026.png">
<link rel="alternate" type="text/markdown" href="/{slug}.md">
<meta name="theme-color" content="#1e5eff">
{ld}
{FONTS}
<link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
{sprite(main)}
{main}
{script}
</body>
</html>
'''


def head_block(kicker, h1, lede, crumb):
    return f'''<section class="phead"><div class="wrap">
  <div class="crumbs"><a href="/">Fold POS</a> › {esc(crumb)}</div>
  <div class="kicker">{kicker}</div>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</div></section>'''


def md_footer():
    return ('\n## More\n\n- [Home](/fold-pos.md) · [Pricing](/pricing.md) · [FAQ](/faq.md) · [Help](/help.md)'
            ' · [Contact](/contact.md) · [About](/about.md)\n- [Printers](/printers.md) · [Store setup](/setup.md) · [Print helper](/download.md)'
            ' · [All features](/features.md) · [Developers & AI](/developers.md)'
            '\n- [Hey Fold](/hey-fold.md) · [Pickup & delivery](/pickup-delivery.md)\n')


# ════════════════════════════ PRICING ════════════════════════════
PLANS = [
    ('Starter', 39, 'One counter.', False, [
        'Check-in, orders board and payments', 'Customer accounts and history',
        'Receipts, tags and printing', 'Daily reporting', 'Machine maintenance log', 'Hey Fold']),
    ('Growth', 59, 'Adding delivery and staff.', True, [
        'Everything in Starter', 'Pickup &amp; delivery routing', 'Staff shifts and clock-in',
        'Express and subscription pricing', 'Marketing and order reminders', 'Supply inventory and reorder suggestions']),
    ('Pro', 79, 'More than one location.', False, [
        'Everything in Growth', 'Multi-location reporting', 'Route optimization',
        'Role-based staff permissions', 'Priority support']),
]
ROWS = [
    ('The counter', None),
    ('Check-in by the pound, the piece or the job', 'SGP'), ('Orders board, stations and shelf spots', 'SGP'),
    ('Payments on your own processor', 'SGP'), ('Customer accounts and history', 'SGP'),
    ('Receipts and 1 × 3 in tags on Epson, Star, Bixolon and Zebra', 'SGP'), ('Ready texts in English and Spanish', 'SGP'),
    ('Hey Fold, the counter that listens', 'SGP'), ('Daily reporting', 'SGP'), ('Machine maintenance log', 'SGP'),
    ('Growing the shop', None),
    ('Pickup &amp; delivery routing', 'GP'), ('Staff shifts and clock-in', 'GP'),
    ('Express and subscription pricing', 'GP'), ('Marketing and order reminders', 'GP'),
    ('Supply inventory and reorder suggestions', 'GP'),
    ('More than one door', None),
    ('Multi-location reporting', 'P'), ('Route optimization', 'P'),
    ('Role-based staff permissions', 'P'), ('Priority support', 'P'),
]
PRICING_FAQ = [
    ('Is there a contract?', 'No. Every plan is month to month. Change plans or cancel any time from Settings.'),
    ('Do I need a card to start the trial?', 'No. The first 14 days are free and we don’t ask for a card.'),
    ('What happens when the trial ends?', 'You pick a plan in Settings › Plan &amp; billing. If you don’t, the POS goes read-only: everything you entered stays, and choosing a plan brings it right back.'),
    ('Can I use my own card processor?', 'Yes. Card, cash, check, store credit and split payments, on your processor at your rates.'),
    ('Is Hey Fold extra?', 'No. Hey Fold is built into every plan.'),
    ('What if we have more than five locations?', 'Email <a href="mailto:contact@foldpos.com?subject=More%20than%20five%20locations">contact@foldpos.com</a> and we’ll set it up with you.'),
]


def pricing():
    cards = ''
    for name, price, who, pop, feats in PLANS:
        lis = ''.join(f'<li>{ic("check")}<span>{f}</span></li>' for f in feats)
        cls = 'plan pop' if pop else 'plan'
        badge = '<span class="badge">Most popular</span>' if pop else ''
        btn = 'btn btn-primary' if pop else 'btn btn-ghost'
        cards += (f'<div class="{cls}">{badge}<h3>{name}</h3><div class="for">{who}</div>'
                  f'<div class="price">${price}<small> / month</small></div><ul>{lis}</ul>'
                  f'<a class="{btn}" href="https://pos.foldpos.com/signup">Start free</a></div>')
    trs = ''
    for label, has in ROWS:
        if has is None:
            trs += f'<tr><td class="group" colspan="4">{label}</td></tr>'
            continue
        cells = ''.join(f'<td>{ic("check", "i y")}<span class="visually-hidden">Included</span></td>' if k in has
                        else '<td><span class="n" aria-hidden="true">—</span><span class="visually-hidden">Not included</span></td>' for k in 'SGP')
        trs += f'<tr><td>{label}</td>{cells}</tr>'
    faq = ''.join(f'<details class="qa"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in PRICING_FAQ)
    body = head_block('Pricing', 'One price a month. No surprises.',
                      'Month to month, 14 days free, no card up front. Change or cancel from Settings.', 'Pricing') + f'''
<section class="section"><div class="wrap">
  <h2 class="visually-hidden">Plans</h2>
  <div class="plans">{cards}</div>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap">
  <div class="facts">
    <div class="fact">{ic("card")}<div><b>Your processor, your rates</b><span>Card, cash, check, store credit and split payments.</span></div></div>
    <div class="fact">{ic("mic")}<div><b>Hey Fold on every plan</b><span>Say the order. It’s typed, priced and printing.</span></div></div>
    <div class="fact">{ic("history")}<div><b>No contract</b><span>Month to month. Your data comes with you if you leave.</span></div></div>
  </div>
</div></section>
<section class="section" id="compare"><div class="wrap">
  <h2>Compare plans</h2>
  <p class="sub">Every plan has the whole counter. Growth adds delivery and staff; Pro adds more locations.</p>
  <div class="table-scroll"><table class="compare">
    <thead><tr><th scope="col">What you get</th><th scope="col">Starter<small>$39 / month</small></th><th scope="col">Growth<small>$59 / month</small></th><th scope="col">Pro<small>$79 / month</small></th></tr></thead>
    <tbody>{trs}</tbody>
  </table></div>
</div></section>
<section class="section" id="questions"><div class="wrap narrow">
  <h2>Pricing questions</h2>
  <div style="margin-top:12px">{faq}</div>
  <p class="muted" style="margin-top:20px">More in the <a href="/faq">FAQ</a>.</p>
</div></section>'''
    offers = {"@context": "https://schema.org", "@type": "Product", "name": "Fold POS",
              "description": "Point of sale for laundromats, dry cleaners and tailors.",
              "brand": {"@type": "Brand", "name": "Fold POS"},
              "offers": [{"@type": "Offer", "name": n, "price": f'{p}.00', "priceCurrency": "USD",
                          "url": "https://pos.foldpos.com/signup", "description": strip_tags(w)} for n, p, w, _, _ in PLANS]}
    html_ = page('pricing', 'Pricing — Fold POS', 'Fold POS pricing: Starter $39, Growth $59 and Pro $79 a month. Month to month, 14-day free trial, no card up front, your own card processor, Hey Fold on every plan.',
                 'Fold POS pricing', 'Pricing', body, [offers])
    md = ['# Fold POS pricing', '', '> Canonical page: https://foldpos.com/pricing · Markdown mirror.', '',
          'Month to month, 14-day free trial, no card up front. Change or cancel any time from Settings.', '',
          'Start a free trial: https://pos.foldpos.com/signup', '']
    for name, price, who, pop, feats in PLANS:
        md += [f'## {name} — ${price}/month' + (' (most popular)' if pop else ''), '', md_text(who), '']
        md += [f'- {md_text(f)}' for f in feats] + ['']
    md += ['## Everything else about the money', '']
    md += [f'- **{md_text(q)}** {md_text(a)}' for q, a in PRICING_FAQ]
    return html_, '\n'.join(md) + md_footer()


# ════════════════════════════ FAQ ════════════════════════════
FAQ = [
    ('start', 'Getting started', 'flow', [
        ('What is Fold POS?', '<p>A point of sale and command center for laundromats, dry cleaners and tailors. It follows every order from the counter to the customer’s phone: check-in, tags, the back room, where the order lives, the ready text, pickup and payment, and the reports at the end of the day.</p>'),
        ('Who is it for?', '<p>Laundromats (wash &amp; fold by the pound, the floor and the machines), dry cleaners (every garment its own line and tag, conveyor slots) and tailors (jobs with measurements and fittings). Many shops do more than one; they all live on one counter.</p>'),
        ('Do I need to install anything?', '<p>No. Fold POS runs in any browser at pos.foldpos.com. There is also a desktop app for the counter PC (Windows or Mac) and it runs on the iPad. Windows counter PCs use a small print helper for the printers.</p>'),
        ('How long does it take to set up?', '<p>The <a href="/setup">setup guide</a> is seven short steps: your account, the browser, your price list, the printer, staff, customer texts and a first order. Stuck on a step? Email us and we’ll do it with you.</p>'),
        ('Is it in Spanish?', '<p>Yes. The counter, Hey Fold and the texts your customers get all work in English and Spanish.</p>'),
        ('Can I use Fold POS outside the United States?', '<p>Yes. Shops anywhere in the Americas except Cuba can sign up and run on Fold POS. Plans are billed in US dollars (USD), the counter, Hey Fold and your customer texts work in English and Spanish, and you take payments on your own processor. This site is also <a href="/es/faq" hreflang="es" lang="es">in Spanish</a>.</p>'),
    ]),
    ('pricing', 'Pricing &amp; billing', 'card', [
        ('How much does it cost?', '<p>Starter is $39 a month for one counter, Growth $59 adds delivery and staff, and Pro $79 is for more than one location. See <a href="/pricing">pricing</a> for everything in each plan.</p>'),
        ('Is there a free trial?', '<p>14 days free, with no card up front.</p>'),
        ('Is there a contract?', '<p>No. Every plan is month to month. Change plans or cancel from Settings.</p>'),
        ('What happens after the trial?', '<p>You pick a plan in Settings › Plan &amp; billing. If you don’t, the POS goes read-only: everything you entered stays, and choosing a plan brings it right back.</p>'),
    ]),
    ('printing', 'Printers &amp; hardware', 'printer', [
        ('Which printers does it work with?', '<p>The receipt and tag printers you already own: Epson, Star, Bixolon and Zebra, impact or thermal, USB or network. Receipts print the moment an order is placed, with one 1 × 3 in tag per piece, from a heat-seal tag printer or your impact printer. <a href="/printers">See every printer</a>.</p>'),
        ('Do I need the print helper?', '<p>Chrome can print straight to the printer: Settings › Receipts › Connect printer. On Windows, if the list is empty, or if you use Edge or Firefox, install the <a href="/download">Fold print helper</a> and pair it with the 6-digit code from Settings › Receipts. On a Mac, use Chrome; the Mac helper is on its way.</p>'),
        ('Windows says “Windows protected your PC.” Is that safe?', '<p>That warning appears because the helper is new. Click <b>More info</b>, then <b>Run anyway</b>. The helper only talks to Fold POS and your printers, and it uninstalls like any other program.</p>'),
        ('Does it run on an iPad?', '<p>Yes. Staff can move work along from an iPad on the wall or a phone in their pocket, and the counter sees it the moment they do.</p>'),
    ]),
    ('switching', 'Switching over', 'import', [
        ('Can I bring my customers from Cents or CleanCloud?', '<p>Yes, from Cents, CleanCloud or a CSV: customers and your price list. Export them from your old system, then open Settings › Import data. You can undo an import.</p>'),
        ('Can I take my data with me if I leave?', '<p>Yes, the same way it came in.</p>'),
        ('Will you help us move?', '<p>Yes. Email <a href="mailto:contact@foldpos.com?subject=Switching%20to%20Fold%20POS">contact@foldpos.com</a> and we’ll do it with you.</p>'),
    ]),
    ('payments', 'Payments', 'split', [
        ('Can I use my own card processor?', '<p>Yes. Card, cash, check, store credit and split payments, on your processor at your rates.</p>'),
        ('Can business accounts pay monthly?', '<p>Yes. Monthly invoicing for accounts, with the card on file or however they pay.</p>'),
    ]),
    ('heyfold', 'Hey Fold', 'mic', [
        ('What is Hey Fold?', '<p>Fold’s voice. Say the customer, the pieces and when it’s due, and the order is typed, priced and printing. Fold reads it back and waits for your “yes” before anything happens.</p>'),
        ('How do I talk to it?', '<p>On a computer, press <span class="kbd">Caps Lock</span> to talk and press it again when you’re done, or tap the orb. It works on every screen.</p>'),
        ('Is it listening all the time?', '<p>No. It stays quiet until you call its name, press <span class="kbd">Caps Lock</span> or tap the orb.</p>'),
        ('Does it cost extra?', '<p>No. Hey Fold is on every plan, in English and Spanish.</p>'),
    ]),
    ('delivery', 'Pickup &amp; delivery', 'car', [
        ('Can I run my own delivery service?', '<p>Yes. Today’s pickups and drop-offs with who’s on each, routes built on a map, and the Fold Driver app for your drivers: today’s stops, navigation, and a photo or signature at the door.</p>'),
        ('What if no driver is free?', '<p>Send it with an Uber Direct courier, booked on your store’s own Uber account from the counter.</p>'),
        ('Which plan has delivery?', '<p>Growth and Pro. Route optimization is on Pro.</p>'),
    ]),
    ('fold', 'About Fold', 'store', [
        ('How is Fold POS related to Fold?', '<p>Fold POS is built by Fold Laundry, a laundry and dry-cleaning service. We run our own counters on it. <a href="/about">Our story</a>.</p>'),
        ('Who do I contact?', '<p><a href="mailto:contact@foldpos.com">contact@foldpos.com</a>, or use the <a href="/contact">contact page</a>.</p>'),
    ]),
]


def faq():
    toc = ''.join(f'<a href="#{k}">{t}</a>' for k, t, _, _ in FAQ)
    groups = ''
    for k, t, icon, qs in FAQ:
        items = ''.join(f'<details class="qa"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in qs)
        groups += f'<div class="faq-group" id="{k}"><h2>{ic(icon)}{t}</h2>{items}</div>'
    body = head_block('FAQ', 'Questions owners ask.', 'Pricing, printers, switching over, Hey Fold and delivery. Can’t find it? <a href="/contact">Ask us</a>.', 'FAQ') + f'''
<section class="section"><div class="wrap"><div class="faq-layout">
  <nav class="faq-toc" aria-label="FAQ topics">{toc}</nav>
  <div>{groups}</div>
</div></div></section>'''
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
        for _, _, _, qs in FAQ for q, a in qs]}
    html_ = page('faq', 'FAQ — Fold POS', 'Answers about Fold POS: pricing and the free trial, printers and the print helper, switching from Cents or CleanCloud, payments, Hey Fold, and pickup & delivery.',
                 'Fold POS FAQ', 'FAQ', body, [ld])
    md = ['# Fold POS FAQ', '', '> Canonical page: https://foldpos.com/faq · Markdown mirror. Anything else: contact@foldpos.com.', '']
    for _, t, _, qs in FAQ:
        md += [f'## {md_text(t)}', '']
        for q, a in qs:
            md += [f'**{md_text(q)}** {md_text(a)}', '']
    return html_, '\n'.join(md) + md_footer()


# ════════════════════════════ HELP ════════════════════════════
TOPICS = [
    ('get-started', 'flow', 'Set up your store', 'setup account sign up start first order new store',
     '<ol><li>Create your account at pos.foldpos.com/signup.</li><li>Open Fold POS in the browser on the counter computer and bookmark it.</li><li>Bring in your price list, or start from ours.</li><li>Connect the receipt printer, add staff, check the customer texts.</li><li>Ring up a real order.</li></ol>',
     '/setup', 'The 7-step setup guide'),
    ('printing', 'printer', 'Connect a printer', 'printer receipt tag print helper windows mac usb epson star bixolon pair code',
     '<ul><li><b>In Chrome:</b> Settings › Receipts › Connect printer, then print a test page.</li><li><b>On Windows</b>, if the list is empty or you use Edge or Firefox: install the print helper and type the 6-digit code from Settings › Receipts.</li><li><b>On a Mac:</b> use Chrome.</li><li>Plug the printer in by USB; no need to add it in Windows or macOS.</li></ul>',
     '/printers', 'Printers and how they connect'),
    ('import', 'import', 'Import your data', 'import cents cleancloud csv spreadsheet customers price list switch migrate undo',
     '<ol><li>Export customers and prices from Cents, CleanCloud or a spreadsheet.</li><li>Open Settings › Import data and pick the file.</li><li>Check what came in. You can undo an import.</li></ol>',
     '/faq#switching', 'Switching questions'),
    ('heyfold', 'mic', 'Use Hey Fold', 'hey fold voice mic caps lock speak talk order spanish',
     '<ol><li>Press <span class="kbd">Caps Lock</span> (or tap the orb) and say the order: “two shirts and a suit for Maria, ready Thursday.”</li><li>Fold reads it back with the price.</li><li>Say “yes”. The ticket and tags print.</li></ol>',
     '/#heyfold', 'Try the live demo'),
    ('staff', 'users', 'Add your staff', 'staff employees login admin pin roles shifts clock in',
     '<ul><li>Employees is in the left menu. Give each person their own login, so tickets show who rang them up.</li><li>Staff check orders in and out; only you change prices and settings.</li><li>On the login screen, staff use the <b>Staff</b> side of the toggle.</li></ul>',
     '/setup', 'Setup step 5'),
    ('texts', 'chat', 'Customer texts', 'texts sms ready message customers reminder spanish notifications',
     '<ul><li>The ready text goes out the moment the last piece lands, in your shop’s name.</li><li>It’s on already. Change the wording or turn off anything you don’t want in Settings.</li><li>In English or Spanish.</li></ul>',
     '/setup', 'Setup step 6'),
    ('delivery', 'car', 'Pickup &amp; delivery', 'delivery pickup driver app routes uber courier map',
     '<ul><li>Pickup &amp; delivery in the left menu shows today’s runs and who’s on each.</li><li>Build routes on the map; drivers use the Fold Driver app.</li><li>No driver free? Send it with Uber Direct from the Courier tab.</li></ul>',
     '/faq#delivery', 'Delivery questions'),
    ('billing', 'card', 'Plan &amp; billing', 'billing plan trial cancel upgrade downgrade invoice subscription price',
     '<ul><li>Settings › Plan &amp; billing to pick, change or cancel a plan.</li><li>After the 14-day trial without a plan, the POS goes read-only; your data stays.</li></ul>',
     '/pricing', 'See the plans'),
    ('developers', 'code', 'Developers &amp; AI', 'api mcp developers ai agents llms markdown integration',
     '<ul><li>Markdown copies of every page, llms.txt, and a public read-only MCP server.</li><li>Access to the store-owner API: email us.</li></ul>',
     '/developers', 'Developers &amp; AI'),
]


def help_():
    cards = ''
    for k, icon, t, kw, content, href, more in TOPICS:
        cards += (f'<article class="topic" id="{k}" data-kw="{esc(kw + " " + strip_tags(t).lower())}"><div class="ic">{ic(icon)}</div>'
                  f'<h3>{t}</h3>{content}<a class="more" href="{href}">{more} →</a></article>')
    body = head_block('Help center', 'How can we help?', 'Short answers for the counter. Still stuck? We’ll do it with you.', 'Help') + f'''
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="search" role="search">{ic("search")}<label class="visually-hidden" for="helpq">Search help</label>
    <input id="helpq" type="search" placeholder="Search: printer, import, Caps Lock, billing…" autocomplete="off"></div>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap">
  <h2 class="visually-hidden">Help topics</h2>
  <div class="topics" id="topics">{cards}</div>
  <p class="noresults" id="noresults" hidden>Nothing matches that. Try another word, check the <a href="/faq">FAQ</a>, or <a href="/contact">ask us</a>.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="routes" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr));display:grid">
    <a class="route" href="mailto:contact@foldpos.com?subject=Fold%20POS%20help"><span class="ic">{ic("mail")}</span><span><b>Email support</b><span>contact@foldpos.com. Tell us your store name and what you see.</span></span></a>
    <a class="route" href="/faq"><span class="ic">{ic("chat")}</span><span><b>Read the FAQ</b><span>Pricing, printers, switching, Hey Fold, delivery.</span></span></a>
    <a class="route" href="/setup"><span class="ic">{ic("check")}</span><span><b>Setup guide</b><span>Seven short steps to your first order.</span></span></a>
  </div>
</div></section>'''
    script = '''<script>
(function(){
  var q=document.getElementById('helpq'), cards=[].slice.call(document.querySelectorAll('.topic')), none=document.getElementById('noresults');
  function run(){ var t=(q.value||'').toLowerCase().trim().split(/\\s+/).filter(Boolean), n=0;
    cards.forEach(function(c){ var hay=(c.getAttribute('data-kw')+' '+c.textContent).toLowerCase(), ok=t.every(function(w){return hay.indexOf(w)>-1});
      c.hidden=!ok; if(ok) n++; }); none.hidden=n>0; }
  q.addEventListener('input',run);
})();
</script>'''
    html_ = page('help', 'Help center — Fold POS', 'Fold POS help: set up your store, connect a receipt or tag printer, import from Cents or CleanCloud, use Hey Fold, add staff, customer texts, delivery and billing.',
                 'Fold POS help center', 'Help', body, script=script)
    md = ['# Fold POS help center', '', '> Canonical page: https://foldpos.com/help · Markdown mirror. Still stuck? contact@foldpos.com and we’ll do it with you.', '']
    for k, icon, t, kw, content, href, more in TOPICS:
        md += [f'## {md_text(t)}', '']
        for li in re.findall(r'<li>(.*?)</li>', content, re.S):
            md.append(f'- {strip_tags(li)}')
        link = href if href.startswith('http') else SITE + href
        md += ['', f'{md_text(more)}: {link}', '']
    return html_, '\n'.join(md) + md_footer()


# ════════════════════════════ CONTACT ════════════════════════════
ROUTES_ = [
    ('sales', 'stores', 'See it on your counter', 'A walkthrough with your own price list and questions.', 'Fold POS demo'),
    ('switch', 'import', 'Switch from another system', 'Cents, CleanCloud or a spreadsheet. We’ll move it with you.', 'Switching to Fold POS'),
    ('support', 'chat', 'Help with my store', 'Printers, Hey Fold, texts, billing. Tell us your store name.', 'Fold POS help'),
    ('api', 'code', 'Partners and the API', 'Integrations, the store-owner API, the MCP server.', 'Fold POS API'),
]


def contact():
    routes = ''.join(
        f'<a class="route" href="mailto:contact@foldpos.com?subject={esc(s.replace(" ", "%20"))}"><span class="ic">{ic(i)}</span>'
        f'<span><b>{t}</b><span>{d}</span></span></a>' for k, i, t, d, s in ROUTES_)
    opts = ''.join(f'<option value="{esc(s)}">{strip_tags(t)}</option>' for k, i, t, d, s in ROUTES_)
    body = head_block('Contact', 'Talk to the people who built it.', 'We run laundry counters ourselves. Write to <a href="mailto:contact@foldpos.com">contact@foldpos.com</a>, or use the form and it opens in your email.', 'Contact') + f'''
<section class="section" style="padding-top:12px"><div class="wrap"><div class="contact-grid">
  <div class="routes">{routes}</div>
  <div class="card">
    <h2>Send us a note</h2>
    <p class="muted">This opens a new email to contact@foldpos.com with your note filled in. Nothing is sent until you press send.</p>
    <form class="form" id="cform">
      <div class="row">
        <label for="cname">Your name<input id="cname" name="name" autocomplete="name" required></label>
        <label for="cshop">Store name<input id="cshop" name="shop" autocomplete="organization"></label>
      </div>
      <div class="row">
        <label for="cemail">Email<input id="cemail" name="email" type="email" autocomplete="email" required></label>
        <label for="ctopic">About<select id="ctopic" name="topic">{opts}</select></label>
      </div>
      <label for="cmsg">Message<textarea id="cmsg" name="message" required placeholder="What kind of shop, how many locations, what you use today…"></textarea></label>
      <button class="btn btn-primary" type="submit">Open in my email</button>
      <p class="note">Prefer to write directly? <a href="mailto:contact@foldpos.com">contact@foldpos.com</a></p>
    </form>
  </div>
</div></div></section>'''
    script = '''<script>
(function(){
  var f=document.getElementById('cform'); if(!f) return;
  f.addEventListener('submit',function(e){ e.preventDefault(); if(!f.reportValidity()) return;
    var v=function(id){return document.getElementById(id).value.trim()};
    var body=v('cmsg')+'\\n\\n'+v('cname')+(v('cshop')?' · '+v('cshop'):'')+'\\n'+v('cemail');
    window.location.href='mailto:contact@foldpos.com?subject='+encodeURIComponent(v('ctopic')+(v('cshop')?' · '+v('cshop'):''))+'&body='+encodeURIComponent(body); });
})();
</script>'''
    org = {"@context": "https://schema.org", "@type": "ContactPage", "url": f'{SITE}/contact', "name": "Contact Fold POS",
           "mainEntity": {"@type": "Organization", "@id": f'{SITE}/#organization', "name": "Fold POS",
                          "contactPoint": [{"@type": "ContactPoint", "contactType": "customer support", "email": "contact@foldpos.com", "availableLanguage": ["English", "Spanish"]},
                                           {"@type": "ContactPoint", "contactType": "sales", "email": "contact@foldpos.com"}]}}
    html_ = page('contact', 'Contact — Fold POS', 'Contact Fold POS: a demo on your own counter, help switching from Cents or CleanCloud, support for your store, or partnerships and the API. contact@foldpos.com.',
                 'Contact Fold POS', 'Contact', body, [org], script)
    md = ['# Contact Fold POS', '', '> Canonical page: https://foldpos.com/contact · Markdown mirror.', '',
          'Email: contact@foldpos.com', '']
    md += [f'- **{md_text(t)}**: {md_text(d)} Subject line: "{s}".' for k, i, t, d, s in ROUTES_]
    return html_, '\n'.join(md) + '\n' + md_footer()


# ════════════════════════════ ABOUT ════════════════════════════
def about():
    values = [
        ('store', 'Built at a real counter', 'We run our own counters on Fold POS, so we feel what you feel.'),
        ('history', 'Month to month', 'No contracts, no card to start. We keep you by being useful.'),
        ('import', 'Your data is yours', 'Bring it in from Cents, CleanCloud or a CSV, and take it with you the same way.'),
        ('globe', 'English and Spanish', 'The counter, Hey Fold and your customers’ texts, in both.'),
    ]
    vals = ''.join(f'<div class="fact">{ic(i)}<div><b>{t}</b><span>{d}</span></div></div>' for i, t, d in values)
    body = head_block('About', 'Built by store owners.', 'Fold POS comes from Fold Laundry, a laundry and dry-cleaning service. We wrote the software we couldn’t buy.', 'About') + f'''
<section class="section"><div class="wrap narrow"><div class="story">
  <p>Fold does wash &amp; fold, dry cleaning, same-day service, and free pickup and delivery. We looked for software to run it on, and everything we found was built for some other kind of store.</p>
  <p class="pull">Nothing we could buy knew what a comforter was.</p>
  <p>So we built our own. A counter that prices a bag by the pound, a shirt by the piece and a hem by the job. Tags that know which order they belong to. A back room that sees what the counter sees. A text that tells the customer it’s ready before she has to call. And <b>Hey Fold</b>, so the person at the counter can say the order with their hands full.</p>
  <p>We run our own stores on it every day. When it gets in our way, we fix it, and the fix reaches your store too.</p>
</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap narrow">
  <h2>What we care about</h2>
  <div class="values" style="margin-top:20px">{vals}</div>
</div></section>'''
    html_ = page('about', 'About — Fold POS', 'Fold POS is built by Fold Laundry, a laundry and dry-cleaning service, because nothing it could buy knew what a comforter was. Built at a real counter, month to month, in English and Spanish.',
                 'About Fold POS', 'About', body)
    md = ['# About Fold POS', '', '> Canonical page: https://foldpos.com/about · Markdown mirror.', '',
          strip_tags(body.split('<div class="story">')[1].split('</div>')[0]).replace(' Nothing we could', '\n\nNothing we could'), '',
          '## What we care about', ''] + [f'- **{t}**: {d}' for i, t, d in values]
    return html_, '\n'.join(md) + '\n' + md_footer()


# ════════════════════════════ PRINTERS ════════════════════════════
PRINTER_KINDS = [
    ('printer', 'Receipt printers', 'Epson (TM-T20), Star and Bixolon (SRP-275), impact or thermal.', [
        'A customer copy and a store copy the moment you submit the order',
        'Claim tickets on the impact printer you already own',
        'Reprint the ticket from Check out without leaving the screen']),
    ('tag', 'Tag printers', 'Zebra heat-seal, or 1 × 3 in tags on your impact printer.', [
        'One tag per piece, numbered 1/3, 2/3, 3/3, so nothing goes home alone',
        'Lot number, piece count, customer, due day and barcode on every tag',
        'Permanent heat-sealed barcodes for regulars: scan the garment, it knows the customer']),
    ('scan', 'Barcode scanners', 'Any USB keyboard-wedge scanner.', [
        'Scan a tag at Check out and the whole order comes up',
        'Find a returning customer by barcode mid-order',
        'Plug it in; there is nothing to set up']),
]
CONNECT = [
    ('Chrome, on Windows or a Mac', 'Prints straight to the printer.', 'Settings › Receipts › Connect printer, pick it from the list, print a test page.'),
    ('Windows with Edge or Firefox, or an empty list in Chrome', 'Use the Fold print helper.', 'Install it from <a href="/download">foldpos.com/download</a>, then type the 6-digit code from Settings › Receipts. It stays paired after a restart.'),
    ('A Mac with Safari or Firefox', 'Use Chrome for now.', 'The Mac print helper is on its way. <a href="/contact">Email us</a> and we’ll set you up in the meantime.'),
]
PRINTER_FAQ = [
    ('Do I have to add the printer in Windows or macOS first?', 'No. Plug it in by USB and leave it at that. Fold POS finds it from Settings › Receipts.'),
    ('USB or network?', 'Both work. Most counters use USB to the counter computer.'),
    ('Windows says “Windows protected your PC.”', 'The print helper is new, so Windows doesn’t know it yet. Click <b>More info</b>, then <b>Run anyway</b>. The helper only talks to Fold POS and your printers, and uninstalls like any other program.'),
    ('The printer isn’t in the list.', 'On Windows, install the <a href="/download">print helper</a> and pair it. Still missing? Email <a href="mailto:contact@foldpos.com?subject=Printer%20help">contact@foldpos.com</a> with the printer’s make and model.'),
    ('Can I turn the barcode on tags off?', 'Yes. There’s a switch for barcodes on garment tags in Settings.'),
    ('I don’t have a tag printer yet.', 'Start with receipts and add tags when you’re ready. Tell us what you’re looking at and we’ll tell you if it works.'),
]


def printers():
    kinds = ''
    for i, t, sub, pts in PRINTER_KINDS:
        lis = ''.join(f'<li>{ic("check")}<span>{p}</span></li>' for p in pts)
        kinds += f'<div class="pkind"><div class="ic">{ic(i)}</div><h3>{t}</h3><p class="muted">{sub}</p><ul>{lis}</ul></div>'
    brands = ''.join(f'<span>{b}</span>' for b in ('Epson', 'Star', 'Bixolon', 'Zebra'))
    tags = ''.join(f'<div class="t13"><b>W1042 {n}/3 &nbsp;ORTIZ</b><b class="r">FRI 09/18</b><span>{it}</span></div>'
                   for n, it in ((1, 'Comforter - Wash &amp; Fold'), (2, 'Bag 1 - Wash &amp; Fold'), (3, 'Bag 2 - Wash &amp; Fold')))
    rows = ''.join(f'<tr><th scope="row">{w}</th><td><b>{a}</b><br><span class="muted">{h}</span></td></tr>' for w, a, h in CONNECT)
    faq = ''.join(f'<details class="qa"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in PRINTER_FAQ)
    body = head_block('Printers', 'Prints on the printers you already own.',
                      'Receipts, 1 × 3 in garment tags and barcode scanners. Epson, Star, Bixolon and Zebra, USB or network.', 'Printers')
    body += (
        '<section class="section" style="padding-top:8px"><div class="wrap">'
        f'<div class="brands" aria-label="Supported printer brands">{brands}</div>'
        '<h2 class="visually-hidden">What prints</h2>'
        f'<div class="pkinds">{kinds}</div></div></section>\n'
        '<section class="section" id="tags"><div class="wrap"><div class="tagsplit">'
        '<div><h2>One tag per piece.</h2><p class="sub">Tags print beside the receipt at check-in: the order, the piece number, '
        'the customer, the due day and what the piece is. Scan any tag and the whole order comes up.</p></div>'
        f'<div class="tagstack" aria-label="Example tags for order W1042">{tags}</div></div></div></section>\n'
        '<section class="section" id="connect"><div class="wrap"><h2>How it connects</h2>'
        '<p class="sub">Fold POS runs in the browser, so how it reaches the printer depends on the browser.</p>'
        f'<div class="table-scroll"><table class="connect"><tbody>{rows}</tbody></table></div>'
        '<ol class="steps3">'
        '<li><b>Plug it in.</b> USB to the counter computer, or on your network.</li>'
        '<li><b>Connect it.</b> Settings › Receipts. Chrome lists it; otherwise pair the print helper with the 6-digit code.</li>'
        '<li><b>Print a test page.</b> Then ring up an order: the ticket and tags print together.</li></ol>'
        f'<p style="margin-top:22px"><a class="btn btn-ghost" href="/download">{ic("import")}Download the print helper for Windows</a></p>'
        '</div></section>\n'
        '<section class="section" id="printer-questions"><div class="wrap narrow"><h2>Printer questions</h2>'
        f'<div style="margin-top:12px">{faq}</div></div></section>')
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in PRINTER_FAQ]}
    html_ = page('printers', 'Printers — Fold POS', 'Printers that work with Fold POS: Epson, Star and Bixolon receipt printers, Zebra heat-seal and 1 × 3 in garment tags, and USB barcode scanners. How each browser connects, and the Windows print helper.',
                 'Fold POS printers', 'Printers', body, [ld])
    md = ['# Printers that work with Fold POS', '', '> Canonical page: https://foldpos.com/printers · Markdown mirror.', '',
          'Epson, Star, Bixolon and Zebra, impact or thermal, USB or network. Keep the hardware you have.', '']
    for i, t, sub, pts in PRINTER_KINDS:
        md += [f'## {t}', '', md_text(sub), ''] + [f'- {md_text(p)}' for p in pts] + ['']
    md += ['## How it connects', ''] + [f'- **{md_text(w)}**: {md_text(a)} {md_text(h)}' for w, a, h in CONNECT]
    md += ['', 'Print helper for Windows: https://foldpos.com/download', '', '## Printer questions', '']
    md += [f'**{md_text(q)}** {md_text(a)}\n' for q, a in PRINTER_FAQ]
    return html_, '\n'.join(md) + md_footer()

# ════════════════════════════ chrome on every page ════════════════════════════
ACTIVE = {'hey-fold.html': '/hey-fold', 'pickup-delivery.html': '/pickup-delivery', 'printers.html': '/printers', 'pricing.html': '/pricing', 'faq.html': '/faq', 'help.html': '/help', 'contact.html': '/contact',
          'features.html': '/features', 'laundromats.html': '/laundromats', 'dry-cleaners.html': '/dry-cleaners',
          'alterations.html': '/alterations'}


def url_for(fname):
    """Clean URL path of a page file: index.html -> /, es/index.html -> /es/, es/faq.html -> /es/faq."""
    if fname.endswith('index.html'):
        return '/' + fname[:-len('index.html')]
    return '/' + fname[:-len('.html')]


def pair_of(fname):
    """The same page in the other language, or None when it has no translation."""
    other = fname[3:] if fname.startswith('es/') else 'es/' + fname
    return other if os.path.isfile(other) else None


def chrome_for(fname):
    es = fname.startswith('es/')
    h, f = (HEADER_ES, FOOTER_ES) if es else (HEADER, FOOTER)
    cur = ACTIVE.get(fname[3:] if es else fname)
    if cur:
        if es:
            cur = '/es' + cur
        h = h.replace(f'href="{cur}">', f'href="{cur}" aria-current="page">')
        h = h.replace(f'href="{cur}"><b>', f'href="{cur}" aria-current="page"><b>')
    other = pair_of(fname)
    alt = url_for(other) if other else ('/' if es else '/es/')
    h, f = h.replace('{{ALT}}', alt), f.replace('{{ALT}}', alt)
    return f'<!--fx:header-->\n{h}\n<!--/fx:header-->', f'<!--fx:footer-->\n{f}\n<!--/fx:footer-->'


# ═══════════════════════ languages, regions, sitemap ═══════════════════════
# Fold POS sells to shops anywhere in the Americas, in English and Spanish.
AMERICAS = [{"@type": "Place", "name": n} for n in ("North America", "Central America", "South America", "Caribbean")]
LANGS = ["English", "Spanish"]


def hreflang_block(fname):
    other = pair_of(fname)
    if not other:
        return ''
    en, es = (other, fname) if fname.startswith('es/') else (fname, other)
    return ('<!--fx:hreflang-->\n'
            f'<link rel="alternate" hreflang="en" href="{SITE}{url_for(en)}">\n'
            f'<link rel="alternate" hreflang="es" href="{SITE}{url_for(es)}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{SITE}{url_for(en)}">\n'
            '<!--/fx:hreflang-->')


def fix_ld(obj):
    """Languages and service area in the JSON-LD. Returns True if anything changed."""
    changed = False
    if isinstance(obj, list):
        return any([fix_ld(x) for x in obj])
    if not isinstance(obj, dict):
        return False
    t = obj.get('@type')
    if 'availableLanguage' in obj and obj['availableLanguage'] != LANGS:
        obj['availableLanguage'] = LANGS
        changed = True
    if t in ('Organization', 'SoftwareApplication') and obj.get('@id', '').endswith(('#organization', '#software')):
        if obj.get('areaServed') != AMERICAS:
            obj['areaServed'] = AMERICAS
            changed = True
    if t == 'SoftwareApplication' and obj.get('inLanguage') != ['en', 'es']:
        obj['inLanguage'] = ['en', 'es']
        changed = True
    if t == 'Offer' and obj.get('eligibleRegion') != AMERICAS:
        obj['eligibleRegion'] = AMERICAS
        changed = True
    for v in list(obj.values()):
        if isinstance(v, (dict, list)):
            changed = fix_ld(v) or changed
    return changed


def put_lang(fname):
    """hreflang links, og:locale and the JSON-LD language/region fields."""
    s = open(fname, encoding='utf-8').read()
    es = fname.startswith('es/')
    s = re.sub(r'\n?<!--fx:hreflang-->.*?<!--/fx:hreflang-->', '', s, flags=re.S)
    hb = hreflang_block(fname)
    if hb:
        m = re.search(r'<link[^>]*rel="canonical"[^>]*>', s)
        s = s[:m.end()] + '\n' + hb + s[m.end():]
    loc, alt = ('es_419', 'en_US') if es else ('en_US', 'es_419')
    s = re.sub(r'\n<meta (?=[^>]*property="og:locale(?::alternate)?")[^>]*>', '', s)
    m = re.search(r'<meta (?=[^>]*property="og:site_name")[^>]*>', s)
    tags = f'\n<meta property="og:locale" content="{loc}">' + (f'\n<meta property="og:locale:alternate" content="{alt}">' if hb else '')
    s = s[:m.end()] + tags + s[m.end():]

    def ld(m):
        try:
            data = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        if not fix_ld(data):
            return m.group(0)
        return m.group(1) + '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n' + m.group(3)
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, s, flags=re.S)
    open(fname, 'w', encoding='utf-8').write(s)


SITEMAP_PAGES = [('index.html', '1.0'), ('laundromats.html', '0.9'), ('dry-cleaners.html', '0.9'), ('alterations.html', '0.9'),
                 ('features.html', '0.8'), ('hey-fold.html', '0.8'), ('pickup-delivery.html', '0.8'), ('pricing.html', '0.9'), ('faq.html', '0.7'), ('help.html', '0.7'),
                 ('contact.html', '0.6'), ('about.html', '0.5'), ('printers.html', '0.7'), ('developers.html', '0.6'),
                 ('download.html', '0.5'),
                 ('privacy.html', '0.3'), ('terms.html', '0.3')]
SITEMAP_MD = ['fold-pos.md', 'laundromats.md', 'dry-cleaners.md', 'alterations.md', 'features.md', 'pricing.md', 'faq.md',
              'help.md', 'contact.md', 'about.md', 'printers.md', 'setup.md', 'download.md', 'developers.md',
              'hey-fold.md', 'pickup-delivery.md']


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']

    def url(fname, prio):
        e = [f'  <url><loc>{SITE}{url_for(fname)}</loc><lastmod>{LASTMOD}</lastmod><priority>{prio}</priority>']
        other = pair_of(fname)
        if other:
            en, es = (other, fname) if fname.startswith('es/') else (fname, other)
            e.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{url_for(en)}"/>')
            e.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{SITE}{url_for(es)}"/>')
            e.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{url_for(en)}"/>')
            e.append('  </url>')
            return '\n'.join(e)
        return e[0] + '</url>'
    out.append('  <!-- Pages, English -->')
    out += [url(f, p) for f, p in SITEMAP_PAGES]
    out.append('\n  <!-- Pages, Spanish -->')
    out += [url('es/' + f, p) for f, p in SITEMAP_PAGES if os.path.isfile('es/' + f)]
    out.append('\n  <!-- Markdown mirrors for agents -->')
    for f in SITEMAP_MD + ['es/' + m for m in SITEMAP_MD] + ['llms.txt', 'llms-full.txt']:
        if os.path.isfile(f):
            prio = '0.4' if f.startswith('es/') else '0.5' if f in SITEMAP_MD[:7] + ['llms.txt', 'llms-full.txt'] else '0.4'
            out.append(f'  <url><loc>{SITE}/{f}</loc><lastmod>{LASTMOD}</lastmod><priority>{prio}</priority></url>')
    out.append('</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(out) + '\n')


def put_chrome(fname):
    s = open(fname, encoding='utf-8').read()
    hdr, ftr = chrome_for(fname)
    # header: replace our marker block, else the page's own site header.
    if '<!--fx:header-->' in s:
        s = re.sub(r'<!--fx:header-->.*?<!--/fx:header-->', lambda m: hdr, s, count=1, flags=re.S)
    else:
        m = re.search(r'<header\b[^>]*>.*?</header>', s, re.S)
        if m and s.index('<body') < m.start():
            s = s[:m.start()] + hdr + s[m.end():]
        else:
            b = re.search(r'<body[^>]*>', s)
            s = s[:b.end()] + '\n' + hdr + s[b.end():]
    if '<!--fx:footer-->' in s:
        s = re.sub(r'<!--fx:footer-->.*?<!--/fx:footer-->', lambda m: ftr, s, count=1, flags=re.S)
    else:
        ms = list(re.finditer(r'<footer\b[^>]*>.*?</footer>', s, re.S))
        if ms:
            m = ms[-1]
            s = s[:m.start()] + ftr + s[m.end():]
        else:
            i = s.rindex('</body>')
            s = s[:i] + ftr + '\n' + s[i:]
    # The chrome always sits at the edges of <body>, outside any page container.
    hb = re.search(r'<!--fx:header-->.*?<!--/fx:header-->', s, re.S).group(0)
    s = s.replace('\n' + hb, '', 1) if ('\n' + hb) in s else s.replace(hb, '', 1)
    bm = re.search(r'<body[^>]*>', s)
    s = s[:bm.end()] + '\n' + hb + s[bm.end():]
    fb = re.search(r'<!--fx:footer-->.*?<!--/fx:footer-->', s, re.S).group(0)
    s = s.replace(fb + '\n', '', 1) if (fb + '\n') in s else s.replace(fb, '', 1)
    i = s.rindex('</body>')
    s = s[:i] + fb + '\n' + s[i:]
    if CHROME_CSS not in s:
        s = s.replace('</head>', CHROME_CSS + '\n</head>', 1)
    if 'fonts.googleapis.com/css2?family=Sora' not in s:
        s = s.replace(CHROME_CSS, FONTS + '\n' + CHROME_CSS, 1)
    if CHROME_JS not in s:
        s = s.replace('</body>', CHROME_JS + '\n</body>', 1)
    open(fname, 'w', encoding='utf-8').write(s)


def main():
    from pages_heyfold import hey_fold
    from pages_delivery import pickup_delivery
    for slug, fn in (('pricing', pricing), ('faq', faq), ('help', help_), ('contact', contact), ('about', about), ('printers', printers),
                     ('hey-fold', hey_fold), ('pickup-delivery', pickup_delivery)):
        h, md = fn()
        open(f'{slug}.html', 'w', encoding='utf-8').write(h)
        open(f'{slug}.md', 'w', encoding='utf-8').write(md.rstrip() + '\n')
        print('wrote', slug)
    chrome_pages = sorted(f for f in os.listdir('.') if f.endswith('.html') and f not in ('setup.html', 'new.html'))
    chrome_pages += sorted('es/' + f for f in os.listdir('es') if f.endswith('.html'))
    for f in chrome_pages:
        put_chrome(f)
    print('chrome on', ', '.join(chrome_pages))
    for f in chrome_pages + ['setup.html']:
        put_lang(f)
    sitemap()
    print('hreflang, og:locale, JSON-LD regions and sitemap.xml done')


if __name__ == '__main__':
    main()
