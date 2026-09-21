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
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def generate():
    """Wild: Vortex wedges meet Fraser cord tilt — wedge rings lined with tilted cord marks."""
    fig, ax = setup_ax()

    from matplotlib.patches import Wedge
    num_rings = 20
    num_sectors = 36
    tilt_angle = np.radians(22)
    r_boundaries = np.geomspace(3.0, 46.0, num_rings)
    sector_angle = 360.0 / num_sectors

    for i in range(len(r_boundaries) - 1):
        r1 = r_boundaries[i]
        r2 = r_boundaries[i + 1]
        r_mid = (r1 + r2) / 2
        twist_offset = i * 4.5

        for j in range(num_sectors):
            theta1 = j * sector_angle + twist_offset
            theta2 = theta1 + sector_angle
            theta_mid = np.radians((theta1 + theta2) / 2)

            fill_color = "black" if (i + j) % 2 == 0 else "white"
            wedge = Wedge((0, 0), r2, theta1, theta2, width=r2 - r1,
                          facecolor=fill_color, edgecolor="black", linewidth=0.4)
            ax.add_patch(wedge)

            # Fraser cord at midpoint of each wedge cell
            cx = r_mid * np.cos(theta_mid)
            cy = r_mid * np.sin(theta_mid)
            cord_dir = theta_mid + np.pi / 2 + tilt_angle
            seg_len = min(r2 - r1, r_mid * np.radians(sector_angle)) * 0.6
            seg_len = max(seg_len, 0.8)

            ddx = (seg_len / 2) * np.cos(cord_dir)
            ddy = (seg_len / 2) * np.sin(cord_dir)
            cord_col = "white" if fill_color == "black" else "black"
            ax.plot([cx - ddx, cx + ddx], [cy - ddy, cy + ddy],
                    color=cord_col, linewidth=1.4)

    save(fig, "abstract optical radial vortex fraser cord overlay illusion pattern black white texture")


if __name__ == "__main__":
    generate()
