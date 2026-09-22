from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch, Ellipse
from matplotlib.path import Path as MPath
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


def draw_ghost_ribbon(ax, cx, cy, length, width, angle_deg=45, fill="white", alpha=1.0, is_primary=True):
    """Menggambar hantu pita melayang dengan kontur tunggal kontinu tanpa garis dahi."""
    n_pts = 60
    t = np.linspace(0, 1, n_pts)

    r_head = width * 0.65

    # 1. Kubah Kepala Melengkung Mulus
    t_head = np.linspace(-np.pi / 2, np.pi / 2, 30)
    x_head = r_head * np.cos(t_head)
    y_head = r_head * np.sin(t_head)

    # 2. Ekor Pita Bergelombang & Meruncing (Upper & Lower)
    x_tail_upper = -length * t
    y_tail_upper = (r_head * (1 - t**1.3)) + (width * 0.20 * np.sin(t * np.pi * 2.2))

    x_tail_lower = -length * (1 - t)
    y_tail_lower = (-r_head * (1 - (1 - t)**1.3)) + (width * 0.20 * np.sin((1 - t) * np.pi * 2.2))

    # Gabungkan menjadi SATU kontur tertutup kontinu (tanpa patahan dahi)
    pts_x = np.concatenate([x_head, np.flip(x_tail_upper), x_tail_lower])
    pts_y = np.concatenate([y_head, np.flip(y_tail_upper), y_tail_lower])
    pts = np.column_stack([pts_x, pts_y])

    # Rotasi dan Translasi
    a = np.radians(angle_deg)
    c, s = np.cos(a), np.sin(a)
    R = np.array([[c, -s], [s, c]])
    pts_rot = (R @ pts.T).T + [cx, cy]

    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts_rot) - 2) + [MPath.CLOSEPOLY]
    path = MPath(pts_rot, codes)

    ax.add_patch(PathPatch(path, facecolor=fill, edgecolor="none", alpha=alpha, zorder=2))

    # 3. Mata Hantu
    if is_primary:
        eye_dist = r_head * 0.32
        eye_r = r_head * 0.20
        for eye_y in (-eye_dist, eye_dist):
            ex_local = r_head * 0.22
            ey_local = eye_y
            ex_rot = ex_local * c - ey_local * s + cx
            ey_rot = ex_local * s + ey_local * c + cy
            ax.add_patch(Ellipse((ex_rot, ey_rot), eye_r, eye_r * 1.3,
                                 facecolor="black", edgecolor="none", zorder=3))


def draw():
    """Pola pita hantu melayang diagonal yang presisi, mulus, dan seamless."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    
    # Skala disesuaikan agar hantu tidak bertabrakan dengan baris lain
    length = dx * 0.90
    width = dy * 0.28

    ghosts_data = []
    
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.25 if row % 2 else 0.0)
            cy = (row + 0.5) * dy
            
            # Sudut konsisten melayang diagonal
            base_angle = 40 + ((col + row) % 2) * 10
            ghosts_data.append((cx, cy, base_angle))

    # Render dengan WRAPS agar seamless di batas kanvas
    for cx, cy, ang in ghosts_data:
        for ox, oy in WRAPS:
            px, py = cx + ox, cy + oy
            if -25 <= px <= PERIOD + 25 and -25 <= py <= PERIOD + 25:
                # 1. Hantu bayangan (transparan)
                rad = np.radians(ang)
                echo_off_x = -length * 0.20 * np.cos(rad)
                echo_off_y = -length * 0.20 * np.sin(rad)
                draw_ghost_ribbon(ax, px + echo_off_x, py + echo_off_y,
                                  length * 0.70, width * 0.65, angle_deg=ang,
                                  fill="white", alpha=0.22, is_primary=False)

                # 2. Hantu utama
                draw_ghost_ribbon(ax, px, py, length, width, angle_deg=ang,
                                  fill="white", alpha=0.92, is_primary=True)

    save(fig, "abstract halloween variation ghost trail ribbon swooping minimal dark pattern black white texture")


if __name__ == "__main__":
    draw()