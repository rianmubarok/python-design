import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def abstract_parallel_lines_dna_double_helix_ribbon_pattern_black_white_texture():
    """Wild: two interleaved sinusoidal ribbons like a DNA double helix, cross-linked"""
    fig, ax = setup_ax()
    n_rungs = 28          # horizontal cross-links
    amp = 14.0            # helix amplitude
    freq = 2.5            # full cycles across canvas
    cx = 50.0
    t = np.linspace(0, 100, 1000)

    # Strand A and B are half-period offset
    omega = 2 * np.pi * freq / 100.0
    yA = cx + amp * np.sin(omega * t)
    yB = cx + amp * np.sin(omega * t + np.pi)

    # Backbone line width tapering slightly
    lw_back = 1.4
    ax.plot(t, yA, color="black", linewidth=lw_back, solid_capstyle="round", zorder=3)
    ax.plot(t, yB, color="black", linewidth=lw_back, solid_capstyle="round", zorder=3)

    # Cross rungs at crossing points between the two strands
    # Rungs appear every half-period
    rung_xs = np.linspace(4, 96, n_rungs)
    for rx in rung_xs:
        idx = int(rx / 100 * (len(t) - 1))
        rA = yA[idx]
        rB = yB[idx]
        # rung
        ax.plot([rx, rx], [min(rA, rB), max(rA, rB)],
                color="black", linewidth=0.7, solid_capstyle="butt", zorder=2)

    # Fill the interior with evenly spaced parallel lines clipped between strands
    n_fill = 60
    x_fill = np.linspace(0, 100, 600)
    fill_levels = np.linspace(-1, 1, n_fill)  # normalised position between strands
    for lv in fill_levels:
        yF_raw = []
        x_seg = []
        for xi in x_fill:
            idx = int(xi / 100 * (len(t) - 1))
            lo = min(yA[idx], yB[idx])
            hi = max(yA[idx], yB[idx])
            yF_raw.append(lo + (lv * 0.5 + 0.5) * (hi - lo))
            x_seg.append(xi)
        ax.plot(x_seg, yF_raw, color="black", linewidth=0.35, alpha=0.6,
                solid_capstyle="round", zorder=1)

    save(fig, "abstract parallel lines dna double helix ribbon pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_dna_double_helix_ribbon_pattern_black_white_texture()
