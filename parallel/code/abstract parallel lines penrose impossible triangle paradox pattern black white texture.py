import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


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


def draw():
    """
    Penrose impossible triangle built entirely from parallel lines.
    Three beams of tightly packed parallel lines form the sides of the triangle,
    with the impossible overlap/underpass at each corner creating the paradox.
    Multiple nested impossible triangles at different scales.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 48.0

    def draw_penrose_triangle(cx, cy, size, n_lines, lw):
        """Draw one impossible triangle of given size filled with parallel lines."""
        # Triangle vertices (equilateral, pointing up)
        h = size * np.sqrt(3) / 2
        # Outer triangle
        A = np.array([cx, cy + h * 0.6])           # top
        B = np.array([cx - size / 2, cy - h * 0.4])  # bottom-left
        C = np.array([cx + size / 2, cy - h * 0.4])  # bottom-right

        beam_width = size * 0.12

        # For each side, draw parallel lines along the beam
        sides = [(A, B), (B, C), (C, A)]

        for side_idx, (p1, p2) in enumerate(sides):
            direction = p2 - p1
            length = np.linalg.norm(direction)
            d_unit = direction / length
            # Normal to the side (perpendicular)
            n_unit = np.array([-d_unit[1], d_unit[0]])

            for k in range(n_lines):
                t = (k / (n_lines - 1) - 0.5) * beam_width
                # Offset line parallel to the side
                start = p1 + n_unit * t
                end = p2 + n_unit * t

                # Shorten lines at corners to create the impossible overlap
                # Trim start by a fraction and end by a fraction
                trim_start = 0.08
                trim_end = 0.08
                start_trimmed = start + d_unit * length * trim_start
                end_trimmed = end - d_unit * length * trim_end

                ax.plot([start_trimmed[0], end_trimmed[0]],
                        [start_trimmed[1], end_trimmed[1]],
                        color="black", linewidth=lw, solid_capstyle="butt")

        # Draw corner overlaps to create the impossible illusion
        for corner_idx in range(3):
            p_corner = [A, B, C][corner_idx]
            p_prev = [C, A, B][corner_idx]
            p_next = [B, C, A][corner_idx]

            # Draw short connecting lines at corners
            d1 = (p_prev - p_corner)
            d1 = d1 / np.linalg.norm(d1)
            d2 = (p_next - p_corner)
            d2 = d2 / np.linalg.norm(d2)

            for k in range(n_lines):
                t = (k / (n_lines - 1) - 0.5) * beam_width
                n1 = np.array([-d1[1], d1[0]])
                pt1 = p_corner + d1 * beam_width * 0.8 + n1 * t

                n2 = np.array([-d2[1], d2[0]])
                pt2 = p_corner + d2 * beam_width * 0.8 + n2 * t

                ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]],
                        color="black", linewidth=lw * 0.6,
                        solid_capstyle="round")

    # Draw nested impossible triangles
    scales = [42, 34, 26, 18, 11, 6]
    for s in scales:
        n = max(3, int(s * 0.4))
        lw = 0.25 + 0.2 * (s / 42)
        draw_penrose_triangle(cx, cy, s, n, lw)

    save(fig, "abstract parallel lines penrose impossible triangle paradox pattern black white texture")


if __name__ == "__main__":
    draw()
