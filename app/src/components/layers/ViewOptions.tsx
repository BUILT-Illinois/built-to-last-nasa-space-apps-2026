// View options: the things the store could already do but had no control on the page: which date
// is shown, swipe compare against a second layer or a second date, the map under the radar
// (streets or satellite), and how see-through the radar image is.
// It only reads the shared store and calls its actions (setDate, setCompare, setCompareDate,
// setBasemap, setLayerOpacity); it never touches the map and imports no other component
// (docs/PLAN.md section 5).
// Owner: Diego (app/src/components/layers/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { selectActiveLayer, selectCompareLayer, useAppStore } from '../../state/store';
import type { Basemap } from '../../state/store';
import type { Layer } from '../../types/manifest';
import './layers.css';

const BASEMAPS: { id: Basemap; label: string }[] = [
  { id: 'streets', label: 'Streets' },
  { id: 'satellite', label: 'Satellite' },
];

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** "2025-11-11" reads as "Nov 11, 2025". Anything else is shown as the manifest gives it. */
function formatDate(iso: string): string {
  const parts = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  const month = parts ? MONTHS[Number(parts[2]) - 1] : undefined;
  return parts && month ? `${month} ${Number(parts[3])}, ${parts[1]}` : iso;
}

/** Keep an index inside the layer's frames, the same way the store does for the map. */
function clampIndex(layer: Layer, index: number): number {
  return Math.min(Math.max(0, index), layer.frames.length - 1);
}

/** One date picker: the frames of a layer, by date. */
function DateSelect(props: { label: string; layer: Layer; index: number; onChange: (index: number) => void }) {
  return (
    <label className="view-options__row">
      <span className="view-options__label">{props.label}</span>
      <select
        className="view-options__select"
        value={props.index}
        onChange={(e) => props.onChange(Number(e.target.value))}
      >
        {props.layer.frames.map((frame, i) => (
          <option key={frame.date} value={i}>
            {formatDate(frame.date)}
          </option>
        ))}
      </select>
    </label>
  );
}

export default function ViewOptions() {
  const layers = useAppStore((s) => s.manifest?.layers);
  const activeLayer = useAppStore(selectActiveLayer);
  const compareLayer = useAppStore(selectCompareLayer);
  const dateIndex = useAppStore((s) => s.dateIndex);
  const compareDateIndex = useAppStore((s) => s.compareDateIndex);
  const basemap = useAppStore((s) => s.basemap);
  const opacity = useAppStore((s) => s.layerOpacity);
  const setDate = useAppStore((s) => s.setDate);
  const setCompare = useAppStore((s) => s.setCompare);
  const setCompareDate = useAppStore((s) => s.setCompareDate);
  const setBasemap = useAppStore((s) => s.setBasemap);
  const setLayerOpacity = useAppStore((s) => s.setLayerOpacity);

  if (!layers || layers.length === 0) return null;
  const percent = Math.round(opacity * 100);
  const comparing = compareLayer !== undefined;
  // The same frames the map draws: the left side uses dateIndex, and the right side uses its own
  // index, or the left one when it has none.
  const leftIndex = activeLayer ? clampIndex(activeLayer, dateIndex) : 0;
  const rightIndex = compareLayer ? clampIndex(compareLayer, compareDateIndex ?? dateIndex) : 0;

  const chooseCompare = (layerId: string) => {
    if (layerId === '') {
      setCompare(null);
      return;
    }
    // The same layer on both sides only shows something with two different dates, so the right
    // side starts on the last date (or the first, if the left side is already on the last).
    if (activeLayer && layerId === activeLayer.id && activeLayer.frames.length > 1) {
      const last = activeLayer.frames.length - 1;
      setCompare(layerId, leftIndex === last ? 0 : last);
      return;
    }
    setCompare(layerId);
  };

  return (
    <div className="view-options">
      {activeLayer && activeLayer.frames.length > 1 && (
        <DateSelect
          label={comparing ? 'Date, left side' : 'Date'}
          layer={activeLayer}
          index={leftIndex}
          onChange={setDate}
        />
      )}

      <label className="view-options__row">
        <span className="view-options__label">Swipe against</span>
        <select
          className="view-options__select"
          value={compareLayer?.id ?? ''}
          onChange={(e) => chooseCompare(e.target.value)}
        >
          <option value="">Nothing (swipe off)</option>
          {layers.map((layer) => (
            <option key={layer.id} value={layer.id}>
              {layer.id === activeLayer?.id && layer.frames.length > 1 ? 'This layer, another date' : layer.title}
            </option>
          ))}
        </select>
      </label>

      {compareLayer && compareLayer.frames.length > 1 && (
        <DateSelect label="Date, right side" layer={compareLayer} index={rightIndex} onChange={setCompareDate} />
      )}

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
