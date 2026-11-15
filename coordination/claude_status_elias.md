Elias status (12:57 AM Sun)
DONE: API live on Azure and Cloudflare. Merged #13, #15, #17, #18, #19. 12 months of radar frames processed.
SIGNED OFF: RBF-03 sign mismatch (Elias, 12:57 AM). LOS positive = away from the satellite, matching Eduardo's #26 files. DATA_CONTRACT.md updated on the PR #24 branch (f1b668d). Still pending: Eduardo's DECISIONS.md line and T-35 confirmation.
OPEN PRs: #24 sinking ingest (draft, waits on raster + T-32). #22 smoke checks (CI green). #28 landmark backscatter series (CI green). #29 AI usage audit (docs only).
PARKED: T-34 flood map (Eduardo, 11:05 PM). PR #20 stays a draft.
BLOCKED: citywide sinking layer. The first los_rate_cm_per_year.tif from Eduardo was invalid (uint32, no CRS). Waiting on the real float32 EPSG:32614 file, zipped. The ingest runs as soon as it lands.
REVIEWS: #26 OK'd by Diego.

G2 CHECKLIST (1 AM)
Go = map + sinking + landmarks working end to end.
• Done: both sites load with zero console errors. The API is live.
• Needed: map with radar frames and time slider (T-09, Eduardo)
• Needed: citywide sinking layer (Elias). Ingest ready, waiting on a valid raster. Diego building the toggle and legend.
• Needed: Monica's 7 landmark cards served by the API (PR #21 into landmarks.json)
• Needed: story locked. Option: "Mexico City is sinking up to 2 cm a month, and the old lake is coming back. NISAR lets us watch it happen."
• Can wait until the 8 AM freeze: guided tour (PR #21)
• Caracas: dropped at the 11:30 PM cutoff
