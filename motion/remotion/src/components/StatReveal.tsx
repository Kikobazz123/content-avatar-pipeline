import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { BRAND, LAYOUT } from "../brand";

export type StatProps = {
  value: number;
  label: string;
  prefix?: string;
  suffix?: string;
  accent?: string;
  y?: number;
  /** Count up to `value`. Off for a figure that is the point precisely because
   *  it is zero - animating 0 to 0 is dead air. */
  countUp?: boolean;
  outFrames?: number;
};

/**
 * One number, held long enough to land.
 *
 * Use for a figure the script states out loud - "exactly zero naira", "nine
 * tools". Seeing a number while hearing it is what makes it stick; a number the
 * script does not say is just decoration.
 */
export const StatReveal: React.FC<StatProps> = ({
  value,
  label,
  prefix = "",
  suffix = "",
  accent = BRAND.accent,
  y = LAYOUT.safeOverlayY,
  countUp = true,
  outFrames = 8,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const enter = spring({ frame, fps, config: { damping: 13, mass: 0.6 } });
  const exit = interpolate(
    frame,
    [durationInFrames - outFrames, durationInFrames - 1],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const shown = countUp
    ? Math.round(
        interpolate(frame, [2, Math.min(26, durationInFrames - outFrames)], [0, value], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      )
    : value;

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
          opacity: enter * exit,
          transform: `scale(${interpolate(enter, [0, 1], [0.86, 1])})`,
        }}
      >
        <div
          style={{
            fontFamily: BRAND.display,
            fontSize: 210,
            lineHeight: 1,
            color: accent,
            textShadow: "0 14px 44px rgba(0,0,0,0.6)",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {prefix}
          {shown.toLocaleString()}
          {suffix}
        </div>
        <div
          style={{
            fontFamily: BRAND.display,
            fontSize: 46,
            color: BRAND.fg,
            textTransform: "uppercase",
            letterSpacing: 2,
            marginTop: 10,
            backgroundColor: BRAND.bg,
            padding: "12px 26px",
          }}
        >
          {label}
        </div>
      </div>
    </AbsoluteFill>
  );
};
