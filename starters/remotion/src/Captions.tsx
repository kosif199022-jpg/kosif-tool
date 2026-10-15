import React, { useEffect, useMemo, useState } from "react";
import {
  continueRender,
  delayRender,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/** One entry of public/words.json. Times are seconds from the start of the film. */
export type TimedWord = { word: string; start: number; end: number };
export type Direction = "rtl" | "ltr";

type CaptionsProps = {
  accent: string;
  lang: "ar" | "en";
  /** File name inside public/. Default: words.json */
  file?: string;
  /** Maximum words shown together on one caption card. */
  maxWordsPerLine?: number;
  /** A silence longer than this (seconds) starts a new caption card. */
  gapSeconds?: number;
  /** Seconds a finished card stays visible after its last word. */
  holdSeconds?: number;
  /** Seconds a card appears before its first word starts. */
  leadSeconds?: number;
};

const FONT =
  '"Noto Naskh Arabic", "Noto Sans Arabic", "Cairo", "Tajawal", "IBM Plex Sans Arabic", "Segoe UI", "DejaVu Sans", system-ui, sans-serif';

// First "strong" character decides the direction of a caption card.
const RTL_CHAR =
  /[֐-׿؀-ۿݐ-ݿࢠ-ࣿיִ-﷿ﹰ-﻿]/;
const STRONG_CHAR =
  /[A-Za-zÀ-ɏͰ-ϿЀ-ӿ֐-׿؀-ۿݐ-ݿࢠ-ࣿיִ-﷿ﹰ-﻿]/;

export const detectDirection = (text: string, fallback: Direction): Direction => {
  const match = STRONG_CHAR.exec(text);
  if (!match) {
    return fallback;
  }
  return RTL_CHAR.test(match[0]) ? "rtl" : "ltr";
};

export const isTimedWord = (value: unknown): value is TimedWord => {
  if (typeof value !== "object" || value === null) {
    return false;
  }
  const record = value as Record<string, unknown>;
  return (
    typeof record.word === "string" &&
    record.word.trim().length > 0 &&
    typeof record.start === "number" &&
    typeof record.end === "number" &&
    Number.isFinite(record.start) &&
    Number.isFinite(record.end) &&
    record.end >= record.start
  );
};

/** Splits the word list into caption cards by word count and by silences. */
export const groupWords = (
  words: TimedWord[],
  maxWords: number,
  gapSeconds: number,
): TimedWord[][] => {
  const cards: TimedWord[][] = [];
  let current: TimedWord[] = [];
  for (const word of words) {
    const previous = current[current.length - 1];
    if (previous && (current.length >= maxWords || word.start - previous.end > gapSeconds)) {
      cards.push(current);
      current = [];
    }
    current.push(word);
  }
  if (current.length > 0) {
    cards.push(current);
  }
  return cards;
};

/**
 * Loads a {word,start,end}[] JSON file from public/ and blocks the render
 * until it arrives. A missing or malformed file logs a warning and yields [].
 */
export const useTimedWords = (file: string): TimedWord[] | null => {
  const [words, setWords] = useState<TimedWord[] | null>(null);
  const [handle] = useState(() => delayRender(`Loading ${file}`));

  useEffect(() => {
    let alive = true;
    fetch(staticFile(file))
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json() as Promise<unknown>;
      })
      .then((json) => {
        if (!alive) {
          return;
        }
        const list = Array.isArray(json) ? json.filter(isTimedWord) : [];
        setWords([...list].sort((a, b) => a.start - b.start));
        continueRender(handle);
      })
      .catch((error: unknown) => {
        if (!alive) {
          return;
        }
        console.warn(`[Captions] could not load public/${file}:`, error);
        setWords([]);
        continueRender(handle);
      });
    return () => {
      alive = false;
    };
  }, [file, handle]);

  return words;
};

/**
 * Word-level captions. The active word takes the accent colour and pops with
 * a spring; past words stay bright, upcoming words are dimmed.
 *
 * Arabic safety: the card gets dir="rtl" (or "ltr") so the flex row lays out
 * words in reading order, and every word is its own `unicode-bidi: plaintext`
 * box with `white-space: nowrap`, so a word is never split, re-ordered inside,
 * or broken across lines. Only whole words are ever shown.
 */
export const Captions: React.FC<CaptionsProps> = ({
  accent,
  lang,
  file = "words.json",
  maxWordsPerLine = 4,
  gapSeconds = 0.6,
  holdSeconds = 0.35,
  leadSeconds = 0.15,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const seconds = frame / fps;
  const words = useTimedWords(file);

  const cards = useMemo(
    () => groupWords(words ?? [], maxWordsPerLine, gapSeconds),
    [words, maxWordsPerLine, gapSeconds],
  );

  const card = cards.find((group) => {
    const first = group[0];
    const last = group[group.length - 1];
    return seconds >= first.start - leadSeconds && seconds < last.end + holdSeconds;
  });

  if (!card) {
    return null;
  }

  const fallback: Direction = lang === "ar" ? "rtl" : "ltr";
  const dir = detectDirection(card.map((w) => w.word).join(" "), fallback);

  return (
    <div
      style={{
        position: "absolute",
        left: 60,
        right: 60,
        bottom: 260,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
      }}
    >
      <div
        dir={dir}
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "6px 20px",
          padding: "20px 38px",
          borderRadius: 30,
          background: "rgba(8, 10, 16, 0.66)",
          fontFamily: FONT,
          fontSize: 58,
          fontWeight: 700,
          lineHeight: 1.45,
          color: "#ffffff",
          unicodeBidi: "plaintext",
        }}
      >
        {card.map((item, index) => {
          const active = seconds >= item.start && seconds < item.end;
          const done = seconds >= item.end;
          const pop = spring({
            frame: frame - Math.round(item.start * fps),
            fps,
            config: { damping: 12, stiffness: 220, mass: 0.7 },
          });
          const scale = active ? 1 + 0.1 * pop : 1;
          return (
            <span
              key={`${item.start}-${index}`}
              dir={dir}
              style={{
                display: "inline-block",
                unicodeBidi: "plaintext",
                whiteSpace: "nowrap",
                hyphens: "none",
                overflowWrap: "normal",
                color: active ? accent : "#ffffff",
                opacity: active || done ? 1 : 0.42,
                transform: `scale(${scale})`,
                transformOrigin: "center",
              }}
            >
              {item.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
