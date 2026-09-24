# Fold print helper — print from any browser

> Canonical page: https://foldpos.com/download · Markdown mirror.

The Fold print helper is a small program for the counter computer. It starts when you sign in, finds the receipt and tag printers you already have, and prints whatever Fold POS sends — from Chrome, Edge or Firefox on Windows.

**Download for Windows** — 22 MB · Windows 10 and 11 · https://foldpos.com/download/Fold-Print-Agent-Setup.exe

On a Mac? Chrome prints straight to the printer — open Fold POS in Chrome, then **Settings › Receipts › Connect printer**. The Mac helper for Safari and Firefox is on its way; email contact@foldpos.com and we'll set it up with you in the meantime.

Download it on the Windows computer the printer is plugged into.

## Three steps

1. Open the file you downloaded and click **Next** through it. No admin password is needed.
2. When it finishes, a page opens in your browser. Sign in to Fold POS, go to **Settings › Receipts › Fold Print Agent › Pair with a code**, and type the 6-digit code into that page.
3. Pick your printer in Settings › Receipts and print a test receipt. Done — it stays paired even after a restart.

## If Windows shows a blue warning

**"Windows protected your PC"** appears because the helper is new and not yet in Microsoft's reputation list. Click **More info**, then **Run anyway**.

The helper only talks to `app.foldpos.com` and your printers. It doesn't change printer settings, and it's removed from Windows › Add or remove programs like anything else. Its status page is always at `localhost:9377` on that computer.

## More

Need a hand? Email contact@foldpos.com — we'll do it with you over a call.

- [Store setup guide](/setup.md) · [Home](/fold-pos.md) · [FAQ](/faq.md)
