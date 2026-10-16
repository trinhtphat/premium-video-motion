# Embedded audio library

Ships with the repo so the pipeline works offline after download.

- `music/` — 7 background tracks, renamed by mood. BPM, beat offset, drop guess, breakdowns and energy per bar are
  pre-computed in `library.json` (from `tools/beatgrid.py`), so an agent can pick a track and plan splices without re-analysing.
- `sfx/` — 40 short effects (`category__name.wav`): transitions, tech UI, cinematic hits, retro pops, game.
- `sfx.json` — default cue-type → file map used by `tools/mix.py` (paths relative to this folder).

Pick a track: match `mood` / `good_for` to the brand playbook, then check `energy_db_per_bar` for the lift (≈ +3 dB)
and the drop; put the logo on the lift and the hero moment on the drop.

Licences: tracks come from Pixabay / chosic.com free libraries — Pixabay tracks are free for commercial use;
chosic.com tracks may require attribution. Check `licence` in `library.json` and the source page before paid ads.
Replace or add tracks freely: drop a file in `music/`, run `python3 tools/beatgrid.py music/<file>` and add an entry.

## User-supplied sound-effects-pack.zip

The imported pack contains 133 effects in `sound-effects-pack/` and 17 music tracks. Every file is recorded in `sound-effects-pack-manifest.json` with its SHA-256, measured duration and the user's 2026-10-16 commercial-use and public redistribution confirmation. The ZIP README is descriptive metadata; the rights evidence is the user's confirmation.

Use `pack.<folder>.<filename-without-extension>` as a cue type, for example `pack.transition.arrow-whoosh-1491` or `pack.ui.select-click-1109`. These keys are in the default `sfx.json` and work with `tools/mix.py`. The mixer checks the selected file against the manifest before playback. Keep effects aligned to actual visual events and mix them below the music.

The 17 tracks are listed in `music-pack.json`. Select one as `--music assets/audio/sound-effects-pack/music/<filename>.mp3`; analyze its beat grid with `tools/beatgrid.py` before making beat-accurate cuts. The existing seven analyzed tracks remain in `library.json`.
