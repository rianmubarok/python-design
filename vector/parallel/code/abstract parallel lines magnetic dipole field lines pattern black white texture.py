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


def abstract_parallel_lines_magnetic_dipole_field_lines_pattern_black_white_texture():
    """Magnetic dipole field lines traced by integrating the dipole vector field"""
    fig, ax = setup_ax()

    # Two poles placed symmetrically
    p_pos = np.array([50.0, 62.0])  # north (+)
    p_neg = np.array([50.0, 38.0])  # south (-)
    strength = 320.0

    def field(x, y):
        """Sum of two monopole fields: B ~ r_hat / r^2"""
        r1 = np.array([x - p_pos[0], y - p_pos[1]])
        r2 = np.array([x - p_neg[0], y - p_neg[1]])
        d1 = max(np.linalg.norm(r1), 0.8)
        d2 = max(np.linalg.norm(r2), 0.8)
        B = r1 / d1 ** 3 - r2 / d2 ** 3
        return B

    # Seed positions around the north pole
    n_seeds = 36
    seed_r = 3.5
    angles = np.linspace(0, 2 * np.pi, n_seeds, endpoint=False)
    seeds = [(p_pos[0] + seed_r * np.cos(a), p_pos[1] + seed_r * np.sin(a)) for a in angles]

    dt = 0.18
    max_steps = 1800

    for sx, sy in seeds:
        xs, ys = [sx], [sy]
        x, y = sx, sy
        for _ in range(max_steps):
            B = field(x, y)
            norm = np.linalg.norm(B)
            if norm < 1e-9:
                break
            dx = dt * B[0] / norm
            dy = dt * B[1] / norm
            x += dx
            y += dy
            xs.append(x)
            ys.append(y)
            # Stop near the south pole or out of bounds
            if np.hypot(x - p_neg[0], y - p_neg[1]) < 2.5:
                break
            if x < -6 or x > 106 or y < -6 or y > 106:
                break
        lw = 0.55
        ax.plot(xs, ys, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines magnetic dipole field lines pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_magnetic_dipole_field_lines_pattern_black_white_texture()
