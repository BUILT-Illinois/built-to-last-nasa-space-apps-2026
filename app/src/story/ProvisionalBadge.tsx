// Data-maturity badge (T-23). The label comes from the manifest, so a synthetic sample region never
// shows "PROVISIONAL". Owner: Monica (app/src/story/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useAppStore } from '../state/store';

/** The badge text for the loaded manifest, or null before any data is loaded. */
function useBadgeLabel(): string | null {
  const maturity = useAppStore((s) => s.manifest?.dataMaturity);
  const synthetic = useAppStore((s) => s.manifest?.synthetic === true);
  if (synthetic) return 'Synthetic test data';
  return maturity ? `${maturity.charAt(0)}${maturity.slice(1).toLowerCase()} data` : null;
}

/** A badge, or a button that looks like one when `onClick` is given. */
export default function ProvisionalBadge({ onClick, title }: { onClick?: () => void; title?: string }) {
  const label = useBadgeLabel();
  if (!label) return null;
  if (!onClick) {
    return (
      <span className="data-badge" title={title}>
        {label}
      </span>
    );
  }
  return (
    <button type="button" className="data-badge data-badge--button" onClick={onClick} title={title}>
      {label}
      <span className="visually-hidden">: what this means</span>
    </button>
  );
}
