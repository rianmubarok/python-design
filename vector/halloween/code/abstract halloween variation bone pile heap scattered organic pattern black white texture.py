from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.transforms import Affine2D
import matplotlib

matplotlib.use("Agg")

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("black")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="black")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="black")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def single_bone(ax, cx, cy, length, width, angle_deg, fill="white"):
    """Menggambar 1 tulang dengan siluet klasik yang jelas dan proporsional."""
    tr = Affine2D().rotate_deg(angle_deg).translate(cx, cy) + ax.transData
    half = length / 2.0
    knob_r = width * 0.72

    # Batang Utama (Shaft)
    ax.add_patch(
        FancyBboxPatch(
            (-half, -width / 2.0),
            length,
            width,
            boxstyle=f"round,pad=0,rounding_size={width * 0.4:.4f}",
            facecolor=fill,
            edgecolor="none",
            transform=tr,
            zorder=2,
        )
    )

    # Benjolan Sendi Ganda di Kedua Ujung
    for ex in (-half, half):
        for off_y in (-knob_r * 0.5, knob_r * 0.5):
            ax.add_patch(
                Circle(
                    (ex, off_y),
                    knob_r,
                    facecolor=fill,
                    edgecolor="none",
                    transform=tr,
                    zorder=3,
                )
            )


def draw():
    """Tumpukan tulang acak yang presisi, proporsional, dan seamless tanpa peleburan blob."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(22)
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    pile_r = min(dx, dy) * 0.40

    # Pre-generate data tumpukan tulang secara konsisten
    piles_data = []
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + rng.uniform(-dx * 0.08, dx * 0.08)
            cy = (row + 0.5) * dy + rng.uniform(-dy * 0.08, dy * 0.08)
            n_bones = rng.integers(3, 5)  # Terkontrol agar tidak melebur

            bones_in_pile = []
            for _ in range(n_bones):
                dist = rng.uniform(0, pile_r * 0.50)
                ang = rng.uniform(0, 2 * np.pi)
                bx = cx + dist * np.cos(ang)
                by = cy + dist * np.sin(ang)

                blen = rng.uniform(pile_r * 0.8, pile_r * 1.15)
                bwidth = blen * 0.14  # Rasio lebar ideal
                bangle = rng.uniform(0, 180)

                bones_in_pile.append((bx, by, blen, bwidth, bangle))

            piles_data.append(bones_in_pile)

    # Rendering dengan duplikasi WRAPS untuk Seamless Tile
    for pile in piles_data:
        for bx, by, blen, bwidth, bangle in pile:
            for ox, oy in WRAPS:
                px = bx + ox
                py = by + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    single_bone(ax, px, py, blen, bwidth, bangle, fill="white")

    save(
        fig,
        "abstract halloween variation bone pile heap scattered organic pattern black white texture",
    )


if __name__ == "__main__":
    draw()