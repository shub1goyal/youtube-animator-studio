import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Icon } from "@iconify/react";
import { COLORS, FONTS, SPRINGS } from "../theme/tokens";
import { RoughRect } from "../components/RoughShape";

export const CompressionLoupeStage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const loupeIn = spring({
    frame,
    fps,
    config: SPRINGS.bouncy,
  });

  // Progressive crush factor from 0 -> 1
  const crush = interpolate(frame, [4, durationInFrames - 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Sub-beat at frame 42 (~1.4s): "couldn't even draw swords" callout slams in!
  const swordBanIn = spring({
    frame: frame - 38,
    fps,
    config: SPRINGS.snappy,
  });

  // 61 soldiers packed in concentric hexagonal rings inside the loupe
  const soldiers: { angle: number; ring: number; id: number }[] = [{ angle: 0, ring: 0, id: 0 }];
  let sid = 1;
  [6, 12, 18, 24].forEach((count, rIdx) => {
    for (let i = 0; i < count; i++) {
      soldiers.push({
        angle: (i * 2 * Math.PI) / count + rIdx * 0.25,
        ring: rIdx + 1,
        id: sid++,
      });
    }
  });

  return (
    <AbsoluteFill
      style={{
        padding: "110px 96px 140px 96px",
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 56,
      }}
    >
      {/* LEFT: Giant Circular Tactical Magnifying Loupe */}
      <div
        style={{
          width: 680,
          height: 680,
          position: "relative",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          transform: `scale(${loupeIn})`,
        }}
      >
        <svg width="680" height="680" viewBox="0 0 680 680">
          <defs>
            <clipPath id="loupe-clip">
              <circle cx={340} cy={340} r={285} />
            </clipPath>
          </defs>

          {/* Outer Brass / Ink Rim */}
          <circle
            cx={340}
            cy={340}
            r={302}
            fill={COLORS.ink}
          />
          <circle
            cx={340}
            cy={340}
            r={290}
            fill={COLORS.parchmentCard}
            stroke={COLORS.gold}
            strokeWidth={6}
          />

          <g clipPath="url(#loupe-clip)">
            {/* Crushing Outer Carthaginian Ring */}
            <circle
              cx={340}
              cy={340}
              r={268 - crush * 64}
              fill="rgba(184,41,37,0.12)"
              stroke={COLORS.carthage}
              strokeWidth={26}
            />

            {/* 61 Jammed Roman Infantry Circles */}
            {soldiers.map((s) => {
              const spacing = 48 - crush * 14.5; // compresses until shields touch & lock!
              const jitterX = Math.sin(frame * 0.8 + s.id * 1.7) * (1.2 + crush * 1.8);
              const jitterY = Math.cos(frame * 0.9 + s.id * 2.3) * (1.2 + crush * 1.8);
              const sx = 340 + Math.cos(s.angle) * s.ring * spacing + jitterX;
              const sy = 340 + Math.sin(s.angle) * s.ring * spacing + jitterY;
              return (
                <g key={s.id} transform={`translate(${sx}, ${sy})`}>
                  <circle
                    r={18}
                    fill={COLORS.rome}
                    stroke={COLORS.ink}
                    strokeWidth={2.5}
                  />
                  <circle r={6} fill={COLORS.parchmentCenter} />
                </g>
              );
            })}

            {/* 4 Inward Hydraulic Crush Arrows */}
            {[0, 90, 180, 270].map((deg) => (
              <g
                key={deg}
                transform={`translate(340, 340) rotate(${deg}) translate(0, ${-255 + crush * 52})`}
              >
                <polygon
                  points="-18,-26 18,-26 0,8"
                  fill={COLORS.goldBright}
                  stroke={COLORS.ink}
                  strokeWidth={2.5}
                />
              </g>
            ))}
          </g>
        </svg>

        {/* Loupe Tag */}
        <div
          style={{
            position: "absolute",
            bottom: 10,
            background: COLORS.ink,
            color: COLORS.goldBright,
            fontFamily: FONTS.mono,
            fontSize: 18,
            fontWeight: 700,
            padding: "8px 22px",
            borderRadius: 999,
            letterSpacing: "0.12em",
          }}
        >
          10× TACTICAL CROWD DENSITY
        </div>
      </div>

      {/* RIGHT: Biomechanical Breakdown Card */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 30 }}>
        <div
          style={{
            position: "relative",
            padding: "34px 42px",
          }}
        >
          <svg width="960" height="260" style={{ position: "absolute", inset: 0 }}>
            <RoughRect
              x={0}
              y={0}
              width={960}
              height={260}
              seed={71}
              options={{
                fill: COLORS.parchmentCard,
                fillStyle: "solid",
                stroke: COLORS.ink,
                strokeWidth: 3.5,
              }}
            />
          </svg>
          <div style={{ position: "relative" }}>
            <div
              style={{
                fontFamily: FONTS.mono,
                fontSize: 19,
                fontWeight: 700,
                color: COLORS.rome,
                letterSpacing: "0.14em",
              }}
            >
              SOLDIER SPACING COLLAPSE
            </div>
            <div
              style={{
                fontFamily: FONTS.mono,
                fontSize: 64,
                fontWeight: 700,
                color: COLORS.ink,
                marginTop: 8,
              }}
            >
              {(1.8 - crush * 1.35).toFixed(2)}m{" "}
              <span style={{ fontSize: 28, color: COLORS.inkMuted }}>
                PER LEGIONARY (NEEDED: 1.80m)
              </span>
            </div>
            <div
              style={{
                marginTop: 18,
                height: 18,
                background: "rgba(26,22,19,0.12)",
                borderRadius: 9,
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${interpolate(crush, [0, 1], [100, 24])}%`,
                  height: "100%",
                  background: COLORS.rome,
                }}
              />
            </div>
          </div>
        </div>

        {/* Sub-Beat 2: Gladius Sword Disabled Card */}
        <div
          style={{
            position: "relative",
            padding: "34px 42px",
            opacity: swordBanIn,
            transform: `translateX(${interpolate(swordBanIn, [0, 1], [50, 0])}px)`,
          }}
        >
          <svg width="960" height="310" style={{ position: "absolute", inset: 0 }}>
            <RoughRect
              x={0}
              y={0}
              width={960}
              height={310}
              seed={83}
              options={{
                fill: COLORS.ink,
                fillStyle: "solid",
                stroke: COLORS.rome,
                strokeWidth: 4,
              }}
            />
          </svg>
          <div
            style={{
              position: "relative",
              display: "flex",
              alignItems: "center",
              gap: 36,
            }}
          >
            {/* Crossed-Out Gladius Emblem */}
            <div
              style={{
                width: 156,
                height: 156,
                borderRadius: "50%",
                background: "rgba(246,239,226,0.08)",
                border: `5px solid ${COLORS.rome}`,
                position: "relative",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                flexShrink: 0,
              }}
            >
              <Icon
                icon="game-icons:gladius"
                width={96}
                height={96}
                color={COLORS.chalk}
              />
              <div
                style={{
                  position: "absolute",
                  width: "108%",
                  height: 8,
                  background: COLORS.rome,
                  transform: "rotate(-45deg)",
                }}
              />
            </div>

            <div>
              <div
                style={{
                  fontFamily: FONTS.display,
                  fontSize: 44,
                  fontWeight: 900,
                  color: COLORS.goldBright,
                  lineHeight: 1.1,
                }}
              >
                ARMS PINNED TO RIBS
              </div>
              <div
                style={{
                  fontFamily: FONTS.sans,
                  fontSize: 26,
                  color: COLORS.chalk,
                  marginTop: 12,
                  lineHeight: 1.35,
                }}
              >
                Shields interlocked under lateral pressure — impossible to draw a{" "}
                <strong style={{ color: COLORS.goldBright }}>Gladius</strong> or swing.
              </div>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
