# Fold POS para desarrolladores y agentes de IA

> Página canónica: https://foldpos.com/es/developers · Espejo en markdown.

Fold POS es un software de punto de venta (POS) y operaciones para lavanderías, tintorerías y sastrerías, creado por Fold Laundry. Esta página es la entrada legible por máquinas: un mapa del sitio para modelos de lenguaje, copias en markdown de cada página y un servidor MCP público que responde preguntas sobre el producto. Todo lo que hay aquí es público y de solo lectura; nada requiere una cuenta.

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
| `availability` | Dónde se puede usar Fold POS (el continente americano), idiomas y cobro en USD. `country` opcional. |
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

## La API para dueños de tienda

La API que accede a los clientes, pedidos e informes de una tienda es **privada**. No forma parte del servidor MCP público y no tiene documentación pública. Si es cliente de Fold POS o un socio que necesita acceso programático a los datos de una tienda, escriba a contact@foldpos.com y cuéntenos qué está creando.

Los marketplaces de entrega son un camino aparte: Fold, Laundryheap y Rinse se conectan desde el propio POS. Active al socio, entréguele la clave de API y sus trabajos llegan a la agenda de la tienda, con actualizaciones de estado de ida y vuelta.

## Más

- [Inicio](/es/fold-pos.md) · [Todas las funciones](/es/features.md) · [Precios](/es/pricing.md) · [Preguntas frecuentes](/es/faq.md)
