import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { evolvePath } from "@remotion/paths";
import { Icon } from "@iconify/react";
import { COLORS, FONTS, SPRINGS } from "../theme/tokens";
import { RoughRect } from "../components/RoughShape";
import { StickmanActor } from "../components/StickmanActor";

interface MythGambitStageProps {
  flipStartFrame: number;
}

export const MythGambitStage: React.FC<MythGambitStageProps> = ({ flipStartFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cardIn = spring({
    frame,
    fps,
    config: SPRINGS.snappy,
  });

  const isFlipped = frame >= flipStartFrame;
  const flipFrame = Math.max(0, frame - flipStartFrame);

  const slashProgress = interpolate(flipFrame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  const stampIn = spring({
    frame: flipFrame - 6,
    fps,
    config: SPRINGS.bouncy,
  });

  const bendProgress = spring({
    frame: flipFrame - 3,
    fps,
    config: SPRINGS.heavy,
  });

  const shakeX =
    isFlipped && flipFrame < 8
      ? Math.sin(flipFrame * 2.8) * (8 - flipFrame) * 1.4
      : 0;
  const stageScale = isFlipped
    ? interpolate(stampIn, [0, 1], [1.0, 1.055])
    : interpolate(cardIn, [0, 1], [0.94, 1.0]);

  const slashPath1 = "M 320 425 Q 960 398 1600 375";
  const slashPath2 = "M 335 445 Q 960 422 1585 402";
  const ev1 = evolvePath(slashProgress, slashPath1);
  const ev2 = evolvePath(slashProgress, slashPath2);

  const blockIndices = [-3, -2, -1, 0, 1, 2, 3];

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        transform: `translateX(${shakeX}px) scale(${stageScale})`,
      }}
    >
      {/* STICKMAN ACTOR: Hannibal thinking / scheming */}
      <StickmanActor
        x={75}
        y={490}
        scale={0.78}
        pose={isFlipped ? "smug_point" : "thinking"}
        expression={isFlipped ? "smirk" : "confident"}
        costume="alexander_greek"
      />

      {/* Main Doctrine Poster */}
      <div
        style={{
          position: "relative",
          width: 1380,
          height: 680,
          marginLeft: 140,
          opacity: cardIn,
          transform: `translateY(${interpolate(cardIn, [0, 1], [35, 0])}px)`,
        }}
      >
        <svg
          width="1380"
          height="680"
          style={{ position: "absolute", inset: 0, overflow: "visible" }}
        >
          <RoughRect
            x={0}
            y={0}
            width={1380}
            height={680}
            options={{
              fill: COLORS.parchmentCard,
              fillStyle: "solid",
              stroke: COLORS.ink,
              strokeWidth: 4,
            }}
          />
        </svg>

        {/* Top Label */}
        <div
          style={{
            position: "relative",
            paddingTop: 46,
            textAlign: "center",
            fontFamily: FONTS.mono,
            fontSize: 21,
            fontWeight: 700,
            letterSpacing: "0.2em",
            color: COLORS.inkMuted,
          }}
        >
          CLASSICAL INFANTRY DOCTRINE · AXIOM #01
        </div>

        {/* Giant Doctrine Headline */}
        <div
          style={{
            position: "relative",
            marginTop: 28,
            textAlign: "center",
            fontFamily: FONTS.display,
            fontSize: 66,
            fontWeight: 900,
            letterSpacing: "0.02em",
            color: isFlipped ? "rgba(26,22,19,0.36)" : COLORS.ink,
            padding: "0 60px",
            lineHeight: 1.12,
          }}
        >
          “NEVER LET YOUR CENTER BEND.”
        </div>

        {/* Live 7-Unit Tactical Line Schematic */}
        <div
          style={{
            position: "relative",
            marginTop: 58,
            height: 210,
            display: "flex",
            justifyContent: "center",
            alignItems: "flex-start",
            gap: 24,
          }}
        >
          {blockIndices.map((pos, idx) => {
            const centerWeight = 1 - Math.abs(pos) / 3.4;
            const yOffset = isFlipped ? bendProgress * centerWeight * 108 : 0;
            const rot = isFlipped ? bendProgress * pos * -5.5 : 0;
            const unitEnter = spring({
              frame: frame - 5 - idx * 2,
              fps,
              config: SPRINGS.snappy,
            });
            const isFlank = Math.abs(pos) === 3;
            return (
              <div
                key={pos}
                style={{
                  width: 120,
                  height: 68,
                  background: isFlank
                    ? COLORS.carthageDark
                    : isFlipped
                    ? COLORS.gold
                    : COLORS.ink,
                  border: `3px solid ${COLORS.ink}`,
                  borderRadius: 6,
                  boxShadow: "4px 5px 0px rgba(26,22,19,0.35)",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  color: COLORS.parchmentCenter,
                  transform: `translateY(${yOffset}px) rotate(${rot}deg) scale(${unitEnter})`,
                }}
              >
                <Icon
                  icon={isFlank ? "lucide:shield" : "lucide:minus"}
                  width={30}
                  height={30}
                />
              </div>
            );
          })}
        </div>

        {/* Flip Stamp Banner */}
        {isFlipped && (
          <div
            style={{
              position: "absolute",
              bottom: 42,
              left: 0,
              right: 0,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                transform: `scale(${stampIn}) rotate(-1.6deg)`,
                background: COLORS.rome,
                color: COLORS.parchmentCenter,
                padding: "16px 46px",
                border: `4px solid ${COLORS.ink}`,
                boxShadow: "8px 8px 0px rgba(26,22,19,0.9)",
                fontFamily: FONTS.display,
                fontSize: 42,
                fontWeight: 900,
                letterSpacing: "0.04em",
                display: "flex",
                alignItems: "center",
                gap: 18,
              }}
            >
              <Icon icon="lucide:zap" width={36} height={36} color={COLORS.goldBright} />
              <span>HANNIBAL BENT HIS ON PURPOSE</span>
            </div>
          </div>
        )}
      </div>

      {/* Double Hand-Inked Crimson Strike-Through Overlay */}
      {isFlipped && (
        <svg
          width="1920"
          height="1080"
          style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
        >
          <path
            d={slashPath1}
            fill="none"
            stroke={COLORS.rome}
            strokeWidth={13}
            strokeLinecap="round"
            strokeDasharray={ev1.strokeDasharray}
            strokeDashoffset={ev1.strokeDashoffset}
          />
          <path
            d={slashPath2}
            fill="none"
            stroke={COLORS.romeDark}
            strokeWidth={7}
            strokeLinecap="round"
            strokeDasharray={ev2.strokeDasharray}
            strokeDashoffset={ev2.strokeDashoffset}
          />
        </svg>
      )}
    </AbsoluteFill>
  );
};
