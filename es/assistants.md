# Conecte un asistente de IA a su tienda

> Página canónica: https://foldpos.com/es/assistants · Versión en Markdown.

Si usa un asistente de IA como Claude, puede dejar que mire su tienda en Fold POS. Pregúntele “¿cómo vamos hoy?”, “¿qué pedidos están atrasados?” o “¿qué necesita mi atención?” desde donde esté, y le responde con los registros de su propia tienda.

- **Solo el propietario**: Solo un propietario puede conectar un asistente, ver la lista o quitar uno. El personal no puede.
- **Solo mira, salvo que usted permita más**: Los cambios están apagados hasta que usted los enciende, y son solo tres.
- **Sin costo extra**: No depende de un plan.

## Qué puede hacer: Responde con los registros de su propia tienda.

Un asistente conectado puede mirar:

- Las ventas de hoy y cómo se pagaron, y las ventas de una semana, un mes o un año, con el impuesto sobre las ventas.
- Pedidos: buscar uno, ver todo sobre él, ver cuáles están atrasados y cuáles están listos y esperando a que los recojan.
- Clientes: buscar uno, ver sus datos, pedidos, crédito de tienda y notas.
- Máquinas: cuáles están en uso, cuáles están fuera de servicio y qué mantenimiento toca.
- Los insumos que se están acabando y qué volver a pedir.
- Las recogidas y entregas del día, si su plan incluye recogida y entrega.
- Quién está en turno y las horas que trabajó cada persona, si su plan incluye turnos del personal.
- Una lista corta de lo que necesita su atención en este momento.

Si no puede leer algo, le dice que no pudo. No le muestra un cero en su lugar.

## Cambios: Tres cambios pequeños, solo si usted los permite.

Los cambios están apagados hasta que usted los enciende, y cada asistente necesita además su permiso para hacerlos.

- Marcar un pedido como listo.
- Agregar una nota del personal a un pedido.
- Agregar una nota del personal al expediente de un cliente.
- Antes de cada cambio, el asistente ve exactamente lo que pasaría y tiene que confirmarlo. Tiene la instrucción de mostrárselo primero a usted y esperar su “sí”.
- Cada cambio aparece bajo la campana en el mostrador y en su lista de actividad.
- Si su tienda envía el mensaje de texto “su pedido está listo”, marcar un pedido como listo lo envía, igual que al presionar Listo en el mostrador. Su personal puede regresar el pedido a En proceso, pero un mensaje que ya salió no se puede retirar.
- Una nota que agrega un asistente no se puede editar ni quitar después.

Fold POS no puede comprobar que el asistente le preguntó a usted, y por eso los cambios son así de pequeños.

## Qué no puede hacer: Nunca mueve dinero.

Un asistente no puede:

- Cobrar un pago, dar un reembolso o un descuento, ni mover dinero de ninguna forma.
- Cancelar o eliminar un pedido, ni cambiar lo que contiene.
- Cambiar sus precios, su configuración ni su personal.
- Ver cuánto se le paga a su personal.
- Ver números de tarjeta. Fold POS no los guarda.
- Ver ninguna otra tienda que no sea la que usted conectó.

En las listas, los teléfonos y correos de los clientes aparecen parcialmente ocultos. El asistente los ve completos solo cuando consulta un cliente o un pedido.

## Conectar: Conecte iniciando sesión.

Agregue la dirección en su asistente y luego apruebe dentro de Fold POS.

- Paso 1. En la configuración de su asistente, agregue un conector personalizado. Algunos lo llaman servidor MCP.
- Paso 2. Póngale esta dirección: https://app.foldpos.com/v1/mcp/store
- Paso 3. El asistente lo envía a Fold POS. Inicie sesión como siempre, si todavía no lo ha hecho.
- Paso 4. Fold POS le muestra qué está pidiendo acceso. Revise el nombre de la app, adónde regresará usted después de responder y para qué tienda es.
- Paso 5. Si el asistente pidió hacer cambios, elija si lo permite. Luego apruebe.

Adónde regresará usted es la parte que no se puede falsificar. Debe ser el sitio del asistente que está conectando. Si la pantalla le advierte que no reconoce la app, o que la solicitud no se inició desde su dispositivo, y usted no lo esperaba, diga que no. Nunca apruebe una solicitud que le llegó como un enlace de otra persona.

## Token: O conecte con un token.

Algunas apps de escritorio no lo envían a Fold POS para aprobar. Piden un token.

- Paso 1. En Fold POS, abra Configuración › Asistentes y cree un token.
- Paso 2. Póngale un nombre que reconozca después, como “Claude en mi laptop”.
- Paso 3. Elija cuánto debe durar (hasta 366 días, o sin fecha de vencimiento) y si puede hacer cambios.
- Paso 4. Copie el token. Se muestra una sola vez. Fold POS no puede volver a mostrárselo.
- Paso 5. En la configuración de su asistente, agregue un conector personalizado o servidor MCP con la dirección https://app.foldpos.com/v1/mcp/store y pegue el token donde le pida una clave o un encabezado de autorización.

Trate un token como una contraseña. Quien lo tenga puede leer los pedidos, los clientes y las ventas de su tienda. No lo pegue en un chat ni en un correo. Si le pierde la pista a uno, quítelo y cree otro.

## Pausar y quitar: Pause, quite y vea lo que pasó.

Todo está en Configuración › Asistentes.

- Pausar. Un interruptor detiene a todos los asistentes conectados a la vez. No se quita nada; vuelva a encenderlo y funcionan otra vez.
- Detener los cambios. Un segundo interruptor decide si los asistentes pueden hacer los tres cambios. Apagado significa que solo pueden mirar.
- Quitar. Cada asistente conectado aparece con su nombre y la última vez que se usó. Quite uno y deja de funcionar de inmediato.
- Actividad. Una lista de lo que preguntó cada asistente y lo que cambió, de lo más reciente a lo más antiguo, que se conserva 90 días. Muestra qué herramienta se usó y cuándo. No guarda las respuestas, ni nombres, teléfonos o el texto de las notas.
- Un correo cada vez. Cada vez que se conecta un asistente a su tienda, la persona que lo conectó recibe un correo que lo avisa.

Una tienda puede tener 20 asistentes conectados a la vez.

## Resúmenes y alertas: O deje que Fold POS le escriba.

Para esto no necesita un asistente conectado. El propio Fold POS puede enviarle un mensaje corto sobre su tienda.

- Un resumen por la mañana. Las ventas de ayer y lo que necesita su atención, a la hora y en los días que usted elija.
- Alertas. Una máquina queda fuera de servicio, un pedido lleva dos días de atraso o un insumo se está acabando. Cada una se avisa una sola vez.
- Dónde se enciende. Configuración › Asistentes › Resúmenes y alertas. Está apagado hasta que usted lo enciende, y solo un propietario puede hacerlo.
- Adónde llega. Al correo de su cuenta. La tarjeta muestra adónde irá el próximo mensaje, y “Enviarme una prueba” envía allí el resumen de hoy en ese momento.
- Límites. Como máximo 5 mensajes al día. No hay alertas entre las 9 p. m. y las 7 a. m. en su tienda; lo que siga siendo cierto sale por la mañana. Varias alertas a la vez llegan en un solo mensaje.
- Qué contiene un mensaje. Cantidades, nombres de máquinas y de insumos, y números de pedido. Nunca el nombre, el teléfono ni la dirección de un cliente.
- Idioma. Inglés o español, a su elección.

Su tienda necesita tener su zona horaria en Configuración › Negocio, para que el resumen llegue en su mañana. La tarjeta también permite elegir mensajes de texto; hasta que se enciendan los mensajes de texto para propietarios, esos también llegan a su correo, y la tarjeta lo dice.

## Si alguien más entró: Si cree que alguien más entró.

Haga esto en orden.

- Paso 1. Abra Configuración › Asistentes y quite cualquier conexión que no reconozca. Si no está seguro de cuál, primero pause todas.
- Paso 2. Cambie su contraseña. Esto desconecta todos los asistentes que usted conectó, así que tendrá que volver a conectar los que quiera.
- Paso 3. Revise la lista de actividad para ver qué se preguntó.
- Paso 4. Escriba a [contact@foldpos.com](mailto:contact@foldpos.com) y díganos el nombre de su tienda.

El cambio de su contraseña no afecta a los asistentes que conectó otro propietario de la tienda. Quítelos de la lista.

## Preguntas sobre los asistentes

**¿Cuesta extra?** No. No depende de un plan. Dos de las cosas que un asistente puede mirar dependen de su plan: las recogidas y entregas, y los turnos del personal.

**¿Puede configurarlo mi gerente?** No. Solo un propietario puede conectar un asistente, ver la lista o quitar uno.

**¿Puede Fold conectar un asistente por mí?** No. Una persona del equipo de Fold que le ayude desde nuestro lado puede pausar los asistentes o quitar uno, pero no puede conectar uno ni encender los cambios. Eso tiene que hacerlo usted, con su propia sesión.

**¿En qué idioma responde?** Su asistente responde en el idioma en que usted le escribe. La información que recibe de Fold POS está en inglés.

**¿Mis clientes también pueden usar un asistente?** Aparte de todo esto, el asistente de un cliente puede reservar una recogida en una tienda que tenga activadas las reservas en línea. Sigue las mismas reglas que su página de reservas, y la campana le avisa cuando una reserva llegó así.

## Para seguir

- [Para desarrolladores](https://foldpos.com/es/developers#store-mcp): La dirección, las herramientas y las reglas.
- [Hey Fold](https://foldpos.com/es/hey-fold#briefings): Pregunte “¿qué necesita mi atención?” en voz alta en Fold POS.
- [Reservas en línea](https://foldpos.com/es/pickup-delivery#booking): La página de reservas que usan sus clientes.
- [Centro de ayuda](https://foldpos.com/es/help): Respuestas cortas para el mostrador.

## Más

- [Inicio](/es/fold-pos.md) · [Precios](/es/pricing.md) · [Preguntas frecuentes](/es/faq.md) · [Ayuda](/es/help.md) · [Contacto](/es/contact.md) · [Nosotros](/es/about.md)
- [Impresoras](/es/printers.md) · [Configuración de la tienda](/setup.md) · [Asistente de impresión](/es/download.md) · [Todas las funciones](/es/features.md) · [Desarrolladores e IA](/es/developers.md)
- [Hey Fold](/es/hey-fold.md) · [Recogida y entrega](/es/pickup-delivery.md) · [El dinero en el mostrador](/es/counter-money.md) · [Plantas y tiendas de recepción](/es/plants.md)
