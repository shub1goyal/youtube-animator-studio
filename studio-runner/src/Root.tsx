import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";
import timelineData from "./data/timeline.json";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CannaeProof"
        component={MainVideo}
        durationInFrames={timelineData.totalFrames}
        fps={timelineData.fps}
        width={1920}
        height={1080}
      />
    </>
  );
};
