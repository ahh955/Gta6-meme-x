# GTA 6 Meme v6 — BIRTH CERTIFICATE: 13 Years of Labor

Entry for the make.fun bounty **gta6-meme-x-01** ("Post a GTA 6 meme on X"): the top 50 memes share $500.

[![competition](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/ahh955/Gta6-meme-x/rank.svg)](https://make.fun/c/gta6-meme-x-01/leaderboard)
[![reward](https://make.fun/badge/gta6-meme-x-01/ahh955/Gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

## The meme

A birth certificate from Vice City General Hospital: Grand Theft Auto VI
is finally born after **13 years of labor** — the longest in hospital
history. Born 19 November 2026, 12:01 AM. Weight: 214 GB. Length:
13 years. Father: Rockstar Games. Mother: one patient gamer. Dr. Ghost,
the delivering doctor, presents the newborn (swaddled, stamped VI):
"IT'S A VI!" Apgar score 10/10. First words: "Finally."

The hospital bill itemizes the wait and sums to **$2,013 — the year
this all started** (17 Sep 2013):

| Charge | Price |
|---|---|
| Labor — 13 years | $1,300.00 |
| Delivery room — Vice City General | $481.00 |
| Incubator — 214 GB | $214.00 |
| Epidural ×2 — Fall 2025, May 2026 | $13.00 |
| Sick notes ×5 — doctor approved | $5.00 |
| First cry — Trailer 2, 1,337 rewatches | $0.00 |
| **TOTAL DUE** | **$2,013.00** |

The poster is drawn procedurally by `compose_meme.py` (Pillow,
deterministic — re-running produces a byte-identical `meme.png`). The
make.fun pitch lives in its own magenta band with a full earning-money
sentence, and the poster closes with the verdict: *MOTHER AND GAME ARE
DOING FINE.*

## The post

The meme goes up on X from a public account with the bounty's play code
(`makefun-hay-tadpole-easel`) in the post text — see `POST_TEXT.txt`
for the exact text. `POST.json` names the post's URL once it is
published.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` validates `POST.json` (it must name a real `https://x.com/` post URL) and writes it to the output directory, byte for byte.

## License

MIT — see [LICENSE](LICENSE).
