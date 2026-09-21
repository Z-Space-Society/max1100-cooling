"""Box fit test v2. All dimensions in mm.

Just the spigot from the card part v2.1: 76 x 24 outer, 32 into the bay,
with the 3 mm shroud-side stop lip. No tab, no outside run, so it prints fast.

Frame: card frame in common.py. Not mirrored; the part is symmetric in y.

Print lip-down (the lip's outer face is flat on the bed). No supports.
"""
from common import D, U, blk, export

TUBE_Y, TUBE_Z = 76.0, 24.0
INSERT = 32.0
WALL = 1.6
LIP_H, LIP_T = 3.0, 2.4

tube = blk(-INSERT, LIP_T, 0, TUBE_Y, 0, TUBE_Z)
lip = blk(0, LIP_T, 0, TUBE_Y, -LIP_H, 0)
bore = blk(-INSERT - 1, LIP_T + 1, WALL, TUBE_Y - WALL, WALL, TUBE_Z - WALL)
part = D(U([tube, lip]), [bore])
export(part, "max1100-box-fit-test-v2")
