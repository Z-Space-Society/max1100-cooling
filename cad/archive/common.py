"""ARCHIVED. Helpers for the v2.1 scripts (duct_card.py, box_fit_test.py). In mm.

Superseded by the card adapter (cad/card_adapter.py, cad/profiles.py), which
uses the CAD frame in README.md. This is the older, left-handed v2.1 frame:
  x  along the card. 0 = shroud end plane. Negative = into the card.
  y  across the bay (the 76). 0 = inside bottom edge of the opening
     (finger side). 76 = the 12V-2x6 end (top-edge side).
  z  through the card (the 24). 0 = inside of the shroud top.
     Positive = toward the PCB and the bracket plate.

This frame is left-handed relative to the real card. Parts are built in it
and then mirrored in y on export (MIRROR_Y) so the printed part is correct.
"""
from pathlib import Path

import trimesh
from trimesh.creation import box

REPO = Path(__file__).resolve().parents[2]
STL_DIR = REPO / "stl" / "archive"

# Exported y = -y. See module docstring.
MIRROR_Y = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def at(m, x=0, y=0, z=0):
    m.apply_translation([x, y, z]); return m


def blk(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from its min/max corners."""
    return at(box([x1 - x0, y1 - y0, z1 - z0]),
              (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)


def U(ms):
    return trimesh.boolean.union(ms, engine="manifold")


def D(a, bs):
    return trimesh.boolean.difference([a] + bs, engine="manifold")


def export(part, name, subdir=""):
    """Write stl/<subdir>/<name>.stl and print a sanity line."""
    out = STL_DIR / subdir / f"{name}.stl"
    out.parent.mkdir(parents=True, exist_ok=True)
    part.export(out)
    print(f"{out.relative_to(REPO)}  watertight: {part.is_watertight}  "
          f"extents: {part.extents.round(2)}  bounds: {part.bounds.round(2).tolist()}")
