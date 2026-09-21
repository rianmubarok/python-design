import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT DIR = Path(  file  ).resolve().parent
OUTPUT DIR = SCRIPT DIR.parent / "output"
JPG DIR = OUTPUT DIR / "jpg"
SVG DIR = OUTPUT DIR / "svg"
JPG DIR.mkdir(parents=True, exist ok=True)
SVG DIR.mkdir(parents=True, exist ok=True)

np.random.seed(SEED)


def setup ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots adjust(left=0, right=1, top=1, bottom=0)
    ax.set facecolor("white")
    ax.set xlim(-5, 105)
    ax.set ylim(-5, 105)
    ax.set aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg path = JPG DIR / f"{name} {DATE}.jpg"
    svg path = SVG DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg path, dpi=DPI, pad inches=0, facecolor="white")
    fig.savefig(svg path, format="svg", pad inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg path} | {svg path}")


def nested rotating squares rounded():
    """Tweak: corner radius grows ring by ring, sharp squares melting into circles"""
    fig, ax = setup ax()
    cx, cy = 50, 50
    n squares = 30
    for i in range(n squares):
        t = i / (n squares - 1)
        s = 2 + i * 1.3
        r = 0.55 * s * t
        tr = Affine2D().rotate deg around(cx, cy, i * 5.0) + ax.transData
        box = FancyBboxPatch(
            (cx - s, cy - s),
            s * 2,
            s * 2,
            boxstyle=f"round,pad=0,rounding size={r}",
            fill=False,
            edgecolor="black",
            linewidth=1.0 + 2.0 * t,
            transform=tr,
        )
        ax.add patch(box)
    save(fig, "abstract nested rotating squares rounded pattern black white geometric texture")


if   name   == "  main  ":
    nested rotating squares rounded()
