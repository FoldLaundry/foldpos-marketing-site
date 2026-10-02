#!/usr/bin/env python3
"""The Pickup & delivery page of foldpos.com, in English and Spanish.

    from pages_delivery import pickup_delivery      # -> (html, md) for slug 'pickup-delivery'

build_site.py writes the English page like about() and printers(). The Spanish page,
es/pickup-delivery.html and .md, is a static file like the rest of es/: it was written from
pickup_delivery_es() below, so run `python3 pages_delivery.py --es` after changing the copy
here to rewrite it, then build_site.py (header, footer, hreflang) and check_seo.py.

Every claim comes from the site's own copy (index.html #delivery, fold-pos.md, features.md,
faq.md #delivery, help.md, llms-full.txt, pricing.md). The online booking section was
checked against the app and the API on 2 Oct 2026; it does not claim rescheduling, paying
online or customer accounts, because those are not built.
"""
import os
import sys

from build_site import page, md_footer, md_text, strip_tags, esc, ic, SITE, BAND

SLUG = 'pickup-delivery'
IMG = '/assets/img/new/{}.webp'
IMG_STYLE = ('width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:16px;'
             'background:#fff;box-shadow:0 30px 60px -44px rgba(14,23,48,.4)')
LABEL_STYLE = 'display:flex;gap:8px;align-items:center;font-weight:700;font-size:14px;color:var(--brand);margin-bottom:12px'

EN = {
    'lang': 'en', 'home': '/', 'pre': '',
    'title': 'Pickup & delivery — Fold POS',
    'desc': 'Run pickup & delivery from your Fold POS counter: today’s runs, routes on a map, the Fold Driver app, Uber Direct couriers, online booking and cost per stop.',
    'og': 'Pickup & delivery with Fold POS',
    'crumb': 'Pickup & delivery',
    'kicker': 'Pickup &amp; delivery',
    'h1': 'Your own delivery service, run from the counter.',
    'lede': 'Your drivers, partner marketplaces and on-demand couriers, in one schedule, in the same screen as your counter.',
    'facts': [
        ('car', 'On Growth and Pro', 'Pickup &amp; delivery routing from $59 a month. Route optimization on Pro.'),
        ('chat', 'Customers texted at each step', 'Picked up, ready and out for delivery, in your shop’s name.'),
        ('globe', 'English or Spanish', 'The texts your customers get work in both.'),
    ],
    'steps': [
        ('runs', 'flow', 'Today’s runs', 'Every pickup and drop-off, and who’s on it.',
         'Open Pickup &amp; delivery in the left menu and today’s runs are there: each pickup and drop-off, with the driver on it.',
         'A live stop list and status for every driver on the road.',
         'pd-activities', 'Fold POS Pickup & delivery, Activities tab: pickups and deliveries with the staff assigned to each, and today’s activities.'),
        ('routes', 'route', 'Routes on a map', 'Tick your drivers. Build the day’s routes.',
         'Pick the drivers, press Build, and every pickup and delivery is sequenced into a route with ETAs and a map. Drag a stop to reorder it.',
         'Route optimization is on the Pro plan.',
         'pd-routes', 'Fold POS Routes tab: drivers ticked at the top, one driver’s stops in order with ETAs, and the route drawn on a map.'),
        ('driver', 'ipad', 'The Fold Driver app', 'A stop list instead of sticky notes.',
         'Your drivers use the Fold Driver app on their phone: today’s stops, navigation, and a photo or signature at the door.',
         'Proof of delivery and order status are tied back to the same ticket.',
         'pd-driver', 'The Fold Driver app on three phones: today’s route, a stop with a Navigate button, and the delivered screen with a photo and a signature.'),
        ('courier', 'car', 'Uber Direct couriers', 'No driver free? Send it with Uber.',
         'Book an Uber Direct courier from the counter, on your store’s own Uber account. It’s the Courier tab in Pickup &amp; delivery.',
         'Your drivers and the couriers sit in the same schedule.',
         'pd-courier', 'Fold POS Courier tab: Uber Direct couriers on the road with the order and status of each, and a Send with Uber button for an order with no driver free.'),
    ],
    'booking': {
        'label': 'Online booking', 'h2': 'Customers book their own pickup.',
        'sub': 'Turn on Take bookings online and your shop has its own booking page. A customer types the address, picks a pickup window and how the order comes back, and confirms with a code texted to their phone. No account, no password, no card.',
        'items': [
            ('flow', 'You set the rules', 'Your service area by postal code, the pickup and delivery windows and how many stops each one takes, turnaround, the cutoff and how far ahead. It’s in Settings › Hours &amp; turnaround.'),
            ('car', 'It lands in your schedule', 'A booking shows in Pickup &amp; delivery as a stop marked Online, next to the runs you entered yourself.'),
            ('history', 'Weekly pickups', 'A customer can ask for the same pickup every week, and you can add one from the Weekly tab. Stop it any time.'),
            ('chat', 'One tap to book again', 'The confirmation text has a link to view or cancel the pickup. The thank-you text has a link to book the next one, already filled in.'),
            ('browser', 'A link, a button and a QR code', 'Share the link, put the button on your own website, and print the QR code on receipts, bags and door hangers.'),
            ('globe', 'English or Spanish', 'The booking page and its texts work in both.'),
        ],
        'note': 'Customers pay when you have their clothes. Online booking needs customer texts set up for your shop, because the code arrives by text.',
    },
    'loop_label': 'Texts and checkout',
    'loop_h2': 'The customer hears from you. The fee is on the order.',
    'loop': [
        ('chat', 'Status texts', 'Customers get automatic texts as their order is picked up, ready and out for delivery. In your shop’s name, in English or Spanish.'),
        ('card', 'Delivery fees at checkout', 'The delivery fee is charged at checkout, with cash, card or pay-on-delivery.'),
    ],
    'cost': ('costs', 'ledger', 'What it costs', 'Know whether delivery is paying for itself.',
             'Insights shows cost, margin and on-time, per stop and per driver.',
             'Cost per stop and margin per order, next to the day’s pickups and deliveries.',
             'pd-insights', 'Fold POS Insights tab: stops completed, on-time, cost and margin per order, stops per day, cost assumptions and a table by driver.'),
    'partners_label': 'Partner jobs',
    'partners_h2': 'Partner jobs land in the same schedule.',
    'partners': 'Turn on a delivery marketplace (Fold, Laundryheap or Rinse), give it the API key, and its jobs land in your schedule with status updates flowing back.',
    'plans_h2': 'Which plans have it',
    'plans_sub': 'Pickup &amp; delivery comes with Growth ($59 a month) and Pro ($79 a month). Route optimization is on Pro. Every plan is month to month, with 14 days free.',
    'plans_head': ('What you get', 'Starter', 'Growth', 'Pro', '/ month'),
    'plans_rows': [('Pickup &amp; delivery routing', 'GP'), ('Route optimization', 'P')],
    'inc': 'Included', 'notinc': 'Not included',
    'plans_link': 'See everything in each plan',
    'faq_h2': 'Delivery questions',
    'faq': [
        ('Can I run my own delivery service?', 'Yes. Today’s pickups and drop-offs with who’s on each, routes built on a map, and the Fold Driver app for your drivers: today’s stops, navigation, and a photo or signature at the door.'),
        ('What if no driver is free?', 'Send it with an Uber Direct courier, booked on your store’s own Uber account from the counter.'),
        ('Can customers book a pickup online?', 'Yes. Turn on Take bookings online in Settings › Hours &amp; turnaround and your shop has its own booking page, with a link, a button for your website and a QR code. Bookings land in your schedule marked Online.'),
        ('Which plan has delivery?', 'Growth and Pro. Route optimization is on Pro.'),
        ('Is it in Spanish?', 'Yes. The counter, Hey Fold and the texts your customers get all work in English and Spanish.'),
    ],
    'faq_more': 'More in the <a href="/faq#delivery">FAQ</a>.',
    'more_h2': 'Where to next',
    'more': [
        ('/help#delivery', 'check', 'Pickup &amp; delivery help', 'Where it is in the POS, routes, the driver app and the Courier tab.'),
        ('/faq#delivery', 'chat', 'Delivery FAQ', 'Your own drivers, Uber Direct and which plan has it.'),
        ('/pricing', 'card', 'Pricing', 'Starter $39, Growth $59, Pro $79. Month to month.'),
        ('/contact', 'mail', 'Talk to us', 'Questions about running delivery on Fold POS? Write to us.'),
    ],
    'md_title': '# Pickup & delivery with Fold POS',
    'md_canon': '> Canonical page: https://foldpos.com/pickup-delivery · Markdown mirror.',
    'md_plans': '## Which plans have it',
    'md_faq': '## Delivery questions',
    'md_more': '## Where to next',
}

ES = {
    'lang': 'es', 'home': '/es/', 'pre': '/es',
    'title': 'Recogida y entrega — Fold POS',
    'desc': 'Maneje la recogida y entrega desde el mostrador de Fold POS: recorridos del día, rutas en un mapa, la app Fold Driver, mensajeros de Uber Direct, reservas en línea y costos.',
    'og': 'Recogida y entrega con Fold POS',
    'crumb': 'Recogida y entrega',
    'kicker': 'Recogida y entrega',
    'h1': 'Su propio servicio a domicilio, desde el mostrador.',
    'lede': 'Sus repartidores, los marketplaces asociados y los mensajeros bajo demanda, en un solo calendario y en la misma pantalla que su mostrador.',
    'facts': [
        ('car', 'En Growth y Pro', 'Rutas de recogida y entrega desde $59 al mes. Optimización de rutas en Pro.'),
        ('chat', 'Clientes avisados en cada paso', 'Al recoger, cuando está listo y cuando sale a entrega, con el nombre de su tienda.'),
        ('globe', 'En español o en inglés', 'Los mensajes que reciben sus clientes funcionan en los dos idiomas.'),
    ],
    'steps': [
        ('runs', 'flow', 'Recorridos del día', 'Cada recogida y cada entrega, y quién va en cada una.',
         'Abra Recogida y entrega en el menú de la izquierda y ahí están los recorridos del día: cada recogida y cada entrega, con el repartidor asignado.',
         'Lista de paradas y estado en vivo de cada repartidor en ruta.',
         'pd-activities', 'Fold POS, Recogida y entrega, pestaña Actividades: recogidas y entregas con el personal asignado a cada una, y las actividades de hoy.'),
        ('routes', 'route', 'Rutas en un mapa', 'Marque a sus repartidores. Arme las rutas del día.',
         'Elija a los repartidores, pulse Crear rutas y cada recogida y entrega queda ordenada en una ruta con horas estimadas de llegada y un mapa. Arrastre una parada para cambiarla de lugar.',
         'La optimización de rutas está en el plan Pro.',
         'pd-routes', 'Pestaña Rutas de Fold POS: repartidores marcados arriba, las paradas de un repartidor en orden con horas estimadas y la ruta trazada en un mapa.'),
        ('driver', 'ipad', 'La app Fold Driver', 'Una lista de paradas en lugar de notas adhesivas.',
         'Sus repartidores usan la app Fold Driver en su teléfono: las paradas del día, navegación y una foto o firma en la puerta.',
         'El comprobante de entrega y el estado del pedido quedan ligados al mismo ticket.',
         'pd-driver', 'La app Fold Driver en tres teléfonos: la ruta del día, una parada con el botón para navegar y la pantalla de entregado con foto y firma.'),
        ('courier', 'car', 'Mensajeros de Uber Direct', '¿Ningún repartidor libre? Envíelo con Uber.',
         'Reserve un mensajero de Uber Direct desde el mostrador, con la propia cuenta de Uber de su tienda. Está en la pestaña Mensajería de Recogida y entrega.',
         'Sus repartidores y los mensajeros quedan en el mismo calendario.',
         'pd-courier', 'Pestaña Mensajería de Fold POS: mensajeros de Uber Direct en camino con el pedido y el estado de cada uno, y un botón para enviar con Uber un pedido sin repartidor libre.'),
    ],
    'booking': {
        'label': 'Reservas en línea', 'h2': 'Sus clientes reservan su propia recogida.',
        'sub': 'Active Aceptar reservas en línea y su tienda tiene su propia página de reservas. El cliente escribe la dirección, elige un horario de recogida y cómo regresa el pedido, y confirma con un código que le llega por mensaje de texto. Sin cuenta, sin contraseña, sin tarjeta.',
        'items': [
            ('flow', 'Usted pone las reglas', 'Su área de servicio por código postal, los horarios de recogida y entrega y cuántas paradas admite cada uno, el tiempo de entrega, la hora límite y con cuánta anticipación. Está en Configuración › Horario y tiempos de entrega.'),
            ('car', 'Llega a su calendario', 'La reserva aparece en Recogida y entrega como una parada marcada En línea, junto a los recorridos que usted mismo ingresó.'),
            ('history', 'Recogidas semanales', 'El cliente puede pedir la misma recogida cada semana, y usted puede agregar una desde la pestaña Semanales. Deténgala cuando quiera.'),
            ('chat', 'Un toque para volver a reservar', 'El mensaje de confirmación trae un enlace para ver o cancelar la recogida. El mensaje de agradecimiento trae un enlace para reservar la siguiente, con los datos ya puestos.'),
            ('browser', 'Un enlace, un botón y un código QR', 'Comparta el enlace, ponga el botón en su propio sitio web e imprima el código QR en recibos, bolsas y colgantes de puerta.'),
            ('globe', 'En español o en inglés', 'La página de reservas y sus mensajes funcionan en los dos idiomas.'),
        ],
        'note': 'El cliente paga cuando usted ya tiene su ropa. Las reservas en línea necesitan que los mensajes al cliente estén configurados para su tienda, porque el código llega por mensaje de texto.',
    },
    'loop_label': 'Mensajes y cobro',
    'loop_h2': 'El cliente sabe de usted. El cargo va en el pedido.',
    'loop': [
        ('chat', 'Mensajes de estado', 'Sus clientes reciben mensajes automáticos cuando su pedido se recoge, cuando está listo y cuando sale a entrega. Con el nombre de su tienda, en español o en inglés.'),
        ('card', 'Cargo de entrega al cobrar', 'El cargo de entrega se cobra al pagar, en efectivo, con tarjeta o contra entrega.'),
    ],
    'cost': ('costs', 'ledger', 'Lo que cuesta', 'Sepa si las entregas se pagan solas.',
             'Métricas muestra costo, margen y puntualidad, por parada y por repartidor.',
             'Costo por parada y margen por pedido, junto a las recogidas y entregas del día.',
             'pd-insights', 'Pestaña Métricas de Fold POS: paradas completadas, puntualidad, costo y margen por pedido, paradas por día, supuestos de costo y una tabla por repartidor.'),
    'partners_label': 'Pedidos de socios',
    'partners_h2': 'Los pedidos de socios llegan al mismo calendario.',
    'partners': 'Active un marketplace de entregas (Fold, Laundryheap o Rinse), entréguele la clave de API y sus trabajos llegan a su calendario, con actualizaciones de estado de ida y vuelta.',
    'plans_h2': 'Qué planes lo incluyen',
    'plans_sub': 'La recogida y entrega viene con Growth ($59 al mes) y Pro ($79 al mes), en dólares estadounidenses (USD). La optimización de rutas está en Pro. Todos los planes son mes a mes, con 14 días gratis.',
    'plans_head': ('Qué incluye', 'Starter', 'Growth', 'Pro', '/ mes'),
    'plans_rows': [('Rutas de recogida y entrega', 'GP'), ('Optimización de rutas', 'P')],
    'inc': 'Incluido', 'notinc': 'No incluido',
    'plans_link': 'Vea todo lo que incluye cada plan',
    'faq_h2': 'Preguntas sobre entregas',
    'faq': [
        ('¿Puedo tener mi propio servicio de entregas?', 'Sí. Las recogidas y entregas del día con quién va en cada una, rutas armadas en un mapa y la app Fold Driver para sus repartidores: las paradas del día, navegación y una foto o firma en la puerta.'),
        ('¿Y si no hay ningún repartidor libre?', 'Envíelo con un mensajero de Uber Direct, reservado desde el mostrador con la propia cuenta de Uber de su tienda.'),
        ('¿Mis clientes pueden reservar una recogida en línea?', 'Sí. Active Aceptar reservas en línea en Configuración › Horario y tiempos de entrega y su tienda tiene su propia página de reservas, con un enlace, un botón para su sitio web y un código QR. Las reservas llegan a su calendario marcadas En línea.'),
        ('¿Qué plan incluye entregas?', 'Growth y Pro. La optimización de rutas está en Pro.'),
        ('¿Está en español?', 'Sí. El mostrador, Hey Fold y los mensajes que reciben sus clientes funcionan en español e inglés.'),
    ],
    'faq_more': 'Más en las <a href="/es/faq#delivery">preguntas frecuentes</a>.',
    'more_h2': 'Siga por aquí',
    'more': [
        ('/es/help#delivery', 'check', 'Ayuda de recogida y entrega', 'Dónde está en el POS, las rutas, la app para repartidores y la pestaña Mensajería.'),
        ('/es/faq#delivery', 'chat', 'Preguntas sobre entregas', 'Sus propios repartidores, Uber Direct y qué plan lo incluye.'),
        ('/es/pricing', 'card', 'Precios', 'Starter $39, Growth $59, Pro $79. Mes a mes.'),
        ('/es/contact', 'mail', 'Hable con nosotros', '¿Preguntas sobre cómo manejar entregas con Fold POS? Escríbanos.'),
    ],
    'md_title': '# Recogida y entrega con Fold POS',
    'md_canon': '> Página canónica: https://foldpos.com/es/pickup-delivery · Versión en Markdown.',
    'md_plans': '## Qué planes lo incluyen',
    'md_faq': '## Preguntas sobre entregas',
    'md_more': '## Siga por aquí',
}

BAND_ES = '''<section class="band"><div class="wrap"><div class="in">
  <div><h2>Pruébelo en su propio mostrador.</h2><p>14 días gratis. Sin tarjeta, sin contrato, sin llamadas de ventas.</p></div>
  <div class="acts"><a class="btn btn-primary" href="https://pos.foldpos.com/signup">Empiece gratis</a>
  <a class="btn btn-ghost" href="/es/contact">Hable con nosotros</a></div>
</div></div></section>'''

MD_FOOTER_ES = ('\n## Más\n\n- [Inicio](/es/fold-pos.md) · [Precios](/es/pricing.md) · [Preguntas frecuentes](/es/faq.md) · [Ayuda](/es/help.md)'
                ' · [Contacto](/es/contact.md) · [Nosotros](/es/about.md)\n- [Impresoras](/es/printers.md) · [Configuración de la tienda](/setup.md)'
                ' · [Asistente de impresión](/es/download.md) · [Todas las funciones](/es/features.md) · [Desarrolladores e IA](/es/developers.md)'
                '\n- [Hey Fold](/es/hey-fold.md) · [Recogida y entrega](/es/pickup-delivery.md) · [El dinero en el mostrador](/es/counter-money.md)'
                ' · [Plantas y tiendas de recepción](/es/plants.md)\n')


def _label(icon, text):
    return f'<div style="{LABEL_STYLE}">{ic(icon)}<span>{text}</span></div>'


def _split(key, icon, label, h2, sub, note, img, alt):
    return (f'<section class="section" id="{key}"><div class="wrap"><div class="tagsplit">'
            f'<div>{_label(icon, label)}<h2>{h2}</h2><p class="sub" style="margin-bottom:12px">{sub}</p>'
            f'<p class="muted">{note}</p></div>'
            f'<div><img src="{IMG.format(img)}" alt="{esc(alt)}" width="1600" height="1000" loading="lazy" decoding="async" style="{IMG_STYLE}"></div>'
            '</div></div></section>')


def _build(t):
    facts = ''.join(f'<div class="fact">{ic(i)}<div><b>{b}</b><span>{s}</span></div></div>' for i, b, s in t['facts'])
    steps = '\n'.join(_split(*s) for s in t['steps'])
    bk = t['booking']
    booking = ''.join(f'<div class="fact">{ic(i)}<div><b>{b}</b><span>{s}</span></div></div>' for i, b, s in bk['items'])
    loop = ''.join(f'<div class="fact">{ic(i)}<div><b>{b}</b><span>{s}</span></div></div>' for i, b, s in t['loop'])
    h = t['plans_head']
    trs = ''
    for label, has in t['plans_rows']:
        cells = ''.join(f'<td>{ic("check", "i y")}<span class="visually-hidden">{t["inc"]}</span></td>' if k in has
                        else f'<td><span class="n" aria-hidden="true">—</span><span class="visually-hidden">{t["notinc"]}</span></td>' for k in 'SGP')
        trs += f'<tr><td>{label}</td>{cells}</tr>'
    faq = ''.join(f'<details class="qa"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in t['faq'])
    more = ''.join(f'<a class="route" href="{href}"><span class="ic">{ic(i)}</span><span><b>{b}</b><span>{s}</span></span></a>'
                   for href, i, b, s in t['more'])
    pre = t['pre']
    body = f'''<section class="phead"><div class="wrap">
  <div class="crumbs"><a href="{t['home']}">Fold POS</a> › {esc(t['crumb'])}</div>
  <div class="kicker">{t['kicker']}</div>
  <h1>{t['h1']}</h1>
  <p class="lede">{t['lede']}</p>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap">
  <h2 class="visually-hidden">{t['kicker']}</h2>
  <div class="facts">{facts}</div>
</div></section>
{steps}
<section class="section" id="booking"><div class="wrap">
  {_label('browser', bk['label'])}<h2>{bk['h2']}</h2>
  <p class="sub">{bk['sub']}</p>
  <div class="facts">{booking}</div>
  <p class="muted" style="margin-top:18px;font-size:14.5px;max-width:70ch">{bk['note']}</p>
</div></section>
<section class="section" id="texts"><div class="wrap">
  {_label('chat', t['loop_label'])}<h2>{t['loop_h2']}</h2>
  <div class="values" style="margin-top:20px">{loop}</div>
</div></section>
{_split(*t['cost'])}
<section class="section" id="partners"><div class="wrap narrow">
  {_label('stores', t['partners_label'])}<h2>{t['partners_h2']}</h2>
  <p class="sub" style="margin-bottom:0">{t['partners']}</p>
</div></section>
<section class="section" id="plans"><div class="wrap narrow">
  <h2>{t['plans_h2']}</h2>
  <p class="sub">{t['plans_sub']}</p>
  <div class="table-scroll"><table class="compare" style="min-width:0">
    <thead><tr><th scope="col">{h[0]}</th><th scope="col">{h[1]}<small>$39 {h[4]}</small></th><th scope="col">{h[2]}<small>$59 {h[4]}</small></th><th scope="col">{h[3]}<small>$79 {h[4]}</small></th></tr></thead>
    <tbody>{trs}</tbody>
  </table></div>
  <p style="margin-top:22px"><a class="btn btn-ghost" href="{pre}/pricing">{t['plans_link']}</a></p>
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
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in t['faq']]}
    slug = SLUG if t['lang'] == 'en' else 'es/' + SLUG
    html_ = page(slug, t['title'], t['desc'], t['og'], t['crumb'], body, [ld])
    if t['lang'] == 'es':
        for a, b in (('<html lang="en">', '<html lang="es">'), (BAND, BAND_ES),
                     (f'"item": "{SITE}/"', f'"item": "{SITE}/es/"')):
            assert a in html_, a
            html_ = html_.replace(a, b, 1)

    # markdown mirror
    md = [t['md_title'], '', t['md_canon'], '', md_text(t['lede']), '']
    md += [f'- **{md_text(b)}**: {md_text(s)}' for i, b, s in t['facts']] + ['']
    for key, icon, label, h2, sub, note, img, alt in t['steps']:
        md += [f'## {md_text(label)}: {md_text(h2)}', '', f'{md_text(sub)} {md_text(note)}', '']
    md += [f'## {md_text(bk["label"])}: {md_text(bk["h2"])}', '', md_text(bk['sub']), '']
    md += [f'- **{md_text(b)}**: {md_text(s)}' for i, b, s in bk['items']] + ['', md_text(bk['note']), '']
    md += [f'## {md_text(t["loop_label"])}: {md_text(t["loop_h2"])}', '']
    md += [f'- **{md_text(b)}**: {md_text(s)}' for i, b, s in t['loop']] + ['']
    key, icon, label, h2, sub, note, img, alt = t['cost']
    md += [f'## {md_text(label)}: {md_text(h2)}', '', f'{md_text(sub)} {md_text(note)}', '']
    md += [f'## {md_text(t["partners_label"])}: {md_text(t["partners_h2"])}', '', md_text(t['partners']), '']
    md += [t['md_plans'], '', md_text(t['plans_sub']), '']
    md += [f'- {md_text(label)}: ' + ', '.join(n for k, n in zip('SGP', h[1:4]) if k in has) for label, has in t['plans_rows']]
    md += ['', f'{md_text(t["plans_link"])}: {SITE}{pre}/pricing', '', t['md_faq'], '']
    md += [f'**{md_text(q)}** {md_text(a)}\n' for q, a in t['faq']]
    md += [t['md_more'], ''] + [f'- [{md_text(b)}]({SITE}{href}): {md_text(s)}' for href, i, b, s in t['more']]
    md = '\n'.join(md) + '\n' + (md_footer() if t['lang'] == 'en' else MD_FOOTER_ES)
    return html_, md


def pickup_delivery():
    """English page: (html, md) for slug 'pickup-delivery'."""
    return _build(EN)


def pickup_delivery_es():
    """Spanish page: (html, md) for es/pickup-delivery (a static file; see the module docstring)."""
    return _build(ES)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    targets = [('es/' + SLUG, pickup_delivery_es)] if '--es' in sys.argv else [(SLUG, pickup_delivery), ('es/' + SLUG, pickup_delivery_es)]
    for path, fn in targets:
        h, md = fn()
        open(os.path.join(root, path + '.html'), 'w', encoding='utf-8').write(h)
        open(os.path.join(root, path + '.md'), 'w', encoding='utf-8').write(md.rstrip() + '\n')
        print('wrote', path)
