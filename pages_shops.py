#!/usr/bin/env python3
"""The three shop pages, /laundromats, /dry-cleaners and /alterations, in English and Spanish, on the
same page system as Pricing, Features, Hey Fold, Pickup & delivery and Fold Time (pages.css).

    from pages_shops import shop          # shop('laundromat'|'drycleaner'|'tailor', 'en'|'es') -> html

build_site.py writes the English pages. The Spanish pages are static files like the rest of es/:
run `python3 pages_shops.py --es` after changing the copy here, then build_site.py and check_seo.py.
The .md mirrors are static.

These pages used to be built by build_pages.py from templates/shop-base.html (the 2025 homepage).
The words are the ones those pages had on Oct 15 2026; the design is new, the screens are real
Fold POS screens (assets/img/new), and the old pricing table is a line pointing to /pricing so the
plans are only described in one place.
"""
import os
import sys

from build_site import page, esc, ic, SITE, BAND
from pages_delivery import BAND_ES, IMG_STYLE, LABEL_STYLE

DATA = {('en', 'laundromat'): {'slug': 'laundromats',
                        'title': 'Laundromat POS — Fold POS',
                        'desc': 'Point of sale for laundromats: wash & fold by the pound, a live floor map of every washer and dryer, machines, supplies, '
                                'pickup & delivery and staff shifts. 14-day free trial, no card.',
                        'og': 'Fold POS for laundromats',
                        'hero': {'eyebrow': 'Point of sale for laundromats',
                                 'h1': 'A laundromat POS for owners, by owners.',
                                 'lede': 'Wash &amp; fold by the pound at the counter, a live map of every washer and dryer on the floor, and every order '
                                         'followed from drop-off to pickup.',
                                 'btns': [('https://pos.foldpos.com/signup', 'Start free trial'),
                                          ('mailto:contact@foldpos.com?subject=Fold%20POS%20demo', 'Book a demo')],
                                 'note': '14 days free · no card · runs in your browser, on Mac, Windows and iPad · talks back when you say “Hey Fold”'},
                        'voice': {'eyebrow': 'Hey Fold · built into every plan',
                                  'h2': "The only POS you can talk to. Say the order — it's rung up, printed and tagged.",
                                  'lede': "Hands full of someone's laundry? Talk to the counter. Fold listens for its name, takes the order down, confirms it "
                                          'back to you, and sends the receipt and garment tags to the printer.',
                                  'pts': ['Say “Hey Fold”, press Caps Lock or tap the orb; it stays quiet until called',
                                          'Customer lookup, order status and production updates by voice',
                                          'Works on the browser, Mac and Windows builds with a plain microphone'],
                                  'rows': [('You', 'you', 'Hey Fold — new order for Maria Garcia. Two bags wash and fold, one comforter, pickup Thursday.'),
                                           ('Fold', 'fold', 'Got it. Maria Garcia — 2 bags wash &amp; fold, 1 comforter, due Thursday. $46.50. Print and tag?'),
                                           ('You', 'you', 'Yes.'),
                                           ('Print',
                                            'print',
                                            'Receipt #WNF-0417 · customer + store copy → Epson TM-T20<br/>Tags 1/3 · 2/3 · 3/3 → Zebra heat-seal')]},
                        'switch': {'eyebrow': 'Built for how your shop works',
                                   'h2': 'What a laundromat gets on day one.',
                                   'lede': 'Choose “Laundromat” at sign-up and this is the POS you see — the tools below and nothing that gets in the way. '
                                           'Change it any time in Settings.',
                                   'q': 'Not a laundromat?',
                                   'links': [('dry-cleaners', 'For dry cleaners'), ('alterations', 'For tailors')]},
                        'chapters': [{'eyebrow': 'Wash &amp; fold · drop-off laundry',
                                      'h2': 'Ring it up the way the customer describes it.',
                                      'lede': '“Two bags, one comforter, rush it.” Weigh a bag, add a per-piece item, toggle express — and the price is right '
                                              "before you've finished talking.",
                                      'pts': ['By the pound with a minimum, by the bag, or by the piece, on one order',
                                              'Express fees, discounts and per-customer default pricing applied automatically',
                                              'Bag counts and weights on the ticket, so a 3-bag order comes back as 3 bags',
                                              'Find a returning customer by name, phone or barcode scan mid-order',
                                              'Cash, card or pay-on-delivery; split a payment across two'],
                                      'fact': ('Two receipts, one tap.',
                                               'A customer copy and a store copy print the moment you submit — on the impact or thermal printer you already '
                                               'own.'),
                                      'shots': [('Check in · Wash & fold',
                                                 'assets/img/order-intake.webp',
                                                 'Check-in screen with wash and fold items and an order summary')]},
                                     {'eyebrow': 'Self-service floor',
                                      'h2': 'Your floor becomes a live map. Every machine on it keeps a record.',
                                      'lede': "Every washer and dryer sits on a floor plan. Ring a machine up at the counter and the plan shows what's free, "
                                              "what's in use and how long is left — for your staff and for the customer who asks “is 12 open?” Tap any machine "
                                              'and its whole life is there: turns, repairs, the technician who fixed it last.',
                                      'pts': ['Floor plan built from your real brands, sizes, stacks and zones',
                                              'Turns per machine per day — see which machines earn their keep',
                                              'Ring up a machine at the counter with the time and the wash type; add 15 minutes or end it from the same screen',
                                              'Each machine in use shows whose load is in it',
                                              'Repair history per machine with cost and downtime; book the technician from the same screen',
                                              'Preventive service reminders by turns run, not just by the calendar'],
                                      'fact': None,
                                      'shots': [('Laundromat · Main floor',
                                                 'assets/img/laundromat.webp',
                                                 'Laundromat floor plan with washers and dryers and their status'),
                                                ('Machine management',
                                                 'assets/img/machines.webp',
                                                 "Machine management list with each machine's status and last service")]},
                                     {'eyebrow': 'Orders',
                                      'h2': 'Every order has a column. Every column has a count.',
                                      'lede': 'Orders move left to right through washing, drying, folding and completed, so nothing sits forgotten in a '
                                              'machine.',
                                      'pts': ['Separate boards for wash &amp; fold, dry cleaning and alterations',
                                              'Express orders flagged in red, due dates on every card',
                                              'Assign a washer or dryer in one tap; live cycle countdown on the card',
                                              'Photos, notes and price changes stay on the ticket'],
                                      'fact': None,
                                      'shots': [('Orders · Wash & fold',
                                                 'assets/img/kanban-board.webp',
                                                 'Workflow board with orders in to-do, washing, drying, ironing, folding and completed columns')]}],
                        'shared': {'eyebrow': 'The same for every shop',
                                   'h2': 'Whatever you clean, the back office is the same.',
                                   'lede': 'Customers, staff, marketing, printing, reports and payments work identically for a laundromat, a dry cleaner or a '
                                           'tailor — so a mixed shop never runs two systems.',
                                   'blocks': [{'eyebrow': 'Marketing',
                                               'h2': 'Reach customers before they think to call.',
                                               'lede': 'Automated flows that fire on their own — a thank-you after the first order, a nudge at 45 days quiet, '
                                                       'a birthday treat — plus SMS, email and push campaigns to segments Fold POS builds for you.',
                                               'pts': ['Flows triggered by first order, order completed, inactivity, birthday',
                                                       'Segments by spend, service mix and last visit, updated automatically',
                                                       '“Orders not collected” reminders in one click from Reports',
                                                       'Delivery and reply tracking on every campaign']},
                                              {'eyebrow': 'Staff',
                                               'h2': 'A clean handoff every time the shift changes.',
                                               'lede': 'Staff clock in and out on the same screen they ring orders on. Roles decide what each person can open. '
                                                       'The morning shift sees exactly what happened overnight.',
                                               'pts': ['Clock-in, breaks and clock-out tied to each employee',
                                                       'Roles and permissions per module, an audit log of who changed what',
                                                       'Shift statistics: orders, revenue and service mix per person',
                                                       'Built-in team chat and notifications']}]},
                        'tickets': {'eyebrow': 'Receipts &amp; tags',
                                    'h2': 'Prints on the printers you already own.',
                                    'lede': 'Claim tickets on the impact printer, garment tags on the heat-seal printer — Fold Print Agent pairs with a '
                                            'six-digit code and keeps them printing from any browser tab or the desktop app.',
                                    'pts': ['Epson TM-T20, Bixolon SRP-275, Star and Zebra out of the box',
                                            'Lot number, piece count, customer, due day and barcode on every tag',
                                            'Permanent heat-sealed barcodes for regulars: scan the garment, it knows the customer',
                                            'Reprint any receipt or tag from the print queue'],
                                    'paper': '<div class="receipt"> <div class="row"><span>FOLD POS · DOWNTOWN</span><span>DC-0417</span></div> <div '
                                             'class="big">THU 11</div> <div class="row"><span>MARIA GARCIA</span><span>···3021</span></div> <hr/> <div '
                                             'class="row"><span>2× WASH &amp; FOLD BAG</span><span>32.00</span></div> <div class="row"><span>1× '
                                             'COMFORTER</span><span>14.50</span></div> <div class="row"><span>PIECES</span><span>3</span></div> <hr/> <div '
                                             'class="row"><span>DUE</span><span><b>$46.50</b></span></div> <div class="bar"></div> <div '
                                             'style="text-align:center">CUSTOMER COPY</div> </div> <div class="tagstack"> <div '
                                             'class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>COMFORTER · WHITE</div><div '
                                             'class="n">1/3</div></div> <div class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>W&amp;F BAG</div><div '
                                             'class="n">2/3</div></div> <div class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>W&amp;F BAG</div><div '
                                             'class="n">3/3</div></div> </div>'},
                        'more': {'eyebrow': 'Also in every shop',
                                 'h2': "Everything a shop needs, nothing it doesn't.",
                                 'lede': "The parts you'd otherwise run in three other apps and a spreadsheet.",
                                 'cards': [('Customers &amp; B2B accounts',
                                            'History, preferences, addresses and notes at the counter. Tax id, payment terms and monthly invoicing for hotels, '
                                            'gyms and restaurants.'),
                                           ('Invoices',
                                            'Individual and business invoices with due dates, cancel-with-reason and a paid/pending view you can filter in a '
                                            'second.'),
                                           ('Reports you can actually read',
                                            'Sales by day, week and month, service mix, customers, costs, profit &amp; loss, orders not collected — and CSV '
                                            'export of any of them.'),
                                           ('Conveyor',
                                            'Slots by conveyor and line, assigned at check-in and freed at hand-over. Scan the ticket, the rail tells you '
                                            'where the order hangs.'),
                                           ('Payments built in',
                                            'Cash, card, pay-on-delivery and split tenders. On your own card processor, at your rates, with a payment link '
                                            'your customer can pay on their phone.'),
                                           ('Search anything, ⌘F',
                                            'One search box for customers, orders, tickets and settings. Keyboard-wedge barcode scanners just work.')]}},
 ('en', 'drycleaner'): {'slug': 'dry-cleaners',
                        'title': 'Dry cleaner POS — Fold POS',
                        'desc': 'Point of sale for dry cleaners: per-piece tickets, heat-seal garment tags, conveyor slots, alterations on the same ticket, '
                                'wash & fold and pickup & delivery. 14-day free trial, no card.',
                        'og': 'Fold POS for dry cleaners',
                        'hero': {'eyebrow': 'Point of sale for dry cleaners',
                                 'h1': 'A dry cleaning POS for owners, by owners.',
                                 'lede': 'Garment tags, conveyor slots and per-piece tickets — with wash &amp; fold and pickup &amp; delivery on the same '
                                         'counter when you offer them.',
                                 'btns': [('https://pos.foldpos.com/signup', 'Start free trial'),
                                          ('mailto:contact@foldpos.com?subject=Fold%20POS%20demo', 'Book a demo')],
                                 'note': '14 days free · no card · runs in your browser, on Mac, Windows and iPad · talks back when you say “Hey Fold”'},
                        'voice': {'eyebrow': 'Hey Fold · built into every plan',
                                  'h2': "The only POS you can talk to. Say the order — it's rung up, printed and tagged.",
                                  'lede': "Hands full of someone's laundry? Talk to the counter. Fold listens for its name, takes the order down, confirms it "
                                          'back to you, and sends the receipt and garment tags to the printer.',
                                  'pts': ['Say “Hey Fold”, press Caps Lock or tap the orb; it stays quiet until called',
                                          'Customer lookup, order status and production updates by voice',
                                          'Works on the browser, Mac and Windows builds with a plain microphone'],
                                  'rows': [('You', 'you', 'Hey Fold — new order for Maria Garcia. Two bags wash and fold, one comforter, pickup Thursday.'),
                                           ('Fold', 'fold', 'Got it. Maria Garcia — 2 bags wash &amp; fold, 1 comforter, due Thursday. $46.50. Print and tag?'),
                                           ('You', 'you', 'Yes.'),
                                           ('Print',
                                            'print',
                                            'Receipt #WNF-0417 · customer + store copy → Epson TM-T20<br/>Tags 1/3 · 2/3 · 3/3 → Zebra heat-seal')]},
                        'switch': {'eyebrow': 'Built for how your shop works',
                                   'h2': 'What a dry cleaner gets on day one.',
                                   'lede': 'Choose “Dry cleaner” at sign-up and this is the POS you see — the tools below and nothing that gets in the way. '
                                           'Change it any time in Settings.',
                                   'q': 'Not a dry cleaner?',
                                   'links': [('laundromats', 'For laundromats'), ('alterations', 'For tailors')]},
                        'chapters': [{'eyebrow': 'Dry cleaning',
                                      'h2': 'Every garment gets a tag. Every order gets a slot.',
                                      'lede': 'Itemize by the piece, note the stain, heat-seal a barcode on each garment, hang the order on the conveyor — and '
                                              'Fold POS remembers where it is until the customer walks in.',
                                      'pts': ['Per-piece tickets with photos, stain and damage notes',
                                              'Heat-seal tags numbered 1/8 … 8/8 with lot number and due day',
                                              'Conveyor slot assigned at check-in, freed at hand-over; find any order by scanning its ticket',
                                              'Alterations priced per task on the same ticket',
                                              '<span>Sending work to a plant? <a href="/plants">Every piece is counted there and back</a></span>'],
                                      'fact': None,
                                      'shots': [('Order details',
                                                 'assets/img/order-detail.webp',
                                                 'Order ticket with itemized garments, customer details, notes and photos')]},
                                     {'eyebrow': 'Wash &amp; fold · drop-off laundry',
                                      'h2': 'Ring it up the way the customer describes it.',
                                      'lede': '“Two bags, one comforter, rush it.” Weigh a bag, add a per-piece item, toggle express — and the price is right '
                                              "before you've finished talking.",
                                      'pts': ['By the pound with a minimum, by the bag, or by the piece, on one order',
                                              'Express fees, discounts and per-customer default pricing applied automatically',
                                              'Lives beside dry cleaning on the same counter — one customer, one ticket, two services',
                                              'Find a returning customer by name, phone or barcode scan mid-order',
                                              'Cash, card or pay-on-delivery; split a payment across two'],
                                      'fact': ('Two receipts, one tap.',
                                               'A customer copy and a store copy print the moment you submit — on the impact or thermal printer you already '
                                               'own.'),
                                      'shots': [('Check in · Wash & fold',
                                                 'assets/img/order-intake.webp',
                                                 'Check-in screen with wash and fold items and an order summary')]},
                                     {'eyebrow': 'Orders',
                                      'h2': 'Every order has a column. Every column has a count.',
                                      'lede': 'Orders move left to right through inspection &amp; tagging, cleaning, pressing and completed, so nothing sits '
                                              'forgotten on a rail.',
                                      'pts': ['Separate boards for wash &amp; fold, dry cleaning and alterations',
                                              'Express orders flagged in red, due dates on every card',
                                              'Assign a presser or seamstress in one tap',
                                              'Photos, notes and price changes stay on the ticket'],
                                      'fact': None,
                                      'shots': [('Orders · Dry cleaning',
                                                 'assets/img/orders-board.webp',
                                                 'Dry cleaning workflow board: to-do, inspection and tagging, dry cleaning, ironing, completed')]}],
                        'shared': {'eyebrow': 'The same for every shop',
                                   'h2': 'Whatever you clean, the back office is the same.',
                                   'lede': 'Customers, staff, marketing, printing, reports and payments work identically for a laundromat, a dry cleaner or a '
                                           'tailor — so a mixed shop never runs two systems.',
                                   'blocks': [{'eyebrow': 'Marketing',
                                               'h2': 'Reach customers before they think to call.',
                                               'lede': 'Automated flows that fire on their own — a thank-you after the first order, a nudge at 45 days quiet, '
                                                       'a birthday treat — plus SMS, email and push campaigns to segments Fold POS builds for you.',
                                               'pts': ['Flows triggered by first order, order completed, inactivity, birthday',
                                                       'Segments by spend, service mix and last visit, updated automatically',
                                                       '“Orders not collected” reminders in one click from Reports',
                                                       'Delivery and reply tracking on every campaign']},
                                              {'eyebrow': 'Staff',
                                               'h2': 'A clean handoff every time the shift changes.',
                                               'lede': 'Staff clock in and out on the same screen they ring orders on. Roles decide what each person can open. '
                                                       'The morning shift sees exactly what happened overnight.',
                                               'pts': ['Clock-in, breaks and clock-out tied to each employee',
                                                       'Roles and permissions per module, an audit log of who changed what',
                                                       'Shift statistics: orders, revenue and service mix per person',
                                                       'Built-in team chat and notifications']}]},
                        'tickets': {'eyebrow': 'Receipts &amp; tags',
                                    'h2': 'Prints on the printers you already own.',
                                    'lede': 'Claim tickets on the impact printer, garment tags on the heat-seal printer — Fold Print Agent pairs with a '
                                            'six-digit code and keeps them printing from any browser tab or the desktop app.',
                                    'pts': ['Epson TM-T20, Bixolon SRP-275, Star and Zebra out of the box',
                                            'Lot number, piece count, customer, due day and barcode on every tag',
                                            'Permanent heat-sealed barcodes for regulars: scan the garment, it knows the customer',
                                            'Reprint any receipt or tag from the print queue'],
                                    'paper': '<div class="receipt"> <div class="row"><span>FOLD POS · DOWNTOWN</span><span>DC-0417</span></div> <div '
                                             'class="big">THU 11</div> <div class="row"><span>MARIA GARCIA</span><span>···3021</span></div> <hr/> <div '
                                             'class="row"><span>2× WASH &amp; FOLD BAG</span><span>32.00</span></div> <div class="row"><span>1× '
                                             'COMFORTER</span><span>14.50</span></div> <div class="row"><span>PIECES</span><span>3</span></div> <hr/> <div '
                                             'class="row"><span>DUE</span><span><b>$46.50</b></span></div> <div class="bar"></div> <div '
                                             'style="text-align:center">CUSTOMER COPY</div> </div> <div class="tagstack"> <div '
                                             'class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>COMFORTER · WHITE</div><div '
                                             'class="n">1/3</div></div> <div class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>W&amp;F BAG</div><div '
                                             'class="n">2/3</div></div> <div class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>W&amp;F BAG</div><div '
                                             'class="n">3/3</div></div> </div>'},
                        'more': {'eyebrow': 'Also in every shop',
                                 'h2': "Everything a shop needs, nothing it doesn't.",
                                 'lede': "The parts you'd otherwise run in three other apps and a spreadsheet.",
                                 'cards': [('Customers &amp; B2B accounts',
                                            'History, preferences, addresses and notes at the counter. Tax id, payment terms and monthly invoicing for hotels, '
                                            'gyms and restaurants.'),
                                           ('Invoices',
                                            'Individual and business invoices with due dates, cancel-with-reason and a paid/pending view you can filter in a '
                                            'second.'),
                                           ('Reports you can actually read',
                                            'Sales by day, week and month, service mix, customers, costs, profit &amp; loss, orders not collected — and CSV '
                                            'export of any of them.'),
                                           ('Conveyor',
                                            'Slots by conveyor and line, assigned at check-in and freed at hand-over. Scan the ticket, the rail tells you '
                                            'where the order hangs.'),
                                           ('Payments built in',
                                            'Cash, card, pay-on-delivery and split tenders. On your own card processor, at your rates, with a payment link '
                                            'your customer can pay on their phone.'),
                                           ('Search anything, ⌘F',
                                            'One search box for customers, orders, tickets and settings. Keyboard-wedge barcode scanners just work.')]}},
 ('en', 'tailor'): {'slug': 'alterations',
                    'title': 'Alterations & tailoring POS — Fold POS',
                    'desc': 'Point of sale for alterations and tailoring shops: per-task pricing, measurements, photos and notes on every ticket, due-date '
                            'reminders, customers and staff. 14-day free trial, no card.',
                    'og': 'Fold POS for tailors',
                    'hero': {'eyebrow': 'Point of sale for alterations &amp; tailoring',
                             'h1': 'A tailoring POS for owners, by owners.',
                             'lede': 'Per-task pricing, measurements and photos on every ticket, due-date reminders — and none of the laundry screens in the '
                                     'way.',
                             'btns': [('https://pos.foldpos.com/signup', 'Start free trial'),
                                      ('mailto:contact@foldpos.com?subject=Fold%20POS%20demo', 'Book a demo')],
                             'note': '14 days free · no card · runs in your browser, on Mac, Windows and iPad · talks back when you say “Hey Fold”'},
                    'voice': {'eyebrow': 'Hey Fold · built into every plan',
                              'h2': "The only POS you can talk to. Say the order — it's rung up, printed and tagged.",
                              'lede': "Hands full of someone's laundry? Talk to the counter. Fold listens for its name, takes the order down, confirms it back "
                                      'to you, and sends the receipt and garment tags to the printer.',
                              'pts': ['Say “Hey Fold”, press Caps Lock or tap the orb; it stays quiet until called',
                                      'Customer lookup, order status and production updates by voice',
                                      'Works on the browser, Mac and Windows builds with a plain microphone'],
                              'rows': [('You', 'you', 'Hey Fold — new order for Maria Garcia. Two bags wash and fold, one comforter, pickup Thursday.'),
                                       ('Fold', 'fold', 'Got it. Maria Garcia — 2 bags wash &amp; fold, 1 comforter, due Thursday. $46.50. Print and tag?'),
                                       ('You', 'you', 'Yes.'),
                                       ('Print',
                                        'print',
                                        'Receipt #WNF-0417 · customer + store copy → Epson TM-T20<br/>Tags 1/3 · 2/3 · 3/3 → Zebra heat-seal')]},
                    'switch': {'eyebrow': 'Built for how your shop works',
                               'h2': 'What an alterations shop gets on day one.',
                               'lede': 'Choose “Alterations” at sign-up and this is the POS you see — the tools below and nothing that gets in the way. Change '
                                       'it any time in Settings.',
                               'q': 'Not an alterations shop?',
                               'links': [('laundromats', 'For laundromats'), ('dry-cleaners', 'For dry cleaners')]},
                    'chapters': [{'eyebrow': 'Alterations',
                                  'h2': 'Every job priced by the task, every garment on a ticket.',
                                  'lede': 'Hems, zippers, take-ins and custom work priced per task, with measurements, photos and notes on the ticket so '
                                          'nothing is lost between fittings.',
                                  'pts': ['Per-piece tickets with photos, stain and damage notes',
                                          'Heat-seal tags numbered 1/8 … 8/8 with lot number and due day',
                                          'Task pricing you set once and reuse: hem, taper, zipper, relining',
                                          'Add dry cleaning later with one switch in Settings'],
                                  'fact': None,
                                  'shots': [('Order details',
                                             'assets/img/order-detail.webp',
                                             'Order ticket with itemized garments, customer details, notes and photos')]},
                                 {'eyebrow': 'Orders',
                                  'h2': 'Every order has a column. Every column has a count.',
                                  'lede': 'Orders move left to right through fitting, in progress, pressing and ready, with the due date on every card.',
                                  'pts': ['Express orders flagged in red, due dates on every card',
                                          'Assign a presser or seamstress in one tap',
                                          'Photos, notes and price changes stay on the ticket'],
                                  'fact': None,
                                  'shots': [('Orders · Dry cleaning',
                                             'assets/img/orders-board.webp',
                                             'Dry cleaning workflow board: to-do, inspection and tagging, dry cleaning, ironing, completed')]}],
                    'shared': {'eyebrow': 'The same for every shop',
                               'h2': 'Whatever you clean, the back office is the same.',
                               'lede': 'Customers, staff, marketing, printing, reports and payments work identically for a laundromat, a dry cleaner or a '
                                       'tailor — so a mixed shop never runs two systems.',
                               'blocks': [{'eyebrow': 'Marketing',
                                           'h2': 'Reach customers before they think to call.',
                                           'lede': 'Automated flows that fire on their own — a thank-you after the first order, a nudge at 45 days quiet, a '
                                                   'birthday treat — plus SMS, email and push campaigns to segments Fold POS builds for you.',
                                           'pts': ['Flows triggered by first order, order completed, inactivity, birthday',
                                                   'Segments by spend, service mix and last visit, updated automatically',
                                                   '“Orders not collected” reminders in one click from Reports',
                                                   'Delivery and reply tracking on every campaign']},
                                          {'eyebrow': 'Staff',
                                           'h2': 'A clean handoff every time the shift changes.',
                                           'lede': 'Staff clock in and out on the same screen they ring orders on. Roles decide what each person can open. The '
                                                   'morning shift sees exactly what happened overnight.',
                                           'pts': ['Clock-in, breaks and clock-out tied to each employee',
                                                   'Roles and permissions per module, an audit log of who changed what',
                                                   'Shift statistics: orders, revenue and service mix per person',
                                                   'Built-in team chat and notifications']}]},
                    'tickets': {'eyebrow': 'Receipts &amp; tags',
                                'h2': 'Prints on the printers you already own.',
                                'lede': 'Claim tickets on the impact printer, garment tags on the heat-seal printer — Fold Print Agent pairs with a six-digit '
                                        'code and keeps them printing from any browser tab or the desktop app.',
                                'pts': ['Epson TM-T20, Bixolon SRP-275, Star and Zebra out of the box',
                                        'Lot number, piece count, customer, due day and barcode on every tag',
                                        'Permanent heat-sealed barcodes for regulars: scan the garment, it knows the customer',
                                        'Reprint any receipt or tag from the print queue'],
                                'paper': '<div class="receipt"> <div class="row"><span>FOLD POS · DOWNTOWN</span><span>DC-0417</span></div> <div '
                                         'class="big">THU 11</div> <div class="row"><span>MARIA GARCIA</span><span>···3021</span></div> <hr/> <div '
                                         'class="row"><span>2× WASH &amp; FOLD BAG</span><span>32.00</span></div> <div class="row"><span>1× '
                                         'COMFORTER</span><span>14.50</span></div> <div class="row"><span>PIECES</span><span>3</span></div> <hr/> <div '
                                         'class="row"><span>DUE</span><span><b>$46.50</b></span></div> <div class="bar"></div> <div '
                                         'style="text-align:center">CUSTOMER COPY</div> </div> <div class="tagstack"> <div '
                                         'class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>COMFORTER · WHITE</div><div class="n">1/3</div></div> '
                                         '<div class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>W&amp;F BAG</div><div class="n">2/3</div></div> '
                                         '<div class="heattag"><div><b>DC-0417</b><br/>GARCIA · THU 11<br/>W&amp;F BAG</div><div class="n">3/3</div></div> '
                                         '</div>'},
                    'more': {'eyebrow': 'Also in every shop',
                             'h2': "Everything a shop needs, nothing it doesn't.",
                             'lede': "The parts you'd otherwise run in three other apps and a spreadsheet.",
                             'cards': [('Customers &amp; B2B accounts',
                                        'History, preferences, addresses and notes at the counter. Tax id, payment terms and monthly invoicing for hotels, '
                                        'gyms and restaurants.'),
                                       ('Invoices',
                                        'Individual and business invoices with due dates, cancel-with-reason and a paid/pending view you can filter in a '
                                        'second.'),
                                       ('Reports you can actually read',
                                        'Sales by day, week and month, service mix, customers, costs, profit &amp; loss, orders not collected — and CSV export '
                                        'of any of them.'),
                                       ('Conveyor',
                                        'Slots by conveyor and line, assigned at check-in and freed at hand-over. Scan the ticket, the rail tells you where '
                                        'the order hangs.'),
                                       ('Payments built in',
                                        'Cash, card, pay-on-delivery and split tenders. On your own card processor, at your rates, with a payment link your '
                                        'customer can pay on their phone.'),
                                       ('Search anything, ⌘F',
                                        'One search box for customers, orders, tickets and settings. Keyboard-wedge barcode scanners just work.')]}},
 ('es', 'laundromat'): {'slug': 'laundromats',
                        'title': 'Software POS para lavanderías — Fold POS',
                        'desc': 'Punto de venta (POS) para lavanderías: lavado y doblado por libra, un mapa en vivo de cada lavadora y secadora, máquinas, '
                                'insumos, recogida y entrega y turnos del personal. Prueba gratis de 14 días, sin tarjeta.',
                        'og': 'Fold POS para lavanderías',
                        'hero': {'eyebrow': 'Punto de venta para lavanderías',
                                 'h1': 'Un POS de lavandería hecho por dueños, para dueños.',
                                 'lede': 'Lavado y doblado por libra en el mostrador, un mapa en vivo de cada lavadora y secadora del local y cada pedido '
                                         'seguido desde que lo dejan hasta que lo recogen.',
                                 'btns': [('https://pos.foldpos.com/signup', 'Empiece su prueba gratis'),
                                          ('mailto:contact@foldpos.com?subject=Fold%20POS%20demo', 'Agende una demo')],
                                 'note': '14 días gratis · sin tarjeta · funciona en su navegador, en Mac, Windows y iPad · le responde cuando dice “Hey '
                                         'Fold”'},
                        'voice': {'eyebrow': 'Hey Fold · incluido en todos los planes',
                                  'h2': 'El único POS con el que puede hablar. Diga el pedido — queda registrado, impreso y etiquetado.',
                                  'lede': '¿Tiene las manos llenas de ropa de un cliente? Háblele al mostrador. Fold escucha su nombre, toma el pedido, se lo '
                                          'confirma y envía el recibo y las etiquetas de las prendas a la impresora.',
                                  'pts': ['Diga “Hey Fold”, presione Bloq Mayús o toque el orbe; se queda en silencio hasta que lo llama',
                                          'Búsqueda de clientes, estado de pedidos y avances de producción por voz',
                                          'Funciona en el navegador y en las versiones para Mac y Windows con un micrófono común'],
                                  'rows': [('Usted',
                                            'you',
                                            'Hey Fold — nuevo pedido para María García. Dos bolsas de lavado y doblado, un edredón, lo recoge el jueves.'),
                                           ('Fold',
                                            'fold',
                                            'Entendido. María García — 2 bolsas de lavado y doblado, 1 edredón, para el jueves. $46.50. ¿Imprimo y etiqueto?'),
                                           ('Usted', 'you', 'Sí.'),
                                           ('Imprime',
                                            'print',
                                            'Recibo #WNF-0417 · copia del cliente + copia de la tienda → Epson TM-T20<br/>Etiquetas 1/3 · 2/3 · 3/3 → Zebra '
                                            'termoadhesiva')]},
                        'switch': {'eyebrow': 'Hecho para la forma en que trabaja su negocio',
                                   'h2': 'Lo que recibe una lavandería desde el primer día.',
                                   'lede': 'Elija “Lavandería” al registrarse y este es el POS que verá: las herramientas de abajo y nada que estorbe. '
                                           'Cámbielo cuando quiera en Ajustes.',
                                   'q': '¿No tiene una lavandería?',
                                   'links': [('/es/dry-cleaners', 'Para tintorerías'), ('/es/alterations', 'Para sastrerías')]},
                        'chapters': [{'eyebrow': 'Lavado y doblado · ropa por encargo',
                                      'h2': 'Cóbrelo tal como el cliente lo describe.',
                                      'lede': '“Dos bolsas, un edredón, y lo necesito urgente.” Pese una bolsa, agregue un artículo por pieza, active el '
                                              'exprés — y el precio está listo antes de que termine de hablar.',
                                      'pts': ['Por libra con mínimo, por bolsa o por pieza, en un mismo pedido',
                                              'Cargos exprés, descuentos y precios predeterminados por cliente aplicados automáticamente',
                                              'Cantidad de bolsas y peso en el ticket, para que un pedido de 3 bolsas regrese como 3 bolsas',
                                              'Encuentre a un cliente habitual por nombre, teléfono o código de barras sin salir del pedido',
                                              'Efectivo, tarjeta o pago contra entrega; divida un pago entre dos medios'],
                                      'fact': ('Dos recibos, un toque.',
                                               'Una copia para el cliente y otra para la tienda se imprimen en cuanto confirma — en la impresora de impacto o '
                                               'térmica que ya tiene.'),
                                      'shots': [('Recepción · Lavado y doblado',
                                                 '/assets/img/order-intake.webp',
                                                 'Pantalla de recepción con artículos de lavado y doblado y un resumen del pedido')]},
                                     {'eyebrow': 'Área de autoservicio',
                                      'h2': 'Su local se convierte en un mapa en vivo. Cada máquina guarda su historial.',
                                      'lede': 'Cada lavadora y secadora aparece en un plano. Asigne una máquina desde el mostrador y el plano muestra cuál '
                                              'está libre, cuál está en uso y cuánto le falta — para su personal y para el cliente que pregunta “¿está libre '
                                              'la 12?”. Toque cualquier máquina y ahí está toda su historia: ciclos, reparaciones, el técnico que la arregló '
                                              'la última vez.',
                                      'pts': ['Plano armado con sus marcas, tamaños, torres y zonas reales',
                                              'Ciclos por máquina por día — vea qué máquinas se pagan solas',
                                              'Asigne una máquina desde el mostrador con el tiempo y el tipo de lavado; agregue 15 minutos o termínela desde '
                                              'la misma pantalla',
                                              'Cada máquina en uso muestra de quién es la carga',
                                              'Historial de reparaciones por máquina con costo y tiempo fuera de servicio; agende al técnico desde la misma '
                                              'pantalla',
                                              'Recordatorios de mantenimiento preventivo según los ciclos realizados, no solo por calendario'],
                                      'fact': None,
                                      'shots': [('Lavandería · Piso principal',
                                                 '/assets/img/laundromat.webp',
                                                 'Plano de la lavandería con lavadoras y secadoras y su estado'),
                                                ('Gestión de máquinas',
                                                 '/assets/img/machines.webp',
                                                 'Lista de gestión de máquinas con el estado y el último servicio de cada una')]},
                                     {'eyebrow': 'Pedidos',
                                      'h2': 'Cada pedido tiene su columna. Cada columna, su conteo.',
                                      'lede': 'Los pedidos avanzan de izquierda a derecha por lavado, secado, doblado y completado, para que nada quede '
                                              'olvidado en una máquina.',
                                      'pts': ['Tableros separados para lavado y doblado, tintorería y arreglos',
                                              'Pedidos exprés marcados en rojo, fecha de entrega en cada tarjeta',
                                              'Asigne una lavadora o secadora con un toque; cuenta regresiva del ciclo en vivo en la tarjeta',
                                              'Fotos, notas y cambios de precio quedan en el ticket'],
                                      'fact': None,
                                      'shots': [('Pedidos · Lavado y doblado',
                                                 '/assets/img/kanban-board.webp',
                                                 'Tablero de flujo de trabajo con pedidos en las columnas por hacer, lavado, secado, planchado, doblado y '
                                                 'completado')]}],
                        'shared': {'eyebrow': 'Igual para todos los negocios',
                                   'h2': 'Limpie lo que limpie, la administración es la misma.',
                                   'lede': 'Clientes, personal, marketing, impresión, informes y pagos funcionan igual para una lavandería, una tintorería o '
                                           'una sastrería — así un negocio mixto nunca maneja dos sistemas.',
                                   'blocks': [{'eyebrow': 'Marketing',
                                               'h2': 'Llegue a sus clientes antes de que piensen en llamar.',
                                               'lede': 'Flujos automáticos que se activan solos — un agradecimiento tras el primer pedido, un recordatorio '
                                                       'después de 45 días sin visitas, un detalle de cumpleaños — además de campañas por SMS, correo '
                                                       'electrónico y notificaciones push a segmentos que Fold POS arma por usted.',
                                               'pts': ['Flujos que se activan por primer pedido, pedido completado, inactividad o cumpleaños',
                                                       'Segmentos por gasto, combinación de servicios y última visita, actualizados automáticamente',
                                                       'Recordatorios de “pedidos no recogidos” con un clic desde Informes',
                                                       'Seguimiento de entregas y respuestas en cada campaña']},
                                              {'eyebrow': 'Personal',
                                               'h2': 'Un relevo ordenado en cada cambio de turno.',
                                               'lede': 'El personal marca entrada y salida en la misma pantalla donde registra los pedidos. Los roles deciden '
                                                       'qué puede abrir cada persona. El turno de la mañana ve exactamente qué pasó durante la noche.',
                                               'pts': ['Entrada, descansos y salida vinculados a cada empleado',
                                                       'Roles y permisos por módulo, con un registro de auditoría de quién cambió qué',
                                                       'Estadísticas por turno: pedidos, ingresos y combinación de servicios por persona',
                                                       'Chat de equipo y notificaciones integrados']}]},
                        'tickets': {'eyebrow': 'Recibos y etiquetas',
                                    'h2': 'Imprime en las impresoras que ya tiene.',
                                    'lede': 'Tickets de retiro en la impresora de impacto, etiquetas de prendas en la termoselladora — Fold Print Agent se '
                                            'vincula con un código de seis dígitos y las mantiene imprimiendo desde cualquier pestaña del navegador o la app '
                                            'de escritorio.',
                                    'pts': ['Epson TM-T20, Bixolon SRP-275, Star y Zebra listas para usar',
                                            'Número de lote, cantidad de piezas, cliente, día de entrega y código de barras en cada etiqueta',
                                            'Códigos de barras termoadhesivos permanentes para clientes frecuentes: escanee la prenda y sabe de quién es',
                                            'Reimprima cualquier recibo o etiqueta desde la cola de impresión'],
                                    'paper': '<div class="receipt"> <div class="row"><span>FOLD POS · CENTRO</span><span>DC-0417</span></div> <div '
                                             'class="big">JUE 11</div> <div class="row"><span>MARÍA GARCÍA</span><span>···3021</span></div> <hr/> <div '
                                             'class="row"><span>2× BOLSA LAV. Y DOBL.</span><span>32.00</span></div> <div class="row"><span>1× '
                                             'EDREDÓN</span><span>14.50</span></div> <div class="row"><span>PIEZAS</span><span>3</span></div> <hr/> <div '
                                             'class="row"><span>A PAGAR</span><span><b>$46.50</b></span></div> <div class="bar"></div> <div '
                                             'style="text-align:center">COPIA DEL CLIENTE</div> </div> <div class="tagstack"> <div '
                                             'class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>EDREDÓN · BLANCO</div><div class="n">1/3</div></div> '
                                             '<div class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>BOLSA L&amp;D</div><div '
                                             'class="n">2/3</div></div> <div class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>BOLSA '
                                             'L&amp;D</div><div class="n">3/3</div></div> </div>'},
                        'more': {'eyebrow': 'También en todos los negocios',
                                 'h2': 'Todo lo que un negocio necesita, nada que no.',
                                 'lede': 'Lo que de otro modo manejaría con otras tres apps y una hoja de cálculo.',
                                 'cards': [('Clientes y cuentas empresariales (B2B)',
                                            'Historial, preferencias, direcciones y notas en el mostrador. Identificación fiscal, condiciones de pago y '
                                            'facturación mensual para hoteles, gimnasios y restaurantes.'),
                                           ('Facturas',
                                            'Facturas para particulares y empresas con fecha de vencimiento, anulación con motivo y una vista de '
                                            'pagadas/pendientes que filtra en un segundo.'),
                                           ('Informes que de verdad se entienden',
                                            'Ventas por día, semana y mes, combinación de servicios, clientes, costos, pérdidas y ganancias, pedidos no '
                                            'recogidos — y exportación a CSV de cualquiera de ellos.'),
                                           ('Transportador',
                                            'Espacios por transportador y línea, asignados en la recepción y liberados en la entrega. Escanee el ticket y el '
                                            'riel le indica dónde cuelga el pedido.'),
                                           ('Pagos integrados',
                                            'Efectivo, tarjeta, pago contra entrega y pagos divididos. Con su propio procesador de tarjetas, a sus tarifas, y '
                                            'con un enlace de pago que su cliente puede pagar desde el teléfono.'),
                                           ('Busque lo que sea, ⌘F',
                                            'Un solo buscador para clientes, pedidos, tickets y ajustes. Los lectores de códigos de barras que funcionan como '
                                            'teclado sirven sin configurar nada.')]}},
 ('es', 'drycleaner'): {'slug': 'dry-cleaners',
                        'title': 'Software POS para tintorerías y lavanderías en seco — Fold POS',
                        'desc': 'Punto de venta (POS) para tintorerías: tickets por prenda, etiquetas termoadhesivas, espacios en el transportador, arreglos '
                                'en el mismo ticket, lavado y doblado y recogida y entrega. Prueba gratis de 14 días, sin tarjeta.',
                        'og': 'Fold POS para tintorerías',
                        'hero': {'eyebrow': 'Punto de venta para tintorerías',
                                 'h1': 'Un POS de tintorería hecho por dueños, para dueños.',
                                 'lede': 'Etiquetas para cada prenda, espacios en el transportador y tickets por prenda — con lavado y doblado y recogida y '
                                         'entrega en el mismo mostrador, si los ofrece.',
                                 'btns': [('https://pos.foldpos.com/signup', 'Empiece su prueba gratis'),
                                          ('mailto:contact@foldpos.com?subject=Fold%20POS%20demo', 'Agende una demo')],
                                 'note': '14 días gratis · sin tarjeta · funciona en su navegador, en Mac, Windows y iPad · le responde cuando dice “Hey '
                                         'Fold”'},
                        'voice': {'eyebrow': 'Hey Fold · incluido en todos los planes',
                                  'h2': 'El único POS con el que puede hablar. Diga el pedido — queda registrado, impreso y etiquetado.',
                                  'lede': '¿Tiene las manos llenas de ropa de un cliente? Háblele al mostrador. Fold escucha su nombre, toma el pedido, se lo '
                                          'confirma y envía el recibo y las etiquetas de las prendas a la impresora.',
                                  'pts': ['Diga “Hey Fold”, presione Bloq Mayús o toque el orbe; se queda en silencio hasta que lo llama',
                                          'Búsqueda de clientes, estado de pedidos y avances de producción por voz',
                                          'Funciona en el navegador y en las versiones para Mac y Windows con un micrófono común'],
                                  'rows': [('Usted',
                                            'you',
                                            'Hey Fold — nuevo pedido para María García. Dos bolsas de lavado y doblado, un edredón, lo recoge el jueves.'),
                                           ('Fold',
                                            'fold',
                                            'Entendido. María García — 2 bolsas de lavado y doblado, 1 edredón, para el jueves. $46.50. ¿Imprimo y etiqueto?'),
                                           ('Usted', 'you', 'Sí.'),
                                           ('Imprime',
                                            'print',
                                            'Recibo #WNF-0417 · copia del cliente + copia de la tienda → Epson TM-T20<br/>Etiquetas 1/3 · 2/3 · 3/3 → Zebra '
                                            'termoadhesiva')]},
                        'switch': {'eyebrow': 'Hecho para la forma en que trabaja su negocio',
                                   'h2': 'Lo que recibe una tintorería desde el primer día.',
                                   'lede': 'Elija “Tintorería” al registrarse y este es el POS que verá: las herramientas de abajo y nada que estorbe. '
                                           'Cámbielo cuando quiera en Ajustes.',
                                   'q': '¿No tiene una tintorería?',
                                   'links': [('/es/laundromats', 'Para lavanderías'), ('/es/alterations', 'Para sastrerías')]},
                        'chapters': [{'eyebrow': 'Tintorería',
                                      'h2': 'Cada prenda lleva su etiqueta. Cada pedido, su lugar.',
                                      'lede': 'Detalle prenda por prenda, anote la mancha, selle un código de barras en cada prenda, cuelgue el pedido en el '
                                              'transportador — y Fold POS recuerda dónde está hasta que llega el cliente.',
                                      'pts': ['Tickets por prenda con fotos y notas de manchas y daños',
                                              'Etiquetas termoadhesivas numeradas 1/8 … 8/8 con número de lote y día de entrega',
                                              'Espacio en el transportador asignado en la recepción y liberado en la entrega; encuentre cualquier pedido '
                                              'escaneando su ticket',
                                              'Arreglos con precio por tarea en el mismo ticket',
                                              '<span>¿Envía trabajo a una planta? <a href="/es/plants">Cada pieza se cuenta a la ida y a la vuelta</a></span>'],
                                      'fact': None,
                                      'shots': [('Detalles del pedido',
                                                 '/assets/img/order-detail.webp',
                                                 'Ticket de pedido con prendas detalladas, datos del cliente, notas y fotos')]},
                                     {'eyebrow': 'Lavado y doblado · ropa por encargo',
                                      'h2': 'Cóbrelo tal como el cliente lo describe.',
                                      'lede': '“Dos bolsas, un edredón, y lo necesito urgente.” Pese una bolsa, agregue un artículo por pieza, active el '
                                              'exprés — y el precio está listo antes de que termine de hablar.',
                                      'pts': ['Por libra con mínimo, por bolsa o por pieza, en un mismo pedido',
                                              'Cargos exprés, descuentos y precios predeterminados por cliente aplicados automáticamente',
                                              'Convive con la tintorería en el mismo mostrador — un cliente, un ticket, dos servicios',
                                              'Encuentre a un cliente habitual por nombre, teléfono o código de barras sin salir del pedido',
                                              'Efectivo, tarjeta o pago contra entrega; divida un pago entre dos medios'],
                                      'fact': ('Dos recibos, un toque.',
                                               'Una copia para el cliente y otra para la tienda se imprimen en cuanto confirma — en la impresora de impacto o '
                                               'térmica que ya tiene.'),
                                      'shots': [('Recepción · Lavado y doblado',
                                                 '/assets/img/order-intake.webp',
                                                 'Pantalla de recepción con artículos de lavado y doblado y un resumen del pedido')]},
                                     {'eyebrow': 'Pedidos',
                                      'h2': 'Cada pedido tiene su columna. Cada columna, su conteo.',
                                      'lede': 'Los pedidos avanzan de izquierda a derecha por inspección y etiquetado, limpieza, planchado y completado, para '
                                              'que nada quede olvidado en un riel.',
                                      'pts': ['Tableros separados para lavado y doblado, tintorería y arreglos',
                                              'Pedidos exprés marcados en rojo, fecha de entrega en cada tarjeta',
                                              'Asigne un planchador o una costurera con un toque',
                                              'Fotos, notas y cambios de precio quedan en el ticket'],
                                      'fact': None,
                                      'shots': [('Pedidos · Tintorería',
                                                 '/assets/img/orders-board.webp',
                                                 'Tablero de flujo de tintorería: por hacer, inspección y etiquetado, lavado en seco, planchado, '
                                                 'completado')]}],
                        'shared': {'eyebrow': 'Igual para todos los negocios',
                                   'h2': 'Limpie lo que limpie, la administración es la misma.',
                                   'lede': 'Clientes, personal, marketing, impresión, informes y pagos funcionan igual para una lavandería, una tintorería o '
                                           'una sastrería — así un negocio mixto nunca maneja dos sistemas.',
                                   'blocks': [{'eyebrow': 'Marketing',
                                               'h2': 'Llegue a sus clientes antes de que piensen en llamar.',
                                               'lede': 'Flujos automáticos que se activan solos — un agradecimiento tras el primer pedido, un recordatorio '
                                                       'después de 45 días sin visitas, un detalle de cumpleaños — además de campañas por SMS, correo '
                                                       'electrónico y notificaciones push a segmentos que Fold POS arma por usted.',
                                               'pts': ['Flujos que se activan por primer pedido, pedido completado, inactividad o cumpleaños',
                                                       'Segmentos por gasto, combinación de servicios y última visita, actualizados automáticamente',
                                                       'Recordatorios de “pedidos no recogidos” con un clic desde Informes',
                                                       'Seguimiento de entregas y respuestas en cada campaña']},
                                              {'eyebrow': 'Personal',
                                               'h2': 'Un relevo ordenado en cada cambio de turno.',
                                               'lede': 'El personal marca entrada y salida en la misma pantalla donde registra los pedidos. Los roles deciden '
                                                       'qué puede abrir cada persona. El turno de la mañana ve exactamente qué pasó durante la noche.',
                                               'pts': ['Entrada, descansos y salida vinculados a cada empleado',
                                                       'Roles y permisos por módulo, con un registro de auditoría de quién cambió qué',
                                                       'Estadísticas por turno: pedidos, ingresos y combinación de servicios por persona',
                                                       'Chat de equipo y notificaciones integrados']}]},
                        'tickets': {'eyebrow': 'Recibos y etiquetas',
                                    'h2': 'Imprime en las impresoras que ya tiene.',
                                    'lede': 'Tickets de retiro en la impresora de impacto, etiquetas de prendas en la termoselladora — Fold Print Agent se '
                                            'vincula con un código de seis dígitos y las mantiene imprimiendo desde cualquier pestaña del navegador o la app '
                                            'de escritorio.',
                                    'pts': ['Epson TM-T20, Bixolon SRP-275, Star y Zebra listas para usar',
                                            'Número de lote, cantidad de piezas, cliente, día de entrega y código de barras en cada etiqueta',
                                            'Códigos de barras termoadhesivos permanentes para clientes frecuentes: escanee la prenda y sabe de quién es',
                                            'Reimprima cualquier recibo o etiqueta desde la cola de impresión'],
                                    'paper': '<div class="receipt"> <div class="row"><span>FOLD POS · CENTRO</span><span>DC-0417</span></div> <div '
                                             'class="big">JUE 11</div> <div class="row"><span>MARÍA GARCÍA</span><span>···3021</span></div> <hr/> <div '
                                             'class="row"><span>2× BOLSA LAV. Y DOBL.</span><span>32.00</span></div> <div class="row"><span>1× '
                                             'EDREDÓN</span><span>14.50</span></div> <div class="row"><span>PIEZAS</span><span>3</span></div> <hr/> <div '
                                             'class="row"><span>A PAGAR</span><span><b>$46.50</b></span></div> <div class="bar"></div> <div '
                                             'style="text-align:center">COPIA DEL CLIENTE</div> </div> <div class="tagstack"> <div '
                                             'class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>EDREDÓN · BLANCO</div><div class="n">1/3</div></div> '
                                             '<div class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>BOLSA L&amp;D</div><div '
                                             'class="n">2/3</div></div> <div class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>BOLSA '
                                             'L&amp;D</div><div class="n">3/3</div></div> </div>'},
                        'more': {'eyebrow': 'También en todos los negocios',
                                 'h2': 'Todo lo que un negocio necesita, nada que no.',
                                 'lede': 'Lo que de otro modo manejaría con otras tres apps y una hoja de cálculo.',
                                 'cards': [('Clientes y cuentas empresariales (B2B)',
                                            'Historial, preferencias, direcciones y notas en el mostrador. Identificación fiscal, condiciones de pago y '
                                            'facturación mensual para hoteles, gimnasios y restaurantes.'),
                                           ('Facturas',
                                            'Facturas para particulares y empresas con fecha de vencimiento, anulación con motivo y una vista de '
                                            'pagadas/pendientes que filtra en un segundo.'),
                                           ('Informes que de verdad se entienden',
                                            'Ventas por día, semana y mes, combinación de servicios, clientes, costos, pérdidas y ganancias, pedidos no '
                                            'recogidos — y exportación a CSV de cualquiera de ellos.'),
                                           ('Transportador',
                                            'Espacios por transportador y línea, asignados en la recepción y liberados en la entrega. Escanee el ticket y el '
                                            'riel le indica dónde cuelga el pedido.'),
                                           ('Pagos integrados',
                                            'Efectivo, tarjeta, pago contra entrega y pagos divididos. Con su propio procesador de tarjetas, a sus tarifas, y '
                                            'con un enlace de pago que su cliente puede pagar desde el teléfono.'),
                                           ('Busque lo que sea, ⌘F',
                                            'Un solo buscador para clientes, pedidos, tickets y ajustes. Los lectores de códigos de barras que funcionan como '
                                            'teclado sirven sin configurar nada.')]}},
 ('es', 'tailor'): {'slug': 'alterations',
                    'title': 'Software POS para sastrerías y arreglos de ropa — Fold POS',
                    'desc': 'Punto de venta (POS) para sastrerías y talleres de arreglos de ropa: precios por tarea, medidas, fotos y notas en cada ticket, '
                            'recordatorios de fecha de entrega, clientes y personal. Prueba gratis de 14 días, sin tarjeta.',
                    'og': 'Fold POS para sastrerías',
                    'hero': {'eyebrow': 'Punto de venta para arreglos y sastrería',
                             'h1': 'Un POS de sastrería hecho por dueños, para dueños.',
                             'lede': 'Precios por tarea, medidas y fotos en cada ticket, recordatorios de fecha de entrega — y ninguna pantalla de lavandería '
                                     'estorbando.',
                             'btns': [('https://pos.foldpos.com/signup', 'Empiece su prueba gratis'),
                                      ('mailto:contact@foldpos.com?subject=Fold%20POS%20demo', 'Agende una demo')],
                             'note': '14 días gratis · sin tarjeta · funciona en su navegador, en Mac, Windows y iPad · le responde cuando dice “Hey Fold”'},
                    'voice': {'eyebrow': 'Hey Fold · incluido en todos los planes',
                              'h2': 'El único POS con el que puede hablar. Diga el pedido — queda registrado, impreso y etiquetado.',
                              'lede': '¿Tiene las manos llenas de ropa de un cliente? Háblele al mostrador. Fold escucha su nombre, toma el pedido, se lo '
                                      'confirma y envía el recibo y las etiquetas de las prendas a la impresora.',
                              'pts': ['Diga “Hey Fold”, presione Bloq Mayús o toque el orbe; se queda en silencio hasta que lo llama',
                                      'Búsqueda de clientes, estado de pedidos y avances de producción por voz',
                                      'Funciona en el navegador y en las versiones para Mac y Windows con un micrófono común'],
                              'rows': [('Usted',
                                        'you',
                                        'Hey Fold — nuevo pedido para María García. Dos bolsas de lavado y doblado, un edredón, lo recoge el jueves.'),
                                       ('Fold',
                                        'fold',
                                        'Entendido. María García — 2 bolsas de lavado y doblado, 1 edredón, para el jueves. $46.50. ¿Imprimo y etiqueto?'),
                                       ('Usted', 'you', 'Sí.'),
                                       ('Imprime',
                                        'print',
                                        'Recibo #WNF-0417 · copia del cliente + copia de la tienda → Epson TM-T20<br/>Etiquetas 1/3 · 2/3 · 3/3 → Zebra '
                                        'termoadhesiva')]},
                    'switch': {'eyebrow': 'Hecho para la forma en que trabaja su negocio',
                               'h2': 'Lo que recibe una sastrería desde el primer día.',
                               'lede': 'Elija “Sastrería” al registrarse y este es el POS que verá: las herramientas de abajo y nada que estorbe. Cámbielo '
                                       'cuando quiera en Ajustes.',
                               'q': '¿No tiene una sastrería?',
                               'links': [('/es/laundromats', 'Para lavanderías'), ('/es/dry-cleaners', 'Para tintorerías')]},
                    'chapters': [{'eyebrow': 'Arreglos',
                                  'h2': 'Cada trabajo con precio por tarea, cada prenda en un ticket.',
                                  'lede': 'Dobladillos, cierres, ajustes y trabajos a medida con precio por tarea, con medidas, fotos y notas en el ticket '
                                          'para que nada se pierda entre pruebas.',
                                  'pts': ['Tickets por prenda con fotos y notas de manchas y daños',
                                          'Etiquetas termoadhesivas numeradas 1/8 … 8/8 con número de lote y día de entrega',
                                          'Precios por tarea que define una vez y reutiliza: dobladillo, entallado, cierre, cambio de forro',
                                          'Agregue tintorería más adelante con un solo interruptor en Ajustes'],
                                  'fact': None,
                                  'shots': [('Detalles del pedido',
                                             '/assets/img/order-detail.webp',
                                             'Ticket de pedido con prendas detalladas, datos del cliente, notas y fotos')]},
                                 {'eyebrow': 'Pedidos',
                                  'h2': 'Cada pedido tiene su columna. Cada columna, su conteo.',
                                  'lede': 'Los pedidos avanzan de izquierda a derecha por prueba, en proceso, planchado y listo, con la fecha de entrega en '
                                          'cada tarjeta.',
                                  'pts': ['Pedidos exprés marcados en rojo, fecha de entrega en cada tarjeta',
                                          'Asigne un planchador o una costurera con un toque',
                                          'Fotos, notas y cambios de precio quedan en el ticket'],
                                  'fact': None,
                                  'shots': [('Pedidos · Tintorería',
                                             '/assets/img/orders-board.webp',
                                             'Tablero de flujo de tintorería: por hacer, inspección y etiquetado, lavado en seco, planchado, completado')]}],
                    'shared': {'eyebrow': 'Igual para todos los negocios',
                               'h2': 'Limpie lo que limpie, la administración es la misma.',
                               'lede': 'Clientes, personal, marketing, impresión, informes y pagos funcionan igual para una lavandería, una tintorería o una '
                                       'sastrería — así un negocio mixto nunca maneja dos sistemas.',
                               'blocks': [{'eyebrow': 'Marketing',
                                           'h2': 'Llegue a sus clientes antes de que piensen en llamar.',
                                           'lede': 'Flujos automáticos que se activan solos — un agradecimiento tras el primer pedido, un recordatorio después '
                                                   'de 45 días sin visitas, un detalle de cumpleaños — además de campañas por SMS, correo electrónico y '
                                                   'notificaciones push a segmentos que Fold POS arma por usted.',
                                           'pts': ['Flujos que se activan por primer pedido, pedido completado, inactividad o cumpleaños',
                                                   'Segmentos por gasto, combinación de servicios y última visita, actualizados automáticamente',
                                                   'Recordatorios de “pedidos no recogidos” con un clic desde Informes',
                                                   'Seguimiento de entregas y respuestas en cada campaña']},
                                          {'eyebrow': 'Personal',
                                           'h2': 'Un relevo ordenado en cada cambio de turno.',
                                           'lede': 'El personal marca entrada y salida en la misma pantalla donde registra los pedidos. Los roles deciden qué '
                                                   'puede abrir cada persona. El turno de la mañana ve exactamente qué pasó durante la noche.',
                                           'pts': ['Entrada, descansos y salida vinculados a cada empleado',
                                                   'Roles y permisos por módulo, con un registro de auditoría de quién cambió qué',
                                                   'Estadísticas por turno: pedidos, ingresos y combinación de servicios por persona',
                                                   'Chat de equipo y notificaciones integrados']}]},
                    'tickets': {'eyebrow': 'Recibos y etiquetas',
                                'h2': 'Imprime en las impresoras que ya tiene.',
                                'lede': 'Tickets de retiro en la impresora de impacto, etiquetas de prendas en la termoselladora — Fold Print Agent se vincula '
                                        'con un código de seis dígitos y las mantiene imprimiendo desde cualquier pestaña del navegador o la app de '
                                        'escritorio.',
                                'pts': ['Epson TM-T20, Bixolon SRP-275, Star y Zebra listas para usar',
                                        'Número de lote, cantidad de piezas, cliente, día de entrega y código de barras en cada etiqueta',
                                        'Códigos de barras termoadhesivos permanentes para clientes frecuentes: escanee la prenda y sabe de quién es',
                                        'Reimprima cualquier recibo o etiqueta desde la cola de impresión'],
                                'paper': '<div class="receipt"> <div class="row"><span>FOLD POS · CENTRO</span><span>DC-0417</span></div> <div class="big">JUE '
                                         '11</div> <div class="row"><span>MARÍA GARCÍA</span><span>···3021</span></div> <hr/> <div class="row"><span>2× BOLSA '
                                         'LAV. Y DOBL.</span><span>32.00</span></div> <div class="row"><span>1× EDREDÓN</span><span>14.50</span></div> <div '
                                         'class="row"><span>PIEZAS</span><span>3</span></div> <hr/> <div class="row"><span>A '
                                         'PAGAR</span><span><b>$46.50</b></span></div> <div class="bar"></div> <div style="text-align:center">COPIA DEL '
                                         'CLIENTE</div> </div> <div class="tagstack"> <div class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>EDREDÓN '
                                         '· BLANCO</div><div class="n">1/3</div></div> <div class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>BOLSA '
                                         'L&amp;D</div><div class="n">2/3</div></div> <div class="heattag"><div><b>DC-0417</b><br/>GARCÍA · JUE 11<br/>BOLSA '
                                         'L&amp;D</div><div class="n">3/3</div></div> </div>'},
                    'more': {'eyebrow': 'También en todos los negocios',
                             'h2': 'Todo lo que un negocio necesita, nada que no.',
                             'lede': 'Lo que de otro modo manejaría con otras tres apps y una hoja de cálculo.',
                             'cards': [('Clientes y cuentas empresariales (B2B)',
                                        'Historial, preferencias, direcciones y notas en el mostrador. Identificación fiscal, condiciones de pago y '
                                        'facturación mensual para hoteles, gimnasios y restaurantes.'),
                                       ('Facturas',
                                        'Facturas para particulares y empresas con fecha de vencimiento, anulación con motivo y una vista de '
                                        'pagadas/pendientes que filtra en un segundo.'),
                                       ('Informes que de verdad se entienden',
                                        'Ventas por día, semana y mes, combinación de servicios, clientes, costos, pérdidas y ganancias, pedidos no recogidos '
                                        '— y exportación a CSV de cualquiera de ellos.'),
                                       ('Transportador',
                                        'Espacios por transportador y línea, asignados en la recepción y liberados en la entrega. Escanee el ticket y el riel '
                                        'le indica dónde cuelga el pedido.'),
                                       ('Pagos integrados',
                                        'Efectivo, tarjeta, pago contra entrega y pagos divididos. Con su propio procesador de tarjetas, a sus tarifas, y con '
                                        'un enlace de pago que su cliente puede pagar desde el teléfono.'),
                                       ('Busque lo que sea, ⌘F',
                                        'Un solo buscador para clientes, pedidos, tickets y ajustes. Los lectores de códigos de barras que funcionan como '
                                        'teclado sirven sin configurar nada.')]}}}

NEW = '/assets/img/new/{}.webp'
# old screenshot -> the real screen that replaces it, per shop
SCREEN = {
    ('laundromat', '/assets/img/order-intake.webp'): 'checkin-wf', ('drycleaner', '/assets/img/order-intake.webp'): 'checkin-wf',
    ('laundromat', '/assets/img/laundromat.webp'): 'floor',
    ('laundromat', '/assets/img/kanban-board.webp'): 'orders-wf',
    ('drycleaner', '/assets/img/order-detail.webp'): 'checkin-dc', ('tailor', '/assets/img/order-detail.webp'): 'checkin-alt',
    ('drycleaner', '/assets/img/orders-board.webp'): 'orders-dc', ('tailor', '/assets/img/orders-board.webp'): 'orders-alt',
}
ICON = {'checkin-wf': 'scan', 'floor': 'store', 'orders-wf': 'layers', 'checkin-dc': 'tag', 'checkin-alt': 'tag',
        'orders-dc': 'layers', 'orders-alt': 'layers'}
ALT = {
    'dashboard':   ('The Fold POS dashboard: revenue, today’s orders, orders ready for pickup and machines in use',
                    'El panel de Fold POS: ingresos, pedidos de hoy, pedidos listos para recoger y máquinas en uso'),
    'checkin-wf':  ('Check in: wash and fold items priced by the pound, with the order summary on the right',
                    'Recepción: artículos de lavado y doblado con precio por libra y el resumen del pedido a la derecha'),
    'floor':       ('The floor map: washers and dryers laid out as they stand, each showing whether it is free',
                    'El plano del local: lavadoras y secadoras tal como están, cada una indicando si está libre'),
    'orders-wf':   ('The wash and fold orders board: To-do, Washing, Drying, Ironing, Folding and Completed',
                    'El tablero de pedidos de lavado y doblado: por hacer, lavado, secado, planchado, doblado y terminado'),
    'checkin-dc':  ('Dry cleaning check in: each piece priced on its own, with the order summary',
                    'Recepción de tintorería: cada prenda con su precio y el resumen del pedido'),
    'checkin-alt': ('Alterations check in: each task priced on its own, with the order summary',
                    'Recepción de arreglos: cada tarea con su precio y el resumen del pedido'),
    'orders-dc':   ('The dry cleaning orders board, with an order ready for inspection',
                    'El tablero de pedidos de tintorería, con un pedido listo para inspección'),
    'orders-alt':  ('The alterations orders board, with each order’s tasks and due date',
                    'El tablero de pedidos de arreglos, con las tareas y la fecha de entrega de cada pedido'),
    'marketing':   ('Marketing: automated campaigns with their type and results',
                    'Marketing: campañas automáticas con su tipo y sus resultados'),
}
FT = '/assets/img/fold-time/'
STAFF_ART = {
    'en': (f'<div class="ff-pair"><img class="ff-dev" src="{FT}device-front-cut.webp" width="456" height="548" loading="lazy" decoding="async" alt="Fold Time wall device: Tap your phone">'
           f'<img class="ff-phone" src="{FT}staff-clocked-in.webp" width="520" height="885" loading="lazy" decoding="async" alt="Phone screen after a tap on Fold Time: Clocked in, 11:32 AM, with Undo"></div>'),
    'es': (f'<div class="ff-pair"><img class="ff-dev" src="{FT}device-front-cut.webp" width="456" height="548" loading="lazy" decoding="async" alt="Dispositivo de pared Fold Time: Toque con su teléfono">'
           f'<img class="ff-phone" src="{FT}staff-my-hours-es.webp" width="520" height="885" loading="lazy" decoding="async" alt="Mis horas en un teléfono: este periodo de pago, día por día"></div>'),
}
WORDS = {
    'en': dict(home='/', pre='', start='Start free', talk='Talk to us', talk_href='/contact',
               crumb={'laundromat': 'Laundromats', 'drycleaner': 'Dry cleaners', 'tailor': 'Tailors'},
               fold_time='<a href="/fold-time">Fold Time</a>: staff tap their phone on the wall device to clock in, take breaks and clock out. No app. On Growth and Pro, your first device free',
               plans_h2='Pick the plan that matches how many doors you run.',
               plans='Starter $79, Growth $149 and Pro $249 a month. Month to month, 14 days free, no card up front.',
               plans_btn='Compare the plans', plans_href='/pricing'),
    'es': dict(home='/es/', pre='/es', start='Empiece gratis', talk='Hable con nosotros', talk_href='/es/contact',
               crumb={'laundromat': 'Lavanderías', 'drycleaner': 'Tintorerías', 'tailor': 'Sastrerías'},
               fold_time='<a href="/es/fold-time">Fold Time</a>: el personal toca el dispositivo de pared con su teléfono para marcar entrada, descansos y salida. Sin app. En Growth y Pro, el primer dispositivo gratis',
               plans_h2='Elija el plan según cuántas sucursales tenga.',
               plans='Starter $79, Growth $149 y Pro $249 al mes (USD). Mes a mes, 14 días gratis, sin tarjeta para empezar.',
               plans_btn='Comparar los planes', plans_href='/es/pricing'),
}

STYLE = """<style>
.sp-acts{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap}
.sp-fine{margin-top:16px;font-size:14px;color:var(--ink-3)}
.sp-hero{padding:8px 0 24px}
.sp-pts{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:10px;color:var(--ink-2);font-size:15px;max-width:60ch}
.sp-pts li{display:flex;gap:10px;align-items:flex-start}
.sp-pts svg{color:var(--brand);width:18px;height:18px;margin-top:3px;flex:none}
.sp-pts a{font-weight:600}
.sp-note{margin-top:18px;padding-top:16px;border-top:1px solid var(--line);color:var(--ink-2);font-size:15px;max-width:60ch}
.sp-note b{color:var(--ink)}
.sp-sec .tagsplit{align-items:center}
.sp-alt .tagsplit>div:first-child{order:2}
.sp-links{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:20px;color:var(--ink-3);font-size:15px}
.ff-pair{display:flex;align-items:center;justify-content:center;gap:28px;padding:36px 24px;border-radius:22px;background:var(--fog)}
.ff-dev{width:44%;max-width:230px;height:auto;filter:drop-shadow(0 22px 26px rgba(20,27,61,.18))}
.ff-phone{width:42%;max-width:220px;height:auto;border-radius:26px;border:1px solid var(--line);background:#fff;box-shadow:0 26px 48px -28px rgba(20,27,61,.55)}
.values.three{grid-template-columns:repeat(3,1fr)}
.values .fact p{color:var(--ink-2);font-size:15px;line-height:1.55;margin-top:6px}
/* Hey Fold: navy, with Hey Fold's purple and green as a low light along the bottom edge */
.sp-voice{position:relative;background:#0e1730;color:#fff;overflow:hidden;isolation:isolate}
.sp-voice::after{content:"";position:absolute;left:0;right:0;bottom:0;height:160px;z-index:-1;pointer-events:none;
  background:radial-gradient(40% 90% at 22% 100%,rgba(124,92,255,.42),transparent 70%),radial-gradient(40% 90% at 52% 100%,rgba(18,168,111,.32),transparent 70%),radial-gradient(40% 90% at 80% 100%,rgba(167,139,250,.36),transparent 70%)}
.sp-voice h2{color:#fff}
.sp-voice .sub{color:#c7d0ea}
.sp-voice .sp-pts{color:#c7d0ea}
.sp-voice .sp-pts svg{color:#a78bfa}
.sp-voice .lbl{color:#a78bfa}
.sp-tr{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:20px}
.sp-tr .row{display:flex;gap:12px;align-items:flex-start;padding:8px 0}
.sp-tr .who{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#a3aed0;width:52px;flex:none;padding-top:9px}
.sp-tr .bubble{background:rgba(255,255,255,.1);border-radius:14px;padding:10px 14px;color:#fff;font-size:15px;line-height:1.5}
.sp-tr .fold .bubble{background:#1e5eff}
.sp-tr .print .bubble{background:transparent;border:1px dashed rgba(255,255,255,.3);color:#c7d0ea;font:500 12.5px/1.6 ui-monospace,"SF Mono",Menlo,Consolas,monospace}
/* receipt and tags, drawn the way they print */
.paper{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap;justify-content:center}
.receipt{background:#fff;width:250px;padding:18px 16px;font:500 12px/1.55 ui-monospace,"SF Mono",Menlo,Consolas,monospace;color:var(--ink);box-shadow:0 16px 40px -18px rgba(14,23,48,.35);border:1px solid var(--line);border-radius:4px}
.receipt .big{font-size:26px;font-weight:600;margin:6px 0}
.receipt .row{display:flex;justify-content:space-between;gap:10px}
.receipt hr{border:0;border-top:1px dashed #cbd0dc;margin:8px 0}
.receipt .bar{height:34px;margin:8px 0 4px;background:repeating-linear-gradient(90deg,var(--ink) 0 2px,transparent 2px 4px,var(--ink) 4px 5px,transparent 5px 8px,var(--ink) 8px 11px,transparent 11px 13px)}
.tagstack{display:flex;flex-direction:column;gap:10px}
.heattag{background:#fff;border:1px solid var(--line);border-radius:4px;width:230px;padding:8px 12px;font:500 11px/1.45 ui-monospace,"SF Mono",Menlo,Consolas,monospace;display:grid;grid-template-columns:1fr auto;gap:6px;box-shadow:0 8px 20px -14px rgba(14,23,48,.35)}
.heattag b{font-size:13px}
.heattag .n{font-size:15px;font-weight:600;align-self:center}
@media (max-width:900px){.sp-alt .tagsplit>div:first-child{order:0}.values.three{grid-template-columns:1fr}}
</style>"""


def _label(icon, text, cls=''):
    return f'<div class="lbl" style="{LABEL_STYLE}">{ic(icon)}<span>{text}</span></div>'


def _img(key, lang):
    alt = ALT[key][0 if lang == 'en' else 1]
    return (f'<img src="{NEW.format(key)}" alt="{esc(alt)}" width="1600" height="1000" loading="lazy" decoding="async" style="{IMG_STYLE}">')


def _split(sid, icon, label, h2, lede, pts, art, note='', alt=False, cls='sp-sec'):
    lis = ''.join(f'<li>{ic("check")}<span>{p}</span></li>' for p in pts)
    return (f'<section class="section {cls}{" sp-alt" if alt else ""}"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}><div class="wrap"><div class="tagsplit">'
            f'<div>{_label(icon, label)}<h2>{h2}</h2>' + (f'<p class="sub" style="margin-bottom:0">{lede}</p>' if lede else '') +
            (f'<ul class="sp-pts">{lis}</ul>' if pts else '') + note + f'</div><div>{art}</div></div></div></section>')


def shop(key, lang):
    d, w = DATA[(lang, key)], WORDS[lang]
    h = d['hero']
    out = [STYLE, f"""<section class="phead"><div class="wrap">
  <div class="crumbs"><a href="{w['home']}">Fold POS</a> › {w['crumb'][key]}</div>
  <h1>{h['h1']}</h1>
  <p class="lede">{h['lede']}</p>
  <div class="sp-acts"><a class="btn btn-primary" href="https://pos.foldpos.com/signup">{w['start']}</a><a class="btn btn-ghost" href="{w['talk_href']}">{w['talk']}</a></div>
  <p class="sp-fine">{h['note']}</p>
</div></section>
<section class="sp-hero"><div class="wrap">{_img('dashboard', lang)}</div></section>"""]
    # Hey Fold
    v = d['voice']
    rows = ''.join(f'<div class="row {kind}"><span class="who">{who}</span><div class="bubble">{txt}</div></div>' for who, kind, txt in v['rows'])
    out.append(_split('voice', 'mic', v['eyebrow'], v['h2'], v['lede'], v['pts'],
                      f'<div class="sp-tr" aria-label="{"Example voice order" if lang == "en" else "Ejemplo de un pedido por voz"}">{rows}</div>',
                      cls='sp-voice'))
    # what this kind of shop gets
    s = d['switch']
    links = ''.join(f'<a class="btn btn-ghost" href="{w["pre"]}/{href.split("/")[-1]}">{txt}</a>' for href, txt in s['links'])
    out.append(f"""<section class="section" id="intro"><div class="wrap narrow">
  <h2>{s['h2']}</h2><p class="sub" style="margin-bottom:0">{s['lede']}</p>
  <div class="sp-links"><span>{s['q']}</span>{links}</div>
</div></section>""")
    # chapters, one real screen each
    alt = False
    for i, c in enumerate(d['chapters']):
        scr = SCREEN[(key, '/' + c['shots'][0][1].lstrip('/'))]
        note = f'<p class="sp-note"><b>{c["fact"][0]}</b> {c["fact"][1]}</p>' if c['fact'] else ''
        out.append(_split('counter' if i == 0 else None, ICON[scr], c['eyebrow'], c['h2'], c['lede'], c['pts'], _img(scr, lang), note, alt))
        alt = not alt
    # the back office, the same for every shop
    sh = d['shared']
    out.append(f"""<section class="section" id="shared" style="padding-bottom:0"><div class="wrap narrow">
  <h2>{sh['h2']}</h2><p class="sub" style="margin-bottom:0">{sh['lede']}</p>
</div></section>""")
    mk, st = sh['blocks']
    out.append(_split(None, 'mail', mk['eyebrow'], mk['h2'], mk['lede'], mk['pts'], _img('marketing', lang), alt=alt))
    out.append(_split(None, 'users', st['eyebrow'], st['h2'], st['lede'], [w['fold_time']] + st['pts'], STAFF_ART[lang], alt=not alt))
    # receipts and tags, drawn as they print
    t = d['tickets']
    out.append(_split('tags', 'printer', t['eyebrow'], t['h2'], t['lede'], t['pts'], f'<div class="paper" aria-hidden="true">{t["paper"]}</div>', alt=alt))
    # everything else
    m = d['more']
    cards = ''.join(f'<div class="fact"><b>{b}</b><p>{p}</p></div>' for b, p in m['cards'])
    out.append(f"""<section class="section" id="more"><div class="wrap">
  <h2>{m['h2']}</h2><p class="sub">{m['lede']}</p>
  <div class="values three">{cards}</div>
</div></section>
<section class="section" id="pricing" style="padding-top:0"><div class="wrap narrow">
  <h2>{w['plans_h2']}</h2><p class="sub" style="margin-bottom:0">{w['plans']}</p>
  <p style="margin-top:20px"><a class="btn btn-ghost" href="{w['plans_href']}">{w['plans_btn']}</a></p>
</div></section>""")
    slug = d['slug'] if lang == 'en' else 'es/' + d['slug']
    html_ = page(slug, d['title'], d['desc'], d['og'], w['crumb'][key], '\n'.join(out))
    if lang == 'es':
        for a, b in (('<html lang="en">', '<html lang="es">'), (BAND, BAND_ES), (f'"item": "{SITE}/"', f'"item": "{SITE}/es/"')):
            assert a in html_, a
            html_ = html_.replace(a, b, 1)
    return html_


def laundromats():
    return shop('laundromat', 'en')


def dry_cleaners():
    return shop('drycleaner', 'en')


def alterations():
    return shop('tailor', 'en')


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    langs = ['es'] if '--es' in sys.argv else ['en', 'es']
    for lang in langs:
        for key in ('laundromat', 'drycleaner', 'tailor'):
            slug = DATA[(lang, key)]['slug']
            path = slug if lang == 'en' else 'es/' + slug
            open(os.path.join(root, path + '.html'), 'w', encoding='utf-8').write(shop(key, lang))
            print('wrote', path)
