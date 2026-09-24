# Cooling

All mm. Names follow [Terminology](../README.md#terminology). See also
[dimensions](dimensions.md) and [the chassis](rackchoice-4u.md). The project
log and host notes are in SCNVault: `Projects/Max 1100 Notes/` for the single
card, `Projects/QuadBox/` for the four-card appliance.

## Problem

The Max 1100 is passive and built for a server's front-to-back fan wall. It
needs to be ducted to ordinary fans, first as a single card in Salmon (LANCOOL
216 tower), then as four cards in a 4U chassis.

## Thermal facts

From datasheet 817799.

- 300 W. 12V-2x6 power connector.
- GPU and HBM Tj max 105 °C. Card shuts down at 125 °C.
- Required airflow (Figure 6-3): `LFM = 0.014x³ − 0.6694x² + 13.324x + 150.78`,
  where x is the approach air temperature in °C. About 285 LFM at 25 °C and
  400 LFM at 35 °C.
- Figure 6-4, the airflow impedance curve, **hasn't been read yet**. It
  settles the fan choice.
- The datasheet doesn't dimension the heatsink, fin opening or tail bay, and
  there's no separate thermal design guide for this card.

## Design

- **Push.** The fan is at the tail end. Air goes through the fins and out the
  I/O end, which matches both a server's airflow and the tower's own
  front-to-back flow.
- **Card adapter** (`cad/card_adapter.py`, V4):
  - The tube goes 16 into the bay.
  - The flange sits on the shroud end plane.
  - The extension bracket's screws go through the bracket holes into the
    card, so the bracket clamps the adapter on.
  - The power notch clears the 12V-2x6, outside the tube.
  - Bore 73 × 19.
  - The scoop: the PCB-side wall carries on 10 past the tube's end, angled 5
    toward the PCB side. It widens the air stream onto the fins on that side
    and cuts the air leaking back out through the power notch. It goes in by
    hooking it over the power plug and sliding it home, and stops 4 short of
    the top-edge end to clear the header pins there.
- **The same adapter serves 1 or 4 cards.** It is always its own piece,
  bolted to the card by the extension bracket. Only the fan side changes:
  - Salmon gets a flare from the adapter to one fan.
  - The quad gets a plenum feeding four adapters, joined by a slip joint.
  - Neither is designed yet.
- **No 90° 12VHPWR adapter.**

## Airflow

- At 285 LFM through the ~1390 mm² bore, the card needs only about 4 CFM.
  Volume isn't the problem; **static pressure** through 267 of dense fins is.
- **But that 4 CFM may be 2.75× too low.** It assumes the datasheet's LFM is
  referenced to our bore area. Approach-velocity figures are normally
  referenced to the card's slot cross-section. That was taken as
  34.35 × 111.15 = 3818 mm², giving **~12 CFM per card, ~47 CFM for the
  quad**. The card measured 38.64 on 2026-09-23
  ([dimensions](dimensions.md#thickness-3864-not-3435)), so the area is
  really 4295 mm² and scenario B is about **12 % higher, ~53 CFM**. The
  static estimates below still use 47 and have not been redone; the
  correction pushes every one of them the same way and changes no ranking. It changes
  how much fan the quad needs: at 17 CFM total a front stage plus two panel
  fans is heavily over-fanned and every fan runs near shutoff, where they are
  stall-noisy for no benefit; at 47 CFM it's about right. The Figure 6-4
  impedance curve's x-axis should settle which area the LFM refers to.
- **Quiet is the binding constraint**, because these machines live in a
  closet. Fan size is still open. A bigger fan turns slower at the same flow.
- A quiet 120 or 140 makes about 2 mmH₂O, and full 300 W likely needs several
  times that. **Plan on fans in series** — see [Fans](#fans) for why series
  and not more fans side by side.
## Fans

### Pressure scales with rpm², so the model matters

Two knobs, and they do different things:

- **Width (parallel) buys flow**, which is usually the resource in surplus.
- **Depth (series) buys pressure**, which is the scarce one. Pressure adds.

**But width only stops helping once you're already far left on the curve** —
that qualifier matters and an earlier version of this note left it off. Going
2 × 140 across → 3 across moved the estimate from ~4.2 to ~4.4 mmH₂O, because
at 21 % of free air those fans were already on the flat part. One 120 at
scenario B is at 61 % of free air, on the *steep* part, and there a second fan
across is worth a lot. Check where on its curve a fan actually sits before
assuming width is wasted.

And because **pressure ∝ rpm² while flow ∝ rpm**, you can't trade width for
quiet: slow a wide array down and static collapses quadratically. The quiet
way to get static is *series at reduced rpm* — three fans at 1500 rpm against
one at 2500 makes about the same pressure and is roughly **6 dB quieter**
(−11 dB per fan from the rpm ratio, +4.8 dB for having three).

### 120 or 140: the chassis settles it

**A 140 fan does not mount on the RackChoice front plate.** Its upper screw
holes land 9.5 inside the power button cutout — see
[dimensions](dimensions.md#rackchoice-4u-chassis). Not tight; it doesn't fit.
That takes the 140 out of the quad duct regardless of its aerodynamics, and
the P14 Pros bought on 2026-09-22 go to Salmon, which is the first target and
has room for them.

Manufacturer figures, both PWM with PST:

| | P12 Pro PST | P14 Pro PST |
|---|---|---|
| Part # | ACFAN00307A | ACFAN00319A |
| Static | **6.9 mmH₂O** | 5.2 |
| Free air | 77 CFM | 110 |
| Range | 600–3000 rpm | 400–2500 |
| Thickness | 25 | 27 |

The 120 makes **33 % more static** and moves 30 % less air — the usual trade,
and pressure is the scarce resource here. Three in series:

| | 120 | 140 |
|---|---|---|
| Scenario A, 17 CFM | **~16.2 mmH₂O** | ~13.2 |
| Scenario B, 47 CFM | ~7.7 | ~8.6 |

So the 120 wins scenario A outright and loses B by ~10 %. A scaling-law
estimate had put the P12 Pro at ~5.5 mmH₂O; the two fans aren't geometrically
similar, so that ran 20 % low. Use the published figures, not the scaling law.

### Which Arctic P14

Same P-series aerodynamics across the line; what changes is the rpm ceiling,
the control type and the bearing. The rpm ceiling is the one that bites, via
that rpm² law:

| | P14 | P14 Pro PST | P14 Pro PST CO |
|---|---|---|---|
| Part # | — | ACFAN00319A (5-pack) | ACFAN00316A |
| Max rpm | 1700 | 2500 | 2500 |
| Static, max | ~2.4 mmH₂O | 5.2 | 5.2 |
| Free air | ~75 CFM | 110 | 110 |
| Control | 3-pin DC | PWM, 400–2500, stops below 5 % | PWM, same |
| Bearing | FDB | FDB | Dual ball |

**The plain P14 is not usable here.** (1700/2500)² = 0.46, so it makes
~2.4 mmH₂O — less than half. Worked through option C below, three in series:
~5.6 mmH₂O at scenario A and **~2.4 at scenario B**, against an estimate that
300 W needs several times 2. Its 3-pin DC control also gives roughly 2:1 of
usable range against the Pro's 6:1, and the test method needs fan speed driven
from GPU temperature. A 1700 ceiling also leaves nothing in reserve when a
card hits 95 °C.

**PST is worth having for a series stack.** Series stages must pass identical
flow or one becomes a restriction, so they need a common PWM signal. PST
daisy-chains them off one header and they track exactly — the wiring problem
solved by the connector.

**CO vs not is a trade, not an upgrade.** Dual ball tolerates heat better,
which matters for 24/7 in a warm closet; FDB is quieter, and quiet is the
binding constraint. Not worth holding out for: if FDB life proves short it's a
swap, not a redesign.

### Buying

- **P14 Pro PST 5-pack, ACFAN00319A**, ~$80 at Memory Express (2026-09-22),
  ~$16/fan. Stock was thin — one pack online, nothing in the Lower Mainland
  stores.
- Five doesn't cover everything at once. Option C wants 3 duct + 1 CPU + 1
  spare; option B wants 4 + 1 and no spare; and **Salmon is the first target**
  and wants two for the series pair. Expect to split a pack and buy a second
  when the quad gets real.
- **Salmon length budget:** 392 GPU clearance − 266.7 card = 125 behind the
  card. The extension bracket takes 45 of it.

## Quad

Four cards in the RackChoice 4U ([rackchoice-4u](rackchoice-4u.md)), board
slots 1, 3, 5, 7, standing upright, tails facing the case front, the column
against one side wall. Worked through 2026-09-22.

**Status: brainstorming.** Nothing here is decided and nothing here is
retired. This is a record of options and the reasoning behind them, written
down so ideas don't get lost — not a decision log.

The one thing the user has said out loud is that the **card adapter** is its
own piece, bolted to each card by the extension bracket, with a **plenum**
beyond it (2026-09-22). Even that gets revisited if hardware says otherwise.

Everything else — fan sizes, counts, layout, how the plenum splits — is an
option on the table. Where a number looks firm, it's firm *given that option*.
Options that are currently behind are kept below **with the reason they're
behind**, so they can be picked back up when something hits a dead end.
Nothing gets decided until we've played with real hardware in the case.

### Ground rules that survive most changes

- The four adapters are parallel branches: flow adds and pressure doesn't. The
  quad needs **the same static pressure as one card, at four times the flow**.
  That means more of the same fan, not a stronger one.
- **The risk is uneven distribution.** The plenum's cross-section needs to be
  several times the total bore area (4 × 1387 = 5548 mm²), or the card
  nearest the fans takes the air.

### Architecture

Two stages, separate pieces:

1. **Card adapter**, one per card, bolted to the card by the extension
   bracket's own screws. The same part for Salmon and the quad.
2. **Plenum** beyond it — possibly itself two pieces — joined to each adapter
   by a slip joint.

**The slip joint is the tolerance joint, and that is the main reason the
plenum can't be one piece with the adapters.** Slot pitch is nominally 40.64,
but across four slots on a real board in a real case the four flange faces
won't be coplanar or evenly spaced; expect ±1 to 2 of accumulated error. Each
adapter gets screwed down wherever its card happens to sit, and the plenum
then floats onto four stubs with a few mm of axial travel and about 1 of
lateral float, with foam tape taking up the rest. Nothing has to be accurate.

Two more reasons for the split: the bracket screws go in axially right past
the bore wall (T8, hole centres 4 from the tube's outer face, ~2.3 clear at
the hole edge), so nothing can be in the way while an adapter is fitted; and
pulling one card shouldn't mean removing the plenum.

### The slip joint

Common to every fan option below.

- **Male on the adapter, female on the plenum.** A plenum tube plugging *into*
  the bore would have to be smaller than 73 × 19 and would choke the tightest
  section in the whole path. Male-on-the-adapter keeps the bore 73 × 19 end to
  end with no step.
- **Three-sided stub**, skipping the finger-side face. That leaves the T8 a
  clear shot at both bracket holes and clears the extension bracket's plate,
  which lies on top of the flange at that end. The socket seals on three faces
  and lands on the flange face at the fourth.
- A +Z stub breaks the current flange-down print orientation, because material
  would sit on both sides of the flange. Untested options: print on its side
  (axis horizontal, the bore's upper face bridges 19, no supports); stub-down
  with a 45° flare out to the flange (supportless and good for airflow, but
  adds up to 14 of height); or make the stub a separate printed collar. Test
  print before committing — it also changes layer orientation at the
  bracket-hole bosses, which the screws clamp through.

### Column geometry

Slot pitch 40.64, measured from the slot-side case wall with card 1 against it.
Derived from `card_adapter.py` V4, not measured in a case.

| | Card 1 | Card 2 | Card 3 | Card 4 |
|---|---|---|---|---|
| Flange, 38 wide | 0–38 | 40.6–78.6 | 81.3–119.3 | 121.9–159.9 |
| Bore, 19 wide | 15.5–34.5 | 56.1–75.1 | 96.8–115.8 | 137.4–156.4 |
| Bore centre | 25 | 65.6 | 106.3 | 146.9 |

- Flange column 160 wide. Bore band 15.5 to 156.4, centred at 86.
- **2.64 between adjacent flanges** — but the flange only exists at Z = 0 to 2.
  Past it the gap between adjacent *bores* is **21.6**, so four plenum tubes
  with 1.5 walls still have 18.6 of air between them. Per-card tubes are not
  the problem.
- What *is* in that 21.6 is each card's **extension bracket plate**, running
  Z = 0 to +45 in its card's plane. So either the plenum tubes stay short
  stubs onto the flange face, or the web between them needs a slot per card.

### How the fans feed it — the options

Three shapes are on the table. They share everything above (adapters, slip
joint, column geometry) and differ only in what sits between the front of the
case and the plenum.

| | Fans | Front width used | Est. static, scenario B | Biggest printed part |
|---|---|---|---|---|
| **E** — 1 across × 3–4 deep | 3–4×120 | 120 | ~7.7 / ~10.2 | transition, 121 wide |
| **A** — fan panel + collar | 2×120 panel, 2×140 front | 280 | ~8.4 | fan panel, 240 wide |
| **B** — 2 across × 2 deep | 4×140, all in the duct | 280 | ~8.4 | transition, 280 wide |
| **C** — 1 across × 3 deep | 3×140, all in the duct | 140 | ~8.6 | transition, 141 wide |
| **F** — 2 across × 2–3 deep | 4–6×120 | 240 | ~8.0 / ~11.9 | transition, 240 wide |
| **G** — tail box | E's stack, in a box | 120–240 | ~8.6 (no transition loss) | tail wall, ~170 wide |

**G is a different shape of thing and not a competitor to the others.** It
replaces the plumbing — adapters, slip joint, transition, collar — with one
box, and E's fan stack sits inside it unchanged. Read the fan rows as the
question of how many fans, and G as the question of what holds them.

**Currently leaning E** (2026-09-23) for the fan stack. The chassis decided most of it: a 140
doesn't mount on the front plate, which takes B and C out on hardware rather
than on aerodynamics, and A used 140s for its front stage. F is the fallback
if E turns out short on pressure, but it's side-by-side and a 240-wide part,
which the user would rather avoid — a fourth fan in series on E is the
cheaper way to the same place. Still a lean, not a decision.

All four estimates assume the **P14 Pro** at 2500 rpm. Width buys flow, depth
buys pressure, and pressure goes as rpm² — see [Fans](#fans), which is why
three options out of four stack in series rather than spreading out.

### Option G — the tail box

Proposed 2026-09-23. One box from the case front wall back to the four tail
ends — the 165 from the grill to the flange faces — bolted to the six floor
standoffs, to the top rail and to the front wall, with a lid. The fans mount
at the front of it. **It seals on the card column instead of on four separate
adapters**, so the card adapter, the plenum tubes and the slip joint all come
out.

**The one hardware result so far went its way.** Comb V1 (`cad/comb.py`), a
rigid bar with three teeth on the 40.64 pitch, fitted the four installed cards
on 2026-09-23 — see [dimensions](dimensions.md#quad-column). A single rigid
part spans the column, which is what the whole idea rests on.

#### What it deletes

- **The slip joint**, and with it the hardest problem in the quad: four
  joints each absorbing slot-to-slot error. One compliant perimeter replaces
  four tolerance joints. (The split between adapter and plenum still has two
  other justifications — axial screw access and pulling one card without
  disturbing the rest — so this doesn't retire the adapter architecture, it
  removes its main argument.)
- **The transition.** The box *is* the plenum, so there's no 3D contraction to
  design, print or seal, and no ~121 × 120 × 75 part.
- **The collar and the front stage.** A box bolted to the front wall breathes
  filtered room air by construction. That was worth more than a fan stage —
  see [the front stage](#front-stage-as-option-a-uses-it) for why — and here
  it costs nothing.
- **The slant.** The fan centre is fixed at 77.9 and the bore centre is 52–70;
  a duct had to slant between them. A box just contains both.
- **The power notch problem.** In the adapter, the notch is an open cutout
  that lets air out of the bay before it reaches the fins
  ([dimensions](dimensions.md#power), parked, never measured). Inside the box
  it opens into the plenum, not the room, so there's no pressure across it and
  nothing to leak.

#### Inlet area decouples from fan area

A duct bolted to one grill position inherits ~1.2 mmH₂O of inlet loss. A box
whose front face spans two positions with a fan on one drops that to ~0.30 —
**~0.9 mmH₂O recovered for nothing**, more than a fourth fan in series is
worth per stage. A box can breathe through more grill than its fans cover; a
duct can't.

The counter-pressure is option D's surviving conclusion: **at least one front
position stays with the rest of the machine.** With three positions, a box
spanning two leaves one for the CPU, PSU and drives. That's the trade to keep
an eye on, and it argues for a box no wider than it needs to be.

#### The comb, and what the teeth do

Four jobs in one part: seal the gap between cards, locate each card sideways,
carry the column's 5.2 kg, and replace the hanging card-guide rail ([rackchoice-4u](rackchoice-4u.md#tail-support)).
The [leak arithmetic](dimensions.md#quad-column) is why it's not optional —
the gaps are a nearly free bypass straight into the case, so unsealed they
take the air whatever they measure.

- **Teeth are 2.0**, which went into all three gaps as printed. Confirmed
  over the last 25 before the tail end plane — the region a tail wall seals
  in. Deeper than ~45 along the card, past the extension bracket plate, the
  gap may open up.
- **A floor-mounted comb can't reach back past the tail plane.** That space is
  over the motherboard. So the V1 test comb hangs from the top edges instead,
  which also makes it a single constant cross-section to print. Where the
  real one lives depends on the motherboard's front edge, still unmeasured.
- **Support vertically, with clearance, never by clamping.** The box is
  registered to the case floor and the cards to the board; a rigid tie between
  them preloads the PCIe connectors with the whole tolerance chain.
- **Removing the extension brackets** is then on the table: their job is to
  reach a card guide, which the comb does better, and they currently occupy
  the inter-card gap from Z = 0 to +45 where the teeth want to be. Reversible.

#### What it gives up, and what it risks

- **The scoop.** The adapter's only genuine airflow claim is aiming the stream
  at the PCB-side edge of the fin throat. A box pressurises the opening but
  doesn't aim anything. Worth re-testing as a bay insert — a scoop with no
  flange and no bracket holes — *after* the box works, and only once the fin
  throat has been calipered. It may never have been needed.
- **Salmon still needs the card adapter.** Single card, no box, the fan has to
  attach to something. V4 and the flare are untouched by any of this.
- **Perimeter leak scales with box size.** A 1 mm gap around a 200 × 140 box
  perimeter is ~700 mm², 13 % of bore. Keep the box to the column's width, not
  the case's.
- **Print size.** 165 deep × 160–200 wide × ~140 tall is nobody's 220 bed.
  Likely a printed frame with flat panels, or a folded aluminium floor piece
  carrying printed parts, rather than an all-printed box.
- **Fan vibration.** Bolting fans to the sheet front plate will make the panel
  sing, and quiet is the binding constraint. Soft-mount them to the box.

#### What it needs measured

Beyond the whole [not-yet-measured list](dimensions.md#not-yet-measured), four
belong to this option specifically: the **motherboard's front edge** (where
the floor piece can start), **which end of the column** the 12 of case-wall
clearance sits at, the **standoff thread and positions**, and **which grill
positions** sit in front of the column. Plus one from the photo: the row of modules in sheet-metal
brackets between the front bar and the board is in the box's footprint —
whatever it is, does it stay?

### Option E — one 120 wide, three (or four) deep

**Currently the strongest**, and the one the user prefers (2026-09-23): no
side-by-side, one narrow printed transition, and it's the only fan size that
mounts on the front plate at all.

Depth, from measured chassis numbers ([dimensions](dimensions.md#rackchoice-4u-chassis)):

| | From the grill |
|---|---|
| Three fans (25 each) | 0–75 |
| or four fans | 0–100 |
| Extension bracket tips | 120 |
| Duct | 100–165 (65 with four fans, 90 with three) |
| Flange faces | 165 |

**Four deep fits** inside the clear space before the bracket tips, with 65
left for the transition — a 20° half-angle contraction, comfortable. A 5-pack
covers four plus a spare. That's the lever if the impedance curve turns out
harsh: scenario B goes from ~7.7 at three deep to **~10.2 at four**, before
grill losses. Run three if the curve is benign.

**Geometry.** A 120 frame against the 140.9 bore band means the duct has to
*expand* ~10.5 per side laterally while contracting 120 → 73 vertically, so
it's a 3D transition rather than the 2D squeeze a 140 would have given. At
65–90 of length the lateral half-angle is 7–9°, inside the no-separation rule.
Net area 10,029 → 5,548 = **1.81:1**, gentler than a 140's 2.28:1. The part is
about **121 × 120 × 75**.

The fan's centre is fixed at 77.9 above the case floor by the plate's screw
holes, while the bore centre is an estimated 52–70, so the duct slants down
slightly on its way back. Measuring the bore centre settles how much.

**The grill is the inlet, and it costs.** Loss goes as v², so spreading the
inlet across positions helps fast. At ~55 % open with a sharp-edge coefficient
of ~1.5, scenario B:

| Positions used | Hole velocity | Loss |
|---|---|---|
| 1 | 3.6 m/s | ~1.2 mmH₂O |
| 2 | 1.8 m/s | ~0.30 |
| 3 | 1.2 m/s | ~0.13 |

A fan bolted straight to one position inherits the ~1.2, taking scenario B
from ~7.7 to ~6.5. Worth checking whether the grill can be cut out — that
recovers it without an inlet box and without spending depth.

### Option C — one 140 wide, three deep

**The fan is the same width as the bore band.** Bore band, card 1's near edge
to card 4's far edge, is **140.9**. A 140 fan frame is **140**. Centre it on
the column and the frame lands 0.45 inside each end.

So **there is no lateral transition at all.** The duct squeezes in one plane
only: 140 tall at the fan down to 73 at the bores, 1.9:1 in the card-height
axis, nothing in the pitch axis. A 2D contraction, not a 3D flare — much
easier to print and more efficient. Total area ~127 round (the impeller
aperture, not the 140 frame) down to 5548, so **2.3:1**. Gentle.

The transition comes out about **141 × 140 × 65** — one piece on a 220 bed.
That's the main argument over option B, whose 280-wide transition won't fit
most beds and needs splitting plus a seam to seal.

Vertically it isn't centred: a 140 centred on the bore would want to sit below
the chassis floor, so the fan ends up ~10 high. The duct absorbs it.

**Depth budget** — 170 from flange faces (267) to front wall (437), three fans
is 75:

| | Depth from rear wall |
|---|---|
| Transition duct | 267–332 (65) |
| Fan 3 | 332–357 |
| Settling gap | 357–377 (20) |
| Fan 2 | 377–402 |
| Fan 1 | 402–427 |
| Slack | 10 |

One gap rather than two, prioritising duct length. Face-to-face series fans
work, just slightly less efficiently. Both gaps would leave ~45 of duct, a 22°
half-angle contraction — more abrupt but still acceptable.

**The spacers have to be closed collars.** If the gap between stages is open
to the case, the series effect is lost entirely: stage 1 dumps into the case
and stage 2 ingests case air. So the printed spacer is a continuous
**140 × 140 collar** with a ~127 bore and through-bolts at its corners, not
four corner posts. Trivial print, load-bearing for the whole idea. A 3-stack
with one gap is ~100 deep, so it needs M4 threaded rod or M4×110–130 screws,
not fan screws.

**Mounting: hang it off the front bar** (276–366, lid height). That bar runs
the full length of the duct and solves the cantilever problem. Should clear
vertically (duct top ~140, bar ~170) unless its down-turned flange drops more
than ~30 — still open ([rackchoice-4u](rackchoice-4u.md#open-issues)).

**The card-guide rail wants the same space.** The tail-support plan
hangs an aluminium angle from that same bar at 40.64 pitch to catch the
bracket tips at ~312 — inside the duct. Two things resolve it:

1. **The bracket plates themselves are harmless.** Thin sheet lying in each
   card's plane, parallel to the flow. In a single open duct volume behind a
   windowed back wall they just sit in the airstream, acting as flow
   straighteners if anything. Only per-card internal tubes with webs would
   collide. Another argument for short stubs and a windowed back wall.
2. **Put the rail above the duct.** The bore band tops out around 106; the
   bracket guide holes are at 117–125, so the rail clears by ~11–19. The duct
   covers the bore band only and the top-edge strip stays outside and above —
   consistent with the sealing call below. Both can hang off the same bar on
   shared standoffs.

**Part count:** four card adapters, one transition duct, two fan collars, one
hanger. Nothing over 141 wide.

### Option A — fan panel plus collar

Still on the table. It's behind C mainly on part size (a 240-wide fan panel
plus a separate collar, versus one 141-wide transition) and on mixing fan
sizes in series. But it has the shallowest duct of the three and keeps the
fans off the front bar entirely, so if the bar's flange turns out to foul the
duct, this is where to come back to.

**120 looks right for the panel, 140 looks hard.** In the card-height axis the bore centre is an estimated 52
to 70 above the chassis floor (the spread is where the flange sits in the
card's 111.15 height, compounded with the card height above
the floor, now measured at 127). A 120 resting on the floor centres at 60 — inside that band, so no
riser. A 140 on the floor centres at 70, at the top of the band or past it, and
wants 140 of card height where there is only ~111.

**Two 120s side by side into one shared plenum, not one fan per pair of
cards.** The column can only start at the slot-side wall, so two touching 120s
sit at centres 60 and 180, while the card *pairs* are centred at 45.3 and
126.6 — only 81.3 apart where the frames force 120. Split into two boxes,
fan 1 puts 41 of its face against the divider and fan 2 barely reaches card 3,
which starves. Shared, the imbalance disappears because all four branches draw
on a common static. Shared also means one fan failing costs flow, not two
cards.

- Fan panel 240 × 120, its slot-side edge flush with the column's wall, fans
  on the chassis floor. Aperture 28800 against 5548 of bore — **5.2×**, well
  into "pressure box, not duct".
- Fan 1 (0–120) sits directly over cards 1–3. Only fan 2 overhangs.
- **The offset toward the PSU side costs almost nothing.** The four adapters
  are parallel branches, so what each card gets is set by the static pressure
  at its flange, not by where a fan points. At this flow the fans are far from
  free air and make no coherent jet, and the fin stack dominates the loop hard
  enough to wash out upstream non-uniformity.
- **Taper the PSU-side end** of the plenum inward, from the fan face back
  toward the column, rather than leaving a square corner. That turns fan 2's
  outer 84 back into the box instead of parking a dead recirculation pocket.
- More pressure, if needed, comes from stacking a second 120 behind the first.

#### Front stage, as option A uses it

Two 140s on the case front wall, sealed by a short collar into the face of the
two 120s. The **reasoning here applies to every option** — B and C simply put
the front fans inside the duct instead of feeding a panel through a collar.

**The reason is approach air temperature, not pressure.** The datasheet curve
wants 285 LFM at 25 °C and 400 LFM at 35 °C: ten degrees of preheat costs 40 %
more airflow to hold the same die temperature. An unsealed panel feeds the
cards case air, downstream of a ~1.5 kW PSU and the CPU. A sealed collar feeds
them filtered room air. That's worth more than another fan stage.

Secondary: two 140s is 39200 of fan face against 28800 for two 120s, 36 %
more, so lower rpm for the same flow. Quiet is the binding constraint.

- 280 across into a 240 panel is a **contraction**, the forgiving direction.
  Contractions tolerate being abrupt; expansions don't. A few cm is plenty.
- **Same rotation, same PWM signal** on both stages. Series stages pass
  identical flow, so if their curves drift apart one stage becomes a
  restriction. PST daisy-chaining handles this.
- The ~30 gap is a feature, not a compromise: stage 1's swirl dies before
  stage 2 sees it. Better than bolting fans face to face.
- Leave the remaining ~140 of front width open for CPU, PSU and drives. Don't
  seal the whole front to the duct — the stock 80 mm rear exhausts are
  reportedly loud and shouldn't be leaned on.
- Contingent on the front wall behind the door being open
  ([rackchoice-4u](rackchoice-4u.md#open-issues), issue 5).

#### Depth budget for option A

Card tail at ~267 from the inside of the rear wall, front wall at ~437
([rackchoice-4u](rackchoice-4u.md), scaled from photos, ±10). About 170 to work in.

| | Depth from the rear wall |
|---|---|
| Flange faces | 267 |
| Plenum, ~60 (about ½ a fan diameter, so the hub dead zone recovers) | 267–327 |
| One 120 on the fan panel | 327–352 |
| Collar | 352–382 |
| Two 140s on the front wall | 382–407 |
| Front wall | ~437 |

About 30 spare. A second 120 on the panel takes that to ~5, so within option A
**the front stage and a second panel fan are alternatives, not both**. The
power cables escape through the top-edge strip rather than the plenum's back
wall, so they cost no plenum depth.

### Option B — two 140s across, two deep

Four 140s, all inside the duct, no panel and no collar. Same estimated static
as C (~8.4 vs ~8.1 at scenario B) and it **degrades better**: lose one fan and
you drop a column but keep running, where a 3-stack loses a third of its
pressure *and* the dead fan becomes a restriction.

It's behind C on two things: the 280-wide transition exceeds most print beds
and needs splitting plus a sealed seam, and 280 against a 160 column means
real lateral necking where C has none. If uptime turns out to matter more than
part size, or if scenario B (below) proves real and ~8 mmH₂O isn't enough,
this is the one to come back to — it's also the base for a 2×3 six-fan version
at ~12.6 mmH₂O.

### Option F — two 120s across, two or three deep

Kept as the fallback if E is short on pressure. One 120 at scenario B sits at
61 % of free air, on the steep part of its curve, so a second fan across is
worth much more here than it was for the 140s:

| | Fans | Static, scenario B |
|---|---|---|
| 2 across × 2 deep | 4 | ~8.0 |
| 2 across × 3 deep | 6 | ~11.9 |

Behind E on two counts the user cares about: it's side-by-side, and the
transition goes to 240 wide, past a 220 bed, so it splits into two pieces with
a seam to seal. A fourth fan in series on E reaches ~10.2 with neither
problem. Come back here if four-deep still isn't enough.

### Option D — three 140s across, one deep

Considered 2026-09-22 and currently the weakest of the four, recorded so the
reasoning isn't re-derived:

- **Almost no pressure gain.** 3 across vs 2 across moved the estimate from
  ~4.2 to ~4.4 mmH₂O. Parallel width doesn't buy static, and we're already far
  enough left on the curve to be on its flat part.
- **420 against ~430 inside** is tighter than the arithmetic looks once fan
  flanges, case wall and duct walls are counted.
- **It seals off the case's only intake.** Every front position goes to the
  duct, so CPU, PSU and drives get whatever the two loud 80 mm rear exhausts
  can drag through the seams. The case goes negative-pressure and pulls
  unfiltered air through every gap, bypassing the front filter. On an EPYC
  board with a 158 mm tower cooler that's not a detail.

**At least one front position should stay with the rest of the machine** —
that conclusion survives regardless of which option wins.

### Sealing

The plenum seals onto the four flange faces, over the bore band only. The
**top-edge strip stays outside the plenum**: the 12V-2x6 plugs, their 35 of
straight cable, and the connector columns. The adapter tube's wall already
separates the bore from the power notch, so that costs nothing.

But note that **the power notch itself is an open cutout, not a seal** — there
is a large unsealed gap around the plug. That doesn't leak the plenum (it's
outside it), but it does let air out of the bay before it reaches the fins.
If that turns out to matter, the fix is a collar or closed boss in the *card
adapter*, not in the quad parts. Parked, not solved.

Leak area is the thing most likely to wreck the quad — far more than fan
placement. Four bracket-plate slots plus any escape through the plenum wall
can easily add up to more than 5548 mm².

## Test method

**Stage 0, driver bring-up.**
- Idle is about 50 W. With no forced air that's a 50 to 75 °C rise, which is
  enough to throttle. There's no RMA path, so **don't run the card bare**.
  Any fan pointed into the tail, or a desk fan into the open case, is enough.
- **Get a temperature reading working first**, from either:
  - `xpu-smi`, from the pinned LTS 2523 bundle (1.3.3 dropped Max support), or
  - the `xe` driver's sysfs:
    `/sys/class/drm/card*/device/hwmon/hwmon*/temp1_input`

**Stage 1, with the adapter.**
1. Start at 150 W with one fan. Confirm the adapter seals and the temperature
   responds.
2. Step the power up: 150 → 200 → 250 → 300 W. At each step, record GPU and
   HBM Tj, the fan rpm needed to hold it, and tokens/sec. Keep well clear of
   105 °C.
3. Drive the fan PWM from GPU temperature, never a fixed speed.

**That power curve is the deliverable.** It's what sizes the quad.

## Print settings

PETG, 0.2 mm layers, 4 perimeters, 20 % infill, no supports. Card adapter:
flange down on the bed.

## Open

- [ ] Print card adapter V2. Check that:
  - the 22 tube fits the opening
  - the bracket holes line up with the bracket mounting holes
  - the power notch clears the plug and its latch
  - the flange sits flat on the shroud end plane
- [x] V3 printed and fitted (2026-09-22). It goes in, hooked over the power
      plug. Two fixes, both in V4: bracket holes Ø3.0 → Ø3.4, and the scoop
      stops 4 short of the top-edge end to clear the header pins.
- [ ] Print V4 and confirm both fixes on the card
- [ ] Scoop length (10 or 8) and drop (5), once it's in and the fins can be seen (M2.5 or M3), and whether Ø3.0 holes pass it
- [ ] Read the Figure 6-4 impedance curve — it also settles what area the 285 LFM is referenced to, which sets the quad's fan count
- [ ] Fan size for Salmon: 120 or 140
- [x] P14 Pro PST (ACFAN00319A, 5-pack) ordered 2026-09-22. Now headed for Salmon: a 140 doesn't mount on the quad chassis' front plate
- [ ] Order P12 Pro PST (ACFAN00307A, 5-pack, ~$65) for the quad duct — 4 deep plus a spare
- [ ] Check whether the front grill can be cut out. Worth ~1.2 mmH₂O at scenario B, for free
- [x] Comb V1 printed and fitted (2026-09-23). One rigid part spans the four cards on the 40.64 pitch, and 2.0 teeth enter all three gaps
- [ ] Quad fan layout: options A–G are all live. Leaning E (1 across × 3–4 deep, 120s) for the stack, with G (the tail box) as the shape around it. Figure 6-4 decides three deep vs four
- [x] Card thickness settled at 38.64 by comb V1 (2026-09-23), not the datasheet's 34.35. Gap between cards is 2.0
- [ ] Redo the scenario B flow and the static estimates on 53 CFM rather than 47, now the card's frontal area is known
- [ ] Note which end of the column the 12 of case-wall clearance sits at — card 1's PCB side or card 4's shroud side
- [ ] Measure the motherboard's front edge from the card tail plane. Decides where the tail box's floor piece can bolt and whether the comb can be supported from below
- [ ] Floor and side-wall standoffs: thread size and positions
- [ ] Which front grill positions sit in front of the card column, and how many the tail box can take while leaving one for the rest of the machine
- [ ] Identify the row of modules in sheet-metal brackets between the front bar and the board — it sits in the tail box's footprint
- [ ] Does the front bar's down-turned flange foul the duct? If yes, option A comes back into play
- [ ] Design the Salmon flare
- [ ] Measure the bore centre's height above the chassis floor with a card installed. The 52-to-70 estimate is what decides whether the panel 120s sit on the floor or need a riser
- [ ] Test print the card adapter with a +Z stub, to pick the print orientation
- [ ] Decide whether the power notch gap needs sealing, and if so add a collar to the card adapter
- [ ] Confirm the front wall behind the door is open enough for two 140s
