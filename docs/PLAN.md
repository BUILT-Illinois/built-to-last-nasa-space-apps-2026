# Hackathon plan: Dancing with the SARs, Mexico City

**Status: v0.5, approved by Eduardo and in force since Sat Nov 14, 11:30 PM CT.**
v0.5 sets the story (Mexico City sinking, measured by NISAR; D-16), moves the ground-motion layer and the flood-priority map into Tier 1, redefines the 1:00 AM gate, drops two bad GCOV dates (RB-D04, D-17) and cancels Venezuela and other side work (D-18).
v0.4 records G1 as passed, drops the Oct 30, 2025 acquisition from every layer (D-13), cancels T-11, marks T-04 and T-05 done, and sets the live pitch to 4 minutes (D-14).
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
| One track (19, frame 11, ascending) covers all of Mexico City with **29 GCOV dates and 28 chained GUNW pairs, Oct 30, 2025 to Oct 13, 2026, all PROVISIONAL**. | [catalog summary](../pipeline/reports/summary_mexico_city.md) | No January to June gap. No mixing of BETA and PROVISIONAL. A one-year story is possible. **Since v0.4 the Oct 30, 2025 acquisition is excluded (D-13), so we use 28 GCOV dates and 27 chained GUNW pairs, Nov 11, 2025 to Oct 13, 2026.** |
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
| **Corrected in v0.4.** We first read the Oct 30, 2025 to Nov 6, 2026 comparison as real change: the flat zone north-east of the airport darker in HV, the southern wetland brighter. Diego's check of all 29 dates (RB-D01) shows the Oct 30, 2025 acquisition has measurement errors: every dark area in the valley is lifted on that date only, most in HV, and the other track shows no such drop. In same-release data without that date, the north-east zone changes by under 1 dB and the southern wetland shows no year-over-year change. | **Oct 30, 2025 is dropped from every layer and frame (D-13).** What still stands from T-25: a step in the southern wetland in late June 2026 (medium confidence), and a seasonal brightening of the farm belt on the southern edge of the box that Diego has not reviewed yet. Place names still need checking on a map. |

Other Mexican regions with data (granule counts for GCOV / GUNW / SME2, all collections): Monterrey 120 / 94 / 112, Mexicali Valley 117 / 100 / 112, Popocatepetl 95 / 83 / 89, Guadalajara and Chapala 90 / 72 / 82, Aguascalientes 87 / 71 / 82, Tabasco wetlands 81 / 64 / 73. Stretch only.

## 2. Story and scope

**Story (v0.5, D-16): "Mexico City is sinking, and NISAR measured a year of it."** NISAR helps governments and international organizations recognize and measure a slow natural hazard before it becomes a disaster. Our proof of concept (`poc/mexico_city_sinking/`) adds up the 27 consecutive 12-day GUNW pairs (Nov 11, 2025 to Oct 13, 2026) and finds two sinking bowls: the airport, Nezahualcoyotl and the old Texcoco lakebed in the north-east, and Tlahuac, Chalco and the Xochimilco lakebed in the south-east. The key landmark is "the lake that came back" (new Lake Chalco, Lago de Tlahuac-Xico), whose history comes from cited sources. The stakes are the 2024 Chalco flood, with a team member's family connection if they consent to share it. The flood-priority map ranks places where sinking ground and standing water coincide, as a screening aid, not a forecast. Wording rule: "recognize and measure", never "predict".

Numbers we may use (from the proof of concept, line of sight, PROVISIONAL): up to about 2 cm per month at Nezahualcoyotl; 24 cm per year at the 99th percentile; about 338 km2 moving faster than 10 cm per year, where about 3.2 million people live (WorldPop 2020). The sign is inferred from where the motion is until T-35 confirms it from the product specification.

| Tier | What ships | Deadline |
|---|---|---|
| **1, must ship** | Map with GCOV layers (HH, HV, HH/HV composite), swipe, **ground-motion layer (year total, line of sight)**, **flood-priority map (T-34)**, 7 landmark cards with real numbers, polarization explainer, provisional label, sources page. Static, on Azure, with bundled sample data. | Core by Sun 1:00 AM (G2); text pieces by the 8:00 AM freeze |
| **2** | GCOV and ground-motion time slider (monthly frames), time-series chart per landmark, guided tour (T-18). | By the 8:00 AM freeze |
| **3** | Cancelled in v0.5 (D-18). | |

If we fall behind, cut in this order: the guided tour, the time slider, the per-landmark chart, the HH/HV composite. Never cut: real NISAR data on the map, the ground-motion layer, the flood-priority map, the landmark cards, the polarization explainer, the provisional label, the sources.

## 3. Gates

| Gate | Time | Question | If no |
|---|---|---|---|
| G1 | Sat 4:30 PM | Can we read our window out of a remote GCOV file and a remote GUNW file? | **Passed.** Elias read both track 19 / frame 11 PROVISIONAL windows over HTTPS (T-01): GCOV HH and HV in 31.9 s and 14 MB, GUNW unwrapped phase in 21.0 s and 10 MB. The pre-approved fallback downloads are cancelled. |
| GS | Sat 5:30 PM | Has the team chosen the story from the data (T-25)? | Default story: surface change in GCOV. Ground motion stays a Tier 2 option behind G2. **As of 6:25 PM no decision is recorded, so the default applies until the team records one.** |
| Checkpoint | Sat 9:30 PM | Progress report, not a gate. Is the core of Tier 1 live on the public URL with real data (GCOV layers, swipe, landmark cards; text may still be placeholders)? Each person says what is left for G2. | Nothing is cut here. Problems found go into block E. |
| G2 | Sun 1:00 AM | Go or no-go, before anyone sleeps. **Redefined in v0.5:** are the map with radar layers, the ground-motion layer, the flood-priority map and the 7 landmark cards working end to end on the live URL? The explainer, provisional label and sources page may land by the 8:00 AM freeze. | No: Sunday 7:00 to 8:00 AM finishes the missing core piece only; the tour and slider are cut. |
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

What was moved off Elias, per the workload rule: ground-motion math (Eduardo), landmark sampling and validator (Zainab), fetch-job babysitting (Diego; the rendering helpers went back into T-10 when T-11 was cancelled in v0.4), all docs (Zainab), demo and page (Monica). Elias keeps pipeline, API, deploy, integration.

Coding exercises that are real project code:

| Person | Exercise | How to check |
|---|---|---|
| Zainab | T-08 write the sample manifest by hand from the contract, then `validate_manifest.py` | `pytest pipeline/tests/test_validate.py` passes; a broken fixture fails |
| Zainab | T-16 complete `sample_at_points()` | Given tests with a synthetic raster pass |
| Zainab | T-31t write tests for `displacement.py` and explain the module in `docs/ARCHITECTURE.md` | Tests pass; Eduardo reads the explanation |
| Diego | ~~T-11~~ cancelled in v0.4: no starter files or tests were ever assigned, and T-10 does its own rendering | |
| Diego | T-12, T-13 build the layer controls against the sample manifest | Works with sample data before real data exists |
| Diego | T-59t follow the README on a clean clone | App runs with no help; gaps filed to Zainab |

## 5. Interfaces that keep five people out of each other's way

**Folder ownership.** You edit your own folders. To change someone else's, ask them or put it in your status file.

| Path | Owner |
|---|---|
| `pipeline/` (except below), `api/`, `.github/`, root config files | Elias |
| `pipeline/science/` | Eduardo |
| `pipeline/validate_manifest.py`, `pipeline/landmarks.py`, `pipeline/tests/` | Zainab |
| `pipeline/render.py` (not created; T-11 cancelled) | nobody |
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

1. Read the unwrapped phase, coherence, connected-components, and ionosphere layers for our window (80 m pixels) from each of the 27 pairs, starting with Nov 11 to Nov 23, 2025. The Oct 30 to Nov 11, 2025 pair is not used (D-13).
2. Mask pixels with low coherence or no connected component. Water and vegetation will drop out. That is expected.
3. Check in the spec whether the unwrapped phase already has the ionosphere correction applied. Apply it if not. In the local file the ionosphere layer is large (tens of centimeters when converted), so this step cannot be skipped. Then remove a best-fit tilt across the box from each pair.
4. Subtract the median phase of a reference area that is known to be stable (a rock outcrop named in the literature, not a guess).
5. Convert phase to centimeters along the line of sight using the wavelength stored in the file. Confirm the sign convention against the JPL image: the airport area must come out as moving away from the satellite.
6. Add the 27 pairs in order to get cumulative movement per date. Divide by elapsed years for a rate map.
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
| T-04 | **Done Sat 6:06 PM (PR #4).** CI on PRs, and deploys to Azure Static Web Apps and Cloudflare Pages from `main`; both deploy jobs passed on the next run. Left over: put both public URLs in the README (Elias, 5 min), then T-55. | Elias (backup Eduardo) | B | 1.25 | Public Azure URL and fallback URL both serve main; both URLs in README |
| T-05 | **Done.** Organizer answers are in section 13 and D-14: Azure hosting qualifies, the pitch is 4 minutes plus questions, no edits after 1:30 PM for the in-person awards. | Monica | A | 0.25 | Answers logged in `DECISIONS.md` |
| T-06 | Read NASA "What is SAR" and the JPL Mexico City article; draft a 150-word plain-language explainer of radar, HH, and HV | Monica (Eduardo reviews) | A | 1.0 | Draft in `content/`; every claim has a source ID |
| T-07 | README skeleton, MIT `LICENSE`, `docs/SOURCES.md`, keep `docs/AI_USAGE.md` current | Zainab | A | 1.0 | A stranger can see what the project is and how it will run; license present |
| T-08 | Sample dataset in `app/public/data/sample/` written by hand from the contract, then `validate_manifest.py` with tests | Zainab | A | 1.5 | Sample fixture merged by 4:00 PM (unblocks all front-end work); validator passes on it and fails on a broken copy |
| T-09 | Map screen: basemap, image layers from the manifest, layer and date switching from state, swipe compare, attribution | Eduardo (backup Monica) | A, B | 2.5 | Sample layers sit in the right place; swipe works with mouse and touch; no API key in the code |
| T-10 | GCOV build: crops to dB, reproject, WebP, composite, `manifest.json` for the two chosen dates. **Merged Sat 6:17 PM (PR #5) with the dates Oct 30, 2025 and Oct 13, 2026.** The first date is now excluded, see T-10b. | Elias (backup Eduardo) | B, C | 2.5 | One command rebuilds `app/public/data/mexico_city/`; validator passes; folder under 30 MB |
| T-10b | Rebuild the Mexico City bundle without Oct 30, 2025 (D-13): two dates of release P05023 between Nov 11, 2025 and Oct 13, 2026, one dry-season and one rainy-season. One command: `python pipeline/build_manifest.py --dates <d1> <d2>`. Until this merges, the live site shows the excluded date. | Elias (backup Eduardo) | C | 0.25 | No `2025-10-30` anywhere under `app/public/data/mexico_city/`; validator passes; live before the 7:30 PM talk |
| ~~T-11~~ | **Cancelled in v0.4 (RB-D02).** `render.py` helpers as an exercise: nobody was assigned to write the starter and tests, and T-10 already renders. | Diego | | | |
| T-12 | Layer switcher and legend | Diego (backup Zainab) | B, D | 2.0 | Lists layers from the manifest, shows units, range, and the provisional note; usable at 375 px wide |
| T-13 | Time slider with play and pause for the GCOV and ground-motion frames. No Oct 30, 2025, Dec 5, 2025 or Apr 16, 2026 frame (D-13, D-17). | Diego | G | 1.5 | Scrubs frames of the active layer; shows the date; hidden when a layer has one frame |
| T-14 | Landmark panel: list, select, fly to, card with "radar shows" and "we infer" kept separate | Zainab (backup Monica) | B, C | 2.0 | Works from `landmarks.json`; selecting on the map and in the list stay in sync |
| T-15 | Time-series chart per landmark, from `los_displacement_cm` in `landmarks.json` (values from `poc/mexico_city_sinking/landmark_series_los_cm.csv`) | Zainab | G | 1.5 | Axis titles with units, gaps for missing dates, provisional note, readable on a phone |
| ~~T-16~~ | **Cancelled in v0.5 (D-18).** The proof of concept's landmark CSV replaces `sample_at_points()`. | Zainab | | | |
| T-17 | Project name and tagline for the v0.5 story (Monica leans "Project Lago") | Monica | E | 0.5 | Team agrees by 12:30 AM |
| T-18 | Intro screen and guided walkthrough driven by `content/story/mexico_city.json` | Monica (backup Zainab) | B to D | 3.0 | A first-time visitor understands the point in 60 seconds; "explore freely" exits the tour |
| T-19 | Landmark cards for 7 places (new Lake Chalco, Tlahuac, Nezahualcoyotl, airport, Centro Historico, Angel de la Independencia, Chalco) with real numbers from the proof of concept and a source for every claim | Monica writes, Eduardo reviews | E, F | 1.5 + 0.5 | `landmarks.json` on `main` has the 7 cards before 1:00 AM; no unsourced claim |
| T-20 | Typed API on Azure Functions: health, regions, manifest, landmarks | Elias (backup Zainab) | D, E | 1.0 | Four routes live on the Azure URL; error shape per contract; app still works with the API off |
| ~~T-21~~ | **Cancelled in v0.5 (D-18).** Borough layer. | Diego | | | |
| T-22 | Integration pass for the 9:30 PM checkpoint | Elias, everyone tests | D | 0.75 | Live URL shows real GCOV with swipe, landmarks, and tour; no console errors; works on one phone |
| T-23 | Explainer cards (polarization; shows vs. infer), provisional badge, mobile pass | Monica | E, F | 1.5 | Badge visible on every data view; live by G2 (Sun 1:00 AM) |
| T-24 | Sources page in the app, generated from the manifest `sources` and `SOURCES.md` | Zainab | E, F | 0.5 | Every dataset, library, and image is listed with a link; live by G2 (Sun 1:00 AM) |
| T-30 | Tier 2: fetch the GUNW windows. All 28 pairs may be fetched, but only the 27 from Nov 11, 2025 on are used (D-13). | Diego runs, Elias backs up | C (runs during the talk) | 1.0 | Crops in `data/interim/`; failures listed in the status file |
| T-31 | Ground motion from the GUNW chain. **Done by the proof of concept** (`poc/mexico_city_sinking/sinking_poc.py`, 27 pairs, shared reference, ionosphere correction, component re-attachment, gap filling). Move it to `pipeline/science/displacement.py` after the freeze if time allows. | Eduardo | done | | Output `data/Mexico_City/displacement_cumulative.npz` |
| T-32 | Sanity check. **Done:** bowls where JPL places them; 2.0 cm per month at Nezahualcoyotl against JPL's "more than 2 centimeters per month"; control in the hills -2.2 cm over the year (about 2 cm uncertainty). Details in `poc/mexico_city_sinking/README.md`. | Eduardo | done | | |
| T-33 | Ground-motion layer in the build: year-total WebP (and monthly frames if time allows) from the proof of concept output, with units, sign, reference area and granule IDs in the manifest. Elias runs the script himself on the 27 crops (about 20 s). | Elias | E, F | 1.0 | Layer live on the URL before 1:00 AM; validator passes |
| T-34 | **Flood-priority map (PR #20, kept in v0.5).** Combines the line-of-sight sinking rate with dark-in-both-HH-and-HV months from the monthly GCOV crops, ranked at 500 m; hotspots endpoint in the API. Uses the real rate raster from T-33. Labeled a screening aid built on PROVISIONAL data, not a flood forecast. Water months exclude Dec 5, 2025 and Apr 16, 2026 (D-17). Old T-34 (show new layers in the app) is folded into T-12, T-13 and T-15. | Elias (backup Eduardo) | F | 1.5 | Layer and hotspots live before 1:00 AM; score weights documented in `docs/FLOOD_PRIORITY.md`; 2024 flood-zone checks reported |
| T-35 | Confirm the GUNW unwrapped-phase sign convention in the product specification (JPL D-102272) so the app can say "sinking" in words; also look up the incidence angle for a rough vertical conversion | Eduardo | F | 0.5 | Line in `DECISIONS.md` with the page reference |
| ~~T-40+~~ | **Cancelled in v0.5 (D-18).** Tier 3. | | | | |
| T-50 | Demo deck, **7 slides at most** | Monica (backup Zainab) | E, H | 2.5 | Draft with placeholders by Sat 11:30 PM; final by Sun 10:30 AM; public link opens in a private window |
| T-51 | Text for all 8 project page fields in `docs/submission/PROJECT_PAGE.md` | Monica, Eduardo reviews | F, H | 1.5 + 0.5 | Draft Sat night; reviewed by Sun 9:30 AM |
| T-52 | References: every dataset, tool, library, image, and text source | Zainab | all | 0.75 | `SOURCES.md` complete at G5; pasted into the form field |
| T-53 | SI disclosure text; check every AI-written file has its header; confirm no unmarked AI imagery | Zainab | H | 0.5 | Disclosure matches `AI_USAGE.md` |
| T-54 | Make the repo public after a secrets scan (Eduardo has the rights) | Eduardo, Elias runs the scan | H (earlier if agreed) | 0.25 | Repo public; no credentials in history |
| T-55 | FortiGuard web filter classification request for the live URL | Elias | C | 0.2 | Submitted the evening the URL exists |
| T-56 | Open every submission link in a private window | Zainab | G5 | 0.25 | Demo, project, repo all open with no login |
| T-57 | Live pitch script and two rehearsals. The pitch is 4 minutes, then judges' questions. | Monica leads, all | I | 1.0 | Runs 3:45 or less on a timer, twice |
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

Live pitch: **4 minutes, then a few minutes of judges' questions** (organizers, D-14). We may present whatever we like: the app, the deck, or both. Plan: 30 seconds on the problem, 2 minutes live in the app following the tour, 45 seconds on how it works and what is provisional, 30 seconds on what comes next, 15 seconds spare. One speaker and one driver. Every member can answer "what does HH vs. HV show?" and "why is this provisional?".

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

Answered at 6:20 PM (plan v0.4, D-13 to D-15):

- G1 passed. The fallback downloads are cancelled.
- The Oct 30, 2025 acquisition is dropped from every layer and frame because of measurement errors (RB-D01).
- T-11 is cancelled. T-04 and T-05 are done.
- Organizers on Azure: "as long as your team has some usage of Microsoft Azure that you can talk about on their podcast if you win, you're good to go". Hosting on Azure Static Web Apps counts.
- Organizers on the pitch: 4 minutes at local judging, with a few minutes for judges' questions. We can present the app, the 7-slide deck, or a 30-second video. For global judging the Project Demo field must be the 7-slide deck or the 30-second video, and the page must be submitted by 11:59 PM CT.
- No edits after 1:30 PM for the in-person awards. What is on the project page at 1:30 PM is final for local judging.

Answered at 11:30 PM (plan v0.5, D-16 to D-18): the story is Mexico City sinking, measured with NISAR; the flood-priority map stays in; the 1:00 AM gate is the core end to end; Dec 5, 2025 and Apr 16, 2026 are dropped from GCOV frames and water counts; Venezuela, T-10c, T-16, T-21 and Tier 3 are cancelled; T-16 is no longer Zainab's.

Still open:

1. **The personal connection.** Which member, which place, and their consent to share it on a public page.
2. **The sign** (T-35).

Earlier open items, now closed:

1. **The story.** GS passed at 5:30 PM with no decision recorded. Until the team records one, the default from section 3 applies: surface change in GCOV. With Oct 30, 2025 dropped, that means change within Nov 2025 to Oct 2026, not year over year.
2. (closed) **Which two dates T-10b uses.** Elias picks from Diego's 29-date pictures unless the team says otherwise.

Timeline note: kickoff slipped from 2:00 to 3:10 PM. Gate times are unchanged, so block A is 70 minutes instead of two hours. T-02 and T-08 merge by 4:00 PM. If T-01 is not finished at 4:30 PM, G1 moves to 5:00 PM and nothing else moves.

## 14. Start here

**Every person, once:** create `CLAUDE.local.md` in the repo root (it is git-ignored) with three lines: `name:`, `role:`, `backup for:`. Copy your role and backups from section 4. Then paste the short prompt from [COORDINATION.md](COORDINATION.md) section 7 into your Claude Code session, followed by your own lines below.

**Everyone, first 20 minutes:** read [challenge/README.md](challenge/README.md), the [decision memo](DECISION_MEMO.md), your rows in sections 4, 5, and 9, and NASA's "What is SAR" page. Put the AI-generation header on every file an agent writes.

Lines to add after the short prompt:

- **Elias:** "I own `pipeline/` (except `science/`, `render.py`, `landmarks.py`, `validate_manifest.py`, `tests/`), `api/`, `.github/`, `app/src/types/`, `app/src/lib/`, and the data contract. My first task is T-01, the remote-read probe that decides gate G1 at 4:30 PM; start from the reading code in `pipeline/quicklook.py`. Then T-03, and T-04 before 6:00 PM. Never put credentials in the repo. If a Python package fails to install, switch to Python 3.12 instead of debugging."
- **Diego:** "I own `pipeline/render.py`, `app/src/components/layers/`, and `app/src/components/time/`. My first task is T-25: make quick-look pictures with `pipeline/quicklook.py` and collect what is visible for each story candidate in the decision memo. Explain each step to me as we go; I am new to this. Do not start any download over 1 GB without telling me so I can ask Eduardo. After the 4:30 PM standup: T-30, then T-12 against the sample data (T-11 was cancelled in v0.4)."
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
