import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import timelineData from "./data/timeline.json";
import { BeatItem, InkPressChrome, WordItem } from "./components/InkPressChrome";
import { StickmanActor } from "./components/StickmanActor";
import { Icon } from "@iconify/react";
import { COLORS, FONTS } from "./theme/tokens";
import { RoughRect } from "./components/RoughShape";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const beats = timelineData.beats as BeatItem[];
  const words = timelineData.words as WordItem[];

  const activeBeat =
    beats.find((b) => frame >= b.startFrame && frame < b.endFrame) ||
    beats[beats.length - 1];

  const b0 = beats[0]; // 0.0 - 5.5s
  const b1 = beats[1]; // 5.5 - 10.5s
  const b2 = beats[2]; // 10.5 - 15.7s
  const b3 = beats[3]; // 15.7 - 18.6s
  const b4 = beats[4]; // 18.6 - 21.8s
  const b5 = beats[5]; // 21.8 - 27.3s
  const b6 = beats[6]; // 27.3 - 33.3s
  const b7 = beats[7]; // 33.3 - 38.0s
  const b8 = beats[8]; // 38.0 - 40.7s

  const isDark = activeBeat.index === 4 || activeBeat.index === 5; // Night crossing

  return (
    <AbsoluteFill>
      <Audio src={staticFile(timelineData.audioSrc)} />

      {/* Shared Archival Chrome + Word Subtitles */}
      <InkPressChrome
        darkMode={isDark}
        chapter={activeBeat.chapter}
        beatIndex={activeBeat.index}
        totalBeats={beats.length}
        words={words}
        activeBeat={activeBeat}
      />

      {/* SCENE 1: Alexander at India's Border (0.0s -> 5.5s) */}
      <Sequence from={b0.startFrame} durationInFrames={b0.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <StickmanActor
            x={760}
            y={460}
            scale={1.15}
            pose="smug_point"
            expression="confident"
            costume="alexander_greek"
          />
          {/* Border Post Landmark */}
          <div style={{ position: "absolute", left: 1220, top: 320, width: 28, height: 420, background: COLORS.ink }} />
          <div style={{ position: "absolute", left: 1180, top: 290, padding: "12px 24px", background: COLORS.rome, color: COLORS.chalk, border: `3px solid ${COLORS.ink}`, fontFamily: FONTS.display, fontSize: 28, fontWeight: 900 }}>
            INDIA BORDER · 326 BC
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* SCENE 2: The Standoff — Alexander vs King Porus & War Elephant (5.5s -> 10.5s) */}
      <Sequence from={b1.startFrame} durationInFrames={b1.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          {/* Shocked Alexander Left */}
          <StickmanActor
            x={280}
            y={490}
            scale={0.95}
            pose="shocked"
            expression="scared"
            costume="alexander_greek"
          />

          {/* King Porus Right */}
          <StickmanActor
            x={1320}
            y={490}
            scale={1.05}
            pose="arms_crossed"
            expression="confident"
            costume="porus_indian"
            flipX={true}
          />

          {/* Giant 200 War Elephant Badge Center */}
          <div style={{ position: "absolute", left: "50%", top: "42%", transform: "translate(-50%, -50%)", textAlign: "center" }}>
            <div style={{ width: 190, height: 190, borderRadius: "50%", background: COLORS.carthage, border: `6px solid ${COLORS.gold}`, display: "flex", justifyContent: "center", alignItems: "center", margin: "0 auto", boxShadow: "0 18px 40px rgba(0,0,0,0.3)" }}>
              <Icon icon="game-icons:elephant" width={130} height={130} color={COLORS.goldBright} />
            </div>
            <div style={{ fontFamily: FONTS.mono, fontSize: 56, fontWeight: 700, color: COLORS.rome, marginTop: 14 }}>
              200 WAR ELEPHANTS
            </div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 22, fontWeight: 700, color: COLORS.inkMuted }}>
              KING PORUS · JHELUM RIVER FRONT
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* SCENE 3: Greek Horses Terrified & Running (10.5s -> 15.7s) */}
      <Sequence from={b2.startFrame} durationInFrames={b2.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          {/* Running Scared Greek Soldier */}
          <StickmanActor
            x={340}
            y={500}
            scale={0.9}
            pose="running_scared"
            expression="scared"
            costume="alexander_greek"
          />
          <StickmanActor
            x={640}
            y={520}
            scale={0.82}
            pose="running_scared"
            expression="scared"
            costume="alexander_greek"
          />

          {/* Elephant Roar Soundwave Icon Card */}
          <div style={{ position: "absolute", right: 180, top: 260, width: 680, padding: 36, background: COLORS.parchmentCard, border: `4px solid ${COLORS.rome}`, boxShadow: "10px 10px 0 rgba(26,22,19,0.85)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
              <Icon icon="game-icons:cavalry" width={64} height={64} color={COLORS.rome} />
              <div>
                <div style={{ fontFamily: FONTS.mono, fontSize: 18, color: COLORS.rome, fontWeight: 700 }}>CAVALRY PANIC REACTION</div>
                <div style={{ fontFamily: FONTS.display, fontSize: 44, fontWeight: 900, color: COLORS.ink }}>HORSES REFUSED TO ADVANCE</div>
              </div>
            </div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 24, marginTop: 14, color: COLORS.inkSoft }}>
              Trunk roars and foreign smell caused complete panic in Greek mounts.
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* SCENE 4: Alexander's Scheme (15.7s -> 18.6s) */}
      <Sequence from={b3.startFrame} durationInFrames={b3.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <StickmanActor
            x={420}
            y={480}
            scale={1.1}
            pose="thinking"
            expression="scheming"
            costume="alexander_greek"
          />
          {/* Idea Lightbulb / Mindgame Banner */}
          <div style={{ position: "absolute", left: 980, top: 340, padding: "26px 48px", background: COLORS.ink, color: COLORS.goldBright, border: `4px solid ${COLORS.goldBright}`, boxShadow: "12px 12px 0 rgba(0,0,0,0.4)" }}>
            <div style={{ fontFamily: FONTS.mono, fontSize: 20, letterSpacing: "0.16em" }}>STRATAGEM #01</div>
            <div style={{ fontFamily: FONTS.display, fontSize: 52, fontWeight: 900, marginTop: 6 }}>PSYCHOLOGICAL FEINT</div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* SCENE 5: Night Feint / Loud Camps (18.6s -> 21.8s) */}
      <Sequence from={b4.startFrame} durationInFrames={b4.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <StickmanActor
            x={320}
            y={490}
            scale={0.95}
            pose="shouting_charge"
            expression="angry_shout"
            costume="alexander_greek"
          />
          {/* Night Drums & Camp Noise Radar */}
          <div style={{ position: "absolute", right: 260, top: 290, width: 780, padding: 36, background: "rgba(18,15,13,0.92)", border: `3px solid ${COLORS.gold}`, borderRadius: 12 }}>
            <div style={{ fontFamily: FONTS.mono, fontSize: 20, color: COLORS.goldBright }}>NIGHT EXHAUSTION TACTIC</div>
            <div style={{ fontFamily: FONTS.display, fontSize: 44, color: COLORS.chalk, marginTop: 8, fontWeight: 900 }}>
              FAKE NIGHT ALARMS
            </div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 24, color: "rgba(246,239,226,0.72)", marginTop: 10 }}>
              Alexander marched up and down shouting every night until Porus stopped reacting.
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* SCENE 6: Storm Crossing (21.8s -> 27.3s) */}
      <Sequence from={b5.startFrame} durationInFrames={b5.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          {/* Thunder Storm River Crossing */}
          <div style={{ width: 1400, padding: 48, background: "rgba(18,15,13,0.95)", border: `4px solid ${COLORS.rome}`, boxShadow: "14px 14px 0 rgba(0,0,0,0.6)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{ fontFamily: FONTS.mono, fontSize: 22, color: COLORS.rome }}>SECRET RIVER FLANK</div>
                <div style={{ fontFamily: FONTS.display, fontSize: 62, fontWeight: 900, color: COLORS.chalk, marginTop: 8 }}>
                  17 MILES UPSTREAM
                </div>
              </div>
              <Icon icon="game-icons:compass" width={96} height={96} color={COLORS.goldBright} />
            </div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 28, color: "rgba(246,239,226,0.85)", marginTop: 22, lineHeight: 1.4 }}>
              Under heavy monsoon rain and thunder, Alexander crossed the flooded Jhelum River undetected.
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* SCENE 7: Archers Target Elephants (27.3s -> 33.3s) */}
      <Sequence from={b6.startFrame} durationInFrames={b6.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <StickmanActor
            x={260}
            y={500}
            scale={0.92}
            pose="smug_point"
            expression="confident"
            costume="alexander_greek"
          />
          {/* Target Eyes / Mahout Callout */}
          <div style={{ position: "absolute", right: 220, top: 280, width: 840, padding: 40, background: COLORS.parchmentCard, border: `4px solid ${COLORS.ink}`, boxShadow: "10px 10px 0 rgba(26,22,19,0.9)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
              <Icon icon="game-icons:spear-hook" width={68} height={68} color={COLORS.rome} />
              <div>
                <div style={{ fontFamily: FONTS.mono, fontSize: 20, color: COLORS.rome, fontWeight: 700 }}>TACTICAL WEAK POINT</div>
                <div style={{ fontFamily: FONTS.display, fontSize: 46, fontWeight: 900, color: COLORS.ink }}>BLINDING THE ELEPHANTS</div>
              </div>
            </div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 26, color: COLORS.inkSoft, marginTop: 14 }}>
              Greek archers specifically targeted the drivers (mahouts) and elephants' eyes with heavy arrows.
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* SCENE 8: Elephant Stampede Chaos (33.3s -> 38.0s) */}
      <Sequence from={b7.startFrame} durationInFrames={b7.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <div style={{ width: 1360, padding: 52, background: COLORS.rome, border: `5px solid ${COLORS.ink}`, color: COLORS.chalk, boxShadow: "14px 14px 0 rgba(26,22,19,0.95)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
              <Icon icon="game-icons:elephant" width={96} height={96} color={COLORS.goldBright} />
              <div>
                <div style={{ fontFamily: FONTS.mono, fontSize: 22, letterSpacing: "0.14em" }}>THE WEAPON BACKFIRES</div>
                <div style={{ fontFamily: FONTS.display, fontSize: 64, fontWeight: 900, marginTop: 6 }}>
                  UNCONTROLLABLE FRENZY
                </div>
              </div>
            </div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 28, marginTop: 22, lineHeight: 1.4, color: COLORS.chalk }}>
              Blinded and enraged, the war elephants trampled backwards through Porus's own infantry lines.
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* SCENE 9: Respect & Mutual Stand (38.0s -> 40.7s) */}
      <Sequence from={b8.startFrame} durationInFrames={b8.durationFrames}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          {/* Alexander and Porus facing with respect */}
          <StickmanActor
            x={420}
            y={490}
            scale={1.0}
            pose="arms_crossed"
            expression="confident"
            costume="alexander_greek"
          />
          <StickmanActor
            x={1160}
            y={490}
            scale={1.08}
            pose="arms_crossed"
            expression="confident"
            costume="porus_indian"
            flipX={true}
          />
          <div style={{ position: "absolute", top: 180, textAlign: "center" }}>
            <div style={{ fontFamily: FONTS.mono, fontSize: 22, color: COLORS.rome, fontWeight: 700 }}>THE LEGEND OF JHELUM</div>
            <div style={{ fontFamily: FONTS.display, fontSize: 52, fontWeight: 900, color: COLORS.ink, marginTop: 6 }}>
              “TREAT ME LIKE A KING TREATS A KING.”
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
