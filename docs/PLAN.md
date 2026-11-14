# Hackathon plan: Dancing with the SARs, Mexico City

**Status: v0.3, approved by Eduardo and in force since Sat Nov 14, 3:55 PM CT.**
v0.3 merges the 9:30 PM and 11:30 PM gates into one go/no-go at Sun 1:00 AM (G2), keeps 9:30 PM as a progress checkpoint, and moves the G1-fallback GUNW download to Eduardo's laptop in the evening (see section 13).
v0.2 added Eduardo's answers (map owner, Azure, repo, slide deck), a first look at the files in `Datasets/`, and a story decision gate: the team analyses the data and picks the story.
Only the plan agent (Eduardo's session) edits this file, and only after Eduardo says yes. Everyone else raises problems in their own status file and references task IDs (T-01, T-02, ...).

All times are Central Time. **Hard deadline: Sun Nov 15, 1:30 PM. We submit by 12:00 PM.**

Related pages: [challenge requirements](challenge/README.md) · [decision memo](DECISION_MEMO.md) · [data contract](DATA_CONTRACT.md) · [decisions log](DECISIONS.md) · [AI usage](AI_USAGE.md)

---

## 1. What we checked, and what it changes

| Finding | Evidence | What it changes |
|---|---|---|
| The demo is **7 slides or a video of 30 seconds or less**. Going over makes us ineligible for global judging. | Submission Guide | No long demo video. We make a 7-slide deck. A short screen recording is a bonus for the README, not the demo. |
| We can edit and resubmit until Sun 11:59 PM, and only the last saved version is judged. | Submission Guide | Still treat 1:30 PM as final. Local judges start at 2:00 PM. |
| The AI field is called "Use of Super Intelligence (SI)". AI should not come up with the idea. Generated code needs a notice in text and metadata, generated images and video need a watermark. | Submission Guide | The team makes the story decision (see memo). Every AI-written file gets a header comment. We generate no images or video with AI. |
| Judging criteria are Impact, Creativity, Validity, Relevance, Presentation, each 1 to 5. | Judging Guide | Same as 2025. |
| One track (19, frame 11, ascending) covers all of Mexico City with **29 GCOV dates and 28 chained GUNW pairs, Oct 30, 2025 to Oct 13, 2026, all PROVISIONAL**. | [catalog summary](../pipeline/reports/summary_mexico_city.md) | No January to June gap. No mixing of BETA and PROVISIONAL. A one-year story is possible. |
| Polarizations are HH and HV only. | Same | The polarization answer is HH vs. HV. We do not have VV. |
| Files are big: GCOV 7.1 GB, GUNW 2.3 GB each. The full one-track set is 205 GB + 65 GB. | Same | We cannot download the time series. We read only our window from the cloud-hosted files (gate G1), with sized fallbacks. |
| Soil moisture (SME2) exists here as PROVISIONAL, 0.12 GB per file, "not yet fully calibrated". | Catalog + ASF known issues | Optional Tier 3 extra, not a dependency. |
| NASA/JPL published NISAR subsidence over Mexico City on Apr 29, 2026. | JPL article (link in memo) | We have a reference to check against. We also cannot claim the finding as new. |
| Browse PNG quicklooks of each granule download with no login. HDF5 files need Earthdata login. | Tested Nov 14 | Quicklooks can seed the sample dataset. There is no `.netrc` on Eduardo's laptop yet. |
| The repo is **private** and has no license. | `gh repo view` | It must be public with a license before we submit. |
| The saved challenge pages are in `docs/challenge/` and stay out of git (20 MB of site assets, and they contain a logged-in account name). | Repo | The summary in `docs/challenge/README.md` is what gets committed. |

First look at the four files in `Datasets/` (16 GB, on Eduardo's laptop, git-ignored). Pictures are in `data/quicklooks/`, made by `pipeline/quicklook.py`.

| Finding | What it changes |
|---|---|
| Dataset names and grids are confirmed on real files. GCOV: `frequencyA` is 10 m pixels (33,480 x 34,128), `frequencyB` is 80 m. GUNW: unwrapped phase, coherence, connected components, and ionosphere screen at 80 m; wrapped interferogram at 20 m. Everything is in UTM zone 14N (EPSG:32614). Radar wavelength from the file: 24.2 cm. | The recipes in section 7 are no longer guesses. Cropping our box from a local file takes about a second. |
| The three complete files do not match each other. The Oct 30, 2025 GCOV is **BETA** (release X05009). The Nov 6, 2026 GCOV is release P05036 from the `NISAR_L2_GCOV_V1` collection, not the PROVISIONAL collection. The GUNW is track 113 (descending), Oct 8 to Oct 20, 2026. | Fine for exploring. For the app, use one release per layer. A PROVISIONAL version of the Oct 30, 2025 scene exists. Check how ASF labels `NISAR_L2_GCOV_V1` before we describe that file. |
| A fourth file (105 MB, same name as the Nov 6 file without "(2)") was a truncated download that would not open. | Deleted on Eduardo's instruction, Nov 14, 3:09 PM. |
| **One 12-day GUNW pair does not show sinking on its own.** The raw picture is a smooth tilt of several centimeters across the valley. After removing the tilt, blobs of about 1 cm remain everywhere, including over the mountains. That is the size of the motion we expect in 12 days, so signal and noise cannot be told apart in one pair. | A ground-motion layer needs many pairs added together. It depends on G1 (remote reads) or on about 32 to 65 GB of downloads. Do not promise it before G2 (Sun 1:00 AM). |
| GCOV from Oct 30, 2025 to Nov 6, 2026 (same season, one year apart): the dark lakebed zone north-east of the airport is clearly darker in HV in 2026, and patches in the southern wetland and farm zone are brighter. The whole scene is also about 1.4 dB brighter in HV, which is probably the different processing releases, not the ground. Place names are read off pixel positions and need checking on a map. | Year-over-year and seasonal surface change is visible in GCOV with almost no processing. It is a real candidate story. Repeat with two files of the same release before believing any number. |

Other Mexican regions with data (granule counts for GCOV / GUNW / SME2, all collections): Monterrey 120 / 94 / 112, Mexicali Valley 117 / 100 / 112, Popocatepetl 95 / 83 / 89, Guadalajara and Chapala 90 / 72 / 82, Aguascalientes 87 / 71 / 82, Tabasco wetlands 81 / 64 / 73. Stretch only.

## 2. Story and scope

**The story is not chosen yet.** The team looks at the data first (T-25) and decides by **Sat 5:30 PM** (gate GS). The candidates, what the catalog and the local files say about each, and the sources for every number are in the [decision memo](DECISION_MEMO.md).

Building does not wait for the decision. Tier 1 below is the same for every candidate: it shows GCOV layers, a swipe, and landmark cards. The story decides which dates, which landmarks, what the text says, and what Tier 2 is. If there is no decision by 5:30 PM, the default is surface change seen in GCOV (seasonal and year-over-year), because Tier 1 already carries it.

| Tier | What ships | Deadline |
|---|---|---|
| **1, must ship** | Map with GCOV layers (HH, HV, HH/HV composite) for one dry-season and one rainy-season date, swipe slider, 5 to 7 landmark cards, polarization explainer, provisional label, sources page. Static, on Azure, with bundled sample data. | Core live at the Sat 9:30 PM checkpoint; complete and live by Sun 1:00 AM (G2) |
| **2** | Ground-motion layer from 28 GUNW pairs with a chart per landmark. GCOV time slider with about monthly frames. | Checked Sun 1:00 AM (G2), in the app by Sun 8:00 AM |
| **3** | Soil moisture layer, second region, Spanish/English toggle, point query API, Azure AI helper, data-quality flag. | Only if Tier 2 is in by Sun 7:30 AM |

If we fall behind, cut in this order: all of Tier 3, the borough context layer (T-21), GCOV time slider, per-landmark charts, ground-motion layer, HH/HV composite. Never cut: real NISAR data on the map, the swipe, the landmark text, the polarization explainer, the provisional label, the sources.

## 3. Gates

| Gate | Time | Question | If no |
|---|---|---|---|
| G1 | Sat 4:30 PM | Can we read our window out of a remote GCOV file and a remote GUNW file? | Full-file downloads, **pre-approved by Eduardo**: 2 GCOV of one release (14 GB, about 55 min). Tier 2 shrinks to 14 GUNW pairs (32 GB, about 2 h), downloaded on Eduardo's laptop as soon as G1 fails, after the GCOV files so they do not split the Wi-Fi. Not overnight. Shared with other machines through LocalSend over a direct Ethernet link. Anything beyond these two sets still needs Eduardo's yes. |
| GS | Sat 5:30 PM | Has the team chosen the story from the data (T-25)? | Default story: surface change in GCOV. Ground motion stays a Tier 2 option behind G2. |
| Checkpoint | Sat 9:30 PM | Progress report, not a gate. Is the core of Tier 1 live on the public URL with real data (GCOV layers, swipe, landmark cards; text may still be placeholders)? Each person says what is left for G2. | Nothing is cut here. Problems found go into block E. |
| G2 | Sun 1:00 AM | Go or no-go, before anyone sleeps. (a) Is all of Tier 1 live, including the polarization explainer, provisional label, sources page, and landmark text? (b) Does the ground-motion map pass the T-32 sanity check? This one gate replaces the old G2 (9:30 PM) and G3 (11:30 PM). | (a) No: no Tier 2; block G finishes Tier 1. (b) No: cut or shrink the layer; the headline becomes seasonal change. |
| G4 | Sun 8:00 AM | Feature freeze. Main deployed and working? | Roll back to the last good deploy. |
| G5 | Sun 10:30 AM | All links open in a private window, all form fields drafted? | All hands on the submission. |

At each gate the plan agent posts one line in `coordination/CHANGELOG.md`: on track or not, and what was cut.

## 4. Who owns what

Eduardo confirmed he owns the map screen (Nov 14, 2:30 PM) and approved the rest with plan v0.2.

| Person | Area | Core component (ships in the app) | Backup | Also |
|---|---|---|---|---|
| **Elias** | Data pipeline, API, deploy, integration | **Data build**: `pipeline/` turns NISAR windows into images, `manifest.json`, and `landmarks.json`; plus the typed API in `api/` and the Azure deploy | Eduardo (pipeline, deploy), Zainab (API) | Stretch: data-quality flag |
| **Eduardo** | Lead, science, core map | **Map screen**: `app/src/map/` and the shared app state; MapLibre map, image layers from the manifest, swipe compare | Monica | Tier 2 ground-motion math in `pipeline/science/`, science review of every claim, final submit |
| **Monica** | Story, UI/UX, submission | **Story layer**: `app/src/story/`; intro, guided walkthrough, explainer cards, visual design, mobile | Zainab | Slides, project page text, landmark copy, pitch |
| **Zainab** | Documentation, front end | **Landmark panel and chart**: `app/src/components/landmarks/` and `chart/`; plus the manifest validator in `pipeline/` | Monica (UI), Eduardo (validator) | README, data contract write-up, `AI_USAGE.md`, `SOURCES.md`, tests |
| **Diego** | Data acquisition, front end | **Layer controls**: `app/src/components/layers/` and `time/`; layer switcher, legend, time slider | Elias (data), Zainab (UI) | Runs the fetch jobs paired with Elias, keeps the local-data table |

Estimated share of coding hours (about 32 hours in total): Elias 28%, Zainab 23%, Eduardo 18%, Diego 18%, Monica 13%. Monica's lower share is offset by the slides, project page, and pitch (about 6 hours).

What was moved off Elias, per the workload rule: ground-motion math (Eduardo), landmark sampling and validator (Zainab), image rendering helpers and fetch-job babysitting (Diego), all docs (Zainab), demo and page (Monica). Elias keeps pipeline, API, deploy, integration.

Coding exercises that are real project code:

| Person | Exercise | How to check |
|---|---|---|
| Zainab | T-08 write the sample manifest by hand from the contract, then `validate_manifest.py` | `pytest pipeline/tests/test_validate.py` passes; a broken fixture fails |
| Zainab | T-16 complete `sample_at_points()` | Given tests with a synthetic raster pass |
| Zainab | T-31t write tests for `displacement.py` and explain the module in `docs/ARCHITECTURE.md` | Tests pass; Eduardo reads the explanation |
| Diego | T-11 complete `to_db()`, `stretch()`, `apply_colormap()` in `pipeline/render.py` | Given tests pass; one PNG looks right |
| Diego | T-12, T-13 build the layer controls against the sample manifest | Works with sample data before real data exists |
| Diego | T-59t follow the README on a clean clone | App runs with no help; gaps filed to Zainab |

## 5. Interfaces that keep five people out of each other's way

**Folder ownership.** You edit your own folders. To change someone else's, ask them or put it in your status file.

| Path | Owner |
|---|---|
| `pipeline/` (except below), `api/`, `.github/`, root config files | Elias |
| `pipeline/science/` | Eduardo |
| `pipeline/validate_manifest.py`, `pipeline/landmarks.py`, `pipeline/tests/` | Zainab |
| `pipeline/render.py` | Diego |
| `app/src/App.tsx`, `app/src/map/`, `app/src/state/` | Eduardo |
| `app/src/types/`, `app/src/lib/` (manifest loader) | Elias |
| `app/src/story/`, `app/src/styles/`, `content/` | Monica |
| `app/src/components/landmarks/`, `app/src/components/chart/`, `app/src/components/sources/` | Zainab |
| `app/src/components/layers/`, `app/src/components/time/` | Diego |
| `app/public/data/<region>/` | Generated by the pipeline (Elias commits) |
| `app/public/data/sample/` | Zainab |
| `docs/` except the next two rows | Zainab |
| `docs/PLAN.md`, `docs/DECISIONS.md`, `docs/DECISION_MEMO.md`, `coordination/CHANGELOG.md` | Plan agent (Eduardo) |
| `docs/submission/` | Monica |
| `coordination/claude_status_<name>.md` | That person only |

**Front-end boundary.** Components never import each other. Each one reads and writes one shared state object, and `App.tsx` places them on the page. The map reacts to the state.

```ts
// app/src/state/store.ts (owner: Eduardo). Drafted with AI assistance.
type AppState = {
  regionId: string;
  manifest: Manifest | null;
  landmarks: Landmark[];
  activeLayerId: string;            // layer shown (left side of the swipe)
  compareLayerId: string | null;    // right side of the swipe; null = no swipe
  dateIndex: number;                // index into the active layer's frames
  compareDateIndex: number | null;
  selectedLandmarkId: string | null;
  storyStep: number | null;         // null = free exploration
};
// actions: setLayer, setCompare, setDate, selectLandmark, setStoryStep
```

Story steps are data, not code: `{ title, body, set: Partial<AppState>, camera: { center, zoom } }` in `content/story/<region>.json`. The walkthrough applies `set` and the map moves.

**Data boundary.** The [data contract](DATA_CONTRACT.md). Front-end work starts against `app/public/data/sample/` and does not wait for real data.

**Git.** One branch per person (`<name>/<short-topic>`), small PRs, squash merge, main always deployable. `git pull --rebase origin main` before starting a task. Never force-push. Nobody merges a red build.

## 6. Repo layout

```text
app/                        Vite + React + TypeScript + MapLibre GL JS
  public/data/<region>/     generated manifest, landmarks, images (small, in git)
  public/data/sample/       tiny bundled sample so the app always runs
  src/{map,state,story,components,lib,types,styles}/
api/                        Azure Functions in TypeScript (typed API)
pipeline/                   Python
  config/regions.json       the only place a region is defined
  search_granules.py        catalog search (done)
  fetch_crops.py            read a window from remote NISAR files into data/interim/
  render.py                 array to color image
  build_manifest.py         writes app/public/data/<region>/
  landmarks.py              sample rasters at landmark points
  validate_manifest.py      contract check
  science/displacement.py   GUNW pairs to ground motion
  tests/
  reports/                  catalog evidence (CSV and summary)
content/                    hand-written landmark and story text
data/                       raw and interim data, git-ignored
coordination/               one status file per person, CHANGELOG
docs/                       plan, memo, contract, sources, AI usage, submission drafts
```

A new region is a new entry in `pipeline/config/regions.json` plus a content file. No code changes.

## 7. Technical approach

**Getting the data without downloading 270 GB.** NISAR files sit in the cloud and can be read in pieces over HTTPS with an Earthdata login. ASF documents this with `earthaccess` (<https://nisar-docs.asf.alaska.edu/earthaccess/>): `earthaccess.login()` reads `~/.netrc`, then `earthaccess.get_fsspec_https_session()` opens a file by URL, and `h5py` or `xarray` reads only the part we ask for. Do not pass `daac='ASF'`; the ASF page says it causes errors for NISAR. This is unproven on our Wi-Fi until T-01 is done. That is what gate G1 is for.

**GCOV recipe (Tier 1).** Dataset names below are confirmed on the local files. `pipeline/quicklook.py` already does steps 1 to 3 and 5 for a local file.

1. Open `/science/LSAR/GCOV/grids/frequencyB` (80 m pixels, tiny) for the whole valley. Use `frequencyA` (10 m pixels) later, only for zoomed windows around landmarks.
2. Convert our bounding box to the grid's map projection and find the row and column range.
3. Read the `HHHH` and `HVHV` windows. Mask empty pixels. Convert to decibels with `10 * log10(x)`.
4. Reproject to Web Mercator with `rasterio`, stretch between the 2nd and 98th percentile, save as WebP.
5. Composite: red = HH, green = HV, blue = HH minus HV in dB.
6. Write `manifest.json`, run the validator.

Dates: one late dry-season date and one late rainy-season date, both on track 19 / frame 11 so the viewing geometry is identical. Pick them after looking at the quicklooks. Cite a source for when the rainy season is before the app says it.

**GUNW recipe (Tier 2, if the team chooses ground motion).** Spec: JPL D-102272 (linked from the ASF product pages). Dataset names are confirmed on the local file: `/science/LSAR/GUNW/grids/frequencyA/unwrappedInterferogram/HH/` holds `unwrappedPhase`, `coherenceMagnitude`, `connectedComponents`, and `ionospherePhaseScreen`. One pair is not enough (see section 1); the method only works on the chain of pairs.

1. Read the unwrapped phase, coherence, connected-components, and ionosphere layers for our window (80 m pixels) from each of the 28 pairs.
2. Mask pixels with low coherence or no connected component. Water and vegetation will drop out. That is expected.
3. Check in the spec whether the unwrapped phase already has the ionosphere correction applied. Apply it if not. In the local file the ionosphere layer is large (tens of centimeters when converted), so this step cannot be skipped. Then remove a best-fit tilt across the box from each pair.
4. Subtract the median phase of a reference area that is known to be stable (a rock outcrop named in the literature, not a guess).
5. Convert phase to centimeters along the line of sight using the wavelength stored in the file. Confirm the sign convention against the JPL image: the airport area must come out as moving away from the satellite.
6. Add the 28 pairs in order to get cumulative movement per date. Divide by elapsed years for a rate map.
7. Sanity check (T-32) before anything goes on the map.

What we will say: movement is along the radar's line of sight, relative to our reference area, from provisional data. We do not call it vertical sinking in centimeters unless we convert it and say how.

**Azure.** Azure Static Web Apps (free tier) serves `app/`, and its managed Azure Functions serve `api/` on the same origin. Deployed by a GitHub Actions workflow with a deployment token stored as a repo secret. The app loads static files first and never needs the API for the demo. Fallback host: the same `app/dist` on GitHub Pages or Cloudflare Pages. Whether hosting alone counts for the Best Use of Technology award is unconfirmed (T-05).

**Map.** MapLibre GL JS. No API keys in the front end. T-09 picks a keyless basemap and an optical imagery layer (candidates: OpenFreeMap; NASA GIBS imagery; Sentinel-2 cloudless) and records license and attribution in `docs/SOURCES.md`.

**Python.** Use Python 3.12 in a virtual environment for the pipeline. If `h5py` or `rasterio` fails to install on a newer Python, do not debug it, switch to 3.12.

## 8. Timeline

| When | Block | What happens |
|---|---|---|
| Sat 3:10 to 3:20 PM | Kickoff | 10-minute standup. Everyone pulls `main`, creates `CLAUDE.local.md`, and starts their agent with the prompt in section 14. Earthdata `.netrc` set up on the two NVIDIA laptops. |
| 3:20 to 4:30 PM | A: prove the data path, look at the data | T-01 to T-09 and T-25. |
| **4:30 PM** | **G1** | 10-minute standup. |
| 4:30 to 6:00 PM | B: first real images | Pipeline on two GCOV dates. Components against sample data. First Azure deploy before dinner. **GS at 5:30 PM: story chosen.** |
| 6:00 to 6:45 PM | Dinner | |
| 6:45 to 7:30 PM | C | First real data on the live URL. Start the long fetch jobs before the talk. |
| 7:30 to 8:30 PM | Speaker talk | Jobs run unattended. (Length assumed 1 hour.) |
| 8:30 to 9:30 PM | D: Tier 1 integration | Everyone tests the live site on a laptop and a phone. |
| **9:30 PM** | **Checkpoint** | Progress report: core Tier 1 on the live URL, and what is left for G2. Not a go/no-go. |
| 9:30 to 11:30 PM | E | Tier 1 text and pages (T-19, T-23, T-24). Tier 2 processing (T-31, T-33). Slides and page text drafted with placeholders. |
| **11:30 PM** | Standup | Short standup. No gate. |
| 11:30 PM to 1:00 AM | F | Finish Tier 1. T-32 sanity check. Start overnight jobs. Main green and deployed. |
| **1:00 AM** | **G2** | Go or no-go for Tier 2, then sleep. |
| 1:00 to 7:00 AM | Sleep | |
| Sun 7:00 to 8:00 AM | G | Wire Tier 2 in if G2 said go (T-34); otherwise finish Tier 1. |
| **8:00 AM** | **G4, feature freeze** | Breakfast. |
| 8:30 to 10:30 AM | H: submission build | Bug fixes only. Copy, screenshots, slides, page text, README. Repo public. |
| **10:30 AM** | **G5** | Link check in a private window. |
| 10:30 to 11:45 AM | I | Eduardo's final review. Text fixes only. |
| **12:00 PM** | **Submit for Judging** | Then lunch. |
| 12:30 to 1:15 PM | Rehearsal | Two full run-throughs of the live pitch. |
| **1:30 PM** | **Local deadline** | Nothing changes after 1:15 PM. |
| 2:00 to 5:00 PM | Judging | Laptop on the fallback URL as a second tab. |

That is about 13 working hours per person.

## 9. Task board

Tier 1 unless marked. "Est." is hands-on hours. Blocks refer to section 8.

| ID | Task | Owner | Block | Est. | Done when |
|---|---|---|---|---|---|
| T-01 | Remote-read probe: Earthdata login, then read one GCOV `frequencyB` HH and HV window and one GUNW unwrapped-phase window over the Mexico City box straight from the cloud. Start from the reading code in `pipeline/quicklook.py`, which already works on local files. | Elias (Diego joins after T-25) | A | 1.0 | Two crops saved in `data/interim/`, a quick PNG of each in the team chat, seconds and megabytes per read written in the status file. Feeds G1. |
| T-25 | Data exploration for the story choice. Run `pipeline/quicklook.py` on the local files (whole valley at 80 m, then 10 m zooms on places that look interesting). Flip through the no-login browse pictures of all 29 GCOV dates on ASF Vertex. For each candidate in the memo, write what is visible, where, and how sure we are. | Diego drives, Monica looks for the story, Eduardo interprets (20 min at 4:15 PM) | A | 1.5 | Half a page of findings with pictures shown at the 4:30 PM standup; team decision recorded in `DECISIONS.md` by 5:30 PM (GS) |
| T-02 | App scaffold: Vite + React + TypeScript + MapLibre, state store, contract types stub, lint and build scripts | Eduardo | A | 0.75 | `npm run dev` shows a map of Mexico City; `npm run build` passes; merged by 4:00 PM |
| T-03 | Pipeline skeleton: `fetch_crops.py` from the T-01 probe, region config loader, `pytest` wired | Elias | A | 1.0 | `python pipeline/fetch_crops.py --region mexico_city --product GCOV --date <d>` writes a crop; one test passes |
| T-04 | Get an Azure subscription, then Azure Static Web Apps deploy from `main`, fallback host, CI (lint, test, build) on PRs. Eduardo adds the deployment token as a repo secret. | Elias (backup Eduardo) | B | 1.25 | Public Azure URL and fallback URL both serve main; both URLs in README; done before 6:00 PM |
| T-05 | Ask the organizers: does Azure hosting plus Functions qualify for the award, how long is the live pitch and what do judges look at, may we edit after 1:30 PM | Monica | A | 0.25 | Answers given to Eduardo by 3:00 PM and logged in `DECISIONS.md` |
| T-06 | Read NASA "What is SAR" and the JPL Mexico City article; draft a 150-word plain-language explainer of radar, HH, and HV | Monica (Eduardo reviews) | A | 1.0 | Draft in `content/`; every claim has a source ID |
| T-07 | README skeleton, MIT `LICENSE`, `docs/SOURCES.md`, keep `docs/AI_USAGE.md` current | Zainab | A | 1.0 | A stranger can see what the project is and how it will run; license present |
| T-08 | Sample dataset in `app/public/data/sample/` written by hand from the contract, then `validate_manifest.py` with tests | Zainab | A | 1.5 | Sample fixture merged by 4:00 PM (unblocks all front-end work); validator passes on it and fails on a broken copy |
| T-09 | Map screen: basemap, image layers from the manifest, layer and date switching from state, swipe compare, attribution | Eduardo (backup Monica) | A, B | 2.5 | Sample layers sit in the right place; swipe works with mouse and touch; no API key in the code |
| T-10 | GCOV build: crops to dB, reproject, WebP, composite, `manifest.json` for the two chosen dates | Elias (backup Eduardo) | B, C | 2.5 | One command rebuilds `app/public/data/mexico_city/`; validator passes; folder under 30 MB |
| T-11 | `pipeline/render.py`: `to_db`, `stretch`, `apply_colormap` against given tests | Diego | B | 1.0 | Tests pass; used by T-10 |
| T-12 | Layer switcher and legend | Diego (backup Zainab) | B, D | 2.0 | Lists layers from the manifest, shows units, range, and the provisional note; usable at 375 px wide |
| T-13 | Time slider with play and pause (Tier 2 data, built against sample) | Diego | E | 1.5 | Scrubs frames of the active layer; shows the date; hidden when a layer has one frame |
| T-14 | Landmark panel: list, select, fly to, card with "radar shows" and "we infer" kept separate | Zainab (backup Monica) | B, C | 2.0 | Works from `landmarks.json`; selecting on the map and in the list stay in sync |
| T-15 | Time-series chart per landmark (Tier 2) | Zainab | E | 1.5 | Axis titles with units, gaps for missing dates, provisional note, readable on a phone |
| T-16 | `pipeline/landmarks.py`: `sample_at_points()` against given tests | Zainab | D | 1.0 | Tests pass; pipeline fills `series` in `landmarks.json` |
| T-17 | Project name, tagline, story outline in 6 steps, written once the story is chosen (GS) | Monica | B | 0.5 | Team agrees before dinner |
| T-18 | Intro screen and guided walkthrough driven by `content/story/mexico_city.json` | Monica (backup Zainab) | B to D | 3.0 | A first-time visitor understands the point in 60 seconds; "explore freely" exits the tour |
| T-19 | Landmark text for 5 to 7 places with a source for every claim | Monica writes, Eduardo reviews | C to E | 1.5 + 0.75 | `content/landmarks/mexico_city.json` merged; no unsourced claim; live by G2 (Sun 1:00 AM) |
| T-20 | Typed API on Azure Functions: health, regions, manifest, landmarks | Elias (backup Zainab) | D, E | 1.0 | Four routes live on the Azure URL; error shape per contract; app still works with the API off |
| T-21 | Borough boundaries with population as a GeoJSON context layer | Diego | F, G | 1.0 | File under 1 MB; official source and license in `SOURCES.md`. First to cut. |
| T-22 | Integration pass for the 9:30 PM checkpoint | Elias, everyone tests | D | 0.75 | Live URL shows real GCOV with swipe, landmarks, and tour; no console errors; works on one phone |
| T-23 | Explainer cards (polarization; shows vs. infer), provisional badge, mobile pass | Monica | E, F | 1.5 | Badge visible on every data view; live by G2 (Sun 1:00 AM) |
| T-24 | Sources page in the app, generated from the manifest `sources` and `SOURCES.md` | Zainab | E, F | 0.5 | Every dataset, library, and image is listed with a link; live by G2 (Sun 1:00 AM) |
| T-30 | Tier 2: fetch the GUNW windows for all 28 pairs | Diego runs, Elias backs up | C (runs during the talk) | 1.0 | 28 crops in `data/interim/`; failures listed in the status file |
| T-31 | Tier 2: `pipeline/science/displacement.py` per the recipe in section 7 | Eduardo | E | 2.5 | Runs on the 28 crops; Zainab's tests (T-31t, 0.75 h) pass on synthetic data |
| T-32 | Tier 2: sanity check for G2 | Eduardo | F | 0.5 | Written in `DECISIONS.md`: where the fastest motion is, its rate, how stable the reference area is, how that compares with the JPL article and the literature |
| T-33 | Tier 2: add ground-motion layer and about monthly GCOV frames to the build | Elias | E, F | 1.0 | Both in the manifest; validator passes; folder under 60 MB |
| T-34 | Tier 2: show the new layers in the app (legend, slider, chart) | Diego, Zainab, Eduardo | G | 1.5 | Live before 8:00 AM Sunday |
| T-40+ | Tier 3 items, in the order of section 2 | Unassigned | G | | Only with Eduardo's go |
| T-50 | Demo deck, **7 slides at most** | Monica (backup Zainab) | E, H | 2.5 | Draft with placeholders by Sat 11:30 PM; final by Sun 10:30 AM; public link opens in a private window |
| T-51 | Text for all 8 project page fields in `docs/submission/PROJECT_PAGE.md` | Monica, Eduardo reviews | F, H | 1.5 + 0.5 | Draft Sat night; reviewed by Sun 9:30 AM |
| T-52 | References: every dataset, tool, library, image, and text source | Zainab | all | 0.75 | `SOURCES.md` complete at G5; pasted into the form field |
| T-53 | SI disclosure text; check every AI-written file has its header; confirm no unmarked AI imagery | Zainab | H | 0.5 | Disclosure matches `AI_USAGE.md` |
| T-54 | Make the repo public after a secrets scan (Eduardo has the rights) | Eduardo, Elias runs the scan | H (earlier if agreed) | 0.25 | Repo public; no credentials in history |
| T-55 | FortiGuard web filter classification request for the live URL | Elias | C | 0.2 | Submitted the evening the URL exists |
| T-56 | Open every submission link in a private window | Zainab | G5 | 0.25 | Demo, project, repo all open with no login |
| T-57 | Live pitch script and two rehearsals | Monica leads, all | I | 1.0 | Fits the organizers' time limit with 15 seconds to spare |
| T-58 | Fill the form, tick both boxes, Submit for Judging | Eduardo | Sun 12:00 PM | 0.5 | Confirmation banner seen; screenshot saved |
| T-59 | README final; Diego runs it on a clean clone (T-59t) | Zainab, Diego | H | 1.0 | Clean clone to running app with only the README |

## 10. What runs while we are away

| When | Job | Machine | Owner |
|---|---|---|---|
| During the talk | T-30 GUNW windows, 28 pairs | NVIDIA laptop 1 | Diego |
| During the talk | GCOV `frequencyB` windows for about 12 monthly dates | NVIDIA laptop 2 | Elias |
| Overnight | GCOV `frequencyA` (10 m) windows around the landmarks for the two Tier 1 dates | NVIDIA laptop 2 | Elias |
| Evening, as soon as G1 fails (after the GCOV fallback) | Full GUNW downloads (32 GB), shared with other machines through LocalSend over a direct Ethernet link | Eduardo's laptop, plugged in, sleep disabled | Eduardo |

Jobs write to `data/interim/`, log to a file, and can be re-run without redoing finished items. Nothing that touches `main` or the deploy runs unattended.

## 11. Demo and pitch outline

The deck and the app tell the same six-step story, and the in-app tour uses the same steps.

| Slide | Content |
|---|---|
| 1 | Project name and tagline. Team B[U]ILT to Last, the five names, the challenge name. |
| 2 | The problem in one picture: a city of millions on an old lakebed, changing in ways nobody can see from the street. Sourced numbers only. |
| 3 | What radar sees that a camera does not, and what HH and HV each pick out. |
| 4 | The app: a screenshot of the swipe and a landmark card. The user experience in three verbs: swipe, tap, read. |
| 5 | What the data shows: the ground-motion map and one landmark chart (Tier 2), or the seasonal comparison (Tier 1). "Radar shows" next to "we infer". |
| 6 | How it works: NISAR data from NASA and ISRO, open pipeline, static app on Azure, open source, provisional-data caveats. |
| 7 | What comes next: any region through one config entry; future NISAR uses. Links to the app and repo. |

Live pitch (length to be confirmed in T-05; plan for 3 minutes): 20 seconds on the problem, 90 seconds live in the app following the tour, 30 seconds on how it works and what is provisional, 20 seconds on what comes next, then questions. One speaker and one driver. Every member can answer "what does HH vs. HV show?" and "why is this provisional?".

## 12. Submission checklist

| Item | Owner | Reviewer | Due |
|---|---|---|---|
| Project Name, High-Level Summary, Detailed Description | Monica | Eduardo | Sun 9:30 AM |
| Link to Project Demo (7-slide deck, public) | Monica | Zainab | Sun 10:30 AM |
| Link to Final Project (Azure URL; repo link in the description) | Elias | Zainab | Sun 10:30 AM |
| Use of SI | Zainab | Eduardo | Sun 10:00 AM |
| NASA Data (exact collection names, granule list, tools) | Zainab from the manifest | Eduardo | Sun 10:00 AM |
| Partner data and references (ISRO for NISAR; ESA if we use Sentinel-2 imagery; all libraries) | Zainab | Monica | Sun 10:00 AM |
| Repo public, MIT license, README runs from a clean clone | Zainab, Elias | Diego | Sun 10:00 AM |
| Two or three screenshots under 10 MB for the page | Monica | | Sun 10:00 AM |
| Submit for Judging | Eduardo | | Sun 12:00 PM |

## 13. Answered and still open

Answered by Eduardo on Nov 14, 2:30 PM: Eduardo owns the map screen. `docs/COORDINATION.md` is in. The story is chosen by the team after data analysis (GS). Elias gets the Azure subscription. Eduardo can make the repo public and add secrets. The demo is a slide deck.

Also answered at 3:05 PM: the plan is approved. The G1 fallback downloads are approved in advance (14 GB of GCOV, 32 GB of GUNW overnight); they start only if G1 fails. The truncated file is deleted.

Changed at 3:55 PM (plan v0.3): one go/no-go at Sun 1:00 AM (G2) instead of gates at 9:30 PM and 11:30 PM, because Tier 1 text (T-19, T-23, T-24) was scheduled after the 9:30 PM gate and an overnight GUNW download could not finish before the 11:30 PM gate. 9:30 PM stays as a progress checkpoint. The 32 GB GUNW fallback runs on Eduardo's laptop in the evening and moves between machines over LocalSend on a direct Ethernet link. The download sizes approved at 3:05 PM are unchanged.

Still open:

1. **Organizer answers** (T-05): does Azure hosting plus Functions qualify for the award, how long is the live pitch, may we edit after 1:30 PM?
2. **The story** (GS, 5:30 PM).

Timeline note: kickoff slipped from 2:00 to 3:10 PM. Gate times are unchanged, so block A is 70 minutes instead of two hours. T-02 and T-08 merge by 4:00 PM. If T-01 is not finished at 4:30 PM, G1 moves to 5:00 PM and nothing else moves.

## 14. Start here

**Every person, once:** create `CLAUDE.local.md` in the repo root (it is git-ignored) with three lines: `name:`, `role:`, `backup for:`. Copy your role and backups from section 4. Then paste the short prompt from [COORDINATION.md](COORDINATION.md) section 7 into your Claude Code session, followed by your own lines below.

**Everyone, first 20 minutes:** read [challenge/README.md](challenge/README.md), the [decision memo](DECISION_MEMO.md), your rows in sections 4, 5, and 9, and NASA's "What is SAR" page. Put the AI-generation header on every file an agent writes.

Lines to add after the short prompt:

- **Elias:** "I own `pipeline/` (except `science/`, `render.py`, `landmarks.py`, `validate_manifest.py`, `tests/`), `api/`, `.github/`, `app/src/types/`, `app/src/lib/`, and the data contract. My first task is T-01, the remote-read probe that decides gate G1 at 4:30 PM; start from the reading code in `pipeline/quicklook.py`. Then T-03, and T-04 before 6:00 PM. Never put credentials in the repo. If a Python package fails to install, switch to Python 3.12 instead of debugging."
- **Diego:** "I own `pipeline/render.py`, `app/src/components/layers/`, and `app/src/components/time/`. My first task is T-25: make quick-look pictures with `pipeline/quicklook.py` and collect what is visible for each story candidate in the decision memo. Explain each step to me as we go; I am new to this. Do not start any download over 1 GB without telling me so I can ask Eduardo. After the 4:30 PM standup: T-11, then T-12 against the sample data."
- **Zainab:** "I own `docs/` (except `PLAN.md`, `DECISIONS.md`, `DECISION_MEMO.md`, and `docs/submission/`), `pipeline/validate_manifest.py`, `pipeline/landmarks.py`, `pipeline/tests/`, `app/public/data/sample/`, and `app/src/components/landmarks/`, `chart/`, `sources/`. My first task is T-08: the sample dataset from `docs/DATA_CONTRACT.md`, merged by 4:00 PM because the front end is waiting on it. Give me exercises as functions with tests to complete, and have me explain the code back. Then T-07, then T-14."
- **Monica:** "I own `app/src/story/`, `app/src/styles/`, `content/`, and `docs/submission/`. My first tasks are T-05 (three questions for the organizers) and T-06, then T-25 with Diego to look for the story in the data. Every factual sentence needs a source that is listed in the decision memo table; if one is missing, flag it instead of writing the claim. The demo is at most 7 slides. After the story is chosen: T-17, then T-18 against the sample data."
- **Eduardo:** T-02 (merge by 4:00 PM) and T-09. Join T-25 at 4:15 PM.

## 15. Risks

| # | Risk | What we do about it |
|---|---|---|
| 1 | Nobody has SAR experience, so a wrong science claim slips in | Only claims with a source in the memo table; "radar shows" kept apart from "we infer"; Eduardo reviews all copy; our ground-motion map is checked against the JPL image |
| 2 | Remote window reads do not work or are too slow on venue Wi-Fi | G1 at 4:30 PM with sized download fallbacks |
| 3 | Ground-motion processing goes wrong (reference area, sign, noise) | It is Tier 2 behind G2; Tier 1 does not depend on it |
| 4 | Azure setup stalls (subscription, org permissions on a private repo) | Deploy before dinner; fallback host serves the same static build |
| 5 | Demo exceeds 7 slides or 30 seconds | Limit written on the task; Zainab counts slides at G5 |
| 6 | Repo still private or unlicensed at submission | T-54 and T-07 with owners and times |
| 7 | Elias is a single point of failure | Named backups; math, rendering, sampling, docs moved to others |
| 8 | Five agents collide in the same files | Folder ownership, shared state boundary, sample data from the first hour |
| 9 | NASA already published this finding, so Creativity scores low | Lead with the tool: full year, place by place, polarizations explained, open and reusable for other regions |
| 10 | SI rules: the idea must be ours, generated code must say so | Team makes the story call; headers on generated files; `AI_USAGE.md`; no AI images |
| 11 | Main is broken when people go to sleep | Rule in block F; G4 rollback |
| 12 | Judges cannot open the site behind a web filter | T-55 on Saturday evening; fallback URL; screenshots on the project page |
