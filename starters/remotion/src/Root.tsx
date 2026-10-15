import React from "react";
import { Composition } from "remotion";
import { Film, type FilmProps } from "./Film";

export const FPS = 30;
export const DEFAULT_SECONDS = 12;

export const defaultFilmProps: FilmProps = {
  title: "حرّك فكرتك بالأرقام",
  words: ["موشن", "عربي", "بيانات", "Remotion"],
  accent: "#ff7a1a",
  lang: "ar",
};

export const Root: React.FC = () => {
  return (
    <Composition
      id="KosifFilm"
      component={Film}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={DEFAULT_SECONDS * FPS}
      defaultProps={defaultFilmProps}
    />
  );
};
