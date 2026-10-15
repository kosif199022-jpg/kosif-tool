import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Captions } from "./Captions";
import { easeInOutCubic, easeOutCubic, easeOutExpo, progress, staggerStart } from "./easing";

export type Lang = "ar" | "en";

export type FilmProps = {
  /** Headline, revealed word by word in scene 1 and repeated on the closing card. */
  title: string;
  /** Keywords shown as pills under the headline. */
  words: string[];
  /** Accent colour: any CSS colour, 6-digit hex recommended. */
  accent: string;
  /** Drives text direction and the built-in UI strings. */
  lang: Lang;
};

/**
 * Optional master audio. Drop a file into public/ and put its name here
 * (for example "voice.mp3"). It starts at frame 0, so the times inside
 * public/words.json are measured against it.
 */
const AUDIO_FILE: string = "";

const FONT =
  '"Noto Naskh Arabic", "Noto Sans Arabic", "Cairo", "Tajawal", "IBM Plex Sans Arabic", "Segoe UI", "DejaVu Sans", system-ui, sans-serif';
const INK = "#0b0d12";
const PAPER = "#f4f1ea";

const COPY = {
  ar: { chart: "نمو المشاهدات خلال تسعة أسابيع", unit: "ألف", closing: "صُنع بأداة KOSIF" },
  en: { chart: "Views over nine weeks", unit: "k", closing: "Made with KOSIF TOOL" },
} as const;

const dirOf = (lang: Lang): "rtl" | "ltr" => (lang === "ar" ? "rtl" : "ltr");

/** Adds alpha to a colour whether it is 6-digit hex, rgb(), hsl() or a named colour. */
export const withAlpha = (color: string, alpha: number): string => {
  const hex = /^#([0-9a-f]{6})$/i.exec(color.trim());
  if (hex) {
    return `#${hex[1]}${Math.round(alpha * 255).toString(16).padStart(2, "0")}`;
  }
  return `color-mix(in srgb, ${color} ${Math.round(alpha * 100)}%, transparent)`;
};

/** Scene lengths derived from the composition length, so the film scales with duration. */
export const sceneLayout = (total: number) => {
  const s1 = Math.round(total * 0.34);
  const s2 = Math.round(total * 0.4);
  return { s1, s2, s3: total - s1 - s2 };
};

/** 1 while a scene is on, easing from 0 at its first frame and back to 0 at its last. */
const sceneFade = (frame: number, length: number, edge = 10): number =>
  Math.min(
    progress(frame, 0, edge, easeOutCubic),
    1 - progress(frame, length - edge, edge, easeOutCubic),
  );

const CLAMP = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/* ------------------------------------------------------------------ */
/* Backdrop: accent glow plus a slowly drifting dot grid                */
/* ------------------------------------------------------------------ */

const Backdrop: React.FC<{ accent: string }> = ({ accent }) => {
  const frame = useCurrentFrame();
  const drift = frame * 0.35;
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 80% at 50% 18%, ${withAlpha(accent, 0.3)} 0%, ${INK} 62%)`,
      }}
    >
      <AbsoluteFill
        style={{
          backgroundImage: `radial-gradient(${withAlpha(PAPER, 0.18)} 1.5px, transparent 1.6px)`,
          backgroundSize: "44px 44px",
          backgroundPosition: `${drift}px ${drift * 0.6}px`,
          opacity: 0.55,
        }}
      />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* CameraRig: one group transform that pushes, pans and settles         */
/* ------------------------------------------------------------------ */

const CameraRig: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const { s1, s2 } = sceneLayout(durationInFrames);
  const keys = [0, s1, s1 + s2, durationInFrames];
  const options = { ...CLAMP, easing: easeInOutCubic };

  const scale = interpolate(frame, keys, [1.08, 1.0, 1.04, 1.1], options);
  const x = interpolate(frame, keys, [0, 0, -36, 0], options);
  const y = interpolate(frame, keys, [26, 0, -18, 0], options);
  const rotate = interpolate(frame, [0, durationInFrames], [-0.8, 0.8], options);

  return (
    <AbsoluteFill
      style={{
        transform: `translate(${x}px, ${y}px) rotate(${rotate}deg) scale(${scale})`,
        transformOrigin: "50% 50%",
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* Scene 1: title reveal with staggered words + keyword pills           */
/* ------------------------------------------------------------------ */

const TitleReveal: React.FC<FilmProps & { length: number }> = ({
  title,
  words,
  accent,
  lang,
  length,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dir = dirOf(lang);
  const titleWords = title.trim().split(/\s+/).filter(Boolean);
  const fade = sceneFade(frame, length);
  const rule = progress(frame, 4, 28, easeOutExpo);
  const pillsOffset = staggerStart(titleWords.length, 5, 14);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: "0 80px",
        opacity: fade,
      }}
    >
      <div
        style={{
          width: 180 * rule,
          height: 10,
          borderRadius: 5,
          background: accent,
          marginBottom: 56,
        }}
      />
      <h1
        dir={dir}
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "0 30px",
          margin: 0,
          fontFamily: FONT,
          fontSize: 112,
          fontWeight: 800,
          lineHeight: 1.3,
          color: PAPER,
          textAlign: "center",
          unicodeBidi: "plaintext",
        }}
      >
        {titleWords.map((word, index) => {
          const s = spring({
            frame: frame - staggerStart(index, 5, 6),
            fps,
            config: { damping: 14, stiffness: 120, mass: 0.9 },
          });
          return (
            <span
              key={`${word}-${index}`}
              style={{
                display: "inline-block",
                unicodeBidi: "plaintext",
                whiteSpace: "nowrap",
                opacity: s,
                transform: `translateY(${(1 - s) * 80}px) scale(${0.85 + 0.15 * s})`,
              }}
            >
              {word}
            </span>
          );
        })}
      </h1>
      <div
        dir={dir}
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 16,
          marginTop: 64,
        }}
      >
        {words.map((word, index) => {
          const s = spring({
            frame: frame - staggerStart(index, 4, pillsOffset),
            fps,
            config: { damping: 12, stiffness: 150 },
          });
          return (
            <span
              key={`${word}-${index}`}
              style={{
                display: "inline-block",
                unicodeBidi: "plaintext",
                whiteSpace: "nowrap",
                fontFamily: FONT,
                fontSize: 40,
                fontWeight: 600,
                color: PAPER,
                padding: "12px 30px",
                borderRadius: 999,
                border: `3px solid ${withAlpha(accent, 0.9)}`,
                background: withAlpha(accent, 0.14),
                opacity: s,
                transform: `translateY(${(1 - s) * 36}px)`,
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* Scene 2: animated SVG line chart                                     */
/* ------------------------------------------------------------------ */

const POINTS = 9;
const CHART_W = 920;
const CHART_H = 620;
const PAD = { left: 60, right: 40, top: 50, bottom: 70 };
const DRAW_START = 12;
const DRAW_LENGTH = 66;

type Point = { x: number; y: number; value: number };

/** Deterministic sample data: a rising trend with seeded noise. */
const makeSeries = (seed: string): number[] =>
  Array.from({ length: POINTS }, (_, i) =>
    Math.round(18 + i * 7.5 + random(`${seed}:${i}`) * 20),
  );

/** Smooth cubic path through the points; control handles sit a third of the way across. */
const smoothPath = (points: Point[]): string => {
  const [first, ...rest] = points;
  if (!first) {
    return "";
  }
  let d = `M ${first.x} ${first.y}`;
  let previous = first;
  for (const point of rest) {
    const dx = (point.x - previous.x) / 3;
    d += ` C ${previous.x + dx} ${previous.y}, ${point.x - dx} ${point.y}, ${point.x} ${point.y}`;
    previous = point;
  }
  return d;
};

const LineChart: React.FC<{ accent: string; lang: Lang; length: number }> = ({
  accent,
  lang,
  length,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const copy = COPY[lang];
  const fade = sceneFade(frame, length);

  const series = useMemo(() => makeSeries("kosif-chart"), []);
  const innerW = CHART_W - PAD.left - PAD.right;
  const innerH = CHART_H - PAD.top - PAD.bottom;
  const top = Math.max(...series) * 1.15;
  const points: Point[] = series.map((value, i) => ({
    x: PAD.left + (innerW * i) / (POINTS - 1),
    y: PAD.top + innerH - (innerH * value) / top,
    value,
  }));
  const first = points[0];
  const last = points[points.length - 1];

  // Line drawing is linear so that each dot pops exactly when the pen reaches it.
  const draw = interpolate(frame, [DRAW_START, DRAW_START + DRAW_LENGTH], [0, 1], CLAMP);
  const grid = progress(frame, 0, 20, easeOutCubic);
  const headline = spring({ frame, fps, config: { damping: 16, stiffness: 110 } });
  const counter = Math.round(
    interpolate(frame, [DRAW_START, DRAW_START + DRAW_LENGTH], [0, last.value], {
      ...CLAMP,
      easing: easeOutExpo,
    }),
  );
  const format = useMemo(
    () => new Intl.NumberFormat(lang === "ar" ? "ar-EG" : "en-US"),
    [lang],
  );

  const linePath = smoothPath(points);
  const baseline = PAD.top + innerH;
  const areaPath = `${linePath} L ${last.x} ${baseline} L ${first.x} ${baseline} Z`;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: "0 60px",
        opacity: fade,
      }}
    >
      <div
        dir={dirOf(lang)}
        style={{
          width: "100%",
          fontFamily: FONT,
          color: PAPER,
          opacity: headline,
          transform: `translateY(${(1 - headline) * 30}px)`,
        }}
      >
        <div style={{ fontSize: 36, opacity: 0.72, unicodeBidi: "plaintext" }}>{copy.chart}</div>
        <div
          style={{
            fontSize: 124,
            fontWeight: 800,
            lineHeight: 1.15,
            color: accent,
            fontVariantNumeric: "tabular-nums",
            unicodeBidi: "plaintext",
          }}
        >
          {format.format(counter)}
          <span style={{ fontSize: 44, color: PAPER, marginInlineStart: 14 }}>{copy.unit}</span>
        </div>
      </div>

      <svg
        viewBox={`0 0 ${CHART_W} ${CHART_H}`}
        width="100%"
        style={{ marginTop: 36, overflow: "visible" }}
      >
        <defs>
          <linearGradient id="kosif-area" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={accent} stopOpacity={0.45} />
            <stop offset="1" stopColor={accent} stopOpacity={0} />
          </linearGradient>
          <clipPath id="kosif-reveal">
            <rect x={0} y={0} width={PAD.left + innerW * draw + 2} height={CHART_H} />
          </clipPath>
        </defs>

        {[0, 0.25, 0.5, 0.75, 1].map((level) => {
          const y = PAD.top + innerH * (1 - level);
          return (
            <line
              key={level}
              x1={PAD.left}
              x2={PAD.left + innerW * grid}
              y1={y}
              y2={y}
              stroke={withAlpha(PAPER, level === 0 ? 0.4 : 0.14)}
              strokeWidth={2}
              strokeDasharray={level === 0 ? undefined : "6 10"}
            />
          );
        })}

        <path d={areaPath} fill="url(#kosif-area)" clipPath="url(#kosif-reveal)" />
        <path
          d={linePath}
          fill="none"
          stroke={accent}
          strokeWidth={10}
          strokeLinecap="round"
          strokeLinejoin="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - draw}
        />

        {points.map((point, i) => {
          const reach = DRAW_START + (DRAW_LENGTH * i) / (POINTS - 1);
          const s = spring({
            frame: frame - reach,
            fps,
            config: { damping: 10, stiffness: 180 },
          });
          return (
            <g key={i} transform={`translate(${point.x} ${point.y}) scale(${s})`}>
              <circle r={15} fill={INK} stroke={accent} strokeWidth={6} />
              <text
                y={-30}
                textAnchor="middle"
                fontFamily={FONT}
                fontSize={26}
                fontWeight={700}
                fill={PAPER}
                opacity={s}
              >
                {format.format(point.value)}
              </text>
            </g>
          );
        })}

        {points.map((point, i) => (
          <text
            key={`label-${i}`}
            x={point.x}
            y={baseline + 44}
            textAnchor="middle"
            fontFamily={FONT}
            fontSize={24}
            fill={withAlpha(PAPER, 0.6)}
            opacity={grid}
          >
            {format.format(i + 1)}
          </text>
        ))}
      </svg>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* Scene 3: closing logo card                                           */
/* ------------------------------------------------------------------ */

const LogoCard: React.FC<{ title: string; accent: string; lang: Lang; length: number }> = ({
  title,
  accent,
  lang,
  length,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fade = sceneFade(frame, length);
  const card = spring({ frame, fps, config: { damping: 14, stiffness: 90, mass: 1.1 } });
  const ring = progress(frame, 8, 40, easeInOutCubic);
  const mark = spring({ frame: frame - 18, fps, config: { damping: 11, stiffness: 160 } });
  const text = progress(frame, 34, 18, easeOutCubic);
  const radius = 150;
  const circumference = 2 * Math.PI * radius;

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: fade }}>
      <div
        style={{
          width: 760,
          padding: "80px 60px",
          borderRadius: 48,
          background: withAlpha(PAPER, 0.06),
          border: `2px solid ${withAlpha(PAPER, 0.12)}`,
          boxShadow: `0 40px 120px ${withAlpha(INK, 0.6)}`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 36,
          transform: `scale(${0.8 + 0.2 * card})`,
          opacity: card,
        }}
      >
        <svg width={360} height={360} viewBox="0 0 360 360">
          <circle
            cx={180}
            cy={180}
            r={radius}
            fill="none"
            stroke={withAlpha(PAPER, 0.15)}
            strokeWidth={10}
          />
          <circle
            cx={180}
            cy={180}
            r={radius}
            fill="none"
            stroke={accent}
            strokeWidth={10}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference * (1 - ring)}
            transform="rotate(-90 180 180)"
          />
          {/* Simple original mark: an upright stem and an accent chevron. */}
          <g transform={`translate(180 180) scale(${mark}) translate(-180 -180)`}>
            <path d="M 122 110 L 122 250" stroke={PAPER} strokeWidth={34} strokeLinecap="round" />
            <path
              d="M 236 112 L 152 180 L 236 248"
              fill="none"
              stroke={accent}
              strokeWidth={34}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </g>
        </svg>
        <div
          dir={dirOf(lang)}
          style={{
            fontFamily: FONT,
            color: PAPER,
            fontSize: 56,
            fontWeight: 800,
            lineHeight: 1.3,
            textAlign: "center",
            unicodeBidi: "plaintext",
            opacity: text,
            transform: `translateY(${(1 - text) * 20}px)`,
          }}
        >
          {title}
        </div>
        <div
          dir={dirOf(lang)}
          style={{
            fontFamily: FONT,
            color: withAlpha(PAPER, 0.65),
            fontSize: 30,
            unicodeBidi: "plaintext",
            opacity: text,
          }}
        >
          {COPY[lang].closing}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* Film: three scenes inside one camera rig, captions on top           */
/* ------------------------------------------------------------------ */

export const Film: React.FC<FilmProps> = (props) => {
  const { durationInFrames } = useVideoConfig();
  const { s1, s2, s3 } = sceneLayout(durationInFrames);

  return (
    <AbsoluteFill style={{ backgroundColor: INK, fontFamily: FONT }}>
      {AUDIO_FILE ? <Audio src={staticFile(AUDIO_FILE)} /> : null}
      <Backdrop accent={props.accent} />
      <CameraRig>
        <Sequence from={0} durationInFrames={s1} name="Title">
          <TitleReveal {...props} length={s1} />
        </Sequence>
        <Sequence from={s1} durationInFrames={s2} name="Chart">
          <LineChart accent={props.accent} lang={props.lang} length={s2} />
        </Sequence>
        <Sequence from={s1 + s2} durationInFrames={s3} name="Logo">
          <LogoCard title={props.title} accent={props.accent} lang={props.lang} length={s3} />
        </Sequence>
      </CameraRig>
      <Captions accent={props.accent} lang={props.lang} />
    </AbsoluteFill>
  );
};
