# Cooling

All mm. Names follow [Terminology](../README.md#terminology). See also
[dimensions](dimensions.md). The project log and host notes are in SCNVault:
`Projects/Max 1100 Notes/`.

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
- **Card adapter** (`cad/card_adapter.py`, V2):
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
- **The same adapter serves 1 or 4 cards.** Only the fan side changes:
  - Salmon gets a flare from the adapter to one fan.
  - The quad gets a plenum feeding four adapters.
  - Neither is designed yet.
- **No 90° 12VHPWR adapter.**

## Airflow and fans

- At 285 LFM through the ~1390 mm² bore, the card needs only about 4 CFM.
  Volume isn't the problem; **static pressure** through 267 of dense fins is.
- **Quiet is the binding constraint**, because these machines live in a
  closet. The fan is 120 or 140 (undecided). A bigger fan turns slower at the
  same flow.
- A quiet 120 or 140 makes about 2 mmH₂O, and full 300 W likely needs several
  times that. **Plan on two fans in series** (on the same through-bolts) at
  300 W, which roughly doubles the static pressure.
- **Salmon length budget:** 392 GPU clearance − 266.7 card = 125 behind the
  card. The extension bracket takes 45 of it.
- **Candidate fan** (not bought): Arctic P14 Pro PST CO, ACFAN00316A.
  - 140 mm, 5.2 mmH₂O, 110 CFM.
  - 400–2500 rpm PWM, and stops completely below 5 % PWM.
  - Dual ball bearing, which lasts better running 24/7 in a warm closet.
  - Buy two, so the series pair can be tested.

## Quad

- Card pitch is 40.6, so fans can't sit inline with each card. Instead, a fan
  wall feeds one plenum, and the plenum feeds four adapters.
- The four adapters are parallel branches: flow adds and pressure doesn't. The
  quad needs **the same static pressure as one card, at four times the flow**
  (about 17 CFM at 300 W each). That means more of the same fan, not a
  stronger one.
- **The risk is uneven distribution.** The plenum's cross-section needs to be
  several times the total bore area (4 × 1390 ≈ 5550 mm²), or the card
  nearest the fans takes the air.

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
- [ ] Read the Figure 6-4 impedance curve
- [ ] Fan size: 120 or 140
- [ ] Design the Salmon flare
