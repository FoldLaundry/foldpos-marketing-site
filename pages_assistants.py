#!/usr/bin/env python3
"""The help article "Connect an AI assistant to your store", in English and Spanish:

    /assistants      what a connected assistant can and cannot do, connecting by sign-in or
                     with a token, pausing and removing, the activity list, briefings and alerts by email,
                     and what to do if you think someone else got in

    from pages_assistants import assistants     # -> (html, md), English

build_site.py writes the English page like counter_money() and plants(). The Spanish page
(es/assistants: .html and .md) is a static file like the rest of es/: run
`python3 pages_assistants.py --es` after changing the copy here, then build_site.py and
check_seo.py. The page is built by pages_more._build, so it uses that page's markup and
styles and adds none of its own.

Every claim comes from the API's docs/STORE-MCP-OWNER-GUIDE.md and docs/STORE-MCP.md
(5 Oct 2026); the briefings section from docs/OWNER-BRIEFINGS.md (live 7 Oct 2026, by email:
it says nothing about texts beyond what the card itself shows). Deliberately NOT said, because those documents do not say it: any assistant
by name other than "such as Claude", a listing in anybody's directory, a plan or a price
for the feature, and anything an assistant can do beyond the list here.

The Settings › Assistants screen and the approval screen ship with the app release that
follows the API. This page describes them, so it goes live with that release, not before.

A new top-level page must also be in RESERVED_SLUGS in the API
(src/online-booking/online-booking.util.ts), or it would hide a shop's booking link:
add 'assistants' there.
"""
import os
import sys

from pages_more import _build

ADDRESS = 'https://app.foldpos.com/v1/mcp/store'

EN = {
    'slug': 'assistants', 'lang': 'en', 'home': '/', 'pre': '',
    'title': 'Connect an AI assistant to your store — Fold POS',
    'desc': 'Let your own AI assistant, such as Claude, answer questions about your Fold POS store: sales, orders, customers, machines and staff. It only looks unless you allow three small changes.',
    'og': 'Connect an AI assistant to your Fold POS store',
    'crumb': 'Connect an AI assistant',
    'kicker': 'Help center',
    'h1': 'Connect an AI assistant to your store.',
    'lede': 'If you use an AI assistant such as Claude, you can let it look at your store in Fold POS. Ask it “how are we doing today?”, “which orders are late?” or “what needs me?” from wherever you are, and it answers from your own store’s records.',
    'facts': [
        ('shield', 'Owner only', 'Only an owner can connect an assistant, see the list or remove one. Staff cannot.'),
        ('check', 'It looks, unless you allow more', 'Changes are off until you switch them on, and there are only three.'),
        ('card', 'No extra cost', 'It is not tied to a plan.'),
    ],
    'sections': [
        ('can', 'chat', 'What it can do', 'It answers from your own store’s records.',
         'A connected assistant can look at:',
         ['Today’s sales and how they were paid, and sales over a week, a month or a year, including sales tax.',
          'Orders: find one, see everything about it, see which are late and which are ready and waiting to be collected.',
          'Customers: find one, see their details, orders, store credit and notes.',
          'Machines: what is running, what is out of service, what maintenance is due.',
          'Supplies that are running low and what to reorder.',
          'The day’s pickups and deliveries, if your plan includes pickup &amp; delivery.',
          'Who is on shift and the hours people worked, if your plan includes staff shifts.',
          'A short list of what needs your attention right now.'],
         'If it cannot read something, it tells you it could not. It does not show you a zero in its place.', None),
        ('changes', 'flow', 'Changes', 'Three small changes, only if you allow them.',
         'Changes are off until you switch them on, and each assistant also needs your permission to make them.',
         ['Mark an order ready.',
          'Add a staff note to an order.',
          'Add a staff note to a customer’s file.',
          'Before every change the assistant is shown exactly what would happen and has to confirm it. It is told to show you first and wait for your yes.',
          'Every change appears under the bell at the counter and in your activity list.',
          'If your store sends a “your order is ready” text, marking an order ready sends it, the same as pressing Ready at the counter. Your staff can put the order back to In progress, but a text that went out cannot be taken back.',
          'A note an assistant adds cannot be edited or removed afterwards.'],
         'Fold POS cannot check that the assistant asked you, which is why the changes are kept this small.', None),
        ('cannot', 'shield', 'What it cannot do', 'It never moves money.',
         'An assistant cannot:',
         ['Take a payment, give a refund or a discount, or move money in any way.',
          'Cancel or delete an order, or change what is on one.',
          'Change your prices, your settings or your staff.',
          'See what your staff are paid.',
          'See card numbers. Fold POS does not store them.',
          'See any store but the one you connected it to.'],
         'In lists, customers’ phone numbers and emails are partly hidden. The assistant sees them in full only when it looks up one customer or one order.', None),
        ('connect', 'browser', 'Connect', 'Connect by signing in.',
         'Add the address in your assistant, then approve inside Fold POS.',
         ['<b>Step 1.</b> In your assistant’s settings, add a custom connector. Some call it an MCP server.',
          f'<b>Step 2.</b> Give it this address: <b>{ADDRESS}</b>',
          '<b>Step 3.</b> The assistant sends you to Fold POS. Sign in the way you always do, if you are not signed in already.',
          '<b>Step 4.</b> Fold POS shows you what is asking for access. Check the name of the app, where you will be sent back to after you answer, and the store it is for.',
          '<b>Step 5.</b> If the assistant asked to make changes, choose whether to allow that. Then approve.'],
         'Where you will be sent back to is the part that cannot be faked. It should be the site of the assistant you are connecting. If the screen warns you that it does not recognise the app, or that the request was not started from your device, and you did not expect that, say no. Never approve a request that arrived as a link from someone else.', None),
        ('token', 'code', 'Token', 'Or connect with a token.',
         'Some desktop apps do not send you to Fold POS to approve. They ask for a token instead.',
         ['<b>Step 1.</b> In Fold POS, open Settings › Assistants and create a token.',
          '<b>Step 2.</b> Give it a name you will recognise later, such as “Claude on my laptop”.',
          '<b>Step 3.</b> Choose how long it should last (up to 366 days, or no end date), and whether it may make changes.',
          '<b>Step 4.</b> Copy the token. It is shown once. Fold POS cannot show it to you again.',
          f'<b>Step 5.</b> In your assistant’s settings, add a custom connector or MCP server with the address <b>{ADDRESS}</b> and paste the token where it asks for a key or an authorization header.'],
         'Treat a token like a password. Anyone who has it can read your store’s orders, customers and sales. Do not paste it into a chat or an email. If you lose track of one, remove it and make a new one.', None),
        ('manage', 'history', 'Pause and remove', 'Pause, remove, and see what happened.',
         'All in Settings › Assistants.',
         ['<b>Pause.</b> One switch stops every connected assistant at once. Nothing is removed; switch it back on and they work again.',
          '<b>Stop changes.</b> A second switch decides whether assistants may make the three changes. Off means they can only look.',
          '<b>Remove.</b> Each connected assistant is listed with its name and when it was last used. Remove one and it stops working straight away.',
          '<b>Activity.</b> A list of what each assistant asked and what it changed, newest first, kept for 90 days. It shows which tool was used and when. It does not keep the answers, and it does not keep names, phone numbers or the text of notes.',
          '<b>An email each time.</b> Whenever an assistant is connected to your store, the person who connected it gets an email saying so.'],
         'A store can have 20 assistants connected at a time.', None),
        ('briefings', 'mail', 'Briefings and alerts', 'Or let Fold POS write to you.',
         'You do not need a connected assistant for this. Fold POS itself can send you a short message about your store.',
         ['<b>A morning briefing.</b> Yesterday’s sales and what needs you, at the time and on the days you pick.',
          '<b>Alerts.</b> A machine goes out of service, an order is two days late, or a supply runs low. Each one is announced once.',
          '<b>Where to switch it on.</b> Settings › Assistants › Briefings and alerts. It is off until you turn it on, and only an owner can.',
          '<b>Where it goes.</b> To the email on your account. The card shows where the next message will go, and “Send me a test” sends today’s briefing there now.',
          '<b>Limits.</b> At most 5 messages a day. No alerts between 9 pm and 7 am at your store; whatever is still true goes out in the morning. Several alerts at once arrive as one message.',
          '<b>What a message contains.</b> Counts, machine and supply names, and order numbers. Never a customer’s name, phone number or address.',
          '<b>Language.</b> English or Spanish, your choice.'],
         'Your store needs its time zone set in Settings › Business first, so the morning briefing arrives in your morning. The card also lets you choose text messages; until texting to owners is switched on, those go to your email as well, and the card says so.', None),
        ('security', 'bell', 'If someone else got in', 'If you think someone else got in.',
         'Do these in order.',
         ['<b>Step 1.</b> Open Settings › Assistants and remove any connection you do not recognise. If you are not sure which, pause all of them first.',
          '<b>Step 2.</b> Change your password. This disconnects every assistant you connected, so you will need to connect the ones you want again.',
          '<b>Step 3.</b> Look at the activity list to see what was asked.',
          '<b>Step 4.</b> Email <a href="mailto:contact@foldpos.com">contact@foldpos.com</a> and tell us your store name.'],
         'Assistants connected by another owner of the store are not affected by your password change. Remove those from the list.', None),
    ],
    'faq_h2': 'Assistant questions',
    'faq': [
        ('Does this cost extra?', 'No. It is not tied to a plan. Two of the things an assistant can look at follow your plan: pickups and deliveries, and staff shifts.'),
        ('Can my manager set this up?', 'No. Only an owner can connect an assistant, see the list or remove one.'),
        ('Can Fold connect an assistant for me?', 'No. A member of Fold’s team helping you from our side can pause assistants or remove one, but cannot connect one or switch changes on. That has to be you, signed in as yourself.'),
        ('What language does it answer in?', 'Your assistant answers in the language you write in. The information it gets from Fold POS is in English.'),
        ('Can my customers use an assistant too?', 'Separately from all of this, a customer’s own assistant can book a pickup with a shop that has online booking switched on. It follows the same rules as your booking page, and the bell tells you when a booking came in that way.'),
    ],
    'faq_more': 'Building an assistant or a connector? The address, the tools and the rules are on the <a href="/developers#store-mcp">developers page</a>. More short answers in the <a href="/help">help center</a>.',
    'more_h2': 'Where to next',
    'more': [
        ('/developers#store-mcp', 'code', 'For developers', 'The address, the tools and the rules.'),
        ('/hey-fold#briefings', 'mic', 'Hey Fold', 'Ask “what needs me?” out loud in Fold POS.'),
        ('/pickup-delivery#booking', 'car', 'Online booking', 'The booking page your customers use.'),
        ('/help', 'flow', 'Help center', 'Short answers for the counter.'),
    ],
    'md_title': '# Connect an AI assistant to your store',
    'md_canon': '> Canonical page: https://foldpos.com/assistants · Markdown mirror.',
    'md_faq': '## Assistant questions', 'md_more': '## Where to next',
}

ES = {
    'slug': 'assistants', 'lang': 'es', 'home': '/es/', 'pre': '/es',
    'title': 'Conecte un asistente de IA a su tienda — Fold POS',
    'desc': 'Deje que su propio asistente de IA, como Claude, responda preguntas sobre su tienda en Fold POS: ventas, pedidos, clientes, máquinas y personal. Solo mira, salvo que usted permita tres cambios pequeños.',
    'og': 'Conecte un asistente de IA a su tienda en Fold POS',
    'crumb': 'Conectar un asistente de IA',
    'kicker': 'Centro de ayuda',
    'h1': 'Conecte un asistente de IA a su tienda.',
    'lede': 'Si usa un asistente de IA como Claude, puede dejar que mire su tienda en Fold POS. Pregúntele “¿cómo vamos hoy?”, “¿qué pedidos están atrasados?” o “¿qué necesita mi atención?” desde donde esté, y le responde con los registros de su propia tienda.',
    'facts': [
        ('shield', 'Solo el propietario', 'Solo un propietario puede conectar un asistente, ver la lista o quitar uno. El personal no puede.'),
        ('check', 'Solo mira, salvo que usted permita más', 'Los cambios están apagados hasta que usted los enciende, y son solo tres.'),
        ('card', 'Sin costo extra', 'No depende de un plan.'),
    ],
    'sections': [
        ('can', 'chat', 'Qué puede hacer', 'Responde con los registros de su propia tienda.',
         'Un asistente conectado puede mirar:',
         ['Las ventas de hoy y cómo se pagaron, y las ventas de una semana, un mes o un año, con el impuesto sobre las ventas.',
          'Pedidos: buscar uno, ver todo sobre él, ver cuáles están atrasados y cuáles están listos y esperando a que los recojan.',
          'Clientes: buscar uno, ver sus datos, pedidos, crédito de tienda y notas.',
          'Máquinas: cuáles están en uso, cuáles están fuera de servicio y qué mantenimiento toca.',
          'Los insumos que se están acabando y qué volver a pedir.',
          'Las recogidas y entregas del día, si su plan incluye recogida y entrega.',
          'Quién está en turno y las horas que trabajó cada persona, si su plan incluye turnos del personal.',
          'Una lista corta de lo que necesita su atención en este momento.'],
         'Si no puede leer algo, le dice que no pudo. No le muestra un cero en su lugar.', None),
        ('changes', 'flow', 'Cambios', 'Tres cambios pequeños, solo si usted los permite.',
         'Los cambios están apagados hasta que usted los enciende, y cada asistente necesita además su permiso para hacerlos.',
         ['Marcar un pedido como listo.',
          'Agregar una nota del personal a un pedido.',
          'Agregar una nota del personal al expediente de un cliente.',
          'Antes de cada cambio, el asistente ve exactamente lo que pasaría y tiene que confirmarlo. Tiene la instrucción de mostrárselo primero a usted y esperar su “sí”.',
          'Cada cambio aparece bajo la campana en el mostrador y en su lista de actividad.',
          'Si su tienda envía el mensaje de texto “su pedido está listo”, marcar un pedido como listo lo envía, igual que al presionar Listo en el mostrador. Su personal puede regresar el pedido a En proceso, pero un mensaje que ya salió no se puede retirar.',
          'Una nota que agrega un asistente no se puede editar ni quitar después.'],
         'Fold POS no puede comprobar que el asistente le preguntó a usted, y por eso los cambios son así de pequeños.', None),
        ('cannot', 'shield', 'Qué no puede hacer', 'Nunca mueve dinero.',
         'Un asistente no puede:',
         ['Cobrar un pago, dar un reembolso o un descuento, ni mover dinero de ninguna forma.',
          'Cancelar o eliminar un pedido, ni cambiar lo que contiene.',
          'Cambiar sus precios, su configuración ni su personal.',
          'Ver cuánto se le paga a su personal.',
          'Ver números de tarjeta. Fold POS no los guarda.',
          'Ver ninguna otra tienda que no sea la que usted conectó.'],
         'En las listas, los teléfonos y correos de los clientes aparecen parcialmente ocultos. El asistente los ve completos solo cuando consulta un cliente o un pedido.', None),
        ('connect', 'browser', 'Conectar', 'Conecte iniciando sesión.',
         'Agregue la dirección en su asistente y luego apruebe dentro de Fold POS.',
         ['<b>Paso 1.</b> En la configuración de su asistente, agregue un conector personalizado. Algunos lo llaman servidor MCP.',
          f'<b>Paso 2.</b> Póngale esta dirección: <b>{ADDRESS}</b>',
          '<b>Paso 3.</b> El asistente lo envía a Fold POS. Inicie sesión como siempre, si todavía no lo ha hecho.',
          '<b>Paso 4.</b> Fold POS le muestra qué está pidiendo acceso. Revise el nombre de la app, adónde regresará usted después de responder y para qué tienda es.',
          '<b>Paso 5.</b> Si el asistente pidió hacer cambios, elija si lo permite. Luego apruebe.'],
         'Adónde regresará usted es la parte que no se puede falsificar. Debe ser el sitio del asistente que está conectando. Si la pantalla le advierte que no reconoce la app, o que la solicitud no se inició desde su dispositivo, y usted no lo esperaba, diga que no. Nunca apruebe una solicitud que le llegó como un enlace de otra persona.', None),
        ('token', 'code', 'Token', 'O conecte con un token.',
         'Algunas apps de escritorio no lo envían a Fold POS para aprobar. Piden un token.',
         ['<b>Paso 1.</b> En Fold POS, abra Configuración › Asistentes y cree un token.',
          '<b>Paso 2.</b> Póngale un nombre que reconozca después, como “Claude en mi laptop”.',
          '<b>Paso 3.</b> Elija cuánto debe durar (hasta 366 días, o sin fecha de vencimiento) y si puede hacer cambios.',
          '<b>Paso 4.</b> Copie el token. Se muestra una sola vez. Fold POS no puede volver a mostrárselo.',
          f'<b>Paso 5.</b> En la configuración de su asistente, agregue un conector personalizado o servidor MCP con la dirección <b>{ADDRESS}</b> y pegue el token donde le pida una clave o un encabezado de autorización.'],
         'Trate un token como una contraseña. Quien lo tenga puede leer los pedidos, los clientes y las ventas de su tienda. No lo pegue en un chat ni en un correo. Si le pierde la pista a uno, quítelo y cree otro.', None),
        ('manage', 'history', 'Pausar y quitar', 'Pause, quite y vea lo que pasó.',
         'Todo está en Configuración › Asistentes.',
         ['<b>Pausar.</b> Un interruptor detiene a todos los asistentes conectados a la vez. No se quita nada; vuelva a encenderlo y funcionan otra vez.',
          '<b>Detener los cambios.</b> Un segundo interruptor decide si los asistentes pueden hacer los tres cambios. Apagado significa que solo pueden mirar.',
          '<b>Quitar.</b> Cada asistente conectado aparece con su nombre y la última vez que se usó. Quite uno y deja de funcionar de inmediato.',
          '<b>Actividad.</b> Una lista de lo que preguntó cada asistente y lo que cambió, de lo más reciente a lo más antiguo, que se conserva 90 días. Muestra qué herramienta se usó y cuándo. No guarda las respuestas, ni nombres, teléfonos o el texto de las notas.',
          '<b>Un correo cada vez.</b> Cada vez que se conecta un asistente a su tienda, la persona que lo conectó recibe un correo que lo avisa.'],
         'Una tienda puede tener 20 asistentes conectados a la vez.', None),
        ('briefings', 'mail', 'Resúmenes y alertas', 'O deje que Fold POS le escriba.',
         'Para esto no necesita un asistente conectado. El propio Fold POS puede enviarle un mensaje corto sobre su tienda.',
         ['<b>Un resumen por la mañana.</b> Las ventas de ayer y lo que necesita su atención, a la hora y en los días que usted elija.',
          '<b>Alertas.</b> Una máquina queda fuera de servicio, un pedido lleva dos días de atraso o un insumo se está acabando. Cada una se avisa una sola vez.',
          '<b>Dónde se enciende.</b> Configuración › Asistentes › Resúmenes y alertas. Está apagado hasta que usted lo enciende, y solo un propietario puede hacerlo.',
          '<b>Adónde llega.</b> Al correo de su cuenta. La tarjeta muestra adónde irá el próximo mensaje, y “Enviarme una prueba” envía allí el resumen de hoy en ese momento.',
          '<b>Límites.</b> Como máximo 5 mensajes al día. No hay alertas entre las 9 p. m. y las 7 a. m. en su tienda; lo que siga siendo cierto sale por la mañana. Varias alertas a la vez llegan en un solo mensaje.',
          '<b>Qué contiene un mensaje.</b> Cantidades, nombres de máquinas y de insumos, y números de pedido. Nunca el nombre, el teléfono ni la dirección de un cliente.',
          '<b>Idioma.</b> Inglés o español, a su elección.'],
         'Su tienda necesita tener su zona horaria en Configuración › Negocio, para que el resumen llegue en su mañana. La tarjeta también permite elegir mensajes de texto; hasta que se enciendan los mensajes de texto para propietarios, esos también llegan a su correo, y la tarjeta lo dice.', None),
        ('security', 'bell', 'Si alguien más entró', 'Si cree que alguien más entró.',
         'Haga esto en orden.',
         ['<b>Paso 1.</b> Abra Configuración › Asistentes y quite cualquier conexión que no reconozca. Si no está seguro de cuál, primero pause todas.',
          '<b>Paso 2.</b> Cambie su contraseña. Esto desconecta todos los asistentes que usted conectó, así que tendrá que volver a conectar los que quiera.',
          '<b>Paso 3.</b> Revise la lista de actividad para ver qué se preguntó.',
          '<b>Paso 4.</b> Escriba a <a href="mailto:contact@foldpos.com">contact@foldpos.com</a> y díganos el nombre de su tienda.'],
         'El cambio de su contraseña no afecta a los asistentes que conectó otro propietario de la tienda. Quítelos de la lista.', None),
    ],
    'faq_h2': 'Preguntas sobre los asistentes',
    'faq': [
        ('¿Cuesta extra?', 'No. No depende de un plan. Dos de las cosas que un asistente puede mirar dependen de su plan: las recogidas y entregas, y los turnos del personal.'),
        ('¿Puede configurarlo mi gerente?', 'No. Solo un propietario puede conectar un asistente, ver la lista o quitar uno.'),
        ('¿Puede Fold conectar un asistente por mí?', 'No. Una persona del equipo de Fold que le ayude desde nuestro lado puede pausar los asistentes o quitar uno, pero no puede conectar uno ni encender los cambios. Eso tiene que hacerlo usted, con su propia sesión.'),
        ('¿En qué idioma responde?', 'Su asistente responde en el idioma en que usted le escribe. La información que recibe de Fold POS está en inglés.'),
        ('¿Mis clientes también pueden usar un asistente?', 'Aparte de todo esto, el asistente de un cliente puede reservar una recogida en una tienda que tenga activadas las reservas en línea. Sigue las mismas reglas que su página de reservas, y la campana le avisa cuando una reserva llegó así.'),
    ],
    'faq_more': '¿Está creando un asistente o un conector? La dirección, las herramientas y las reglas están en la <a href="/es/developers#store-mcp">página para desarrolladores</a>. Más respuestas cortas en el <a href="/es/help">centro de ayuda</a>.',
    'more_h2': 'Para seguir',
    'more': [
        ('/es/developers#store-mcp', 'code', 'Para desarrolladores', 'La dirección, las herramientas y las reglas.'),
        ('/es/hey-fold#briefings', 'mic', 'Hey Fold', 'Pregunte “¿qué necesita mi atención?” en voz alta en Fold POS.'),
        ('/es/pickup-delivery#booking', 'car', 'Reservas en línea', 'La página de reservas que usan sus clientes.'),
        ('/es/help', 'flow', 'Centro de ayuda', 'Respuestas cortas para el mostrador.'),
    ],
    'md_title': '# Conecte un asistente de IA a su tienda',
    'md_canon': '> Página canónica: https://foldpos.com/es/assistants · Versión en Markdown.',
    'md_faq': '## Preguntas sobre los asistentes', 'md_more': '## Para seguir',
}


def assistants():
    """English page: (html, md) for slug 'assistants'."""
    return _build(EN)


def assistants_es():
    """Spanish page: (html, md) for es/assistants (a static file; see the module docstring)."""
    return _build(ES)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    targets = [('es/assistants', assistants_es)]
    if '--es' not in sys.argv:
        targets = [('assistants', assistants)] + targets
    for path, fn in targets:
        h, md = fn()
        open(os.path.join(root, path + '.html'), 'w', encoding='utf-8').write(h)
        open(os.path.join(root, path + '.md'), 'w', encoding='utf-8').write(md.rstrip() + '\n')
        print('wrote', path)
