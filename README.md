# max1100-cooling

Printed ducts for cooling the Intel Data Center GPU Max 1100, a passive 300 W
server card, with ordinary fans. First target is a single card in **Salmon**
(Lian Li LANCOOL 216 tower). The per-card part carries over to a four-card
plenum in a 4U chassis.

- [Dimensions](docs/dimensions.md): card, column and chassis measurements,
  datasheet and hand-measured
- [Cooling](docs/cooling.md): the problem, design decisions, fan choice, test method
- [RackChoice 4U](docs/rackchoice-4u.md): the quad's chassis — what fits, what's
  still unmeasured
- Project log and host notes live in SCNVault: `Projects/Max 1100 Notes/` for
  the single card, `Projects/QuadBox/` for the four-card appliance

## Terminology

Use these names every time. **Do not use front, back, top, bottom, left or
right on their own.** Left and right are only allowed with a named view (below).

### The card

```
                          SIDE VIEW (looking at the shroud side)

   I/O end                                                     tail end
     ┃ ┌───────────────────────── top edge ──────────────────────────┐
     ┃ │                                                             │▒ bay  ══ extension
     ┃ │                    shroud side (cover)                      │▒         bracket
     ┃ │                                                             │▒
     ┃ └──────┬▄▄▄▄▄▄▄▄▄▄▄▄┬───────── finger edge ───────────────────┘
     ┃        gold fingers
  I/O bracket

   ◀── into the card (−Z)                                   out past the tail (+Z) ──▶
```

```
                 TAIL VIEW (the default): standing past the tail end,
                 looking into the bay, shroud side up. Schematic, not to scale.
                 This is Rhino's Top view of the card adapter models.

                                   SHROUD SIDE  (+Y)
                ┌────────────────────────────────────────────────────┐  ┬
                │   ┌──────────────────────────────────────────┐     │  │
   FINGER EDGE  │ ● │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ fin band ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│     │  │  TOP EDGE
      (−X)   ◀──┤   │              bay opening                 │ 12V ├──▶   (+X)
                │ ● │      base plate · PCB · headers          │ 2x6 │  │
                │   └──────────────────────────────────────────┘     │  │ 38.64
                └────────────────────────────────────────────────────┘  ┴ thickness
                                    PCB SIDE  (−Y)
                ├──────────────────────── 111.15 height ─────────────┤

                ● = extension bracket mounting holes (finger side)
                +Z points out of the page, toward you (out past the tail)
```

| Term | Means | Avoid saying |
|---|---|---|
| **I/O end** | End with the PCIe I/O bracket. Air **exits** here. Sits at the rear of a case. | back, rear, front |
| **Tail end** | Opposite end: the bay, fins, 12V-2x6, extension bracket. Air **enters** here. | front, back, end |
| **Finger edge** | Long edge with the PCIe gold fingers. Plugs into the board. | bottom |
| **Top edge** | Long edge opposite the fingers. Black strip (bridge cover?) runs along it. | top (alone) |
| **Shroud side** | Face covered by the shroud cover. The fins sit against it inside. Older notes: "shroud top". "Up" in the tail view. | top, front, cooler side |
| **PCB side** | Opposite face: the back of the PCB, where the extension bracket plate sits. "Down" in the tail view. | back, bottom |
| **Length** | I/O end → tail end. 266.7 (312 with extension bracket). | |
| **Height** | Finger edge → top edge. 111.15. | width |
| **Thickness** | Shroud side → PCB side. **38.64** measured, not the datasheet's 34.35. | width, depth |

### The tail end

| Term | Means |
|---|---|
| **Shroud end plane** | Plane of the shroud's end at the tail. Z = 0. All "into the card" and "past the tail" distances measure from here. |
| **Bay** | The recessed pocket at the tail end. Not a flat face. |
| **Opening** | The bay's mouth at the shroud end plane, where the tube goes in. |
| **Fin band** | The fin stack as seen in the bay: a band along the shroud side. |
| **Fin face** | The fins' exposed ends, 37 to 39 into the bay. |
| **Fin throat** | The area of fin face air can actually enter. Not yet calipered. |
| **Connector column** | The part of the bay beside the fins with the 12V-2x6 (top-edge side), headers (CNSPI1, CNAMC1, SWAMC1). Stays open to the room. |
| **12V-2x6** | Power connector. Top-edge side of the tail end, toward the PCB side. Plugs in axially, needs ~35 straight cable. |
| **Extension bracket** | Flat L-plate on the PCB side, reaches 45 past the tail to a server card guide. Stays on: its screws now clamp the card adapter to the card. |
| **Bracket mounting holes** | The two threaded holes on the card, finger side of the tail end, that the extension bracket screws into (Torx T8). 19 apart (Katie). The adapter's bracket holes line up with these. |
| **Bracket plate** | The part of the extension bracket lying against the PCB side. |

### Card adapter (current design)

The printed piece that joins the GPU's own parts (the bay, the shroud end
plane, the extension bracket) to the printed ducting. Everything after it
(flare, fan) plugs into it. The working base since 2026-09-21: Katie's Rhino
model, adjusted here.

```
   CARD ADAPTER V2 in the tail view: flange face toward you, tube going away into the bay.

                                      shroud side ↑
      ┌──────────────────────────────────────────────────────────────┐ ┬ 2
      │      ┌─────────────────────────────────────────────────┐     │ ┼
      │  ○   │                                                 │     │ │
      │      │           tube 76 × 22 outside, 16 deep         │     │ │ 22
      │      │           bore 73 × 19 (1.5 wall)               │     │ │
      │  ○   └─────────────────────────────┬──────────────────┬┘     │ ┼
      │                                    │ power notch      │      │ │ 14
      └────────────────────────────────────┘ 24 × 14          └──────┘ ┴
                                      PCB side ↓
      ├─ 10 ─┼──────────────────────── 76 ──────────────────────┼─ 9 ─┤
      finger edge ◀                                            ▶ top edge

      Flange 95 × 38 × 2.   ○ bracket holes Ø3, 19 apart, 4 out from the tube's
      finger-side face: one 4 in from the tube's shroud face, one 1 past its PCB face.
      Power notch: from the flange's PCB edge up to the tube; its top-edge side
      is flush with the bore's inside face.
```

| Term | Means |
|---|---|
| **Card adapter** | The per-card printed piece (`cad/card_adapter.py`): adapter tube + flange. Always its own piece, bolted to the card by the extension bracket. One per card; the quad reuses it unchanged. Not "shroud": that's the GPU's own cover. |
| **Adapter tube** | Rectangular duct that goes 16 into the bay (−Z). Plain "tube" inside `card_adapter.py` means this one. |
| **Bore** | The inside of the air path, 73 × 19, where the air goes. Runs through the adapter tube, the flange and the plenum tube at the same section, with no step. |
| **Flange** | Plate on the shroud end plane. Sets the depth and carries the bracket holes. |
| **Power notch** | Cutout in the flange's PCB side, top-edge end, clearing the 12V-2x6. |
| **Scoop** | The tube's PCB-side wall carried on past the tube's end, angled toward the PCB side, so air reaches the fins on that side. Goes in by hooking it over the power plug and sliding it home. Stops short of the top-edge end to clear the header pins in the bay. |
| **Bracket holes** | Two Ø3 holes in the flange's finger-side end. The extension bracket's screws pass through them into the card's bracket mounting holes. |
| **Fan connector** | Reference outline in the .3dm (120 × 120) for the fan-side piece. Not solid. |
| **Flare** | Future Salmon-only piece: card adapter → fan. Size (120 or 140) undecided. |

### Quad (brainstorming)

Nothing is decided. These are names for things being talked about, so we're
arguing about the same objects — not a description of a design. Several fan
layouts are live; see [cooling](docs/cooling.md#quad). The only thing drawn so
far is the comb, and that's a fit test.

| Term | Means |
|---|---|
| **Plenum** | The quad's chamber beyond the card adapters: one box, fed by the fan panel, feeding all four. Maybe more than one printed piece. Never one piece with the adapters. |
| **Plenum tube** | One of the four passages from the plenum to a card adapter (+Z from the flange face). Same 73 × 19 bore as the adapter tube — the same air path, split across two parts. |
| **Slip joint** | Where a plenum tube meets a card adapter. Whatever its final form, it is the **tolerance joint**: it absorbs the slot-to-slot error so neither part has to be accurate. |
| **Fan panel** | The plenum's front face, carrying the fans that feed it. Its slot-side edge is flush with the card column's wall, so anything wider overhangs toward the PSU side. |
| **Front stage** | Fans on the case front wall feeding the plenum. There for **filtered room air**, not for pressure. |
| **Collar** | A short sealed duct between fan stages, or from the front stage into the fan panel. Must be a closed ring, not corner posts, or series fans lose their series. |
| **Transition** | The printed piece from the fan face to the four plenum tubes, where the duct changes section. |
| **Card column** | The four cards at 40.64 slot pitch: 160 measured across the cards, bore band 141. Sits against one side wall, so everything wider has to overhang toward the PSU. |
| **Tail box** | Option G: one box from the case front wall back to the four tail ends, sealing on the card column instead of on four separate adapters. Bolts to the floor standoffs, the top rail and the front wall. |
| **Tail wall** | The tail box's face at the tail end plane — the thing the user called the "back plate". Closes everything except the four bay openings. |
| **Comb** | Spine plus teeth spanning the column, holding the teeth on the 40.64 pitch. Part of the tail wall. `cad/comb.py`. |
| **Comb tooth** | One tooth, in the gap between two adjacent cards — the "spacer between the GPUs". Seals the gap, locates the card sideways, and in a floor-mounted comb carries its weight. 2.0 thick. |

### Views

Say which view you mean before saying left or right.

| View | How you look | What's where |
|---|---|---|
| **Tail view** (the default) | Standing past the tail end, looking into the bay, **shroud side up**. Rhino's Top view. | Finger edge **left**, top edge and 12V-2x6 **right**, PCB side down |
| **Salmon installed** | Standing at the case front, looking in toward the rear | Card horizontal. Shroud side **down**, finger edge **right** (into the board), top edge toward the glass, tail end toward you |

### CAD frame

The CAD frame is Katie's Rhino frame. It's right-handed, so nothing is
mirrored.

| Axis | + direction | In the tail view |
|---|---|---|
| **X** | Toward the top edge | Right |
| **Y** | Toward the shroud side | Up |
| **Z** | Out past the tail. − = into the card | Toward you |

Z = 0 is the shroud end plane. In XY, the card adapter measures from **REF**,
the tube's outer corner at the finger side and PCB side. REF is placed at
Katie's Rhino coordinates (−1.5259, −7.3609) so our files overlay hers exactly.

## Parts

| Script | Output | Status |
|---|---|---|
| [`cad/card_adapter.py`](cad/card_adapter.py) | `rhino/max1100-card-adapter-v4.3dm`, `stl/max1100-card-adapter-v4.stl` | **Card adapter V4** (`CURRENT`): V3 + Ø3.4 bracket holes and the scoop 4 short of the top-edge end. Not yet printed |
| | `*-v2.*`, `*-v3.*` | Earlier versions, kept as the record. V3 was printed and fitted. `make parts` writes only `CURRENT`; to rebuild an older one, point `CURRENT` at it |
| [`cad/comb.py`](cad/comb.py) | `rhino/max1100-comb-v1.3dm`, `stl/max1100-comb-v1.stl` | **Comb V1** (`CURRENT`): fit test for the quad. Printed and fitted 2026-09-23 — spans the four cards, teeth into all three gaps |
| [`cad/check_v1.py`](cad/check_v1.py) | (none) | Confirms the card adapter's `V1` still reproduces Katie's `.3dm` |
| [`cad/archive/`](cad/archive/) | `stl/archive/`, `images/archive/` | Superseded: card part v2.1, box fit tests, hole coupon. Kept for the record |

Rhino models are in [`rhino/`](rhino/): Katie's originals, plus the `.3dm`
each script writes. Parts are built from extruded profiles in
[`cad/profiles.py`](cad/profiles.py), which writes each one as a native Rhino
extrusion (editable in Rhino) and as a single watertight STL.

**Print settings** (match the coupons or the numbers don't transfer): PETG,
0.2 mm layers, 4 perimeters, 20 % infill, no supports. Orientation is in each
script's docstring — card adapter flange down, comb flat on its X-Y face.

## Build

```sh
make setup     # uv venv + pinned trimesh, manifold3d, numpy, scipy, rhino3dm
make parts     # regenerate the current parts (.3dm + .stl)
make check     # V1 still matches Katie's Rhino file
make archive   # regenerate stl/archive/
```

All dimensions are mm. File names use hyphens (`max1100-card-adapter-v2.3dm`);
Python scripts use underscores so they can import each other.
