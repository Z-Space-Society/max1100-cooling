"""Card part v2.1: spigot + bolt tab. All dimensions in mm.

Spigot goes 32 into the tail bay, carries on out past the tail end, and bolts
through the extension bracket's outer hole with one M3. The bracket stays on
the card. A separate flare part (not yet drawn) plugs into the open end.

Frame: card frame in common.py, mirrored in y on export.

Print standing on the outer end (x = OUT_LEN on the bed). PETG, 0.2 mm,
4 perimeters, 20 % infill, no supports.
"""
import trimesh
from trimesh.creation import cylinder

from common import MIRROR_Y, D, U, at, blk, export

# ---- Spigot / tube -------------------------------------------------------
TUBE_Y, TUBE_Z = 76.0, 24.0   # outer section (was 26, printed 2 too tall)
INSERT = 32.0                 # depth into the bay
OUT_LEN = 50.0                # length past the shroud end; clears bracket (45)
WALL = 1.6                    # 4 perimeters at 0.4

# Depth stop: small lip on the shroud side only, seats on the shroud end.
LIP_H, LIP_T = 3.0, 2.4

# ---- Bolt tab (measured 2026-09-18, tape) --------------------------------
HOLE_X = 38.1                 # 1.5" past the shroud end
HOLE_Y = -6.35                # 0.25" below the inside bottom edge of the opening
# Card stack, from the shroud: PCB top at 31.75 (1.25"). Bracket plate sits on
# the back of the PCB. PCB thickness assumed 1.6.
PCB_T = 1.6
PLATE_Z = 31.75 + PCB_T       # inner face of the bracket plate
PAD_GAP = 0.5                 # leave a hair; the bolt pulls it in
PAD_T = 3.0                   # tab thickness
PAD_X0 = 16.0                 # stay clear of the riveted inner hole (~8 out)
PAD_Y0, PAD_Y1 = -10.0, 12.0  # -10 = assumed clearance to the L's side flange
HOLE_D = 3.4                  # M3 clearance
SLOT = 4.0                    # slot length along x, for fine-tuning

x0, x1 = -INSERT, OUT_LEN
tube = blk(x0, x1, 0, TUBE_Y, 0, TUBE_Z)
bore = blk(x0 - 1, x1 + 1, WALL, TUBE_Y - WALL, WALL, TUBE_Z - WALL)

# Stop lip on the shroud side, with a 45 deg chamfer under it for printing.
lip = blk(0, LIP_T, 0, TUBE_Y, -LIP_H, 0)
chamfer = trimesh.convex.convex_hull([
    (x, y, z) for y in (0, TUBE_Y)
    for (x, z) in [(LIP_T - 0.01, 0.01), (LIP_T + LIP_H, 0.01), (LIP_T - 0.01, -LIP_H)]])

pad_z1 = PLATE_Z - PAD_GAP
pad_z0 = pad_z1 - PAD_T
pad = blk(PAD_X0, x1, PAD_Y0, PAD_Y1, pad_z0, pad_z1)
web = blk(PAD_X0, x1, 0, PAD_Y1, TUBE_Z - WALL, pad_z0 + 0.01)

slot = U([
    at(cylinder(radius=HOLE_D / 2, height=20, sections=48),
       HOLE_X - SLOT / 2, HOLE_Y, pad_z1 - 5),
    at(cylinder(radius=HOLE_D / 2, height=20, sections=48),
       HOLE_X + SLOT / 2, HOLE_Y, pad_z1 - 5),
    blk(HOLE_X - SLOT / 2, HOLE_X + SLOT / 2,
        HOLE_Y - HOLE_D / 2, HOLE_Y + HOLE_D / 2, pad_z1 - 15, pad_z1 + 5),
])

part = D(U([tube, lip, chamfer, pad, web]), [bore, slot])
# Mirror so the tab lands on the finger side: left in the tail view, shroud
# up (v2 shipped mirrored).
part.apply_transform(MIRROR_Y)
export(part, "max1100-duct-card")
