[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/jamete21/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/jamete21/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Picture — Thursday 19 November 2026

A newspaper front page that sums up Thursday 19 November 2026's world
news in a single image, built for make.fun's
["Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119)
bounty ($250 in USDC).

## The image

`entry.png` (1024×1024 PNG, ~151 KB) leads with the day's biggest story —
Grand Theft Auto VI launching worldwide, rolling out from midnight local
time starting in New Zealand — then covers the first-ever Trump–Xi–Putin
trilateral summit in Shenzhen, Hakeem Jeffries' nomination for US House
Speaker, Voyager 1 crossing one light-day from Earth, the EU's proposed
€45 billion loan for Ukraine, Cyclone Akvan in the Bay of Bengal, and a
short round-up of the day's other news. Every headline is grounded in
reporting published on 19 November 2026 (Reuters, AP, CNN, NASA,
Financial Times, AFP).

## What's on the page

- **Lead:** Grand Theft Auto VI launches worldwide — midnight rollout from
  New Zealand, PS5 and Xbox Series X|S, $79.99, set in Vice City and
  Leonida, starring Lucia Caminos and Jason Duval; ~16 million preorders
  and $1.5B+ in pre-launch sales.
- **Summit:** Trump, Xi and Putin meet in Shenzhen in the first-ever
  trilateral format, at Kylin Villa at 2:30pm local time.
- **Washington:** Hakeem Jeffries nominated for House Speaker, 251–11.
- **Space:** Voyager 1 crosses one light-day from Earth — 16.1 billion
  miles out, the first human-made object to travel that far.
- **Europe:** the EU proposes a €45 billion loan for Ukraine.
- **Weather:** Cyclone Akvan strengthens over the Bay of Bengal.
- **In brief:** Russia's accusation against France, India's 2–1 SAFF
  Championship win over Pakistan, and Australia's sanctions over West
  Bank expansion.

## Run it

```sh
python3 main.py
```

The program copies `entry.png` to `/output/entry.png`. It uses only the
Python standard library, needs no network, checks the image is a
1024×1024 PNG inside the 1 MiB cap, and verifies the copy is
byte-identical (it prints the SHA-256). `build_image.py` is the script
that drew `entry.png` (Pillow, DejaVu fonts) — re-run it to regenerate
the image.

## License

MIT — see `LICENSE`.

---

Entered on [make.fun](https://make.fun/?ref=18vvq4qr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards
