#!/usr/bin/env python3
"""The Hey Fold page of foldpos.com, in English and Spanish.

    from pages_heyfold import hey_fold      # -> (html, md) for slug 'hey-fold'

build_site.py writes the English page like about() and printers(). The Spanish page,
es/hey-fold.html and .md, is a static file like the rest of es/: it is written from
hey_fold_es() below, so run `python3 pages_heyfold.py --es` after changing the Spanish
copy here, then build_site.py (header, footer, hreflang) and check_seo.py.

Every claim comes from the site's own copy: faq.md #heyfold, help.md (Use Hey Fold),
fold-pos.md, pricing.md and the homepage demo. The live demo itself stays on the
homepage (#heyfold); this page links to it rather than carrying a second copy.
"""
import os
import sys

from build_site import page, md_footer, md_text, strip_tags, esc, ic, SITE, BAND
from pages_delivery import BAND_ES, MD_FOOTER_ES

SLUG = 'hey-fold'

EN = {
    'lang': 'en', 'pre': '',
    'title': 'Hey Fold, the counter that listens — Fold POS',
    'desc': 'Hey Fold is the voice of Fold POS. Say the customer, the pieces and the day; the order is priced and printing. English and Spanish, in every plan.',
    'og': 'Hey Fold: the counter that listens',
    'crumb': 'Hey Fold',
    'kicker': 'Hey Fold',
    'h1': 'The counter that listens.',
    'lede': 'Say the customer, the pieces and when it’s due. The order is typed, priced and printing, and Fold reads it back and waits for your “yes” before anything happens.',
    'facts': [
        ('mic', 'In every plan', 'No add-on, no extra cost. Starter, Growth and Pro all have it.'),
        ('chat', 'English and Spanish', 'Talk to it in either. Your customers’ texts go out in either too.'),
        ('check', 'Nothing without your “yes”', 'Fold reads the order back with the price and waits for you.'),
    ],
    'film': True,
    'film_caption': 'Hey Fold at the counter, then the tags, the ready text and the office. 8 seconds, no sound.',
    'how_h2': 'How it works',
    'how_sub': 'Three steps, at the counter or anywhere in the POS.',
    'steps': [
        ('Call it', 'Press <span class="kbd">Caps Lock</span> on the computer, tap the orb, or say its name.'),
        ('Say the order', 'The customer, the pieces and the day: “two shirts and a suit for Maria, ready Thursday.”'),
        ('Say “yes”', 'Fold reads it back with the price. On your “yes”, the ticket and the tags print.'),
    ],
    'say_h2': 'Say it the way you would say it',
    'say_sub': 'A few orders, and what lands on the ticket.',
    'say_head': ('You say', 'On the ticket'),
    'say': [
        ('“Two bags and a comforter, rush it.”', 'Wash &amp; fold by the pound for the two bags, the comforter, and the rush charge. One tag per piece.'),
        ('“Five shirts and a suit for Maria, ready Saturday.”', 'Maria’s ticket: five shirts and a two-piece suit, ready Saturday.'),
        ('“Hem two pairs of pants.”', 'Two hems, as alterations, with the usual turnaround for alterations.'),
        ('“Dos bolsas y un edredón, urgente.”', 'The same order as the first one, said in Spanish.'),
    ],
    'say_note': 'Prices come from your own price list.',
    'try_h2': 'Try it now',
    'try_sub': 'The homepage has a live demo. Type an order, or press Caps Lock and say one, and watch it get rung up.',
    'try_btn': 'Try the live demo',
    'try_href': '/#heyfold',
    'quiet_h2': 'It listens when you ask it to',
    'quiet': [
        ('mic', 'Quiet until called', 'It stays quiet until you call its name, press Caps Lock or tap the orb.'),
        ('check', 'You confirm every order', 'Fold reads the order back and waits for your “yes” before anything happens.'),
        ('flow', 'Every screen', 'On a computer, press Caps Lock to talk and press it again when you’re done, or tap the orb. It works on every screen.'),
        ('card', 'No extra cost', 'Hey Fold is on every plan, in English and Spanish.'),
    ],
    'faq_h2': 'Hey Fold questions',
    'faq': [
        ('What is Hey Fold?', 'Fold’s voice. Say the customer, the pieces and when it’s due, and the order is typed, priced and printing. Fold reads it back and waits for your “yes” before anything happens.'),
        ('How do I talk to it?', 'On a computer, press <span class="kbd">Caps Lock</span> to talk and press it again when you’re done, or tap the orb. It works on every screen.'),
        ('Is it listening all the time?', 'No. It stays quiet until you call its name, press <span class="kbd">Caps Lock</span> or tap the orb.'),
        ('Does it cost extra?', 'No. Hey Fold is on every plan, in English and Spanish.'),
    ],
    'faq_more': 'More in the <a href="/faq#heyfold">FAQ</a> and the <a href="/help#heyfold">help center</a>.',
    'more_h2': 'Where to next',
    'more': [
        ('/#heyfold', 'mic', 'The live demo', 'Say or type an order on the homepage.'),
        ('/help#heyfold', 'flow', 'Use Hey Fold', 'The three steps in the help center.'),
        ('/pricing', 'card', 'Pricing', 'Starter $39, Growth $59, Pro $79. Hey Fold is in all three.'),
        ('/contact', 'mail', 'Talk to us', 'See it on your own counter.'),
    ],
    'md_title': '# Hey Fold: the counter that listens',
    'md_canon': f'> Canonical page: {SITE}/hey-fold · Markdown mirror.',
}

ES = {
    'lang': 'es', 'pre': '/es',
    'title': 'Hey Fold, el mostrador que escucha — Fold POS',
    'desc': 'Hey Fold es la voz de Fold POS. Diga el cliente, las piezas y el día; el pedido queda con precio e imprimiéndose. En español e inglés, en todos los planes.',
    'og': 'Hey Fold: el mostrador que escucha',
    'crumb': 'Hey Fold',
    'kicker': 'Hey Fold',
    'h1': 'El mostrador que escucha.',
    'lede': 'Diga el cliente, las piezas y para cuándo es. El pedido queda escrito, con precio y ya se está imprimiendo; Fold se lo repite y espera su “sí” antes de hacer nada.',
    'facts': [
        ('mic', 'En todos los planes', 'Sin complementos ni costo extra. Starter, Growth y Pro lo incluyen.'),
        ('chat', 'En español e inglés', 'Háblele en cualquiera de los dos. Los mensajes a sus clientes también salen en los dos.'),
        ('check', 'Nada sin su “sí”', 'Fold le repite el pedido con el precio y espera su respuesta.'),
    ],
    'film': False,
    'how_h2': 'Cómo funciona',
    'how_sub': 'Tres pasos, en el mostrador o en cualquier pantalla del POS.',
    'steps': [
        ('Llámelo', 'Presione <span class="kbd">Bloq Mayús</span> (Caps Lock) en la computadora, toque el orbe o diga su nombre.'),
        ('Diga el pedido', 'El cliente, las piezas y el día: “dos camisas y un traje para María, listo el jueves”.'),
        ('Diga “sí”', 'Fold se lo repite con el precio. Con su “sí”, se imprimen el ticket y las etiquetas.'),
    ],
    'say_h2': 'Dígalo como lo diría',
    'say_sub': 'Algunos pedidos, y lo que queda en el ticket.',
    'say_head': ('Usted dice', 'En el ticket'),
    'say': [
        ('“Dos bolsas y un edredón, urgente.”', 'Lavado y doblado por libra para las dos bolsas, el edredón y el cargo por urgencia. Una etiqueta por pieza.'),
        ('“Cinco camisas y un traje para María, listo el sábado.”', 'El ticket de María: cinco camisas y un traje de dos piezas, listo el sábado.'),
        ('“Dobladillo a dos pares de pantalones.”', 'Dos dobladillos, como arreglos, con el plazo habitual de los arreglos.'),
        ('“Two bags and a comforter, rush it.”', 'El mismo pedido que el primero, dicho en inglés.'),
    ],
    'say_note': 'Los precios salen de su propia lista de precios.',
    'try_h2': 'Pruébelo ahora',
    'try_sub': 'La página de inicio tiene una demostración en vivo. Escriba un pedido, o presione Bloq Mayús y dígalo, y vea cómo se registra.',
    'try_btn': 'Probar la demostración',
    'try_href': '/es/#heyfold',
    'quiet_h2': 'Escucha cuando usted se lo pide',
    'quiet': [
        ('mic', 'En silencio hasta que lo llama', 'Se queda en silencio hasta que usted dice su nombre, presiona Bloq Mayús o toca el orbe.'),
        ('check', 'Usted confirma cada pedido', 'Fold le repite el pedido y espera su “sí” antes de hacer nada.'),
        ('flow', 'En todas las pantallas', 'En una computadora, presione Bloq Mayús para hablar y vuelva a presionarla cuando termine, o toque el orbe. Funciona en todas las pantallas.'),
        ('card', 'Sin costo extra', 'Hey Fold viene en todos los planes, en español e inglés.'),
    ],
    'faq_h2': 'Preguntas sobre Hey Fold',
    'faq': [
        ('¿Qué es Hey Fold?', 'La voz de Fold. Diga el cliente, las piezas y para cuándo es, y el pedido queda escrito, con precio y ya se está imprimiendo. Fold se lo repite y espera su “sí” antes de hacer nada.'),
        ('¿Cómo le hablo?', 'En una computadora, presione <span class="kbd">Bloq Mayús</span> (Caps Lock) para hablar y vuelva a presionarla cuando termine, o toque el orbe. Funciona en todas las pantallas.'),
        ('¿Escucha todo el tiempo?', 'No. Se queda en silencio hasta que usted dice su nombre, presiona <span class="kbd">Bloq Mayús</span> o toca el orbe.'),
        ('¿Cuesta extra?', 'No. Hey Fold viene en todos los planes, en español e inglés.'),
    ],
    'faq_more': 'Más en las <a href="/es/faq#heyfold">preguntas frecuentes</a> y en el <a href="/es/help#heyfold">centro de ayuda</a>.',
    'more_h2': 'Para seguir',
    'more': [
        ('/es/#heyfold', 'mic', 'La demostración en vivo', 'Diga o escriba un pedido en la página de inicio.'),
        ('/es/help#heyfold', 'flow', 'Usar Hey Fold', 'Los tres pasos en el centro de ayuda.'),
        ('/es/pricing', 'card', 'Precios', 'Starter $39, Growth $59, Pro $79 (USD). Hey Fold viene en los tres.'),
        ('/es/contact', 'mail', 'Hable con nosotros', 'Véalo en su propio mostrador.'),
    ],
    'md_title': '# Hey Fold: el mostrador que escucha',
    'md_canon': f'> Página canónica: {SITE}/es/hey-fold · Versión en Markdown.',
}

FILM = '''<figure style="margin:0">
    <video controls muted playsinline preload="none" poster="/assets/video/fold-hey-fold-film-poster.jpg" width="1920" height="1080"
      style="width:100%;height:auto;display:block;border-radius:16px;border:1px solid var(--line);background:#0e1730"
      aria-label="Hey Fold at the counter, then the tags, the ready text and the office">
      <source src="/assets/video/fold-hey-fold-film.webm" type="video/webm">
      <source src="/assets/video/fold-hey-fold-film.mp4" type="video/mp4">
    </video>
    <figcaption class="muted" style="margin-top:10px;font-size:14px">{cap}</figcaption>
  </figure>'''


def _build(t):
    pre = t['pre']
    facts = ''.join(f'<div class="fact">{ic(i)}<div><b>{b}</b><span>{s}</span></div></div>' for i, b, s in t['facts'])
    steps = ''.join(f'<li><b>{b}</b>{s}</li>' for b, s in t['steps'])
    rows = ''.join(f'<tr><td style="text-align:left">{a}</td><td style="text-align:left">{b}</td></tr>' for a, b in t['say'])
    quiet = ''.join(f'<div class="fact">{ic(i)}<div><b>{b}</b><span>{s}</span></div></div>' for i, b, s in t['quiet'])
    faq = ''.join(f'<details class="qa"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in t['faq'])
    more = ''.join(f'<a class="route" href="{h}"><div class="ic">{ic(i)}</div><div><b>{b}</b><span>{s}</span></div></a>' for h, i, b, s in t['more'])
    film = f'<section class="section" style="padding-top:0"><div class="wrap narrow">{FILM.format(cap=t["film_caption"])}</div></section>' if t['film'] else ''
    body = f'''<section class="phead"><div class="wrap">
  <div class="crumbs"><a href="{pre}/">Fold POS</a> › {esc(t['crumb'])}</div>
  <div class="kicker">{t['kicker']}</div>
  <h1>{t['h1']}</h1>
  <p class="lede">{t['lede']}</p>
  <p style="margin-top:22px"><a class="btn btn-primary" href="{t['try_href']}">{t['try_btn']}</a></p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="facts">{facts}</div></div></section>
{film}
<section class="section" id="how"><div class="wrap">
  <h2>{t['how_h2']}</h2>
  <p class="sub">{t['how_sub']}</p>
  <ol class="steps3">{steps}</ol>
</div></section>
<section class="section" id="say"><div class="wrap narrow">
  <h2>{t['say_h2']}</h2>
  <p class="sub">{t['say_sub']}</p>
  <div class="table-scroll"><table class="compare" style="min-width:0">
    <thead><tr><th scope="col" style="text-align:left">{t['say_head'][0]}</th><th scope="col" style="text-align:left">{t['say_head'][1]}</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <p class="muted" style="margin-top:14px">{t['say_note']}</p>
</div></section>
<section class="section" id="try"><div class="wrap narrow">
  <h2>{t['try_h2']}</h2>
  <p class="sub">{t['try_sub']}</p>
  <p style="margin-top:18px"><a class="btn btn-primary" href="{t['try_href']}">{t['try_btn']}</a></p>
</div></section>
<section class="section" id="listening"><div class="wrap">
  <h2>{t['quiet_h2']}</h2>
  <div class="values" style="margin-top:20px">{quiet}</div>
</div></section>
<section class="section" id="questions"><div class="wrap narrow">
  <h2>{t['faq_h2']}</h2>
  <div style="margin-top:12px">{faq}</div>
  <p class="muted" style="margin-top:20px">{t['faq_more']}</p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <h2>{t['more_h2']}</h2>
  <div class="routes" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr));display:grid;margin-top:20px">{more}</div>
</div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in t['faq']]}]
    if t['film']:
        ld.append({"@context": "https://schema.org", "@type": "VideoObject", "name": "Hey Fold at the counter",
                   "description": strip_tags(t['film_caption']), "thumbnailUrl": SITE + "/assets/video/fold-hey-fold-film-poster.jpg",
                   "contentUrl": SITE + "/assets/video/fold-hey-fold-film.mp4", "uploadDate": "2026-09-24", "duration": "PT8S"})
    slug = SLUG if t['lang'] == 'en' else 'es/' + SLUG
    html_ = page(slug, t['title'], t['desc'], t['og'], t['crumb'], body, ld)
    if t['lang'] == 'es':
        for a, b in (('<html lang="en">', '<html lang="es">'), (BAND, BAND_ES),
                     (f'"item": "{SITE}/"', f'"item": "{SITE}/es/"')):
            assert a in html_, a
            html_ = html_.replace(a, b, 1)

    md = [t['md_title'], '', t['md_canon'], '', md_text(t['lede']), '']
    md += [f'- **{md_text(b)}**: {md_text(s)}' for i, b, s in t['facts']] + ['']
    md += [f'## {md_text(t["how_h2"])}', '']
    md += [f'{n}. **{md_text(b)}** {md_text(s)}' for n, (b, s) in enumerate(t['steps'], 1)] + ['']
    md += [f'## {md_text(t["say_h2"])}', '', f'| {t["say_head"][0]} | {t["say_head"][1]} |', '| --- | --- |']
    md += [f'| {md_text(a)} | {md_text(b)} |' for a, b in t['say']] + ['', md_text(t['say_note']), '']
    md += [f'## {md_text(t["try_h2"])}', '', f'{md_text(t["try_sub"])} {SITE}{t["try_href"]}', '']
    md += [f'## {md_text(t["quiet_h2"])}', ''] + [f'- **{md_text(b)}**: {md_text(s)}' for i, b, s in t['quiet']] + ['']
    md += [f'## {md_text(t["faq_h2"])}', ''] + [f'**{md_text(q)}** {md_text(a)}\n' for q, a in t['faq']]
    md += [f'## {md_text(t["more_h2"])}', ''] + [f'- [{md_text(b)}]({SITE}{h}): {md_text(s)}' for h, i, b, s in t['more']]
    md = '\n'.join(md) + '\n' + (md_footer() if t['lang'] == 'en' else MD_FOOTER_ES)
    return html_, md


def hey_fold():
    """English page: (html, md) for slug 'hey-fold'."""
    return _build(EN)


def hey_fold_es():
    """Spanish page: (html, md) for es/hey-fold (a static file; see the module docstring)."""
    return _build(ES)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    targets = [('es/' + SLUG, hey_fold_es)] if '--es' in sys.argv else [(SLUG, hey_fold), ('es/' + SLUG, hey_fold_es)]
    for path, fn in targets:
        h, md = fn()
        open(os.path.join(root, path + '.html'), 'w', encoding='utf-8').write(h)
        open(os.path.join(root, path + '.md'), 'w', encoding='utf-8').write(md.rstrip() + '\n')
        print('wrote', path)
