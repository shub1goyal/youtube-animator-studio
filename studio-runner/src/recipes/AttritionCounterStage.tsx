import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Icon } from "@iconify/react";
import { COLORS, FONTS, SPRINGS } from "../theme/tokens";

export const AttritionCounterStage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const cardIn = spring({ frame, fps, config: SPRINGS.snappy });

  const deadCount = Math.round(
    interpolate(frame, [2, Math.min(42, durationInFrames - 12)], [0, 70000], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  // Sub-beat at ~1.3s: "two hundred every minute" radial gauge
  const rateIn = spring({
    frame: frame - 34,
    fps,
    config: SPRINGS.bouncy,
  });

  const ringProgress = interpolate(frame, [4, 48], [0, 0.814], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const radius = 195;
  const circumference = 2 * Math.PI * radius;

  return (
    <AbsoluteFill
      style={{
        padding: "120px 110px 150px 110px",
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      {/* LEFT: Monumental 70,000 Casualties Readout */}
      <div
        style={{
          flex: 1.25,
          opacity: cardIn,
          transform: `translateY(${interpolate(cardIn, [0, 1], [35, 0])}px)`,
        }}
      >
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 14,
            background: "rgba(184,41,37,0.22)",
            border: `2px solid ${COLORS.rome}`,
            padding: "10px 22px",
            borderRadius: 6,
            fontFamily: FONTS.mono,
            fontSize: 19,
            fontWeight: 700,
            color: "#FF7873",
            letterSpacing: "0.14em",
          }}
        >
          <Icon icon="game-icons:broken-shield" width={26} height={26} />
          <span>SINGLE-DAY CASUALTIES · 4 HOURS</span>
        </div>

        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 164,
            fontWeight: 700,
            color: COLORS.chalk,
            lineHeight: 1.0,
            marginTop: 22,
            letterSpacing: "-0.03em",
            textShadow: "0 0 48px rgba(184,41,37,0.45)",
          }}
        >
          {deadCount.toLocaleString()}
        </div>

        <div
          style={{
            fontFamily: FONTS.display,
            fontSize: 42,
            fontWeight: 700,
            color: COLORS.goldBright,
            marginTop: 12,
            letterSpacing: "0.04em",
          }}
        >
          ROMAN SOLDIERS FALLEN
        </div>

        <div
          style={{
            fontFamily: FONTS.sans,
            fontSize: 25,
            color: "rgba(246,239,226,0.72)",
            marginTop: 16,
            maxWidth: 740,
          }}
        >
          Including 80 Roman Senators and 29 of 48 Military Tribunes.
        </div>
      </div>

      {/* RIGHT: 81% Wipeout Ring + 200/MIN Ticker */}
      <div
        style={{
          width: 520,
          height: 520,
          position: "relative",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          transform: `scale(${cardIn})`,
        }}
      >
        <svg width="500" height="500" viewBox="0 0 500 500">
          <circle
            cx={250}
            cy={250}
            r={radius}
            fill="none"
            stroke="rgba(246,239,226,0.12)"
            strokeWidth={32}
          />
          <circle
            cx={250}
            cy={250}
            r={radius}
            fill="none"
            stroke={COLORS.rome}
            strokeWidth={32}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference * (1 - ringProgress)}
            transform="rotate(-90 250 250)"
          />
        </svg>

        <div
          style={{
            position: "absolute",
            textAlign: "center",
            transform: `scale(${rateIn > 0.05 ? interpolate(rateIn, [0, 1], [0.85, 1]) : 1})`,
          }}
        >
          {frame < 34 ? (
            <>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 76,
                  fontWeight: 700,
                  color: COLORS.chalk,
                }}
              >
                {Math.round(ringProgress * 100)}%
              </div>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 18,
                  color: "rgba(246,239,226,0.65)",
                  letterSpacing: "0.14em",
                }}
              >
                ARMY ANNIHILATED
              </div>
            </>
          ) : (
            <>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 84,
                  fontWeight: 700,
                  color: COLORS.goldBright,
                  lineHeight: 1,
                }}
              >
                200+
              </div>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 22,
                  fontWeight: 700,
                  color: COLORS.chalk,
                  marginTop: 8,
                  letterSpacing: "0.12em",
                }}
              >
                EVERY MINUTE
              </div>
            </>
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};
