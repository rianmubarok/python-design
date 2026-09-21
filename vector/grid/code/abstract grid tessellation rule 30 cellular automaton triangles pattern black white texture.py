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
    Rule 30 Cellular Automaton Triangles.

    A true 1-D elementary cellular automaton (Wolfram Rule 30) evolved row by
    row: the next state of a cell is a function of its left/centre/right
    neighbours in the row above -> 100, 011, 010, 001 become active (1),
    everything else stays inactive (0). The result is the famous chaotic
    triangle/pyramid.

    Every cell is drawn as a bordered box with a micro centre dot: active cells
    are solid black with a white dot, inactive cells are white with a black dot.
    A wide automaton is computed and the central square is shown, so the pattern
    fills the 1:1 canvas instead of leaving empty bands.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    grid_size = 80
    cell_size = 1.0
    dot_radius = 0.08

    # Rule 30 lookup keyed by (left, centre, right)
    rule = {
        (1, 1, 1): 0, (1, 1, 0): 0, (1, 0, 1): 0, (1, 0, 0): 1,
        (0, 1, 1): 1, (0, 1, 0): 1, (0, 0, 1): 1, (0, 0, 0): 0,
    }

    # Wider array avoids boundary artefacts; the centre square is rendered.
    width = grid_size * 2
    state = np.zeros((grid_size, width), dtype=int)
    state[0, width // 2] = 1

    for r in range(1, grid_size):
        for c in range(1, width - 1):
            state[r, c] = rule[(state[r - 1, c - 1], state[r - 1, c], state[r - 1, c + 1])]

    start_c = (width - grid_size) // 2

    for r in range(grid_size):
        for c in range(grid_size):
            x = c * cell_size
            y = (grid_size - 1 - r) * cell_size   # row 0 on top

            active = state[r, start_c + c]

            if active:
                ax.add_patch(patches.Rectangle((x, y), cell_size, cell_size,
                                               facecolor="black", edgecolor="black", linewidth=0.3))
                ax.add_patch(patches.Circle((x + cell_size / 2, y + cell_size / 2), dot_radius,
                                            facecolor="white", edgecolor="none"))
            else:
                ax.add_patch(patches.Rectangle((x, y), cell_size, cell_size,
                                               facecolor="white", edgecolor="black", linewidth=0.3))
                ax.add_patch(patches.Circle((x + cell_size / 2, y + cell_size / 2), dot_radius,
                                            facecolor="black", edgecolor="none"))

    ax.set_xlim(0, grid_size * cell_size)
    ax.set_ylim(0, grid_size * cell_size)

    save(fig, "abstract grid tessellation rule 30 cellular automaton triangles pattern black white texture")


if __name__ == "__main__":
    draw()
