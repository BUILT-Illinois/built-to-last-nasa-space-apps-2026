Draft for Monica to build in Canva. Drafted with AI assistance (Claude Code); see docs/AI_USAGE.md.

# Demo deck outline: 7 slides (hard limit: 7, title slide included)

Slide count: **7** (1, 2, 3, 4, 5, 6, 7). Do not add a slide; going over 7 makes the project ineligible for global judging (`docs/challenge/README.md`).

Rules for the deck (from `docs/challenge/README.md` and the memo):

- Must show: team name, member names, the challenge, an image of the project, the user experience, and how NASA and partner data make it possible.
- Body text at most 25 words per slide (counts in parentheses). Headlines and the footer URL line are not counted.
- Every ground-motion number says "line of sight", and the data is PROVISIONAL (CRID P05023). Positive = away from the satellite.
- No NASA logos, flags or mission identifiers. No images of anyone under 18. No AI-generated images.
- Every number is in `docs/submission/CLAIMS.md`.
- Visuals marked **[IF SHIPPED]** depend on features not confirmed live at the last status update (Sun 6:45 AM: ground-motion layer, layer switcher and legend being merged; landmark cards on the map not confirmed; flood-priority map not shipped). If the feature is not live at G5, use the fallback named on the slide.

---

## Slide 1: Title

- **Headline:** [PROJECT NAME]: Mexico City is sinking, and NISAR measured a year of it
- **Body:** B[U]ILT to Last: Eduardo Aranda (lead), Elias Ghanayem, Monica Venancio, Diego [last name], Zainab [last name]. Dancing with the SARs. NASA Space Apps 2026 Chicago. **(25 words** with the placeholders; 23 once the two last names are filled in, if each is one word)
- **Visual:** live site default view

## Slide 2: The hook

- **Headline:** About 2 cm a month along the line of sight
- **Body:** Over one year, Nezahualcóyotl's ground moved about 21.9 cm away from the satellite, line of sight (PROVISIONAL data). JPL: groundwater pumping, urban weight, lakebed compaction. **(25 words)**
- **Visual:** poc/mexico_city_sinking/fig_mexico_city_year_of_sinking.png

## Slide 3: What NISAR is, and why L-band radar

- **Headline:** Why NISAR: L-band radar, about 23 cm wavelength
- **Body:** NISAR (NASA and ISRO) sends radar pulses and records the echo, night or day, regardless of weather. Comparing passes 12 days apart measures ground movement. **(25 words)**
- **Visual:** HH swipe Nov vs Oct (Nov 11, 2025 on one side, Oct 13, 2026 on the other)

## Slide 4: What we built

- **Headline:** Swipe and compare: a live, open-source map
- **Body:** Real NISAR HH and HV radar images, Nov 2025 to Oct 2026. Swipe between dates by mouse or touch. Open source, no login, on Azure. **(25 words)**
- **Visual:** phone view (fallback if the phone layout was not checked at G5: live site default view)

## Slide 5: What the data shows

- **Headline:** Two sinking bowls, about 3.2 million people (PROVISIONAL data)
- **Body:** 27 NISAR interferograms show two bowls, north-east and south-east. About 3.2 million people live where ground moves over 10 cm/yr, line of sight (WorldPop 2020). **(25 words)**
- **Visual:** sinking layer with legend **[IF SHIPPED]** (fallback: poc/mexico_city_sinking/fig_mexico_city_year_of_sinking.png, cropped to the map panel)

## Slide 6: The lake that came back

- **Headline:** The lake that came back: new Lake Chalco
- **Body:** Drained in the early 1900s; water collected again from 1988, due to pumping (UNAM 2007). Chalco, 2024: floodwater stayed in homes over a month (AP). **(25 words)**
- **Visual:** landmark card for new Lake Chalco **[IF SHIPPED]** (fallback: live site default view zoomed on the lake in the HH/HV composite)
- **Note:** keep the lake and the 2024 flood visually separate (two text blocks). The memo says not to tie the flood to the lake, to sinking or to our data.

## Slide 7: Honest limits, and what comes next

- **Headline:** Honest limits, and what comes next
- **Body:** PROVISIONAL data (CRID P05023), line of sight, about 2 cm uncertainty. Next: new regions by configuration, no code changes; each new pass extends the record. **(25 words)**
- **Visual:** live site default view
- **Footer (not counted):** yellow-desert-02401091e.4.azurestaticapps.net · github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026 · B[U]ILT to Last

Body word counts: 25, 25, 25, 25, 25, 25, 25. Slides: 7.

---

## Pitch script (live, 4-minute slot; target 3:45 or less)

Pace assumed: about 2.5 spoken words per second. One speaker per slide, one driver at the laptop for slide 4. Word counts are given so the speakers can check the pace on a timer.

| Slide | Speaker | Time | Running total |
|---|---|---|---|
| 1 | [speaker] | 0:15 | 0:15 |
| 2 | [speaker] | 0:35 | 0:50 |
| 3 | [speaker] | 0:35 | 1:25 |
| 4 | [speaker] + [driver] | 0:40 | 2:05 |
| 5 | [speaker] | 0:35 | 2:40 |
| 6 | [speaker] | 0:35 | 3:15 |
| 7 | [speaker] | 0:30 | 3:45 |

**Total: 3:45** (0:15 of the 4:00 slot left for handover). If the [IF SHIPPED] or family-connection sentences are added, cut the same time from slide 4.

### Slide 1 — [speaker] — 0:15 (running 0:15)

"We're B[U]ILT to Last: Eduardo, Elias, Monica, Diego and Zainab. Our challenge is Dancing with the SARs. Our project: Mexico City is sinking, and NISAR measured a year of it."

### Slide 2 — [speaker] — 0:35 (running 0:50)

"JPL reports that in the 1990s and 2000s, parts of Mexico City were sinking by around 14 inches, 35 centimeters, a year. The Angel of Independence has had 14 steps added to its base as the land sank. In provisional NISAR data from November 2025 to October 2026, the ground at Nezahualcóyotl moved about 21.9 centimeters away from the satellite, along the line of sight: about 2 centimeters a month. JPL names the causes: groundwater pumping, the weight of the city, and the old lakebed compacting."

### Slide 3 — [speaker] — 0:35 (running 1:25)

"NISAR is a joint NASA and ISRO mission, and JPL provided its L-band radar. A radar sends out a pulse of energy and records what bounces back, night or day, regardless of weather. L-band's wavelength is about 23 centimeters, and NISAR's L-band is unhindered by clouds. Every 12 days NISAR passes again. Comparing two passes shows how far the ground moved toward or away from the satellite. We measure motion in HH; HV adds a second view of the surface."

### Slide 4 — [speaker] + [driver] — 0:40 (running 2:05)

[Driver opens the live site.] "This is our live app on Azure. These are real NISAR radar images of the Valley of Mexico, in HH and HV. Drag the swipe to compare November 2025 with October 2026. [IF SHIPPED: Now the ground-motion layer: the legend is centimeters along the line of sight.] [IF SHIPPED: Tap a landmark, and the card keeps what the radar shows apart from what we infer.] No login, open source, and the pipeline is built to take other regions."

### Slide 5 — [speaker] — 0:35 (running 2:40)

"Adding 27 consecutive pairs, almost all 12 days apart, gives a year of motion, and two bowls appear. North-east: the airport, Nezahualcóyotl and the old Texcoco lakebed. South-east: Tláhuac, Chalco and the Xochimilco lakebed. The western hills barely move, and the bowls sit where JPL's April 2026 image puts the sinking. About 338 square kilometers move faster than 10 centimeters a year along the line of sight. About 3.2 million people live there, by WorldPop 2020 counts."

### Slide 6 — [speaker] — 0:35 (running 3:15)

"One landmark is the lake that came back. Lake Chalco was drained in the early 20th century. In 1988, water began collecting again in the sinking hollow, as a consequence of pumping. By the time of a 2007 UNAM study, it covered a little over 1,000 hectares. Separately, in 2024, AP reported floodwater in Chalco homes for over a month, with more than 7,000 residents affected, according to Chalco's government. We don't link that flood to the lake or to our data. [Team member's family connection — only with their consent]"

### Slide 7 — [speaker] — 0:30 (running 3:45)

"Our limits: the data is PROVISIONAL. We measure along the line of sight; if the motion were purely vertical, sinking would be roughly 1.27 times larger. Treat about 2 centimeters as the uncertainty of any one number. What's next: a new region is one config entry plus a content file, and every new pass extends the record. NISAR can help cities recognize and measure slow hazards like this one. Thank you."

### Spoken word counts (for pacing)

Counted without the bracketed [IF SHIPPED], driver and placeholder text. At 2.5 words per second:

| Slide | Words | Spoken time | Slot |
|---|---|---|---|
| 1 | 30 | about 0:12 | 0:15 |
| 2 | 86 | about 0:34 | 0:35 |
| 3 | 80 | about 0:32 | 0:35 |
| 4 | 45 | about 0:18, plus live clicks | 0:40 |
| 5 | 77 | about 0:31 | 0:35 |
| 6 | 82 | about 0:33 | 0:35 |
| 7 | 71 | about 0:28 | 0:30 |

Slide 4 keeps about 22 seconds for the driver's clicks and for the two [IF SHIPPED] sentences (29 words, about 12 seconds), which leaves about 10 seconds of clicks if both are said. The flood-priority map is not shipped, so slide 7 has no [IF SHIPPED] sentence. The family-connection sentence on slide 6 does not fit: if the team adds it, take the time from slide 4.
