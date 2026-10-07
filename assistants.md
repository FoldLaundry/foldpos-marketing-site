# Connect an AI assistant to your store

> Canonical page: https://foldpos.com/assistants · Markdown mirror.

If you use an AI assistant such as Claude, you can let it look at your store in Fold POS. Ask it “how are we doing today?”, “which orders are late?” or “what needs me?” from wherever you are, and it answers from your own store’s records.

- **Owner only**: Only an owner can connect an assistant, see the list or remove one. Staff cannot.
- **It looks, unless you allow more**: Changes are off until you switch them on, and there are only three.
- **No extra cost**: It is not tied to a plan.

## What it can do: It answers from your own store’s records.

A connected assistant can look at:

- Today’s sales and how they were paid, and sales over a week, a month or a year, including sales tax.
- Orders: find one, see everything about it, see which are late and which are ready and waiting to be collected.
- Customers: find one, see their details, orders, store credit and notes.
- Machines: what is running, what is out of service, what maintenance is due.
- Supplies that are running low and what to reorder.
- The day’s pickups and deliveries, if your plan includes pickup & delivery.
- Who is on shift and the hours people worked, if your plan includes staff shifts.
- A short list of what needs your attention right now.

If it cannot read something, it tells you it could not. It does not show you a zero in its place.

## Changes: Three small changes, only if you allow them.

Changes are off until you switch them on, and each assistant also needs your permission to make them.

- Mark an order ready.
- Add a staff note to an order.
- Add a staff note to a customer’s file.
- Before every change the assistant is shown exactly what would happen and has to confirm it. It is told to show you first and wait for your yes.
- Every change appears under the bell at the counter and in your activity list.
- If your store sends a “your order is ready” text, marking an order ready sends it, the same as pressing Ready at the counter. Your staff can put the order back to In progress, but a text that went out cannot be taken back.
- A note an assistant adds cannot be edited or removed afterwards.

Fold POS cannot check that the assistant asked you, which is why the changes are kept this small.

## What it cannot do: It never moves money.

An assistant cannot:

- Take a payment, give a refund or a discount, or move money in any way.
- Cancel or delete an order, or change what is on one.
- Change your prices, your settings or your staff.
- See what your staff are paid.
- See card numbers. Fold POS does not store them.
- See any store but the one you connected it to.

In lists, customers’ phone numbers and emails are partly hidden. The assistant sees them in full only when it looks up one customer or one order.

## Connect: Connect by signing in.

Add the address in your assistant, then approve inside Fold POS.

- Step 1. In your assistant’s settings, add a custom connector. Some call it an MCP server.
- Step 2. Give it this address: https://app.foldpos.com/v1/mcp/store
- Step 3. The assistant sends you to Fold POS. Sign in the way you always do, if you are not signed in already.
- Step 4. Fold POS shows you what is asking for access. Check the name of the app, where you will be sent back to after you answer, and the store it is for.
- Step 5. If the assistant asked to make changes, choose whether to allow that. Then approve.

Where you will be sent back to is the part that cannot be faked. It should be the site of the assistant you are connecting. If the screen warns you that it does not recognise the app, or that the request was not started from your device, and you did not expect that, say no. Never approve a request that arrived as a link from someone else.

## Token: Or connect with a token.

Some desktop apps do not send you to Fold POS to approve. They ask for a token instead.

- Step 1. In Fold POS, open Settings › Assistants and create a token.
- Step 2. Give it a name you will recognise later, such as “Claude on my laptop”.
- Step 3. Choose how long it should last (up to 366 days, or no end date), and whether it may make changes.
- Step 4. Copy the token. It is shown once. Fold POS cannot show it to you again.
- Step 5. In your assistant’s settings, add a custom connector or MCP server with the address https://app.foldpos.com/v1/mcp/store and paste the token where it asks for a key or an authorization header.

Treat a token like a password. Anyone who has it can read your store’s orders, customers and sales. Do not paste it into a chat or an email. If you lose track of one, remove it and make a new one.

## Pause and remove: Pause, remove, and see what happened.

All in Settings › Assistants.

- Pause. One switch stops every connected assistant at once. Nothing is removed; switch it back on and they work again.
- Stop changes. A second switch decides whether assistants may make the three changes. Off means they can only look.
- Remove. Each connected assistant is listed with its name and when it was last used. Remove one and it stops working straight away.
- Activity. A list of what each assistant asked and what it changed, newest first, kept for 90 days. It shows which tool was used and when. It does not keep the answers, and it does not keep names, phone numbers or the text of notes.
- An email each time. Whenever an assistant is connected to your store, the person who connected it gets an email saying so.

A store can have 20 assistants connected at a time.

## Briefings and alerts: Or let Fold POS write to you.

You do not need a connected assistant for this. Fold POS itself can send you a short message about your store.

- A morning briefing. Yesterday’s sales and what needs you, at the time and on the days you pick.
- Alerts. A machine goes out of service, an order is two days late, or a supply runs low. Each one is announced once.
- Where to switch it on. Settings › Assistants › Briefings and alerts. It is off until you turn it on, and only an owner can.
- Where it goes. To the email on your account. The card shows where the next message will go, and “Send me a test” sends today’s briefing there now.
- Limits. At most 5 messages a day. No alerts between 9 pm and 7 am at your store; whatever is still true goes out in the morning. Several alerts at once arrive as one message.
- What a message contains. Counts, machine and supply names, and order numbers. Never a customer’s name, phone number or address.
- Language. English or Spanish, your choice.

Your store needs its time zone set in Settings › Business first, so the morning briefing arrives in your morning. The card also lets you choose text messages; until texting to owners is switched on, those go to your email as well, and the card says so.

## If someone else got in: If you think someone else got in.

Do these in order.

- Step 1. Open Settings › Assistants and remove any connection you do not recognise. If you are not sure which, pause all of them first.
- Step 2. Change your password. This disconnects every assistant you connected, so you will need to connect the ones you want again.
- Step 3. Look at the activity list to see what was asked.
- Step 4. Email [contact@foldpos.com](mailto:contact@foldpos.com) and tell us your store name.

Assistants connected by another owner of the store are not affected by your password change. Remove those from the list.

## Assistant questions

**Does this cost extra?** No. It is not tied to a plan. Two of the things an assistant can look at follow your plan: pickups and deliveries, and staff shifts.

**Can my manager set this up?** No. Only an owner can connect an assistant, see the list or remove one.

**Can Fold connect an assistant for me?** No. A member of Fold’s team helping you from our side can pause assistants or remove one, but cannot connect one or switch changes on. That has to be you, signed in as yourself.

**What language does it answer in?** Your assistant answers in the language you write in. The information it gets from Fold POS is in English.

**Can my customers use an assistant too?** Separately from all of this, a customer’s own assistant can book a pickup with a shop that has online booking switched on. It follows the same rules as your booking page, and the bell tells you when a booking came in that way.

## Where to next

- [For developers](https://foldpos.com/developers#store-mcp): The address, the tools and the rules.
- [Hey Fold](https://foldpos.com/hey-fold#briefings): Ask “what needs me?” out loud in Fold POS.
- [Online booking](https://foldpos.com/pickup-delivery#booking): The booking page your customers use.
- [Help center](https://foldpos.com/help): Short answers for the counter.

## More

- [Home](/fold-pos.md) · [Pricing](/pricing.md) · [FAQ](/faq.md) · [Help](/help.md) · [Contact](/contact.md) · [About](/about.md)
- [Printers](/printers.md) · [Store setup](/setup.md) · [Print helper](/download.md) · [All features](/features.md) · [Developers & AI](/developers.md)
- [Hey Fold](/hey-fold.md) · [Pickup & delivery](/pickup-delivery.md) · [Money at the counter](/counter-money.md) · [Plants & drop stores](/plants.md)
