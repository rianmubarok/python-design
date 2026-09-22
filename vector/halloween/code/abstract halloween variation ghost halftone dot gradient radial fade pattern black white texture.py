import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI  = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR  = SCRIPT_DIR.parent / "output"
JPG_DIR     = OUTPUT_DIR / "jpg"
SVG_DIR     = OUTPUT_DIR / "svg"
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


def ghost_dot_field(ax, cx, cy, s):
    """Ghost silhouette implied purely by a halftone dot field.
    Dots are largest and densest at the ghost's solid core, shrinking
    radially outward to give a dissolving/fading-into-fog effect.
    No outline — pure dot cloud.
    """
    # Ghost body bounding box (approximate shape mask)
    # We use a simple ellipse-distance field to determine dot size
    head_cx, head_cy = cx, cy + s * 0.20
    head_rx, head_ry = s * 0.30, s * 0.30
    body_cx, body_cy = cx, cy - s * 0.05
    body_rx, body_ry = s * 0.38, s * 0.36

    dot_spacing = s * 0.095
    max_r       = s * 0.50
    dot_r_max   = dot_spacing * 0.46

    # Regular dot grid over the ghost's bounding zone
    x_range = np.arange(cx - max_r, cx + max_r + dot_spacing, dot_spacing)
    y_range = np.arange(cy - max_r - s * 0.10, cy + max_r + dot_spacing, dot_spacing)

    for gx in x_range:
        for gy in y_range:
            # Distance to head ellipse and body ellipse — take minimum
            d_head = np.hypot((gx - head_cx) / head_rx, (gy - head_cy) / head_ry)
            d_body = np.hypot((gx - body_cx) / body_rx, (gy - body_cy) / body_ry)
            d = min(d_head, d_body)

            # Also factor in wavy hem: ghost base is wavy, trim dots below it
            hem_y = cy - s * 0.28 + s * 0.06 * np.sin((gx - cx) / (s * 0.38) * 2.5 * np.pi)
            if gy < hem_y:
                continue

            # Map ellipse-distance to dot radius: solid inside (d<1), fade outside
            if d < 0.6:
                r = dot_r_max
            elif d < 1.8:
                r = dot_r_max * (1.0 - (d - 0.6) / 1.2)
            else:
                continue

            if r < dot_r_max * 0.08:
                continue

            ax.add_patch(Circle((gx, gy), r, facecolor="white", edgecolor="none"))

    # Eye dots: two clusters of denser black dots inside ghost
    for ex, ey in [(cx - s * 0.105, cy + s * 0.26), (cx + s * 0.105, cy + s * 0.26)]:
        for _ in range(6):
            jx = ex + np.random.uniform(-s*0.035, s*0.035)
            jy = ey + np.random.uniform(-s*0.045, s*0.045)
            ax.add_patch(Circle((jx, jy), dot_r_max * 0.55,
                                facecolor="black", edgecolor="none"))


def draw():
    """3×4 grid of ghost halftone dot fields. Black background.
    Each ghost is a dissolving dot cloud — no hard silhouette edges.
    """
    fig, ax = setup_ax()

    rng = np.random.default_rng(42)
    np.random.seed(42)

    cols, rows = 3, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.78

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    ghost_dot_field(ax, px, py, s)

    save(fig,
         "abstract halloween variation ghost halftone dot gradient radial "
         "fade pattern black white texture")


if __name__ == "__main__":
    draw()
