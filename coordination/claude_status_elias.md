Elias status (10:30 PM Sat):

DONE
• T-20 API live on Azure and Cloudflare: health, regions, manifest (12 dates x 3 layers), landmarks (0 entries until Monica's file lands). Unknown regions return JSON 404.
• Merged: #13 API, #15 retry, #17 favicon, #18 hard-kill wrapper (Diego's code), #19 config-driven regions. A new region takes about 7 to 12 min.
• Landmark frequency-A batch done (6 points, 2 dates, 0 failures). The April 16 frame checked clean.

PROPOSED, NEEDS EDUARDO'S OK
• T-34 flood-priority map (draft PR #20, unmerged). It scores 500 m cells on sinking rate plus how often water persists. It's a screening map, not a flood prediction. Water half built: New Lake Chalco 7/12 months, dry city controls 0/12. Misses small ponds (Bosque de Tláhuac 0/12).
• Doesn't touch the core sinking + lake story. Can be parked with no impact.

BLOCKED
• T-34 needs Eduardo's sinking raster: file, units, sign, reference area, GUNW granule IDs.
• Zainab's PRs #6 and #11 wait on her fixes: synthetic sample labeling, README notes.

OPEN
• Caracas stretch goal (Diego, cutoff 11:30 PM). Diego is away right now.
• Story lock by 11:30 PM (Eduardo's call).
