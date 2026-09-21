from datetime import datetime
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")
PERIOD = 1.0

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_position([0, 0, 1, 1])
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.margins(0)
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")


def plot_wrapped(ax, xs, ys, **kwargs):
    for dx in (-PERIOD, 0.0, PERIOD):
        for dy in (-PERIOD, 0.0, PERIOD):
            ax.plot(
                [x + dx for x in xs],
                [y + dy for y in ys],
                **kwargs,
            )


def diamond_points(cx, cy, w, h):
    return (
        [cx, cx + w / 2.0, cx, cx - w / 2.0, cx],
        [cy + h / 2.0, cy, cy - h / 2.0, cy, cy + h / 2.0],
    )


def diamond_grid_compressed_density():
    """Teselasi belah ketupat rapat saling tumpang, full canvas, seamless."""
    fig, ax = setup_ax()

    cols = 24
    rows = 30
    step_x = PERIOD / cols
    step_y = PERIOD / rows
    w = step_x / 0.9
    h = 2.0 * step_y / 0.85

    for r in range(-1, rows + 1):
        for c in range(-1, cols + 1):
            cx = c * step_x
            if r % 2 != 0:
                cx += step_x / 2.0
            cy = r * step_y
            xs, ys = diamond_points(cx, cy, w, h)
            lw = 0.55 + 0.22 * (r % 3)
            plot_wrapped(
                ax,
                xs,
                ys,
                color="black",
                linewidth=lw,
                solid_capstyle="round",
                solid_joinstyle="miter",
                clip_on=True,
            )

    save(fig, "abstract geometric diamond grid compressed density pattern black white texture")


if __name__ == "__main__":
    diamond_grid_compressed_density()
