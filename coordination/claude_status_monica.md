<!-- Status file for Monica. Drafted with AI assistance (Claude); reviewed by Monica. -->

# Status: Monica (Story, UI/UX, submission)

Last updated: Sat Nov 14, 6:40 PM CT
Plan version read: v0.4 (D-13 drops Oct 30, 2025; D-14 organizer answers)

## Done
- **T-05** Organizer questions answered and relayed to Eduardo in person; logged as D-14 (Azure hosting counts, pitch is 4 min plus questions, no edits after 1:30 PM).
- **T-06** Radar explainer drafted in `content/radar_explainer.md`. Waiting on Eduardo's review. Two lines need the NASA "What is SAR" source row.
- **T-25** Data exploration with Diego. New Lake Chalco (Lago de Tláhuac-Xico) and the Bosque de Tláhuac lake are visible in the 2026 composite and matched on Google Maps. Change images (2025 → 2026) show both lakes much brighter in HH and HV, consistent with vegetation spreading across the water; Google Earth historical imagery agrees. **Caveat (D-13):** if these change images used the Oct 30, 2025 scene, they must be redone from Nov 11, 2025 before the finding goes into the story or slides.
- **Sources** 8 new rows sent to Eduardo on Slack (UNAM 2007 Lake Chalco study, IAHS 2020, AP 2024 Chalco flood, NASA "What is SAR", challenge page, Tláhuac sources). AP numbers need confirming on the AP page.
- **GS** Story chosen: Option A (surface change across seasons), "The lake that came back."

## In progress
- **T-17** 6-step story outline drafted. Name and tagline ideas next, then a team vote at dinner.

## Next
- **T-18** Intro screen and guided walkthrough (against sample data)
- **T-19** Landmark text: new Lake Chalco, Santa Cecilia (Tláhuac), Bosque de Tláhuac lake, plus others
- **T-23** Explainer cards and provisional badge
- **T-50** Deck draft (Canva, 7 slides max) by 11:30 PM

## Blocked / waiting on
- Eduardo: T-06 review; add the new source rows to the memo table
- Diego: redo the 2025 → 2026 lake change images from Nov 11, 2025 (D-13), if they used Oct 30
- Diego (optional): dry vs. rainy season comparison from the same release, for the Tláhuac crop

## Roadblocks (append-only; mark resolved, never delete)

### RB-M01  [FYI]  OPEN   Needed by: Sat 11:30 PM (before the T-19 and T-23 copy is final)
What I was trying to do: Write the T-06 radar/HH/HV explainer using only claims listed in the decision memo table.
What happened (exact error or evidence):
(1) Seven claims come from S1 (Earthdata SAR) and S2 (JPL article). Both sources are in the memo table, but the claims themselves are not rows. The list is in the "Claim check" table of `content/explainers/radar_hh_hv.md`.
(2) The Earthdata SAR page never defines HV in words. It defines HH and VH, and mentions only "cross-polarized data like VH or HV".
(3) Earthdata gives L-band as "about 23 cm". PLAN section 1 says our file stores 24.2 cm.
What I already tried: Re-read both pages. Left the HV definition and the wavelength number out of the text.
Impact on the plan (task IDs, timeline, tiers): T-06 ships, but it can only say that HV is "cross-polarized". T-19 and T-23 also need the HV definition and a guide to reading bright and dark areas ("calm water dark, buildings bright"). Neither has a source yet.
Options (2 or 3, with cost in hours):
(a) Eduardo adds the 7 rows to the memo table (0.1 h).
(b) Someone finds the HV definition and the bright/dark guidance in the NISAR Data User Guide and adds rows (0.25 h).
(c) Ship without them (0 h, weaker explainer).
My recommendation: (a) now, and (b) before T-23. I can do the reading for (b) if Eduardo agrees.

## Reviews of other people's roadblocks
<!-- - RB-X01: AGREE / DISAGREE / ALTERNATIVE / NEED MORE INFO. One or two lines. -->

## Local data (so nobody downloads the same file twice)
| file | product | collection | date | track/frame | GB | checksum | derived outputs |
|---|---|---|---|---|---|---|---|
| (none, no NISAR files on this laptop) | | | | | | | |
