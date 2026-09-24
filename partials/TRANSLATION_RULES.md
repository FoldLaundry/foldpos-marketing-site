# Rules for the Spanish (es) versions of foldpos.com pages

Audience: laundromat, dry-cleaner (tintorería / lavandería / lavaseco) and tailor (sastrería / arreglos de ropa) OWNERS across Latin America, Mexico and the US Hispanic market. Write neutral Latin American Spanish, formal "usted" (the app's Spanish uses usted: "Inicie sesión"). Natural, short, confident — the English copy is deliberately terse; keep that. Do not translate word for word when it reads stiff.

Terminology (use consistently):
- laundromat → lavandería (autoservicio when it means self-service); wash & fold → lavado y doblado (por libra/kilo only as in source: keep "por libra" where the source says pound)
- dry cleaner → tintorería (you may add "tintorerías y lavanderías" in titles/meta for SEO); dry cleaning → lavado en seco / tintorería
- tailor / alterations → sastrería / arreglos de ropa
- counter → mostrador; ticket → ticket; tag (garment tag) → etiqueta; heat-seal tag → etiqueta termoadhesiva; rack/conveyor → rack / transportador
- pickup & delivery → recogida y entrega; driver → repartidor / conductor; courier (Uber Direct) → mensajero de Uber Direct
- point of sale / POS → punto de venta (POS)
- "Start free" → "Empiece gratis"; "Log in" → "Iniciar sesión"; free trial → prueba gratis
Never translate: Fold POS, Fold, Fold Laundry, Hey Fold, Fold Driver, Uber Direct, Epson/Star/Bixolon/Zebra, Cents, CleanCloud, Chrome/Edge/Safari/Firefox, Caps Lock (write "Bloq Mayús (Caps Lock)" the first time), code, URLs, email addresses, prices ($39 etc. stay in US dollars; say "dólares estadounidenses (USD)" once where pricing is explained).
App menu paths (e.g. "Settings › Receipts"): look up the exact Spanish label in /mnt/user-data/uploads/Developer/fold-pos-build/lib/l10n/arb/app_es.arb by finding the English value in app_en.arb with the same key. If you can't find it, translate naturally.

HTML rules:
- Translate ONLY human-visible text and text meant for people/search: element text, alt, title, aria-label, placeholder, <title>, meta description, og:title/og:description, twitter:title/description, JSON-LD human-readable values (name, description, text, question/answer, featureList). Keep every tag, class, id, data-attribute, inline style and script logic byte-for-byte otherwise.
- <html lang="en"> → lang="es". og:locale → es_419 (add it if missing).
- canonical and og:url → https://foldpos.com/es/<slug> (homepage: https://foldpos.com/es/). BreadcrumbList item URLs → the /es/ URLs, names translated.
- Internal links: rewrite href="/X" and href="X" (relative) to "/es/X" ONLY for these pages, which have Spanish versions: / (→ /es/), /pricing, /faq, /help, /contact, /about, /printers, /laundromats, /dry-cleaners, /alterations, /features, /developers, /download. Keep anchors (#...) as they are. Leave /setup, /privacy, /terms, /download/... files, .md, .txt, and external links (pos.foldpos.com etc.) unchanged.
- <link rel="alternate" type="text/markdown"> → /es/<slug>.md (homepage: /es/fold-pos.md), and WRITE that markdown file too: a faithful Spanish translation of the English .md mirror (fold-pos.md for home, <slug>.md otherwise), with its "Canonical page" line pointing to the /es/ URL and links pointing to /es/*.md where they exist.
- Asset paths: the Spanish file lives one folder deeper (/es/). Any RELATIVE src/href/url() to assets (e.g. "assets/img/..", "favicon-32.png") must become root-absolute ("/assets/img/..", "/favicon-32.png") so they still load.
- Do NOT touch anything between <!--fx:header--> ... <!--/fx:header--> or <!--fx:footer--> ... <!--/fx:footer--> (the Spanish header/footer are injected later). Do not add hreflang tags (added later).
- JavaScript: translate string literals that are shown to people. Do not change variable names, keys, ids, regexes or logic, except where a task says so.
- Do not invent facts, features, numbers, testimonials or country-specific claims that are not in the English page.

Deliverable check before you finish: the file parses (python3 -c "import html.parser" is not enough — load it in Playwright/Chromium: `python3` + `playwright` are installed) with no JS page errors; no leftover English sentences in visible text (brand names excepted); all rewritten internal links point to pages in the list above.

## Maintaining the Spanish pages

- The Spanish pages in es/ are static files: build_pages.py and build_site.py do not regenerate their content. When an English page changes, make the same change in es/<page>.html and es/<page>.md.
- build_site.py does put the Spanish header and footer (partials/header.es.html, partials/footer.es.html) on es/*.html, adds the hreflang en/es/x-default links, og:locale, the JSON-LD languages and regions, and rewrites sitemap.xml with both languages.
- check_seo.py checks es/ like the English pages, plus hreflang reciprocity and the sitemap entries.
- The Spanish homepage uses its own hero loop (assets/video/fold-hero-ambient-es*), rendered from ambient.html?es.
