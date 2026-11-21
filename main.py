#!/usr/bin/env python3
"""news-image-20261121 entry: writes the front page to /output/entry.png.
The image is pre-rendered by draw_frontpage.py (PIL, no network); this
program just copies it to /output, deterministically. Stdlib only, so
it runs in the grader's stock Python image."""
import os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(outdir, exist_ok=True)
shutil.copyfile(os.path.join(BASE, "entry.png"),
                os.path.join(outdir, "entry.png"))
print("wrote", os.path.join(outdir, "entry.png"))
