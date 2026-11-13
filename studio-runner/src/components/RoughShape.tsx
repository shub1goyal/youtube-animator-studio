import React, { useMemo } from "react";
import rough from "roughjs/bin/rough";
import type { Options } from "roughjs/bin/core";

interface RoughRectProps {
  x: number;
  y: number;
  width: number;
  height: number;
  options?: Options;
  seed?: number;
}

function renderDrawableToPaths(
  drawable: ReturnType<ReturnType<typeof rough.generator>["rectangle"]>
) {
  const gen = rough.generator();
  const info = gen.toPaths(drawable);
  return info.map((p, idx) => (
    <path
      key={idx}
      d={p.d}
      stroke={p.stroke}
      strokeWidth={p.strokeWidth}
      fill={p.fill || "none"}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  ));
}

export const RoughRect: React.FC<RoughRectProps> = ({
  x,
  y,
  width,
  height,
  options,
  seed = 11,
}) => {
  const paths = useMemo(() => {
    const gen = rough.generator();
    const d = gen.rectangle(x, y, width, height, {
      roughness: 1.35,
      bowing: 1.1,
      stroke: "#1A1613",
      strokeWidth: 3,
      seed,
      ...options,
    });
    return renderDrawableToPaths(d);
  }, [x, y, width, height, seed, options]);

  return <g>{paths}</g>;
};

interface RoughCircleProps {
  cx: number;
  cy: number;
  diameter: number;
  options?: Options;
  seed?: number;
}

export const RoughCircle: React.FC<RoughCircleProps> = ({
  cx,
  cy,
  diameter,
  options,
  seed = 17,
}) => {
  const paths = useMemo(() => {
    const gen = rough.generator();
    const d = gen.circle(cx, cy, diameter, {
      roughness: 1.3,
      stroke: "#1A1613",
      strokeWidth: 3,
      seed,
      ...options,
    });
    return renderDrawableToPaths(d);
  }, [cx, cy, diameter, seed, options]);

  return <g>{paths}</g>;
};

interface RoughLineProps {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  options?: Options;
  seed?: number;
}

export const RoughLine: React.FC<RoughLineProps> = ({
  x1,
  y1,
  x2,
  y2,
  options,
  seed = 23,
}) => {
  const paths = useMemo(() => {
    const gen = rough.generator();
    const d = gen.line(x1, y1, x2, y2, {
      roughness: 1.6,
      bowing: 1.2,
      stroke: "#B82925",
      strokeWidth: 6,
      seed,
      ...options,
    });
    return renderDrawableToPaths(d);
  }, [x1, y1, x2, y2, seed, options]);

  return <g>{paths}</g>;
};
