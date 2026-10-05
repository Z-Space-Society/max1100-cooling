"""Flare: card adapter → one 140 fan, for the single card in Salmon. All in mm.

A first draft, to print and see what works. Nothing here is settled.

A lip drops into the card adapter's seat (the rebate around the bore's mouth)
and lands on its floor, so the bore stays 73 × 19 with no step. The lip skips
the power notch's length, like the rebate; there the joint is a butt joint,
and the gap keys the flare so it only goes on one way.

The taper is two stages, because profiles.py only extrudes:

1. **Stage 1** widens shroud side ↔ PCB side and stays the tube's size along
   the height. Side sections, extruded across X. The shroud-side wall widens
   straight off the seat face. The PCB-side wall runs straight for 30 (room
   to push the power cable aside), angles to the extension bracket's bar,
   passes it, and carries on widening past the card's PCB-side face.
2. **Stage 2** widens finger edge ↔ top edge at a constant thickness.
   Sections extruded across Y.

Over the bar the PCB-side wall is thickened into a pad with a flat face lying
on the bar. An ear at each end carries a hole over the bar's hole, outside
the air path, so a screwdriver reaches both from the PCB side.

The fan bolts onto the fan plate, face to face. The duct behind the plate is
smaller than the fan (`mouth`) so the whole thing ends 130 past the tail end
with a 27 fan on it: Salmon has 135 (docs/dimensions.md).

Guessed, not measured: the bar's shroud-facing face is taken as 2 inside the
flange's PCB-side edge (1 gap + 1 of sheet, and the flange's edge flush with
the card's PCB-side face). If the pad doesn't lie on the bar, that's why.

Frame: CAD frame (README.md), the card adapter's. Dimensions are measured
from REF like the adapter's.

Print fan plate down. Every wall is then vertical or leans 45°. No supports.
"""
from dataclasses import dataclass, replace
from math import hypot, pi, tan

import card_adapter
from profiles import FUSE_EPS, Hole, Slab, export, rect


@dataclass(frozen=True)
class Flare:
    adapter: card_adapter.CardAdapter = card_adapter.V4
    wall: float = 2.0           # so it reaches 0.5 outside the tube all round
    wall_notch: float = 1.5     # PCB side over the power notch, straight run
                                # only: flush with the tube, clear of the plug
    wall_finger: float = 1.5    # finger-side cheek: flush with the tube, where
                                # V3's tube already cleared the bracket's foot
    # ---- Lip (into the adapter's rebate) ----
    lip_clear: float = 0.2      # off the rebate's outer wall. A guess: no
                                # print-to-print fit has been measured yet
    # ---- Stage 1 ----
    straight: float = 30.0      # PCB-side wall, past the seat face, before it angles
    # ---- Extension bracket's bar (docs/dimensions.md, 2026-10-02) ----
    bar_z0: float = 35.0        # past the shroud end plane
    bar_z1: float = 45.0
    bar_inside: float = 2.0     # bar's shroud-facing face, in from the flange's
                                # PCB-side edge. Guessed, see above
    bar_clear: float = 1.0      # past the bar's far edge before widening again
    bar_holes: tuple = (-8.0, 80.0)  # X: round hole, slot. 4 past the bracket holes; 88 apart
    bar_hole_z: float = 42.0
    bar_hole_d: float = 3.4     # same as the adapter's bracket holes
    ear_t: float = 3.0
    ear_finger: float = -12.0   # X of the bar's ends
    ear_top: float = 84.0
    # ---- Fan ----
    mouth: float = 129.0        # duct's inside at the fan, square. Sets the length
    fan: float = 140.0
    fan_holes: float = 124.5    # hole spacing
    fan_hole_d: float = 4.3     # fan screws cut their own thread
    plate_t: float = 3.0
    corner: float = 13.0        # plate left across each corner of the mouth, for the screws
    # ---- Fit test ----
    stop_at_bar: bool = False   # cut off at the bar's far edge: just the lip,
                                # the straight run, the bar pad and the ears


V1 = Flare()

# The least that checks both joints: lip in the adapter's seat, pad and ears
# on the bar. The shroud-side wall is left straight. Print cut end down (the bar's far edge on the bed), no supports.
FIT_V1 = replace(V1, stop_at_bar=True)

# Fit test V1 printed 2026-10-05. The lip didn't drop into V4's rebate or
# line up with it; not yet diagnosed, Katie to look at it in Rhino.
V2 = replace(
    V1,
    wall_notch=2.0,             # 1.5 → 2: the step over the power notch wasn't
                                # needed to clear the plug and looked cluttered.
)                               # The PCB side is now flat all the way across
FIT_V2 = replace(V2, stop_at_bar=True)


def _meet(p, d, q, e):
    den = d[0] * e[1] - d[1] * e[0]
    s = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    return (p[0] + s * d[0], p[1] + s * d[1])


def _outer(inner, t, side):
    """The wall's outside face: `inner` [(u, z)], z rising, moved t square to
    each run toward `side` (±u), mitred, ends cut at inner's end heights.
    t can be a list, one per run."""
    ts = t if isinstance(t, (list, tuple)) else [t] * (len(inner) - 1)
    lines = []
    for (u0, z0), (u1, z1), tt in zip(inner, inner[1:], ts):
        n = hypot(u1 - u0, z1 - z0)
        lines.append(((u0 + side * (z1 - z0) / n * tt, z0 - side * (u1 - u0) / n * tt),
                      (u1 - u0, z1 - z0)))
    pts = [_meet(*lines[0], (0, inner[0][1]), (1, 0))]
    pts += [_meet(*a, *b) for a, b in zip(lines, lines[1:])]
    pts.append(_meet(*lines[-1], (0, inner[-1][1]), (1, 0)))
    return pts


def build(p):
    a = p.adapter
    w, h, b = a.tube_x, a.tube_y, a.wall
    ox, oy = card_adapter.ORIGIN
    z_floor = a.flange_t                    # rebate floor
    z_seat = a.flange_t + a.seat_t          # seat face
    nx0 = w - b - a.power_notch_w           # finger-side end of the lip's gap
    t = p.wall
    mitre = t * tan(pi / 8)                 # a 45° corner moves the outside this far

    # ---- Air path, stage 1: (Y, Z) ----
    bar_y = -a.flange_pcb + p.bar_inside    # the face the pad lies on
    z_bend = z_seat + p.straight
    z_pass = p.bar_z1 + p.bar_clear + mitre
    lap = 0.5                               # straight run where two pieces fuse
    z_open = z_seat + lap                   # the lip comes up this far into the walls
    # Where the inside reaches `mouth` across, both walls at 45°.
    z1 = (p.mouth - (h - b) + z_open + (bar_y + t) + z_pass) / 2
    ys, yp = (h - b) + (z1 - z_open), (bar_y + t) - (z1 - z_pass)
    shroud_in = [(h - b, z_seat), (h - b, z_open), (ys, z1), (ys, z1 + lap / 2)]
    pcb_in = [(b, z_seat), (b, z_bend), (bar_y + t, z_bend + b - (bar_y + t)),
              (bar_y + t, z_pass), (yp, z1), (yp, z1 + lap / 2)]
    if p.stop_at_bar:
        zc = p.bar_z1
        shroud_in = [(h - b, z_seat), (h - b, zc)]  # straight: nothing to test there
        pcb_in = pcb_in[:3] + [(bar_y + t, zc)]
    # The shroud side widens straight off the seat face, so its outside is
    # the slope carried back to that face (a mitre there would dip below it).
    so = _outer(shroud_in[1:], t, +1) if not p.stop_at_bar else []
    shroud_out = [(so[0][0] - lap, z_seat)] + so if so else _outer(shroud_in, t, +1)
    pcb_out = _outer(pcb_in, t, -1)
    pcb_out_notch = _outer(pcb_in, [p.wall_notch] + [t] * (len(pcb_in) - 2), -1)

    xs = lambda pts: [(y + oy, z) for y, z in pts]          # axis="x" outline
    ys_ = lambda pts: [(z, x + ox) for x, z in pts]         # axis="y" outline
    x0, x1 = 0.0, w + (t - b)               # stage 1's outside along the height

    # ---- Lip: a C, the rebate less its clearance, inside flush with the bore ----
    i = b - a.seat_inset + p.lip_clear
    lip = [(i, i), (nx0 - p.lip_clear, i), (nx0 - p.lip_clear, b), (b, b), (b, h - b),
           (w - b, h - b), (w - b, b), (w - i, b), (w - i, h - i), (i, h - i)]
    parts = [Slab("Lip", [(x + ox, y + oy) for x, y in lip], z_floor, z_open)]

    # ---- Stage 1 ----
    side = shroud_out + pcb_out[::-1]
    parts += [
        Slab("Shroud-side wall", xs(shroud_in + shroud_out[::-1]), ox + x0, ox + x1, axis="x"),
        Slab("PCB-side wall", xs(pcb_in + pcb_out[::-1]), ox + x0, ox + nx0, axis="x"),
        Slab("PCB-side wall", xs(pcb_in + pcb_out_notch[::-1]), ox + nx0 - 0.5, ox + x1, axis="x"),
        Slab("Cheeks", xs(side), ox + x0, ox + p.wall_finger, axis="x"),
        Slab("Cheeks", xs(side), ox + w - b, ox + x1, axis="x"),
        # Pad: the wall thickened down to the bar, flat face on it.
        Slab("Bar pad", xs([(bar_y, p.bar_z0), (-t, p.bar_z0), (bar_y + 1, p.bar_z1),
                            (bar_y, p.bar_z1)]), ox + x0, ox + x1, axis="x"),
    ]
    # Ears: past the cheeks, over the bar's holes. The slope on the fan side
    # is so they print without support, fan plate down.
    for xe, xin, hx in ((p.ear_finger, x0 + 0.5, p.bar_holes[0]),
                        (p.ear_top, x1 - 0.5, p.bar_holes[1])):
        ear = [(xin, p.bar_z0), (xe, p.bar_z0), (xe, p.bar_z1), (xin, p.bar_z1 + abs(xe - xin))]
        if p.stop_at_bar:
            ear[-1] = (xin, p.bar_z1)
        parts.append(Slab("Ears", ys_(ear), oy + bar_y, oy + bar_y + p.ear_t, axis="y",
                          holes=[Hole(p.bar_hole_z, hx + ox, p.bar_hole_d)]))
    if p.stop_at_bar:
        return parts

    # ---- Stage 2: (X, Z), across the full thickness ----
    dx = (p.mouth - (w - 2 * b)) / 2
    z2 = z1 + lap + dx                      # fan face
    zs = z1 + lap / 4                       # starts inside stage 1's last straight run
    # Stage 2 starts 0.05 bigger all round than stage 1, inside and out. Faces
    # of the two that lie in one plane, or 1 µm apart, break the STL's union.
    g = 0.05
    finger_in = [(b - g, zs), (b - g, z1 + lap), (b - dx, z2)]
    top_in = [(w - b + g, zs), (w - b + g, z1 + lap), (w - b + dx, z2)]
    finger_out, top_out = _outer(finger_in, t, -1), _outer(top_in, t, +1)
    y0, y1 = yp - t - g, ys + t + g
    plate = finger_out + top_out[::-1]
    parts += [
        Slab("Finger-side wall", ys_(finger_in + finger_out[::-1]), oy + y0, oy + y1, axis="y"),
        Slab("Top-edge-side wall", ys_(top_in + top_out[::-1]), oy + y0, oy + y1, axis="y"),
        Slab("Stage 2 plates", ys_(plate), oy + y0, oy + yp - g, axis="y"),
        Slab("Stage 2 plates", ys_(plate), oy + ys + g, oy + y1, axis="y"),
    ]

    # ---- Fan plate: the fan bolts on face to face ----
    # Exactly coplanar faces break the STL's union (see profiles.to_mesh), so
    # the plate's opening is cut 0.5 into the walls standing on it, and its
    # fan face is 1 µm past the walls' ends.
    cx, cy, m, c = w / 2, (ys + yp) / 2, p.mouth / 2 + 0.5, p.corner + 0.5
    mouth = [(cx - m + c, cy - m), (cx + m - c, cy - m), (cx + m, cy - m + c), (cx + m, cy + m - c),
             (cx + m - c, cy + m), (cx - m + c, cy + m), (cx - m, cy + m - c), (cx - m, cy - m + c)]
    f, s = p.fan / 2, p.fan_holes / 2
    parts.append(Slab(
        "Fan plate", [(x + ox, y + oy) for x, y in rect(cx - f, cy - f, cx + f, cy + f)],
        z2 - p.plate_t, z2 + FUSE_EPS, cutouts=[[(x + ox, y + oy) for x, y in mouth]],
        holes=[Hole(cx + i * s + ox, cy + j * s + oy, p.fan_hole_d) for i in (-1, 1) for j in (-1, 1)]))
    return parts


CURRENT = ("v2", V2)

if __name__ == "__main__":
    n, p = CURRENT
    export(build(p), f"max1100-flare-{n}",
           source=f"cad/flare.py {n.upper()} (generated; edit the script, not this file)")
    export(build(FIT_V2), f"max1100-flare-fit-test-{n}",
           source=f"cad/flare.py FIT_{n.upper()} (generated; edit the script, not this file)")
