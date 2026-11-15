Drafted with AI assistance (Claude Code); see docs/AI_USAGE.md. For the fact-checker.

# Claims used in PROJECT_PAGE.md and DECK_OUTLINE.md, and where each comes from

All paths are relative to the repo root, as checked out from `origin/main` on Sun Nov 15, about 6:20 AM CT. "Memo" = `docs/DECISION_MEMO.md`; "memo L129" = line 129 of that file, which is a row of the "Numbers we may quote" table (lines 101 to 131). "PoC README" = `poc/mexico_city_sinking/README.md`. Column "Used in": P = PROJECT_PAGE.md, D = DECK_OUTLINE.md (slides), S = DECK_OUTLINE.md (pitch script).

**Fact-check (Sun Nov 15, after the 6:45 AM status).** Each claim was checked on its own against the source files, not against this table. TRACES = matches the source as written. FIXED = the wording was changed so that it matches the source (the change is described). DELETED = removed from the page and deck because nothing supports it. Result (99 rows): 82 TRACES, 14 FIXED, 3 DELETED. The 27 GUNW names (page field 7) were checked by script against `provenance.json` `granules` (identical, same order). The 11 GCOV names were checked by script against the unique names in `app/public/data/mexico_city/manifest.json` (identical; no Oct 30, 2025, Dec 5, 2025 or Apr 16, 2026 date among them).

## A. Ground-motion numbers (our analysis)

| # | Claim as written | Used in | Source | Fact-check |
|---|---|---|---|---|
| A1 | 27 consecutive NISAR interferograms (GUNW): 26 span 12 days, one spans 24 days (Jul 21 to Aug 14, 2026); Nov 11, 2025 to Oct 13, 2026 | P (x3), D5, S5 | `provenance.json` L48-77 (dates; gaps computed by script: 26 × 12 d + 1 × 24 d = 336 d); memo L52 ("one 24-day step in August"); memo L129 | FIXED: the page and pitch said "27 consecutive 12-day" pairs (PoC README L11 says that too), but the dates include one 24-day pair. Slide 5 ("27 NISAR interferograms") already traced. |
| A2 | 336 days (only implied: "over the year") | P | memo L129 ("Nov 11, 2025 to Oct 13, 2026 (336 days)") | TRACES |
| A3 | Nezahualcóyotl about 21.9 cm away from the satellite, line of sight | P, D2, S2 | memo L129; PoC README L20; `landmark_series_los_cm.csv` L3 (21.92) | TRACES |
| A4 | Tláhuac 16.4 cm; airport area 15.3 cm; Centro Histórico 9.2 cm; Chalco 7.6 cm; Angel of Independence 4.3 cm; Iztapalapa 3.3 cm (line of sight) | P (table) | memo L129; PoC README L21-26; CSV last column (16.41, 15.30, 9.22, 7.64, 4.26, 3.30) | TRACES |
| A5 | Per-month values 2.0 / 1.5 / 1.4 / 0.8 / 0.7 / 0.4 / 0.3 cm | P (table) | PoC README L20-26, column "Per month"; recomputed from the CSV over 336 days (1.99, 1.49, 1.39, 0.83, 0.69, 0.39, 0.30) | TRACES |
| A6 | About 2 cm per month at Nezahualcóyotl, line of sight | P, D2 headline, S2 | memo L130; PoC README L20 | FIXED in S2: "About 2 centimeters a month" stood alone without "line of sight"; now joined to the line-of-sight clause. P and D2 traced. |
| A7 | 1% of the valid area moves faster than 24 cm per year (99th percentile), line of sight | P | memo L130; PoC README L31; `provenance.json` L102 (24.23) | TRACES |
| A8 | About 338 km² faster than 10 cm/yr; about 105 km² faster than 20 cm/yr, line of sight | P, S5 | memo L130; PoC README L32; `provenance.json` L103-104 (338.25, 105.3) | TRACES |
| A9 | About 3.2 million people live on ground moving faster than 10 cm/yr, line of sight, WorldPop 2020 | P, D5, S5 | memo L131 (3.23 million on 338 km²) | TRACES |
| A10 | About 4 cm per month at the fastest 0.1% of pixels in the first 72 days, line of sight | P | PoC README L33, L39; `provenance.json` L105 (9.7 cm by Jan 22 → 4.1 cm/month) | TRACES |
| A11 | About 2 cm uncertainty on any single number; hills control point drifts about -2.2 cm | P, D7, S7 | memo L129; PoC README L27, L61; CSV L9 (-2.16) | TRACES |
| A12 | Vertical roughly 1.27 times line of sight if motion is purely vertical (cos 38°) | P, S7 | memo L130; `docs/DECISIONS.md` L25 (D-19); `docs/T35_SIGN_CHECK.md` L42 | TRACES (assumption named both times; no vertical number given) |
| A13 | Horizontal motion at bowl edges breaks the vertical assumption | P | `docs/T35_SIGN_CHECK.md` L44 | TRACES |
| A14 | Positive = away from the satellite (sinking) | P, deck header | `docs/DECISIONS.md` L25 (D-19); `docs/T35_SIGN_CHECK.md` L9; memo L129. **Note:** `provenance.json` L5-6 still says "INFERRED, not confirmed (T-35)"; stale after D-19. | TRACES |
| A15 | Sign: specification JPL D-102272 not public; four checks agree (ISCE3, ARIA-tools, MintPy, our bowls) | P | `docs/T35_SIGN_CHECK.md` L11, L21-26; D-19 (L25) | TRACES |
| A16 | Reference area in the western hills, -99.27 to -99.22 E, 19.33 to 19.38 N | P (x2) | memo L129; `provenance.json` L8-13 | TRACES |
| A17 | Method steps: shared zero, no tilt removal, ionosphere subtracted, unwrapping patches re-attached, gap filling (at most 4 of 27), consecutive pairs cancel atmosphere | P | PoC README L47-54; `provenance.json` L84-85 | TRACES |
| A18 | 87% of pixels needed no filling, 12% filled, 1% dropped (water, steep forest) | P | PoC README L52; `provenance.json` L87-89 (0.8685, 0.1187, 0.0128) | TRACES |
| A19 | Two bowls: north-east (airport, Nezahualcóyotl, old Texcoco lakebed), south-east (Tláhuac, Chalco, Xochimilco lakebed); western hills and Sierra de Guadalupe barely move | P, D5, S5 | PoC README L11-16 | TRACES |
| A20 | JPL image puts "Benito Juarez International Airport near the center of the mapped deformation field" | P, S5 | PoC README L16 (quoting the JPL article, memo L103) | TRACES |
| A21 | 80 m pixels are averages; quote percentiles, never the maximum | P | PoC README L62-63; memo L130; `provenance.json` L93 | TRACES |
| A22 | Place locations approximate | P | PoC README L18, L62 | TRACES |

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
| B13 | NASA/JPL published NISAR sinking over Mexico City in April 2026; our contribution is the tool, the full year, place by place | P | memo L62, L75; `docs/PLAN.md` L28 | TRACES |

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
| D4 | The 27 GUNW granule names | P field 7 | `provenance.json` L20-46 | TRACES (script: identical, same order) |
| D5 | The 11 GCOV granule names and "11 dates", Nov 11, 2025 to Oct 13, 2026; same granules for HH, HV and composite | P | manifest (script: 11 unique names, identical set) | TRACES |
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
| D17 | Provisional caveat "Provisional NISAR data. Interpret with caution." on each layer | P ([IF SHIPPED]) | manifest L42, L177, L312. Whether the UI shows it is unverified, so the marker stays. | TRACES |
| D18 | App loads static files only; no login; no API needed | P, D4, S4 | `README.md` L12-13 | TRACES |
| D19 | Pipeline reads only the window over HTTPS with Earthdata login (`earthaccess`, `h5py`), so it does not need whole granules | P | `docs/PLAN.md` L174; D-03 (L9); D-15 (L21, G1 passed) | FIXED: "we never download whole granules" is false; the memo (L34) records three whole files (16 GB) downloaded for the first look. |
| D20 | GCOV build: dB, Web Mercator reprojection, small images, manifest with granule names | P | `docs/PLAN.md` L178-183; manifest | TRACES |
| D21 | Azure Static Web Apps + managed Azure Functions typed API; Cloudflare Pages backup | P, D4, S4 | `README.md` L13, L46-47; `docs/AI_USAGE.md` L21, L31; D-05 (L11) | TRACES |
| D22 | Live URLs: https://yellow-desert-02401091e.4.azurestaticapps.net and https://built-to-last-6or.pages.dev | P field 4, D7 footer | `README.md` L46-47 | TRACES |
| D23 | Repo URL https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026, MIT license | P, D7 | `docs/AI_USAGE.md` L20 (PR links); `README.md` L42 (MIT) | TRACES |
| D24 | A new region is one entry in `pipeline/config/regions.json` plus a content file, with no code changes | P, D7, S4, S7 | `docs/PLAN.md` L170 | FIXED: D7 and S7 said "one config entry" and dropped the content file; S4 said "the same pipeline works for other regions" (no other region is shown working). Now D7 "new regions by configuration, no code changes", S7 "one config entry plus a content file", S4 "the pipeline is built to take other regions". P traced. |
| D25 | Libraries and languages | P | `docs/SOURCES.md` L28-29; PoC README L85 (matplotlib) | TRACES |
| D26 | Status of live features: ground-motion layer, layer switcher and legend being merged (Sun 6:45 AM); 7 landmark points in `landmarks.json`; landmark cards on the map not confirmed; flood-priority map not shipped | P notes, D header, all [IF SHIPPED] markers | 6:45 AM status relayed to the fact-checker; `app/public/data/mexico_city/landmarks.json` L7-697 (7 named landmarks). The origin/main manifest has no ground-motion layer yet, so the marker stays. | FIXED: the notes cited the 1:45 AM status. The summary's single [IF SHIPPED] covering both the layer and the cards is now two markers. |
| D27 | Flood-priority map as a shipped feature | P (What we built, Benefits), S7 | Not shipped (6:45 AM status) | DELETED: the [IF SHIPPED] flood-map bullet on the page and the [IF SHIPPED] sentence in S7. Kept only as "Planned next ... screening aid on PROVISIONAL data, not a forecast", which traces to `docs/PLAN.md` L47, L271 (T-34) and D-16 (L22). |
| D28 | Seven landmark names; new Lake Chalco = Lago de Tláhuac-Xico | P | `docs/PLAN.md` L261 (T-19); `landmarks.json` L7, L122, L237, L352, L467, L582, L697 | TRACES |
| D29 | Story line, "recognize and measure", landmark, stakes | P, D1, S1, S7 | `docs/DECISIONS.md` L22 (D-16); `docs/PLAN.md` L47 | TRACES |
| D30 | Valley of Mexico | P, S4 | manifest L7 | TRACES |
| D31 | WorldPop file name, CC BY 4.0, URL | P field 8 | memo L131 | TRACES |
| D32 | ISRO *NISAR Data Product Format Document* v1.2.1 read for the sign check | P field 8 | `docs/T35_SIGN_CHECK.md` L21 | TRACES |
| D33 | NISAR Data User Guide GUNW page and earthaccess page URLs | P field 7 | `docs/T35_SIGN_CHECK.md` L28; `docs/PLAN.md` L174 | TRACES |
| D34 | Learning resource URLs | P field 8 | `docs/SOURCES.md` L16-25; `docs/challenge/README.md` L79-88 | TRACES |
| D35 | Six-step guided tour, live | P (summary, What it does, What we built) | `content/story/mexico_city.json` (6 steps); `app/src/story/StoryTour.tsx`; PR #35, merged Sun 8:15 AM. Live Azure bundle checked Sun about 9 AM: contains "Project Lago" and "Take the tour" | TRACES |
| D36 | "How to read this map" explainers (HH and HV; radar shows vs. we infer; provisional data) and a provisional-data badge on every data view, live; each layer's legend shows "Provisional NISAR data. Interpret with caution." | P (What it does, What we built) | `content/explainers/cards.json`; `app/src/story/ReadingGuide.tsx`, `ProvisionalBadge.tsx` (#35); legend caveat from the manifest (D17) via `Legend.tsx` (#30, #37). Live bundle contains "How to read this map" and "Provisional data" | TRACES. Replaces the [IF SHIPPED] status of D17 for the page |
| D37 | Ground-motion layer, live | P (summary, What it does, What we built, Benefits) | PR #24; live `/data/mexico_city/manifest.json` lists layer `sinking` (checked Sun about 9 AM) | TRACES. Replaces the D26 status for this layer |
| D38 | Landmark cards on the map (tap a landmark; each card separates what the radar shows from what we infer, names human and natural drivers, lists sources) | **Not used.** Left out of the page | Card text is in `content/landmarks/mexico_city.json` (#35), but no component displays it: Zainab's panel (T-14) is not merged as of Sun about 9 AM | LEFT OUT until T-14 is live; then add to "What it does" and cite its PR here |
| D39 | The lake itself is not measured yet; our seasonal reading of the lake is not reviewed | P (Honest limits) | memo L139 (lake point not in `landmark_series_los_cm.csv`); memo L140 (Diego's HV numbers not reviewed) | TRACES |

## E. AI use (field 6) and rules

| # | Claim | Used in | Source | Fact-check |
|---|---|---|---|---|
| E1 | Claude Code uses (Eduardo, Zainab), item by item | P field 6 | `docs/AI_USAGE.md` L14-19, L22-23, L33-35, L37 | TRACES (each item checked against a row) |
| E2 | Codex uses (Elias), item by item, including the favicon | P field 6 | `docs/AI_USAGE.md` L20-21, L24-32, L36, L38-44 | TRACES (each item checked against a row) |
| E3 | GitHub Copilot left automated review comments | P field 6, field 8 | `docs/AI_USAGE.md` L20-41 ("Review: Copilot commented") | TRACES. The log's Tool column lists only Claude Code and Codex; Copilot appears as a reviewer, which is how the page describes it. |
| E4 | This page and the deck outline were drafted with Claude Code | P, D header | This drafting session | FIXED: true but not in `docs/AI_USAGE.md`, so field 6 and the log disagree. Kept (deleting it would hide AI use) with a bracketed note for the team to add a log row before submitting. |
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
| F3 | Project name placeholder; Monica leans "Project Lago" | P field 1 | `docs/PLAN.md` L259 (T-17) | TRACES |
| F4 | "UIUC" (page line 5, pitch slide 1) | P, S1 | Not in any source file | DELETED: no source in the repo. The team can add it back if they want. |
| F5 | "Where one of us has family" (summary); "Our teammate Monica's family is from Santa Cecilia, in Tláhuac" (lake section) | P | Monica's own statement; she consented to it on the page, Sun Nov 15. How close Santa Cecilia is to the lake is **not** claimed (memo L138: source not read) | TRACES (personal, with consent) |
| F6 | Name and tagline: Project Lago, "See the ground beneath your city move." | P field 1, summary | Team decision (T-17), recorded in `coordination/claude_status_monica.md` (#44) | TRACES (not a factual claim) |
| F7 | Next: a Spanish version and a classroom mode | P (Future applications) | Team plan (T-17 outline) | TRACES (a plan, not a claim about the shipped app) |

## G. Wording found during the fact-check

| # | Claim | Used in | Source | Fact-check |
|---|---|---|---|---|
| G1 | Sinking is hard to see from the street "until something breaks or floods" | P (The problem) | None | DELETED: no source. "Slow and hard to see from the street" kept (D-16: "a slow hazard"). |
| G2 | Slide 4 headline "Swipe, tap, read" | D4 | Implied the landmark cards, which are not confirmed on the map | FIXED: now "Swipe and compare: a live, open-source map". |
| G3 | Spoken word counts and the [IF SHIPPED] timing note | S | Counted by script (bracketed text excluded, 2.5 words per second) | FIXED: counts are now 30 / 86 / 80 / 45 / 77 / 82 / 71. The slide 4 [IF SHIPPED] sentences are 29 words (the note said 15). Slide 7 no longer has an [IF SHIPPED] sentence. |

## Flags for the fact-checker

1. **Favicon.** `docs/AI_USAGE.md` L32 says Codex drafted the favicon (`app/public/favicon.svg`, `.ico`). The rules (`docs/challenge/README.md` L46) say AI-generated images need a visible watermark. The team should decide whether the favicon needs a watermark or a visible note.
2. **Stale sign text.** `provenance.json` L5-6 and PoC README L59 still say the sign is inferred. D-19 settles it. The page follows D-19.
3. **"Works on a phone"** is not claimed as fact anywhere. Slide 4 uses a phone screenshot only if the phone layout was checked at G5.
4. **"Water collected again from 1988"** (slide 6) frames the UNAM fact "water first collected in 1988" (memo L122) as part of the D-16 "lake that came back" story.
5. **Paraphrases of quoted rows:** "urban weight" / "the weight of the city" for "the weight of urban development" (B4); "records the echo" for "records the amount of that energy reflected back" (B7); "due to pumping" for "como consecuencia del bombeo" (C4).
6. **"12-day" in the PoC README and PLAN.** PoC README L11 and `docs/PLAN.md` L47 also say "27 consecutive 12-day" pairs. The page and deck now follow the dates in `provenance.json` (one 24-day pair).
7. **AI_USAGE row needed** for the drafting of this page and deck (E4).

## Claims left out because they have no usable source row

- Chaussard et al. (2021) "rates reach up to 50 cm per year": memo L107 says to read the abstract first; nobody recorded doing so. Listed as a reference only.
- AP coverage of the JPL release, "nearly 10 inches (about 25 centimeters) a year" (PoC README L40): no URL or memo row.
- Vertical figure for Nezahualcóyotl (about 28 cm, `docs/T35_SIGN_CHECK.md` L43): not in the memo table or the PoC README. Only the 1.27x factor is used.
- How fast the ground moves at new Lake Chalco: not sampled (memo L139).
- "Water looks dark, buildings look bright": not on the Earthdata page (memo L136).
- The late-June 2026 wetland step and the farm-belt seasonal brightening (memo L43): not in the quote table; the farm-belt pass is unreviewed.
- Diego's lake HV numbers (+1.2 dB): not reviewed (memo L140).
- The UNAM 2007 projections for 2010 and 2015 (memo L124-125): projections, not checked.
- Tláhuac history and borders (memo L138): sources not read.
- Incidence angles 36.7° to 40.7° and wavelength 24.2 cm: the memo's cos(38°) is used instead; the PoC README's 24.2 cm is left out to avoid confusion with "about 23 cm".
- The flood-priority map as a live feature: not shipped as of Sun 6:45 AM (D27).
