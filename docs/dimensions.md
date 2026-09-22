# Max 1100 Dimensions

All mm. Names follow [Terminology](../README.md#terminology). See also
[cooling](cooling.md).

## Card

Intel Data Center GPU Max 1100 datasheet, document 817799.

| | |
|---|---|
| Length | 266.7 (312 with the extension bracket, which reaches 45 past the tail) |
| Height | 111.15 (PCIe full height) |
| Thickness | 34.35 (dual slot) |
| Mass | 1308 g card, 35 g extension bracket |

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

## Inside the bay

- A row of header pins runs near the **top-edge end**, 2 to 3 in from that side
  of the opening. Anything reaching deeper than the tube has to stay clear of
  them: the V3 scoop fouled them and had to be cut back by hand (2026-09-22).
  V4 stops the scoop 4 short of the top-edge end.
- The fin face is 37 to 39 in, so there's open bay in front of it.

## Not yet measured

| | |
|---|---|
| Fin throat, width × height | Estimated from photos: 15–20 × ~68 |
| Fin count / fin pitch | |
| Tallest header above the PCB | |

## Other

- The bay also has debug and management headers: CNSPI1, CNAMC1, SWAMC1.
- The black strip along the top edge may be a removable bridge connector cover.
- The extension bracket's inner hole is riveted.
