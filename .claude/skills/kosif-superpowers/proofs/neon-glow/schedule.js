/* Neon ignition schedule — shared by index.html (picture) and sound.py (sound).
 * Everything after "window.NEON_SCHEDULE =" is plain JSON so Python can read it.
 * Segments are [start_s, end_s, level 0..1]; outside every segment the tube is dark.
 * The last segment of a tube ends at 99 (stays lit) and gets a warm-up ramp.
 */
window.NEON_SCHEDULE = {
  "duration": 10,
  "fps": 30,
  "fadeIn": 0.6,
  "warmup": 0.5,
  "arabic": [[0.50, 0.70, 0.12], [0.70, 0.733, 0.9], [0.80, 0.833, 0.35], [0.967, 1.0, 1.0], [1.10, 1.233, 0.6], [1.30, 1.333, 0.95], [1.40, 1.433, 0.45], [1.50, 99, 1]],
  "latinStart": 2.3,
  "latinStep": 0.1,
  "latinPattern": [[0, 0.034, 0.85], [0.10, 0.134, 0.45], [0.20, 99, 1]],
  "faulty": {
    "index": 6,
    "pattern": [[0, 0.034, 0.7], [0.30, 0.334, 0.9], [0.60, 0.70, 0.35], [1.00, 1.034, 1], [1.20, 1.30, 0.55], [1.50, 99, 1]],
    "dropouts": [[7.80, 7.867, 0], [7.867, 7.90, 0.5], [7.90, 7.967, 0]]
  },
  "cup": { "body": [3.4, 4.15], "handle": [4.05, 4.35], "saucer": [4.25, 4.65] },
  "steam": { "start": 4.8, "step": 0.3, "states": [[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 1, 1]] },
  "sweep": [5.6, 7.4]
}
;
