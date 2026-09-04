// Mirrors pipeline/repurpose/brand.json so motion graphics, quote cards and the
// burned-in captions all read as one identity. If that file changes, change this.
export const BRAND = {
  bg: "#12141A",
  fg: "#FFFFFF",
  accent: "#22D3EE", // same cyan as the karaoke caption highlight
  muted: "#8B94A3",
  display: '"Arial Black", "Arial Bold", Gadget, sans-serif',
  body: '"Arial", Helvetica, sans-serif',
};

// Frame geometry, at compose.py's default --split 0.55 on a 1080x1920 canvas.
//   top pane    0 -> 1056   screen recording / inserts
//   captions  420 ->  600   burned in, top-anchored at margin_v 420
//   bottom   1056 -> 1920   the presenter's face
// A full-frame overlay must therefore avoid 420-600 and everything below 1056.
// 700-1000 is the clear band: inside the top pane, under the captions, above
// the face.
export const LAYOUT = {
  width: 1080,
  height: 1920,
  topPaneHeight: 1056,
  captionBand: [420, 600] as const,
  safeOverlayY: 700,
};
