<!-- Status file for Monica. Drafted with AI assistance (Claude); reviewed by Monica. -->

# Status: Monica (Story, UI/UX, submission)

Last updated: Sun Nov 15, 8:40 AM CT

**Name and tagline (locked):** Project Lago, "See the ground beneath your city move."

## Story (current)
City-wide ground motion across Mexico City, with **"the lake that came back"** (new Lake Chalco / Lago de Tláhuac-Xico) as the key landmark. History from UNAM 2007: water first pooled in 1988 and became a small lake by 1991, as a consequence of groundwater pumping (not "began in 1984"; see the memo row). Our data: about 16 cm line-of-sight movement at nearby Tláhuac, fastest in the east (Nezahualcóyotl about 22 cm). Stakes: the 2024 Chalco flood (AP), as context only, not tied to sinking. Caracas: a "what's next" slide only.

## Done
- **#35 merged by Eduardo at 8:15 AM, all checks green.** Includes:
  - T-18: intro screen (Project Lago) and the 6-step tour.
  - T-19: card text for 7 landmarks, with a sources list (pipeline merge by #40).
  - T-23: "How to read this map" (HH vs HV, radar shows vs. we infer, provisional data), a provisional badge on every data view, and a 375 px mobile pass.
- **Diego's #41** (control panel, phone bottom sheet) reviewed and approved (`base.css`). Badge-style mismatch noted there for later.
- **T-05** Organizer questions sent in Discord. No answers yet.
- **T-25** Data exploration with Diego. Lake located and matched on the map. Old 2025→2026 brightening claim dropped (mixed releases).
- **Sources** 8 rows sent to Eduardo; memo rows landed in #27.
- **Landmark coordinates** sent to Elias (all inside the frame).

## Next
- **T-51** Project page with Eduardo (#38).
- **T-50** Deck in Canva, final by 10:30 AM.
- **Tour step 5 card size** (bug fix, after 9:00): on desktop the card covers much of the left side of the swipe it asks you to compare.
- **Pitch rehearsal**, as lead.
- **T-06** Radar explainer (PR #16): apply Eduardo's review.

## Blocked / waiting on
- **Held claims** (kept out of visible text per the memo): the lake's own ground-motion number (lake point not sampled), Diego's lake HV +1.2 dB (not reviewed), Santa Cecilia next to San José (source not read), NISAR's 12-day repeat (no quotable row).
- **Elias / Zainab:** a `context` field in the landmark contract, for the paragraphs held in `content/landmarks/README.md`.
- **Organizers:** T-05 answers (pitch length affects the talk script).
