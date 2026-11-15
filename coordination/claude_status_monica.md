<!-- Status file for Monica. Drafted with AI assistance (Claude); reviewed by Monica. -->

# Status: Monica (Story, UI/UX, submission)

Last updated: Sat Nov 14, 10:33 PM CT

## Story (current)
City-wide ground motion across Mexico City, with **"the lake that came back"** (new Lake Chalco / Lago de Tláhuac-Xico) as the key landmark. History comes from sources (UNAM 2007: pumping from 1984 → sinking → lake by 1991). Our data shows the ground around it still moving fast (Eduardo's ground-motion map) and a seasonal rhythm at the lake (Diego: HV dry vs. rainy, coherence drop). Stakes: the 2024 Chalco flood (AP). Caracas: suggested as a "what's next" slide only.

## Done
- **T-05** Organizer questions sent in Discord. No answers yet.
- **T-06** Radar explainer in `content/radar_explainer.md` (PR on `monica/radar-explainer-2`). Waiting on Eduardo's review + NASA "What is SAR" memo row.
- **T-25** Data exploration with Diego. Lake located and matched on map. Old 2025→2026 brightening claim dropped (mixed releases).
- **Sources** 8 rows sent to Eduardo on Slack.
- **Landmark coordinates** sent to Elias (all inside frame).

## In progress
- **T-19** Landmark cards for all 7 (lake, Tláhuac, Nezahualcóyotl, airport, Centro Histórico, Ángel, Chalco) in `content/landmarks/mexico_city.json`, draft **PR #21**. Numbers are "about X cm" placeholders until Elias's T-34 output. Context/personal paragraphs parked in `content/landmarks/README.md` (no contract field yet).
- **T-18** Tour content: 6 steps being updated in `content/story/mexico_city.json` for the city-wide story. Tour code committed on `monica/intro-tour` (draft PR #21). Map movement needs T-09.
- **T-17** Name: leaning **Project Lago**. Tagline still open (top option: "Where the ground sank, the water returned.").

## Next
- Swap in T-34 numbers and ranks when ready
- Commit cards + tour content by ~12:30 AM (before the 1 AM go/no-go)
- Sun morning: **T-50** deck draft (moved from 11:30 PM), **T-23** explainer cards + provisional badge, **T-51** project page text (due 9:30 AM)

## Blocked / waiting on
- **Eduardo:** memo rows for `unam-2007-chalco`, `iahs-2020`, `ap-2024-chalco` (+ NASA "What is SAR"); T-06 review; T-09 map merge
- **Elias:** T-34 numbers/ranks per landmark; add all 7 card source ids to the manifest source list; a `context` field in the landmark contract
- **Organizers:** T-05 answers (pitch length affects the talk script)
