# RackChoice 4U chassis

The case the quad goes in. All mm. Names follow
[Terminology](../README.md#terminology). See also [dimensions](dimensions.md)
and [cooling](cooling.md).

Moved here from SCNVault on 2026-09-23, because the chassis and the duct
design stopped being separable — the tail box is shaped by the case, not by
the card. The vault keeps a pointer at
`Projects/QuadBox/RackChoice 4U Fit`. **The case is a QuadBox part**, not a
single-card one; it sat under `Max 1100 Notes` until the move. Host, driver
and project-log notes stay in the vault.

**Numbers taken with the case in hand live in
[dimensions](dimensions.md#rackchoice-4u-chassis).** What's here is the
research, the fit reasoning and what's still unmeasured. Anything marked
*(photo)* is scaled from the listing's top-down photo against the 438 width,
good to about ±10, and should be replaced as it gets measured.

## The case

- Amazon.ca ASIN B0BXJ5HF2W, $333 CAD, sold by CICHENG INC, ships from Amazon
- External 438 W × 178 H × 465 D (483 with rack ears). 6.94 kg. Zinc-coated steel
- EATX / ATX / mATX / Mini-ITX
- 8 full-height expansion slots, perforated covers
- 1 ATX PSU bay, PSU stands on edge (about 86 wide) at the opposite side from
  the slots
- 2 × 80 mm rear exhaust fans included (reviews: loud)
- **No front fans or fan wall.** Front is a honeycomb door with a filter
  behind it; the front plate behind it carries 3 × 120 positions
- Two screwed-in crossbars at lid height: a rear bar with six round holes, and
  a plain front bar (the "elevated 360 radiator" mount, unconfirmed)
- Threaded standoffs about 5 proud on the case floor and on the slot-side wall
- 2 × 3.5 internal. No sliding rails; use a shelf
- Reviewer fit a 158 mm Noctua NH-U12S, just touching the lid
- No manual

## What fits (assumes ROMED8-2T, Node 1)

- **Slots:** 4 dual-slot cards in board slots 1, 3, 5, 7. Slot 7's card needs
  the 8th case slot, which this case has
- **Width:** ATX board 305 + PSU on edge ~86 = ~391 against ~430 inside
- **Orientation:** cards stand upright, tails facing the case front, fins I/O
  end to tail end
- **Depth:** inside depth ~437 *(photo)*. Card tails at ~267 from the rear
  wall, leaving ~150 to 170 in front of them
- **Height:** inside ~170. Card top edge **127** above the floor (measured)
- **Exhaust:** cards exhaust through the perforated slot covers; the 80 mm
  pair covers the CPU zone

## Chassis layout *(photo)*

| Feature | From inside of rear wall |
|---|---|
| Rear bar (six holes) | 110 to 195 |
| Card tail | ~267 |
| Front bar | 276 to 366, centre ~321 |
| Extension bracket tip (card + 45) | ~312 |
| Front wall | ~437 |

The card column sits against the slot-side wall, roughly 0 to 160 in.

**The motherboard's front edge is the one that matters and isn't measured.**
An EEB board is 330 deep, so on this layout it would reach ~63 past the card
tails — meaning the first ~63 in front of the tails is over the board, not
over free floor, and only beyond that can anything bolt down. That sets where
the tail box's floor piece can start and whether a comb can be supported from
below. See [cooling](cooling.md#option-g--the-tail-box).

## Tail support

The tails must be supported. Each extension bracket has a screw hole at the
top that locates into a guide.

**The bracket tips land under the front bar** (~312 against a bar spanning 276
to 366), about 10 behind its centreline. No need to relocate it front to back.

**The gap is vertical.** The bar is at lid height (~170); the bracket hole is
near the card top edge (127). Expect a 40 to 50 drop.

### Option 1: hanging card-guide rail

- Aluminium angle, 20×20 or 25×25, running side to side under the front bar
- Hung from the bar on two M4 standoffs or spacers, cut to the measured drop
- **Slotted** mounting holes to take up the ±10 depth uncertainty
- Four holes at **40.64 pitch** (2 × 20.32), one per card
- **Drill in place:** fit the four cards, clamp the rail to the bracket tips,
  mark through, drill. Absorbs slot tolerance

If the bar turns out badly placed: it is screwed at each end, so drill two new
holes per side wall and move it. Still hang from the bar rather than running a
wall-to-wall rail, since the card column sits against one wall and the far end
would float mid-case.

### Option 2: the tail box carries them

Added 2026-09-23. If the quad goes the [tail box](cooling.md#option-g--the-tail-box)
route, the box's comb does this job instead: teeth between the cards locate
them laterally and a cradle under each finger edge takes the weight, with the
box bolted to the floor standoffs and the front wall. No rail, no drilling,
and the extension brackets may come off entirely. Both are live.

Whichever wins, support the cards **vertically and with clearance, not by
clamping**. The box is registered to the case floor and the cards to the
board; a rigid tie between them preloads the PCIe connectors with whatever the
tolerance chain gives.

### Conflict with the duct design

The vault's old `cooling` decision 4 bolted the duct to the two ledge holes
and **replaced** the extension bracket. The card adapter instead uses the
bracket's **own screws** to clamp itself on, so the bracket stays and that
conflict doesn't arise. All of it is still being brainstormed — if the
bracket-replacing approach comes back, this section describes what it costs.

What still applies:

- Each bracket plate runs through the 267 to 312 zone in its card's plane, so
  anything spanning the column needs a slot or cutout per card. It sits in the
  gap between adjacent bores, which is exactly where a plenum would want to
  put material
- With a card adapter per card and a plenum beyond it, the slip joint is what
  absorbs the slot-to-slot tolerance, so the rail's "drill in place" trick and
  the plenum no longer have to agree on anything

## Open issues

1. **No intake fans.** The fan wall or plenum is ours to build
2. **PSU:** one ATX bay. Full load ~1.5 kW; at the 150 W cap ~850 W. Needs
   **four 12V-2x6 leads**, native or 2×8-pin to 12V-2x6. No 90° adapters.
   Count leads before buying. The PSU breathes case air, which is fine because
   the cards exhaust out the rear
3. **Xe Link bridges vs the rear bar.** The rear bar's down-turned flange may
   leave only ~25 above the card tops. Remove the bar if it fouls. Bridges are
   not needed for bring-up
4. **Slot 1 card vs DIMMs and CPU cooler** on the ROMED8-2T. Not confirmed
5. **Front wall behind the door:** open or solid? Drill if solid
6. **Power cables:** 35 straight past each 12V-2x6 before a bend. The tightest
   part of the layout, and it decides how anything spanning the card tops
   installs — the comb slides on from the case front, so it goes on before the
   cables
7. **What the row of modules in sheet-metal brackets between the front bar and
   the board is** (photo, 2026-09-23). Stock fan wall? Drive cages? It sits in
   the tail box's footprint. If it stays, the box doesn't fit as sketched

## Build path

- **Stage 0 (bring-up):** four cards, 150 W cap and watchdog on all four. Two
  P14 Pros on the floor in front of the tails blowing toward the I/O ends,
  cardboard shroud. Enough for driver bring-up and first idle and load numbers
- **Stage 1:** a plenum or tail box across the four tails. Fan layout is in
  [cooling](cooling.md#quad), where options A–G are all live. Note the bore is
  73 × 19, so the old "four spigots, 26 × 76 × 32" sizing needs redoing
  whichever option wins

## Measure on arrival

- [x] Bracket tip distance from the front grill — **120**, 2026-09-23
- [x] Card top edge above the chassis floor — **127** (PCB side), 2026-09-23
- [x] Front plate fan positions and screw heights — 2026-09-23, and they rule
      out a 140
- [ ] **Bore centre above the chassis floor, card installed.** Estimated 52 to
      70. Now one measurement away: the card's finger edge is 15.85 above the
      floor, so all that's left is the bore centre above the finger edge
- [ ] **Motherboard front edge, from the card tail plane.** Decides where the
      tail box's floor can bolt down
- [ ] **Floor and side-wall standoffs**: thread, and positions relative to the
      card tail plane and the slot-side wall
- [ ] Front bar underside height above floor; flange or not
- [ ] Front bar position front to back (checks 276 to 366)
- [ ] Inside depth along the card column
- [ ] Gap under the rear bar, for Xe Link bridges
- [ ] Front wall behind the door: open area, and whether the grill can be cut out

## Sources

- [Amazon.ca listing](https://www.amazon.ca/dp/B0BXJ5HF2W)
- [RackChoice product page](https://rackchoice.net/Liquidcoolingchassis/111.html)
- SCNVault `Projects/QuadBox/` — the appliance this case is for: `hardware`,
  `bom`, `orders-and-inventory` (where the case was ordered), and the pointer
  stub this note left behind
- SCNVault `Projects/Max 1100 Notes/` — the single-card work: project log,
  host and driver notes
