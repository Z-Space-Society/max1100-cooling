"""Case side rib: an L down the gap beside card 4 and along the case wall to
the case front. All in mm.

Card 4's shroud side is 12 from the case wall (tape, 2026-09-28,
docs/dimensions.md). The rib has three pieces:

- **Rib**: fills that gap from the case floor up to the top of the power
  buttons (157), so air can't go past the column on that side, and stands on
  the case floor to carry what's above. 10 along the card, from the tail end
  plane toward the I/O end. The cards reach 20 past the motherboard's edge,
  so the floor there is clear.
- **Rail**: turns at the top of the rib and runs along the case wall to the
  case front, top at 157. It's the edge the case's top cover seals against.
  Stops 1 short of the front wall (165 from the tail end plane) so it always
  goes in.
- **Tab**: hangs down from the rail to the wall standoff (~5 proud, 60 from
  the front wall, ~125 above the case floor) and screws to it. A pocket on
  its wall side goes over the standoff, so the rail lies flat on the wall and
  still seals.

11.5 across rather than 12: the 12 is a tape reading, and at a true 12 the
rib would be a press fit, or wouldn't go in at all. The rail and tab keep the
same 11.5, so the part is one flat plate on the wall.

Frame: the comb's (cad/comb.py). X up from the case floor, Y = 0 at card 1's
PCB side and + toward the case wall, Z = 0 the tail end plane and + toward
the case front.

Print on its wall-side face (Y = column + width on the bed), pocket down.
174 × 157 on the bed, 11.5 tall. No supports.
"""
from dataclasses import dataclass

import comb as comb_v
from profiles import Hole, Slab, export, rect


@dataclass(frozen=True)
class CaseSideRib:
    comb: comb_v.Comb = comb_v.V1
    width: float = 11.5         # card 4's shroud side → case wall is 12
                                # (tape); 0.5 under so it slides in
    height: float = 157.0       # case floor → top of the power buttons (tape)
    depth: float = 10.0         # −Z from the tail end plane, toward the I/O end
    # ---- Rail (along the top of the case wall) ----
    front: float = 165.0        # tail end plane → front wall (derived, tape)
    clear: float = 1.0          # off the front, so it always goes in
    rail_h: float = 10.0
    # ---- Tab (down to the wall standoff) ----
    standoff_z: float = 105.0   # 60 from the front wall (tape)
    standoff_x: float = 125.0   # above the case floor (tape, photo)
    tab_w: float = 15.0         # along Z, centred on the standoff
    tab_below: float = 8.0      # tab's lower edge, below the screw
    grip: float = 2.0           # tab up into the rail, so the two fuse
    pocket_d: float = 7.5       # over the standoff
    pocket_depth: float = 5.5   # standoff is ~5 proud
    screw_d: float = 3.6        # clears both 6-32 and M3


V1 = CaseSideRib()


def build(p):
    c = p.comb
    y0 = (c.cards - 1) * c.pitch + c.card_t     # card 4's shroud side
    y1 = y0 + p.width                           # against the case wall
    rail_x = p.height - p.rail_h
    # Tab outline in (z, x): axis="y" slabs, so the holes run across the wall
    zs, xs = p.standoff_z, p.standoff_x
    tab = rect(zs - p.tab_w / 2, xs - p.tab_below,
               zs + p.tab_w / 2, rail_x + p.grip)
    y_pocket = y1 - p.pocket_depth
    return [
        Slab("Rib", rect(0, y0, p.height, y1), -p.depth, 0),
        Slab("Rail", rect(rail_x, y0, p.height, y1),
             -p.depth, p.front - p.clear),
        Slab("Tab", tab, y0, y_pocket, axis="y",
             holes=[Hole(zs, xs, p.screw_d)]),
        # Runs grip back into the screw half so the two fuse. The pocket still
        # stops at y_pocket: the screw half is solid around it there.
        Slab("Tab", tab, y_pocket - p.grip, y1, axis="y",
             holes=[Hole(zs, xs, p.pocket_d)]),
    ]


CURRENT = ("v1", V1)

if __name__ == "__main__":
    n, p = CURRENT
    export(build(p), f"max1100-case-side-rib-{n}",
           source=f"cad/case_side_rib.py {n.upper()} (generated; edit the script, not this file)")
