"""Check that card_adapter.V1 still reproduces Katie's Rhino model.

Compares, with rhino/1100-singleshroud-v1.3dm, the XY bounding box of every
extrusion profile (outline, bore, bracket holes; the power notch is part of
the flange outline) and each extrusion's overall bounding box. Profile Z is
left out: Katie extruded the tube from 0 down to -16, we go from -16 up, so
the same solid has its profiles at opposite ends. Run after touching
profiles.py or build(). Exits non-zero on a mismatch.
"""
import sys

import rhino3dm as r

from card_adapter import V1, build
from profiles import RHINO_DIR, write_3dm

TOL = 0.01  # V1 rounds Katie's hole X from -2.9947 to -3.0


def profile_boxes(path):
    boxes = []
    for o in r.File3dm.Read(str(path)).Objects:
        g = o.Geometry
        if type(g).__name__ != "Extrusion":
            continue
        b = g.GetBoundingBox()
        boxes.append((b.Min.X, b.Min.Y, b.Min.Z, b.Max.X, b.Max.Y, b.Max.Z))
        for i in range(g.ProfileCount):
            b = g.Profile3d(i, 0.0).GetBoundingBox()
            boxes.append((b.Min.X, b.Min.Y, b.Max.X, b.Max.Y))
    # Sort on rounded values so float noise can't reorder near-equal boxes.
    return sorted(boxes, key=lambda b: (len(b), [round(v, 1) for v in b]))


ours_path = write_3dm(build(V1), "_check-v1")
try:
    ours = profile_boxes(ours_path)
finally:
    ours_path.unlink()
katie = profile_boxes(RHINO_DIR / "1100-singleshroud-v1.3dm")

worst = max((abs(a - b) for p, q in zip(ours, katie) for a, b in zip(p, q)), default=0)
ok = len(ours) == len(katie) and worst <= TOL
print(f"V1 vs Katie: {len(ours)}/{len(katie)} boxes, worst deviation {worst:.4f} mm "
      f"-> {'OK' if ok else 'MISMATCH'}")
sys.exit(0 if ok else 1)
