import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Icon } from "@iconify/react";
import { COLORS, FONTS, SPRINGS } from "../theme/tokens";
import { RoughRect } from "../components/RoughShape";

export const ThesisPosterStage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Sub-beat 1 (t=0s): "Rome brought a hammer."
  const hammerIn = spring({
    frame,
    fps,
    config: SPRINGS.heavy,
  });

  // Sub-beat 2 (t=1.25s / frame 38): "Hannibal brought a net."
  const netIn = spring({
    frame: frame - 36,
    fps,
    config: SPRINGS.snappy,
  });

  return (
    <AbsoluteFill
      style={{
        padding: "118px 96px 148px 96px",
        display: "flex",
        flexDirection: "row",
        gap: 48,
        alignItems: "stretch",
      }}
    >
      {/* LEFT POSTER: ROME BROUGHT A HAMMER */}
      <div
        style={{
          flex: 1,
          position: "relative",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: 44,
          opacity: hammerIn,
          transform: `translateY(${interpolate(hammerIn, [0, 1], [-45, 0])}px)`,
        }}
      >
        <svg width="815" height="790" style={{ position: "absolute", inset: 0 }}>
          <RoughRect
            x={0}
            y={0}
            width={815}
            height={790}
            seed={91}
            options={{
              fill: COLORS.parchmentCard,
              fillStyle: "solid",
              stroke: COLORS.rome,
              strokeWidth: 4,
            }}
          />
        </svg>

        <div
          style={{
            position: "relative",
            width: 186,
            height: 186,
            borderRadius: 24,
            background: COLORS.rome,
            border: `4px solid ${COLORS.ink}`,
            boxShadow: "8px 8px 0px rgba(26,22,19,0.88)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            color: COLORS.parchmentCenter,
          }}
        >
          <Icon icon="game-icons:hammer-drop" width={124} height={124} />
        </div>

        <div
          style={{
            position: "relative",
            marginTop: 42,
            fontFamily: FONTS.mono,
            fontSize: 20,
            fontWeight: 700,
            letterSpacing: "0.18em",
            color: COLORS.romeDark,
          }}
        >
          BRUTE FORCE DOCTRINE
        </div>

        <div
          style={{
            position: "relative",
            marginTop: 14,
            fontFamily: FONTS.display,
            fontSize: 58,
            fontWeight: 900,
            textAlign: "center",
            lineHeight: 1.12,
            color: COLORS.ink,
          }}
        >
          ROME BROUGHT
          <br />
          <span style={{ color: COLORS.rome }}>A HAMMER.</span>
        </div>
      </div>

      {/* RIGHT POSTER: HANNIBAL BROUGHT A NET */}
      <div
        style={{
          flex: 1,
          position: "relative",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: 44,
          opacity: netIn,
          transform: `scale(${interpolate(netIn, [0, 1], [0.92, 1])})`,
        }}
      >
        <svg width="815" height="790" style={{ position: "absolute", inset: 0 }}>
          <RoughRect
            x={0}
            y={0}
            width={815}
            height={790}
            seed={105}
            options={{
              fill: COLORS.ink,
              fillStyle: "solid",
              stroke: COLORS.goldBright,
              strokeWidth: 4,
            }}
          />
        </svg>

        <div
          style={{
            position: "relative",
            width: 186,
            height: 186,
            borderRadius: 24,
            background: COLORS.carthage,
            border: `4px solid ${COLORS.goldBright}`,
            boxShadow: "8px 8px 0px rgba(212,148,30,0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            color: COLORS.goldBright,
          }}
        >
          <Icon icon="game-icons:fishing-net" width={124} height={124} />
        </div>

        <div
          style={{
            position: "relative",
            marginTop: 42,
            fontFamily: FONTS.mono,
            fontSize: 20,
            fontWeight: 700,
            letterSpacing: "0.18em",
            color: COLORS.goldBright,
          }}
        >
          GEOMETRIC ASYMMETRY
        </div>

        <div
          style={{
            position: "relative",
            marginTop: 14,
            fontFamily: FONTS.display,
            fontSize: 58,
            fontWeight: 900,
            textAlign: "center",
            lineHeight: 1.12,
            color: COLORS.chalk,
          }}
        >
          HANNIBAL BROUGHT
          <br />
          <span style={{ color: COLORS.goldBright }}>A NET.</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
