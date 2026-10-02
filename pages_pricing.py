#!/usr/bin/env python3
"""The Pricing page of foldpos.com, in English and Spanish.

    from pages_pricing import pricing        # -> (html, md) for slug 'pricing'

build_site.py writes the English page. The Spanish page (es/pricing.html and .md) is a
static file like the rest of es/: run `python3 pages_pricing.py --es` after changing the
copy here, then build_site.py and check_seo.py.

Prices set on 2 Oct 2026: Starter $79, Growth $149, Pro $249 a month. The same three
numbers also appear on the home page, the shop pages, the FAQ, Pickup & delivery, Hey Fold,
llms.txt, llms-full.txt and fold-pos.md, in both languages; change them together.

What the page promises has to match what Settings › Plan & billing charges:
  * the plan prices come from the API (src/common/enums/plan.enum.ts) and Stripe;
  * add-ons are set up by Fold by hand (no self-serve add-on billing yet), which is why
    the page says "write to us";
  * nothing here about yearly billing, a shop's own texting number or Fold Pay: not
    available yet.
"""
import os
import sys

from build_site import page, md_footer, md_text, strip_tags, esc, ic, SITE, BAND
from pages_delivery import BAND_ES, MD_FOOTER_ES

SIGNUP = 'https://pos.foldpos.com/signup'
PRICES = {'S': 79, 'G': 149, 'P': 249}

STYLE = '''<style>
.px-old{margin-top:22px;border:1px solid var(--line);border-radius:14px;padding:14px 18px;background:var(--fog);color:var(--ink-2);font-size:14.5px;max-width:70ch}
.px-old b{color:var(--ink)}
.px-adds{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:8px}
.px-add{border:1px solid var(--line);border-radius:16px;padding:20px 22px;background:#fff;display:grid;grid-template-columns:1fr auto;column-gap:16px;row-gap:6px;align-items:baseline}
.px-add h3{font-size:17px;margin:0}
.px-add .p{font:700 17px/1.2 "Sora",sans-serif;white-space:nowrap;color:var(--ink)}
.px-add .p small{font:500 13px "Plus Jakarta Sans",sans-serif;color:var(--ink-3)}
.px-add p{grid-column:1 / -1;margin:0;color:var(--ink-2);font-size:14.5px}
.compare td.v{font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums;white-space:nowrap}
@media (max-width:760px){.px-adds{grid-template-columns:1fr}}
</style>'''

EN = {
    'lang': 'en', 'home': '/', 'pre': '',
    'title': 'Pricing — Fold POS',
    'desc': 'Fold POS pricing: Starter $79, Growth $149 and Pro $249 a month. Month to month, 14-day free trial, no card up front, your own card processor, Hey Fold and customer texts on every plan.',
    'og': 'Fold POS pricing', 'crumb': 'Pricing', 'kicker': 'Pricing',
    'h1': 'One price a month. No surprises.',
    'lede': 'Month to month, 14 days free, no card up front. Every plan has the whole counter, Hey Fold and your customer texts.',
    'per': '/ month', 'popular': 'Most popular', 'start': 'Start free', 'plans_h2': 'Plans',
    'plans': [
        ('S', 'Starter', 'One counter.', False, [
            'Check-in, orders board and payments', 'Customer accounts and history', 'Receipts, tags and printing',
            'Refunds, cash drawer and sales tax', 'Keeps taking orders offline', 'Daily reporting and the machine maintenance log',
            'Hey Fold', '500 customer texts a month']),
        ('G', 'Growth', 'Adding delivery and staff.', True, [
            'Everything in Starter', 'Pickup &amp; delivery routing', 'Online booking and weekly pickups', 'Staff shifts and clock-in',
            'Express and subscription pricing', 'Marketing and order reminders', 'Supply inventory and reorder suggestions',
            '1,500 customer texts a month']),
        ('P', 'Pro', 'More than one door.', False, [
            'Everything in Growth', 'Multi-location reporting', 'Plants &amp; drop stores', 'Route optimization',
            'Role-based staff permissions', 'Priority support', '3,000 customer texts a month']),
    ],
    'old': '<b>Already on Fold POS?</b> Your price stays what it is today.',
    'facts': [
        ('card', 'Your processor, your rates', 'Card, cash, check, store credit and split payments.'),
        ('mic', 'Hey Fold on every plan', 'Say the order. It’s typed, priced and printing.'),
        ('history', 'No contract', 'Month to month. Your data comes with you if you leave.'),
    ],
    'cmp_h2': 'Compare plans',
    'cmp_sub': 'Every plan has the whole counter. Growth adds delivery, booking and staff; Pro adds more locations and plants.',
    'cmp_head': 'What you get', 'inc': 'Included', 'notinc': 'Not included', 'addon': 'Add-on',
    'rows': [
        ('The counter', None),
        ('Check-in by the pound, the piece or the job', 'SGP'), ('Orders board, stations and shelf spots', 'SGP'),
        ('Payments on your own processor', 'SGP'), ('Refunds, cash drawer and end-of-day reports', 'SGP'),
        ('Sales tax and the sales tax report', 'SGP'), ('Keeps taking orders offline', 'SGP'),
        ('Customer accounts and history', 'SGP'),
        ('Receipts and 1 × 3 in tags on Epson, Star, Bixolon and Zebra', 'SGP'), ('Ready texts in English and Spanish', 'SGP'),
        ('Hey Fold, the counter that listens', 'SGP'), ('Daily reporting', 'SGP'), ('Machine maintenance log', 'SGP'),
        ('Customer texts included each month', ('500', '1,500', '3,000')),
        ('Growing the shop', None),
        ('Pickup &amp; delivery routing', 'GP'), ('Online booking and weekly pickups', 'GP'), ('Staff shifts and clock-in', 'GP'),
        ('Express and subscription pricing', 'GP'), ('Marketing and order reminders', 'GP'),
        ('Supply inventory and reorder suggestions', 'GP'),
        ('More than one door', None),
        ('Multi-location reporting', 'P'), ('Plants &amp; drop stores', ('+', '+', True)), ('Route optimization', 'P'),
        ('Role-based staff permissions', 'P'), ('Priority support', 'P'),
    ],
    'add_h2': 'Add-ons',
    'add_sub': 'Only if you need them. Write to <a href="mailto:contact@foldpos.com?subject=Fold%20POS%20add-on">contact@foldpos.com</a> and we add it to your plan.',
    'adds': [
        ('More texts', '$20', '/ month', 'Another 1,000 customer texts a month, on any plan. We tell you before you run out.'),
        ('Another location', '$59', '/ month', 'Each location after the first, on Pro. One login, one report across all of them.'),
        ('Plants &amp; drop stores', '$49', '/ month', 'On Starter or Growth, for each plant. Bags scanned at every hand-off and a monthly statement. Included in Pro.'),
        ('We move you', '$299', 'once', 'We bring your customers and price list over from Cents, CleanCloud or a spreadsheet and check them with you. Importing them yourself is free.'),
    ],
    'faq_h2': 'Pricing questions',
    'faq': [
        ('Is there a contract?', 'No. Every plan is month to month. Change plans or cancel any time from Settings.'),
        ('Do I need a card to start the trial?', 'No. The first 14 days are free and we don’t ask for a card.'),
        ('What happens when the trial ends?', 'You pick a plan in Settings › Plan &amp; billing. If you don’t, the POS goes read-only: everything you entered stays, and choosing a plan brings it right back.'),
        ('I’m already a customer. Does my price change?', 'No. If you’re on Fold POS today, your price stays what it is.'),
        ('What counts as a customer text?', 'Each text Fold sends for your shop: order ready, pickup and delivery updates, booking codes and reminders. Texts your customers send you don’t count.'),
        ('What if I need more texts?', 'Add 1,000 more a month for $20. Your customers’ texts don’t stop without warning; we write to you first.'),
        ('Can I use my own card processor?', 'Yes. Card, cash, check, store credit and split payments, on your processor at your rates.'),
        ('Is Hey Fold extra?', 'No. Hey Fold is built into every plan.'),
        ('What if we have more than five locations?', 'Email <a href="mailto:contact@foldpos.com?subject=More%20than%20five%20locations">contact@foldpos.com</a> and we’ll set it up with you.'),
    ],
    'faq_more': 'More in the <a href="/faq">FAQ</a>.',
    'md_title': '# Fold POS pricing',
    'md_canon': '> Canonical page: https://foldpos.com/pricing · Markdown mirror.',
    'md_intro': 'Month to month, 14-day free trial, no card up front. Change or cancel any time from Settings.',
    'md_start': 'Start a free trial', 'md_month': '/month', 'md_popular': ' (most popular)',
    'md_adds': '## Add-ons', 'md_faq': '## Everything else about the money',
}

ES = {
    'lang': 'es', 'home': '/es/', 'pre': '/es',
    'title': 'Precios — Fold POS',
    'desc': 'Precios de Fold POS para lavanderías y tintorerías: Starter $79, Growth $149 y Pro $249 al mes (USD). Mes a mes, 14 días gratis, sin tarjeta, con Hey Fold y mensajes al cliente en todos los planes.',
    'og': 'Precios de Fold POS', 'crumb': 'Precios', 'kicker': 'Precios',
    'h1': 'Un precio al mes. Sin sorpresas.',
    'lede': 'Mes a mes, 14 días gratis, sin tarjeta para empezar. Todos los planes traen el mostrador completo, Hey Fold y los mensajes a sus clientes. Precios en dólares estadounidenses (USD).',
    'per': '/ mes', 'popular': 'El más popular', 'start': 'Empiece gratis', 'plans_h2': 'Planes',
    'plans': [
        ('S', 'Starter', 'Un mostrador.', False, [
            'Recepción, tablero de pedidos y cobros', 'Cuentas de clientes e historial', 'Recibos, etiquetas e impresión',
            'Reembolsos, caja e impuesto sobre las ventas', 'Sigue tomando pedidos sin conexión', 'Informes diarios y registro de mantenimiento de máquinas',
            'Hey Fold', '500 mensajes a clientes al mes']),
        ('G', 'Growth', 'Para sumar entregas y personal.', True, [
            'Todo lo de Starter', 'Rutas de recogida y entrega', 'Reservas en línea y recogidas semanales', 'Turnos y registro de entrada del personal',
            'Precios exprés y por suscripción', 'Marketing y recordatorios de pedidos', 'Inventario de insumos y sugerencias de reabastecimiento',
            '1,500 mensajes a clientes al mes']),
        ('P', 'Pro', 'Más de una sucursal.', False, [
            'Todo lo de Growth', 'Informes de varias sucursales', 'Plantas y tiendas de recepción', 'Optimización de rutas',
            'Permisos del personal por rol', 'Soporte prioritario', '3,000 mensajes a clientes al mes']),
    ],
    'old': '<b>¿Ya usa Fold POS?</b> Su precio se queda como está hoy.',
    'facts': [
        ('card', 'Su procesador, sus tarifas', 'Tarjeta, efectivo, cheque, crédito de la tienda y pagos divididos.'),
        ('mic', 'Hey Fold en todos los planes', 'Diga el pedido. Queda escrito, con precio y ya se está imprimiendo.'),
        ('history', 'Sin contrato', 'Mes a mes. Sus datos se van con usted si se va.'),
    ],
    'cmp_h2': 'Compare los planes',
    'cmp_sub': 'Todos los planes incluyen el mostrador completo. Growth suma entregas, reservas y personal; Pro suma más sucursales y plantas.',
    'cmp_head': 'Qué incluye', 'inc': 'Incluido', 'notinc': 'No incluido', 'addon': 'Complemento',
    'rows': [
        ('El mostrador', None),
        ('Recepción por libra, por pieza o por trabajo', 'SGP'), ('Tablero de pedidos, estaciones y lugares en los estantes', 'SGP'),
        ('Cobros con su propio procesador', 'SGP'), ('Reembolsos, caja y reportes de cierre del día', 'SGP'),
        ('Impuesto sobre las ventas y su informe', 'SGP'), ('Sigue tomando pedidos sin conexión', 'SGP'),
        ('Cuentas de clientes e historial', 'SGP'),
        ('Recibos y etiquetas de 1 × 3 in en Epson, Star, Bixolon y Zebra', 'SGP'), ('Avisos de “listo” en español e inglés', 'SGP'),
        ('Hey Fold, el mostrador que escucha', 'SGP'), ('Informes diarios', 'SGP'), ('Registro de mantenimiento de máquinas', 'SGP'),
        ('Mensajes a clientes incluidos cada mes', ('500', '1,500', '3,000')),
        ('Para crecer', None),
        ('Rutas de recogida y entrega', 'GP'), ('Reservas en línea y recogidas semanales', 'GP'), ('Turnos y registro de entrada del personal', 'GP'),
        ('Precios exprés y por suscripción', 'GP'), ('Marketing y recordatorios de pedidos', 'GP'),
        ('Inventario de insumos y sugerencias de reabastecimiento', 'GP'),
        ('Más de una sucursal', None),
        ('Informes de varias sucursales', 'P'), ('Plantas y tiendas de recepción', ('+', '+', True)), ('Optimización de rutas', 'P'),
        ('Permisos del personal por rol', 'P'), ('Soporte prioritario', 'P'),
    ],
    'add_h2': 'Complementos',
    'add_sub': 'Solo si los necesita. Escriba a <a href="mailto:contact@foldpos.com?subject=Complemento%20de%20Fold%20POS">contact@foldpos.com</a> y lo agregamos a su plan.',
    'adds': [
        ('Más mensajes', '$20', '/ mes', 'Otros 1,000 mensajes a clientes al mes, en cualquier plan. Le avisamos antes de que se le acaben.'),
        ('Otra sucursal', '$59', '/ mes', 'Cada sucursal después de la primera, en Pro. Un solo usuario y un solo informe para todas.'),
        ('Plantas y tiendas de recepción', '$49', '/ mes', 'En Starter o Growth, por cada planta. Bolsas escaneadas en cada entrega y un estado de cuenta mensual. Incluido en Pro.'),
        ('Lo cambiamos nosotros', '$299', 'una vez', 'Traemos sus clientes y su lista de precios desde Cents, CleanCloud o una hoja de cálculo y los revisamos con usted. Importarlos usted mismo es gratis.'),
    ],
    'faq_h2': 'Preguntas sobre precios',
    'faq': [
        ('¿Hay contrato?', 'No. Todos los planes son mes a mes. Cambie de plan o cancele cuando quiera desde Ajustes.'),
        ('¿Necesito una tarjeta para empezar la prueba?', 'No. Los primeros 14 días son gratis y no le pedimos tarjeta.'),
        ('¿Qué pasa cuando termina la prueba?', 'Usted elige un plan en Ajustes › Plan y facturación. Si no lo hace, el POS queda en solo lectura: todo lo que ingresó se conserva y, al elegir un plan, vuelve de inmediato.'),
        ('Ya soy cliente. ¿Cambia mi precio?', 'No. Si hoy usa Fold POS, su precio se queda como está.'),
        ('¿Qué cuenta como un mensaje a clientes?', 'Cada mensaje de texto que Fold envía por su tienda: pedido listo, avisos de recogida y entrega, códigos de reserva y recordatorios. Los mensajes que sus clientes le envían no cuentan.'),
        ('¿Y si necesito más mensajes?', 'Agregue 1,000 más al mes por $20. Los mensajes a sus clientes no se detienen sin aviso; primero le escribimos.'),
        ('¿Puedo usar mi propio procesador de tarjetas?', 'Sí. Tarjeta, efectivo, cheque, crédito de la tienda y pagos divididos, con su procesador y a sus tarifas.'),
        ('¿Hey Fold se cobra aparte?', 'No. Hey Fold viene incluido en todos los planes.'),
        ('¿Y si tenemos más de cinco sucursales?', 'Escriba a <a href="mailto:contact@foldpos.com?subject=M%C3%A1s%20de%20cinco%20sucursales">contact@foldpos.com</a> y lo configuramos con usted.'),
    ],
    'faq_more': 'Más en las <a href="/es/faq">preguntas frecuentes</a>.',
    'md_title': '# Precios de Fold POS',
    'md_canon': '> Página canónica: https://foldpos.com/es/pricing · Versión en Markdown.',
    'md_intro': 'Mes a mes, 14 días de prueba gratis, sin tarjeta para empezar. Cambie de plan o cancele cuando quiera desde Ajustes. Precios en dólares estadounidenses (USD).',
    'md_start': 'Empiece una prueba gratis', 'md_month': '/mes', 'md_popular': ' (el más popular)',
    'md_adds': '## Complementos', 'md_faq': '## Todo lo demás sobre el dinero',
}


def _cell(t, has, k, i):
    yes = f'<td>{ic("check", "i y")}<span class="visually-hidden">{t["inc"]}</span></td>'
    no = f'<td><span class="n" aria-hidden="true">—</span><span class="visually-hidden">{t["notinc"]}</span></td>'
    if isinstance(has, tuple):
        v = has[i]
        if v is True:
            return yes
        if v == '+':
            return f'<td class="v"><a href="#addons">{t["addon"]}</a></td>'
        return f'<td class="v">{v}</td>'
    return yes if k in has else no


def _build(t):
    cards = ''
    for k, name, who, pop, feats in t['plans']:
        lis = ''.join(f'<li>{ic("check")}<span>{f}</span></li>' for f in feats)
        badge = f'<span class="badge">{t["popular"]}</span>' if pop else ''
        cards += (f'<div class="{"plan pop" if pop else "plan"}">{badge}<h3>{name}</h3><div class="for">{who}</div>'
                  f'<div class="price">${PRICES[k]}<small> {t["per"]}</small></div><ul>{lis}</ul>'
                  f'<a class="{"btn btn-primary" if pop else "btn btn-ghost"}" href="{SIGNUP}">{t["start"]}</a></div>')
    trs = ''
    for label, has in t['rows']:
        if has is None:
            trs += f'<tr><td class="group" colspan="4">{label}</td></tr>'
        else:
            trs += f'<tr><td>{label}</td>' + ''.join(_cell(t, has, k, i) for i, k in enumerate('SGP')) + '</tr>'
    heads = ''.join(f'<th scope="col">{name}<small>${PRICES[k]} {t["per"]}</small></th>' for k, name, _, _, _ in t['plans'])
    facts = ''.join(f'<div class="fact">{ic(i)}<div><b>{b}</b><span>{s}</span></div></div>' for i, b, s in t['facts'])
    adds = ''.join(f'<div class="px-add"><h3>{n}</h3><div class="p">{p}<small> {u}</small></div><p>{d}</p></div>' for n, p, u, d in t['adds'])
    faq = ''.join(f'<details class="qa"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in t['faq'])
    body = f'''{STYLE}
<section class="phead"><div class="wrap">
  <div class="crumbs"><a href="{t['home']}">Fold POS</a> › {esc(t['crumb'])}</div>
  <div class="kicker">{t['kicker']}</div>
  <h1>{t['h1']}</h1>
  <p class="lede">{t['lede']}</p>
</div></section>
<section class="section"><div class="wrap">
  <h2 class="visually-hidden">{t['plans_h2']}</h2>
  <div class="plans">{cards}</div>
  <p class="px-old">{t['old']}</p>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap">
  <div class="facts">{facts}</div>
</div></section>
<section class="section" id="compare"><div class="wrap">
  <h2>{t['cmp_h2']}</h2>
  <p class="sub">{t['cmp_sub']}</p>
  <div class="table-scroll"><table class="compare">
    <thead><tr><th scope="col">{t['cmp_head']}</th>{heads}</tr></thead>
    <tbody>{trs}</tbody>
  </table></div>
</div></section>
<section class="section" id="addons"><div class="wrap">
  <h2>{t['add_h2']}</h2>
  <p class="sub">{t['add_sub']}</p>
  <div class="px-adds">{adds}</div>
</div></section>
<section class="section" id="questions"><div class="wrap narrow">
  <h2>{t['faq_h2']}</h2>
  <div style="margin-top:12px">{faq}</div>
  <p class="muted" style="margin-top:20px">{t['faq_more']}</p>
</div></section>'''
    offers = {"@context": "https://schema.org", "@type": "Product", "name": "Fold POS",
              "description": strip_tags(t['desc']), "brand": {"@type": "Brand", "name": "Fold POS"},
              "offers": [{"@type": "Offer", "name": n, "price": f'{PRICES[k]}.00', "priceCurrency": "USD",
                          "url": SIGNUP, "description": strip_tags(w)} for k, n, w, _, _ in t['plans']]}
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in t['faq']]}
    slug = 'pricing' if t['lang'] == 'en' else 'es/pricing'
    html_ = page(slug, t['title'], t['desc'], t['og'], t['crumb'], body, [offers, ld])
    if t['lang'] == 'es':
        for a, b in (('<html lang="en">', '<html lang="es">'), (BAND, BAND_ES),
                     (f'"item": "{SITE}/"', f'"item": "{SITE}/es/"')):
            assert a in html_, a
            html_ = html_.replace(a, b, 1)

    md = [t['md_title'], '', t['md_canon'], '', t['md_intro'], '', f'{t["md_start"]}: {SIGNUP}', '']
    for k, name, who, pop, feats in t['plans']:
        md += [f'## {name} — ${PRICES[k]}{t["md_month"]}' + (t['md_popular'] if pop else ''), '', md_text(who), '']
        md += [f'- {md_text(f)}' for f in feats] + ['']
    md += [md_text(t['old']), '', t['md_adds'], '', md_text(t['add_sub']), '']
    md += [f'- **{md_text(n)}** — {p} {u}. {md_text(d)}' for n, p, u, d in t['adds']] + ['']
    md += [t['md_faq'], ''] + [f'- **{md_text(q)}** {md_text(a)}' for q, a in t['faq']]
    md = '\n'.join(md) + (md_footer() if t['lang'] == 'en' else MD_FOOTER_ES)
    return html_, md


def pricing():
    return _build(EN)


def pricing_es():
    return _build(ES)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    targets = [('es/pricing', pricing_es)] if '--es' in sys.argv else [('pricing', pricing), ('es/pricing', pricing_es)]
    for path, fn in targets:
        h, md = fn()
        open(os.path.join(root, path + '.html'), 'w', encoding='utf-8').write(h)
        open(os.path.join(root, path + '.md'), 'w', encoding='utf-8').write(md.rstrip() + '\n')
        print('wrote', path)
