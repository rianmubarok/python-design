import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from pathlib import Path
from datetime import datetime

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


def drip_bottom_edge(n_pts, band_top_y, drip_depth, rng, phase_offset=0.0):
    """Generate the bottom edge of a wax drip band:
    A flat top at band_top_y + irregular drip blobs hanging down.
    Returns array of (x, y) points for a closed polygon fill."""
    xs = np.linspace(0, PERIOD, n_pts, endpoint=False)

    # Base sinusoidal wave + random bumps to simulate organic drip blobs
    base_wave = drip_depth * 0.35 * np.sin(xs / PERIOD * 2 * np.pi * 3 + phase_offset)
    # Add Gaussian blob drips at pseudo-random x positions
    drip_y = np.zeros(n_pts)
    n_drips = int(PERIOD / 8)
    drip_xs = rng.uniform(0, PERIOD, n_drips)
    drip_ws = rng.uniform(2.0, 5.5, n_drips)
    drip_hs = rng.uniform(drip_depth * 0.4, drip_depth, n_drips)
    for dx_pos, dw, dh in zip(drip_xs, drip_ws, drip_hs):
        dist = np.minimum(np.abs(xs - dx_pos), PERIOD - np.abs(xs - dx_pos))
        drip_y += dh * np.exp(-(dist ** 2) / (2 * dw ** 2))

    bottom_y = band_top_y - base_wave - drip_y

    return xs, bottom_y


def draw_drip_band(ax, band_top_y, band_bottom_y, fill, drip_depth, rng,
                   phase_offset=0.0, ox=0.0, oy=0.0):
    """Draw one horizontal wax band with organic drip bottom edge.
    The band fills from band_bottom_y flat top to the drip bottom."""
    n_pts = 300
    xs, drip_ys = drip_bottom_edge(n_pts, band_top_y, drip_depth, rng, phase_offset)

    # Build closed polygon: flat top → drip bottom → back
    top_pts = [(xs[0] + ox, band_top_y + oy),
               (xs[-1] + ox + PERIOD / n_pts, band_top_y + oy)]
    bot_pts = list(zip(xs + ox, drip_ys + oy))
    all_pts = ([(ox - 1, band_top_y + oy)] +
               [(x + ox, band_top_y + oy) for x in xs] +
               [(xs[-1] + ox + 1, band_top_y + oy),
                (xs[-1] + ox + 1, drip_ys[-1] + oy)] +
               bot_pts[::-1] +
               [(ox - 1, drip_ys[0] + oy)])
    ax.add_patch(Polygon(all_pts, closed=True,
                         facecolor=fill, edgecolor="none", zorder=2))


def draw():
    """Alternating horizontal bands of black and white melting wax.
    The bottom edge of each white band drips downward with organic blob shapes.
    Black bands drip upward (inverted). Together they create a layered
    melting horror texture. Seamless left-right (wraps at x=0/PERIOD)."""
    fig, ax = setup_ax()

    n_bands = 7
    band_h = PERIOD / n_bands
    drip_d = band_h * 0.42
    rng = np.random.default_rng(13)

    for row in range(-1, n_bands + 2):
        band_top = (row + 1) * band_h
        fill = "white" if row % 2 == 0 else "black"
        phase = row * 1.3

        for ox, oy in WRAPS:
            # Flat background rectangle for this band
            ax.add_patch(Rectangle(
                (0 + ox, row * band_h + oy), PERIOD, band_h,
                facecolor=fill, edgecolor="none", zorder=1))

            # Drip overhang below the bottom edge of this band
            drip_fill = fill
            draw_drip_band(ax, band_top + oy, (row - 1) * band_h + oy,
                           drip_fill, drip_d, rng,
                           phase_offset=phase, ox=ox, oy=0)

    save(fig, "abstract halloween variation drip melting wax horizontal wave band repeat pattern black white texture")


if __name__ == "__main__":
    draw()
