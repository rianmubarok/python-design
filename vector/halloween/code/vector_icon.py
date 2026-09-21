"""Pure-code Halloween icon silhouettes for matplotlib.

All shapes are defined entirely in this file as SVG path strings (no
external assets, no third-party SVG parser).  A self-contained SVG-path
tokeniser converts them to matplotlib Path objects at import time.

Icons are faithful reproductions of the Lucide icon designs, redrawn as
hardcoded path data - no file loading required.
"""

import re
import math
import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath
from matplotlib.transforms import Affine2D

# ---------------------------------------------------------------------------
# Minimal SVG-path parser  (supports M/m, L/l, H/h, V/v, C/c, S/s, Q/q,
#                             A/a, Z/z)
# ---------------------------------------------------------------------------

_CMD_RE = re.compile(r"([MmLlHhVvCcSsQqAaZz])|([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)")


def _tokenise(d):
    for m in _CMD_RE.finditer(d):
        if m.group(1):
            yield ("cmd", m.group(1))
        else:
            yield ("num", float(m.group(2)))


def _angle(ux, uy, vx, vy):
    cross = ux * vy - uy * vx
    dot = ux * vx + uy * vy
    n = math.hypot(ux, uy) * math.hypot(vx, vy)
    return math.copysign(math.acos(max(-1.0, min(1.0, dot / (n or 1e-12)))), cross)


def _arc_to_cubic(x1, y1, rx, ry, phi_deg, large, sweep, x2, y2, n_segs=8):
    if x1 == x2 and y1 == y2:
        return []
    phi = math.radians(phi_deg)
    cp, sp = math.cos(phi), math.sin(phi)
    rx, ry = abs(rx), abs(ry)
    mx, my = (x1 - x2) / 2, (y1 - y2) / 2
    x1p =  cp * mx + sp * my
    y1p = -sp * mx + cp * my
    num   = max(0.0, rx**2 * ry**2 - rx**2 * y1p**2 - ry**2 * x1p**2)
    denom = rx**2 * y1p**2 + ry**2 * x1p**2
    sq = math.sqrt(num / denom) if denom else 0.0
    if large == sweep:
        sq = -sq
    cxp =  sq * rx * y1p / ry
    cyp = -sq * ry * x1p / rx
    cx = cp * cxp - sp * cyp + (x1 + x2) / 2
    cy = sp * cxp + cp * cyp + (y1 + y2) / 2
    theta1 = _angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = _angle((x1p - cxp) / rx, (y1p - cyp) / ry,
                    (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sweep and dtheta < 0:
        dtheta += 2 * math.pi
    segs = []
    t0 = theta1
    dt = dtheta / n_segs
    alpha = math.sin(dt) * (math.sqrt(4 + 3 * math.tan(dt / 2) ** 2) - 1) / 3
    for _ in range(n_segs):
        t1 = t0 + dt
        p0 = np.array([cx + rx * math.cos(t0) * cp - ry * math.sin(t0) * sp,
                        cy + rx * math.cos(t0) * sp + ry * math.sin(t0) * cp])
        p3 = np.array([cx + rx * math.cos(t1) * cp - ry * math.sin(t1) * sp,
                        cy + rx * math.cos(t1) * sp + ry * math.sin(t1) * cp])
        d0 = np.array([-rx * math.sin(t0) * cp - ry * math.cos(t0) * sp,
                        -rx * math.sin(t0) * sp + ry * math.cos(t0) * cp])
        d1 = np.array([-rx * math.sin(t1) * cp - ry * math.cos(t1) * sp,
                        -rx * math.sin(t1) * sp + ry * math.cos(t1) * cp])
        segs.append((p0 + alpha * d0, p3 - alpha * d1, p3))
        t0 = t1
    return segs


def _parse_svg_path(d):
    tokens = list(_tokenise(d))
    segments = []
    cur_cmd = None
    buf = []
    for kind, val in tokens:
        if kind == "cmd":
            if cur_cmd is not None:
                segments.append((cur_cmd, buf))
            cur_cmd = val
            buf = []
        else:
            buf.append(val)
    if cur_cmd is not None:
        segments.append((cur_cmd, buf))

    verts = []
    codes = []
    cx, cy = 0.0, 0.0
    sx, sy = 0.0, 0.0
    lc1x, lc1y = None, None

    def moveto(ax, ay):
        nonlocal cx, cy, sx, sy
        verts.append([ax, ay]); codes.append(MplPath.MOVETO)
        cx, cy = ax, ay; sx, sy = ax, ay

    def lineto(ax, ay):
        nonlocal cx, cy
        verts.append([ax, ay]); codes.append(MplPath.LINETO)
        cx, cy = ax, ay

    def curveto(c1x, c1y, c2x, c2y, ax, ay):
        nonlocal cx, cy, lc1x, lc1y
        verts += [[c1x, c1y], [c2x, c2y], [ax, ay]]
        codes += [MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4]
        lc1x, lc1y = c2x, c2y
        cx, cy = ax, ay

    def closepath():
        nonlocal cx, cy
        verts.append([sx, sy]); codes.append(MplPath.CLOSEPOLY)
        cx, cy = sx, sy

    for cmd, args in segments:
        rel = cmd.islower()
        c = cmd.upper()
        ns = list(args)

        if c == "M":
            pairs = [(ns[i], ns[i+1]) for i in range(0, len(ns)-1, 2)]
            for k, (ax, ay) in enumerate(pairs):
                if rel: ax += cx; ay += cy
                if k == 0: moveto(ax, ay)
                else:      lineto(ax, ay)
            lc1x = lc1y = None

        elif c == "Z":
            closepath(); lc1x = lc1y = None

        elif c == "L":
            for i in range(0, len(ns)-1, 2):
                ax, ay = ns[i], ns[i+1]
                if rel: ax += cx; ay += cy
                lineto(ax, ay)
            lc1x = lc1y = None

        elif c == "H":
            for v in ns:
                ax = (cx + v) if rel else v
                lineto(ax, cy)
            lc1x = lc1y = None

        elif c == "V":
            for v in ns:
                ay = (cy + v) if rel else v
                lineto(cx, ay)
            lc1x = lc1y = None

        elif c == "C":
            for i in range(0, len(ns)-5, 6):
                c1x, c1y, c2x, c2y, ax, ay = ns[i:i+6]
                if rel:
                    c1x+=cx; c1y+=cy; c2x+=cx; c2y+=cy; ax+=cx; ay+=cy
                curveto(c1x, c1y, c2x, c2y, ax, ay)

        elif c == "S":
            for i in range(0, len(ns)-3, 4):
                c2x, c2y, ax, ay = ns[i:i+4]
                if rel: c2x+=cx; c2y+=cy; ax+=cx; ay+=cy
                c1x = 2*cx - lc1x if lc1x is not None else cx
                c1y = 2*cy - lc1y if lc1y is not None else cy
                curveto(c1x, c1y, c2x, c2y, ax, ay)

        elif c == "Q":
            for i in range(0, len(ns)-3, 4):
                qx, qy, ax, ay = ns[i:i+4]
                if rel: qx+=cx; qy+=cy; ax+=cx; ay+=cy
                c1x = cx + 2/3*(qx-cx); c1y = cy + 2/3*(qy-cy)
                c2x = ax + 2/3*(qx-ax); c2y = ay + 2/3*(qy-ay)
                curveto(c1x, c1y, c2x, c2y, ax, ay)
            lc1x = lc1y = None

        elif c == "A":
            for i in range(0, len(ns)-6, 7):
                rx2,ry2,phi,large,sweep,ax,ay = ns[i:i+7]
                if rel: ax+=cx; ay+=cy
                for cp1,cp2,ep in _arc_to_cubic(cx,cy,rx2,ry2,phi,int(large),int(sweep),ax,ay):
                    curveto(cp1[0],cp1[1],cp2[0],cp2[1],ep[0],ep[1])
            lc1x = lc1y = None

    if not verts:
        raise ValueError("Empty path")
    return MplPath(np.array(verts, dtype=float), np.array(codes, dtype=np.uint8))


# ---------------------------------------------------------------------------
# Hardcoded icon path data  (viewBox 0 0 24 24, from Lucide icon designs)
# ---------------------------------------------------------------------------

_ICON_PATHS = {
    "cat": [
        "M12 5c.67 0 1.35.09 2 .26 1.78-2 5.03-2.84 6.42-2.26 1.4.58-.42 7-.42 7 .57 1.07 1 2.24 1 3.44C21 17.9 16.97 21 12 21s-9-3-9-7.56c0-1.25.5-2.4 1-3.44 0 0-1.89-6.42-.5-7 1.39-.58 4.72.23 6.5 2.23A9.04 9.04 0 0 1 12 5Z",
        "M8 14v.5",
        "M16 14v.5",
        "M11.25 16.25h1.5L12 17l-.75-.75Z",
    ],
    "ghost": [
        "M15 10v1",
        "M7.528 20.472a1.6 1.6 0 012.277 0l1.057 1.056a1.6 1.6 0 002.276 0l1.057-1.056a1.6 1.6 0 012.277 0l1.114 1.114a1.4 1.4 0 002.414-1V10a8 8 0 00-16 0v10.586a1.4 1.4 0 002.414 1z",
        "M9 10v1",
    ],
    "pumpkin": [
        "M13 2c-1 1-1 2-1 2",
        "M17 4c-.9 0-1.8.4-2.5 1.2a3.32 3.32 0 0 0-5 0C8.8 4.4 7.9 4 7 4c-2.8 0-5 4-5 9s2.2 9 5 9c.9 0 1.8-.4 2.5-1.2a3.32 3.32 0 0 0 5 0c.7.8 1.6 1.2 2.5 1.2 2.8 0 5-4 5-9s-2.2-9-5-9",
        "M10 11 8 9l-2 2",
        "m18 11-2-2-2 2",
        "m6 15 2 2 2-2 2 2 2-2 2 2 2-2",
    ],
    "spider": [
        "M10 5v1",
        "M14 6V5",
        "M10 10.4V8a2 2 0 1 1 4 0v2.4",
        "M7 15H4l-2 2.5",
        "M7.42 17 5 20l1 2",
        "m8 12-4-1-2-3",
        "M9 11 5.5 6 7 2",
        "M8 18a5 5 0 1 1 8 0s-2 3-4 4c-2-1-4-4-4-4",
        "m15 11 3.5-5L17 2",
        "m16 12 4-1 2-3",
        "M17 15h3l2 2.5",
        "M16.57 17 19 20l-1 2",
    ],
    "owl": [
        "M12 9a4 4 0 1 1 8 0v12h-4C9.4 21 4 15.6 4 9a4 4 0 1 1 8 0v1",
        "M8 9h.01",
        "M16 9h.01",
        "M20 21a3.9 3.9 0 1 1 0-7.8",
        "M10 19.4V22",
        "M14 20.85V22",
    ],
}

# ---------------------------------------------------------------------------
# Build / cache matplotlib Paths
# ---------------------------------------------------------------------------

_CACHE = {}


def _build_path(name):
    parts = []
    for d_str in _ICON_PATHS[name]:
        try:
            parts.append(_parse_svg_path(d_str.strip()))
        except Exception:
            continue
    if not parts:
        raise ValueError(f"No paths built for icon '{name}'")
    if len(parts) == 1:
        return parts[0]
    verts = np.concatenate([p.vertices for p in parts])
    codes = np.concatenate([p.codes for p in parts])
    return MplPath(verts, codes)


# ---------------------------------------------------------------------------
# Public API  (identical to the original vector_icon.py)
# ---------------------------------------------------------------------------

def icon_patch(name, cx, cy, size, facecolor="black", edgecolor="none",
               linewidth=4.0, zorder=2):
    """Return a PathPatch of icon *name* centred at (cx, cy) within *size*."""
    if name not in _CACHE:
        _CACHE[name] = _build_path(name)
    path = _CACHE[name]
    verts = path.vertices
    xmin, ymin = verts.min(axis=0)
    xmax, ymax = verts.max(axis=0)
    w = max(xmax - xmin, 1e-6)
    h = max(ymax - ymin, 1e-6)
    scale = size / max(w, h)
    trans = (
        Affine2D()
        .translate(-(xmin + xmax) / 2, -(ymin + ymax) / 2)
        .scale(scale, -scale)
        .translate(cx, cy)
    )
    return PathPatch(
        path.transformed(trans),
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        joinstyle="round",
        capstyle="round",
        zorder=zorder,
    )
