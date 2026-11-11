/* Fold POS site analytics: Microsoft Clarity (heatmaps, session recordings, funnels).
 *
 * Loaded on every public page by build_site.py, only when analytics.json has a clarity_id.
 * - Every visitor: recordings, heatmaps, clicks, scroll. Clarity masks what people type (default
 *   "Balanced" masking); the Hey Fold demo box is masked explicitly as well.
 * - A browser that sends Global Privacy Control gets Clarity's no-cookie mode.
 * - Custom events (filter recordings / build funnels in Clarity): cta_start_free, cta_log_in,
 *   cta_contact, cta_try_hey_fold, contact_email, download, language_switch, heyfold_demo_used,
 *   faq_opened, section_<id>, scroll_50, scroll_90.
 * - Custom tags: site_page, site_lang, utm_source/medium/campaign, cta_location.
 * - Every "Start free" link also carries ?src_page=…&src_cta=… and the visit's utm_* tags, so the
 *   app can tell which page and button sent each signup.
 */
(function () {
  var me = document.currentScript; if (!me) return;
  var ID = me.getAttribute('data-clarity'); if (!ID) return;
  var ES = (document.documentElement.lang || '').toLowerCase().indexOf('es') === 0;
  var PAGE = location.pathname.replace(/\.html$/, '').replace(/\/$/, '') || '/';

  // ── Clarity's standard loader ──
  (function (c, l, a, r, i, t, y) {
    c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
    t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
    y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
  })(window, document, 'clarity', 'script', ID);
  function C() { try { window.clarity.apply(null, arguments); } catch (e) {} }   // always the live function

  if (navigator.globalPrivacyControl === true) C('consentv2', { ad_Storage: 'denied', analytics_Storage: 'denied' });

  C('set', 'site_page', PAGE);
  C('set', 'site_lang', ES ? 'es' : 'en');
  var q = new URLSearchParams(location.search), UTM = {};
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'].forEach(function (k) {
    if (q.get(k)) UTM[k] = q.get(k);
  });
  try {
    if (Object.keys(UTM).length) sessionStorage.setItem('fx_utm', JSON.stringify(UTM));
    else UTM = JSON.parse(sessionStorage.getItem('fx_utm') || '{}');
  } catch (e) {}
  ['utm_source', 'utm_medium', 'utm_campaign'].forEach(function (k) { if (UTM[k]) C('set', k, UTM[k]); });

  function ev(name) { C('event', name); }

  // ── Where on the page a click came from ──
  function where(el) {
    if (el.closest('.fx-nav, header')) return 'header';
    if (el.closest('footer, .fx-foot')) return 'footer';
    var plan = el.closest('.plan');
    if (plan) { var h = plan.querySelector('h3'); return 'plan_' + (h ? h.textContent.trim().toLowerCase() : 'x'); }
    var sec = el.closest('section[id], section[class]');
    if (sec) return sec.id || sec.className.split(' ')[0];
    return 'body';
  }

  // ── Clicks: signup / login / contact / downloads / language ──
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
    var href = a.getAttribute('href'), loc = where(a), label = (a.textContent || '').trim();
    if (/pos\.foldpos\.com\/signup/.test(href)) {
      var u = new URL(a.href);
      u.searchParams.set('src_page', PAGE); u.searchParams.set('src_cta', loc);
      Object.keys(UTM).forEach(function (k) { u.searchParams.set(k, UTM[k]); });
      a.href = u.toString();
      C('set', 'cta_location', loc);
      ev('cta_start_free');
      C('upgrade', 'start_free');        // always keep recordings of visitors who click Start free
    } else if (/pos\.foldpos\.com\/login/.test(href)) ev('cta_log_in');
    else if (/^mailto:/.test(href)) ev('contact_email');
    else if (/\/contact$|\/contact\.html$/.test(href)) ev('cta_contact');
    else if (/\/download\//.test(href) || /\.exe$|\.pkg$/.test(href)) ev('download');
    else if (/^(ES|Español|EN|English)$/i.test(label)) ev('language_switch');
    else if (href === '#heyfold') ev('cta_try_hey_fold');
  }, true);

  // ── Sections seen (once each), scroll depth, demo, FAQ ──
  function onReady(fn) { if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  onReady(function () {
    if ('IntersectionObserver' in window) {
      var seen = {};
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          var id = en.target.id;
          if (en.isIntersecting && !seen[id]) { seen[id] = 1; ev('section_' + id.replace(/-/g, '_')); io.unobserve(en.target); }
        });
      }, { rootMargin: '0px 0px -50% 0px' });   // seen = reached the middle of the screen (works for very tall sections)
      document.querySelectorAll('section[id]').forEach(function (s) { io.observe(s); });
    }
    var hit = {};
    window.addEventListener('scroll', function () {
      var h = document.documentElement, max = h.scrollHeight - h.clientHeight; if (max <= 0) return;
      var pct = (h.scrollTop || document.body.scrollTop) / max * 100;
      [50, 90].forEach(function (m) { if (pct >= m && !hit[m]) { hit[m] = 1; ev('scroll_' + m); } });
    }, { passive: true });

    var say = document.getElementById('sayInput'), tried = false;
    if (say) {
      say.setAttribute('data-clarity-mask', 'True');
      say.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !tried && say.value.trim()) { tried = true; ev('heyfold_demo_used'); }
      });
    }
    document.querySelectorAll('details').forEach(function (d) {
      d.addEventListener('toggle', function () { if (d.open) ev('faq_opened'); });
    });
  });
})();
