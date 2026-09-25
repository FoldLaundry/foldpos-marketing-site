#!/usr/bin/env python3
"""Check the SEO / agent-readability invariants of the foldpos.com static site.

Run from the repository root:  python3 check_seo.py

It checks, for every .html file in the repo:
  * a non-empty <title> and <meta name="description">, both unique across pages
  * a <link rel="canonical"> in clean-URL form that points at this page
  * Open Graph (og:title, og:description, og:image, og:url) and twitter:card
  * every <script type="application/ld+json"> block parses as JSON
  * every internal <a href> resolves to a file in the repo (clean URLs included)
  * the <link rel="alternate" type="text/markdown"> target exists
  * <html lang> matches the folder (es/ is Spanish), and a page with a translation
    carries hreflang en / es / x-default links that point back at each other

Spanish pages live in es/ and are checked the same way as the English ones.

and, site-wide:
  * every <loc> in sitemap.xml maps to a file that exists
  * robots.txt names the AI crawlers and points at the sitemap
  * llms.txt / llms-full.txt exist and the links inside llms.txt resolve

Exit status is 0 when everything passes, 1 otherwise.
"""
import json
import os
import re
import sys
import glob
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://foldpos.com'

# Files that live on the server but are not checked into this copy of the repo.
EXTERNAL_PREFIXES = ('assets/', 'download/')

AI_CRAWLERS = [
    'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-User',
    'Claude-SearchBot', 'anthropic-ai', 'PerplexityBot', 'Google-Extended',
    'Applebot-Extended', 'Bingbot', 'CCBot', 'Amazonbot', 'Meta-ExternalAgent',
    'cohere-ai', 'DuckAssistBot',
]

errors = []
notes = []


def err(where, msg):
    errors.append('%s: %s' % (where, msg))


class Page(HTMLParser):
    """Just enough HTML parsing for the head metadata, links and JSON-LD."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ''
        self._in_title = False
        self.meta = {}          # name/property -> content
        self.links = []         # (rel, href, type)
        self.hrefs = []         # <a href>
        self.jsonld = []
        self.lang = ''
        self.hreflang = {}      # hreflang -> href
        self._in_ld = False
        self._ld = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang', '')
        if tag == 'link' and a.get('hreflang') and a.get('rel', '').lower() == 'alternate':
            self.hreflang[a['hreflang']] = a.get('href', '')
        if tag == 'title':
            self._in_title = True
        elif tag == 'meta':
            key = a.get('name') or a.get('property')
            if key:
                self.meta[key.lower()] = a.get('content', '')
        elif tag == 'link':
            self.links.append((a.get('rel', '').lower(), a.get('href', ''), a.get('type', '')))
        elif tag == 'a' and 'href' in a:
            self.hrefs.append(a['href'])
        elif tag == 'script' and a.get('type', '').lower() == 'application/ld+json':
            self._in_ld = True
            self._ld = []

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
        elif tag == 'script' and self._in_ld:
            self.jsonld.append(''.join(self._ld))
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._ld.append(data)

    def link(self, rel):
        for r, href, _t in self.links:
            if r == rel:
                return href
        return None

    def alternate_md(self):
        for r, href, t in self.links:
            if r == 'alternate' and t == 'text/markdown':
                return href
        return None


def exists(relpath):
    return os.path.isfile(os.path.join(ROOT, relpath))


def resolve(target):
    """Map a site-relative path to a file in the repo, honouring nginx's
    try_files $uri $uri.html. Returns the file path, or None."""
    p = unquote(target).lstrip('/')
    if p in ('', '.'):
        p = 'index.html'
    if p.endswith('/'):
        p += 'index.html'
    for cand in (p, p + '.html', os.path.join(p, 'index.html')):
        if exists(cand):
            return cand
    return None


def canonical_for(fname):
    """The clean-URL canonical this file should declare."""
    if fname.endswith('index.html'):
        return SITE + '/' + fname[:-len('index.html')]
    return SITE + '/' + fname[:-len('.html')]


HREFLANG = {}   # fname -> {hreflang: href}, checked for reciprocity in main()


def check_page(fname):
    src = open(os.path.join(ROOT, fname), encoding='utf-8').read()
    p = Page()
    p.feed(src)

    want_lang = 'es' if fname.startswith('es/') else 'en'
    if not p.lang.startswith(want_lang):
        err(fname, '<html lang=%r>, expected %r' % (p.lang, want_lang))
    HREFLANG[fname] = p.hreflang

    title = p.title.strip()
    if not title:
        err(fname, 'missing <title>')
    desc = p.meta.get('description', '').strip()
    if not desc:
        err(fname, 'missing <meta name="description">')

    canon = p.link('canonical')
    if not canon:
        err(fname, 'missing <link rel="canonical">')
    else:
        want = canonical_for(fname)
        if canon != want:
            err(fname, 'canonical is %r, expected the clean URL %r' % (canon, want))

    for key in ('og:title', 'og:description', 'og:image', 'og:url', 'og:type'):
        if not p.meta.get(key):
            err(fname, 'missing <meta property="%s">' % key)
    if not p.meta.get('twitter:card'):
        err(fname, 'missing <meta name="twitter:card">')
    if canon and p.meta.get('og:url') and p.meta['og:url'] != canon:
        err(fname, 'og:url %r does not match canonical %r' % (p.meta['og:url'], canon))

    if not p.jsonld:
        err(fname, 'no JSON-LD on the page')
    for i, block in enumerate(p.jsonld):
        try:
            data = json.loads(block)
        except ValueError as e:
            err(fname, 'JSON-LD block %d does not parse: %s' % (i + 1, e))
            continue
        if '@type' not in data and '@graph' not in data:
            err(fname, 'JSON-LD block %d has no @type' % (i + 1))

    md = p.alternate_md()
    if md:
        if not exists(md.lstrip('/')):
            err(fname, 'markdown alternate %r does not exist' % md)
    elif fname not in ('privacy.html', 'terms.html', '404.html'):
        err(fname, 'missing <link rel="alternate" type="text/markdown">')

    for href in p.hrefs:
        u = urlsplit(href)
        if u.scheme or u.netloc:          # absolute / mailto: / tel:
            continue
        if not u.path:                    # pure #anchor
            continue
        rel = u.path.lstrip('/')
        if rel.startswith(EXTERNAL_PREFIXES):
            notes.append('%s: link to %s not checked (not in this repo copy)' % (fname, u.path))
            continue
        if resolve(u.path) is None:
            err(fname, 'link %r does not resolve to a file' % href)

    return title, desc


def main():
    os.chdir(ROOT)
    pages = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html')))
    pages += sorted('es/' + os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'es', '*.html')))
    # A page that only redirects (meta refresh, noindex) has no content to check.
    redirects = [f for f in pages if 'http-equiv="refresh"' in open(os.path.join(ROOT, f), encoding='utf-8').read()]
    for f in redirects:
        notes.append('%s: redirect page, skipped' % f)
    pages = [f for f in pages if f not in redirects]
    if not pages:
        err('repo', 'no .html files found')

    seen_titles, seen_descs = {}, {}
    for fname in pages:
        title, desc = check_page(fname)
        if title:
            if title in seen_titles:
                err(fname, 'duplicate <title>, also used by %s' % seen_titles[title])
            seen_titles[title] = fname
        if desc:
            if desc in seen_descs:
                err(fname, 'duplicate meta description, also used by %s' % seen_descs[desc])
            seen_descs[desc] = fname

    # ---- hreflang: every translated page names both languages and x-default, reciprocally ----
    for fname in pages:
        other = fname[3:] if fname.startswith('es/') else 'es/' + fname
        hl = HREFLANG.get(fname, {})
        if other not in pages:
            if hl:
                err(fname, 'has hreflang links but no translation file %s' % other)
            continue
        for key in ('en', 'es', 'x-default'):
            if key not in hl:
                err(fname, 'missing hreflang=%r (translation %s exists)' % (key, other))
        en, es = (other, fname) if fname.startswith('es/') else (fname, other)
        if hl.get('en') != canonical_for(en) or hl.get('es') != canonical_for(es):
            err(fname, 'hreflang en/es %r / %r do not match the canonicals of %s / %s' % (hl.get('en'), hl.get('es'), en, es))
        if hl.get('x-default') != canonical_for(en):
            err(fname, 'hreflang x-default should be the English page')
        if HREFLANG.get(other, {}) and HREFLANG[other].get('en') != hl.get('en'):
            err(fname, 'hreflang is not reciprocal with %s' % other)

    # ---- sitemap ----
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    if not os.path.isfile(sm_path):
        err('sitemap.xml', 'missing')
    else:
        sm = open(sm_path, encoding='utf-8').read()
        locs = re.findall(r'<loc>([^<]+)</loc>', sm)
        if not locs:
            err('sitemap.xml', 'no <loc> entries')
        for loc in locs:
            if not loc.startswith(SITE):
                err('sitemap.xml', '%s is not on %s' % (loc, SITE))
                continue
            if resolve(loc[len(SITE):]) is None:
                err('sitemap.xml', '%s does not map to a file' % loc)
        for alt in re.findall(r'<xhtml:link[^>]*href="([^"]+)"', sm):
            if not alt.startswith(SITE) or resolve(alt[len(SITE):]) is None:
                err('sitemap.xml', 'alternate %s does not map to a file' % alt)
        for f in pages:
            if canonical_for(f) not in locs and f not in ('setup.html', '404.html'):   # both noindex
                err('sitemap.xml', '%s (%s) is not listed' % (canonical_for(f), f))
        if 'setup' in [urlsplit(l).path.strip('/') for l in locs]:
            err('sitemap.xml', '/setup is noindex and must not be listed')
        for loc in locs:
            if '<lastmod>' not in sm:
                err('sitemap.xml', 'entries have no <lastmod>')
                break

    # ---- robots ----
    rb_path = os.path.join(ROOT, 'robots.txt')
    if not os.path.isfile(rb_path):
        err('robots.txt', 'missing')
    else:
        rb = open(rb_path, encoding='utf-8').read()
        if not re.search(r'(?mi)^User-agent:\s*\*\s*$', rb) or 'Allow: /' not in rb:
            err('robots.txt', 'does not keep "User-agent: *" / "Allow: /"')
        for bot in AI_CRAWLERS:
            if not re.search(r'(?mi)^User-agent:\s*%s\s*$' % re.escape(bot), rb):
                err('robots.txt', 'does not name %s' % bot)
        if 'sitemap.xml' not in rb:
            err('robots.txt', 'does not point at the sitemap')
        if 'llms.txt' not in rb:
            err('robots.txt', 'does not mention llms.txt')

    # ---- llms.txt ----
    for f in ('llms.txt', 'llms-full.txt'):
        if not exists(f):
            err(f, 'missing')
    if exists('llms.txt'):
        llms = open(os.path.join(ROOT, 'llms.txt'), encoding='utf-8').read()
        if not llms.startswith('# '):
            err('llms.txt', 'does not start with an H1')
        if '\n> ' not in llms:
            err('llms.txt', 'has no blockquote summary')
        if '\n## Optional' not in llms:
            err('llms.txt', 'has no "Optional" section')
        if '\n## En español' not in llms:
            err('llms.txt', 'has no "En español" section')
        for url in re.findall(r'\]\((%s[^)\s]*)\)' % re.escape(SITE), llms):
            if resolve(url[len(SITE):]) is None:
                err('llms.txt', '%s does not map to a file' % url)

    # ---- report ----
    for n in sorted(set(notes)):
        print('note   ', n)
    # ---- MCP server card ----
    card = os.path.join(ROOT, '.well-known', 'mcp.json')
    if not os.path.isfile(card):
        err('.well-known/mcp.json', 'missing')
    else:
        try:
            c = json.load(open(card, encoding='utf-8'))
            if not c.get('remotes') and not c.get('url') and not c.get('endpoints'):
                err('.well-known/mcp.json', 'names no server endpoint')
        except ValueError as e:
            err('.well-known/mcp.json', 'does not parse: %s' % e)

    print('checked %d HTML pages (%d Spanish), sitemap.xml, robots.txt, llms.txt, mcp.json'
          % (len(pages), sum(f.startswith('es/') for f in pages)))
    if errors:
        print('\n%d problem(s):' % len(errors))
        for e in errors:
            print('  FAIL', e)
        return 1
    print('OK — all checks passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
