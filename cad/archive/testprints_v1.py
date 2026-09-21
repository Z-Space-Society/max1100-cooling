"""SUPERSEDED. SCN Single 1100 test prints, v1. All dimensions in mm.

Kept for the record. Results (2026-09-18): the 26 box was 2 too tall (now 24,
see cad/box_fit_test.py); no hole pair lined up, and the ledge holes were
dropped for one bolt through the extension bracket (see cad/duct_card.py).

max1100-box-fit-test.stl : 26 x 76 box, 32 mm into the card, with a depth-stop flange.
max1100-hole-coupon.stl  : flat plate testing the bracket foot hole pattern.
Print: PETG, 0.2 mm layers, 4 perimeters, flat face on bed, no supports.
"""
from pathlib import Path

import trimesh
from trimesh.creation import box, cylinder

OUT = Path(__file__).resolve().parents[2] / "stl" / "archive"
OUT.mkdir(parents=True, exist_ok=True)

# ---- Box fit test -------------------------------------------------------
BOX_H, BOX_W, BOX_DEPTH = 26.0, 76.0, 32.0   # outer section, insertion depth
WALL = 1.6                                   # 4 perimeters at 0.4 mm
FLANGE_LIP, FLANGE_T = 3.0, 2.4              # stop flange overhang and thickness

def at(mesh, x=0, y=0, z=0):
    mesh.apply_translation([x, y, z]); return mesh

flange = at(box([BOX_W + 2*FLANGE_LIP, BOX_H + 2*FLANGE_LIP, FLANGE_T]), z=FLANGE_T/2)
tube_outer = at(box([BOX_W, BOX_H, BOX_DEPTH]), z=FLANGE_T + BOX_DEPTH/2)
bore = at(box([BOX_W - 2*WALL, BOX_H - 2*WALL, FLANGE_T + BOX_DEPTH + 2]),
          z=(FLANGE_T + BOX_DEPTH)/2)
box_part = trimesh.boolean.difference(
    [trimesh.boolean.union([flange, tube_outer], engine="manifold"), bore],
    engine="manifold")
box_part.export(OUT / "max1100-box-fit-test.stl")

# ---- Hole coupon --------------------------------------------------------
T = 2.4             # plate thickness
D = 3.4             # clearance: passes both M2.5 and M3
SPACING = 30.0      # center to center, from the rubbing
OFFSET = 4.4        # possible sideways offset of the second hole, from the rubbing
plate = at(box([22.0, SPACING + 14.0, T]), x=OFFSET/2, y=SPACING/2, z=T/2)
holes = [at(cylinder(radius=D/2, height=T + 2, sections=64), x=x, y=y, z=T/2)
         for x, y in [(0, 0),          # A: reference hole
                      (0, SPACING),    # B: straight-line pattern
                      (OFFSET, SPACING)]]  # C: offset pattern
coupon = trimesh.boolean.difference([plate] + holes, engine="manifold")
coupon.export(OUT / "max1100-hole-coupon.stl")

for name, m in [("max1100-box-fit-test", box_part), ("max1100-hole-coupon", coupon)]:
    print(name, "watertight:", m.is_watertight, "extents:", m.extents.round(2))
