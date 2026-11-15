// Legend for the active layer (T-12): color ramp with min and max, units, description, caveats,
// a source note, and data-maturity and synthetic-data badges. All science wording comes from
// manifest fields (docs/DATA_CONTRACT.md); this file adds only neutral labels.
// It only reads the shared store; it never touches the map and imports no other component.
// Owner: Diego (app/src/components/layers/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { selectActiveFrame, selectActiveLayer, useAppStore } from '../../state/store';
import './layers.css';

/**
 * The colormap names the pipeline writes, as a CSS gradient plus the color name of each end.
 * A name that is not listed here (for example "rgb", which has no single ramp) shows the numbers
 * without a color bar. The blue-white-red stops match pipeline/ingest_sinking.py (PR #24):
 * min is blue #2166ac, zero is white, max is red #b2182b.
 */
const RAMPS: Record<string, { gradient: string; minColor: string; maxColor: string }> = {
  gray: { gradient: 'linear-gradient(to right, #000000, #ffffff)', minColor: 'black', maxColor: 'white' },
  'los-blue-white-red': {
    gradient: 'linear-gradient(to right, #2166ac, #ffffff, #b2182b)',
    minColor: 'blue',
    maxColor: 'red',
  },
};

/** The sign caveat pipeline/ingest_sinking.py writes; the legend's own sign line replaces it. */
const PIPELINE_SIGN_CAVEAT = 'Positive means away from the satellite.';

/** Legend numbers: at most one decimal, so -12.965582 reads as -13. */
function formatValue(value: number, showPlus: boolean): string {
  const rounded = Number(value.toFixed(1));
  return showPlus && rounded > 0 ? `+${rounded}` : String(rounded);
}

export default function Legend() {
  const dataMaturity = useAppStore((s) => s.manifest?.dataMaturity);
  const synthetic = useAppStore((s) => s.manifest?.synthetic === true);
  const layer = useAppStore(selectActiveLayer);
  // The same frame the map draws: the store clamps a date index that is past the end.
  const frame = useAppStore(selectActiveFrame);

  if (!layer) return null;

  // 'priority' is added to LayerKind by PR #20; compare as text until that merges.
  const kind: string = layer.kind;
  const isGroundMotion = kind === 'displacement';
  const isPriority = kind === 'priority';

  // Ground motion is named by its line-of-sight label from the manifest; this file adds no
  // "sinking" wording of its own.
  const name = isGroundMotion ? (layer.losLabel ?? 'Line-of-sight movement') : layer.title;
  const ramp = RAMPS[layer.colormap.name];
  const granuleCount = frame?.granules.length ?? 0;

  // What the sign means, only when the manifest says so (awaySign). The pipeline writes
  // "positive" (PR #24, T-35). Typed as text so either value is handled without a types change.
  const awaySign: string | undefined = layer.awaySign;
  let sign: string | null = null;
  if (awaySign === 'negative' || awaySign === 'positive') {
    const color = ramp && (awaySign === 'negative' ? ramp.minColor : ramp.maxColor);
    const word = awaySign === 'negative' ? 'Negative' : 'Positive';
    sign = `${word}${color ? ` (${color})` : ''} = moving away from the satellite`;
  }
  // The pipeline also writes the sign as a caveat; do not show it twice. Only that exact
  // sentence is dropped, so a longer caveat that mentions the satellite still shows.
  const caveats = sign ? layer.caveats.filter((c) => c.trim() !== PIPELINE_SIGN_CAVEAT) : layer.caveats;

  return (
    <section className="legend" aria-label="Legend">
      <h2 className="legend__title">
        {name}, {layer.units}
      </h2>

      {(dataMaturity || synthetic) && (
        <p className="legend__badges">
          {dataMaturity && <span className="legend__badge">{dataMaturity} data</span>}
          {synthetic && <span className="legend__badge">Synthetic test data</span>}
        </p>
      )}

      {isPriority && (
        <p className="legend__note">
          Screening aid built on {dataMaturity ?? 'PROVISIONAL'} data. Not a flood forecast.
        </p>
      )}

      {ramp && <div className="legend__ramp" style={{ background: ramp.gradient }} aria-hidden="true" />}
      <div className="legend__range">
        {/* pipeline/ingest_sinking.py caps rates at the ends of the range before coloring, so for
            ground motion the end colors mean "this value or beyond", not a limit of the data. */}
        <span>
          {isGroundMotion && '≤ '}
          {formatValue(layer.colormap.min, isGroundMotion)}
        </span>
        <span>
          {isGroundMotion && '≥ '}
          {formatValue(layer.colormap.max, isGroundMotion)}
        </span>
      </div>
      {sign && <p className="legend__sign">{sign}</p>}

      <p className="legend__description">{layer.description}</p>

      {caveats.length > 0 && (
        <ul className="legend__caveats">
          {caveats.map((caveat) => (
            <li key={caveat}>{caveat}</li>
          ))}
        </ul>
      )}

      <p className="legend__source">
        {layer.referenceArea && <>Reference area: {layer.referenceArea}. </>}
        {frame?.since && (
          <>
            Period: {frame.since} to {frame.date}.{' '}
          </>
        )}
        {synthetic ? (
          // Generated sample data must not be credited to NISAR, whatever manifest.sources lists.
          <>Source: generated test data, not NISAR.</>
        ) : (
          <>
            Source: NISAR {layer.product} (NASA/ISRO)
            {granuleCount > 0 && <>, {granuleCount === 1 ? '1 granule' : `${granuleCount} granules`}</>}.
          </>
        )}
      </p>
    </section>
  );
}
