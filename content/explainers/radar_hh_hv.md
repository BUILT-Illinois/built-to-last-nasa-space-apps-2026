<!-- Drafted with AI assistance (Claude Code) for Monica Venancio, T-06. Needs Eduardo's review before it ships. -->

# T-06 draft: radar, HH, and HV in plain language

Status: **draft, waiting for Eduardo's review.** Target 150 words; the text below is 151 words, not counting the source tags.
Source IDs: **S1** = NASA Earthdata "What is SAR", **S2** = NASA/JPL Mexico City article. Both are in the decision memo table (full links at the bottom).

---

## Radar brings its own light

A radar satellite does not wait for sunlight. It sends out a pulse of energy and records how much comes back after it hits the ground [S1]. That lets it make images night or day, in any weather [S1]. Clouds and vegetation that get in the way of optical cameras do not stop NISAR's L-band radar [S2].

NISAR is a joint mission of NASA and the Indian Space Research Organisation (ISRO) [S2]. NASA's JPL provided its L-band radar [S2]. L-band has a long wavelength that reaches deeper into a tree canopy [S1].

Radar can send and receive its waves horizontally (H) or vertically (V) [S1]. **HH** means sent H, received H [S1]. HH is most sensitive to *double bounce*, which happens at buildings, tree trunks, and flooded vegetation [S1]. **HV** is a cross-polarized signal [S1]. It is most sensitive to *volume scattering* from the leaves and branches of a canopy [S1].

---

## Claim check (for Eduardo)

| # | Claim in the text | Source | Exact words on the page | Status |
|---|---|---|---|---|
| 1 | Sends a pulse, records how much comes back | S1 | "an instrument sends out a pulse of energy"; "records the amount of that energy reflected back after it interacts with Earth" | Source in memo table, **claim not yet a row** |
| 2 | Night or day, any weather | S1 | "night or day, regardless of weather conditions" | Source in memo table, **claim not yet a row** |
| 3 | Clouds and vegetation that block optical sensors do not stop L-band | S2 | "unhindered by clouds or vegetation that impede optical sensors and higher-frequency radars" | Source in memo table, **claim not yet a row** |
| 4 | NASA and ISRO joint mission | S2 | "A joint mission developed by NASA and the Indian Space Research Organisation (ISRO)" | Source in memo table, **claim not yet a row** |
| 5 | NASA JPL provided the L-band radar | S2 | "provided the satellite's L-band SAR and antenna reflector" | Source in memo table, **claim not yet a row** |
| 6 | L-band reaches deeper into a canopy | S1 | "which enables it to penetrate more deeply through a tree canopy" | Source in memo table, **claim not yet a row** |
| 7 | H and V; HH = sent H, received H | S1 | "The horizontal polarization is indicated by the letter H, and the vertical polarization is indicated by the letter V"; "emitted in horizontal (H) and received in horizontal (H) would be indicated HH" | Source in memo table, **claim not yet a row** |
| 8 | HH most sensitive to double bounce (buildings, trunks, flooded vegetation) | S1 | "caused by buildings, tree trunks, or inundated vegetation"; "most sensitive to an HH polarized signal" | **In memo table** |
| 9 | HV is cross-polarized, most sensitive to canopy volume scattering | S1 | "Volume scattering caused by the leaves and branches in a forest canopy"; "most sensitive to cross-polarized data like VH or HV" | **In memo table** |

## Flags: things I left out on purpose

1. **The definition of HV is missing.** S1 defines HH and VH, but never says in words what HV is. By the page's naming pattern, HV is "sent H, received V", but nothing in the memo table says so. That is why the text only calls HV "cross-polarized". Fix: add a source for the HV definition (the NISAR Data User Guide GCOV page is a likely place), then add "HV means sent H, received V."
2. **Wavelength numbers disagree.** S1 says L-band is "about 23 cm" (and its table gives 15 to 30 cm for the band). Plan section 1 says our own GCOV file stores 24.2 cm. I left the number out. Eduardo should decide which one we quote, and the file value needs a source row if we use it.
3. **"Calm water looks dark, cities look bright" is not in our sources.** S1 does not say it. It would help a first-time visitor read the map, so it is worth finding a source (NISAR Data User Guide or ASF).
4. **What HH and HV show over Mexico City specifically** (lakebed, wetlands, built-up land) is inference until T-25 and the story decision. It belongs in the landmark cards (T-19) as "we infer", not in this explainer.
5. **Rows to add to the memo table** (Eduardo's file): claims 1 to 7 above. They come from sources that are already listed. The rule says the claim itself must be a row.

## Sources

- S1: NASA Earthdata, "Synthetic Aperture Radar (SAR)", <https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar>, read Nov 14, 2026.
- S2: NASA/JPL, "US-Indian Space Mission Maps Extreme Subsidence in Mexico City", Apr 29, 2026, <https://www.jpl.nasa.gov/news/us-indian-space-mission-maps-extreme-subsidence-in-mexico-city/>, read Nov 14, 2026.
