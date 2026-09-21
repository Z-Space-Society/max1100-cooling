"""Card adapter: tube into the bay + flange clamped to the card. All in mm.

The adapter joins the GPU's own parts to the printed ducting. The working base
since 2026-09-21. V1 is Katie's Rhino model (rhino/1100-singleshroud-v1.3dm),
measured off the card. The tube goes into the bay. The flange sits on the
shroud end plane. The extension bracket's own screws pass through the bracket
holes into the card, so the bracket clamps the adapter on. The power notch
clears the 12V-2x6.

Frame: CAD frame (README.md), which is Katie's Rhino frame. Rhino Top view =
tail view. +X toward the top edge, +Y toward the shroud side, +Z out past the
tail. Dimensions below are measured from REF, the tube's outer corner at the
finger edge / PCB side. REF sits at ORIGIN in Rhino so these files overlay
hers exactly.

Print flange-down (z = 2 face on the bed), tube up. No supports.
"""
from dataclasses import dataclass, replace

from profiles import Curve, Hole, Slab, export, offset, rect

ORIGIN = (-1.5259, -7.3609)   # REF in Katie's Rhino coordinates


@dataclass(frozen=True)
class CardAdapter:
    # ---- Tube (goes into the bay) ----
    tube_x: float = 76.0        # across the opening, finger edge → top edge
    tube_y: float = 20.0        # through the card, PCB side → shroud side
    wall: float = 1.5
    insert: float = 16.0        # depth into the bay, from the shroud end plane
    # ---- Flange (sits on the shroud end plane) ----
    flange_t: float = 2.0
    flange_finger: float = 10.0  # past the tube toward the finger edge
    flange_top: float = 9.0      # past the tube toward the top edge
    flange_pcb: float = 14.0     # past the tube toward the PCB side
    flange_shroud: float = 2.0   # past the tube toward the shroud side
    # Power notch: PCB side, top-edge end. Its top-edge side is flush with the
    # bore's inside face; it runs from the flange's PCB edge up to the tube.
    power_notch_w: float = 25.0
    # ---- Bracket holes (over the card's bracket mounting holes) ----
    bracket_hole_d: float = 3.0
    bracket_holes: tuple = ((-3.0, 17.0), (-3.0, -2.0))  # Katie's: -2.9947, rounded
    # ---- Reference only ----
    fan: float = 120.0          # fan outline, centered on the tube


V1 = CardAdapter()

V2 = replace(
    V1,
    tube_y=22.0,                    # 20 → 22; PCB side stays, shroud side grows 2
    bracket_holes=((-4.0, 18.0), (-4.0, -1.0)),  # 1 toward the finger edge, 1 toward the shroud
    power_notch_w=24.0,             # 25 → 24; finger-side edge moves 1 toward the top edge
)                                   # flange follows the tube: 95 × 38


def build(p):
    w, h = p.tube_x, p.tube_y
    bore = rect(p.wall, p.wall, w - p.wall, h - p.wall)
    fx0, fx1 = -p.flange_finger, w + p.flange_top
    fy0, fy1 = -p.flange_pcb, h + p.flange_shroud
    nx1 = w - p.wall
    nx0 = nx1 - p.power_notch_w
    flange = [(fx0, fy0), (nx0, fy0), (nx0, 0), (nx1, 0),
              (nx1, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)]
    cx, cy, s = w / 2, h / 2, p.fan / 2

    ox, oy = ORIGIN
    o = lambda pts: offset(pts, ox, oy)
    return [
        Slab("Tube", o(rect(0, 0, w, h)), -p.insert, 0, cutouts=[o(bore)]),
        Slab("Flange", o(flange), 0, p.flange_t, cutouts=[o(bore)],
             holes=[Hole(x + ox, y + oy, p.bracket_hole_d) for x, y in p.bracket_holes]),
        Curve("Fan connector", o(rect(cx - s, cy - s, cx + s, cy + s))),
    ]


if __name__ == "__main__":
    export(build(V2), "max1100-card-adapter-v2",
           source="cad/card_adapter.py V2 (generated; edit the script, not this file)")
