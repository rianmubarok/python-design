import shutil
from pathlib import Path

BASE = Path(r"D:\PEMROGRAMAN\PROJECT\2026\python-design\parallel")
REAL_DIR = BASE / "real-detected"
SVG_DIR = BASE / "output" / "svg"
DATE = "12092026"

# Map old names to new names
name_map = {
    "parallel_broken_dense": "parallel_vector_nirmana_broken_dense",
    "parallel_broken_sparse": "parallel_vector_nirmana_broken_sparse",
    "parallel_concentric_rect": "parallel_vector_nirmana_concentric_rect",
    "parallel_converging_fan_narrow": "parallel_vector_nirmana_converging_fan_narrow",
    "parallel_converging_fan_wide": "parallel_vector_nirmana_converging_fan_wide",
    "parallel_crossing_x_narrow": "parallel_vector_nirmana_crossing_x_narrow",
    "parallel_crossing_x_wide": "parallel_vector_nirmana_crossing_x_wide",
    "parallel_curved_tight": "parallel_vector_nirmana_curved_tight",
    "parallel_curved_tighter": "parallel_vector_nirmana_curved_tighter",
    "parallel_curved_wider": "parallel_vector_nirmana_curved_wide",
    "parallel_density_center": "parallel_vector_nirmana_density_center",
    "parallel_density_circle_large": "parallel_vector_nirmana_density_circle_large",
    "parallel_density_circle_small": "parallel_vector_nirmana_density_circle_small",
    "parallel_density_edges": "parallel_vector_nirmana_density_edges",
    "parallel_gradient_dense": "parallel_vector_nirmana_gradient_dense",
    "parallel_gradient_offset_bottom": "parallel_vector_nirmana_gradient_offset_bottom",
    "parallel_gradient_offset_top": "parallel_vector_nirmana_gradient_offset_top",
    "parallel_gradient_sparse": "parallel_vector_nirmana_gradient_sparse",
    "parallel_interleaved": "parallel_vector_nirmana_interleaved",
    "parallel_mosaic": "parallel_vector_nirmana_mosaic",
    "parallel_multi_layer_3": "parallel_vector_nirmana_multi_layer_3",
    "parallel_multi_layer_5": "parallel_vector_nirmana_multi_layer_5",
    "parallel_nested_rect_dense": "parallel_vector_nirmana_nested_rect_dense",
    "parallel_nested_rect_sparse": "parallel_vector_nirmana_nested_rect_sparse",
    "parallel_organic_flow_chaotic": "parallel_vector_nirmana_organic_flow_chaotic",
    "parallel_organic_flow_smooth": "parallel_vector_nirmana_organic_flow_smooth",
    "parallel_radial_gradient": "parallel_vector_nirmana_radial_gradient",
    "parallel_rhythmic_fast": "parallel_vector_nirmana_rhythmic_fast",
    "parallel_rhythmic_slow": "parallel_vector_nirmana_rhythmic_slow",
    "parallel_seamless_dashed": "parallel_vector_nirmana_seamless_dashed",
    "parallel_seamless_gradient": "parallel_vector_nirmana_seamless_gradient",
    "parallel_seamless_staggered": "parallel_vector_nirmana_seamless_staggered",
    "parallel_sine_high_freq": "parallel_vector_nirmana_sine_high_freq",
    "parallel_sine_wave": "parallel_vector_nirmana_sine_wave",
    "parallel_staggered_narrow": "parallel_vector_nirmana_staggered_narrow",
    "parallel_staggered_wide": "parallel_vector_nirmana_staggered_wide",
    "parallel_stepped": "parallel_vector_nirmana_stepped",
    "parallel_tapered_extreme": "parallel_vector_nirmana_tapered_extreme",
    "parallel_tapered_gradient": "parallel_vector_nirmana_tapered_gradient",
    "parallel_tapered_subtle": "parallel_vector_nirmana_tapered_subtle",
    "parallel_varying_length_long": "parallel_vector_nirmana_varying_length_long",
    "parallel_varying_length_short": "parallel_vector_nirmana_varying_length_short",
    "parallel_wave_modulated_strong": "parallel_vector_nirmana_wave_modulated_strong",
    "parallel_wave_modulated_weak": "parallel_vector_nirmana_wave_modulated_weak",
    "parallel_woven": "parallel_vector_nirmana_woven",
    "parallel_zigzag": "parallel_vector_nirmana_zigzag",
}

copied = 0
for old_name, new_name in name_map.items():
    svg_file = SVG_DIR / f"{old_name}_{DATE}.svg"
    if svg_file.exists():
        new_file = REAL_DIR / f"{new_name}.svg"
        if not new_file.exists():
            shutil.copy2(svg_file, new_file)
            copied += 1
            print(f"OK: {old_name} -> {new_name}")
    else:
        print(f"Missing: {old_name}")

print(f"\nCopied: {copied}")
