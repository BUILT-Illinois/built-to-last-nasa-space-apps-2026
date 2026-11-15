// Layer switcher (T-12): lists every layer in the loaded manifest by its title and lets the
// user pick the one shown on the map. It only reads the shared store and calls setLayer; it
// never touches the map and imports no other component (docs/PLAN.md section 5).
// A layer that is not in the manifest (for example "sinking" before T-33 lands) is simply not listed.
// Owner: Diego (app/src/components/layers/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useAppStore } from '../../state/store';
import './layers.css';

export default function LayerSwitcher() {
  const manifest = useAppStore((s) => s.manifest);
  const activeLayerId = useAppStore((s) => s.activeLayerId);
  const loadStatus = useAppStore((s) => s.loadStatus);
  const setLayer = useAppStore((s) => s.setLayer);

  if (!manifest) {
    return loadStatus === 'loading' ? (
      <p className="layer-switcher__loading" role="status">
        Loading layers…
      </p>
    ) : null;
  }
  if (manifest.layers.length === 0) return null;

  // Native radio buttons: Tab moves into the group, arrow keys move between layers,
  // and screen readers announce "1 of N" without any extra code.
  return (
    <fieldset className="layer-switcher">
      <legend className="layer-switcher__heading">Layers</legend>
      {manifest.layers.map((layer) => (
        <label
          key={layer.id}
          className={
            layer.id === activeLayerId ? 'layer-switcher__option is-active' : 'layer-switcher__option'
          }
        >
          <input
            type="radio"
            name="active-layer"
            value={layer.id}
            checked={layer.id === activeLayerId}
            onChange={() => setLayer(layer.id)}
          />
          <span>{layer.title}</span>
        </label>
      ))}
    </fieldset>
  );
}
