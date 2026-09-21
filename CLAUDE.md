# CLAUDE.md

Printed cooling ducts for the Intel Max 1100 (passive 300 W PCIe card).
Python generates each part as both a Rhino `.3dm` and an STL; the docs record
what's measured and why.

## Read first

1. `README.md` → **Terminology**. Use those names in replies, docs, code
   comments and variable names. Never say front/back/top/bottom/left/right
   unqualified. Left/right only with a named view ("in the tail view, left").
   "Up" means toward the shroud side, as in the tail view. If the user uses an
   ambiguous word, restate it in the defined term to confirm ("you mean the
   tail end?"). "Shroud" is the GPU's own cover, never our printed part.
2. `docs/dimensions.md` for card measurements. `docs/cooling.md` for why the
   design is the way it is.

## Current design: the card adapter

`cad/card_adapter.py`: the printed piece between the GPU's own parts and the
rest of the printed ducting. It's based on Katie's Rhino model
`rhino/1100-singleshroud-v1.3dm`. Katie is the user's wife, a professional
Rhino user, and not always available, so the scripts have to interoperate with
her files: same coordinates, native extrusions, named layers.

- Versions are `CardAdapter` dataclass instances. `V1` reproduces Katie's
  file (`make check` proves it). Each later version is `replace(previous,
  ...)`, with one comment per change saying what moved and why. Don't edit an
  older version's values.
- Nothing is final until the user says so. A new version is a draft until
  it's been printed and fit-checked.

## Layout

- `cad/profiles.py`: `Slab` (extruded outline, polygon cutouts, round holes),
  `Curve` (reference outline, `.3dm` only), `export()` → `rhino/<name>.3dm` +
  `stl/<name>.stl`
- `cad/card_adapter.py`: the card adapter
- `cad/check_v1.py`: V1 against Katie's `.3dm`
- `cad/archive/`, `stl/archive/`, `images/archive/`: superseded parts (v2.1
  card part, fit tests, coupon). Their own left-handed frame with `MIRROR_Y`.
  Leave them alone.
- `rhino/`: Katie's originals (don't modify) and generated `max1100-*.3dm`
- `docs/`, `images/`

## Running

```sh
make setup   # once
make parts   # regenerate current parts
make check   # after touching profiles.py or build()
```

Each export prints watertight/volume/bounds. **Watertight must be True**
before an STL is committed.

## Conventions

- mm everywhere. File names use hyphens (`max1100-card-adapter-v2.3dm`), never
  underscores. Python scripts use underscores so they can import each other.
- CAD frame = Katie's Rhino frame: +X toward the top edge, +Y toward the
  shroud side, +Z out past the tail, Z = 0 the shroud end plane. The Rhino Top
  view is the tail view. Card adapter dimensions are measured from REF (tube
  outer corner, finger side / PCB side), and `ORIGIN` puts REF at Katie's
  coordinates.
- rhino3dm gotcha: `Extrusion.AddInnerProfile` takes curves in the
  extrusion's local frame (origin at the outline's first point, z = 0).
  `profiles.write_3dm` handles this, so don't pass world coordinates.
- rhino3dm can't do booleans or meshing. Build parts from extruded profiles
  (`Slab`). If a part ever needs something that isn't an extrusion, raise it
  before reaching for another approach.
- Commit the regenerated `.3dm` and STL together with the script change that
  produced them.
- When a card dimension changes, update `docs/dimensions.md` with where the
  number came from (datasheet, calipers, tape, Katie, fit test, plus the date).
  A dimension that's blank there is unknown. Don't guess; ask.
- Refactors must not change geometry. Regenerate and compare: byte-identical
  STL, or matching volume and bounds, and `make check` passes.

## Relationship to SCNVault

The vault (`~/Projects/Z-Space/scnvault/Projects/Max 1100 Notes/`) holds the
project log, host/driver notes and the RackChoice 4U fit. This repo holds the
dimensions, cooling design notes and all CAD. Don't edit the vault from here
unless asked.
