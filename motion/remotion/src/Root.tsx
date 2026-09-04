import React from "react";
import { Composition } from "remotion";
import { KeyPointCallout } from "./components/KeyPointCallout";
import { StatReveal } from "./components/StatReveal";
import { TerminalInsert } from "./components/TerminalInsert";
import { LAYOUT } from "./brand";

const FPS = 30;

// Every scene's length comes from --props at render time, because beats.py
// derives it from the real spoken timings. calculateMetadata is what lets one
// composition serve every beat instead of one composition per cut.
const durationFrom =
  (fallback: number) =>
  ({ props }: { props: Record<string, unknown> }) => ({
    durationInFrames: Math.max(
      6,
      Math.round((props.durationInFrames as number) ?? fallback)
    ),
  });

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Full-frame overlays. Rendered WITH alpha and composited over the
          finished video, so they float above both panes. */}
      <Composition
        id="Callout"
        component={KeyPointCallout as never}
        durationInFrames={75}
        fps={FPS}
        width={LAYOUT.width}
        height={LAYOUT.height}
        defaultProps={{
          text: "Zero naira",
          sub: "nine tools, no revenue",
          y: LAYOUT.safeOverlayY,
        }}
        calculateMetadata={durationFrom(75)}
      />

      <Composition
        id="Stat"
        component={StatReveal as never}
        durationInFrames={75}
        fps={FPS}
        width={LAYOUT.width}
        height={LAYOUT.height}
        defaultProps={{
          value: 9,
          label: "tools built",
          y: LAYOUT.safeOverlayY,
        }}
        calculateMetadata={durationFrom(75)}
      />

      {/* Opaque top-pane insert, at the pane's native size - never upscaled. */}
      <Composition
        id="Terminal"
        component={TerminalInsert as never}
        durationInFrames={90}
        fps={FPS}
        width={LAYOUT.width}
        height={LAYOUT.topPaneHeight}
        defaultProps={{
          command: "claude --version",
          lines: ["+ 9 skills loaded", "+ 0 agents live"],
          title: "bash",
        }}
        calculateMetadata={durationFrom(90)}
      />
    </>
  );
};
