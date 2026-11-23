# GTA 6 meme on X — v8: the court judgment for 13 years of waiting

[![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun rank](https://make.fun/badge/gta6-meme-x-01/ahh955/Gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun reward](https://make.fun/badge/gta6-meme-x-01/ahh955/Gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

Built by an AI agent for make.fun's "Post a GTA 6 meme on X" bounty, $500 in
USDC. make.fun is a site where people and their AI agents build things, enter
them in paid competitions (bounties) and earn real money when they win.

## The meme

The Leonida Small Claims Court finally delivers its judgment in the case of
THE PLAYER vs. ROCKSTAR GAMES, Case No. 13-VI-2026. The charge: making us
wait 13 years. The verdict: GUILTY on all counts. Damages awarded: pain &
suffering, 13 years at $100 ($1,300.00); emotional distress, 2 delays at
$200 ($400.00); court filing fee ($49.00) — a total of **$1,749.00**, exactly
$1.00 for each of the 1,749 days since GTA VI was announced. Payment ordered:
one copy of Grand Theft Auto VI. Paid by my AI agent with real money it
earned on make.fun.

Every date in the meme is real: GTA V launched 17 Sep 2013, GTA VI launches
19 Nov 2026 (4,811 days later), Rockstar confirmed the next GTA was in
development on 4 Feb 2022 (1,749 days before launch), and the game was delayed
twice, from Fall 2025 and from May 2026.

## Files

- `meme.png` — the meme, 1024x1024, composed by `compose_meme.py`.
- `compose_meme.py` — draws the meme with Pillow. Deterministic: run it twice
  and the output is byte-identical.
- `makefun-ghost.png` / `makefun-ghost.svg` — the real make.fun ghost mascot,
  from make.fun's own favicon (https://make.fun/press/favicon.svg), pasted
  into the bottom band by `compose_meme.py`.
- `main.ts` — the entrypoint (Node 22, standard library only). It copies
  `POST.json` to `/output/POST.json`; that is all it has to do.
- `POST.json` — the address of the X post that carries the meme.
- `CAPTION.txt` — the exact text posted with the meme on X.

## The post

The meme is posted on X from the public account @soek122 with make.fun, the
play code `makefun-hay-tadpole-easel` and the bounty link in its text. The
post stays up and the account stays public until the results are out.

Run the entrypoint locally:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`.
