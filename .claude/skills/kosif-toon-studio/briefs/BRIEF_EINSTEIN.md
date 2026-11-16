# Einstein season: changes to BRIEF.md

Follow `BRIEF.md` in full, with these changes for films 31–40:

1. **Short English captions are now required** (this overrides "no text"). Use `films/captions.py` (read it):
   - `cap.title(g, "...", t, t0, t1)` for the one-line idea (2–8 words, top of frame, on screen at least 1.5 s);
   - `cap.note(g, "...", (x, y), t, t0, t1)` for small labels and values (a year, "1 sec", "+38 μs/day");
   - `cap.clock(g, (x, y), r, hours)` for clock faces.
   Use 2–4 captions per film in total: one to name the hook, one for the key fact at the reveal, optionally one with the year / the "Einstein, 1905" credit.
   Captions must never cover a face or the key action. Plain English, correct spelling.
2. **The physics is Einstein's and must be stated correctly.** Do not overstate: if a real effect is tiny, say it is tiny (show it magnified with a "zoom" inset, or say "×1,000,000,000" in a caption).
   Where the film exaggerates for visibility (e.g. a twin aging decades), make it a near-light-speed trip so it is physically right, not a car ride.
3. **No drawing of Einstein's face or any real person.** His name may appear only inside captions.
4. Keep the Cap/Specs dynamic: Cap does the everyday-intuition thing and laughs; Specs knows the Einstein answer; Cap ends amazed.
5. Space scenes are welcome (stars, planets, rockets, Earth from orbit, black holes) as long as they are drawn in the same flat, outlined cartoon style. Use `tk.glow`, `tk.stars`, `tk.sparkles` for light.

Report back as `BRIEF.md` says, and add for each film the exact English captions used.
