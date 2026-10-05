# Fold POS para desarrolladores y agentes de IA

> Página canónica: https://foldpos.com/es/developers · Espejo en markdown.

Fold POS es un software de punto de venta (POS) y operaciones para lavanderías, tintorerías y sastrerías, creado por Fold Laundry. Esta página es la entrada legible por máquinas: un mapa del sitio para modelos de lenguaje, copias en markdown de cada página y un servidor MCP público que responde preguntas sobre el producto. Hay dos servidores MCP más, para los asistentes de IA de cada persona: uno para el propietario de una tienda y otro para un cliente que reserva una recogida. Los archivos y el servidor MCP público son de solo lectura y no requieren una cuenta. El servidor de la tienda requiere el inicio de sesión del propietario o un token. El servidor de reservas no requiere inicio de sesión, solo un código que el cliente recibe por mensaje de texto.

## llms.txt y llms-full.txt

- [/llms.txt](https://foldpos.com/llms.txt) — un índice breve: qué es Fold POS y una lista enlazada de todas las páginas, con una descripción de una línea.
- [/llms-full.txt](https://foldpos.com/llms-full.txt) — el contenido legible de todo el sitio en un solo documento markdown: tipos de negocio, funciones, Hey Fold, impresión y hardware, precios, cómo cambiarse desde otro sistema y cómo empezar.

## Espejos en markdown

Cada página pública tiene un gemelo en markdown, sin navegación, estilos ni elementos de marketing. Cada página HTML apunta a su gemelo con `<link rel="alternate" type="text/markdown">`.

| Página | Markdown |
| --- | --- |
| Inicio | `/fold-pos.md` |
| Para lavanderías | `/laundromats.md` |
| Para tintorerías | `/dry-cleaners.md` |
| Para sastrerías | `/alterations.md` |
| Todas las funciones | `/features.md` |
| Precios | `/pricing.md` |
| Preguntas frecuentes | `/faq.md` |
| Centro de ayuda | `/help.md` |
| Impresoras | `/printers.md` |
| Contacto | `/contact.md` |
| Nosotros | `/about.md` |
| Configuración de la tienda | `/setup.md` |
| Asistente de impresión | `/download.md` |
| Esta página | `/developers.md` |
| Inicio (español) | `/es/fold-pos.md` |
| Para lavanderías (español) | `/es/laundromats.md` |
| Para tintorerías (español) | `/es/dry-cleaners.md` |
| Para sastrerías (español) | `/es/alterations.md` |
| Todas las funciones (español) | `/es/features.md` |
| Precios (español) | `/es/pricing.md` |
| Preguntas frecuentes (español) | `/es/faq.md` |
| Centro de ayuda (español) | `/es/help.md` |
| Impresoras (español) | `/es/printers.md` |
| Contacto (español) | `/es/contact.md` |
| Nosotros (español) | `/es/about.md` |
| Asistente de impresión (español) | `/es/download.md` |
| Esta página (español) | `/es/developers.md` |

## El servidor MCP de Fold POS

Un servidor público de Model Context Protocol responde preguntas sobre el producto a los agentes, para que un modelo no tenga que extraer datos del sitio para acertar con los precios o la lista de impresoras.

- **Endpoint:** `https://app.foldpos.com/v1/mcp`
- **Ficha del servidor:** `https://foldpos.com/.well-known/mcp.json`
- **Transporte:** Streamable HTTP
- **Autenticación:** ninguna, es público
- **Alcance:** solo lectura. Devuelve únicamente información del producto; no hay datos de tiendas, clientes ni pedidos detrás.

### Herramientas

| Herramienta | Devuelve |
| --- | --- |
| `about_fold_pos` | Qué es Fold POS y para quién es. |
| `pricing_plans` | Starter, Growth y Pro, qué incluye cada uno y la prueba gratis de 14 días. `language` opcional: `en` o `es`. |
| `features` | Funciones por área y por tipo de negocio. |
| `availability` | Dónde se puede usar Fold POS (el continente americano, excepto Cuba), idiomas y cobro en USD. `country` opcional. |
| `supported_hardware` | Impresoras de recibos y de etiquetas, escáneres y las plataformas en las que funciona el POS. |
| `switching_from` | Qué se trae desde Cents, CleanCloud o un CSV. |
| `getting_started` | Registro para la prueba gratis, la guía de configuración de la tienda y el asistente de impresión. |
| `faq` | Las preguntas frecuentes en inglés o español, con un filtro `query` opcional. |
| `site_page` | Cualquier página de foldpos.com en markdown, en inglés o español. |
| `contact` | Cómo contactar al equipo de Fold POS. |

Recursos: `foldpos://llms.txt`, `foldpos://llms-full.txt` y cada página como `foldpos://pages/{language}/{page}.md`. Prompts: `recommend_plan` y `explain_fold_pos_es`.

El endpoint es para apps de IA, no para el navegador. Si lo abre en el navegador, vuelve a la página para desarrolladores.

### Claude (claude.ai y la app de escritorio)

1. Abra **Settings › Connectors** (Configuración › Conectores) y elija **Add custom connector** (Agregar conector personalizado).
2. Póngale el nombre **Fold POS** y pegue `https://app.foldpos.com/v1/mcp` como URL. Deje vacíos los campos de inicio de sesión: no necesita cuenta.
3. En un chat nuevo, pregunte algo como "¿Puedo usar Fold POS en México?"

### Claude Code

```
claude mcp add --transport http fold-pos https://app.foldpos.com/v1/mcp
```

### Otros clientes MCP

Los clientes que usan una configuración JSON necesitan los mismos dos datos, el transporte y la URL:

```json
{
  "mcpServers": {
    "fold-pos": {
      "type": "http",
      "url": "https://app.foldpos.com/v1/mcp"
    }
  }
}
```

## El servidor de la tienda: el asistente del propietario

Un segundo servidor de Model Context Protocol permite que el asistente de IA del propietario de una tienda, como Claude, responda preguntas sobre una tienda: ventas, pedidos, clientes, máquinas, insumos, recogidas y entregas, y personal. Solo mira, salvo que el propietario encienda tres cambios pequeños.

**Para quién es:** el propietario de una tienda en Fold POS y quienes crean los asistentes que usan los propietarios. Solo un propietario puede conectar un asistente. El personal no puede.

- Endpoint: `https://app.foldpos.com/v1/mcp/store`
- Transporte: HTTP (`"type": "http"` en la configuración del cliente). Cada solicitud es independiente; no hay sesión.
- Autenticación: obligatoria. El propietario inicia sesión y aprueba dentro de Fold POS (OAuth 2.1 con PKCE), o envía un token personal como encabezado Bearer.
- Alcance: una sola tienda. De solo lectura de forma predeterminada.

### Conectar iniciando sesión

1. En la configuración de su asistente, agregue un conector personalizado (algunos lo llaman servidor MCP) con esta dirección: `https://app.foldpos.com/v1/mcp/store`
2. El asistente lo envía a Fold POS. Inicie sesión como siempre.
3. Fold POS muestra el nombre de la app, adónde regresará usted y la tienda. Elija si el asistente puede hacer cambios y luego apruebe.

Para quienes crean clientes: una llamada sin token recibe un 401 cuyo encabezado `WWW-Authenticate` indica el documento de descubrimiento. Los clientes se registran solos en `/v1/oauth/register`, PKCE con S256 es obligatorio, los alcances son `read` y `write`, y un token de acceso dura una hora y se renueva con un token de actualización.

### Conectar con un token

Algunas apps piden un token. El propietario lo crea en Fold POS, en **Configuración › Asistentes**, y se muestra una sola vez. El asistente lo envía como encabezado Bearer:

```
Authorization: Bearer fpos_pat_…
```

Para los clientes que usan una configuración JSON:

```json
{
  "mcpServers": {
    "fold-pos-store": {
      "type": "http",
      "url": "https://app.foldpos.com/v1/mcp/store",
      "headers": { "Authorization": "Bearer fpos_pat_…" }
    }
  }
}
```

Trate un token como una contraseña. Quien lo tenga puede leer los pedidos, los clientes y las ventas de la tienda.

### Herramientas

Dieciséis herramientas: trece que leen y tres que cambian algo. Una conexión de solo lectura no ve las tres que cambian.

| Herramienta | Qué responde |
| --- | --- |
| `store_overview` | Qué tienda es: nombre, a qué se dedica, zona horaria y la fecha de hoy allí, moneda, plan y si esta conexión puede cambiar algo. |
| `today` | Un día en una sola respuesta: ventas y cómo se pagaron, pedidos recibidos, por entregar y atrasados, pedidos en espera, paradas, ingresos de las máquinas y quién marcó entrada. |
| `needs_attention` | La lista corta de lo que necesita a alguien, primero lo más urgente. |
| `find_orders` | Pedidos por cliente, estado o fecha. |
| `order_detail` | Un pedido completo: cliente, líneas, importes, pagos, dónde está, piezas etiquetadas, notas y mensajes. |
| `ready_not_picked_up` | Pedidos terminados que siguen esperando al cliente, primero el que más lleva. |
| `find_customers` | Clientes por nombre, teléfono o correo, o una lista por fecha reciente, nombre o gasto. |
| `customer_detail` | Un cliente completo: datos de contacto, totales, crédito de tienda, preferencias, direcciones, los últimos 5 pedidos y las últimas 10 notas del personal. |
| `sales_report` | Ventas de un periodo: totales, reembolsos, por servicio, por forma de pago, impuesto sobre las ventas y día por día. |
| `machines` | Conteos, qué está fuera de servicio, qué está en uso, mantenimiento pendiente y solicitudes de reparación abiertas. |
| `supplies_low` | Insumos en su mínimo o por debajo, y qué volver a pedir. |
| `deliveries` | Las paradas de recogida y entrega de un día: rutas, repartidores, cada parada en orden y las paradas sin ruta. Necesita recogida y entrega en el plan de la tienda. |
| `staff_on_shift` | Quién marcó entrada, está en descanso, llegó tarde, está programado, terminó o faltó, y las horas por persona en un periodo. Necesita turnos del personal en el plan de la tienda. |
| `mark_order_ready` | Un cambio. Marca un pedido como listo, igual que el botón Listo de la pantalla Pedidos. |
| `add_order_note` | Un cambio. Agrega una nota interna del personal a un pedido. |
| `add_customer_note` | Un cambio. Agrega una nota del personal al expediente de un cliente. |

Cada respuesta es un resumen corto seguido de los mismos datos en JSON. Una herramienta que falla lo dice. Nunca responde con un cero o una lista vacía en lugar de algo que no pudo leer. Las herramientas responden en inglés; al asistente se le pide responder en el idioma de la persona para quien trabaja.

### Reglas de seguridad

- **Solo el propietario.** Solo un propietario puede conectar un asistente, ver la lista o quitar uno.
- **De solo lectura de forma predeterminada.** Los cambios están apagados hasta que el propietario los enciende, y cada asistente necesita además el permiso del propietario para hacerlos.
- **Los cambios se muestran antes.** La primera llamada describe el cambio y no cambia nada. El cambio se hace solo cuando el asistente vuelve a llamar con el código de la vista previa. El código sirve una vez, durante cinco minutos.
- **El dinero nunca se mueve.** Ninguna herramienta cobra, reembolsa, descuenta, paga, cancela, elimina, envía un mensaje por su cuenta ni cambia una configuración.
- **Una lista de actividad.** Cada pregunta y cada cambio aparece en la lista de actividad del propietario, que se conserva 90 días. Las respuestas no se guardan.
- **Pausar o quitar en cualquier momento.** Un interruptor pausa todos los asistentes. Una conexión que se quita deja de funcionar de inmediato.
- **Datos personales.** En las listas, los teléfonos y correos de los clientes aparecen parcialmente ocultos. Los números de tarjeta nunca se muestran; Fold POS no los guarda.

Para propietarios de tiendas: [Conecte un asistente de IA a su tienda](https://foldpos.com/es/assistants).

El endpoint es para apps de IA, no para el navegador. Si lo abre en el navegador, vuelve a esta sección.

## El servidor de reservas: el asistente del cliente

Un tercer servidor permite que el asistente de IA de un cliente reserve una recogida de ropa en una tienda que tenga activadas las reservas en línea. Hace lo mismo que la página de reservas de la tienda, con las mismas reglas, horarios y precios.

**Para quién es:** los clientes de las tiendas que trabajan con Fold POS y quienes crean los asistentes que ellos usan. Solo se puede llegar a las tiendas que tienen activadas las reservas en línea.

- Endpoint: `https://app.foldpos.com/v1/mcp/book`
- Transporte: HTTP (`"type": "http"` en la configuración del cliente). Cada solicitud es independiente; no hay sesión.
- Autenticación: ninguna. No hay inicio de sesión, igual que en la página de reservas. No se guarda nada hasta que el cliente comprueba su teléfono con un código que recibe por mensaje de texto.
- Pago: no se cobra nada al reservar. El cliente le paga a la tienda cuando recoge el pedido o cuando se lo entregan.

### Conectar

1. En la configuración de su asistente, agregue un conector personalizado (algunos lo llaman servidor MCP) con esta dirección: `https://app.foldpos.com/v1/mcp/book`
2. No necesita inicio de sesión.
3. Pídale al asistente que reserve una recogida. La tienda envía un código de 6 dígitos a su teléfono por mensaje de texto. Dígaselo al asistente para confirmar la reserva.

Para los clientes que usan una configuración JSON:

```json
{
  "mcpServers": {
    "fold-pos-booking": {
      "type": "http",
      "url": "https://app.foldpos.com/v1/mcp/book"
    }
  }
}
```

### Herramientas

Diez herramientas.

| Herramienta | Qué hace |
| --- | --- |
| `find_shop` | Busca tiendas que aceptan reservas, por nombre, ciudad, código postal o nombre de reserva. Hasta 5. |
| `shop_info` | Nombre, teléfono, dirección, horario, servicios, con cuánta anticipación reserva, cargo de entrega, importe para entrega gratis, pedido mínimo y cómo se paga. |
| `pickup_times` | Horarios de recogida libres en una dirección, después de comprobar que la dirección está en el área de la tienda. |
| `return_options` | Cuándo estará listo el pedido y qué horarios de entrega corresponden a un horario de recogida. |
| `send_booking_code` | Le pide a la tienda que envíe un código de 6 dígitos al teléfono del cliente por mensaje de texto. |
| `book_pickup` | Hace la reserva. Necesita el código. |
| `my_booking` | Los horarios de una reserva, y si todavía se puede mover o cancelar aquí. |
| `booking_move_times` | Los horarios a los que se puede mover una reserva. |
| `move_booking` | Mueve una reserva. |
| `cancel_booking` | Cancela una reserva. |

### Reglas de seguridad

- **El código del teléfono del cliente.** Una reserva necesita el código de 6 dígitos que envía la tienda. Solo quien tiene el teléfono en la mano puede leerlo. Un código dura 10 minutos.
- **No se cobra nada.** El cliente le paga a la tienda cuando recoge el pedido o cuando se lo entregan.
- **Solo tiendas que aceptan reservas.** No se puede llegar a una tienda que tiene apagadas las reservas en línea.
- **La tienda se entera de inmediato.** Una reserva nueva aparece bajo la campana en el mostrador, marcada como hecha por medio de un asistente.
- **Una falla es una falla.** Una herramienta que falla lo dice. Nunca se presenta como “no hay horarios disponibles”.

Para propietarios de tiendas: [¿Mis clientes también pueden usar un asistente?](https://foldpos.com/es/assistants#questions) y [cómo funcionan las reservas en línea](https://foldpos.com/es/pickup-delivery#booking).

El endpoint es para apps de IA, no para el navegador. Si lo abre en el navegador, vuelve a esta sección.

## La API para dueños de tienda

La API que accede a los clientes, pedidos e informes de una tienda es **privada**. No forma parte del servidor MCP público y no tiene documentación pública. El asistente de IA del propietario de una tienda no la usa: se conecta por el servidor de la tienda, más arriba. Si es cliente de Fold POS o un socio que necesita acceso programático a los datos de una tienda, escriba a contact@foldpos.com y cuéntenos qué está creando.

Los marketplaces de entrega son un camino aparte: Fold, Laundryheap y Rinse se conectan desde el propio POS. Active al socio, entréguele la clave de API y sus trabajos llegan a la agenda de la tienda, con actualizaciones de estado de ida y vuelta.

## Más

- [Inicio](/es/fold-pos.md) · [Todas las funciones](/es/features.md) · [Precios](/es/pricing.md) · [Preguntas frecuentes](/es/faq.md)
