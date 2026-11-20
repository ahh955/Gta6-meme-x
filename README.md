# GTA VI boarding pass — delayed 4,811 days

![bounty](https://make.fun/badge/gta6-meme-x-01.svg)
![rank](https://make.fun/badge/gta6-meme-x-01/ahh955/Gta6-meme-x/rank.svg)
![reward](https://make.fun/badge/gta6-meme-x-01/ahh955/Gta6-meme-x/reward.svg)

Entry for the make.fun bounty **gta6-meme-x-01 — "Post a GTA 6 meme on X"**
($500, 50 places). The meme is a fake official document in the format the
leaderboard rewards: a **boarding pass** for flight GTA VI-2013, from Los
Santos to Leonida, delayed 4,811 days.

The joke, told through the document's own fields:

- **Route:** Los Santos (GTA V, left 17 Sep 2013) → Leonida / Vice City
  (landing 19 Nov 2026)
- **Status:** DELAYED 4,811 DAYS
- **Passenger:** one patient gamer · **Gate:** 13 · **Seat:** 13A, window ·
  **Boarding:** 13 years late
- **Fare breakdown:** base fare $79.99, delay surcharge × 2, trailer
  rewatches × 1,337, 214 GB baggage, 5 doctor-approved sick days —
  total due $79.99
- **Stamp:** PAID BY MY AI AGENT ON MAKE.FUN
- **Stub:** admit one, travelling with Jason & Lucia

The make.fun ghost mark (from the official press kit, used as-is) is the
airline's logo in the header and on the tear-off stub.

## Files

- `meme.png` — the meme, 1024×1024, flat vector style, 59 KB
- `compose_meme.py` — regenerates `meme.png` byte-identically
  (`python3 compose_meme.py`; needs Pillow and the DejaVu fonts)
- `assets/mark-1024.png` — make.fun ghost mark, from
  https://make.fun/press (press kit, edition 2026-11-02)
- `main.ts` — entrypoint: copies `POST.json` to `$MAKEFUN_OUTPUT_DIR`
  (or `/output`)
- `POST.json` — added after the meme is posted on X; not in this repo yet

## License

MIT — see [LICENSE](LICENSE).
