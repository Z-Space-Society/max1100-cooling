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

Print flange-down (flange face on the bed: z = 2, or the seat's face at z = 3
when there is one), tube up. No supports; the seat's rebate floor is a 1
overhang, 1 above the bed.
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
    # ---- Scoop: the PCB-side wall carries on past the tube's end, angled ----
    # toward the PCB side, so the air reaches the fins on that side. Goes in by
    # hooking it over the power plug and sliding it home. 0 = no scoop.
    scoop_len: float = 0.0      # extra depth past the tube's end
    scoop_drop: float = 0.0     # how far it angles toward the PCB side over that
    scoop_top_gap: float = 0.0  # how far short of the top-edge end it stops,
                                # to clear the row of header pins there
    # ---- Seat: a layer added on the flange face (+Z, toward the fan) that ----
    # stops short of the bore all round, leaving a rebate around the bore's
    # mouth for the next part to sit in. The layer's face becomes the print
    # face; the bore stays full size. The rebate skips the power notch's
    # length on the PCB side. 0 = no seat.
    seat_t: float = 0.0         # layer thickness = rebate depth
    seat_inset: float = 0.0     # how far the layer stops short of the bore
    # ---- Reference only ----
    fan: float = 120.0          # fan outline, centered on the tube


V1 = CardAdapter()

V2 = replace(
    V1,
    tube_y=22.0,                    # 20 → 22; PCB side stays, shroud side grows 2
    bracket_holes=((-4.0, 18.0), (-4.0, -1.0)),  # 1 toward the finger edge, 1 toward the shroud
    power_notch_w=24.0,             # 25 → 24; finger-side edge moves 1 toward the top edge
)                                   # flange follows the tube: 95 × 38

V3 = replace(
    V2,
    scoop_len=10.0,                 # PCB-side wall goes 10 deeper (26 total); could be 8
    scoop_drop=5.0,                 # angled 5 toward the PCB side (~27°), a first guess
)

# V3 printed and fitted 2026-09-22, with two problems: the bracket holes were
# too tight for the screws, and the scoop fouled a row of header pins near the
# top edge (2 to 3 in from the side), which had to be cut away by hand.
# V4 was never printed, so the seat (2026-10-02) went into it in place.
V4 = replace(
    V3,
    bracket_hole_d=3.4,             # 3.0 → 3.4, clearance for M3
    scoop_top_gap=4.0,              # stop 4 short of the top-edge end, clearing the pins
    seat_t=1.0,                     # 1 added on the flange face: 3 thick overall
    seat_inset=1.0,                 # rebate 75 × 21 × 1 deep around the bore, for the next part;
                                    # none along the power notch
)


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
    parts = [
        Slab("Tube", o(rect(0, 0, w, h)), -p.insert, 0, cutouts=[o(bore)]),
        Slab("Flange", o(flange), 0, p.flange_t, cutouts=[o(bore)],
             holes=[Hole(x + ox, y + oy, p.bracket_hole_d) for x, y in p.bracket_holes]),
        Curve("Fan connector", o(rect(cx - s, cy - s, cx + s, cy + s))),
    ]
    if p.seat_t:
        # No rebate along the power notch: the strip left between the two
        # would be too thin to print. The layer runs up to the bore there.
        i, b = p.wall - p.seat_inset, p.wall
        rebate = [(i, i), (nx0, i), (nx0, b), (w - i, b), (w - i, h - i), (i, h - i)]
        parts.append(Slab("Seat", o(flange), p.flange_t, p.flange_t + p.seat_t,
                          cutouts=[o(rebate)],
                          holes=[Hole(x + ox, y + oy, p.bracket_hole_d) for x, y in p.bracket_holes]))
    if p.scoop_len:
        # Side section (Y, Z) of the PCB-side wall, run across the tube's full
        # width. A tab 1 up into the tube's wall fuses the two.
        z0, z1, t, d = -p.insert, -p.insert - p.scoop_len, p.wall, p.scoop_drop
        side = [(0, z0 + 1), (t, z0 + 1), (t, z0), (t - d, z1), (-d, z1), (0, z0)]
        parts.append(Slab("Scoop", [(y + oy, z) for y, z in side],
                          ox, ox + w - p.scoop_top_gap, axis="x"))
    return parts


CURRENT = ("v4", V4)  # what `make parts` writes; older files stay in git as the record

if __name__ == "__main__":
    n, p = CURRENT
    export(build(p), f"max1100-card-adapter-{n}",
           source=f"cad/card_adapter.py {n.upper()} (generated; edit the script, not this file)")
