Drafted with AI assistance (Claude Code), updated with Codex; see docs/AI_USAGE.md. For the fact-checker.

# Claims used in PROJECT_PAGE.md and DECK_OUTLINE.md, and where each comes from

The claims below use the Valley of Mexico deployment. Paths are relative to the repo root. “Memo” refers to docs/DECISION_MEMO.md. P = project page, D = deck slide, S = pitch script.

## A. Ground-motion numbers (our analysis)

| # | Claim as written | Used in | Source | Fact-check |
|---|---|---|---|---|
| A1 | 27 consecutive NISAR GUNW interferograms over 336 days, Nov 11, 2025 to Oct 13, 2026 (26 pairs span 12 days and one spans 24 days) | P, D5, S5 | app/public/data/mexico_city_valley/manifest.json, sinking frame; memo | Traced to the frame dates and granules. |
| A2 | Provisional annualized LOS rates (cm/yr), positive away from the satellite: Nezahualcóyotl +24.2, Tláhuac +17.9, Benito Juárez International Airport +16.5, Centro Histórico +9.0, Chalco +8.4, Ángel de la Independencia +5.1 | P, D2, S2, landmark cards, tour | content/landmarks/mexico_city.json; app/public/data/mexico_city_valley/landmarks.json | Valley claims check. |
| A3 | 186 pixels masked, max +133.7 cm/yr (likely noise, pending review) | P, D7, S7, map legend | app/public/data/mexico_city_valley/manifest.json, sinking caveats | Valley ingest caveat. |
| A12 | Vertical roughly 1.27 times line of sight if motion is purely vertical (cos 38°) | P, S7 | memo L130; `docs/DECISIONS.md` L25 (D-19); `docs/T35_SIGN_CHECK.md` L42 | TRACES (assumption named both times; no vertical number given) |
| A13 | Horizontal motion at bowl edges breaks the vertical assumption | P | `docs/T35_SIGN_CHECK.md` L44 | TRACES |
| A14 | Positive = away from the satellite (sinking) | P, deck header | `docs/DECISIONS.md` L25 (D-19); `docs/T35_SIGN_CHECK.md` L9; memo L129. **Note:** `provenance.json` L5-6 still says "INFERRED, not confirmed (T-35)"; stale after D-19. | TRACES |
| A15 | Sign: specification JPL D-102272 not public; four checks agree (ISCE3, ARIA-tools, MintPy, our bowls) | P | `docs/T35_SIGN_CHECK.md` L11, L21-26; D-19 (L25) | TRACES |
| A16 | Reference area in the western hills, -99.27 to -99.22 E, 19.33 to 19.38 N | P (x2) | memo L129; `provenance.json` L8-13 | TRACES |
| A19 | Two ground-motion bowls: northeast (airport, Nezahualcóyotl, old Texcoco lakebed) and southeast (Tláhuac, Chalco, Xochimilco lakebed) | P, D5, S5 | app/public/data/mexico_city_valley/manifest.json; GUNW overlay; PR #58 | Valley map. |
| A20 | JPL image puts "Benito Juarez International Airport near the center of the mapped deformation field" | P, S5 | PoC README L16 (quoting the JPL article, memo L103) | TRACES |

## B. NASA/JPL, Earthdata, ASF claims

| # | Claim as written | Used in | Source | Fact-check |
|---|---|---|---|---|
| B1 | JPL: preliminary NISAR data Oct 25, 2025 to Jan 17, 2026 show parts of the region "subsiding by more than half an inch (more than 2 centimeters) per month" | P | memo L103 (JPL's words, not converted) | TRACES |
| B2 | JPL: in the 1990s and 2000s parts of the metropolitan area sank "around 14 inches (35 centimeters) per year" | P, S2 | memo L104 | TRACES |
| B3 | Angel of Independence has had 14 steps added to its base as the land sank | P, S2 | memo L105 | TRACES |
| B4 | Causes: groundwater pumping, weight of urban development, compaction of the ancient lakebed | P, D2 ("urban weight, lakebed compaction"), S2 ("the weight of the city") | memo L106 | TRACES (paraphrases keep the meaning) |
| B5 | NISAR is "a joint mission developed by NASA and the Indian Space Research Organisation (ISRO)" | P, D3, S3, P field 8 | memo L113 | TRACES |
| B6 | JPL "provided the satellite's L-band SAR and antenna reflector" | P, S3 | memo L114 | TRACES |
| B7 | SAR "sends out a pulse of energy" and "records the amount of that energy reflected back..." | P, D3, S3 | memo L110 | TRACES |
| B8 | "night or day, regardless of weather conditions" | P, D3, S3 | memo L111 | TRACES |
| B9 | L-band wavelength about 23 cm | P, D3 headline, S3 | memo L109 | TRACES |
| B10 | NISAR's L-band is "unhindered by clouds or vegetation that impede optical sensors and higher-frequency radars" | P, S3 | memo L112, L118 | TRACES |
| B11 | Double bounce most sensitive to HH; volume scattering (forest canopy) to cross-polarized HV | P | memo L108 | TRACES |
| B12 | PROVISIONAL products are calibrated and validated at a limited set of sites | P | memo L117 | TRACES |
| B13 | NASA/JPL published NISAR sinking over Mexico City in April 2026. The app shows 336 days of GUNW ground motion and 11 months of GCOV surface observations. | P | Memo; app/public/data/mexico_city_valley/manifest.json | Product coverage is taken from the Valley bundle. |

## C. Lake Chalco, IAHS and AP (context)

| # | Claim as written | Used in | Source | Fact-check |
|---|---|---|---|---|
| C1 | Old Lake Chalco covered the plain for several thousand years until the early 20th century (slide: "early 1900s"), when it was drained | P, D6, S6 | memo L119 (UNAM 2007, p. 39) | TRACES |
| C2 | 14 wells have pumped the Chalco plain since 1984; intensive pumping started in the early 1960s. The page does not say pumping "began" in 1984. | P | memo L120 | TRACES |
| C3 | Where clay is thickest (300 m), pumping compacts it; ground sunk by up to about 40 cm per year (2007 study) | P | memo L121 | TRACES |
| C4 | New lake formed in the sinking hollow "como consecuencia del bombeo" (as a consequence of pumping) | P, D6 ("due to pumping"), S6 | memo L122 (p. 39) | FIXED in S6: "a hollow formed as a consequence of pumping" attached the phrase to the hollow; now "in the sinking hollow, as a consequence of pumping". P and D6 traced. |
| C5 | Water first collected in 1988 as five pools of up to about 1 ha; about 100 ha by 1991 | P; D6 ("water collected again from 1988"), S6 ("began collecting again") | memo L122 (pp. 32-33) | FIXED in D6: "returned in 1988" overstated five 1-ha pools as a lake's return; now "water collected again from 1988". |
| C6 | Lake covered a little over 1,000 ha at the time of the study | P, S6 | memo L123 | TRACES |
| C7 | In 2006 the lake surface was 12 m below the original ground level | P | memo L123 | TRACES |
| C8 | Sentinel-1 study: "the highest velocities are located on the eastern sector of the city" | P | memo L126 | TRACES |
| C9 | IAHS 2020 (Fernández-Torres et al.): "the lower income inhabitants share a proportionally greater economic cost due to land subsidence and associated shallow faulting." | P | memo L126 | FIXED: the page said "The same IAHS 2020 study" right after a UNAM 2007 sentence, which read as if UNAM said it; now names the study. |
| C10 | AP, Sep 13, 2024: Chalco "a low-income suburb southeast of Mexico City"; floodwaters in homes "for over a month" | P, D6, S6 | memo L127 | TRACES |
| C11 | "According to Chalco's government, more than 2,000 homes and over 7,000 residents have been affected." | P (full), S6 (7,000 residents) | memo L127 | TRACES |
| C12 | Residents (not AP) cite "a combination of unchecked growth and failing infrastructure" | P | memo L128 | TRACES |
| C13 | Flood given as context only; not linked to the lake, sinking or our data; NISAR data starts in 2025 | P, D6 note, S6 | memo L127 | TRACES |

## D. Data, products and app facts

| # | Claim as written | Used in | Source | Fact-check |
|---|---|---|---|---|
| D1 | GUNW collection `NISAR_L2_GUNW_PROVISIONAL_V1` (CRID P05023) | P field 7 | `provenance.json` L15 | TRACES |
| D2 | GCOV collection `NISAR_L2_GCOV_PROVISIONAL_V1`, CRID P05023 | P field 7 | `docs/SOURCES.md` L6; manifest L432; every GCOV name ends `P05023_..._001` | TRACES |
| D3 | Track 19, frame 11, ascending | P, field 7 | `provenance.json` L16-18; D-01 (`docs/DECISIONS.md` L7) | TRACES |
| D4 | 27 GUNW granule IDs for the Valley layer | P field 7 | app/public/data/mexico_city_valley/manifest.json | Identical to the project page list. |
| D5 | GCOV covers 11 observed months, Nov 2025 to Oct 2026, with April 2026 missing. HH, HV and composite have 11 frames each. | P, D4, S4 | app/public/data/mexico_city_valley/manifest.json | Traced to published GCOV frame dates. |
| D6 | Oct 30, 2025 excluded from every layer for measurement errors we observed ourselves (not on ASF's known-issues page) | P | `docs/DECISIONS.md` L19 (D-13); `provenance.json` L78-81 | TRACES |
| D7 | Dec 5, 2025 and Apr 16, 2026 left out of GCOV frames and water counts (not out of the GUNW chain) | P | `docs/DECISIONS.md` L23 (D-17); `provenance.json` L51, L62 | TRACES |
| D8 | Excluded dates decided after Diego's checks | P field 6 | D-13 (L19, RB-D01); D-17 (L23, lake check) | TRACES |
| D9 | GUNW over Mexico City is HH only; GCOV has HH and HV; no VV | P | memo L54 | TRACES |
| D10 | Two tracks cover the city: 19 (ascending) and 113 (descending); combining them would "help separate" vertical from sideways motion | P (future applications) | memo L51; D-08 (L14) | FIXED: "Separate vertical from sideways motion" claimed more than the sources support; now "Help separate". |
| D11 | One track cannot separate vertical from horizontal motion | P | `docs/DECISIONS.md` L14 (D-08) | TRACES |
| D12 | NISAR repeats every 12 days | P, D3, D7, S3 | memo L52 ("every 12 days with one 24-day step in August") | TRACES |
| D13 | Comparing passes measures movement toward or away from the satellite | P, D3, S3 | `docs/T35_SIGN_CHECK.md` L23; memo L129 | TRACES |
| D14 | App layers: HH, HV, HH/HV color composite | P, D4, S4 | manifest L24, L159, L294 | TRACES |
| D15 | Swipe between two dates by mouse, touch or keyboard; satellite basemap option; map credits | P, D4 | `docs/AI_USAGE.md` L35; `README.md` L11 ("a swipe to compare two dates") | FIXED: "between any two dates" is not stated anywhere; now "between two dates". |
| D16 | Street basemap OpenFreeMap "positron"; satellite EOxCloudless 2024 by EOX, CC BY-NC-SA 4.0 | P field 8 | `app/README.md` L73-74; `app/src/map/layers.ts` L12, L16, L19, L21 | TRACES |
| D17 | GCOV legends display “Provisional NISAR data. Interpret with caution.” The GUNW legend displays the caveat in A3. | P | app/public/data/mexico_city_valley/manifest.json; app/src/components/layers/Legend.tsx | Legend reads layer caveats from the manifest. |
| D18 | App loads static files only; no login; no API needed | P, D4, S4 | `README.md` L12-13 | TRACES |
| D19 | Pipeline reads only the window over HTTPS with Earthdata login (`earthaccess`, `h5py`), so it does not need whole granules | P | `docs/PLAN.md` L174; D-03 (L9); D-15 (L21, G1 passed) | FIXED: "we never download whole granules" is false; the memo (L34) records three whole files (16 GB) downloaded for the first look. |
| D20 | GCOV build: dB, Web Mercator reprojection, small images, manifest with granule names | P | `docs/PLAN.md` L178-183; manifest | TRACES |
| D21 | Azure Static Web Apps + managed Azure Functions typed API; Cloudflare Pages backup | P, D4, S4 | `README.md` L13, L46-47; `docs/AI_USAGE.md` L21, L31; D-05 (L11) | TRACES |
| D22 | Live URLs: https://yellow-desert-02401091e.4.azurestaticapps.net and https://built-to-last-6or.pages.dev | P field 4, D7 footer | `README.md` L46-47 | TRACES |
| D23 | Repo URL https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026, MIT license | P, D7 | `docs/AI_USAGE.md` L20 (PR links); `README.md` L42 (MIT) | TRACES |
| D24 | A new region is one entry in `pipeline/config/regions.json` plus a content file, with no code changes | P, D7, S4, S7 | `docs/PLAN.md` L170 | FIXED: D7 and S7 said "one config entry" and dropped the content file; S4 said "the same pipeline works for other regions" (no other region is shown working). Now D7 "new regions by configuration, no code changes", S7 "one config entry plus a content file", S4 "the pipeline is built to take other regions". P traced. |
| D25 | Libraries and languages | P | `docs/SOURCES.md` L28-29; PoC README L85 (matplotlib) | TRACES |
| D27 | Flood-priority map as a shipped feature | P (What we built, Benefits), S7 | Not shipped (6:45 AM status) | DELETED: the [IF SHIPPED] flood-map bullet on the page and the [IF SHIPPED] sentence in S7. Kept only as "Planned next ... screening aid on PROVISIONAL data, not a forecast", which traces to `docs/PLAN.md` L47, L271 (T-34) and D-16 (L22). |
| D28 | Seven landmark names; New Lake Chalco = Lago de Tláhuac-Xico | P | app/public/data/mexico_city_valley/landmarks.json; content/landmarks/mexico_city.json | Valley landmarks. |
| D29 | Story line, "recognize and measure", landmark, stakes | P, D1, S1, S7 | `docs/DECISIONS.md` L22 (D-16); `docs/PLAN.md` L47 | TRACES |
| D30 | Valley of Mexico is the app default. Ground motion is displayed on an approximately 100 m Web Mercator grid. | P, S4 | app/src/state/store.ts; pipeline/config/regions.json; PR #58 | Valley deployment. |
| D32 | ISRO *NISAR Data Product Format Document* v1.2.1 read for the sign check | P field 8 | `docs/T35_SIGN_CHECK.md` L21 | TRACES |
| D33 | NISAR Data User Guide GUNW page and earthaccess page URLs | P field 7 | `docs/T35_SIGN_CHECK.md` L28; `docs/PLAN.md` L174 | TRACES |
| D34 | Learning resource URLs | P field 8 | `docs/SOURCES.md` L16-25; `docs/challenge/README.md` L79-88 | TRACES |
| D35 | Six-step guided tour, live | P (summary, What it does, What we built) | `content/story/mexico_city.json` (6 steps); `app/src/story/StoryTour.tsx`; PR #35, merged Sun 8:15 AM. Live Azure bundle checked Sun about 9 AM: contains "Project Lago" and "Take the tour" | TRACES |
| D36 | “How to read this map” explainers and a provisional-data badge accompany the map. | P | content/explainers/cards.json; app/src/story/ReadingGuide.tsx; app/src/story/ProvisionalBadge.tsx | Valley tour and explainers use the shared app. |
| D37 | The default Valley of Mexico map includes the GUNW ground-motion layer with annualized line-of-sight rates in cm/yr. | P, D4, D5, S4 | README.md; app/public/data/mexico_city_valley/manifest.json; PR #58 | Valley default configuration and deployed bundle. |
| D38 | The Valley map shows seven landmark cards with the shared copy. | P, D6, S4 | PRs #49 and #61; app/src/components/landmarks/landmarkCards.ts | Cards use the Valley landmarks and shared text. |
| D39 | The New Lake Chalco card gives no ground-motion rate and points to Tláhuac. | P, D6 | app/public/data/mexico_city_valley/landmarks.json | The Tláhuac rate is listed in A2. |

## E. AI use (field 6) and rules

| # | Claim | Used in | Source | Fact-check |
|---|---|---|---|---|
| E1 | Claude Code uses (Eduardo, Zainab), item by item | P field 6 | `docs/AI_USAGE.md` L14-19, L22-23, L33-35, L37 | TRACES (each item checked against a row) |
| E2 | Codex uses (Elias), item by item, including the favicon | P field 6 | `docs/AI_USAGE.md` L20-21, L24-32, L36, L38-44 | TRACES (each item checked against a row) |
| E3 | GitHub Copilot left automated review comments | P field 6, field 8 | `docs/AI_USAGE.md` L20-41 ("Review: Copilot commented") | TRACES. The log's Tool column lists only Claude Code and Codex; Copilot appears as a reviewer, which is how the page describes it. |
| E4 | Claude Code drafted the submission copy. Codex corrected the Valley data claims. | P field 6, deck header | docs/AI_USAGE.md | Both tools are disclosed. |
| E5 | Story and approach are the team's decision; AI used to check what the data supports, find and read sources, and plan and write code | P field 6 | `docs/AI_USAGE.md` L10, L16, L37; D-16 (L22) | TRACES |
| E6 | Header notice on every AI-written file; no AI images or video apart from the favicon; no NASA logos, flags or mission identifiers | P field 6, D header | `docs/AI_USAGE.md` L7-9, L32; `docs/challenge/README.md` L46-48 | TRACES (favicon watermark question left open for the team) |
| E7 | Radar layers, figures and screenshots are renderings of NASA data (with the credited basemaps), not generated imagery | P field 6 | `docs/AI_USAGE.md` L17, L34, L35; `app/README.md` L73-74 | FIXED: "The maps ... are renderings of NASA data" ignored the OpenStreetMap and Sentinel-2 basemaps. |
| E8 | Deck: at most 7 slides; must show team, members, challenge, project image, UX, data use; no one under 18 | D header | `docs/challenge/README.md` L21-25 | TRACES (7 slides; every body 25 words, counted by script) |
| E9 | No character limits listed for the form fields | P notes | `docs/challenge/README.md` L27-36 | TRACES |
| E10 | Pitch is 4 minutes plus questions; rehearse to 3:45 or less | S | D-14 (L20); `docs/PLAN.md` L281 (T-57) | TRACES (slots 0:15 + 0:35 + 0:35 + 0:40 + 0:35 + 0:35 + 0:30 = 3:45) |

## F. Other facts

| # | Claim | Used in | Source | Fact-check |
|---|---|---|---|---|
| F1 | Team name B[U]ILT to Last; NASA Space Apps 2026 Chicago; challenge "Dancing with the SARs" | P, D1, S1 | `docs/PLAN.md` L302; `docs/challenge/README.md` L5; `README.md` L3, L9 | TRACES |
| F2 | Members: Eduardo Aranda (team lead), Elias Ghanayem, Monica Venancio, Diego [last name], Zainab [last name] | P, D1, S1 | First names: `docs/AI_USAGE.md`, `docs/DECISIONS.md`; five names: `docs/PLAN.md` L302. Last names are not in the repo (they come from the task brief). | TRACES (team to confirm the spelling of last names) |
| F4 | "UIUC" (page line 5, pitch slide 1) | P, S1 | Not in any source file | DELETED: no source in the repo. The team can add it back if they want. |
| F5 | "Where one of us has family" (summary); "Our teammate Monica's family is from Santa Cecilia, in Tláhuac" (lake section) | P | Monica's own statement; she consented to it on the page, Sun Nov 15. How close Santa Cecilia is to the lake is **not** claimed (memo L138: source not read) | TRACES (personal, with consent) |
| F6 | Name and tagline: Project Lago, "See the ground beneath your city move." | P field 1, summary | Team decision (T-17), recorded in `coordination/claude_status_monica.md` (#44) | TRACES (not a factual claim) |
| F7 | Next: a Spanish version and a classroom mode | P (Future applications) | Team plan (T-17 outline) | TRACES (a plan, not a claim about the shipped app) |

## G. Wording found during the fact-check

| # | Claim | Used in | Source | Fact-check |
|---|---|---|---|---|
| G1 | Sinking is hard to see from the street "until something breaks or floods" | P (The problem) | None | DELETED: no source. "Slow and hard to see from the street" kept (D-16: "a slow hazard"). |
| G3 | Slide and speaker word counts | D, S | docs/submission/DECK_OUTLINE.md | Recounted after the Valley corrections. |

## Flags for the fact-checker

1. **Favicon.** `docs/AI_USAGE.md` L32 says Codex drafted the favicon (`app/public/favicon.svg`, `.ico`). The rules (`docs/challenge/README.md` L46) say AI-generated images need a visible watermark. The team should decide whether the favicon needs a watermark or a visible note.
2. **Stale sign text.** `provenance.json` L5-6 and PoC README L59 still say the sign is inferred. D-19 settles it. The page follows D-19.
3. **"Works on a phone"** is not claimed as fact anywhere. Slide 4 uses a phone screenshot only if the phone layout was checked at G5.
4. **"Water collected again from 1988"** (slide 6) frames the UNAM fact "water first collected in 1988" (memo L122) as part of the D-16 "lake that came back" story.
5. **Paraphrases of quoted rows:** "urban weight" / "the weight of the city" for "the weight of urban development" (B4); "records the echo" for "records the amount of that energy reflected back" (B7); "due to pumping" for "como consecuencia del bombeo" (C4).

## Claims left out because they have no usable source row

- Chaussard et al. (2021) "rates reach up to 50 cm per year": memo L107 says to read the abstract first; nobody recorded doing so. Listed as a reference only.
- How fast the ground moves at new Lake Chalco: not sampled (memo L139).
- "Water looks dark, buildings look bright": not on the Earthdata page (memo L136).
- The late-June 2026 wetland step and the farm-belt seasonal brightening (memo L43): not in the quote table; the farm-belt pass is unreviewed.
- Diego's lake HV numbers (+1.2 dB): not reviewed (memo L140).
- The UNAM 2007 projections for 2010 and 2015 (memo L124-125): projections, not checked.
- Tláhuac history and borders (memo L138): sources not read.
- The flood-priority map as a live feature: not shipped as of Sun 6:45 AM (D27).
