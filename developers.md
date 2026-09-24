# Fold POS for developers and AI agents

> Canonical page: https://foldpos.com/developers · Markdown mirror.

Fold POS is point of sale and operations software for laundromats, dry cleaners and tailors, built by Fold Laundry. This page is the machine-readable entrance: a site map for language models, markdown copies of every page, and a public MCP server that answers questions about the product. Everything here is read-only and public; nothing needs an account.

## llms.txt and llms-full.txt

- [/llms.txt](https://foldpos.com/llms.txt) — a short index: what Fold POS is, and a linked list of every page with a one-line description.
- [/llms-full.txt](https://foldpos.com/llms-full.txt) — the readable content of the entire site in one markdown document: shop types, features, Hey Fold, printing and hardware, pricing, switching over, and how to get started.

## Markdown mirrors

Every public page has a markdown twin with the navigation, styling and marketing chrome stripped out. Each HTML page points at its twin with `<link rel="alternate" type="text/markdown">`.

Every page also has a Spanish version under `/es/` with its own markdown twin: `/es/fold-pos.md`, `/es/pricing.md`, `/es/faq.md` and so on (the full list is on https://foldpos.com/es/developers).

| Page | Markdown |
| --- | --- |
| Home | `/fold-pos.md` |
| For laundromats | `/laundromats.md` |
| For dry cleaners | `/dry-cleaners.md` |
| For tailors | `/alterations.md` |
| All features | `/features.md` |
| Pricing | `/pricing.md` |
| FAQ | `/faq.md` |
| Help center | `/help.md` |
| Printers | `/printers.md` |
| Contact | `/contact.md` |
| About | `/about.md` |
| Store setup | `/setup.md` |
| Print helper | `/download.md` |
| This page | `/developers.md` |

## The Fold POS MCP server

A public Model Context Protocol server answers product questions for agents, so a model does not have to scrape the site to get the pricing or the printer list right.

- **Endpoint:** `https://app.foldpos.com/v1/mcp`
- **Server card:** `https://foldpos.com/.well-known/mcp.json`
- **Transport:** Streamable HTTP
- **Auth:** none — it is public
- **Scope:** read-only. It returns product information only; there is no store, customer or order data behind it.

### Tools

| Tool | Returns |
| --- | --- |
| `about_fold_pos` | What Fold POS is and who it is for. |
| `pricing_plans` | Starter, Growth and Pro, what each includes, and the 14-day free trial. Optional `language`: `en` or `es`. |
| `features` | Features by area and by shop type. |
| `availability` | Where Fold POS can be used (the Americas), languages, and billing in USD. Optional `country`. |
| `supported_hardware` | Receipt and tag printers, scanners, and the platforms the POS runs on. |
| `switching_from` | What comes over from Cents, CleanCloud or a CSV. |
| `getting_started` | Trial signup, the store setup guide and the print helper. |
| `faq` | The FAQ in English or Spanish, optionally filtered by a `query`. |
| `site_page` | Any page of foldpos.com as markdown, in English or Spanish. |
| `contact` | How to reach the Fold POS team. |

Resources: `foldpos://llms.txt`, `foldpos://llms-full.txt`, and every page as `foldpos://pages/{language}/{page}.md`. Prompts: `recommend_plan` and `explain_fold_pos_es`.

### Claude Code and Claude Desktop

```
claude mcp add --transport http fold-pos https://app.foldpos.com/v1/mcp
```

### Other MCP clients

Clients that take a JSON config want the same two facts — the transport and the URL:

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

## The store-owner API

The API that reaches a store's own customers, orders and reporting is **private**. It is not part of the public MCP server and has no public documentation. If you are a Fold POS customer or a partner who needs programmatic access to a store's data, email contact@foldpos.com and tell us what you are building.

Delivery marketplaces are a separate path: Fold, Laundryheap and Rinse connect from inside the POS — turn the partner on, give them the API key, and their jobs land in the store's schedule with status updates flowing back.

## More

- [Home](/fold-pos.md) · [All features](/features.md) · [Pricing](/pricing.md) · [FAQ](/faq.md)
