"""Tail box gauge: the tail box's outline at card-top height. All in mm.

A fit test for option G (docs/cooling.md). Comb V1 settled the column; this
checks the box's other two numbers, both taken by tape on 2026-09-23:

1. **Column datum → case wall, 172.** Does a rail 1 short of it slide in
   beside card 4 along the box's whole depth, with nothing on the slot-side
   wall (standoffs, ~5 proud, positions unknown) in the way?
2. **Tail end plane → grill, 165** (120 to the bracket tip + 45). Does the
   front bar land 1 short of the front plate?
3. And, by being there: does anything at card-top height foul the box's
   footprint? The extension bracket tips, the front bar's underside, the
   row of modules in sheet-metal brackets, the 12V-2x6 cables.

Both nominal dimensions are 1 short on purpose, so the part always goes in
and the gap left is the reading: shim it. If it won't go in, the tape was
more than 1 long.

It is Comb V1 (spine and teeth, unchanged, for registration on the four
cards) plus an open ring: a rail over card 1, a rail in the 12 between card 4
and the case wall, and a bar across at the front plate. Open in the middle
so the power cables and the bracket tips pass through it. It hangs from the
four top edges like the comb and slides on from the case front, before the
power cables.

**Which side the 12 is on** isn't written down (docs/dimensions.md). This
takes it past card 4's shroud side: card 4 is in board slot 7 and spills into
the 8th case slot, the one nearest the side wall, and a card's shroud side
faces away from slot 1. If that's wrong the part is mirrored in Y, not
reworked.

Frame: the comb's (cad/comb.py). X up from the case floor, Y = 0 at card 1's
PCB side and + toward the case wall, Z = 0 the tail end plane and + toward
the case front.

Print ring-face down (the X = card_top + spine_h face on the bed), teeth up.
189 × 171 on the bed, 47 tall. No supports; a brim helps the teeth.
"""
from dataclasses import dataclass

import comb as comb_v
from profiles import Slab, export, rect


@dataclass(frozen=True)
class TailBoxGauge:
    comb: comb_v.Comb = comb_v.V1
    wall: float = 172.0         # card 1's PCB side → case wall (tape)
    front: float = 165.0        # tail end plane → grill (derived, tape)
    clear: float = 1.0          # taken off both, so the part always fits
    rail_w: float = 10.0        # card 1 rail and front bar. The wall rail
                                # fills whatever the 12 is


V1 = TailBoxGauge()


def build(p):
    c = p.comb
    column = (c.cards - 1) * c.pitch + c.card_t
    wall = p.wall - p.clear
    front = p.front - p.clear
    x0, x1 = c.card_top, c.card_top + c.spine_h
    parts = comb_v.build(c)
    parts += [
        Slab("Rails", rect(x0, 0, x1, p.rail_w), -c.depth, front),
        Slab("Rails", rect(x0, column, x1, wall), -c.depth, front),
        Slab("Front bar", rect(x0, 0, x1, wall), front - p.rail_w, front),
    ]
    return parts


CURRENT = ("v1", V1)

if __name__ == "__main__":
    n, p = CURRENT
    export(build(p), f"max1100-tail-box-gauge-{n}",
           source=f"cad/tail_box_gauge.py {n.upper()} (generated; edit the script, not this file)")
