"""Tail box demo: the tail box as an L, for showing people. All in mm.

Not for use. A model of what option G (docs/cooling.md) is building toward,
printed so it can sit on the four cards and be looked at. Same outline as the
tail box gauge (cad/tail_box_gauge.py), 1 short of the case wall and the
front plate, but a shell instead of a frame:

- Comb V1's spine, with its teeth run down to the finger edge, so they seal
  the whole gap between cards, not just the top 37. They are what holds it on.
- One side wall from the lid to the case floor, the full depth, against card
  1's PCB side and flush with the comb's end. Outside the column, so it
  clears card 1 and its extension bracket plate.
- A lid out to the case wall. The case wall is the box's other side, so
  there's no wall printed there.

The wall and lid are 1.2, so anything that fouls (the wall lands on what is
probably motherboard, docs/dimensions.md) can be cut away. The gauge's rails
and front bar are gone; the wall and lid do their job here.

So in the tail view it's an upside-down L, closed by the case wall: open to
the case floor, the fans (+Z) and the cards (−Z).

Frame: the gauge's. Print lid down (the X = card_top + spine_h face on the
bed), wall and teeth up. 189 × 172 on the bed, 137 tall. No supports and no
brim: the first layer is the whole lid.
"""
from dataclasses import dataclass, replace

import comb as comb_v
import tail_box_gauge as gauge_v
from profiles import Slab, export, rect


@dataclass(frozen=True)
class TailBoxDemo:
    gauge: gauge_v.TailBoxGauge = gauge_v.V1
    card_h: float = 111.15      # finger edge → top edge; the teeth stop at
                                # the finger edge
    wall_t: float = 1.2         # wall and lid, 3 lines at a 0.4 nozzle.
                                # Thin to print fast and to cut back where
                                # they foul


V1 = TailBoxDemo()


def build(p):
    g = p.gauge
    c = replace(g.comb, tooth_len=p.card_h)
    t = p.wall_t
    wall = g.wall - g.clear
    front = g.front - g.clear
    x1 = c.card_top + c.spine_h
    parts = comb_v.build(c)
    parts += [
        Slab("Wall", rect(0, -t, x1, 0), -c.depth, front),
        Slab("Lid", rect(x1 - t, -t, x1, wall), -c.depth, front),
    ]
    return parts


CURRENT = ("v1", V1)

if __name__ == "__main__":
    n, p = CURRENT
    export(build(p), f"max1100-tail-box-demo-{n}",
           source=f"cad/tail_box_demo.py {n.upper()} (generated; edit the script, not this file)")
