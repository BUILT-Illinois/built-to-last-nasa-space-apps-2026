// The draggable divider of the swipe compare. Works with mouse, touch, pen, and keyboard.
// Owner: Eduardo (app/src/map/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useRef } from 'react';
import type { KeyboardEvent, PointerEvent } from 'react';

type Props = {
  /** Divider position as a fraction of the map width, 0 to 1. */
  position: number;
  onChange: (position: number) => void;
  leftLabel: string;
  rightLabel: string;
};

const KEY_STEP = 0.05;
const clamp = (x: number) => Math.min(1, Math.max(0, x));

export default function SwipeHandle({ position, onChange, leftLabel, rightLabel }: Props) {
  const dragging = useRef(false);

  const moveTo = (e: PointerEvent<HTMLDivElement>) => {
    const parent = e.currentTarget.parentElement;
    if (!parent) return;
    const rect = parent.getBoundingClientRect();
    onChange(clamp((e.clientX - rect.left) / rect.width));
  };

  const onPointerDown = (e: PointerEvent<HTMLDivElement>) => {
    dragging.current = true;
    e.currentTarget.setPointerCapture(e.pointerId);
    e.preventDefault();
  };
  const onPointerMove = (e: PointerEvent<HTMLDivElement>) => {
    if (dragging.current) moveTo(e);
  };
  const onPointerUp = (e: PointerEvent<HTMLDivElement>) => {
    dragging.current = false;
    e.currentTarget.releasePointerCapture(e.pointerId);
  };
  const onKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'ArrowLeft') onChange(clamp(position - KEY_STEP));
    else if (e.key === 'ArrowRight') onChange(clamp(position + KEY_STEP));
    else if (e.key === 'Home') onChange(0);
    else if (e.key === 'End') onChange(1);
    else return;
    e.preventDefault();
  };

  return (
    <div
      className="swipe-handle"
      style={{ left: `${position * 100}%` }}
      role="slider"
      tabIndex={0}
      aria-label={`Swipe between ${leftLabel} (left) and ${rightLabel} (right)`}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={Math.round(position * 100)}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={onPointerUp}
      onKeyDown={onKeyDown}
    >
      <div className="swipe-handle__line" />
      <div className="swipe-handle__grip" aria-hidden="true">
        ‹ ›
      </div>
    </div>
  );
}
