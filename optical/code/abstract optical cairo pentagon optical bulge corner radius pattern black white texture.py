import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


def resample_and_bulge(pts, n_sub=8, radius=45.0, strength=0.6):
    """Membagi garis ubin menjadi segmen halus lalu menerapkan efek cembung."""
    dense_pts = []
    n = len(pts)
    for i in range(n):
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        for t in np.linspace(0, 1, n_sub, endpoint=False):
            dense_pts.append((1 - t) * p1 + t * p2)
    dense_pts = np.array(dense_pts)

    r = np.linalg.norm(dense_pts, axis=1)
    factor = np.where(r < radius, 1.0 + strength * (1.0 - (r / radius) ** 2), 1.0)
    return dense_pts * factor[:, np.newaxis]


def abstract_optical_cairo_pentagon_optical_bulge_corner_radius_pattern_black_white_texture():
    fig, ax = setup_ax()

    # Parameter Geometri Cairo Pentagonal Tiling Presisi
    a = 8.0
    # Panjang unit cell
    d = a * (1 + np.sqrt(3) / 2)

    # Replikasi Grid Cairo
    step = 2 * d
    grid_range = np.arange(-75, 75, step)

    for gx in grid_range:
        for gy in grid_range:
            # Pusat-pusat simpul grid
            centers = [
                (gx, gy),
                (gx + d, gy + d),
            ]

            for cx, cy in centers:
                # Titik-titik sudut pembentuk 4 pentagon Cairo simetris
                v0 = np.array([cx, cy])
                v_N = np.array([cx, cy + a])
                v_S = np.array([cx, cy - a])
                v_E = np.array([cx + a, cy])
                v_W = np.array([cx - a, cy])

                v_NE = np.array([cx + d, cy + d])
                v_NW = np.array([cx - d, cy + d])
                v_SW = np.array([cx - d, cy - d])
                v_SE = np.array([cx + d, cy - d])

                # 4 Pentagon sejati yang saling mengunci
                pentagons = [
                    np.array([v0, v_E, v_NE, v_N, v0]),
                    np.array([v0, v_N, v_NW, v_W, v0]),
                    np.array([v0, v_W, v_SW, v_S, v0]),
                    np.array([v0, v_S, v_SE, v_E, v0]),
                ]

                for p_idx, pts in enumerate(pentagons):
                    pts_unique = pts[:-1]
                    c_pt = pts_unique.mean(axis=0)

                    if np.abs(c_pt[0]) > 55 or np.abs(c_pt[1]) > 55:
                        continue

                    # Subdivisi dan distorsi cembung
                    b_pts = resample_and_bulge(pts_unique)

                    # Warna ubin berselang-seling hitam dan putih
                    color_val = (int((cx + 100) / a) + int((cy + 100) / a) + p_idx) % 2 == 0

                    poly = Polygon(
                        b_pts,
                        closed=True,
                        facecolor="black" if color_val else "white",
                        edgecolor="black",
                        linewidth=0.8,
                        zorder=2,
                    )
                    ax.add_patch(poly)

    save(
        fig,
        "abstract optical cairo pentagon optical bulge corner radius pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_cairo_pentagon_optical_bulge_corner_radius_pattern_black_white_texture()