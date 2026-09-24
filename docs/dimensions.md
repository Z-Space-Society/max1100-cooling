# Max 1100 Dimensions

All mm. Names follow [Terminology](../README.md#terminology). See also
[cooling](cooling.md) and [the chassis](rackchoice-4u.md).

## Card

Intel Data Center GPU Max 1100 datasheet, document 817799.

| | |
|---|---|
| Length | 266.7 (312 with the extension bracket, which reaches 45 past the tail) |
| Height | 111.15 (PCIe full height) |
| Thickness | **38.64** measured (2026-09-23), not the datasheet's 34.35 — see below |
| Mass | 1308 g card, 35 g extension bracket |

### Thickness: 38.64, not 34.35

The datasheet's "34.35, dual slot" is not the physical envelope. **Settled by
comb V1** on 2026-09-23: the comb's spine is 160.56 long, cut as
3 × 40.64 + 38.64, and it sits **flush with both outer faces** of the installed
column — card 1's PCB side at one end, card 4's shroud side at the other. At
34.35 the column would be 156.27 and the comb would have overhung by 4.3,
which is not something you miss. So:

| | |
|---|---|
| Card envelope, PCB side → shroud side | **38.64** = 160.56 − 3 × 40.64 |
| Gap between adjacent cards | **2.0** = 40.64 − 38.64 |

38.64 also sits just inside the PCIe double-width envelope of 39.37, which is
where a 300 W dual-slot card would be expected to land; 34.35 would be unusually
thin.

Two earlier readings pointed the other way and both were weaker than they
looked:

- The tail-end tape stack — shroud cover → PCB 31.75, plus a guessed PCB and
  bracket plate — lands near 34.35. Three rough numbers stacked, and the guess
  was doing the work. The real PCB-side stack past the PCB is ~6.9.
- A 2 shim reading "snug in some, loose in others" was read as possibly
  catching a proud bracket plate. It was just the gap, with the variation you
  get across four cards in real slots.

**One caveat on where it was measured.** The comb's teeth occupy the last 25 of
the card before the tail end plane, so 2.0 is confirmed *there* — which is the
region a tail wall seals in. A tooth running deeper along the card could find
the gap opening up where the extension bracket plate ends. Check before
lengthening a tooth much past 45.

## Tail end

Katie's measurements, with the V2 fit adjustments where noted. Positions are
given from the opening's edges, which the card adapter's tube fills.

| | |
|---|---|
| Opening, finger edge → top edge | 76 |
| Opening, PCB side → shroud side | 22 (V2; Katie's V1 used 20) |
| Fin face, in from the shroud end plane | 37 to 39 |
| Stack, shroud side → PCB side | shroud cover, fins, copper, base plate, PCB, bracket plate |
| Shroud cover (outside) → base plate | 27.8 (tape) |
| Shroud cover → PCB | 31.75 (tape) |

## Bracket mounting holes

The two threaded holes the extension bracket screws into. The card adapter's
bracket holes sit over them.

| | |
|---|---|
| Spacing | 19 center to center, in a line running PCB side → shroud side |
| Screw axis | Along the card's length (screws go in from past the tail) |
| From the opening's finger-side edge | 4, toward the finger edge (V2) |
| From the opening's PCB-side edge | 1 toward the PCB side, and 18 toward the shroud side (V2) |
| Screws | Torx T8. The adapter's holes are Ø3.4; Ø3.0 was too tight to start the screws (V3 fit, 2026-09-22) |

## Power

- 12V-2x6 sits outside the opening, on its PCB side, at the top-edge end.
- The card adapter's power notch clears it: 24 × 14, running from the
  flange's PCB-side edge to the tube. Its top-edge side lines up with the
  bore's inside face.
- The plug goes in axially and the cable exits straight out past the tail.
  Allow about 35 of straight cable before any bend.
- Check the latch can still be reached with the card adapter fitted.
- The notch is an **open cutout, not a seal**: there is a large unsealed gap
  around the plug (V4 on the card, 2026-09-22). It doesn't open into the bore
  — the adapter tube's wall separates them — but it does let air out of the
  bay before it reaches the fins. Not yet measured, and not yet known to
  matter.

## Inside the bay

- A row of header pins runs near the **top-edge end**, 2 to 3 in from that side
  of the opening. Anything reaching deeper than the tube has to stay clear of
  them: the V3 scoop fouled them and had to be cut back by hand (2026-09-22).
  V4 stops the scoop 4 short of the top-edge end.
- The fin face is 37 to 39 in, so there's open bay in front of it.

## Quad column

Four cards in the RackChoice 4U, board slots 1, 3, 5, 7, standing upright,
tails toward the case front. Measured on the installed cards 2026-09-23 (tape
and shim) except where noted. See [cooling](cooling.md#column-geometry) for
the derived bore positions.

| | |
|---|---|
| Slot pitch | 40.64 (PCIe, 2 × 20.32). Exact: the slots set it |
| Column width, card 1's PCB side → card 4's shroud side | **160.56** — 160 by tape, confirmed to the comb's 160.56 (flush both ends) |
| Gap between adjacent cards | **2.0**, over the last 25 before the tail end plane. See [thickness](#thickness-3864-not-3435) |
| Card envelope | 38.64, not the datasheet's 34.35 |
| Card top edge, above the case floor | **127** (tape), PCB side |
| Card finger edge, above the case floor | 15.85 = 127 − the card's 111.15 (derived) |
| Top edge is a step | The shroud side's top edge sits **1 to 2 lower** than the PCB side's. Matters for anything sealing down onto the card tops |
| Flange thickness vs pitch | 38 against 40.64, so **2.64 between adjacent flanges** |
| Gap between adjacent bores | 21.6, past the flange (Z > 2) |
| Extension bracket plate | Occupies that 21.6 from Z = 0 to +45, one per card |

Leak area, for anything that seals the column: three gaps at 2 × 111.15 is
**~670 mm²** against 5548 of total bore. The gap is a nearly free path — a
111-tall channel running the card's full 267 length is worth well under
0.1 mmH₂O against a fin stack worth several — so unsealed it takes the air
even at 670.

**Confirmed on the cards, 2026-09-23.** Comb V1 (`cad/comb.py`), a rigid
printed bar 160.56 long with three 2.0 teeth on the 40.64 pitch, dropped onto
the four installed cards and fitted. Four results:

- **The column is 160.56 and the card is 38.64.** The spine came out flush
  with both outer faces, so the comb is a go/no-go gauge on the column width,
  not just a fit test. See [thickness](#thickness-3864-not-3435).

- **Pitch accumulates to nothing across the column.** Four cards in a real
  board in a real case take a single rigid part, no per-card float needed at
  the top. This was the biggest unknown in the [tail
  box](cooling.md#option-g--the-tail-box) and it went the right way. It also
  softens the argument that the plenum *must* be separate from the adapters —
  that argument still holds on the axial and service grounds, but not on
  lateral tolerance.
- **2.0 is the universal tooth.** All three gaps took it as printed, no
  trimming, so the printed-over-nominal worry didn't bite.
- **The spine seats on the four top edges** at 127.

## RackChoice 4U chassis

Measured on the case, 2026-09-23 (tape). Chassis research and the photo-scaled
estimates are in [rackchoice-4u](rackchoice-4u.md); these are the numbers
taken with the case in hand. The front wall's inner face is the grill plane.

| | |
|---|---|
| Grill → extension bracket tip edge | **120** (tape). Was estimated 125 from photos |
| Grill → flange faces (derived) | 165 = 120 + the bracket's 45 past the tail |
| Lower fan screw hole, above the case floor | 25.4 (1") |
| Bottom of the power buttons, above the upper screw hole | 10 (1 cm) |
| Front grill positions | 3 × 120 side by side, perforated, screw holes top and bottom |
| Threaded standoffs, case floor | ~5 proud. Six of them, the spare motherboard mounting points. Thread and positions not taken |
| Threaded standoffs, slot-side wall | ~5 proud (photo, 2026-09-23). Thread and positions not taken |
| Column datum → case wall | **172** (tape, 2026-09-23) |
| Clearance past the column, derived | **~12** = 172 − 160.56 |

**The column is not against the case wall.** The 172 runs from the same end
the 160 was taken from, out to the case wall, so there is about **12** of
clearance beyond the card column — which is what the tail wall and the box's
side panel have to close. Which end of the column that 12 sits at (card 1's
PCB side or card 4's shroud side) isn't written down; it decides which side of
the box seals against a card face and which against sheet metal.

Derived from those, above the case floor:

| | |
|---|---|
| 120 fan upper screw hole (105 spacing) | 130.4 |
| Bottom of the power buttons | 140.4 |
| 120 fan body | 17.9 to 137.9, centre 77.9 |
| 140 fan upper screw hole (124.5 spacing) | 149.9 — **9.5 into the power buttons** |

**A 140 fan does not mount on the front plate.** Its upper screws fall inside
the power button cutout. The 120 clears with 10 to spare.

## Not yet measured

| | |
|---|---|
| Fin throat, width × height | Estimated from photos: 15–20 × ~68 |
| Fin count / fin pitch | |
| Tallest header above the PCB | |
| **Motherboard front edge, from the card tail plane** | An EEB board is 330 deep, which would put it ~63 past the tails — so the first ~63 in front of the tails is over the board, not free floor. Decides where the tail box's floor piece can bolt down and whether a comb can be supported from below |
| Which end of the column the 12 of case-wall clearance is at | See the 172 above |
| Gap between cards past the extension bracket plate | 2.0 is confirmed over the last 25 only. Deeper than ~45 along the card it may open up |
| Floor and side-wall standoffs | Thread size, and positions from the card tail plane and the slot-side wall |
| Bore centre above the chassis floor, card installed | Estimated 52–70. Now one measurement away: the finger edge is 15.85 above the floor, so only the bore centre above the finger edge is missing. The front fan's centre is fixed at 77.9, so this sets how far a duct has to slant |
| Front grill open fraction | Assumed 55 % for the inlet-loss estimates. Worth checking, and whether the grill can be cut out — it's worth ~1.2 mmH₂O at scenario B |
| Power notch gap around the plug | Visibly large (photo, 2026-09-22); never calipered |

## Other

- The bay also has debug and management headers: CNSPI1, CNAMC1, SWAMC1.
- The black strip along the top edge may be a removable bridge connector cover.
- The extension bracket's inner hole is riveted.
