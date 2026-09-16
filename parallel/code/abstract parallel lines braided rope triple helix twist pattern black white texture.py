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
    print(f"Saved: {jpg_path} | {svg_path}")


def abstract_parallel_lines_braided_rope_triple_helix_twist_pattern_black_white_texture():
    """
    Three bundles of parallel lines twist around each other like a braided rope
    or triple helix running vertically. Each bundle contains several tightly-spaced
    lines that collectively sinusoidally oscillate — offset by 120° from each other.
    The vertical axis is the twist axis.
    """
    fig, ax = setup_ax()

    # Vertical sweep
    y = np.linspace(-5, 105, 900)

    # Helix parameters
    twist_freq = 0.08      # full twists per canvas unit
    bundle_spread = 3.5    # how wide each strand bundle is
    center_x = 50.0
    amplitude = 22.0       # how far each strand centre swings left-right

    n_strands_per_bundle = 7   # lines per bundle
    n_bundles = 3

    # Phase offsets for each bundle (120° apart)
    phase_offsets = [0, 2 * np.pi / 3, 4 * np.pi / 3]

    # For realistic braid look: each bundle's line weight varies as cosine
    # (thicker when facing viewer = in front)

    for b in range(n_bundles):
        phase = phase_offsets[b]
        # Centre path of this bundle
        cx = center_x + amplitude * np.cos(2 * np.pi * twist_freq * y + phase)

        # "Depth" in the z-direction (determines draw order & weight)
        cz = np.sin(2 * np.pi * twist_freq * y + phase)  # -1 to 1

        for s in range(n_strands_per_bundle):
            offset = (s - (n_strands_per_bundle - 1) / 2) * (bundle_spread / n_strands_per_bundle)
            x_strand = cx + offset

            # Line weight: thicker when in front (cz > 0), thinner behind
            # Segment by segment so weight varies along the curve
            seg_size = 60
            for seg in range(0, len(y) - seg_size, seg_size // 2):
                y_seg = y[seg:seg + seg_size]
                x_seg = x_strand[seg:seg + seg_size]
                cz_seg = float(np.mean(cz[seg:seg + seg_size]))

                depth_factor = (cz_seg + 1) / 2  # 0..1 (0=back, 1=front)
                lw = 0.25 + 0.9 * depth_factor
                alpha_val = 0.35 + 0.65 * depth_factor

                # Mask canvas bounds
                mask = (x_seg < -6) | (x_seg > 106)
                x_seg_m = np.where(mask, np.nan, x_seg)

                ax.plot(x_seg_m, y_seg, color="black", linewidth=lw,
                        alpha=alpha_val, solid_capstyle="round")

    save(fig, "abstract parallel lines braided rope triple helix twist pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_braided_rope_triple_helix_twist_pattern_black_white_texture()
