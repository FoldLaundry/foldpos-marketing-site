# Fold POS for developers and AI agents

> Canonical page: https://foldpos.com/developers · Markdown mirror.

Fold POS is point of sale and operations software for laundromats, dry cleaners and tailors, built by Fold Laundry. This page is the machine-readable entrance: a site map for language models, markdown copies of every page, and a public MCP server that answers questions about the product. Two more MCP servers are for people’s own AI assistants: one for a store owner, and one for a customer booking a pickup. The files and the public MCP server are read-only and need no account. The store server needs the owner’s sign-in or a token. The booking server needs no sign-in, only a code texted to the customer’s phone.

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
| `availability` | Where Fold POS can be used (the Americas, except Cuba), languages, and billing in USD. Optional `country`. |
| `supported_hardware` | Receipt and tag printers, scanners, and the platforms the POS runs on. |
| `switching_from` | What comes over from Cents, CleanCloud or a CSV. |
| `getting_started` | Trial signup, the store setup guide and the print helper. |
| `faq` | The FAQ in English or Spanish, optionally filtered by a `query`. |
| `site_page` | Any page of foldpos.com as markdown, in English or Spanish. |
| `contact` | How to reach the Fold POS team. |

Resources: `foldpos://llms.txt`, `foldpos://llms-full.txt`, and every page as `foldpos://pages/{language}/{page}.md`. Prompts: `recommend_plan` and `explain_fold_pos_es`.

The endpoint is for AI apps, not for a browser. Opening it in a browser brings you back to the developers page.

### Claude (claude.ai and the desktop app)

1. Open **Settings › Connectors** and choose **Add custom connector**.
2. Name it **Fold POS** and paste `https://app.foldpos.com/v1/mcp` as the URL. Leave the sign-in fields empty: it needs no login.
3. In a new chat, ask something like "How much does Fold POS cost for two dry cleaning locations?"

### Claude Code

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

## The store server: an owner’s own assistant

A second Model Context Protocol server lets a store owner’s own AI assistant, such as Claude, answer questions about one store: sales, orders, customers, machines, supplies, pickups and deliveries, and staff. It only looks, unless the owner switches on three small changes.

**Who it is for:** the owner of a store on Fold POS, and the people who build the assistants owners use. Only an owner can connect an assistant. Staff cannot.

- Endpoint: `https://app.foldpos.com/v1/mcp/store`
- Transport: HTTP (`"type": "http"` in a client’s config). Each request stands on its own; there is no session.
- Auth: required. The owner signs in and approves inside Fold POS (OAuth 2.1 with PKCE), or sends a personal token as a Bearer header.
- Scope: one store. Look-only by default.

### Connect by signing in

1. In your assistant’s settings, add a custom connector (some call it an MCP server) with this address: `https://app.foldpos.com/v1/mcp/store`
2. The assistant sends you to Fold POS. Sign in the way you always do.
3. Fold POS shows the name of the app, where you will be sent back to, and the store. Choose whether the assistant may make changes, then approve.

For client builders: a call with no token gets a 401 whose `WWW-Authenticate` header names the discovery document. Clients register themselves at `/v1/oauth/register`, PKCE with S256 is mandatory, the scopes are `read` and `write`, and an access token lasts one hour and is renewed with a refresh token.

### Connect with a token

Some apps ask for a token instead. The owner creates one in Fold POS under **Settings › Assistants**, and it is shown once. The assistant sends it as a Bearer header:

```
Authorization: Bearer fpos_pat_…
```

Clients that take a JSON config:

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

Treat a token like a password. Anyone who has it can read the store’s orders, customers and sales.

### Tools

Sixteen tools: thirteen that read and three that change something. A look-only connection is not shown the three that change.

| Tool | What it answers |
| --- | --- |
| `store_overview` | Which store this is: name, what it does, time zone and today’s date there, currency, plan, and whether this connection may change anything. |
| `today` | One day in one answer: sales and how they were paid, orders taken in, due and late, orders waiting, stops, machine income, who is clocked in. |
| `needs_attention` | The short list of what needs somebody, most pressing first. |
| `find_orders` | Orders by customer, state or date. |
| `order_detail` | One order in full: customer, lines, money, payments, where it is, tagged pieces, notes and messages. |
| `ready_not_picked_up` | Finished orders still waiting for the customer, longest wait first. |
| `find_customers` | Customers by name, phone or email, or a list by recency, name or spend. |
| `customer_detail` | One customer in full: contact details, totals, store credit, preferences, addresses, last 5 orders, last 10 staff notes. |
| `sales_report` | Sales over a period: totals, refunds, by service, by payment type, sales tax, day by day. |
| `machines` | Counts, what is out of service, what is running, maintenance due, open repair requests. |
| `supplies_low` | Supplies at or below their minimum, and what to reorder. |
| `deliveries` | One day’s pickup and delivery stops: routes, drivers, every stop in order, stops on no route. Needs pickup & delivery on the store’s plan. |
| `staff_on_shift` | Who is clocked in, on a break, late, scheduled, done or missed, and hours per person over a range. Needs staff shifts on the store’s plan. |
| `mark_order_ready` | A change. Marks one order ready, as the Ready button on the Orders screen does. |
| `add_order_note` | A change. Adds an internal staff note to one order. |
| `add_customer_note` | A change. Adds a staff note to one customer’s file. |

Every answer is a short summary followed by the same facts as JSON. A tool that fails says so. It never answers with a zero or an empty list in place of something it could not read. The tools answer in English; the assistant is asked to answer in the language of the person it works for.

### Safety rules

- **Owner only.** Only an owner can connect an assistant, see the list or remove one.
- **Look-only by default.** Changes are off until the owner switches them on, and each assistant also needs the owner’s permission to make them.
- **Changes are previewed first.** The first call describes the change and changes nothing. The change is made only when the assistant calls again with the code from the preview. The code works once, for five minutes.
- **Money never moves.** No tool charges, refunds, discounts, pays out, cancels, deletes, sends a message of its own or changes a setting.
- **An activity list.** Every question and every change shows in the owner’s activity list, kept for 90 days. The answers are not kept.
- **Pause or remove at any time.** One switch pauses every assistant. A removed connection stops working straight away.
- **Personal details.** In lists, customers’ phone numbers and emails are partly hidden. Card numbers are never shown; Fold POS does not store them.

For store owners: [Connect an AI assistant to your store](https://foldpos.com/assistants).

The endpoint is for AI apps, not for a browser. Opening it in a browser brings you back to this section.

## The booking server: a customer’s own assistant

A third server lets a customer’s own AI assistant book a laundry pickup with a shop that has online booking switched on. It does what the shop’s booking page does, with the same rules, times and prices.

**Who it is for:** customers of shops that run on Fold POS, and the people who build the assistants they use. Only shops with online booking switched on can be reached.

- Endpoint: `https://app.foldpos.com/v1/mcp/book`
- Transport: HTTP (`"type": "http"` in a client’s config). Each request stands on its own; there is no session.
- Auth: none. There is no sign-in, like the booking page. Nothing is written until the customer proves their phone with a texted code.
- Payment: nothing is charged at booking. The customer pays the shop when the order is collected or delivered.

### Connect

1. In your assistant’s settings, add a custom connector (some call it an MCP server) with this address: `https://app.foldpos.com/v1/mcp/book`
2. It needs no login.
3. Ask the assistant to book a pickup. The shop texts a 6-digit code to your phone. Read it to the assistant to confirm the booking.

Clients that take a JSON config:

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

### Tools

Ten tools.

| Tool | What it does |
| --- | --- |
| `find_shop` | Finds shops that take bookings, by name, town, ZIP or booking name. Up to 5. |
| `shop_info` | Name, phone, address, hours, services, how far ahead it books, delivery fee, free-delivery amount, minimum order, how payment works. |
| `pickup_times` | Free pickup times at an address, after checking the address is in the shop’s area. |
| `return_options` | When the order will be ready and which delivery times go with a pickup time. |
| `send_booking_code` | Asks the shop to text a 6-digit code to the customer’s phone. |
| `book_pickup` | Makes the booking. Needs the code. |
| `my_booking` | A booking’s times, and whether it can still be moved or cancelled here. |
| `booking_move_times` | The times a booking can move to. |
| `move_booking` | Moves a booking. |
| `cancel_booking` | Cancels a booking. |

### Safety rules

- **The code from the customer’s phone.** A booking needs the 6-digit code the shop texts. Only the person holding the phone can read it out. A code lasts 10 minutes.
- **Nothing is charged.** The customer pays the shop when the order is collected or delivered.
- **Only shops that take bookings.** A shop with online booking switched off cannot be reached.
- **The shop is told at once.** A new booking shows under the bell at the counter, marked as booked through an assistant.
- **A failure is a failure.** A tool that fails says so. It is never shown as “no times available”.

For store owners: [Can my customers use an assistant too?](https://foldpos.com/assistants#questions) and [how online booking works](https://foldpos.com/pickup-delivery#booking).

The endpoint is for AI apps, not for a browser. Opening it in a browser brings you back to this section.

## The store-owner API

The API that reaches a store's own customers, orders and reporting is **private**. It is not part of the public MCP server and has no public documentation. A store owner’s own AI assistant does not use it: it connects through the store server above. If you are a Fold POS customer or a partner who needs programmatic access to a store's data, email contact@foldpos.com and tell us what you are building.

Delivery marketplaces are a separate path: Fold, Laundryheap and Rinse connect from inside the POS — turn the partner on, give them the API key, and their jobs land in the store's schedule with status updates flowing back.

## More

- [Home](/fold-pos.md) · [All features](/features.md) · [Pricing](/pricing.md) · [FAQ](/faq.md)
