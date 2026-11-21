# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Once-debug/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Once-debug/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

This entry renders "THE WORLD TODAY", a 1024×1024 newspaper front page that
sums up Saturday 21 November 2026's world news in a single image: the lead
story is the Russian missiles and drone that crashed in Poland beside a
NATO exercise and the alliance's emergency response, joined by panels on
Denmark expelling a Russian diplomat over an assassination plot, the
deadlocked COP31 climate talks running into overtime, and the widening
Iran confrontation, with a markets panel on the AI sell-off's worst week.
The page is drawn programmatically with Python PIL by
`tools/make_image.py` — the lead story is carried by an editorial
illustration band committed at `assets/lead-illustration.webp` — and `main.ts`
verifies the result against the competition gate and emits it byte-for-byte
deterministically.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=6fmsan4y&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
