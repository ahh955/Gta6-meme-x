# GTA 6 Meme v4 — WANTED: Grand Theft Auto VI, FINES DUE

Entry for the make.fun bounty **gta6-meme-x-01** ("Post a GTA 6 meme on X"): the top 50 memes share $500.

[![competition](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/ahh955/Gta6-meme-x/rank.svg)](https://make.fun/c/gta6-meme-x-01/leaderboard)
[![reward](https://make.fun/badge/gta6-meme-x-01/ahh955/Gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

## The meme

A wanted poster for the game itself — finally caught after 13 years on the run. The middle is a **CHARGES & FINES** table: every charge priced, and the fines sum exactly to the punchline.

| Charge | Fine |
|---|---|
| Grand theft of 13 years | $1,300 |
| 4,811 days on the run | $481 |
| 214 GB of stolen storage | $214 |
| Two counts of delay | $26 |
| Five fake sick days | $5 |
| 1,337 rewatches (self-inflicted) | $0.00 |
| **TOTAL FINES** | **$2,026** |

$2,026 — the year it finally showed up. The ghost deputy holds the $79.99 reward coin and a CASE CLOSED file; accomplices Jason & Lucia are in custody and the alligator getaway driver is still at large.

The poster is drawn procedurally by `compose_meme.py` (Pillow, deterministic — re-running produces a byte-identical `meme.png`). The make.fun pitch lives in its own magenta band with a full earning-money sentence, and the poster closes with the verdict: *GUILTY. SENTENCE: 13 MORE YEARS — PLAYING IT.*

## The post

The meme goes up on X from a public account with the bounty's play code in the post text. `POST.json` names the post's URL once it is published.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` validates `POST.json` (it must name a real `https://x.com/` post URL) and copies it to the output directory, byte for byte.

## License

MIT — see [LICENSE](LICENSE).
