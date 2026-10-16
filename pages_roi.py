#!/usr/bin/env python3
"""The laundromat ROI calculator for Fold Pay machine payments: foldpos.com/laundromat-roi

    from pages_roi import roi        # -> (html, md) for slug 'laundromat-roi'

build_site.py writes the page and its Markdown mirror. English only for now.

Everything is worked out in the visitor's browser by the script below: no network calls,
no tracking, nothing stored. The numbers it uses for Fold's own costs sit as constants at
the top of SCRIPT; the page text and the Markdown mirror read them from there, so changing
a number there changes it everywhere on this page (then run build_site.py).

Fold's costs as set on 13 Oct 2026 (wallet top-ups): the store pays 2.49% + 29 cents per
top-up, the customer pays a flat 35 cents per top-up, $10 minimum. The Fold Reader monthly
price is not final: the page says "~$3 per machine per month (pricing being finalized)".
No competitor is named on this page.

A new top-level page must also be in RESERVED_SLUGS in the API
(src/online-booking/online-booking.util.ts), or it would hide a shop's booking link.
"""
import re

from build_site import page, md_footer, esc, ic, SITE

SLUG = 'laundromat-roi'

# ── the calculator script. The constants at its top are the one place Fold's prices live. ──
SCRIPT = r'''<script>
(function(){
'use strict';
/* ---- Fold's prices: change them here, then run build_site.py ---- */
var READER_PER_MACHINE_MONTH = 3;      // Fold Reader rental, $ per machine per month (pricing being finalized)
var STORE_PCT_PER_TOPUP = 0.0249;      // the store pays 2.49% of each top-up...
var STORE_FIXED_PER_TOPUP = 0.29;      // ...plus $0.29 per top-up
var CUSTOMER_FEE_PER_TOPUP = 0.35;     // the customer pays $0.35 per top-up (not the store)
var UPFRONT_HARDWARE = 0;              // what the store pays up front for readers
var DAYS_PER_MONTH = 365 / 12;         // 30.4 days in an average month
/* ----------------------------------------------------------------- */

var form = document.getElementById('roi-form');
if (!form) return;
var $ = function(id){ return document.getElementById(id); };
var KEYS = ['washers','dryers','turns','wprice','dprice','share','topup','offdisc','uplift','coin','dturns','offshare'];
var DEFAULTS = {};
var dturnsLinked = true;   // dryer turns follow washer turns until the owner changes them

function r2(v){ return Math.round(v * 100) / 100; }
function num(v){ var n = parseFloat(v); return isFinite(n) ? n : 0; }
function money(v, cents){
  var neg = v < 0; v = Math.abs(v);
  var s = '$' + v.toLocaleString('en-US', {minimumFractionDigits: cents ? 2 : 0, maximumFractionDigits: cents ? 2 : 0});
  return neg ? '−' + s : s;
}
function signed(v){ return (v < 0 ? '−' : '+') + money(Math.abs(v)); }
function pct(v, d){ return (v * 100).toLocaleString('en-US', {maximumFractionDigits: d == null ? 2 : d}) + '%'; }
function count(v){ return Math.round(v).toLocaleString('en-US'); }
function setText(sel, text){ var els = document.querySelectorAll(sel); for (var i = 0; i < els.length; i++) els[i].textContent = text; }

function field(k){ return { n: $('n-' + k), r: $('r-' + k) }; }
function read(k){
  var f = field(k), v = num(f.n.value);
  var mn = num(f.n.min), mx = f.n.max === '' ? Infinity : num(f.n.max);
  return Math.min(Math.max(v, mn), mx);
}
function valueText(k, v){
  var f = field(k);
  if (f.n.dataset.unit === '%') return v + '%';
  if (f.n.dataset.unit === '$') return money(v, v % 1 !== 0);
  return String(v);
}
function syncRange(k, v){ var f = field(k); f.r.value = v; f.r.setAttribute('aria-valuetext', valueText(k, v)); }

function calc(){
  var x = {};
  KEYS.forEach(function(k){ x[k] = read(k); });
  // every step is rounded to the cent, so the math shown on the page adds up exactly
  var machines = x.washers + x.dryers;
  var washRev = r2(x.washers * x.turns * x.wprice * DAYS_PER_MONTH);
  var dryRev = r2(x.dryers * x.dturns * x.dprice * DAYS_PER_MONTH);
  var rev = r2(washRev + dryRev);
  var walletBase = r2(rev * x.share / 100);
  var uplift = r2(walletBase * x.uplift / 100);
  var walletGross = r2(walletBase + uplift);
  var discount = r2(walletGross * (x.offshare / 100) * (x.offdisc / 100));
  var walletPaid = r2(walletGross - discount);
  var topups = x.topup > 0 ? Math.round(walletPaid / x.topup) : 0;
  var procPct = r2(walletPaid * STORE_PCT_PER_TOPUP);
  var procFixed = r2(topups * STORE_FIXED_PER_TOPUP);
  var proc = r2(procPct + procFixed);
  var reader = r2(machines * READER_PER_MACHINE_MONTH);
  var foldCost = r2(proc + reader);
  var net = r2(uplift + x.coin - discount - foldCost);
  return {x: x, machines: machines, washRev: washRev, dryRev: dryRev, rev: rev, walletBase: walletBase, uplift: uplift,
    walletGross: walletGross, discount: discount, walletPaid: walletPaid, topups: topups, procPct: procPct, procFixed: procFixed,
    proc: proc, reader: reader, foldCost: foldCost, custFees: r2(topups * CUSTOMER_FEE_PER_TOPUP), net: net, year: r2(net * 12)};
}

var liveTimer = null;
function render(){
  var c = calc(), x = c.x;
  setText('[data-o=net]', money(c.net));
  setText('[data-o=uplift]', signed(c.uplift));
  setText('[data-o=coin]', signed(x.coin));
  setText('[data-o=discount]', signed(-c.discount));
  setText('[data-o=proc]', signed(-c.proc));
  setText('[data-o=reader]', signed(-c.reader));
  setText('[data-o=foldcost]', money(c.foldCost));
  setText('[data-o=year]', money(c.year));
  setText('[data-o=machines]', count(c.machines));
  setText('[data-o=topups]', count(c.topups));
  setText('[data-o=custfees]', money(c.custFees));
  document.querySelectorAll('[data-row=discount]').forEach(function(el){ el.hidden = c.discount <= 0; });
  var neg = c.net < 0;
  document.querySelectorAll('.roi-net').forEach(function(el){ el.classList.toggle('is-neg', neg); });
  // payback
  var pb, pbSub;
  if (c.net <= 0) { pb = 'Not at these numbers'; pbSub = 'At these inputs Fold would cost more each month than it brings in.'; }
  else if (UPFRONT_HARDWARE <= 0) { pb = 'No upfront cost'; pbSub = 'Nothing to buy for the readers, so you are ahead from the first month.'; }
  else { var m = Math.ceil(UPFRONT_HARDWARE / c.net); pb = m + (m === 1 ? ' month' : ' months'); pbSub = money(UPFRONT_HARDWARE) + ' up front, paid back by the monthly gain.'; }
  setText('[data-o=payback]', pb);
  setText('[data-o=paybacksub]', pbSub);

  // the math, with this store's numbers
  var D = DAYS_PER_MONTH.toFixed(1);
  setText('[data-m=wash]', x.washers + ' washers × ' + x.turns + ' turns × ' + money(x.wprice, true) + ' × ' + D + ' days = ' + money(c.washRev, true));
  setText('[data-m=dry]', x.dryers + ' dryers × ' + x.dturns + ' turns × ' + money(x.dprice, true) + ' × ' + D + ' days = ' + money(c.dryRev, true));
  setText('[data-m=rev]', money(c.washRev, true) + ' + ' + money(c.dryRev, true) + ' = ' + money(c.rev, true) + ' a month through your machines');
  setText('[data-m=wallet]', money(c.rev, true) + ' × ' + x.share + '% = ' + money(c.walletBase, true) + ' a month paid by phone or wallet instead of coins');
  setText('[data-m=uplift]', money(c.walletBase, true) + ' × ' + x.uplift + '% = ' + money(c.uplift, true) + ' extra a month');
  setText('[data-m=discount]', '(' + money(c.walletBase, true) + ' + ' + money(c.uplift, true) + ') × ' + x.offshare + '% off-peak × ' + x.offdisc + '% off = ' + money(c.discount, true) + ' a month');
  setText('[data-m=topups]', money(c.walletPaid, true) + ' loaded ÷ ' + money(x.topup, x.topup % 1 !== 0) + ' per top-up = ' + count(c.topups) + ' top-ups a month');
  setText('[data-m=proc]', '(' + money(c.walletPaid, true) + ' × ' + pct(STORE_PCT_PER_TOPUP) + ') + (' + count(c.topups) + ' × ' + money(STORE_FIXED_PER_TOPUP, true) + ') = ' + money(c.procPct, true) + ' + ' + money(c.procFixed, true) + ' = ' + money(c.proc, true));
  setText('[data-m=reader]', count(c.machines) + ' machines × ' + money(READER_PER_MACHINE_MONTH, READER_PER_MACHINE_MONTH % 1 !== 0) + ' = ' + money(c.reader, true));
  setText('[data-m=net]', money(c.uplift, true) + ' + ' + money(x.coin, true) + ' − ' + money(c.discount, true) + ' − ' + money(c.proc, true) + ' − ' + money(c.reader, true) + ' = ' + money(c.net, true));
  setText('[data-m=year]', money(c.net, true) + ' × 12 = ' + money(c.year, true));
  setText('[data-m=cust]', count(c.topups) + ' × ' + money(CUSTOMER_FEE_PER_TOPUP, true) + ' = ' + money(c.custFees, true) + ' a month, paid by your customers on top of what they load');

  // "email us these numbers"
  var lines = ['Hi Fold POS team,', '', 'I tried the laundromat ROI calculator. My numbers:', '',
    'Washers: ' + x.washers + ', dryers: ' + x.dryers, 'Turns per washer per day: ' + x.turns + ', per dryer: ' + x.dturns,
    'Washer vend: ' + money(x.wprice, true) + ', dryer revenue per turn: ' + money(x.dprice, true),
    'Paying by phone/wallet: ' + x.share + '%, average top-up: ' + money(x.topup, true) + ', off-peak discount: ' + x.offdisc + '%',
    'Assumed uplift: ' + x.uplift + '%, coin handling saved: ' + money(x.coin) + ' a month', '',
    'Estimated net monthly gain: ' + money(c.net) + ', 12 months: ' + money(c.year), '',
    'Store name:', 'Best phone:', ''];
  var mail = $('roi-mail');
  if (mail) mail.href = 'mailto:contact@foldpos.com?subject=' + encodeURIComponent('Fold Pay machine payments · ROI') + '&body=' + encodeURIComponent(lines.join('\n'));

  clearTimeout(liveTimer);
  liveTimer = setTimeout(function(){
    $('roi-live').textContent = 'Net monthly gain ' + money(c.net) + '. Twelve-month total ' + money(c.year) + '.';
  }, 700);
}

function setValue(k, v, from){
  var f = field(k);
  if (from !== 'n') f.n.value = v;
  syncRange(k, read(k));
  if (k === 'turns' && dturnsLinked) { field('dturns').n.value = read('turns'); syncRange('dturns', read('turns')); }
  if (k === 'dturns' && from) dturnsLinked = false;
  render();
}

KEYS.forEach(function(k){
  var f = field(k);
  DEFAULTS[k] = f.n.value;
  f.r.addEventListener('input', function(){ setValue(k, f.r.value, 'r'); });
  f.n.addEventListener('input', function(){ if (f.n.value !== '') setValue(k, f.n.value, 'n'); });
  f.n.addEventListener('change', function(){ f.n.value = read(k); setValue(k, f.n.value, 'n'); });
  syncRange(k, read(k));
});
$('roi-reset').addEventListener('click', function(){
  dturnsLinked = true;
  KEYS.forEach(function(k){ field(k).n.value = DEFAULTS[k]; syncRange(k, read(k)); });
  render();
});
form.addEventListener('submit', function(e){ e.preventDefault(); });

// phones: a small bar with the result while the results card is off screen
var bar = $('roi-bar'), res = $('results');
if (bar && res && 'IntersectionObserver' in window) {
  new IntersectionObserver(function(es){ var e = es[0]; bar.classList.toggle('show', !e.isIntersecting && e.boundingClientRect.top > 0); }, {threshold: 0}).observe(res);
}
render();
})();
</script>'''


def _const(name):
    return float(re.search(r'var %s = ([\d.]+);' % name, SCRIPT).group(1))


READER = _const('READER_PER_MACHINE_MONTH')
STORE_PCT = _const('STORE_PCT_PER_TOPUP')
STORE_FIXED = _const('STORE_FIXED_PER_TOPUP')
CUST_FEE = _const('CUSTOMER_FEE_PER_TOPUP')


def _m(v):
    """$3, $3.50, $0.29"""
    return '$%d' % v if v == int(v) else '$%.2f' % v


READER_TXT = f'~{_m(READER)} per machine per month (pricing being finalized)'
STORE_TXT = f'{STORE_PCT * 100:.2f}% + {_m(STORE_FIXED)} per top-up'
CUST_TXT = f'{_m(CUST_FEE)} per top-up'

# key, label, default, range min, range max, step, unit ('$', '%' or ''), number-field max, hint
STORE_FIELDS = [
    ('washers', 'Washers', 20, 0, 120, 1, '', 999, ''),
    ('dryers', 'Dryers', 24, 0, 120, 1, '', 999, ''),
    ('turns', 'Turns per washer per day', 4, 0, 12, 0.5, '', 48, 'On average, across the week.'),
    ('wprice', 'Average washer vend price', 4.50, 0, 15, 0.25, '$', 100, ''),
    ('dprice', 'Dryer revenue per turn', 2.00, 0, 10, 0.25, '$', 100, 'What a typical dry brings in, all its time added up.'),
]
CUSTOMER_FIELDS = [
    ('share', 'Customers who’d pay by phone or wallet', 30, 0, 100, 1, '%', 100, 'The rest keep paying with coins or your change machine.'),
    ('topup', 'Average top-up', 20, 10, 100, 5, '$', 500, 'What a customer loads at a time. The minimum is $10.'),
    ('offdisc', 'Off-peak discount you might offer', 0, 0, 50, 1, '%', 100, 'Optional. Leave at 0% if you don’t plan one.'),
]
ASSUME_FIELDS = [
    ('uplift', 'Card and wallet uplift', 10, 0, 30, 1, '%', 100,
     'Stores that take cards tend to see more spent per visit. Applied to the phone and wallet share only. An assumption to adjust, not a promise.'),
    ('coin', 'Coin collection and handling saved a month', 150, 0, 1000, 10, '$', 100000,
     'Collecting, counting, rolling, bank runs, change-machine refills and service calls that phone payments take off your plate.'),
    ('dturns', 'Turns per dryer per day', 4, 0, 12, 0.5, '', 48, 'Follows the washer turns until you change it.'),
    ('offshare', 'Share of wallet spending in off-peak hours', 30, 0, 100, 5, '%', 100, 'Only matters if you offer an off-peak discount.'),
]


def _fmt(v):
    return ('%g' % v) if v != int(v) else str(int(v))


def _field(k, label, val, mn, mx, step, unit, nmax, hint):
    hid = f' aria-describedby="h-{k}"' if hint else ''
    pre = '<span class="roi-u" aria-hidden="true">$</span>' if unit == '$' else ''
    post = '<span class="roi-u" aria-hidden="true">%</span>' if unit == '%' else ''
    val_s = ('%.2f' % val) if unit == '$' and step < 1 else _fmt(val)
    step_s = _fmt(step) if unit != '$' else '0.01'
    unit_name = {'$': ' in dollars', '%': ' in percent'}.get(unit, '')
    return f'''<div class="roi-f">
  <div class="roi-fh">
    <label for="n-{k}" id="l-{k}">{label}<span class="visually-hidden">{unit_name}</span></label>
    <span class="roi-num">{pre}<input id="n-{k}" type="number" inputmode="decimal" min="{_fmt(mn)}" max="{nmax}" step="{step_s}" value="{val_s}" data-unit="{unit}"{hid}>{post}</span>
  </div>
  <input class="roi-range" type="range" id="r-{k}" min="{_fmt(mn)}" max="{_fmt(mx)}" step="{_fmt(step)}" value="{val_s}" aria-labelledby="l-{k}"{hid}>
  {f'<p class="roi-hint" id="h-{k}">{hint}</p>' if hint else ''}
</div>'''


STYLE = '''<style>
.roi{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:40px;align-items:start}
.roi-in{display:grid;gap:22px}
.roi fieldset{border:1px solid var(--line);border-radius:18px;padding:22px 24px 8px;margin:0;background:#fff;min-width:0}
.roi legend{font:700 13px/1 "Figtree",sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--brand);padding:0 8px;margin-left:-8px}
.roi-lede{color:var(--ink-2);font-size:14.5px;margin:2px 0 6px;max-width:58ch}
.roi-f{padding:14px 0 16px;border-top:1px solid var(--line)}
.roi-lede+.roi-f,legend+.roi-f{border-top:0}
.roi-fh{display:flex;align-items:center;justify-content:space-between;gap:16px}
.roi-fh label{font-weight:600;font-size:15px;line-height:1.35}
.roi-num{display:inline-flex;align-items:center;gap:4px;border:1px solid var(--line);border-radius:10px;padding:0 10px;background:#fff;flex:none;transition:border-color .2s}
.roi-num:focus-within{border-color:var(--brand)}
.roi-num input{width:72px;border:0;outline:0;background:transparent;font:600 16px/1 "Figtree",sans-serif;color:var(--ink);padding:10px 0;text-align:right;font-variant-numeric:tabular-nums;-moz-appearance:textfield}
.roi-num input::-webkit-outer-spin-button,.roi-num input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.roi-num:has(input:focus-visible){outline:2px solid var(--brand);outline-offset:2px}
.roi-num input:focus-visible{outline:0}
.roi-u{color:var(--ink-3);font-weight:600;font-size:15px}
.roi-range{width:100%;margin:12px 0 0;height:28px;accent-color:var(--brand);cursor:pointer;background:transparent}
.roi-hint{font-size:13.5px;color:var(--ink-3);margin-top:4px;max-width:60ch}
.roi-assume{background:var(--fog)}
.roi-assume .roi-num{background:#fff}
.roi-costs{border:1px solid var(--line);border-radius:18px;padding:22px 24px;background:#fff}
.roi-costs h2{font-size:18px;margin-bottom:12px}
.roi-costs ul{list-style:none;margin:0;padding:0;display:grid;gap:10px;font-size:15px;color:var(--ink-2)}
.roi-costs li{display:flex;gap:10px;align-items:flex-start}
.roi-costs li svg{color:var(--mint);width:18px;height:18px;margin-top:3px}
.roi-costs b{color:var(--ink)}
.roi-out{position:sticky;top:88px;display:grid;gap:14px}
.roi-card{border:1px solid var(--line);border-radius:20px;padding:26px;background:#fff;box-shadow:0 30px 60px -44px rgba(14,23,48,.4);scroll-margin-top:88px}
.roi-card h2{font-size:15px;font-weight:700;color:var(--ink-3);letter-spacing:0}
.roi-net{font:700 clamp(40px,5vw,52px)/1.05 "Figtree",sans-serif;letter-spacing:-.03em;color:var(--ink);margin-top:8px;font-variant-numeric:tabular-nums}
.roi-net small{font:500 16px "Figtree",sans-serif;color:var(--ink-3);letter-spacing:0}
.roi-net.is-neg{color:#b42318}
.roi-rows{margin:18px 0 0;padding:0;display:grid}
.roi-rows div{display:flex;justify-content:space-between;gap:16px;padding:10px 0;border-top:1px solid var(--line);font-size:15px}
.roi-rows dt{color:var(--ink-2)}
.roi-rows dd{margin:0;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap}
.roi-rows div[hidden]{display:none}
.roi-rows .tot{border-top:1.5px solid var(--ink)}
.roi-rows .tot dt,.roi-rows .tot dd{color:var(--ink);font-weight:700}
.roi-rows .sub{margin:2px 0 0;max-width:none;font-size:13px;color:var(--ink-3);display:block;font-weight:400}
.roi-pb{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.roi-pb>div{background:var(--fog);border-radius:14px;padding:14px 16px}
.roi-pb b{display:block;font-size:17px;line-height:1.25;font-variant-numeric:tabular-nums}
.roi-pb span{display:block;font-size:12.5px;color:var(--ink-3);margin-top:2px}
.roi-pb .k{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin:0 0 6px}
.roi-vs{margin-top:16px;font-weight:700;font-size:15.5px;color:var(--ink);display:flex;gap:8px;align-items:center}
.roi-vs svg{color:var(--mint)}
.roi-acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.roi-acts .btn{flex:1 1 auto}
.roi-fine{font-size:12.5px;color:var(--ink-3);margin-top:14px;line-height:1.5}
.roi-reset{background:none;border:0;padding:0;font:inherit;font-size:14px;font-weight:600;color:var(--brand);cursor:pointer;justify-self:start;text-decoration:underline;text-underline-offset:3px}
.roi-math .qa summary{font-size:18px}
.roi-math ol{margin:0;padding-left:22px;display:grid;gap:14px;color:var(--ink-2)}
.roi-math ol b{color:var(--ink);display:block}
.roi-math code{font:500 14px/1.5 ui-monospace,Menlo,Consolas,monospace;color:var(--ink);background:var(--fog);border-radius:8px;padding:6px 10px;display:block;margin-top:6px;overflow-wrap:anywhere}
.roi-math .note{margin-top:18px;font-size:14px;color:var(--ink-3);max-width:66ch}
.roi-bar{display:none}
@media (max-width:900px){
  .roi{grid-template-columns:1fr;gap:24px}
  .roi-out{position:static}
  .roi-bar{display:flex;position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:40;align-items:center;justify-content:space-between;gap:12px;
    background:var(--deep);color:#fff;border-radius:16px;padding:12px 16px;text-decoration:none;box-shadow:0 18px 40px -16px rgba(14,23,48,.6);
    transform:translateY(140%);transition:transform .3s var(--ease)}
  .roi-bar.show{transform:none}
  .roi-bar span{font-size:13px;color:rgba(255,255,255,.75)}
  .roi-bar b{font-size:20px;font-variant-numeric:tabular-nums}
  .roi-bar .roi-net{font-size:20px;margin:0;color:#fff}
  .roi-bar .roi-net.is-neg{color:#ffb4ab}
}
@media (max-width:520px){
  .roi fieldset{padding:18px 16px 6px}
  .roi-card,.roi-costs{padding:20px 18px}
  .roi-num input{width:60px}
  .roi-pb{grid-template-columns:1fr}
}
@media (prefers-reduced-motion:reduce){.roi-bar{transition:none}}
</style>'''


def roi():
    store = ''.join(_field(*f) for f in STORE_FIELDS)
    cust = ''.join(_field(*f) for f in CUSTOMER_FIELDS)
    assume = ''.join(_field(*f) for f in ASSUME_FIELDS)
    check = ic('check')
    body = f'''{STYLE}
<section class="phead"><div class="wrap">
  <div class="crumbs"><a href="/">Fold POS</a> › Laundromat ROI calculator</div>
  <div class="kicker">Fold Pay for machines</div>
  <h1>What phone payments could add to your laundromat.</h1>
  <p class="lede">Put in your own machines and prices. See what Fold Pay and the Fold Reader would cost you each month, what they could bring in, and the math behind every number.</p>
</div></section>

<section class="section" style="padding-top:8px"><div class="wrap">
  <noscript><p class="roi-fine" style="margin-bottom:16px">The calculator needs JavaScript. The math is written out under “How we calculate this” below.</p></noscript>
  <div class="roi">
    <form class="roi-in" id="roi-form" novalidate>
      <fieldset>
        <legend>Your machines</legend>
        {store}
      </fieldset>
      <fieldset>
        <legend>Your customers</legend>
        {cust}
      </fieldset>
      <fieldset class="roi-assume">
        <legend>Assumptions</legend>
        <p class="roi-lede">Our starting guesses, not promises. Change them to match your store.</p>
        {assume}
      </fieldset>
      <button type="button" class="roi-reset" id="roi-reset">Reset to the starting numbers</button>
    </form>

    <div class="roi-out">
      <div class="roi-card" id="results" tabindex="-1">
        <h2>Net monthly gain</h2>
        <p class="roi-net"><span data-o="net"></span> <small>/ month</small></p>
        <dl class="roi-rows">
          <div><dt>Extra revenue from card &amp; wallet uplift</dt><dd data-o="uplift"></dd></div>
          <div><dt>Coin handling saved</dt><dd data-o="coin"></dd></div>
          <div data-row="discount" hidden><dt>Off-peak discounts you give</dt><dd data-o="discount"></dd></div>
          <div><dt>Fold processing on top-ups<span class="sub"><span data-o="topups"></span> top-ups at {esc(STORE_TXT)}</span></dt><dd data-o="proc"></dd></div>
          <div><dt>Fold Reader rental<span class="sub"><span data-o="machines"></span> machines at {esc(READER_TXT)}</span></dt><dd data-o="reader"></dd></div>
          <div class="tot"><dt>Net monthly gain</dt><dd data-o="net"></dd></div>
        </dl>
        <div class="roi-pb">
          <div><p class="k">Payback</p><b data-o="payback">No upfront cost</b><span data-o="paybacksub"></span></div>
          <div><p class="k">First 12 months</p><b data-o="year"></b><span>Net gain over a year at these numbers.</span></div>
        </div>
        <p class="roi-vs">{check}No 48-month contract. No $3,500 install.</p>
        <div class="roi-acts">
          <a class="btn btn-primary" id="roi-mail" href="mailto:contact@foldpos.com?subject=Fold%20Pay%20machine%20payments">Email us these numbers</a>
          <a class="btn btn-ghost" href="/contact">Talk to us</a>
        </div>
        <p class="roi-fine">An estimate from the numbers you entered, not a quote or a promise of results. Fold Pay for machines is being rolled out store by store. Your customers also pay <span data-o="custfees"></span> a month in top-up fees ({esc(CUST_TXT)}); that never comes out of your revenue.</p>
      </div>

      <div class="roi-costs">
        <h2>What Fold costs</h2>
        <ul>
          <li>{check}<span><b>Your customer pays {esc(CUST_TXT)}</b>, not the store.</span></li>
          <li>{check}<span><b>The store pays {esc(STORE_TXT)}</b>, on what customers load.</span></li>
          <li>{check}<span><b>Fold Reader:</b> {esc(READER_TXT)}.</span></li>
          <li>{check}<span><b>No long contract</b> and nothing to buy up front.</span></li>
        </ul>
      </div>
    </div>
  </div>
  <p class="visually-hidden" id="roi-live" aria-live="polite"></p>
</div></section>

<section class="section roi-math" style="padding-top:0"><div class="wrap narrow">
  <details class="qa">
    <summary>How we calculate this</summary>
    <div class="a">
      <ol>
        <li><b>Machine revenue a month.</b> An average month is 365 ÷ 12 = 30.4 days.
          <code data-m="wash"></code><code data-m="dry"></code><code data-m="rev"></code></li>
        <li><b>The part paid by phone or wallet.</b> Moving a coin sale to the wallet is not new money by itself, so only the uplift below counts as extra revenue.
          <code data-m="wallet"></code></li>
        <li><b>Extra revenue from the uplift.</b> An assumption you set, applied to the phone and wallet share only.
          <code data-m="uplift"></code></li>
        <li><b>Off-peak discounts.</b> What you choose to give, on wallet spending in off-peak hours.
          <code data-m="discount"></code></li>
        <li><b>Top-ups a month.</b> Over time customers load about what they spend.
          <code data-m="topups"></code></li>
        <li><b>Fold processing.</b> {esc(STORE_TXT)}, paid by the store.
          <code data-m="proc"></code></li>
        <li><b>Fold Reader rental.</b> {esc(READER_TXT)}, one reader per machine.
          <code data-m="reader"></code></li>
        <li><b>Net monthly gain.</b> Uplift + coin handling saved − off-peak discounts − Fold processing − Fold Reader rental.
          <code data-m="net"></code></li>
        <li><b>12-month total.</b>
          <code data-m="year"></code></li>
        <li><b>What your customers pay.</b> {esc(CUST_TXT)}, shown for the full picture; it is not a cost to you.
          <code data-m="cust"></code></li>
      </ol>
      <p class="note">Payback: the readers need no upfront hardware, so there is nothing to pay back; when the monthly gain is above zero you are ahead from the first month. Not included: more customers choosing your store because it takes phones and cards, fewer machines down from jammed coin slots, and any card fees you pay today elsewhere.</p>
    </div>
  </details>
</div></section>

<a class="roi-bar" id="roi-bar" href="#results" aria-hidden="true" tabindex="-1"><span>Net monthly gain</span><b class="roi-net" data-o="net"></b></a>'''
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "@id": f'{SITE}/{SLUG}#calculator',
          "name": "Laundromat ROI calculator", "url": f'{SITE}/{SLUG}', "applicationCategory": "BusinessApplication",
          "operatingSystem": "Any", "isAccessibleForFree": True, "inLanguage": "en-US",
          "description": "Estimate what Fold Pay phone and wallet payments on washers and dryers would cost and bring in each month.",
          "publisher": {"@id": f'{SITE}/#organization'}}
    html_ = page(SLUG, 'Laundromat ROI calculator — Fold POS',
                 f'Estimate what Fold Pay phone and wallet payments on your washers and dryers would bring in and cost each month: '
                 f'{STORE_TXT} for the store, {READER_TXT.split(" (")[0]} for the reader, no upfront cost.',
                 'Laundromat ROI calculator — Fold Pay', 'Laundromat ROI calculator', body, [ld], SCRIPT)

    md = ['# Laundromat ROI calculator', '',
          f'> Canonical page: {SITE}/{SLUG} · Markdown mirror. The page works the numbers out in your browser.', '',
          'Estimate what Fold Pay phone and wallet payments on washers and dryers would bring in and cost a laundromat each month.', '',
          '## What Fold costs', '',
          f'- The customer pays {CUST_TXT}, not the store.',
          f'- The store pays {STORE_TXT}.',
          f'- Fold Reader: {READER_TXT}.',
          '- No long contract and no upfront hardware cost. No 48-month contract. No $3,500 install.', '',
          '## Inputs and starting numbers', '']
    for k, label, val, mn, mx, step, unit, nmax, hint in STORE_FIELDS + CUSTOMER_FIELDS + ASSUME_FIELDS:
        v = (f'${val:.2f}' if val != int(val) else f'${int(val)}') if unit == '$' else f'{_fmt(val)}{unit}'
        md.append(f'- {label}: {v}' + (f' ({hint})' if hint else ''))
    md += ['', '## How it is calculated', '',
           '1. Machine revenue a month = washers × turns × washer price × 30.4 days + dryers × dryer turns × dryer revenue per turn × 30.4 days.',
           '2. Wallet share = machine revenue × share paying by phone or wallet (moving coin sales to the wallet is not new money by itself).',
           '3. Extra revenue = wallet share × uplift (an assumption, not a promise).',
           '4. Off-peak discounts = wallet spending × off-peak share × discount.',
           '5. Top-ups a month = money loaded ÷ average top-up.',
           f'6. Fold processing = money loaded × {STORE_PCT * 100:.2f}% + top-ups × {_m(STORE_FIXED)}.',
           f'7. Fold Reader rental = machines × {_m(READER)}.',
           '8. Net monthly gain = extra revenue + coin handling saved − off-peak discounts − Fold processing − reader rental; 12-month total = net × 12.',
           '9. Payback: no upfront hardware, so nothing to pay back.', '',
           'An estimate from the numbers entered, not a quote or a promise of results. Questions: contact@foldpos.com', '']
    return html_, '\n'.join(md) + md_footer()


if __name__ == '__main__':
    h, md = roi()
    open(SLUG + '.html', 'w', encoding='utf-8').write(h)
    open(SLUG + '.md', 'w', encoding='utf-8').write(md.rstrip() + '\n')
    print('wrote', SLUG)
