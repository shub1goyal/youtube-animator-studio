import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Icon } from "@iconify/react";
import { COLORS } from "../theme/tokens";

export type StickPose =
  | "thinking"
  | "smug_point"
  | "shocked"
  | "shouting_charge"
  | "arms_crossed"
  | "running_scared"
  | "bow_aim";

export type StickExpression =
  | "confident"
  | "smirk"
  | "scared"
  | "angry_shout"
  | "scheming";

export type StickCostume =
  | "none"
  | "alexander_greek"
  | "porus_indian"
  | "greek_soldier";

interface StickmanActorProps {
  x?: number;
  y?: number;
  scale?: number;
  pose?: StickPose;
  expression?: StickExpression;
  costume?: StickCostume;
  flipX?: boolean;
}

export const StickmanActor: React.FC<StickmanActorProps> = ({
  x = 0,
  y = 0,
  scale = 1,
  pose = "thinking",
  expression = "smirk",
  costume = "alexander_greek",
  flipX = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Hand-drawn 12fps line boil seed
  const boilSeed = Math.floor(frame / (fps / 12)) % 4;

  // Gentle breathing / idle sway
  const breatheY = Math.sin(frame * 0.12) * 2.2;
  const armSway = Math.sin(frame * 0.16) * 3.5;

  const pop = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 180 },
  });

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `scale(${pop * scale}) scaleX(${flipX ? -1 : 1})`,
        transformOrigin: "bottom center",
        pointerEvents: "none",
        zIndex: 30,
      }}
    >
      <svg
        width="420"
        height="560"
        viewBox="0 0 420 560"
        style={{
          overflow: "visible",
          filter: `url(#line-boil-${boilSeed}) drop-shadow(0 14px 24px rgba(0,0,0,0.18))`,
        }}
      >
        <defs>
          <filter id={`line-boil-${boilSeed}`}>
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.04"
              numOctaves={2}
              seed={boilSeed * 17}
              result="noise"
            />
            <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.2" />
          </filter>
        </defs>

        <g transform={`translate(0, ${breatheY})`}>
          {/* BACK COSTUME / CAPE */}
          {costume === "alexander_greek" && (
            <path
              d="M 175 220 Q 110 360 85 460 Q 185 470 215 450 Q 235 340 235 220 Z"
              fill={COLORS.rome}
              stroke={COLORS.ink}
              strokeWidth="5"
            />
          )}

          {costume === "porus_indian" && (
            <path
              d="M 170 220 Q 130 380 110 490 Q 210 495 245 470 Q 240 330 240 220 Z"
              fill={COLORS.gold}
              stroke={COLORS.ink}
              strokeWidth="5"
            />
          )}

          {/* TORSO */}
          <line
            x1="210"
            y1="210"
            x2="210"
            y2="370"
            stroke={COLORS.ink}
            strokeWidth="7"
            strokeLinecap="round"
          />

          {/* FRONT CHEST PIECE */}
          {costume === "alexander_greek" && (
            <path
              d="M 185 220 Q 210 210 235 220 L 235 320 Q 210 335 185 320 Z"
              fill={COLORS.gold}
              stroke={COLORS.ink}
              strokeWidth="5"
            />
          )}

          {costume === "porus_indian" && (
            <path
              d="M 180 220 Q 210 205 240 220 L 240 340 Q 210 355 180 340 Z"
              fill={COLORS.carthage}
              stroke={COLORS.ink}
              strokeWidth="5"
            />
          )}

          {/* LEGS */}
          {pose === "running_scared" ? (
            <>
              <path d="M 210 370 Q 160 410 130 460" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
              <path d="M 210 370 Q 260 420 300 450" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
            </>
          ) : (
            <>
              <path d="M 210 370 Q 185 430 175 490" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
              <path d="M 210 370 Q 235 430 245 490" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
            </>
          )}

          {/* ARMS BASED ON POSE */}
          {pose === "thinking" && (
            <>
              <path d="M 185 225 Q 145 270 165 315" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
              <path d="M 235 225 Q 285 220 280 145" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
              <circle cx="280" cy="140" r="8" fill={COLORS.chalk} stroke={COLORS.ink} strokeWidth="4" />
            </>
          )}

          {pose === "smug_point" && (
            <>
              <path d="M 185 225 Q 160 270 170 315" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
              <path d={`M 235 225 Q 320 200 375 ${180 + armSway}`} fill="none" stroke={COLORS.ink} strokeWidth="8" strokeLinecap="round" />
              <polygon points={`375,${170 + armSway} 395,${180 + armSway} 375,${190 + armSway}`} fill={COLORS.ink} />
            </>
          )}

          {pose === "shocked" && (
            <>
              <path d="M 185 225 Q 130 180 145 130" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
              <path d="M 235 225 Q 290 180 275 130" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
            </>
          )}

          {pose === "running_scared" && (
            <>
              <path d="M 185 225 Q 120 240 100 200" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
              <path d="M 235 225 Q 290 270 310 240" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
            </>
          )}

          {pose === "arms_crossed" && (
            <>
              <path d="M 185 235 Q 225 295 240 275" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
              <path d="M 235 235 Q 195 295 180 275" fill="none" stroke={COLORS.ink} strokeWidth="7" strokeLinecap="round" />
            </>
          )}

          {/* HEAD: Clean Comic Circle */}
          <circle cx="210" cy="130" r="65" fill={COLORS.chalk} stroke={COLORS.ink} strokeWidth="6" />

          {/* HAIR / HEADWEAR */}
          {costume === "alexander_greek" && (
            <>
              <path d="M 165 95 Q 185 60 215 70 Q 240 55 260 90" fill="none" stroke={COLORS.ink} strokeWidth="6" strokeLinecap="round" />
              <g transform="translate(162, 50)">
                <Icon icon="game-icons:laurel-crown" width="96" height="48" color={COLORS.gold} />
              </g>
            </>
          )}

          {costume === "porus_indian" && (
            <>
              {/* Royal Indian Turban / Crown */}
              <ellipse cx="210" cy="85" rx="66" ry="32" fill={COLORS.gold} stroke={COLORS.ink} strokeWidth="5" />
              <circle cx="210" cy="62" r="10" fill={COLORS.rome} stroke={COLORS.ink} strokeWidth="3" />
              <path d="M 210 52 Q 225 32 230 18 Q 218 36 210 52" fill={COLORS.rome} stroke={COLORS.ink} strokeWidth="2.5" />
              {/* Mustache */}
              <path d="M 195 152 Q 210 148 225 152 Q 235 158 245 152" fill="none" stroke={COLORS.ink} strokeWidth="6" strokeLinecap="round" />
            </>
          )}

          {/* FACIAL EXPRESSIONS */}
          {expression === "smirk" && (
            <>
              <path d="M 180 105 Q 195 95 208 108" fill="none" stroke={COLORS.ink} strokeWidth="5" strokeLinecap="round" />
              <path d="M 225 108 Q 240 102 255 106" fill="none" stroke={COLORS.ink} strokeWidth="5" strokeLinecap="round" />
              <circle cx="196" cy="124" r="6" fill={COLORS.ink} />
              <circle cx="242" cy="124" r="6" fill={COLORS.ink} />
              <path d="M 205 155 Q 235 165 248 142" fill="none" stroke={COLORS.ink} strokeWidth="5" strokeLinecap="round" />
            </>
          )}

          {expression === "confident" && (
            <>
              <line x1="182" y1="108" x2="208" y2="108" stroke={COLORS.ink} strokeWidth="5" strokeLinecap="round" />
              <line x1="225" y1="108" x2="252" y2="108" stroke={COLORS.ink} strokeWidth="5" strokeLinecap="round" />
              <circle cx="196" cy="124" r="6" fill={COLORS.ink} />
              <circle cx="240" cy="124" r="6" fill={COLORS.ink} />
              <path d="M 205 150 Q 220 162 238 150" fill="none" stroke={COLORS.ink} strokeWidth="5" strokeLinecap="round" />
            </>
          )}

          {expression === "scared" && (
            <>
              <path d="M 182 105 Q 198 116 210 108" fill="none" stroke={COLORS.ink} strokeWidth="5" strokeLinecap="round" />
              <path d="M 225 108 Q 238 116 254 105" fill="none" stroke={COLORS.ink} strokeWidth="5" strokeLinecap="round" />
              <ellipse cx="196" cy="126" rx="8" ry="12" fill={COLORS.ink} />
              <ellipse cx="240" cy="126" rx="8" ry="12" fill={COLORS.ink} />
              <ellipse cx="218" cy="162" rx="14" ry="18" fill={COLORS.ink} />
            </>
          )}
        </g>
      </svg>
    </div>
  );
};
