// View options (UI proof of concept, branch diego/ui-poc, not for merge): the three things the
// store could already do but had no control on the page: swipe compare against a second layer,
// the map under the radar (streets or satellite), and how see-through the radar image is.
// It only reads the shared store and calls its actions (setCompare, setBasemap, setLayerOpacity);
// it never touches the map and imports no other component (docs/PLAN.md section 5).
// Owner: Diego (app/src/components/layers/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useAppStore } from '../../state/store';
import type { Basemap } from '../../state/store';
import './layers.css';

const BASEMAPS: { id: Basemap; label: string }[] = [
  { id: 'streets', label: 'Streets' },
  { id: 'satellite', label: 'Satellite' },
];

export default function ViewOptions() {
  const layers = useAppStore((s) => s.manifest?.layers);
  const compareLayerId = useAppStore((s) => s.compareLayerId);
  const basemap = useAppStore((s) => s.basemap);
  const opacity = useAppStore((s) => s.layerOpacity);
  const setCompare = useAppStore((s) => s.setCompare);
  const setBasemap = useAppStore((s) => s.setBasemap);
  const setLayerOpacity = useAppStore((s) => s.setLayerOpacity);

  if (!layers || layers.length === 0) return null;
  const percent = Math.round(opacity * 100);

  return (
    <div className="view-options">
      <label className="view-options__row">
        <span className="view-options__label">Swipe against</span>
        <select
          className="view-options__select"
          value={compareLayerId ?? ''}
          onChange={(e) => setCompare(e.target.value === '' ? null : e.target.value)}
        >
          <option value="">Nothing (swipe off)</option>
          {layers.map((layer) => (
            <option key={layer.id} value={layer.id}>
              {layer.title}
            </option>
          ))}
        </select>
      </label>

      <fieldset className="view-options__row view-options__basemap">
        <legend className="view-options__label">Map underneath</legend>
        <div className="segmented">
          {BASEMAPS.map((b) => (
            <label key={b.id} className={b.id === basemap ? 'segmented__item is-active' : 'segmented__item'}>
              <input
                type="radio"
                name="basemap"
                value={b.id}
                checked={b.id === basemap}
                onChange={() => setBasemap(b.id)}
              />
              <span>{b.label}</span>
            </label>
          ))}
        </div>
      </fieldset>

      <label className="view-options__row">
        <span className="view-options__label">
          Radar opacity <output className="view-options__value">{percent}%</output>
        </span>
        <input
          className="view-options__range"
          type="range"
          min={0}
          max={100}
          step={5}
          value={percent}
          onChange={(e) => setLayerOpacity(Number(e.target.value) / 100)}
        />
      </label>
    </div>
  );
}
