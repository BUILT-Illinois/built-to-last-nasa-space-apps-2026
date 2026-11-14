# Status: Monica        Updated: Sat 3:30 PM CT        Branch: monica/radar-explainer
Plan version read: Sat 3:10 PM | Plan v0.2 approved by Eduardo and in force.

## Now / Next / Done
- Now:  T-05, asking the organizers in person. Questions are in `docs/submission/ORGANIZER_QUESTIONS.md` on my branch. Late: it was due at 3:00 PM. Answers go to Eduardo by about 3:45 PM.
- Next: T-25 with Diego (looking for the story), then T-17 after GS, then T-18 against the sample data.
- Done: T-06 draft in `content/explainers/radar_hh_hv.md` on my branch. It is 151 words and every claim is tagged S1 or S2. Waiting for Eduardo's review.

## Roadblocks (append-only; mark resolved, never delete)
<!-- Copy this block for each roadblock. IDs are RB-<initial><nn>, for example RB-M01.
### RB-M01  [BLOCKER | DEGRADED | FYI]  OPEN   Needed by: Sat 6:00 PM
What I was trying to do:
What happened (exact error or evidence):
What I already tried:
Impact on the plan (task IDs, timeline, tiers):
Options (2 or 3, with cost in hours):
My recommendation:
-->

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
