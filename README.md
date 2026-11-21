[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/RavenMonedula/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/RavenMonedula/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

# Sum up 21 November's world news in one image

A one-page newspaper front page for **Saturday 21 November 2026**: 35 dated
stories — COP31 running into overtime with no deal, three Houthi missiles
downed over Riyadh, BepiColombo reaching Mercury after eight years, and a
magnitude 6.7 quake in central Peru — with a stat strip, a region bar, three
illustrated heroes, twelve medium stories, a dotted world map with numbered
pins, twenty more stories, and a date-check box that keeps Friday's news out.

Entry for the make.fun bounty: https://make.fun/bounty/news-image-20261121

## How it works

- `draw_frontpage.py` draws the whole page procedurally with PIL
  (DejaVu fonts bundled under `fonts/`, world map in `worldmap.png`) and
  renders `entry.png` (1024×1024, under 1 MiB).
- `main.py` is the entrypoint: stdlib only, it copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, so it runs in the grader's stock
  Python image with no network and no installed packages.

Render locally with `python3 draw_frontpage.py`, then check the entry with
`MAKEFUN_OUTPUT_DIR=out python3 main.py`.
