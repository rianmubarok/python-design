import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
SCRIPT_DIR = Path(__file__).resolve().parent

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = SCRIPT_DIR.parent / "output" / "jpg"
SVG_DIR = SCRIPT_DIR.parent / "output" / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")
def flow_field():
    fig, ax = setup_ax()
    def angle_field(x, y):
        return np.sin(x * 0.1) * np.cos(y * 0.1) * np.pi
    for start_x in np.arange(-5, 105, 5):
        for start_y in np.arange(-5, 105, 5):
            x, y = start_x, start_y
            xs, ys = [x], [y]
            for _ in range(100):
                angle = angle_field(x, y)
                x += 0.5 * np.cos(angle)
                y += 0.5 * np.sin(angle)
                if x < -10 or x > 110 or y < -10 or y > 110:
                    break
                xs.append(x)
                ys.append(y)
            if len(xs) > 5:
                lw = 0.8 + 0.5 * np.sin(start_x * 0.2)
                ax.plot(xs, ys, color="black", linewidth=lw, alpha=0.7)
    save(fig, "flow_field")


if __name__ == "__main__":
    flow_field()
