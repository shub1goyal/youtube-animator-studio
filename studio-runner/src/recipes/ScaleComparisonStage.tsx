import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Icon } from "@iconify/react";
import { COLORS, FONTS, SPRINGS } from "../theme/tokens";
import { RoughRect } from "../components/RoughShape";

export const ScaleComparisonStage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Sub-beat 1 (frame 0): Rome 86,000 slams in
  const romeIn = spring({ frame, fps, config: SPRINGS.snappy });
  const romeCount = Math.round(
    interpolate(frame, [2, 34], [0, 86000], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  // Sub-beat 2 (frame 42 / ~1.4s): Hannibal 50,000 slams in when narrator says "Hannibal's fifty thousand"
  const hannibalStart = 40;
  const hannibalIn = spring({
    frame: frame - hannibalStart,
    fps,
    config: SPRINGS.snappy,
  });
  const hannibalCount = Math.round(
    interpolate(frame, [hannibalStart, hannibalStart + 32], [0, 50000], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  const badgeIn = spring({
    frame: frame - (hannibalStart + 16),
    fps,
    config: SPRINGS.bouncy,
  });

  // 90 grid slots (9 rows x 10 cols = 1,000 soldiers per tile)
  const slots = Array.from({ length: 90 }, (_, i) => i);

  return (
    <AbsoluteFill
      style={{
        padding: "108px 92px 145px 92px",
        display: "flex",
        flexDirection: "row",
        gap: 54,
        alignItems: "stretch",
      }}
    >
      {/* LEFT CARD: ROME (86,000) */}
      <div
        style={{
          flex: 1,
          position: "relative",
          padding: "32px 38px",
          opacity: romeIn,
          transform: `translateY(${interpolate(romeIn, [0, 1], [40, 0])}px)`,
        }}
      >
        <svg width="815" height="820" style={{ position: "absolute", inset: 0 }}>
          <RoughRect
            x={0}
            y={0}
            width={815}
            height={820}
            seed={31}
            options={{
              fill: COLORS.parchmentCard,
              fillStyle: "solid",
              stroke: COLORS.rome,
              strokeWidth: 3.5,
            }}
          />
        </svg>

        <div style={{ position: "relative" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
            <div
              style={{
                width: 72,
                height: 72,
                background: COLORS.rome,
                color: COLORS.parchmentCenter,
                borderRadius: 10,
                border: `3px solid ${COLORS.ink}`,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Icon icon="game-icons:centurion-helmet" width={48} height={48} />
            </div>
            <div>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 18,
                  fontWeight: 700,
                  color: COLORS.romeDark,
                  letterSpacing: "0.14em",
                }}
              >
                ROMAN REPUBLIC · 8 LEGIONS
              </div>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 64,
                  fontWeight: 700,
                  color: COLORS.rome,
                  lineHeight: 1.05,
                }}
              >
                {romeCount.toLocaleString()}
              </div>
            </div>
          </div>

          <div
            style={{
              marginTop: 10,
              fontFamily: FONTS.sans,
              fontSize: 19,
              fontWeight: 700,
              color: COLORS.inkMuted,
            }}
          >
            EACH TILE = 1,000 INFANTRY & CAVALRY
          </div>

          {/* 90-Slot Proportional Matrix (86 Filled Crimson) */}
          <div
            style={{
              marginTop: 22,
              display: "grid",
              gridTemplateColumns: "repeat(10, 1fr)",
              gap: 10,
            }}
          >
            {slots.map((idx) => {
              const active = idx < 86;
              const tilePop = spring({
                frame: frame - 3 - Math.floor(idx / 3),
                fps,
                config: SPRINGS.snappy,
              });
              return (
                <div
                  key={idx}
                  style={{
                    height: 48,
                    borderRadius: 5,
                    background: active ? COLORS.rome : "transparent",
                    border: active
                      ? `2px solid ${COLORS.ink}`
                      : "2px dashed rgba(26,22,19,0.18)",
                    transform: `scale(${active ? tilePop : 1})`,
                    opacity: active ? tilePop : 0.45,
                  }}
                />
              );
            })}
          </div>
        </div>
      </div>

      {/* RIGHT CARD: HANNIBAL (50,000) */}
      <div
        style={{
          flex: 1,
          position: "relative",
          padding: "32px 38px",
          opacity: interpolate(hannibalIn, [0, 1], [0.12, 1]),
          transform: `translateY(${interpolate(hannibalIn, [0, 1], [40, 0])}px)`,
        }}
      >
        <svg width="815" height="820" style={{ position: "absolute", inset: 0 }}>
          <RoughRect
            x={0}
            y={0}
            width={815}
            height={820}
            seed={47}
            options={{
              fill: COLORS.parchmentCard,
              fillStyle: "solid",
              stroke: COLORS.carthage,
              strokeWidth: 3.5,
            }}
          />
        </svg>

        <div style={{ position: "relative" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
            <div
              style={{
                width: 72,
                height: 72,
                background: COLORS.carthage,
                color: COLORS.parchmentCenter,
                borderRadius: 10,
                border: `3px solid ${COLORS.ink}`,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Icon icon="game-icons:elephant" width={46} height={46} />
            </div>
            <div>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 18,
                  fontWeight: 700,
                  color: COLORS.carthageDark,
                  letterSpacing: "0.14em",
                }}
              >
                HANNIBAL BARCA · MERCENARY COALITION
              </div>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 64,
                  fontWeight: 700,
                  color: COLORS.carthage,
                  lineHeight: 1.05,
                }}
              >
                {hannibalCount.toLocaleString()}
              </div>
            </div>
          </div>

          <div
            style={{
              marginTop: 10,
              fontFamily: FONTS.sans,
              fontSize: 19,
              fontWeight: 700,
              color: COLORS.inkMuted,
            }}
          >
            36,000 FEWER SOLDIERS ON OPEN GROUND
          </div>

          {/* 90-Slot Proportional Matrix (Only 50 Filled Cobalt, 36 Empty Ghost Slots!) */}
          <div
            style={{
              marginTop: 22,
              display: "grid",
              gridTemplateColumns: "repeat(10, 1fr)",
              gap: 10,
            }}
          >
            {slots.map((idx) => {
              const active = idx < 50;
              const missing = idx >= 50 && idx < 86;
              const tilePop = spring({
                frame: frame - hannibalStart - Math.floor(idx / 2.5),
                fps,
                config: SPRINGS.snappy,
              });
              return (
                <div
                  key={idx}
                  style={{
                    height: 48,
                    borderRadius: 5,
                    background: active
                      ? COLORS.carthage
                      : missing
                      ? "rgba(184,41,37,0.08)"
                      : "transparent",
                    border: active
                      ? `2px solid ${COLORS.ink}`
                      : missing
                      ? `2px dashed ${COLORS.rome}`
                      : "2px dashed rgba(26,22,19,0.14)",
                    transform: `scale(${active ? tilePop : 1})`,
                    opacity: active ? tilePop : 0.65,
                  }}
                />
              );
            })}
          </div>
        </div>
      </div>

      {/* CENTER OVERLAY BADGE: 1.7x OUTNUMBERED */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "47%",
          transform: `translate(-50%, -50%) scale(${badgeIn}) rotate(-4deg)`,
          background: COLORS.ink,
          color: COLORS.goldBright,
          border: `4px solid ${COLORS.goldBright}`,
          padding: "16px 28px",
          boxShadow: "0 14px 32px rgba(0,0,0,0.35)",
          textAlign: "center",
          zIndex: 25,
        }}
      >
        <div style={{ fontFamily: FONTS.mono, fontSize: 16, letterSpacing: "0.14em", color: COLORS.chalk }}>
          FORCE RATIO
        </div>
        <div style={{ fontFamily: FONTS.display, fontSize: 42, fontWeight: 900 }}>
          1.7 : 1
        </div>
      </div>
    </AbsoluteFill>
  );
};
