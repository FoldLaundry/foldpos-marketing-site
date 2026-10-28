#!/usr/bin/env python3
"""The Fold Time page, in English and Spanish:

    /fold-time      Fold Time: the wall device staff tap with their own phone to clock in,
                     take breaks and clock out. Price, the three steps for the owner, what
                     staff see, why the hours hold up, the device, questions, and the
                     interactive walkthrough (/time-clock-tour) embedded lower on the page.

    from pages_foldtime import fold_time     # -> (html, md), English

build_site.py writes the English page like assistants(). The Spanish page (es/fold-time:
.html and .md) is a static file like the rest of es/: run `python3 pages_foldtime.py --es`
after changing the copy here, then build_site.py and check_seo.py. Built by pages_more._build,
so it uses that page's markup and styles; the screenshots and the tour are added here.

Every claim comes from the project brief `claude/fold-time-site-brief-2026-10-14.md`
(checked against the API on Oct 14 2026, prices in API 4e5e0c99). Deliberately NOT said,
because it is not true or not ours to promise: that it works offline (the tap needs the
phone's internet), that it stops all time theft, that it reads location (it reads none),
that staff see more than this pay period and the last, that owners get texts today (say
"by text or email"), that it is on Starter or sold on its own, and free shipping as a
promotion ("shipping included" only).

Images: assets/img/fold-time/*.webp, from the real screens of the local test run (store
"Fold Demo Laundry"; My hours uses sample hours) and CAD renders of the housing.
"""
import os
import sys

from build_site import esc
from pages_more import _build

IMG = '/assets/img/fold-time/'
TOUR = '/time-clock-tour'

EXTRA_STYLE = '''<style>
.ft-shots{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}
.ft-shot{width:min(240px,100%);height:auto;border-radius:18px;border:1px solid var(--line);background:#fff;box-shadow:0 22px 44px -30px rgba(14,23,48,.55)}
.ft-dev{width:min(300px,100%);height:auto;border-radius:18px}
.ft-tour{margin-top:20px;border:1px solid var(--line);border-radius:18px;overflow:hidden;background:var(--surface,#fff)}
.ft-tour iframe{display:block;width:100%;height:min(760px,88vh);border:0}
</style>'''


def _shots(items, cap):
    """One or two phone screens side by side, with a caption."""
    imgs = ''.join(
        f'<img class="ft-shot" src="{IMG}{f}" width="520" height="{h}" loading="lazy" decoding="async" alt="{esc(alt)}">'
        for f, h, alt in items)
    return f'<figure class="mx-art" style="margin:0"><div class="ft-shots">{imgs}</div><figcaption class="mx-cap">{cap}</figcaption></figure>'


def _device(alt, cap):
    return (f'<figure class="mx-art" style="margin:0"><img class="ft-dev" src="{IMG}device-front.webp" width="520" height="676" '
            f'loading="lazy" decoding="async" alt="{esc(alt)}"><figcaption class="mx-cap">{cap}</figcaption></figure>')


EN = {
    'slug': 'fold-time', 'lang': 'en', 'home': '/', 'pre': '',
    'title': 'Fold Time: staff clock in with a tap — Fold POS',
    'desc': 'Fold Time is a small wall device your staff tap with their own phone to clock in, take breaks and clock out. No app, no PINs to share. $39 a device, your first one free, with Growth and Pro.',
    'og': 'Fold Time: staff clock in with a tap of their own phone',
    'crumb': 'Fold Time',
    'kicker_keep': True, 'kicker': 'Staff time clock',
    'h1': 'Fold Time.',
    'lede': 'A small wall device your staff tap with their own phone to clock in, take breaks and clock out. No app, no time-clock terminal, no PINs to share. It arrives set up and switches on with its first tap.',
    'facts': [
        ('card', '$39 a device, your first one free', 'Added to your next Fold POS bill when it ships. Shipping included. With Growth and Pro.'),
        ('shield', 'A copied link won’t work', 'Every tap carries a one-time code from the chip.'),
        ('users', 'No app for your staff', 'The tap opens a page on their own phone.'),
    ],
    'sections': [
        ('start', 'box', 'Getting started', 'Order, unbox, tap.',
         'Four steps, all from Fold POS.',
         ['<b>Order in Fold POS.</b> Schedule › Time clock › Tags › Fold Time devices › Order devices, 1 to 20 at a time. You see the total before you order, and a confirmation with the price comes by text or email.',
          '<b>We ship it ready.</b> Each device is set up at Fold, labeled and boxed. You get an “on the way” message with the tracking link.',
          '<b>Tap to switch it on.</b> The first tap of any device with your own phone switches on the whole box for your store and turns on phone clock-in.',
          '<b>Add your staff.</b> In Fold POS, Time clock › Phones, add each person. They get a text to set up their phone, then tap any Fold Time device to clock in.'],
         'Nothing to pay at checkout: the devices are added to your next Fold POS bill when the box ships.',
         lambda t: _shots([('owner-activated.webp', 1125, 'The page an owner sees after the first tap: Activated, with the devices named Fold Time 1 and Fold Time 2')],
                          'The first tap with your phone switches the box on.')),
        ('staff', 'users', 'For your staff', 'Tap, pick, done.',
         'Staff tap their phone on the device and a page opens. No app to install.',
         ['Clock in, start a meal or rest break, end a break, clock out.',
          'A 10-second Undo after every tap.',
          'Phones set to Spanish see the page in Spanish.',
          'After clocking out they get a text with today’s hours and a link to <b>My hours</b>: this pay period and the last, week by week, each day with start and end times and breaks, overtime, and whether you approved the period.',
          'An optional selfie at clock-in, if you turn it on. Only managers see it, it is never face-matched, and it is deleted after 30 days.'],
         None,
         lambda t: _shots([('staff-clocked-in.webp', 885, 'Phone screen after a tap: Clocked in, 11:32 AM, with Undo'),
                           ('staff-my-hours.webp', 885, 'My hours on a phone: today, this pay period and its days')],
                          'Real screens from a test store. My hours shows sample hours.')),
        ('trust', 'shield', 'Why the hours hold up', 'Hours you can trust.',
         'Built for the questions that come up on payday.',
         ['<b>No buddy punching by copied links.</b> Every tap carries a one-time code from the chip (NTAG 424 DNA). A copied or replayed link is refused.',
          '<b>Only registered phones.</b> A phone you have not added in Fold POS can’t clock anyone in.',
          '<b>Records can’t be quietly changed.</b> Punches are never overwritten. A manager’s correction is recorded next to the original, and the staff member sees “Changed by your manager” in My hours.',
          '<b>California mode.</b> Daily overtime over 8 hours, double time over 12, the seventh-day rule, and meal and rest premiums flagged for you.',
          '<b>Payroll.</b> Approved hours go to QuickBooks by kind of pay. A CSV export works with any payroll.',
          '<b>If a phone is dead.</b> Use the rotating clock-in QR on the POS, or the POS PIN clock.'],
         None,
         lambda t: _shots([('texts-staff.webp', 885, 'Two texts to a staff member: the setup link, and after clocking out, today’s hours with a link to My hours')],
                          'The texts your staff get, from a test store.')),
        ('device', 'tag', 'The device', 'Small, and nothing to plug in.',
         'It screws to the wall by the door or station where people start work.',
         ['80 × 110 × 12 mm. The screws are hidden under the cover.',
          '“TAP YOUR PHONE / TOQUE CON SU TELÉFONO” on the front, and a label with the station name.',
          'No batteries, no power, no Wi-Fi: it works through the housing.',
          'Devices arrive named Fold Time 1, 2 and so on. Rename them in Fold POS.'],
         'Shown: a render of the housing. Photos of the real device are coming.',
         lambda t: _device('Render of the Fold Time wall device: a white rounded rectangle reading FOLD TIME, TAP YOUR PHONE, TOQUE CON SU TELÉFONO',
                           'Fold Time, 80 × 110 × 12 mm.')),
    ],
    'tour_h2': 'Try it',
    'tour_sub': 'A walkthrough of a shift, from the first tap to the hours in QuickBooks.',
    'tour_open': 'Open the walkthrough full screen',
    'tour_title': 'Fold Time walkthrough',
    'tour_src': TOUR,
    'faq_h2': 'Fold Time questions',
    'faq': [
        ('Do my staff need an app?', 'No. The tap opens a web page on their phone.'),
        ('What does it cost?', '$39 a device, your first one free, added to your next Fold POS bill. Shipping included. Fold Time comes with Growth and Pro.'),
        ('What if someone copies the link?', 'It won’t work. Each tap carries a one-time code from the chip, so a copied or replayed link is refused.'),
        ('Can staff clock in from home?', 'Not by tap: they have to tap the device at the store. The backup clock-in QR is on the POS screen, at the store.'),
        ('What if an employee’s phone dies?', 'Use the clock-in QR on the POS or the POS PIN clock.'),
        ('How do staff see their hours?', 'The link in their clock-out text, or the My hours button after any tap. It shows this pay period and the last.'),
        ('How many do I need?', 'One for each door or station where people start work. Most shops need one or two.'),
        ('Does it work with payroll?', 'QuickBooks directly; any other payroll with the CSV export.'),
    ],
    'faq_more': 'Prices and plans on the <a href="/pricing">pricing page</a>. More short answers in the <a href="/help">help center</a>.',
    'more_h2': 'Where to next',
    'more': [
        ('/pricing', 'card', 'Pricing', 'Fold Time comes with Growth and Pro.'),
        ('/hardware', 'printer', 'Hardware', 'What else your shop may need.'),
        ('/help', 'flow', 'Help center', 'Short answers for the counter.'),
    ],
    'md_title': '# Fold Time: staff clock in with a tap',
    'md_canon': '> Canonical page: https://foldpos.com/fold-time · Markdown mirror.',
    'md_faq': '## Fold Time questions', 'md_more': '## Where to next',
}

ES = {
    'slug': 'fold-time', 'lang': 'es', 'home': '/es/', 'pre': '/es',
    'title': 'Fold Time: el personal marca con un toque — Fold POS',
    'desc': 'Fold Time es un pequeño dispositivo de pared que su personal toca con su propio teléfono para marcar entrada, tomar descansos y marcar salida. Sin app y sin PIN compartidos. $39 por dispositivo, el primero gratis, con Growth y Pro.',
    'og': 'Fold Time: el personal marca con un toque de su propio teléfono',
    'crumb': 'Fold Time',
    'kicker_keep': True, 'kicker': 'Reloj de asistencia',
    'h1': 'Fold Time.',
    'lede': 'Un pequeño dispositivo de pared que su personal toca con su propio teléfono para marcar entrada, tomar descansos y marcar salida. Sin app, sin terminal de reloj checador, sin PIN que compartir. Llega configurado y se activa con el primer toque.',
    'facts': [
        ('card', '$39 por dispositivo, el primero gratis', 'Se suma a su próxima factura de Fold POS cuando se envía. Envío incluido. Con Growth y Pro.'),
        ('shield', 'Un enlace copiado no sirve', 'Cada toque lleva un código de un solo uso del chip.'),
        ('users', 'Sin app para su personal', 'El toque abre una página en su propio teléfono.'),
    ],
    'sections': [
        ('start', 'box', 'Para empezar', 'Pida, abra la caja, toque.',
         'Cuatro pasos, todos desde Fold POS.',
         ['<b>Pida en Fold POS.</b> Cronograma › Reloj checador › Etiquetas › Dispositivos Fold Time › Pedir dispositivos, de 1 a 20 a la vez. Ve el total antes de pedir, y le llega una confirmación con el precio por mensaje de texto o correo.',
          '<b>Se lo enviamos listo.</b> Cada dispositivo se configura en Fold, se etiqueta y se empaca. Recibe un aviso de “en camino” con el enlace de seguimiento.',
          '<b>Toque para activarlo.</b> El primer toque de cualquier dispositivo con su propio teléfono activa toda la caja para su tienda y enciende el registro de entrada con el teléfono.',
          '<b>Agregue a su personal.</b> En Fold POS, Reloj checador › Teléfonos, agregue a cada persona. Recibe un mensaje de texto para configurar su teléfono y luego toca cualquier dispositivo Fold Time para marcar entrada.'],
         'No paga nada al pedir: los dispositivos se suman a su próxima factura de Fold POS cuando se envía la caja.',
         lambda t: _shots([('owner-activated.webp', 1125, 'La página que ve el propietario después del primer toque: Activado, con los dispositivos Fold Time 1 y Fold Time 2')],
                          'El primer toque con su teléfono activa la caja. Pantalla mostrada en inglés.')),
        ('staff', 'users', 'Para su personal', 'Tocar, elegir, listo.',
         'Su personal toca el dispositivo con su teléfono y se abre una página. Sin app que instalar.',
         ['Marcar entrada, empezar un descanso para comer o de reposo, terminar el descanso, marcar salida.',
          'Un botón Deshacer de 10 segundos después de cada toque.',
          'Los teléfonos en español ven la página en español.',
          'Al marcar salida reciben un mensaje de texto con las horas del día y un enlace a <b>Mis horas</b>: este periodo de pago y el anterior, semana por semana, cada día con hora de entrada y de salida y descansos, horas extra, y si usted aprobó el periodo.',
          'Una selfie opcional al marcar entrada, si usted la activa. Solo la ven los gerentes, nunca se compara con caras y se borra a los 30 días.'],
         None,
         lambda t: _shots([('staff-clocked-in.webp', 885, 'Pantalla del teléfono después de un toque: entrada marcada a las 11:32 AM, con Deshacer'),
                           ('staff-my-hours-es.webp', 885, 'Mis horas en un teléfono: hoy, este periodo de pago y sus días')],
                          'Pantallas reales de una tienda de prueba. Mis horas muestra horas de ejemplo.')),
        ('trust', 'shield', 'Por qué las horas son confiables', 'Horas en las que puede confiar.',
         'Pensado para las preguntas que surgen el día de pago.',
         ['<b>Nadie marca por otro con un enlace copiado.</b> Cada toque lleva un código de un solo uso del chip (NTAG 424 DNA). Un enlace copiado o repetido se rechaza.',
          '<b>Solo teléfonos registrados.</b> Un teléfono que usted no agregó en Fold POS no puede marcar a nadie.',
          '<b>Los registros no se cambian a escondidas.</b> Las marcas nunca se sobrescriben. La corrección de un gerente queda registrada junto a la original, y el empleado ve “Cambiado por su gerente” en Mis horas.',
          '<b>Modo California.</b> Horas extra diarias después de 8 horas, tiempo doble después de 12, la regla del séptimo día, y las primas por descansos para comer y de reposo señaladas para usted.',
          '<b>Nómina.</b> Las horas aprobadas pasan a QuickBooks por tipo de pago. Una exportación CSV sirve para cualquier nómina.',
          '<b>Si un teléfono se queda sin batería.</b> Use el código QR de entrada que cambia en el POS, o el reloj con PIN del POS.'],
         None, None),
        ('device', 'tag', 'El dispositivo', 'Pequeño y sin nada que conectar.',
         'Se atornilla a la pared junto a la puerta o el puesto donde la gente empieza a trabajar.',
         ['80 × 110 × 12 mm. Los tornillos quedan ocultos bajo la tapa.',
          '“TAP YOUR PHONE / TOQUE CON SU TELÉFONO” en el frente, y una etiqueta con el nombre del puesto.',
          'Sin baterías, sin corriente, sin Wi-Fi: funciona a través de la carcasa.',
          'Los dispositivos llegan con los nombres Fold Time 1, 2, etc. Puede cambiarlos en Fold POS.'],
         'Se muestra una imagen digital de la carcasa. Pronto habrá fotos del dispositivo real.',
         lambda t: _device('Imagen digital del dispositivo de pared Fold Time: un rectángulo blanco redondeado que dice FOLD TIME, TAP YOUR PHONE, TOQUE CON SU TELÉFONO',
                           'Fold Time, 80 × 110 × 12 mm.')),
    ],
    'tour_h2': 'Pruébelo',
    'tour_sub': 'Un recorrido por un turno, desde el primer toque hasta las horas en QuickBooks.',
    'tour_open': 'Abrir el recorrido en pantalla completa',
    'tour_title': 'Recorrido de Fold Time',
    'tour_src': TOUR + '?lang=es',
    'faq_h2': 'Preguntas sobre Fold Time',
    'faq': [
        ('¿Mi personal necesita una app?', 'No. El toque abre una página web en su teléfono.'),
        ('¿Cuánto cuesta?', '$39 por dispositivo, el primero gratis, sumado a su próxima factura de Fold POS. Envío incluido. Fold Time viene con Growth y Pro.'),
        ('¿Y si alguien copia el enlace?', 'No sirve. Cada toque lleva un código de un solo uso del chip, así que un enlace copiado o repetido se rechaza.'),
        ('¿Puede el personal marcar desde casa?', 'No con un toque: tiene que tocar el dispositivo en la tienda. El código QR de respaldo está en la pantalla del POS, en la tienda.'),
        ('¿Y si el teléfono de un empleado se queda sin batería?', 'Use el código QR de entrada del POS o el reloj con PIN del POS.'),
        ('¿Cómo ve el personal sus horas?', 'Con el enlace del mensaje de salida, o con el botón Mis horas después de cualquier toque. Muestra este periodo de pago y el anterior.'),
        ('¿Cuántos necesito?', 'Uno por cada puerta o puesto donde la gente empieza a trabajar. La mayoría de las tiendas necesitan uno o dos.'),
        ('¿Funciona con la nómina?', 'Con QuickBooks directamente; con cualquier otra nómina mediante la exportación CSV.'),
    ],
    'faq_more': 'Precios y planes en la <a href="/es/pricing">página de precios</a>. Más respuestas cortas en el <a href="/es/help">centro de ayuda</a>.',
    'more_h2': 'Para seguir',
    'more': [
        ('/es/pricing', 'card', 'Precios', 'Fold Time viene con Growth y Pro.'),
        ('/hardware', 'printer', 'Equipos (inglés)', 'Qué más puede necesitar su tienda.'),
        ('/es/help', 'flow', 'Centro de ayuda', 'Respuestas cortas para el mostrador.'),
    ],
    'md_title': '# Fold Time: el personal marca con un toque',
    'md_canon': '> Página canónica: https://foldpos.com/es/fold-time · Versión en Markdown.',
    'md_faq': '## Preguntas sobre Fold Time', 'md_more': '## Para seguir',
}


def _with_tour(t):
    """The shared page, plus the screen styles and the walkthrough above the questions."""
    html_, md = _build(t)
    tour = (f'<section class="section" id="tour"><div class="wrap">\n'
            f'  <h2>{t["tour_h2"]}</h2>\n'
            f'  <p class="sub" style="margin-bottom:0">{t["tour_sub"]} <a href="{t["tour_src"]}">{t["tour_open"]}</a>.</p>\n'
            f'  <div class="ft-tour"><iframe src="{t["tour_src"]}" title="{esc(t["tour_title"])}" loading="lazy"></iframe></div>\n'
            f'</div></section>\n')
    anchor = '<section class="section" id="questions">'
    assert html_.count(anchor) == 1, anchor
    html_ = html_.replace(anchor, tour + anchor, 1)
    style_at = html_.index('<style>', html_.index('<body'))
    html_ = html_[:style_at] + EXTRA_STYLE + '\n' + html_[style_at:]
    faq_md = t['md_faq']
    assert md.count(faq_md) == 1, faq_md
    md = md.replace(faq_md, f'## {t["tour_h2"]}\n\n{t["tour_sub"]} https://foldpos.com{t["tour_src"]}\n\n{faq_md}', 1)
    return html_, md


def fold_time():
    """English page: (html, md) for slug 'fold-time'."""
    return _with_tour(EN)


def fold_time_es():
    """Spanish page: (html, md) for es/fold-time (a static file; see the module docstring)."""
    return _with_tour(ES)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    targets = [('es/fold-time', fold_time_es)]
    if '--es' not in sys.argv:
        targets = [('fold-time', fold_time)] + targets
    for path, fn in targets:
        h, md = fn()
        open(os.path.join(root, path + '.html'), 'w', encoding='utf-8').write(h)
        open(os.path.join(root, path + '.md'), 'w', encoding='utf-8').write(md.rstrip() + '\n')
        print('wrote', path)
