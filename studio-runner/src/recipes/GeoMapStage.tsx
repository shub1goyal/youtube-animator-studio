import React, { useMemo } from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { evolvePath } from "@remotion/paths";
import { geoMercator, geoPath } from "d3-geo";
import { feature } from "topojson-client";
import worldData from "world-atlas/countries-110m.json";
import { Icon } from "@iconify/react";
import { COLORS, FONTS, SPRINGS } from "../theme/tokens";
import { RoughRect } from "../components/RoughShape";

export const GeoMapStage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const { landPaths, carthagePt, cannaePt, romePt, routePathD } = useMemo(() => {
    const countries = feature(
      worldData as any,
      (worldData as any).objects.countries
    ) as any;

    const projection = geoMercator()
      .center([13.2, 40.2])
      .scale(2550)
      .translate([960, 540]);

    const pathGen = geoPath().projection(projection);
    const paths = countries.features
      .map((f: any) => pathGen(f))
      .filter(Boolean) as string[];

    const carthage = projection([10.32, 36.85]) || [780, 740];
    const alps = projection([7.2, 44.8]) || [640, 250];
    const cannae = projection([16.15, 41.3]) || [1120, 460];
    const rome = projection([12.49, 41.9]) || [920, 420];

    const d = `M ${carthage[0]} ${carthage[1]} Q ${alps[0] - 90} ${alps[1] + 40} ${alps[0]} ${alps[1]} T ${cannae[0]} ${cannae[1]}`;

    return {
      landPaths: paths,
      carthagePt: carthage,
      cannaePt: cannae,
      romePt: rome,
      routePathD: d,
    };
  }, []);

  const camScale = interpolate(frame, [0, durationInFrames], [1.02, 1.24], {
    extrapolateRight: "clamp",
  });
  const camX = interpolate(frame, [0, durationInFrames], [0, -75], {
    extrapolateRight: "clamp",
  });
  const camY = interpolate(frame, [0, durationInFrames], [0, 28], {
    extrapolateRight: "clamp",
  });

  const routeProgress = interpolate(frame, [4, Math.max(18, durationInFrames - 18)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const evolved = evolvePath(routeProgress, routePathD);

  const pinPop = spring({
    frame: frame - 14,
    fps,
    config: SPRINGS.bouncy,
  });

  const cardPop = spring({
    frame: frame - 8,
    fps,
    config: SPRINGS.snappy,
  });

  const pulseRadius = interpolate((frame % 30) / 30, [0, 1], [16, 58]);
  const pulseOpacity = interpolate((frame % 30) / 30, [0, 1], [0.75, 0]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {/* Sea & Cartographic Map Layer */}
      <div
        style={{
          width: 1920,
          height: 1080,
          transform: `translate(${camX}px, ${camY}px) scale(${camScale})`,
          transformOrigin: `${cannaePt[0]}px ${cannaePt[1]}px`,
        }}
      >
        <svg width="1920" height="1080" viewBox="0 0 1920 1080">
          <defs>
            <radialGradient id="med-sea" cx="50%" cy="50%" r="65%">
              <stop offset="0%" stopColor={COLORS.seaFill} />
              <stop offset="100%" stopColor={COLORS.seaDeep} />
            </radialGradient>
            <filter id="land-shadow" x="-5%" y="-5%" width="110%" height="110%">
              <feDropShadow dx="3" dy="5" stdDeviation="4" floodColor="#3A2E21" floodOpacity="0.24" />
            </filter>
          </defs>

          <rect width="1920" height="1080" fill="url(#med-sea)" />

          {/* Latitude / Longitude Graticule Lines */}
          {[240, 420, 600, 780].map((y) => (
            <line
              key={`lat-${y}`}
              x1={0}
              y1={y}
              x2={1920}
              y2={y}
              stroke="rgba(26,22,19,0.10)"
              strokeDasharray="8 8"
              strokeWidth={1.5}
            />
          ))}
          {[480, 780, 1080, 1380].map((x) => (
            <line
              key={`lon-${x}`}
              x1={x}
              y1={0}
              x2={x}
              y2={1080}
              stroke="rgba(26,22,19,0.10)"
              strokeDasharray="8 8"
              strokeWidth={1.5}
            />
          ))}

          {/* Real Natural Earth Coastlines */}
          <g filter="url(#land-shadow)">
            {landPaths.map((d, idx) => (
              <path
                key={idx}
                d={d}
                fill={COLORS.landFill}
                stroke={COLORS.landStroke}
                strokeWidth={2.4}
                strokeLinejoin="round"
              />
            ))}
          </g>

          {/* Animated Invasion Route: Carthage -> Alps -> Cannae */}
          <path
            d={routePathD}
            fill="none"
            stroke={COLORS.carthage}
            strokeWidth={7}
            strokeLinecap="round"
            strokeDasharray={evolved.strokeDasharray}
            strokeDashoffset={evolved.strokeDashoffset}
          />

          {/* Origin Marker: Carthage */}
          <g transform={`translate(${carthagePt[0]}, ${carthagePt[1]})`}>
            <circle r={9} fill={COLORS.carthage} stroke={COLORS.parchmentCenter} strokeWidth={3} />
            <text
              x={16}
              y={6}
              fontFamily={FONTS.mono}
              fontSize={19}
              fontWeight={700}
              fill={COLORS.carthageDark}
            >
              CARTHAGE
            </text>
          </g>

          {/* Reference Marker: Rome */}
          <g transform={`translate(${romePt[0]}, ${romePt[1]})`}>
            <circle r={8} fill={COLORS.rome} stroke={COLORS.parchmentCenter} strokeWidth={2.5} />
            <text
              x={-72}
              y={-12}
              fontFamily={FONTS.mono}
              fontSize={18}
              fontWeight={700}
              fill={COLORS.romeDark}
            >
              ROME
            </text>
          </g>

          {/* Target Battle Marker: CANNAE */}
          <g
            transform={`translate(${cannaePt[0]}, ${cannaePt[1]}) scale(${pinPop})`}
          >
            <circle
              r={pulseRadius}
              fill="none"
              stroke={COLORS.rome}
              strokeWidth={4}
              opacity={pulseOpacity}
            />
            <circle r={17} fill={COLORS.rome} stroke={COLORS.parchmentCenter} strokeWidth={4} />
            <circle r={6} fill={COLORS.goldBright} />

            {/* Callout Label */}
            <g transform="translate(26, -34)">
              <RoughRect
                x={0}
                y={0}
                width={275}
                height={74}
                options={{
                  fill: COLORS.parchmentCenter,
                  fillStyle: "solid",
                  stroke: COLORS.ink,
                  strokeWidth: 3,
                }}
              />
              <text
                x={18}
                y={33}
                fontFamily={FONTS.display}
                fontSize={26}
                fontWeight={900}
                fill={COLORS.rome}
              >
                CANNAE
              </text>
              <text
                x={18}
                y={58}
                fontFamily={FONTS.mono}
                fontSize={16}
                fontWeight={700}
                fill={COLORS.inkSoft}
              >
                SOUTHERN ITALY · 216 BC
              </text>
            </g>
          </g>
        </svg>
      </div>

      {/* Top-Left Title Stamp Card */}
      <div
        style={{
          position: "absolute",
          top: 112,
          left: 92,
          transform: `translateY(${interpolate(cardPop, [0, 1], [28, 0])}px)`,
          opacity: cardPop,
          background: "rgba(250, 241, 223, 0.95)",
          border: `3px solid ${COLORS.ink}`,
          boxShadow: "8px 8px 0px rgba(26,22,19,0.85)",
          padding: "22px 30px",
          maxWidth: 540,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            fontFamily: FONTS.mono,
            fontSize: 17,
            fontWeight: 700,
            color: COLORS.rome,
            letterSpacing: "0.12em",
            marginBottom: 6,
          }}
        >
          <Icon icon="lucide:compass" width={22} height={22} />
          <span>SECOND PUNIC WAR · APULIA</span>
        </div>
        <div
          style={{
            fontFamily: FONTS.display,
            fontSize: 44,
            fontWeight: 900,
            lineHeight: 1.08,
            color: COLORS.ink,
          }}
        >
          AUGUST 2, 216 BC
        </div>
        <div
          style={{
            fontFamily: FONTS.sans,
            fontSize: 21,
            fontWeight: 500,
            color: COLORS.inkSoft,
            marginTop: 6,
          }}
        >
          1,500 miles from Carthage — deep inside Roman territory
        </div>
      </div>
    </AbsoluteFill>
  );
};
