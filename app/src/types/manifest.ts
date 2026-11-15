// TypeScript types for the data contract v0.1 (docs/DATA_CONTRACT.md).
// Owner: Elias (app/src/types/). Stub written in T-02 by Eduardo's session; Elias may reshape it.
// Shared with api/. Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.

/** [west, south, east, north] in degrees, WGS84. */
export type BBox = [number, number, number, number];

/** [lon, lat] in degrees, WGS84. */
export type LngLat = [number, number];

/** YYYY-MM-DD, UTC. */
export type IsoDate = string;

export type LayerKind = 'backscatter' | 'composite' | 'change' | 'displacement' | 'soil_moisture';

export type Polarization = 'HH' | 'HV' | 'HH+HV' | null;

export type Direction = 'ASCENDING' | 'DESCENDING';

export interface Region {
  id: string;
  name: string;
  bbox: BBox;
  center: LngLat;
  zoom: number;
}

export interface Colormap {
  name: string;
  /** In the layer's units; shown on the legend. */
  min: number;
  max: number;
}

export interface Frame {
  /** For displacement layers this is the end date. */
  date: IsoDate;
  /** Displacement layers only: start date of the cumulative movement. */
  since?: IsoDate;
  /** Relative to the folder holding manifest.json. */
  image: string;
  /** Exact NISAR granule names, so any image traces back to NASA's archive. */
  granules: string[];
  track: number;
  frame: number;
  direction: Direction;
}

export interface Layer {
  id: string;
  title: string;
  kind: LayerKind;
  product: string;
  polarization: Polarization;
  units: string;
  /** Image edges, [west, south, east, north]. Images are in Web Mercator. */
  bounds: BBox;
  colormap: Colormap;
  description: string;
  caveats: string[];
  frames: Frame[];
}

export interface VectorLayer {
  id: string;
  title: string;
  file: string;
  /** An id from Manifest.sources. */
  source: string;
}

export interface Source {
  id: string;
  title: string;
  url: string;
  license: string;
}

export interface Manifest {
  schemaVersion: string;
  generatedAt: string;
  generatedBy: string;
  region: Region;
  /** e.g. "PROVISIONAL". */
  dataMaturity: string;
  layers: Layer[];
  vectors: VectorLayer[];
  sources: Source[];
}

export interface SeriesPoint {
  date: IsoDate;
  /** null means no valid data for that date; charts show a gap, not a zero. */
  value: number | null;
}

export interface LandmarkSeries {
  hh_db?: SeriesPoint[];
  hv_db?: SeriesPoint[];
  water_months?: { count: number; valid_months: number; provisional: true };
  /** Cumulative line-of-sight movement since the first date; negative = away from the satellite. */
  los_displacement_cm?: SeriesPoint[];
}

export interface Landmark {
  id: string;
  name: string;
  lon: number;
  lat: number;
  summary: string;
  radarShows: string;
  weInfer: string;
  drivers: { human: string | null; natural: string | null };
  sourceIds: string[];
  series?: LandmarkSeries;
}

export interface LandmarksFile {
  schemaVersion: string;
  regionId: string;
  landmarks: Landmark[];
}
