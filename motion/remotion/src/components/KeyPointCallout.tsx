import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { BRAND, LAYOUT } from "../brand";

export type CalloutProps = {
  text: string;
  sub?: string | null;
  accent?: string;
  /** Distance from the top of the 1920px frame. Default clears captions and face. */
  y?: number;
  /** Frames of fade at the tail. The head is a spring, so it needs no counterpart. */
  outFrames?: number;
};

/**
 * A key point, over transparent background, timed to land on a spoken phrase.
 *
 * Rendered with an alpha channel and composited over the finished frame, so it
 * floats above both panes without disturbing either. Deliberately short: this is
 * punctuation for something already being said, not a slide.
 */
export const KeyPointCallout: React.FC<CalloutProps> = ({
  text,
  sub = null,
  accent = BRAND.accent,
  y = LAYOUT.safeOverlayY,
  outFrames = 8,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Overshoot slightly on entry: a pure ease-in reads as a slide, a small
  // overshoot reads as an arrival, which is what earns the cut.
  const enter = spring({ frame, fps, config: { damping: 14, mass: 0.5 } });
  const exit = interpolate(
    frame,
    [durationInFrames - outFrames, durationInFrames - 1],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const opacity = enter * exit;
  const translateY = interpolate(enter, [0, 1], [28, 0]);
  const scale = interpolate(enter, [0, 1], [0.94, 1]);

  // The rule sweeps out from the left slightly behind the text.
  const ruleW = interpolate(frame, [3, 16], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "transparent" }}>
      <div
        style={{
          position: "absolute",
          top: y,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          opacity,
          transform: `translateY(${translateY}px) scale(${scale})`,
        }}
      >
        <div
          style={{
            backgroundColor: BRAND.bg, // solid: a translucent card lets busy
            // terminal text read straight through it and looks unfinished
            borderLeft: `10px solid ${accent}`,
            padding: "34px 46px 38px 40px",
            maxWidth: 900,
            boxShadow: "0 24px 60px rgba(0,0,0,0.55)",
          }}
        >
          <div
            style={{
              fontFamily: BRAND.display,
              fontSize: 74,
              lineHeight: 1.06,
              color: BRAND.fg,
              textTransform: "uppercase",
              letterSpacing: -1,
            }}
          >
            {text}
          </div>

          <div
            style={{
              height: 6,
              width: `${ruleW}%`,
              backgroundColor: accent,
              marginTop: 22,
            }}
          />

          {sub ? (
            <div
              style={{
                fontFamily: BRAND.body,
                fontSize: 34,
                color: BRAND.muted,
                marginTop: 20,
              }}
            >
              {sub}
            </div>
          ) : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};
