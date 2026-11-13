import React from "react";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS, FONTS } from "../theme/tokens";

export interface WordItem {
  text: string;
  norm: string;
  start: number;
  end: number;
}

export interface BeatItem {
  index: number;
  id: string;
  archetype: string;
  chapter: string;
  sfx: string;
  text: string;
  startSec: number;
  endSec: number;
  durationSec: number;
  startFrame: number;
  endFrame: number;
  durationFrames: number;
  wordStartIdx: number;
  wordEndIdx: number;
}

interface InkPressChromeProps {
  darkMode?: boolean;
  chapter: string;
  beatIndex: number;
  totalBeats: number;
  words: WordItem[];
  activeBeat: BeatItem;
}

export const InkPressChrome: React.FC<InkPressChromeProps> = ({
  darkMode = false,
  chapter,
  beatIndex,
  totalBeats,
  words,
  activeBeat,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const currentSec = frame / fps;

  const ink = darkMode ? COLORS.chalk : COLORS.ink;
  const muted = darkMode ? "rgba(246,239,226,0.55)" : COLORS.inkMuted;
  const borderCol = darkMode ? "rgba(246,239,226,0.18)" : "rgba(26,22,19,0.20)";
  const gridCol = darkMode ? "rgba(246,239,226,0.045)" : COLORS.gridLine;

  const beatWords = words.slice(activeBeat.wordStartIdx, activeBeat.wordEndIdx + 1);
  const overallProgress = interpolate(frame, [0, durationInFrames - 1], [0, 100], {
    extrapolateRight: "clamp",
  });

  // Subtle 12fps seeded paper grain offset so frame never feels frozen
  const grainSeed = Math.floor(frame / 3) % 7;

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {/* Background radial stage (anti-banding per look.md) */}
      <AbsoluteFill
        style={{
          zIndex: -2,
          background: darkMode
            ? `radial-gradient(circle at 50% 45%, ${COLORS.obsidianCenter} 0%, ${COLORS.obsidianEdge} 100%)`
            : `radial-gradient(circle at 50% 45%, ${COLORS.parchmentCenter} 0%, ${COLORS.parchmentEdge} 100%)`,
        }}
      />

      {/* Archival cartographic coordinate grid */}
      <AbsoluteFill
        style={{
          zIndex: -1,
          backgroundImage: `
            linear-gradient(to right, ${gridCol} 1px, transparent 1px),
            linear-gradient(to bottom, ${gridCol} 1px, transparent 1px)
          `,
          backgroundSize: "96px 96px",
        }}
      />

      {/* Top Editorial Header Bar */}
      <div
        style={{
          position: "absolute",
          top: 34,
          left: 56,
          right: 56,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontFamily: FONTS.mono,
          fontSize: 18,
          letterSpacing: "0.14em",
          color: muted,
          zIndex: 40,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <span
            style={{
              display: "inline-block",
              width: 10,
              height: 10,
              borderRadius: "50%",
              backgroundColor: darkMode ? COLORS.goldBright : COLORS.rome,
            }}
          />
          <span style={{ color: ink, fontWeight: 700 }}>{chapter}</span>
        </div>
        <div>
          CANNAE · 216 BC · BEAT {String(beatIndex + 1).padStart(2, "0")}/
          {String(totalBeats).padStart(2, "0")}
        </div>
      </div>

      {/* Archival Frame Hairline Border */}
      <div
        style={{
          position: "absolute",
          inset: "74px 52px 118px 52px",
          border: `2px solid ${borderCol}`,
          borderRadius: 6,
          zIndex: 35,
        }}
      />

      {/* Word-Synced Documentary Subtitle Band (Bottom Title-Safe Zone) */}
      <div
        style={{
          position: "absolute",
          bottom: 36,
          left: 90,
          right: 90,
          height: 64,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 50,
        }}
      >
        <div
          style={{
            background: darkMode ? "rgba(18,15,13,0.88)" : "rgba(26,22,19,0.92)",
            padding: "12px 30px",
            borderRadius: 999,
            border: `1.5px solid ${darkMode ? "rgba(242,183,53,0.38)" : "rgba(246,239,226,0.2)"}`,
            boxShadow: "0 10px 28px rgba(0,0,0,0.22)",
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "9px",
            fontFamily: FONTS.sans,
            fontSize: 27,
            fontWeight: 700,
          }}
        >
          {beatWords.map((w, idx) => {
            const isSpoken = currentSec >= w.start - 0.04;
            const isCurrent = currentSec >= w.start - 0.04 && currentSec <= w.end + 0.18;
            return (
              <span
                key={`${w.text}-${idx}`}
                style={{
                  color: isCurrent
                    ? COLORS.goldBright
                    : isSpoken
                    ? COLORS.chalk
                    : "rgba(246,239,226,0.42)",
                  transform: isCurrent ? "translateY(-2px) scale(1.05)" : "scale(1)",
                  display: "inline-block",
                }}
              >
                {w.text}
              </span>
            );
          })}
        </div>
      </div>

      {/* Chapter / Episode Progress Rail */}
      <div
        style={{
          position: "absolute",
          bottom: 14,
          left: 52,
          right: 52,
          height: 5,
          background: darkMode ? "rgba(246,239,226,0.12)" : "rgba(26,22,19,0.12)",
          borderRadius: 4,
          overflow: "hidden",
          zIndex: 50,
        }}
      >
        <div
          style={{
            width: `${overallProgress}%`,
            height: "100%",
            background: darkMode ? COLORS.goldBright : COLORS.rome,
          }}
        />
      </div>

      {/* Tactile Archival Paper Grain Overlay (Fast Static Seamless Texture) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `url(${staticFile("paper_grain.png")})`,
          backgroundSize: "512px 512px",
          opacity: darkMode ? 0.055 : 0.045,
          mixBlendMode: darkMode ? "screen" : "multiply",
          zIndex: 60,
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
