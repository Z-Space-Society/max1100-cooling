# Rhino models

Rhino 8 `.3dm`, mm. Two kinds of file live here:

- **Katie's originals** (`1100-singleshroud-v1.3dm`): drawn by hand in Rhino.
  Don't edit them in place; they're the reference `make check` compares
  against.
- **Generated** (`max1100-*.3dm`): written by a script in `cad/`. Every object
  carries a `source` Attribute User Text naming the script. Changes made here in
  Rhino get overwritten on the next `make parts`, so either change the script,
  or save a Rhino edit under a new name and we'll port it back.

All card adapter files share Katie's coordinates. The Top view is the tail
view (README, "Views"), so they overlay one another exactly.

| File | Part | Made by | Notes |
|---|---|---|---|
| `1100-singleshroud-v1.3dm` | Card adapter V1 | Katie, 2026-09-18 | Tube 76 × 20 × 16, flange 95 × 36 × 2, power notch 25 × 14, Ø3 bracket holes 19 apart. `cad/card_adapter.py` `V1` reproduces it (holes rounded 0.005) |
| `max1100-card-adapter-v2.3dm` | Card adapter V2 | `cad/card_adapter.py` | Tube 22, flange 95 × 38, power notch 24 × 14, bracket holes moved 1 toward the finger edge and 1 toward the shroud side. Draft |
