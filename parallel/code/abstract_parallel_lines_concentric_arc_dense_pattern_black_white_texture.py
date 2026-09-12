import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = Path("output/jpg")
SVG_DIR = Path("output/svg")
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


def parallel_concentric_arc_dense():
    fig, ax = setup_ax()
    n_arcs = 30
    for i in range(n_arcs):
        r = 5 + i * 3.5
        theta = np.linspace(0, 2 * np.pi, 200)
        x = 50 + r * np.cos(theta)
        y = 50 + r * np.sin(theta)
        ax.plot(x, y, color="black", linewidth=0.4)
    save(fig, "parallel_concentric_arc_dense")


def parallel_concentric_arc_sparse():
    fig, ax = setup_ax()
    n_arcs = 15
    for i in range(n_arcs):
        r = 5 + i * 7
        theta = np.linspace(0, 2 * np.pi, 200)
        x = 50 + r * np.cos(theta)
        y = 50 + r * np.sin(theta)
        ax.plot(x, y, color="black", linewidth=0.8)
    save(fig, "parallel_concentric_arc_sparse")


def parallel_converging_fan_wide():
    fig, ax = setup_ax()
    n_lines = 25
    for i in range(n_lines):
        angle = -60 + i * 5
        rad = np.radians(angle)
        x1, y1 = 50, -5
        x2 = 50 + 120 * np.sin(rad)
        y2 = -5 + 120 * np.cos(rad)
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=0.6)
    save(fig, "parallel_converging_fan_wide")


def parallel_converging_fan_narrow():
    fig, ax = setup_ax()
    n_lines = 35
    for i in range(n_lines):
        angle = -30 + i * 1.8
        rad = np.radians(angle)
        x1, y1 = 50, -5
        x2 = 50 + 120 * np.sin(rad)
        y2 = -5 + 120 * np.cos(rad)
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=0.5)
    save(fig, "parallel_converging_fan_narrow")


def parallel_crossing_x_wide():
    fig, ax = setup_ax()
    n_lines = 25
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        ax.plot([-5, 105], [y, 105 - y], color="black", linewidth=0.6)
    save(fig, "parallel_crossing_x_wide")


def parallel_crossing_x_narrow():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        ax.plot([-5, 105], [y, 50 + (50 - y) * 0.5], color="black", linewidth=0.4)
    save(fig, "parallel_crossing_x_narrow")


def parallel_multi_layer_3():
    fig, ax = setup_ax()
    for layer in range(3):
        offset = layer * 15
        for i in range(20):
            y = -5 + i * 5.5 + offset
            ax.plot([-5, 105], [y, y], color="black", linewidth=0.5, alpha=0.7)
    save(fig, "parallel_multi_layer_3")


def parallel_multi_layer_5():
    fig, ax = setup_ax()
    for layer in range(5):
        offset = layer * 10
        for i in range(15):
            y = -5 + i * 7.3 + offset
            ax.plot([-5, 105], [y, y], color="black", linewidth=0.4, alpha=0.5)
    save(fig, "parallel_multi_layer_5")


def parallel_nested_rect_dense():
    fig, ax = setup_ax()
    n_rects = 30
    for i in range(n_rects):
        offset = i * 1.7
        rect = plt.Rectangle((offset, offset), 100 - 2 * offset, 100 - 2 * offset,
                              fill=False, edgecolor="black", linewidth=0.3)
        ax.add_patch(rect)
    save(fig, "parallel_nested_rect_dense")


def parallel_nested_rect_sparse():
    fig, ax = setup_ax()
    n_rects = 10
    for i in range(n_rects):
        offset = i * 5
        rect = plt.Rectangle((offset, offset), 100 - 2 * offset, 100 - 2 * offset,
                              fill=False, edgecolor="black", linewidth=0.8)
        ax.add_patch(rect)
    save(fig, "parallel_nested_rect_sparse")


def parallel_organic_flow_smooth():
    fig, ax = setup_ax()
    n_lines = 35
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        y = y_base + 5 * np.sin(x * 0.05 + i * 0.3) * np.cos(x * 0.02)
        ax.plot(x, y, color="black", linewidth=0.5)
    save(fig, "parallel_organic_flow_smooth")


def parallel_organic_flow_chaotic():
    fig, ax = setup_ax()
    n_lines = 30
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        y = y_base + 8 * np.sin(x * 0.1 + i * 0.5) * np.cos(x * 0.03 + i * 0.2)
        ax.plot(x, y, color="black", linewidth=0.5)
    save(fig, "parallel_organic_flow_chaotic")


def parallel_tapered_extreme():
    fig, ax = setup_ax()
    n_lines = 30
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        thickness = 0.1 + 5.0 * np.abs(np.sin(x / 100 * np.pi))
        from matplotlib.collections import LineCollection
        points = np.array([x, np.full_like(x, y)]).T
        segments = np.array([[points[j], points[j+1]] for j in range(len(points)-1)])
        lc = LineCollection(segments, color="black", linewidths=thickness[:-1])
        ax.add_collection(lc)
    save(fig, "parallel_tapered_extreme")


def parallel_tapered_subtle():
    fig, ax = setup_ax()
    n_lines = 45
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        thickness = 0.3 + 1.5 * np.abs(np.sin(x / 100 * np.pi))
        from matplotlib.collections import LineCollection
        points = np.array([x, np.full_like(x, y)]).T
        segments = np.array([[points[j], points[j+1]] for j in range(len(points)-1)])
        lc = LineCollection(segments, color="black", linewidths=thickness[:-1])
        ax.add_collection(lc)
    save(fig, "parallel_tapered_subtle")


def parallel_varying_length_long():
    fig, ax = setup_ax()
    n_lines = 30
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        x_start = -5 + np.random.uniform(0, 20)
        x_end = 105 - np.random.uniform(0, 20)
        lw = np.random.choice([1.5, 2.0, 2.5])
        ax.plot([x_start, x_end], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_varying_length_long")


def parallel_varying_length_short():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        x_start = -5 + np.random.uniform(10, 40)
        x_end = 105 - np.random.uniform(10, 40)
        lw = np.random.choice([1.0, 1.5, 2.0])
        ax.plot([x_start, x_end], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_varying_length_short")


def parallel_density_circle_large():
    fig, ax = setup_ax()
    n_lines = 35
    center_x, center_y = 50, 50
    radius = 40
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        dist = np.sqrt((y - center_y) ** 2)
        density_factor = max(0, 1 - dist / radius)
        n_segments = int(3 + 12 * density_factor)
        segment_length = 110 / n_segments
        for j in range(n_segments):
            x_start = -5 + j * segment_length
            x_end = x_start + segment_length * 0.7
            ax.plot([x_start, x_end], [y, y], color="black", linewidth=0.5 + 1.5 * density_factor)
    save(fig, "parallel_density_circle_large")


def parallel_density_circle_small():
    fig, ax = setup_ax()
    n_lines = 40
    center_x, center_y = 50, 50
    radius = 20
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        dist = np.sqrt((y - center_y) ** 2)
        density_factor = max(0, 1 - dist / radius)
        n_segments = int(2 + 15 * density_factor)
        segment_length = 110 / n_segments
        for j in range(n_segments):
            x_start = -5 + j * segment_length
            x_end = x_start + segment_length * 0.6
            ax.plot([x_start, x_end], [y, y], color="black", linewidth=0.4 + 2.0 * density_factor)
    save(fig, "parallel_density_circle_small")


if __name__ == "__main__":
    parallel_concentric_arc_dense()
    parallel_concentric_arc_sparse()
    parallel_converging_fan_wide()
    parallel_converging_fan_narrow()
    parallel_crossing_x_wide()
    parallel_crossing_x_narrow()
    parallel_multi_layer_3()
    parallel_multi_layer_5()
    parallel_nested_rect_dense()
    parallel_nested_rect_sparse()
    parallel_organic_flow_smooth()
    parallel_organic_flow_chaotic()
    parallel_tapered_extreme()
    parallel_tapered_subtle()
    parallel_varying_length_long()
    parallel_varying_length_short()
    parallel_density_circle_large()
    parallel_density_circle_small()
