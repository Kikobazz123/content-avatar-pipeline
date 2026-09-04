import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { BRAND } from "../brand";

export type TerminalProps = {
  command: string;
  lines?: string[];
  /** Shown in the window chrome. Keep it short - it is read, not studied. */
  title?: string;
  accent?: string;
  durationInFrames?: number;
};

/**
 * An opaque insert for the TOP pane, at its native 1080x1056.
 *
 * This exists because the alternative is upscaling a small screen capture:
 * day01's 880x740 grab was stretched 1.43x and the terminal text went mushy.
 * Rendered text has no such ceiling, so any beat that can be a graphic instead
 * of a recording is sharper for free.
 */
export const TerminalInsert: React.FC<TerminalProps> = ({
  command,
  lines = [],
  title = "bash",
  accent = BRAND.accent,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const appear = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Type the command out, then reveal output lines one at a time. Typing is
  // fast on purpose - at 2-3s the point is momentum, not legibility of process.
  const typeStart = 8;
  const typeFrames = Math.min(22, Math.max(10, command.length));
  const typed = Math.round(
    interpolate(frame, [typeStart, typeStart + typeFrames], [0, command.length], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );
  const caretOn = Math.floor(frame / (fps / 3)) % 2 === 0;

  const outStart = typeStart + typeFrames + 4;
  const perLine = Math.max(
    3,
    Math.floor((durationInFrames - outStart - 6) / Math.max(1, lines.length))
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: BRAND.bg,
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#0B0D12",
          border: "1px solid #232833",
          borderRadius: 16,
          overflow: "hidden",
          opacity: appear,
          transform: `translateY(${interpolate(appear, [0, 1], [18, 0])}px)`,
          boxShadow: "0 30px 70px rgba(0,0,0,0.6)",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            height: 62,
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "0 22px",
            backgroundColor: "#151922",
            borderBottom: "1px solid #232833",
          }}
        >
          {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => (
            <div
              key={c}
              style={{ width: 16, height: 16, borderRadius: 8, backgroundColor: c }}
            />
          ))}
          <div
            style={{
              fontFamily: BRAND.body,
              fontSize: 24,
              color: BRAND.muted,
              marginLeft: 14,
            }}
          >
            {title}
          </div>
        </div>

        <div
          style={{
            flex: 1,
            padding: "30px 34px",
            fontFamily: "Consolas, 'Courier New', monospace",
            fontSize: 40,
            lineHeight: 1.5,
            color: BRAND.fg,
          }}
        >
          <div>
            <span style={{ color: accent }}>$ </span>
            {command.slice(0, typed)}
            {typed < command.length && caretOn ? (
              <span style={{ color: accent }}>_</span>
            ) : null}
          </div>

          {lines.map((ln, i) => {
            const at = outStart + i * perLine;
            const o = interpolate(frame, [at, at + 5], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            return (
              <div
                key={i}
                style={{
                  opacity: o,
                  color: ln.startsWith("+") ? "#28C840" : BRAND.muted,
                  marginTop: i === 0 ? 18 : 4,
                }}
              >
                {ln}
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
