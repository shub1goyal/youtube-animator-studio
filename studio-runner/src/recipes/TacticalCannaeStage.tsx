import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { evolvePath } from "@remotion/paths";
import { Icon } from "@iconify/react";
import { COLORS, FONTS, SPRINGS } from "../theme/tokens";
import { RoughCircle, RoughRect } from "../components/RoughShape";

interface TacticalCannaeStageProps {
  impactStart: number;
  concaveStart: number;
  flanksStart: number;
  pincerStart: number;
}

const Starburst: React.FC<{ x: number; y: number; scale: number; seed: number }> = ({
  x,
  y,
  scale,
  seed,
}) => {
  if (scale <= 0.02) return null;
  const points: string[] = [];
  const spikes = 10;
  for (let i = 0; i < spikes * 2; i++) {
    const angle = (i * Math.PI) / spikes + seed * 0.4;
    const r = i % 2 === 0 ? 34 + (seed % 5) * 2 : 14;
    points.push(`${Math.cos(angle) * r},${Math.sin(angle) * r}`);
  }
  return (
    <g transform={`translate(${x}, ${y}) scale(${scale})`}>
      <polygon
        points={points.join(" ")}
        fill={COLORS.goldBright}
        stroke={COLORS.ink}
        strokeWidth={3}
        strokeLinejoin="round"
      />
      <circle r={8} fill="#FFF8DC" />
    </g>
  );
};

export const TacticalCannaeStage: React.FC<TacticalCannaeStageProps> = ({
  impactStart,
  concaveStart,
  flanksStart,
  pincerStart,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Phase progressions (5 distinct, frame-exact tactical mutations!)
  const enterP = spring({ frame, fps, config: SPRINGS.snappy });
  const impactP = spring({
    frame: frame - impactStart,
    fps,
    config: SPRINGS.heavy,
  });
  const concaveP = spring({
    frame: frame - concaveStart,
    fps,
    config: SPRINGS.heavy,
  });
  const flanksP = spring({
    frame: frame - flanksStart,
    fps,
    config: SPRINGS.snappy,
  });
  const pincerP = interpolate(frame, [pincerStart, pincerStart + 36], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const sealPop = spring({
    frame: frame - (pincerStart + 30),
    fps,
    config: SPRINGS.bouncy,
  });

  // Camera shake at Roman collision & Cavalry slam
  const impactDelta = frame - impactStart;
  const shakeImpact =
    impactDelta >= 0 && impactDelta < 12
      ? Math.sin(impactDelta * 2.9) * (12 - impactDelta) * 1.15
      : 0;
  const slamDelta = frame - (pincerStart + 30);
  const shakeSlam =
    slamDelta >= 0 && slamDelta < 10
      ? Math.cos(slamDelta * 3.2) * (10 - slamDelta) * 1.1
      : 0;

  // Dynamic 2.5D camera framing per phase
  const camScale =
    1.0 +
    impactP * 0.05 -
    concaveP * 0.02 +
    flanksP * 0.05 -
    (pincerP > 0 ? pincerP * 0.06 : 0);

  // Determine current phase banner text
  let phaseTag = "PHASE 01 · FORWARD CONVEX BAIT";
  let phaseColor = COLORS.gold;
  if (frame >= pincerStart) {
    phaseTag = "PHASE 05 · REAR CAVALRY DOUBLE-ENVELOPMENT";
    phaseColor = COLORS.rome;
  } else if (frame >= flanksStart) {
    phaseTag = "PHASE 04 · VETERAN AFRICAN FLANKS CLAMP INWARD";
    phaseColor = COLORS.carthage;
  } else if (frame >= concaveStart) {
    phaseTag = "PHASE 03 · CRESCENT INVERTS INTO DEEP FUNNEL";
    phaseColor = COLORS.gold;
  } else if (frame >= impactStart) {
    phaseTag = "PHASE 02 · 86,000 ROMANS SMASH THE CENTER";
    phaseColor = COLORS.rome;
  }

  // 9 Carthaginian center blocks: bow goes from -115px (upward convex) -> +165px (downward U-funnel!)
  const centerNodes = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
  const currentBow =
    -112 * enterP + impactP * 52 + concaveP * 235; // ends at +175px deep pocket!

  // 32 Roman Legion cohorts (8 cols x 4 rows) advancing and compressing inward as funnel Tightens!
  const romanCols = 8;
  const romanRows = 4;

  // Sweeping cavalry pincer paths
  const leftCavPath = "M 360 660 C 210 430, 350 185, 925 225";
  const rightCavPath = "M 1560 660 C 1710 430, 1570 185, 995 225";
  const leftCavEv = evolvePath(pincerP, leftCavPath);
  const rightCavEv = evolvePath(pincerP, rightCavPath);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {/* War-Table Stage with subtle 2.5D Tactical Tilt */}
      <div
        style={{
          width: 1920,
          height: 1080,
          transform: `perspective(1600px) rotateX(11deg) translate(${shakeImpact + shakeSlam}px, -12px) scale(${camScale})`,
          transformOrigin: "960px 540px",
        }}
      >
        <svg width="1920" height="1080" viewBox="0 0 1920 1080">
          {/* Aufidus River on Right Flank (Geographic Anchor) */}
          <path
            d="M 1730 40 C 1680 280, 1770 520, 1700 780 C 1665 900, 1735 980, 1715 1060"
            fill="none"
            stroke="#9BB8B3"
            strokeWidth={54}
            strokeLinecap="round"
            opacity={0.75}
          />
          <path
            d="M 1730 40 C 1680 280, 1770 520, 1700 780 C 1665 900, 1735 980, 1715 1060"
            fill="none"
            stroke="#5D7D78"
            strokeWidth={3}
            strokeDasharray="12 10"
          />
          <text
            x={1655}
            y={530}
            transform="rotate(86, 1655, 530)"
            fontFamily={FONTS.mono}
            fontSize={18}
            fontWeight={700}
            fill="#48635E"
            letterSpacing="0.2em"
          >
            AUFIDUS RIVER
          </text>

          {/* Left Hill Elevation Contours */}
          <ellipse
            cx={170}
            cy={520}
            rx={135}
            ry={290}
            fill="none"
            stroke="rgba(110,95,75,0.28)"
            strokeWidth={2.5}
            strokeDasharray="10 8"
          />
          <ellipse
            cx={150}
            cy={520}
            rx={85}
            ry={190}
            fill="rgba(110,95,75,0.08)"
            stroke="rgba(110,95,75,0.32)"
            strokeWidth={2}
          />

          {/* Phase 1 Guide: Dashed Crescent Curve */}
          {concaveP < 0.8 && (
            <path
              d={`M 540 595 Q 960 ${595 + currentBow * 1.4} 1380 595`}
              fill="none"
              stroke={COLORS.gold}
              strokeWidth={4}
              strokeDasharray="12 10"
              opacity={0.75}
            />
          )}

          {/* Phase 5 Kill-Pocket Danger Ring */}
          {sealPop > 0.01 && (
            <g opacity={sealPop}>
              <RoughCircle
                cx={960}
                cy={495}
                diameter={650}
                options={{
                  stroke: COLORS.rome,
                  strokeWidth: 5,
                  fill: "rgba(184, 41, 37, 0.12)",
                  fillStyle: "solid",
                }}
              />
            </g>
          )}

          {/* 32 ROMAN LEGION COHORTS (8 x 4 Crimson Steamroller -> Funnelled & Compressed!) */}
          {Array.from({ length: romanRows }).map((_, rIdx) =>
            Array.from({ length: romanCols }).map((__, cIdx) => {
              const normCol = cIdx - (romanCols - 1) / 2; // -3.5 .. +3.5
              const centerFactor = 1 - Math.abs(normCol) / 4.2;

              // Spread narrows as flanks clamp in Phase 4 & 5!
              const colSpacing =
                88 - concaveP * 11 - flanksP * 17 - pincerP * 6;
              const rowSpacing = 48 - flanksP * 6 - pincerP * 5;

              const baseY =
                195 +
                rIdx * rowSpacing +
                impactP * 145 +
                concaveP * (95 + centerFactor * 68) +
                pincerP * 18;

              const x = 960 + normCol * colSpacing;
              const y = baseY;

              return (
                <g
                  key={`rom-${rIdx}-${cIdx}`}
                  transform={`translate(${x - 34}, ${y - 18}) scale(${enterP})`}
                >
                  <rect
                    width={68}
                    height={36}
                    rx={4}
                    fill={COLORS.rome}
                    stroke={COLORS.ink}
                    strokeWidth={2.6}
                  />
                  <rect
                    x={8}
                    y={7}
                    width={52}
                    height={22}
                    rx={2}
                    fill="none"
                    stroke="rgba(250,241,223,0.45)"
                    strokeWidth={1.5}
                  />
                  <circle cx={34} cy={18} r={4.5} fill={COLORS.goldBright} />
                </g>
              );
            })
          )}

          {/* HANNIBAL'S 9 GALLIC/IBERIAN CENTER UNITS (Convex Bulge -> Deep U-Pocket!) */}
          {centerNodes.map((n) => {
            const norm = n / 4; // -1 .. +1
            const parabola = 1 - norm * norm; // 1 at center, 0 at edges
            const x = 960 + n * (94 - concaveP * 10);
            const y = 605 + currentBow * parabola;
            const tangentAngle =
              Math.atan2(currentBow * (-2 * norm), 360) * (180 / Math.PI);

            return (
              <g
                key={`cen-${n}`}
                transform={`translate(${x}, ${y}) rotate(${tangentAngle}) scale(${enterP})`}
              >
                <rect
                  x={-38}
                  y={-17}
                  width={76}
                  height={34}
                  rx={5}
                  fill={COLORS.gold}
                  stroke={COLORS.ink}
                  strokeWidth={2.8}
                />
                <circle r={5} fill={COLORS.ink} />
              </g>
            );
          })}

          {/* HANNIBAL'S ELITE AFRICAN HEAVY FLANKS (Left & Right Columns Pivoting Inward in Phase 4!) */}
          {[-1, 1].map((side) =>
            [0, 1, 2, 3].map((idx) => {
              // Start vertical along outer edges of crescent, then clamp inward horizontally against Roman sides!
              const startX = 960 + side * 455;
              const startY = 560 + idx * 48;
              const clampedX = 960 + side * (310 - pincerP * 18);
              const clampedY = 395 + idx * 58;

              const x = interpolate(flanksP, [0, 1], [startX, clampedX]);
              const y = interpolate(flanksP, [0, 1], [startY, clampedY]);
              const rot = interpolate(flanksP, [0, 1], [0, side * 88]);

              return (
                <g
                  key={`flank-${side}-${idx}`}
                  transform={`translate(${x}, ${y}) rotate(${rot}) scale(${enterP})`}
                >
                  <rect
                    x={-42}
                    y={-19}
                    width={84}
                    height={38}
                    rx={5}
                    fill={COLORS.carthage}
                    stroke={COLORS.ink}
                    strokeWidth={3}
                  />
                  <line
                    x1={-24}
                    y1={0}
                    x2={24}
                    y2={0}
                    stroke={COLORS.chalk}
                    strokeWidth={3}
                  />
                </g>
              );
            })
          )}

          {/* Phase 2 Roman Downward Charge Arrows */}
          {frame >= impactStart && frame < flanksStart && (
            <g opacity={1 - concaveP * 0.65}>
              {[-220, 0, 220].map((dx, i) => (
                <g key={i} transform={`translate(${960 + dx}, ${160 + impactP * 55})`}>
                  <path
                    d="M 0 -45 L 0 28"
                    stroke={COLORS.romeDark}
                    strokeWidth={12}
                    strokeLinecap="round"
                  />
                  <polygon points="-20,20 20,20 0,50" fill={COLORS.romeDark} />
                </g>
              ))}
            </g>
          )}

          {/* Phase 2 Collision Starbursts (Inspired by Reference Frame 4, Pure Vector!) */}
          {frame >= impactStart && frame < concaveStart + 18 && (
            <g>
              {[-270, -140, 0, 140, 270].map((dx, idx) => {
                const burstScale = interpolate(
                  frame - impactStart - idx * 1.5,
                  [0, 6, 36, 48],
                  [0, 1.15, 0.9, 0],
                  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
                );
                const parabola = 1 - Math.pow(dx / 380, 2);
                const by = 565 + currentBow * parabola;
                return (
                  <Starburst
                    key={idx}
                    x={960 + dx}
                    y={by}
                    scale={burstScale}
                    seed={idx + 3}
                  />
                );
              })}
            </g>
          )}

          {/* Phase 4 Flank Clamp Arrows */}
          {frame >= flanksStart && (
            <g opacity={flanksP}>
              <g transform={`translate(${545 + flanksP * 40}, 485)`}>
                <path d="M -55 0 L 18 0" stroke={COLORS.carthageDark} strokeWidth={12} strokeLinecap="round" />
                <polygon points="10,-20 10,20 42,0" fill={COLORS.carthageDark} />
              </g>
              <g transform={`translate(${1375 - flanksP * 40}, 485)`}>
                <path d="M 55 0 L -18 0" stroke={COLORS.carthageDark} strokeWidth={12} strokeLinecap="round" />
                <polygon points="-10,-20 -10,20 -42,0" fill={COLORS.carthageDark} />
              </g>
            </g>
          )}

          {/* Phase 5 Sweeping Rear Cavalry Envelopment Arcs */}
          {frame >= pincerStart && (
            <g>
              <path
                d={leftCavPath}
                fill="none"
                stroke={COLORS.gold}
                strokeWidth={14}
                strokeLinecap="round"
                strokeDasharray={leftCavEv.strokeDasharray}
                strokeDashoffset={leftCavEv.strokeDashoffset}
              />
              <path
                d={rightCavPath}
                fill="none"
                stroke={COLORS.gold}
                strokeWidth={14}
                strokeLinecap="round"
                strokeDasharray={rightCavEv.strokeDasharray}
                strokeDashoffset={rightCavEv.strokeDashoffset}
              />

              {/* Rear Gate Slammed Bar */}
              {sealPop > 0.05 && (
                <g transform={`translate(960, 225) scale(${sealPop})`}>
                  <rect
                    x={-250}
                    y={-22}
                    width={500}
                    height={44}
                    rx={6}
                    fill={COLORS.ink}
                    stroke={COLORS.goldBright}
                    strokeWidth={3.5}
                  />
                  <text
                    x={0}
                    y={8}
                    textAnchor="middle"
                    fontFamily={FONTS.mono}
                    fontSize={21}
                    fontWeight={700}
                    fill={COLORS.goldBright}
                    letterSpacing="0.16em"
                  >
                    REAR EXIT SEALED · 360° TRAP
                  </text>
                </g>
              )}
            </g>
          )}
        </svg>
      </div>

      {/* Top-Left Live Tactical Phase HUD */}
      <div
        style={{
          position: "absolute",
          top: 98,
          left: 84,
          background: COLORS.ink,
          color: COLORS.chalk,
          padding: "14px 26px",
          borderLeft: `8px solid ${phaseColor}`,
          boxShadow: "0 10px 24px rgba(0,0,0,0.22)",
          display: "flex",
          alignItems: "center",
          gap: 14,
        }}
      >
        <Icon icon="game-icons:crossed-swords" width={28} height={28} color={COLORS.goldBright} />
        <span
          style={{
            fontFamily: FONTS.mono,
            fontSize: 20,
            fontWeight: 700,
            letterSpacing: "0.08em",
          }}
        >
          {phaseTag}
        </span>
      </div>
    </AbsoluteFill>
  );
};
