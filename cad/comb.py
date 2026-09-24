"""Comb: spine plus teeth, spanning the four card tails. All in mm.

A fit test, printed and fitted to the four installed cards on 2026-09-23. It
asked three questions and answered all three:

1. Does one rigid part span four cards? PCIe pitch is exactly 40.64, but four
   cards on a real board in a real case could accumulate error across 160.
   **Yes** — no per-card float needed.
2. Do 2.0 teeth enter all three gaps? **Yes**, as printed, no trimming.
3. Does the spine sit flat on the four top edges? **Yes**, at 127.

It also turned out to be a gauge rather than a fit test. The spine is
3 × pitch + card_t long and came out flush with both outer faces of the
column, which settled the card's thickness at 38.64 against the datasheet's
34.35 — at 34.35 it would have overhung by 4.3. See docs/dimensions.md.

**V1 hangs from the top edges** and slides on from the case front, so it goes
on before the power cables. That is a print decision, not a design one: it
makes the part a single constant cross-section — every layer identical, no
overhang anywhere, no supports. A spine down at the case floor, which is where
the tail box would want it so it can carry the cards' weight, cannot follow
the teeth back past the tail end plane: that space is over the motherboard.
The fit questions above are the same either way.

Frame: the CAD frame (README.md), the card adapter's, spanning the column.
X = toward the top edge, which is up from the case floor; X = 0 at the floor.
Y = toward the shroud side, card to card; Y = 0 at card 1's outer face.
Z = out past the tail, toward the case front; Z = 0 the tail end plane, so the
whole part sits at Z < 0, in between and above the cards.

Print flat, the X-Y face on the bed, 25 tall. A brim helps: the teeth are 2
wide on every layer including the first. No supports.
"""
from dataclasses import dataclass

from profiles import Slab, export, rect


@dataclass(frozen=True)
class Comb:
    cards: int = 4
    pitch: float = 40.64        # PCIe, 2 x 20.32. Exact: the slots set it
    # Card envelope, PCB side → shroud side. Measured 38.64, not the
    # datasheet's 34.35: V1's spine came out flush with both outer faces of
    # the column, which settled it. See docs/dimensions.md. Sets both the
    # teeth's place within the pitch and the overall span.
    card_t: float = 38.64
    card_top: float = 127.0     # top edge, PCB side, above the case floor
    # ---- Spine (rests on the four top edges) ----
    spine_h: float = 10.0
    depth: float = 25.0         # −Z, back along the cards. Spine and teeth
                                # share it, which is what keeps this a single
                                # constant cross-section
    # ---- Teeth (down into the gaps between cards) ----
    tooth_t: float = 2.0
    tooth_len: float = 37.0     # down from the top edge
    tooth_grip: float = 2.0     # up into the spine, so the two fuse


V1 = Comb()


def build(p):
    column = (p.cards - 1) * p.pitch + p.card_t
    parts = [Slab("Spine", rect(p.card_top, 0, p.card_top + p.spine_h, column),
                  -p.depth, 0)]
    for n in range(p.cards - 1):
        # The gap runs from this card's shroud face to the next card's PCB
        # face: [n*pitch + card_t, (n+1)*pitch]. Centre the tooth in it.
        mid = n * p.pitch + (p.card_t + p.pitch) / 2
        parts.append(Slab(
            "Teeth",
            rect(p.card_top - p.tooth_len, mid - p.tooth_t / 2,
                 p.card_top + p.tooth_grip, mid + p.tooth_t / 2),
            -p.depth, 0))
    return parts


CURRENT = ("v1", V1)

if __name__ == "__main__":
    n, p = CURRENT
    export(build(p), f"max1100-comb-{n}",
           source=f"cad/comb.py {n.upper()} (generated; edit the script, not this file)")
