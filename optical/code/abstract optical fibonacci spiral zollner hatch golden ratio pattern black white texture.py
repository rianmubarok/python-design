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
    """Fibonacci spiral vortex combined with Zollner hatching illusion pattern filling full canvas."""
    fig, ax = setup_ax()

    n_arms = 6
    phi = (1 + np.sqrt(5)) / 2
    b = np.log(phi) / (np.pi / 2)

    t_vals = np.linspace(0.8, 3.4 * np.pi, 500)

    for arm in range(n_arms):
        angle_offset = arm * (2 * np.pi / n_arms)
        hatch_tilt = 0.45 if arm % 2 == 0 else -0.45

        # Perbesar pengali skala (3.5 -> 7.0) agar spiral mengembang penuh
        r_base = 7.0 * np.exp(b * (t_vals - 0.8) * 0.75)
        theta = t_vals + angle_offset

        x = r_base * np.cos(theta)
        y = r_base * np.sin(theta)

        # Plot Kurva Utama
        ax.plot(x, y, color="black", linewidth=1.8, zorder=2)

        # Plot Arsir Zöllner
        step = 7
        for i in range(2, len(t_vals) - step, step):
            hx, hy = x[i], y[i]
            r_curr = r_base[i]

            if r_curr > 49 or r_curr < 2.5:
                continue

            dx_tan = x[i + 1] - x[i]
            dy_tan = y[i + 1] - y[i]
            tangent = np.arctan2(dy_tan, dx_tan)

            perp = tangent + np.pi / 2 + hatch_tilt

            hatch_len = np.clip(1.5 + r_curr * 0.08, 1.5, 6.5)

            ddx = (hatch_len / 2) * np.cos(perp)
            ddy = (hatch_len / 2) * np.sin(perp)

            ax.plot(
                [hx - ddx, hx + ddx],
                [hy - ddy, hy + ddy],
                color="black",
                linewidth=1.2,
                zorder=3,
            )

    save(
        fig,
        "abstract optical fibonacci spiral zollner hatch golden ratio pattern black white texture",
    )


if __name__ == "__main__":
    generate()