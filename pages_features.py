#!/usr/bin/env python3
"""/features and /es/features, on the same page system as Pricing, Hey Fold, Pickup & delivery,
Money at the counter, Plants and Fold Time (pages.css: page head, quiet fact rows, a label, a
headline and points beside one real Fold POS screen).

    from pages_features import features, features_es    # -> html (the .md mirrors are static)

build_site.py writes the English page. The Spanish page is a static file like the rest of es/:
run `python3 pages_features.py --es` after changing the copy here, then build_site.py and check_seo.py.

The words are the ones the page had before (Oct 15 2026); only the design changed. The screens are
real Fold POS screens from assets/img/new (the same set the homepage uses).
"""
import os
import sys

from build_site import page, esc, ic, SITE, BAND
from pages_delivery import BAND_ES, IMG_STYLE, LABEL_STYLE

DATA = {'en': {'title': 'Fold POS features — counter, workflow board, machines, supplies, delivery',
        'desc': 'Counter POS, workflow board, machine management, floor plan, supplies, marketing, pickup & delivery, staff shifts, payments, and '
                'reporting for laundromats and dry cleaners.',
        'h1': 'Built for the counter, the machines, and the shelves',
        'lede': 'Fold POS is the operating system for a laundromat or dry cleaner — order intake and payments, a live workflow board, equipment and '
                'inventory management, marketing, and pickup &amp; delivery, all in one place.',
        'toc': [['#counter', 'Counter'],
                ['#workflow', 'Workflow board'],
                ['#tickets', 'Tickets'],
                ['#machines', 'Machines'],
                ['#floorplan', 'Floor plan'],
                ['#supplies', 'Supplies'],
                ['#marketing', 'Marketing'],
                ['#delivery', 'Pickup & delivery'],
                ['#shifts', 'Shifts'],
                ['#more', 'Payments & reporting']],
        'sections': [['counter',
                      'The counter',
                      'Ring up any service the way your shop actually prices it',
                      'Switch between wash &amp; fold, dry cleaning, and alterations without leaving the screen. Price by the pound with a minimum, by '
                      'the bag, or by the individual item — set an express rate and a discount once, and Fold POS applies them everywhere they '
                      "belong. Look up a returning customer or add a new one without losing the order you're building.",
                      ['Per-pound, per-bag, and per-item pricing in the same order',
                       'Express service and discounts applied automatically',
                       'Customer search and quick-add, mid-order',
                       'Cash, card, or pay-on-delivery, on every order',
                       'Custom items for one-off requests']],
                     ['workflow',
                      'The workflow board',
                      'Every order has a home, every stage has a count',
                      'Orders move left to right across the exact stages your shop uses — to-do, washing, drying, ironing, folding, completed — with '
                      'a live count on every column. Open a stage to assign a washer, dryer, or staff member, and watch the progress bar move as the '
                      'load runs.',
                      ['Six-stage board that matches how your shop actually runs',
                       'Assign a machine or staff member in one tap',
                       'Live progress bars tied to real load and shift time',
                       'Express orders flagged and easy to spot at a glance',
                       'Search and filter by order ID or customer']],
                     ['tickets',
                      'The ticket',
                      'Nothing about an order gets lost between hands',
                      "Every order carries its own record: an itemized breakdown of tasks and pricing, the customer's contact and intake details, "
                      'and a place for photos and notes. Flag a broken zipper or a stain before you clean it, so whoever hands the order back knows '
                      'exactly what happened to it — and what it cost.',
                      ['Itemized task and pricing breakdown per order',
                       'Photos and notes attached directly to the ticket',
                       'Full customer contact, intake time, and staff on file',
                       'Move an order to its next phase from the same screen',
                       'Edit or cancel an order without starting over']],
                     ['machines',
                      'Machine management',
                      "Know exactly what's going on with every machine you own",
                      'Every washer, dryer, and press has its own record — what was fixed, which parts were replaced, and who worked on it. Fold POS '
                      'tracks usage and flags a machine for service before it breaks down mid-load, and you can schedule a technician without '
                      'leaving the POS.',
                      ['Full repair history per machine — what was fixed, which parts, and who did the work',
                       'Schedule a technician directly from the POS',
                       'Preventive maintenance reminders based on real usage',
                       'Downtime tracking so you know what a repair actually cost you']],
                     ['floorplan',
                      'Your floor, mapped',
                      'A live map of every machine on your floor',
                      'Set up Fold POS once with your actual machine brands, sizes, and layout, and it becomes a live map of your floor — not a '
                      'generic equipment list. See how many turns each machine ran today, and when your own staff use a machine for a wash-and-fold '
                      'order, everyone at the counter can see whose order is running and how much time is left on the cycle.',
                      ['Floor plan built from your real machine brands and sizes',
                       'Turns per machine, per day — see which machines earn their keep',
                       'Live cycle countdowns, visible to every staff member',
                       'See whose order is running in which washer or dryer, at a glance']],
                     ['supplies',
                      'Supplies & inventory',
                      "Know what's running low before it runs out",
                      'Track the detergent, poly bags, hangers, and press pads that keep your operation running, right alongside the vending and '
                      'retail products self-serve customers buy off your shelves. Fold POS learns your average usage against current workload — not '
                      "a fixed reorder point — and tells you what to reorder, and how much, before you're caught short.",
                      ['Live vending and retail inventory for self-serve laundromats',
                       'Usage tracking for the operational supplies orders consume',
                       'AI-driven reorder suggestions and quantities, based on historical use and current workload',
                       "Low-stock alerts before you're down to your last bag — or your last vending box"]],
                     ['marketing',
                      'Marketing',
                      'Reach customers before they think to call you',
                      "Build an SMS or email campaign in minutes — a seasonal promo, a nudge to customers who haven't ordered in a while, or a "
                      "same-night alert when your delivery driver's already in their neighborhood. Fold POS segments your customer list "
                      "automatically, so the message only goes to the people it's actually relevant to.",
                      ['SMS and email campaigns from the customer list you already have',
                       'Templates for promos, reminders, and win-backs',
                       'Location-aware blasts — "we\'re picking up in your neighborhood tonight"',
                       'Delivery and reply tracking on every campaign']],
                     ['delivery',
                      'Pickup & delivery',
                      'End-to-end delivery, from the counter to the door',
                      'Build a route, assign a driver, and let Fold POS handle the rest — customers get automatic texts as their order is picked up, '
                      'cleaned, and on its way back, and your driver gets a stop list instead of a stack of sticky notes.',
                      ['Route building and driver assignment from the POS',
                       'Automatic customer texts for pickup, ready, and out-for-delivery',
                       'Live stop list and status for every driver on the road',
                       'Proof of delivery and order status tied back to the same ticket']],
                     ['shifts',
                      'Staff & shifts',
                      'A clean handoff, every time the shift changes',
                      'Staff clock in and out with a tap of their own phone on a Fold Time device, or on the same screen they ring up orders on. See '
                      'revenue, order volume, and service mix for the shift in progress, and leave a clear activity trail for whoever opens next — '
                      "so the morning shift isn't guessing what happened overnight.",
                      ['<a href="/fold-time">Fold Time</a>: staff tap their phone on the wall device to clock in, take breaks and clock out. No app. '
                       'On Growth and Pro, your first device free',
                       'Clock-in and clock-out tied to each staff member',
                       'Live revenue and order volume for the current shift',
                       'Service mix breakdown — wash &amp; fold, dry cleaning, alterations',
                       'Shift notes and activity history for a clean handoff']]],
        'more_h2': 'The rest of what keeps a shop running',
        'more': [['Payments built in', 'Take cash, card, or pay-on-delivery, on your own card processor at your rates.'],
                 ['Customer accounts', "Every customer's order history, contact info, and preferences saved and searchable right at the counter."],
                 ["Reporting that's actually readable",
                  'Revenue, order volume, and service mix by day, week, or location — no spreadsheet exports required.'],
                 ['Refunds, cash drawer and sales tax',
                  'Refunds that need an owner code, a drawer counted at close with X and Z reports, and sales tax you set once. <a '
                  'href="/counter-money">Money at the counter</a>.'],
                 ['Keeps going offline',
                  'When the internet drops, the counter keeps taking new orders and syncs them by itself. <a href="/counter-money#offline">What '
                  'works offline</a>.'],
                 ['Plants and drop stores',
                  'Bags scanned at every handoff, every piece counted in and out, and a monthly statement for each store. <a href="/plants">Plants '
                  '&amp; drop stores</a>.']]},
 'es': {'title': 'Funciones de Fold POS — mostrador, tablero de pedidos, máquinas, insumos, entregas',
        'desc': 'Punto de venta (POS) para el mostrador, tablero de flujo de trabajo, gestión de máquinas, plano del local, insumos, marketing, '
                'recogida y entrega, turnos del personal, pagos e informes para lavanderías y tintorerías.',
        'h1': 'Hecho para el mostrador, las máquinas y los estantes',
        'lede': 'Fold POS es el sistema operativo de una lavandería o tintorería: recepción de pedidos y pagos, un tablero de pedidos en vivo, '
                'gestión de equipos e inventario, marketing, y recogida y entrega, todo en un solo lugar.',
        'toc': [['#counter', 'Mostrador'],
                ['#workflow', 'Tablero de pedidos'],
                ['#tickets', 'Tickets'],
                ['#machines', 'Máquinas'],
                ['#floorplan', 'Plano del local'],
                ['#supplies', 'Insumos'],
                ['#marketing', 'Marketing'],
                ['#delivery', 'Recogida y entrega'],
                ['#shifts', 'Turnos'],
                ['#more', 'Pagos e informes']],
        'sections': [['counter',
                      'El mostrador',
                      'Cobre cualquier servicio tal como lo cobra su negocio',
                      'Pase de lavado y doblado a lavado en seco o arreglos sin salir de la pantalla. Cobre por libra con un mínimo, por bolsa o por '
                      'prenda; configure una tarifa exprés y un descuento una sola vez, y Fold POS los aplica en todos los lugares donde corresponde. '
                      'Busque a un cliente habitual o agregue uno nuevo sin perder el pedido que está armando.',
                      ['Precio por libra, por bolsa y por prenda en el mismo pedido',
                       'Servicio exprés y descuentos aplicados automáticamente',
                       'Búsqueda y alta rápida de clientes, en pleno pedido',
                       'Efectivo, tarjeta o pago contra entrega, en cada pedido',
                       'Artículos personalizados para pedidos especiales']],
                     ['workflow',
                      'El tablero de pedidos',
                      'Cada pedido tiene su lugar y cada etapa, su conteo',
                      'Los pedidos avanzan de izquierda a derecha por las mismas etapas que usa su negocio (por hacer, lavado, secado, planchado, '
                      'doblado y terminado), con un conteo en vivo en cada columna. Abra una etapa para asignar una lavadora, una secadora o a '
                      'alguien del personal, y vea avanzar la barra de progreso mientras corre la carga.',
                      ['Tablero de seis etapas que refleja cómo funciona de verdad su negocio',
                       'Asigne una máquina o a alguien del personal con un toque',
                       'Barras de progreso en vivo, ligadas a la carga real y al horario del turno',
                       'Pedidos exprés marcados y fáciles de ver de un vistazo',
                       'Busque y filtre por número de pedido o por cliente']],
                     ['tickets',
                      'El ticket',
                      'Nada de un pedido se pierde al pasar de mano en mano',
                      'Cada pedido lleva su propio registro: el detalle de tareas y precios, los datos de contacto del cliente y de la recepción, y '
                      'un espacio para fotos y notas. Marque un cierre roto o una mancha antes de limpiar la prenda, para que quien entregue el '
                      'pedido sepa exactamente qué pasó con él y cuánto costó.',
                      ['Detalle de tareas y precios en cada pedido',
                       'Fotos y notas adjuntas directamente al ticket',
                       'Contacto completo del cliente, hora de recepción y quién lo atendió, todo registrado',
                       'Pase un pedido a su siguiente etapa desde la misma pantalla',
                       'Edite o cancele un pedido sin empezar de cero']],
                     ['machines',
                      'Gestión de máquinas',
                      'Sepa exactamente qué pasa con cada una de sus máquinas',
                      'Cada lavadora, secadora y prensa tiene su propio historial: qué se reparó, qué piezas se cambiaron y quién hizo el trabajo. '
                      'Fold POS registra el uso y marca una máquina para servicio antes de que falle a media carga, y usted puede programar a un '
                      'técnico sin salir del POS.',
                      ['Historial completo de reparaciones por máquina: qué se reparó, qué piezas y quién hizo el trabajo',
                       'Programe a un técnico directamente desde el POS',
                       'Recordatorios de mantenimiento preventivo según el uso real',
                       'Registro del tiempo fuera de servicio, para saber cuánto le costó realmente una reparación']],
                     ['floorplan',
                      'Su local, en un mapa',
                      'Un mapa en vivo de todas las máquinas de su local',
                      'Configure Fold POS una sola vez con las marcas, capacidades y distribución reales de sus máquinas, y se convierte en un mapa '
                      'en vivo de su local, no en una lista genérica de equipos. Vea cuántos ciclos hizo hoy cada máquina y, cuando su personal usa '
                      'una máquina para un pedido de lavado y doblado, todos en el mostrador pueden ver de quién es el pedido que está corriendo y '
                      'cuánto le falta al ciclo.',
                      ['Plano del local armado con las marcas y capacidades reales de sus máquinas',
                       'Ciclos por máquina, por día: vea qué máquinas realmente rinden',
                       'Cuenta regresiva de cada ciclo en vivo, visible para todo el personal',
                       'Vea de un vistazo qué pedido está en cada lavadora o secadora']],
                     ['supplies',
                      'Insumos e inventario',
                      'Sepa qué se está acabando antes de que se acabe',
                      'Controle el detergente, las bolsas plásticas, los ganchos y las almohadillas de planchado que mantienen su operación en '
                      'marcha, junto con los productos de máquinas expendedoras y de venta que los clientes de autoservicio toman de sus estantes. '
                      'Fold POS aprende su consumo promedio frente a la carga de trabajo actual (no un punto de reorden fijo) y le dice qué volver a '
                      'pedir, y cuánto, antes de que le falte.',
                      ['Inventario en vivo de máquinas expendedoras y productos de venta para lavanderías de autoservicio',
                       'Registro del consumo de los insumos que usan los pedidos',
                       'Sugerencias de reorden y cantidades con IA, según el consumo histórico y la carga de trabajo actual',
                       'Alertas de existencias bajas antes de llegar a su última bolsa, o a su última caja de la máquina expendedora']],
                     ['marketing',
                      'Marketing',
                      'Llegue a sus clientes antes de que piensen en llamarlo',
                      'Arme una campaña por SMS o correo electrónico en minutos: una promoción de temporada, un recordatorio para clientes que hace '
                      'tiempo no hacen pedidos o un aviso esa misma noche cuando su repartidor ya está en su barrio. Fold POS segmenta su lista de '
                      'clientes automáticamente, para que el mensaje solo llegue a quienes de verdad les interesa.',
                      ['Campañas por SMS y correo electrónico con la lista de clientes que ya tiene',
                       'Plantillas para promociones, recordatorios y recuperación de clientes',
                       'Envíos masivos por ubicación: “esta noche recogemos en su barrio”',
                       'Seguimiento de entregas y respuestas en cada campaña']],
                     ['delivery',
                      'Recogida y entrega',
                      'Entregas de principio a fin, del mostrador a la puerta',
                      'Arme una ruta, asigne un repartidor y deje que Fold POS se encargue del resto: los clientes reciben mensajes automáticos '
                      'cuando su pedido se recoge, se limpia y va de regreso, y su repartidor recibe una lista de paradas en lugar de un montón de '
                      'notas adhesivas.',
                      ['Armado de rutas y asignación de repartidores desde el POS',
                       'Mensajes automáticos al cliente al recoger, cuando está listo y cuando sale a entrega',
                       'Lista de paradas y estado en vivo de cada repartidor en ruta',
                       'Comprobante de entrega y estado del pedido ligados al mismo ticket']],
                     ['shifts',
                      'Personal y turnos',
                      'Un relevo ordenado en cada cambio de turno',
                      'El personal marca entrada y salida tocando un dispositivo Fold Time con su propio teléfono, o en la misma pantalla donde '
                      'cobra los pedidos. Vea los ingresos, el volumen de pedidos y la mezcla de servicios del turno en curso, y deje un registro '
                      'claro de actividad para quien abra después, para que el turno de la mañana no tenga que adivinar qué pasó durante la noche.',
                      ['<a href="/es/fold-time">Fold Time</a>: el personal toca el dispositivo de pared con su teléfono para marcar entrada, '
                       'descansos y salida. Sin app. En Growth y Pro, el primer dispositivo gratis',
                       'Entrada y salida registradas para cada persona del equipo',
                       'Ingresos y volumen de pedidos en vivo del turno actual',
                       'Desglose por tipo de servicio: lavado y doblado, lavado en seco, arreglos',
                       'Notas del turno e historial de actividad para un relevo ordenado']]],
        'more_h2': 'Lo demás que mantiene un negocio en marcha',
        'more': [['Pagos integrados', 'Cobre en efectivo, con tarjeta o contra entrega, con su propio procesador de pagos y a sus tarifas.'],
                 ['Cuentas de clientes',
                  'El historial de pedidos, los datos de contacto y las preferencias de cada cliente, guardados y fáciles de buscar desde el '
                  'mostrador.'],
                 ['Informes que se entienden',
                  'Ingresos, volumen de pedidos y mezcla de servicios por día, semana o sucursal, sin exportar hojas de cálculo.'],
                 ['Reembolsos, caja e impuestos',
                  'Reembolsos que piden el código del propietario, una caja que se cuenta al cerrar con informes X y Z, y un impuesto que se '
                  'configura una sola vez. <a href="/es/counter-money">El dinero en el mostrador</a>.'],
                 ['Sigue sin conexión',
                  'Cuando se cae el internet, el mostrador sigue tomando pedidos nuevos y los sincroniza solo. <a '
                  'href="/es/counter-money#offline">Qué funciona sin conexión</a>.'],
                 ['Plantas y tiendas de recepción',
                  'Bolsas escaneadas en cada entrega, cada pieza contada al salir y al llegar, y un estado de cuenta mensual por tienda. <a '
                  'href="/es/plants">Plantas y tiendas de recepción</a>.']]}}

# section id -> (icon, screen or None, alt EN, alt ES)
ART = {
    'counter':   ('desktop', 'checkin-wf', 'Check in: wash and fold items priced by the pound, with the order summary on the right',
                  'Recepción: artículos de lavado y doblado con precio por libra y el resumen del pedido a la derecha'),
    'workflow':  ('layers', 'orders-wf', 'The orders board: To-do, Washing, Drying, Ironing, Folding and Completed, with a count on each column',
                  'El tablero de pedidos: por hacer, lavado, secado, planchado, doblado y terminado, con un conteo en cada columna'),
    'tickets':   ('tag', 'checkin-dc', 'A dry cleaning ticket: each piece priced on its own, with the order summary',
                  'Un ticket de tintorería: cada prenda con su precio y el resumen del pedido'),
    'machines':  ('wave', 'machines', 'Machine management: every washer, dryer and dry-clean machine with its type and when it was last serviced',
                  'Gestión de máquinas: cada lavadora, secadora y máquina de lavado en seco con su tipo y su último servicio'),
    'floorplan': ('store', 'floor', 'The floor map: washers and dryers laid out as they stand, each showing whether it is free',
                  'El plano del local: lavadoras y secadoras tal como están, cada una indicando si está libre'),
    'supplies':  ('box', 'supplies', 'Supply management: products running low, out of stock, and reorder suggestions with how much to buy',
                  'Gestión de insumos: productos por acabarse, agotados y sugerencias de reorden con cuánto comprar'),
    'marketing': ('mail', 'marketing', 'Marketing: automated campaigns with their type and results',
                  'Marketing: campañas automáticas con su tipo y sus resultados'),
    'delivery':  ('car', 'pd-routes', "Pickup and delivery routes: the day's stops in order beside a map of the route",
                  'Rutas de recogida y entrega: las paradas del día en orden junto al mapa de la ruta'),
    'shifts':    ('users', None, '', ''),
}
FT = '/assets/img/fold-time/'
SHIFTS_ART = {
    'en': (f'<div class="ff-pair"><img class="ff-dev" src="{FT}device-front-cut.webp" width="456" height="548" loading="lazy" decoding="async" alt="Fold Time wall device: Tap your phone">'
           f'<img class="ff-phone" src="{FT}staff-clocked-in.webp" width="520" height="885" loading="lazy" decoding="async" alt="Phone screen after a tap on Fold Time: Clocked in, 11:32 AM, with Undo"></div>'),
    'es': (f'<div class="ff-pair"><img class="ff-dev" src="{FT}device-front-cut.webp" width="456" height="548" loading="lazy" decoding="async" alt="Dispositivo de pared Fold Time: Toque con su teléfono">'
           f'<img class="ff-phone" src="{FT}staff-my-hours-es.webp" width="520" height="885" loading="lazy" decoding="async" alt="Mis horas en un teléfono: este periodo de pago, día por día"></div>'),
}
WORDS = {
    'en': dict(home='/', crumb='Features', start='Start free', pricing='See pricing', pricing_href='/pricing', jump='On this page'),
    'es': dict(home='/es/', crumb='Funciones', start='Empiece gratis', pricing='Ver precios', pricing_href='/es/pricing', jump='En esta página'),
}

STYLE = """<style>
.ff-sub{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:22px;font-size:14.5px}
.ff-sub a{color:var(--ink-2);text-decoration:none}
.ff-sub a:hover{color:var(--brand)}
.ff-acts{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap}
.ff-pts{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:10px;color:var(--ink-2);font-size:15px;max-width:60ch}
.ff-pts li{display:flex;gap:10px;align-items:flex-start}
.ff-pts svg{color:var(--brand);width:18px;height:18px;margin-top:3px;flex:none}
.ff-pts a{font-weight:600}
.ff-sec .tagsplit{align-items:center}
.ff-sec:nth-of-type(even) .tagsplit>div:first-child{order:2}
.ff-pair{display:flex;align-items:center;justify-content:center;gap:28px;padding:36px 24px;border-radius:18px;background:var(--fog)}
.ff-dev{width:44%;max-width:230px;height:auto;filter:drop-shadow(0 22px 26px rgba(20,27,61,.18))}
.ff-phone{width:42%;max-width:220px;height:auto;border-radius:18px;border:1px solid var(--line);background:#fff;box-shadow:0 26px 48px -28px rgba(20,27,61,.55)}
.values.three{grid-template-columns:repeat(3,1fr)}
.values .fact p{color:var(--ink-2);font-size:15px;line-height:1.55;margin-top:6px}
@media (max-width:900px){.ff-sec:nth-of-type(even) .tagsplit>div:first-child{order:0}.values.three{grid-template-columns:1fr}}
</style>"""


def _label(icon, text):
    return f'<div style="{LABEL_STYLE}">{ic(icon)}<span>{text}</span></div>'


def _build(lang):
    t, w = DATA[lang], WORDS[lang]
    secs = []
    for key, label, h2, body, pts in t['sections']:
        icon, img, alt_en, alt_es = ART[key]
        art = SHIFTS_ART[lang] if img is None else (
            f'<img src="/assets/img/new/{img}.webp" alt="{esc(alt_en if lang == "en" else alt_es)}" width="1600" height="1000" '
            f'loading="lazy" decoding="async" style="{IMG_STYLE}">')
        lis = ''.join(f'<li>{ic("check")}<span>{p}</span></li>' for p in pts)
        secs.append(f'<section class="section ff-sec" id="{key}"><div class="wrap"><div class="tagsplit">'
                    f'<div>{_label(icon, label)}<h2>{h2}</h2><p class="sub" style="margin-bottom:0">{body}</p><ul class="ff-pts">{lis}</ul></div>'
                    f'<div>{art}</div></div></div></section>')
    sub = ''.join(f'<a href="{h}">{esc(x)}</a>' for h, x in t['toc'])
    more = ''.join(f'<div class="fact"><b>{b}</b><p>{p}</p></div>' for b, p in t['more'])
    body = f"""{STYLE}
<section class="phead"><div class="wrap">
  <div class="crumbs"><a href="{w['home']}">Fold POS</a> › {w['crumb']}</div>
  <h1>{t['h1']}</h1>
  <p class="lede">{t['lede']}</p>
  <div class="ff-acts"><a class="btn btn-primary" href="https://pos.foldpos.com/signup">{w['start']}</a><a class="btn btn-ghost" href="{w['pricing_href']}">{w['pricing']}</a></div>
  <nav class="ff-sub" aria-label="{w['jump']}">{sub}</nav>
</div></section>
{chr(10).join(secs)}
<section class="section" id="more"><div class="wrap">
  <h2>{t['more_h2']}</h2>
  <div class="values three" style="margin-top:20px">{more}</div>
</div></section>"""
    items = [{"@type": "ListItem", "position": i + 1, "name": label, "description": h2.replace('&amp;', '&'), "url": f"{SITE}{'/es' if lang == 'es' else ''}/features#{key}"}
             for i, (key, label, h2, body_, pts) in enumerate(t['sections'])]
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Fold POS features" if lang == 'en' else "Funciones de Fold POS",
          "itemListOrder": "https://schema.org/ItemListOrderAscending", "numberOfItems": len(items), "itemListElement": items}
    slug = 'features' if lang == 'en' else 'es/features'
    html_ = page(slug, t['title'], t['desc'], t['title'].split(' — ')[0], w['crumb'], body, [ld])
    if lang == 'es':
        for a, b in (('<html lang="en">', '<html lang="es">'), (BAND, BAND_ES), (f'"item": "{SITE}/"', f'"item": "{SITE}/es/"')):
            assert a in html_, a
            html_ = html_.replace(a, b, 1)
    return html_


def features():
    return _build('en')


def features_es():
    return _build('es')


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    targets = [('es/features', features_es)]
    if '--es' not in sys.argv:
        targets = [('features', features)] + targets
    for path, fn in targets:
        open(os.path.join(root, path + '.html'), 'w', encoding='utf-8').write(fn())
        print('wrote', path)
