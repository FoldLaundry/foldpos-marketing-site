#!/usr/bin/env python3
"""Two pages of foldpos.com, each in English and Spanish:

    /counter-money   refunds, the cash drawer and end of day, sales tax, working offline
    /plants          plants and drop stores: bags, piece tracking, rates and statements

    from pages_more import counter_money, plants     # -> (html, md), English

build_site.py writes the English pages like about() and printers(). The Spanish pages
(es/counter-money, es/plants: .html and .md) are static files like the rest of es/: run
`python3 pages_more.py --es` after changing the copy here, then build_site.py and check_seo.py.

Every claim was checked against the app (fold_pos develop) and the API (master) on
2 Oct 2026. Deliberately NOT claimed, because it is not true today:
  counter-money: card refunds going back by themselves on a standalone terminal; a looked-up
      tax rate, tax filing, more than one rate; offline discounts, store credit, couriers,
      tags or texts; exporting the Z report.
  plants: drivers scanning bags, billing the drop store, texts on alerts, rack locations.
The drawings on these pages are examples drawn in HTML, not screenshots.

A new top-level page must also be in RESERVED_SLUGS in the API
(src/online-booking/online-booking.util.ts), or it would hide a shop's booking link.
"""
import os
import sys

from build_site import page, md_footer, md_text, strip_tags, esc, ic, SITE, BAND
from pages_delivery import BAND_ES, MD_FOOTER_ES, LABEL_STYLE

STYLE = '''<style>
.mx-pts{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:10px;color:var(--ink-2);font-size:15px;max-width:60ch}
.mx-pts li{display:flex;gap:10px;align-items:flex-start}
.mx-pts svg{color:var(--brand);width:18px;height:18px;margin-top:3px;flex:none}
.mx-note{margin-top:16px;font-size:14px;color:var(--ink-3);max-width:60ch}
.mx-art{display:grid;justify-items:center;gap:12px}
.mx-cap{font-size:12.5px;color:var(--ink-3);text-align:center}
.mx-rc{width:min(100%,340px);background:#fff;border:1px solid var(--line);border-radius:4px;box-shadow:0 22px 44px -30px rgba(14,23,48,.55);padding:18px 18px 16px;font:500 13px/1.55 ui-monospace,Menlo,Consolas,monospace;color:#0b0d12}
.mx-rc h3{font:700 13px/1.4 ui-monospace,Menlo,Consolas,monospace;text-align:center;letter-spacing:.06em;margin:0 0 2px}
.mx-rc .c{text-align:center;color:#3b404c}
.mx-rc hr{border:0;border-top:1px dashed #b9c0cc;margin:9px 0}
.mx-rc div.r{display:flex;justify-content:space-between;gap:12px}
.mx-rc div.r span:last-child{white-space:nowrap;font-variant-numeric:tabular-nums}
.mx-rc .b{font-weight:700}
.mx-bar{height:38px;margin-top:10px;background:repeating-linear-gradient(90deg,#0b0d12 0 2px,#fff 2px 4px,#0b0d12 4px 7px,#fff 7px 9px,#0b0d12 9px 10px,#fff 10px 13px)}
.mx-ui{width:min(100%,400px);border:1px solid var(--line);border-radius:14px;background:#fff;box-shadow:0 22px 44px -30px rgba(14,23,48,.55);overflow:hidden;font-size:14px}
.mx-ui .ban{background:var(--ink);color:#fff;font-weight:600;padding:11px 14px;display:flex;gap:10px;align-items:center}
.mx-ui .ban i{width:9px;height:9px;border-radius:50%;background:#fff;opacity:.7;flex:none}
.mx-ui .row{padding:12px 14px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:12px;color:var(--ink-2)}
.mx-ui .row b{color:var(--ink)}
.mx-ui .row .pill{font-size:12px;font-weight:700;color:var(--brand);background:var(--brand-soft);border-radius:999px;padding:2px 9px;white-space:nowrap;align-self:center}
.mx-st{list-style:none;margin:0;padding:6px 0;width:min(100%,400px);border:1px solid var(--line);border-radius:14px;background:#fff;box-shadow:0 22px 44px -30px rgba(14,23,48,.55)}
.mx-st li{position:relative;padding:11px 16px 11px 46px;color:var(--ink-3);font-size:14.5px}
.mx-st li::before{content:"";position:absolute;left:19px;top:16px;width:11px;height:11px;border-radius:50%;border:2px solid var(--line);background:#fff;z-index:1}
.mx-st li::after{content:"";position:absolute;left:25px;top:27px;bottom:-16px;width:2px;background:var(--line)}
.mx-st li:last-child::after{display:none}
.mx-st li.d{color:var(--ink-2)}
.mx-st li.d::before{background:var(--brand);border-color:var(--brand)}
.mx-st li.d::after{background:var(--brand)}
.mx-st li.on{color:var(--ink);font-weight:700}
.mx-st li.on::before{border-color:var(--brand);box-shadow:0 0 0 4px var(--brand-soft)}
.mx-st small{display:block;font-weight:500;color:var(--ink-3);font-size:12.5px}
.mx-tb{width:min(100%,420px);border:1px solid var(--line);border-radius:14px;background:#fff;box-shadow:0 22px 44px -30px rgba(14,23,48,.55);overflow:hidden}
.mx-tb table{width:100%;border-collapse:collapse;font-size:13.5px;font-variant-numeric:tabular-nums}
.mx-tb th,.mx-tb td{padding:9px 12px;text-align:right;border-bottom:1px solid var(--line)}
.mx-tb th:first-child,.mx-tb td:first-child{text-align:left}
.mx-tb thead th{font-size:11.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-3);background:var(--fog)}
.mx-tb tfoot td{font-weight:700;border-bottom:0}
.mx-tb caption{caption-side:top;text-align:left;font-weight:700;padding:12px 12px 10px}
</style>'''


def _rc(title, sub, rows, bar=False):
    """A receipt drawn in HTML. rows: (left, right) pairs, '-' for a rule, or (left, right, True) for bold."""
    out = f'<div class="mx-rc"><h3>{title}</h3><div class="c">{sub}</div><hr>'
    for r in rows:
        if r == '-':
            out += '<hr>'
        else:
            out += f'<div class="r{" b" if len(r) > 2 else ""}"><span>{r[0]}</span><span>{r[1]}</span></div>'
    return out + ('<div class="mx-bar"></div>' if bar else '') + '</div>'


def _art(label, inner, cap):
    return f'<div class="mx-art" role="img" aria-label="{esc(label)}">{inner}<div class="mx-cap">{cap}</div></div>'


# ════════════════════════════ /counter-money ════════════════════════════
MONEY_EN = {
    'slug': 'counter-money', 'lang': 'en', 'home': '/', 'pre': '',
    'title': 'Refunds, cash drawer, sales tax and offline — Fold POS',
    'desc': 'Money at the Fold POS counter: refunds that need an owner code, a counted cash drawer with X and Z reports, sales tax you set once, and new orders when the internet is down.',
    'og': 'Money at the counter with Fold POS',
    'crumb': 'Money at the counter',
    'kicker': 'Money at the counter',
    'h1': 'Every dollar at the counter, accounted for.',
    'lede': 'Refunds that need a code. A cash drawer that gets counted. Sales tax you set once. And a counter that keeps taking orders when the internet drops. On every plan.',
    'facts': [
        ('shield', 'A code on every refund', 'A refund needs an owner or admin code, and a reason.'),
        ('ledger', 'A drawer that’s counted', 'Open with a float, close with a count. Over or short is on the report.'),
        ('history', 'Keeps going offline', 'No internet? New orders are saved on the terminal and sync by themselves.'),
    ],
    'example': 'Example',
    'sections': [
        ('refunds', 'arrows', 'Refunds', 'The whole order, an amount, or one piece.',
         'Refund is on the order and on Check out. Fold asks for an owner or admin code first, and for a reason every time.',
         ['Refund everything, an amount, or by the piece. A piece gives back its share of the discount and the tax.',
          'It can’t go over what was paid on that tender, and a double tap can’t refund twice.',
          'The money goes back the way it came (cash, check or card) or to store credit on the customer’s account.',
          'A refund ticket prints, and the order shows who refunded and who approved it.'],
         'Card taken on your own terminal? Fold records the refund and you run it on the terminal.',
         lambda t: _art('Example refund ticket for one piece of an order', _rc('REFUND', 'Order D-1042 · Ortiz', [
             ('Blazer (1 of 3 pieces)', '$12.00'), ('Its share of the discount', '−$1.20'), ('Sales tax (8.75%)', '$0.95'), '-',
             ('Back in cash', '$11.75', True), '-', ('Refunded by', 'Ana'), ('Approved by', 'Owner code')]), t['example'])),
        ('drawer', 'ledger', 'Cash drawer and end of day', 'Open with a float. Close with a count.',
         'The drawer chip on Check out opens Cash drawer. Each shift starts with the cash in the till and ends with a count.',
         ['Starting cash typed in, or counted by bill, coin and roll.',
          'Paid in, paid out with a reason, safe drop and no sale, each under the clerk’s name.',
          'At close, Fold shows balanced, over or short. More than $5.00 off needs an owner or admin code.',
          'An X report any time in the shift. The Z report closes the day: sales, discounts, tax, refunds, each tender, each employee, and every drawer counted against what it should hold.',
          'The drawer opens after a cash sale. More than one register? Each terminal picks its own.'],
         'X and Z reports print on your receipt printer. The Z report is for staff with access to Reports.',
         lambda t: _art('Example end-of-day Z report', _rc('END OF DAY (Z)', 'Fri, Oct 2 · Register 1', [
             ('Orders', '42'), ('Gross sales', '$1,912.50'), ('Discounts', '−$64.00'), ('Net sales', '$1,848.50', True),
             ('Tax collected', '$87.80'), ('Refunds', '−$23.00'), '-',
             ('Starting cash', '$150.00'), ('Cash sales', '$535.30'), ('Cash refunds', '−$23.00'), ('Paid out', '−$20.00'),
             ('Should hold', '$642.30'), ('Counted', '$640.30'), ('Short by', '$2.00', True)]), t['example'])),
        ('tax', 'invoice', 'Sales tax', 'Set the rate once. It’s on every ticket.',
         'Settings › Payment › Sales tax. You set the rate and what it’s called on the receipt.',
         ['One rate for the store: a percentage to three decimals, or a fixed amount.',
          'Choose what’s taxable: services, the express fee, the delivery fee. Switch any single item on or off in the price list.',
          'Tax-exempt customers, with the reason and the certificate number on their account.',
          'A sales tax report by day: net sales, taxable, non-taxable, exempt and tax collected.',
          'Change the rate and past orders keep the tax they were charged.'],
         'You set the rate. Fold doesn’t look it up and doesn’t file for you.',
         lambda t: _art('Example ticket total with sales tax', _rc('TICKET', 'Order W-2087 · Chen', [
             ('Wash &amp; fold, 24 lb', '$36.00'), ('Comforter', '$12.00'), '-',
             ('Subtotal', '$48.00'), ('Sales tax (8.75%)', '$4.20'), ('Total', '$52.20', True)]), t['example'])),
        ('offline', 'history', 'Offline', 'The internet drops. The counter doesn’t.',
         'A banner tells the clerk the terminal is offline, and new orders keep going.',
         ['Orders are priced from the price list saved on the terminal, with your tax rules and express fee.',
          'Take cash, a check, a card on your own terminal, or pay on collection.',
          'The customer leaves with a ticket: a temporary number and a barcode that still finds the order later.',
          'When the connection is back the orders sync by themselves, oldest first, with no duplicates.'],
         'Garment tags and customer texts go out after the sync. Discounts, store credit, courier bookings, and checking out or refunding an existing order wait for the connection. A terminal has to have been online once to work offline.',
         lambda t: _art('Example of the offline banner at the counter',
                        '<div class="mx-ui"><div class="ban"><i></i>Offline — new orders are saved on this terminal</div>'
                        '<div class="row"><span><b>OFF-0007</b> · Ortiz · 3 pieces</span><span class="pill">Waiting to sync</span></div>'
                        '<div class="row"><span><b>OFF-0008</b> · Chen · 24 lb</span><span class="pill">Waiting to sync</span></div>'
                        '<div class="row"><span>Saved offline. It syncs when the connection is back.</span></div></div>', t['example'])),
    ],
    'faq_h2': 'Money questions',
    'faq': [
        ('Who can give a refund?', 'Anyone at the counter can start one, but it needs an owner or admin code and a reason before it goes through.'),
        ('Does a card refund go back to the card?', 'When the card was taken on your own card terminal, Fold records the refund and you run it on that terminal. Cash, check and store credit are handled in Fold.'),
        ('Does Fold work out my sales tax rate?', 'No. You set one rate for the store and choose what’s taxable. Fold charges it, shows it on the receipt and reports what was collected.'),
        ('What works when the internet is down?', 'Taking new orders and their payment in cash, by check, on your own card terminal or on collection. Tags and customer texts go out once the terminal is back online.'),
        ('Which plan has this?', 'Every plan: Starter, Growth and Pro.'),
    ],
    'faq_more': 'More in the <a href="/faq#payments">FAQ</a>.',
    'more_h2': 'Where to next',
    'more': [
        ('/pricing', 'card', 'Pricing', 'Starter $39, Growth $59, Pro $79. Month to month.'),
        ('/printers', 'printer', 'Printers', 'Receipts, tags and the reports that print on them.'),
        ('/features', 'layers', 'All features', 'The counter, the orders board, the floor and the back office.'),
        ('/contact', 'mail', 'Talk to us', 'Questions about your counter? Write to us.'),
    ],
    'md_title': '# Money at the counter with Fold POS',
    'md_canon': '> Canonical page: https://foldpos.com/counter-money · Markdown mirror.',
    'md_faq': '## Money questions', 'md_more': '## Where to next',
}

MONEY_ES = {
    'slug': 'counter-money', 'lang': 'es', 'home': '/es/', 'pre': '/es',
    'title': 'Reembolsos, caja, impuestos y sin conexión — Fold POS',
    'desc': 'El dinero en el mostrador de Fold POS: reembolsos con código del propietario, caja contada con reportes X y Z, impuesto sobre las ventas y pedidos nuevos sin internet.',
    'og': 'El dinero en el mostrador con Fold POS',
    'crumb': 'El dinero en el mostrador',
    'kicker': 'El dinero en el mostrador',
    'h1': 'Cada dólar del mostrador, bien contado.',
    'lede': 'Reembolsos que piden un código. Una caja que se cuenta. Un impuesto que se configura una sola vez. Y un mostrador que sigue tomando pedidos cuando se cae el internet. En todos los planes.',
    'facts': [
        ('shield', 'Un código en cada reembolso', 'Un reembolso necesita el código del propietario o de un administrador, y un motivo.'),
        ('ledger', 'Una caja que se cuenta', 'Se abre con un fondo y se cierra con un conteo. Lo que sobra o falta queda en el reporte.'),
        ('history', 'Sigue sin conexión', '¿Sin internet? Los pedidos nuevos se guardan en la terminal y se sincronizan solos.'),
    ],
    'example': 'Ejemplo',
    'sections': [
        ('refunds', 'arrows', 'Reembolsos', 'Todo el pedido, un importe o una sola pieza.',
         'Reembolsar está en el pedido y en la pantalla Entrega. Fold pide primero el código del propietario o de un administrador, y siempre un motivo.',
         ['Reembolse todo, un importe o por pieza. La pieza devuelve su parte del descuento y del impuesto.',
          'No puede pasar de lo que se pagó con esa forma de pago, y un doble toque no reembolsa dos veces.',
          'El dinero regresa como llegó (efectivo, cheque o tarjeta) o como crédito de tienda en la cuenta del cliente.',
          'Se imprime un comprobante, y el pedido muestra quién reembolsó y quién lo aprobó.'],
         '¿La tarjeta se cobró en su propia terminal? Fold registra el reembolso y usted lo pasa en la terminal.',
         lambda t: _art('Ejemplo de comprobante de reembolso de una pieza de un pedido', _rc('REEMBOLSO', 'Pedido D-1042 · Ortiz', [
             ('Saco (1 de 3 piezas)', '$12.00'), ('Su parte del descuento', '−$1.20'), ('Impuesto (8.75%)', '$0.95'), '-',
             ('Devuelto en efectivo', '$11.75', True), '-', ('Reembolsó', 'Ana'), ('Aprobó', 'Código del propietario')]), t['example'])),
        ('drawer', 'ledger', 'Caja y cierre del día', 'Se abre con un fondo. Se cierra con un conteo.',
         'El indicador de caja en la pantalla Entrega abre Caja. Cada turno empieza con el efectivo que hay y termina con un conteo.',
         ['El efectivo inicial se escribe o se cuenta por billete, moneda y rollo.',
          'Entrada de efectivo, salida de efectivo con su motivo, depósito a caja fuerte y sin venta, cada uno con el nombre del empleado.',
          'Al cerrar, Fold muestra si cuadra, sobra o falta. Más de $5.00 de diferencia necesita el código del propietario o de un administrador.',
          'Un Reporte X en cualquier momento del turno. El reporte Z cierra el día: ventas, descuentos, impuesto, reembolsos, cada forma de pago, cada empleado y cada caja contada contra lo que debía tener.',
          'La caja se abre después de una venta en efectivo. ¿Más de una caja registradora? Cada terminal elige la suya.'],
         'Los reportes X y Z se imprimen en su impresora de recibos. El reporte Z es para el personal con acceso a Informes.',
         lambda t: _art('Ejemplo de reporte Z de cierre del día', _rc('CIERRE DEL DÍA (Z)', 'Vie, 2 oct · Caja 1', [
             ('Pedidos', '42'), ('Ventas brutas', '$1,912.50'), ('Descuentos', '−$64.00'), ('Ventas netas', '$1,848.50', True),
             ('Impuesto cobrado', '$87.80'), ('Reembolsos', '−$23.00'), '-',
             ('Efectivo inicial', '$150.00'), ('Ventas en efectivo', '$535.30'), ('Reembolsos en efectivo', '−$23.00'), ('Salida de efectivo', '−$20.00'),
             ('Debía tener', '$642.30'), ('Contado', '$640.30'), ('Falta', '$2.00', True)]), t['example'])),
        ('tax', 'invoice', 'Impuesto sobre las ventas', 'Configure la tasa una vez. Va en cada ticket.',
         'Configuración › Pago › Impuesto sobre las ventas. Usted pone la tasa y el nombre que lleva en el recibo.',
         ['Una tasa para la tienda: un porcentaje de hasta tres decimales, o un importe fijo.',
          'Elija qué lleva impuesto: los servicios, el cargo exprés, el cargo de entrega. Active o desactive cualquier artículo en la lista de precios.',
          'Clientes exentos de impuestos, con el motivo y el número de certificado en su cuenta.',
          'Un informe de impuesto por día: ventas netas, gravado, no gravado, exento e impuesto cobrado.',
          'Si cambia la tasa, los pedidos anteriores conservan el impuesto que se les cobró.'],
         'La tasa la pone usted. Fold no la busca ni presenta declaraciones por usted.',
         lambda t: _art('Ejemplo del total de un ticket con impuesto', _rc('TICKET', 'Pedido W-2087 · Chen', [
             ('Lavado y doblado, 24 lb', '$36.00'), ('Edredón', '$12.00'), '-',
             ('Subtotal', '$48.00'), ('Impuesto (8.75%)', '$4.20'), ('Total', '$52.20', True)]), t['example'])),
        ('offline', 'history', 'Sin conexión', 'Se cae el internet. El mostrador no.',
         'Un aviso le dice al empleado que la terminal está sin conexión, y los pedidos nuevos siguen.',
         ['Los pedidos se cobran con la lista de precios guardada en la terminal, con sus reglas de impuesto y el cargo exprés.',
          'Cobre en efectivo, con cheque, con tarjeta en su propia terminal o al recoger.',
          'El cliente se va con su ticket: un número temporal y un código de barras que después sigue encontrando el pedido.',
          'Cuando vuelve la conexión, los pedidos se sincronizan solos, del más antiguo al más nuevo y sin duplicados.'],
         'Las etiquetas de prendas y los mensajes al cliente salen después de sincronizar. Los descuentos, el crédito de tienda, los mensajeros, y entregar o reembolsar un pedido que ya existía esperan a que vuelva la conexión. La terminal debe haber estado en línea una vez para trabajar sin conexión.',
         lambda t: _art('Ejemplo del aviso de sin conexión en el mostrador',
                        '<div class="mx-ui"><div class="ban"><i></i>Sin conexión: los pedidos nuevos se guardan en esta terminal</div>'
                        '<div class="row"><span><b>OFF-0007</b> · Ortiz · 3 piezas</span><span class="pill">Por sincronizar</span></div>'
                        '<div class="row"><span><b>OFF-0008</b> · Chen · 24 lb</span><span class="pill">Por sincronizar</span></div>'
                        '<div class="row"><span>Guardado sin conexión. Se sincroniza cuando vuelva la conexión.</span></div></div>', t['example'])),
    ],
    'faq_h2': 'Preguntas sobre el dinero',
    'faq': [
        ('¿Quién puede hacer un reembolso?', 'Cualquiera en el mostrador puede iniciarlo, pero necesita el código del propietario o de un administrador y un motivo antes de completarse.'),
        ('¿El reembolso de una tarjeta regresa a la tarjeta?', 'Cuando la tarjeta se cobró en su propia terminal de tarjetas, Fold registra el reembolso y usted lo pasa en esa terminal. El efectivo, el cheque y el crédito de tienda se manejan en Fold.'),
        ('¿Fold calcula mi tasa de impuesto?', 'No. Usted pone una tasa para la tienda y elige qué lleva impuesto. Fold lo cobra, lo muestra en el recibo e informa lo que se cobró.'),
        ('¿Qué funciona cuando no hay internet?', 'Tomar pedidos nuevos y cobrarlos en efectivo, con cheque, en su propia terminal de tarjetas o al recoger. Las etiquetas y los mensajes al cliente salen cuando la terminal vuelve a estar en línea.'),
        ('¿Qué plan lo incluye?', 'Todos: Starter, Growth y Pro.'),
    ],
    'faq_more': 'Más en las <a href="/es/faq#payments">preguntas frecuentes</a>.',
    'more_h2': 'Siga por aquí',
    'more': [
        ('/es/pricing', 'card', 'Precios', 'Starter $39, Growth $59, Pro $79. Mes a mes.'),
        ('/es/printers', 'printer', 'Impresoras', 'Recibos, etiquetas y los reportes que se imprimen en ellas.'),
        ('/es/features', 'layers', 'Todas las funciones', 'El mostrador, el tablero de pedidos, el local y la administración.'),
        ('/es/contact', 'mail', 'Hable con nosotros', '¿Preguntas sobre su mostrador? Escríbanos.'),
    ],
    'md_title': '# El dinero en el mostrador con Fold POS',
    'md_canon': '> Página canónica: https://foldpos.com/es/counter-money · Versión en Markdown.',
    'md_faq': '## Preguntas sobre el dinero', 'md_more': '## Siga por aquí',
}


# ════════════════════════════ /plants ════════════════════════════
def _stages(names, at, bag):
    lis = ''
    for i, n in enumerate(names):
        cls = 'd' if i < at else 'on' if i == at else ''
        lis += f'<li class="{cls}">{n}{f"<small>{bag}</small>" if i == at else ""}</li>'
    return f'<ol class="mx-st">{lis}</ol>'


def _stmt(cap, head, rows, foot):
    th = ''.join(f'<th scope="col">{h}</th>' for h in head)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    tf = ''.join(f'<td>{c}</td>' for c in foot)
    return (f'<div class="mx-tb"><table><caption>{cap}</caption><thead><tr>{th}</tr></thead>'
            f'<tbody>{trs}</tbody><tfoot><tr>{tf}</tr></tfoot></table></div>')


PLANTS_EN = {
    'slug': 'plants', 'lang': 'en', 'home': '/', 'pre': '',
    'title': 'Plants and drop stores — Fold POS piece tracking',
    'desc': 'Fold POS for dry cleaning plants and drop stores: link the shops, scan bags at every hand-off, count each piece in and out, find a piece, and bill from a monthly statement.',
    'og': 'Plants and drop stores on Fold POS',
    'crumb': 'Plants & drop stores',
    'kicker': 'Plants &amp; drop stores',
    'h1': 'Every piece, from the drop store to the plant and back.',
    'lede': 'Link your drop stores to the plant that cleans for them. Bags are scanned at each hand-off, every piece is counted in and out, and a short bag raises an alert before the customer does.',
    'facts': [
        ('stores', 'Linked in Settings', 'Shops you own link in one step. A partner shop joins with a one-time code.'),
        ('scan', 'Scanned at every hand-off', 'Bag sealed, bag received, each piece unpacked, each order assembled.'),
        ('invoice', 'A statement every month', 'What the plant cleaned for each store, priced at the rates you set.'),
    ],
    'example': 'Example',
    'sections': [
        ('link', 'stores', 'Link the shops', 'One plant. As many drop stores as you have.',
         'Settings › Plant &amp; drop stores. Only the owner sees it.',
         ['Shops in your own group link in one step.',
          'A partner shop joins with a code: the plant creates a one-time code and the drop store types it in.',
          'A partner plant sees the customer’s first name only. Never the phone, email or address.',
          'End a link whenever you need to. The history and the statements stay readable.'],
         'Plant &amp; bags appears in the left menu once a link exists.', None),
        ('bags', 'box', 'Bags', 'Scan the orders in. Print the label. Seal the bag.',
         'On the Send tab, staff scan orders into a bag, print its label and seal it, with a seal number if you use them.',
         ['The label says where the bag is from and where it’s going, its code, and every order inside with its piece count.',
          'At the other end, Receive: scan the bag, then scan each piece out of it.',
          'Finish, and Fold says how many pieces arrived out of how many were sent.',
          'The same steps bring the clean orders back to the store.'],
         'Bag labels print on your receipt printer. A scan box also takes a typed code.',
         lambda t: _art('Example bag label', _rc('BAG B-0419', 'Main St Cleaners → Central Plant', [
             ('D-1042 · Ortiz', '3 pcs'), ('D-1043 · Chen', '5 pcs'), ('D-1047 · Rivera', '4 pcs'), '-',
             ('3 orders', '12 pieces', True), ('Seal', '004871')], bar=True) +
             '<div class="mx-cap" style="font-weight:600;color:var(--ink-2)">Scan at every hand-off</div>', t['example'])),
        ('track', 'route', 'Where is it?', 'Five stages. One look.',
         'The Board tab shows every order between the store and the plant, and the stage it’s in.',
         ['Find a piece by its tag, the garment’s label, the order number or the bag code.',
          'Each order keeps a timeline of every scan: who, where and when.',
          'At assembly, scan each piece. The order turns Ready when the last one is in, and Fold names the ones still missing.',
          'Your customer’s order page says “At our cleaning plant”. It never names the plant.'],
         None,
         lambda t: _art('Example of an order’s stage between the store and the plant', _stages(
             ['Waiting for pickup', 'On the way to the plant', 'At the plant', 'On the way back', 'Back at the store'], 2,
             'Bag B-0419 · 12 of 12 pieces received'), t['example'])),
        ('alerts', 'bell', 'Alerts', 'A short bag gets noticed the same day.',
         'The Alerts tab holds anything that needs a person.',
         ['<b>Count mismatch:</b> a bag closed with fewer pieces than were sent. Someone has to resolve it, with a note.',
          '<b>Overdue:</b> a bag on the road too long. Twelve hours unless you set another limit.',
          '<b>Not assembled</b> and <b>Unknown scan</b>, so nothing waits unnoticed.'],
         'Alerts show in Fold POS. They don’t send a text or an email.',
         lambda t: _art('Example of a count mismatch alert',
                        '<div class="mx-ui"><div class="ban"><i></i>Count mismatch</div>'
                        '<div class="row"><span><b>Bag B-0419</b> · Central Plant</span><span class="pill">11 of 12 pieces</span></div>'
                        '<div class="row"><span>Missing: <b>D-1042 · Blazer</b> (1 of 3)</span></div>'
                        '<div class="row"><span>Needs a note to resolve</span></div></div>', t['example'])),
        ('rates', 'invoice', 'Rates and statements', 'What the plant charges each store, on one page a month.',
         'Set rates for each link: by the piece, by the pound or by the order.',
         ['A statement for each calendar month: every order, the day the plant received it, pieces, pounds and the amount.',
          'Anything without a rate is listed apart as Not priced, so nothing is billed by accident.',
          'Missing pieces are counted on the statement.',
          'Export it as a CSV.'],
         'The statement is the record you bill from. Fold doesn’t charge the drop store for you.',
         lambda t: _art('Example monthly statement from a plant to a drop store', _stmt(
             'Main St Cleaners · September', ['Order', 'Pieces', 'Amount'],
             [('D-1042', '3', '$9.75'), ('D-1043', '5', '$16.25'), ('D-1047', '4', '$13.00')], ('Total', '12', '$39.00')), t['example'])),
    ],
    'need_h2': 'What you need',
    'need': 'A barcode scanner, a receipt printer for bag labels, and a tag printer that prints barcodes if you want every piece scanned by its tag. Turn on Barcode on garment tags in Settings. <a href="/hardware#plant">See the hardware list</a>, or <a href="/follow-the-bag">follow one bag through the whole trip</a>.',
    'faq_h2': 'Plant questions',
    'faq': [
        ('Do the plant and the drop stores have to belong to the same owner?', 'No. Shops in your own group link in one step, and a partner shop joins with a one-time code from the plant.'),
        ('What does a partner plant see about my customers?', 'The customer’s first name. Not the phone number, the email or the address.'),
        ('What happens when a piece is missing?', 'The bag closes short and Fold raises a Count mismatch alert. It stays open until someone resolves it with a note, and the piece shows as missing on the statement.'),
        ('Does Fold bill the drop store?', 'No. Fold gives you the monthly statement, priced at your rates, and a CSV. Billing is yours.'),
        ('Do I need special hardware?', 'A scanner and a receipt printer. For barcodes on every garment tag, a thermal or label tag printer. The <a href="/hardware#plant">hardware list</a> has what we recommend.'),
    ],
    'faq_more': 'More in the <a href="/faq">FAQ</a>.',
    'more_h2': 'Where to next',
    'more': [
        ('/follow-the-bag', 'route', 'Follow the bag', 'One bag of dry cleaning, from the drop store to the plant and back.'),
        ('/dry-cleaners', 'tag', 'For dry cleaners', 'Per-piece tickets, garment tags and conveyor slots.'),
        ('/hardware', 'printer', 'Hardware', 'Printers, scanners and supplies for each kind of shop.'),
        ('/contact', 'mail', 'Talk to us', 'Running a plant or a group of drop stores? Write to us.'),
    ],
    'md_title': '# Plants and drop stores on Fold POS',
    'md_canon': '> Canonical page: https://foldpos.com/plants · Markdown mirror.',
    'md_faq': '## Plant questions', 'md_more': '## Where to next',
}

PLANTS_ES = {
    'slug': 'plants', 'lang': 'es', 'home': '/es/', 'pre': '/es',
    'title': 'Plantas y tiendas de recepción — Fold POS',
    'desc': 'Fold POS para plantas de tintorería y tiendas de recepción: vincule las tiendas, escanee las bolsas en cada entrega, cuente cada pieza y cobre con un estado de cuenta mensual.',
    'og': 'Plantas y tiendas de recepción con Fold POS',
    'crumb': 'Plantas y tiendas de recepción',
    'kicker': 'Plantas y tiendas de recepción',
    'h1': 'Cada pieza, de la tienda de recepción a la planta y de vuelta.',
    'lede': 'Vincule sus tiendas de recepción con la planta que les limpia. Las bolsas se escanean en cada entrega, cada pieza se cuenta al salir y al llegar, y una bolsa incompleta genera una alerta antes de que el cliente reclame.',
    'facts': [
        ('stores', 'Se vincula en Configuración', 'Sus propias tiendas se vinculan en un paso. Una tienda asociada entra con un código de un solo uso.'),
        ('scan', 'Escaneo en cada entrega', 'Bolsa sellada, bolsa recibida, cada pieza desempacada, cada pedido ensamblado.'),
        ('invoice', 'Un estado de cuenta cada mes', 'Lo que la planta limpió para cada tienda, con las tarifas que usted define.'),
    ],
    'example': 'Ejemplo',
    'sections': [
        ('link', 'stores', 'Vincule las tiendas', 'Una planta. Todas las tiendas de recepción que tenga.',
         'Configuración › Planta y tiendas de recepción. Solo lo ve el propietario.',
         ['Las tiendas de su propio grupo se vinculan en un paso.',
          'Una tienda asociada entra con un código: la planta crea un código de un solo uso y la tienda de recepción lo escribe.',
          'Una planta asociada solo ve el nombre de pila del cliente. Nunca el teléfono, el correo ni la dirección.',
          'Finalice un vínculo cuando lo necesite. El historial y los estados de cuenta se siguen pudiendo consultar.'],
         'Planta y bolsas aparece en el menú de la izquierda cuando existe un vínculo.', None),
        ('bags', 'box', 'Bolsas', 'Escanee los pedidos. Imprima la etiqueta. Selle la bolsa.',
         'En la pestaña Enviar, el personal escanea los pedidos que van en la bolsa, imprime su etiqueta y la sella, con número de sello si los usa.',
         ['La etiqueta dice de dónde sale la bolsa y a dónde va, su código y cada pedido que lleva con su número de piezas.',
          'Al llegar, Recibir: escanee la bolsa y luego cada pieza al sacarla.',
          'Al terminar, Fold dice cuántas piezas llegaron de las que se enviaron.',
          'Los mismos pasos traen los pedidos limpios de vuelta a la tienda.'],
         'Las etiquetas de bolsa se imprimen en su impresora de recibos. El campo de escaneo también acepta un código escrito.',
         lambda t: _art('Ejemplo de etiqueta de bolsa', _rc('BOLSA B-0419', 'Main St Cleaners → Planta Central', [
             ('D-1042 · Ortiz', '3 pzas'), ('D-1043 · Chen', '5 pzas'), ('D-1047 · Rivera', '4 pzas'), '-',
             ('3 pedidos', '12 piezas', True), ('Sello', '004871')], bar=True) +
             '<div class="mx-cap" style="font-weight:600;color:var(--ink-2)">Escanee en cada entrega</div>', t['example'])),
        ('track', 'route', '¿Dónde está?', 'Cinco etapas. Un vistazo.',
         'La pestaña Tablero muestra cada pedido entre la tienda y la planta, y la etapa en la que está.',
         ['Busque una pieza por su etiqueta, la etiqueta de la prenda, el número de pedido o el código de la bolsa.',
          'Cada pedido guarda una línea de tiempo de cada escaneo: quién, dónde y cuándo.',
          'En el ensamblaje, escanee cada pieza. El pedido pasa a Listo cuando entra la última, y Fold nombra las que faltan.',
          'La página del pedido que ve su cliente dice que está en la planta de limpieza. Nunca nombra la planta.'],
         None,
         lambda t: _art('Ejemplo de la etapa de un pedido entre la tienda y la planta', _stages(
             ['Esperando recogida', 'En camino a la planta', 'En la planta', 'De regreso a la tienda', 'De vuelta en la tienda'], 2,
             'Bolsa B-0419 · 12 de 12 piezas recibidas'), t['example'])),
        ('alerts', 'bell', 'Alertas', 'Una bolsa incompleta se nota el mismo día.',
         'La pestaña Alertas reúne todo lo que necesita a una persona.',
         ['<b>Conteo no coincide:</b> una bolsa se cerró con menos piezas de las enviadas. Alguien tiene que resolverla, con una nota.',
          '<b>Atrasada:</b> una bolsa lleva demasiado tiempo en camino. Doce horas, a menos que usted ponga otro límite.',
          '<b>Sin ensamblar</b> y <b>Escaneo desconocido</b>, para que nada espere sin que nadie lo vea.'],
         'Las alertas se ven en Fold POS. No envían mensajes de texto ni correos.',
         lambda t: _art('Ejemplo de una alerta de conteo que no coincide',
                        '<div class="mx-ui"><div class="ban"><i></i>Conteo no coincide</div>'
                        '<div class="row"><span><b>Bolsa B-0419</b> · Planta Central</span><span class="pill">11 de 12 piezas</span></div>'
                        '<div class="row"><span>Falta: <b>D-1042 · Saco</b> (1 de 3)</span></div>'
                        '<div class="row"><span>Necesita una nota para resolverse</span></div></div>', t['example'])),
        ('rates', 'invoice', 'Tarifas y estados de cuenta', 'Lo que la planta cobra a cada tienda, en una página al mes.',
         'Defina las tarifas de cada vínculo: por prenda, por libra o por pedido.',
         ['Un estado de cuenta por cada mes calendario: cada pedido, el día en que la planta lo recibió, piezas, libras e importe.',
          'Lo que no tiene tarifa aparece aparte como Sin precio, para que nada se cobre por error.',
          'Las piezas faltantes se cuentan en el estado de cuenta.',
          'Expórtelo como CSV.'],
         'El estado de cuenta es el registro con el que usted cobra. Fold no le cobra a la tienda de recepción por usted.',
         lambda t: _art('Ejemplo de estado de cuenta mensual de una planta a una tienda de recepción', _stmt(
             'Main St Cleaners · Septiembre', ['Pedido', 'Piezas', 'Importe'],
             [('D-1042', '3', '$9.75'), ('D-1043', '5', '$16.25'), ('D-1047', '4', '$13.00')], ('Total', '12', '$39.00')), t['example'])),
    ],
    'need_h2': 'Lo que necesita',
    'need': 'Un lector de códigos de barras, una impresora de recibos para las etiquetas de bolsa y una impresora de etiquetas que imprima códigos de barras si quiere escanear cada pieza por su etiqueta. Active Código de barras en las etiquetas de prendas en Configuración. <a href="/hardware#plant" hreflang="en">Vea la lista de equipos (en inglés)</a> o <a href="/follow-the-bag" hreflang="en">siga una bolsa en todo su recorrido (en inglés)</a>.',
    'faq_h2': 'Preguntas sobre plantas',
    'faq': [
        ('¿La planta y las tiendas de recepción tienen que ser del mismo dueño?', 'No. Las tiendas de su propio grupo se vinculan en un paso, y una tienda asociada entra con un código de un solo uso que crea la planta.'),
        ('¿Qué ve una planta asociada de mis clientes?', 'El nombre de pila del cliente. No el teléfono, ni el correo, ni la dirección.'),
        ('¿Qué pasa cuando falta una pieza?', 'La bolsa se cierra incompleta y Fold genera una alerta de Conteo no coincide. Sigue abierta hasta que alguien la resuelve con una nota, y la pieza aparece como faltante en el estado de cuenta.'),
        ('¿Fold le cobra a la tienda de recepción?', 'No. Fold le da el estado de cuenta mensual, con sus tarifas, y un CSV. El cobro lo hace usted.'),
        ('¿Necesito equipo especial?', 'Un lector de códigos y una impresora de recibos. Para códigos de barras en cada etiqueta de prenda, una impresora de etiquetas térmica. La <a href="/hardware#plant" hreflang="en">lista de equipos (en inglés)</a> tiene lo que recomendamos.'),
    ],
    'faq_more': 'Más en las <a href="/es/faq">preguntas frecuentes</a>.',
    'more_h2': 'Siga por aquí',
    'more': [
        ('/follow-the-bag', 'route', 'Siga la bolsa (en inglés)', 'Una bolsa de tintorería, de la tienda de recepción a la planta y de vuelta.'),
        ('/es/dry-cleaners', 'tag', 'Para tintorerías', 'Tickets por prenda, etiquetas y lugares en el transportador.'),
        ('/hardware', 'printer', 'Equipos (en inglés)', 'Impresoras, lectores y suministros para cada tipo de tienda.'),
        ('/es/contact', 'mail', 'Hable con nosotros', '¿Tiene una planta o un grupo de tiendas de recepción? Escríbanos.'),
    ],
    'md_title': '# Plantas y tiendas de recepción con Fold POS',
    'md_canon': '> Página canónica: https://foldpos.com/es/plants · Versión en Markdown.',
    'md_faq': '## Preguntas sobre plantas', 'md_more': '## Siga por aquí',
}


# ════════════════════════════ the builder ════════════════════════════
def _label(icon, text):
    return f'<div style="{LABEL_STYLE}">{ic(icon)}<span>{text}</span></div>'


def _section(t, key, icon, label, h2, sub, pts, note, art):
    lis = ''.join(f'<li>{ic("check")}<span>{p}</span></li>' for p in pts)
    text = (f'<div>{_label(icon, label)}<h2>{h2}</h2><p class="sub" style="margin-bottom:0">{sub}</p>'
            f'<ul class="mx-pts">{lis}</ul>' + (f'<p class="mx-note">{note}</p>' if note else '') + '</div>')
    if art is None:
        return f'<section class="section" id="{key}"><div class="wrap narrow">{text}</div></section>'
    return f'<section class="section" id="{key}"><div class="wrap"><div class="tagsplit">{text}{art(t)}</div></div></section>'


def _build(t):
    facts = ''.join(f'<div class="fact">{ic(i)}<div><b>{b}</b><span>{s}</span></div></div>' for i, b, s in t['facts'])
    sections = '\n'.join(_section(t, *s) for s in t['sections'])
    need = (f'<section class="section" id="need"><div class="wrap narrow"><h2>{t["need_h2"]}</h2>'
            f'<p class="sub" style="margin-bottom:0">{t["need"]}</p></div></section>\n') if t.get('need') else ''
    faq = ''.join(f'<details class="qa"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in t['faq'])
    def _hl(href):   # a Spanish page linking to a page that only exists in English
        return ' hreflang="en"' if t['lang'] == 'es' and not href.startswith('/es/') else ''
    more = ''.join(f'<a class="route" href="{href}"{_hl(href)}><span class="ic">{ic(i)}</span><span><b>{b}</b><span>{s}</span></span></a>'
                   for href, i, b, s in t['more'])
    body = f'''{STYLE}
<section class="phead"><div class="wrap">
  <div class="crumbs"><a href="{t['home']}">Fold POS</a> › {esc(t['crumb'])}</div>
  <div class="kicker">{t['kicker']}</div>
  <h1>{t['h1']}</h1>
  <p class="lede">{t['lede']}</p>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap">
  <h2 class="visually-hidden">{t['kicker']}</h2>
  <div class="facts">{facts}</div>
</div></section>
{sections}
{need}<section class="section" id="questions"><div class="wrap narrow">
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
    slug = t['slug'] if t['lang'] == 'en' else 'es/' + t['slug']
    html_ = page(slug, t['title'], t['desc'], t['og'], t['crumb'], body, [ld])
    if t['lang'] == 'es':
        for a, b in (('<html lang="en">', '<html lang="es">'), (BAND, BAND_ES),
                     (f'"item": "{SITE}/"', f'"item": "{SITE}/es/"')):
            assert a in html_, a
            html_ = html_.replace(a, b, 1)

    md = [t['md_title'], '', t['md_canon'], '', md_text(t['lede']), '']
    md += [f'- **{md_text(b)}**: {md_text(s)}' for i, b, s in t['facts']] + ['']
    for key, icon, label, h2, sub, pts, note, art in t['sections']:
        md += [f'## {md_text(label)}: {md_text(h2)}', '', md_text(sub), ''] + [f'- {md_text(p)}' for p in pts] + ['']
        if note:
            md += [md_text(note), '']
    if t.get('need'):
        md += [f'## {md_text(t["need_h2"])}', '', md_text(t['need']), '']
    md += [t['md_faq'], ''] + [f'**{md_text(q)}** {md_text(a)}\n' for q, a in t['faq']]
    md += [t['md_more'], ''] + [f'- [{md_text(b)}]({SITE}{href}): {md_text(s)}' for href, i, b, s in t['more']]
    md = '\n'.join(md) + '\n' + (md_footer() if t['lang'] == 'en' else MD_FOOTER_ES)
    return html_, md


def counter_money():
    return _build(MONEY_EN)


def plants():
    return _build(PLANTS_EN)


def counter_money_es():
    return _build(MONEY_ES)


def plants_es():
    return _build(PLANTS_ES)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    targets = [('es/counter-money', counter_money_es), ('es/plants', plants_es)]
    if '--es' not in sys.argv:
        targets = [('counter-money', counter_money), ('plants', plants)] + targets
    for path, fn in targets:
        h, md = fn()
        open(os.path.join(root, path + '.html'), 'w', encoding='utf-8').write(h)
        open(os.path.join(root, path + '.md'), 'w', encoding='utf-8').write(md.rstrip() + '\n')
        print('wrote', path)
