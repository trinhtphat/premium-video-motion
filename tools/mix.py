#!/usr/bin/env python3
"""Sound design mix: music bed + SFX placed on the page's CUES, loudness-normalised.

  node tools/cues.mjs templates/kinetic-promo/index.html > out/cues.json
  python3 tools/mix.py out/cues.json --music edit.wav --sfx sfx.json --out out/mix.wav [--lufs -14]

sfx.json maps cue type → file (relative to the json), default = assets/audio/sfx.json (embedded library), e.g. {"swoosh": ".../woosh_1.wav", "hit": ".../hit.wav", "tick": ".../click.wav"}.
A cue is {beat, type, gain(dB, peak), align: "onset"|"peak"}. Whooshes default to align on their PEAK
(the loudest moment lands on the cut); clicks/hits align on their onset.

Rules (from real client feedback): SFX 12–20 dB under the music peak; no bell/'ting' clusters;
fewer cues is better — if a sound doesn't help the viewer understand the product, delete it.
"""
import json, argparse, subprocess, tempfile, os, hashlib
from pathlib import Path
import numpy as np, librosa, soundfile as sf

ap = argparse.ArgumentParser(); ap.add_argument('cues'); ap.add_argument('--music'); ap.add_argument('--sfx', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'audio', 'sfx.json'))
ap.add_argument('--out', default='out/mix.wav'); ap.add_argument('--lufs', type=float, default=-14); ap.add_argument('--music-gain', type=float, default=-3); ap.add_argument('--fade', type=float, default=0.05, help='fade-out seconds at the end (use ~1.5 for a logo ending, 0.05 for loops)')
a = ap.parse_args()
C = json.load(open(a.cues)); B = C['B']; dur = C['DUR']; cues = C['cues']; M = json.load(open(a.sfx)); M = {k: (v if os.path.isabs(v) else os.path.join(os.path.dirname(os.path.abspath(a.sfx)), v)) for k, v in M.items() if isinstance(v, str)}; sr = 48000
audio_root = (Path(__file__).resolve().parent.parent / 'assets/audio').resolve()
pack_root = audio_root / 'sound-effects-pack'
pack_manifest = json.loads((audio_root / 'sound-effects-pack-manifest.json').read_text(encoding='utf-8'))
pack_registry = {(audio_root / item['filename']).resolve(): item for item in pack_manifest['sounds']}
approved_statuses = {'user_confirmed', 'licensed', 'public_domain', 'cc0'}

def check_pack_asset(path, expected_group=None):
    selected = Path(path).resolve()
    if not selected.is_relative_to(pack_root):
        return
    entry = pack_registry.get(selected)
    if not entry or entry['license_status'] not in approved_statuses:
        raise ValueError(f'Pack audio has no verified rights: {selected}')
    if expected_group == 'bgm' and entry['category_group'] != 'bgm':
        raise ValueError(f'Pack music selection is not BGM: {selected}')
    if expected_group == 'sfx' and entry['category_group'] == 'bgm':
        raise ValueError(f'Pack cue selection is a music track: {selected}')
    if hashlib.sha256(selected.read_bytes()).hexdigest() != entry['sha256']:
        raise ValueError(f'Pack audio differs from its manifest: {selected}')
L = int(dur * sr)
if a.music:
    check_pack_asset(a.music, 'bgm')
    mus, _ = librosa.load(a.music, sr=sr, mono=False); mus = np.atleast_2d(mus)
    if mus.shape[0] == 1: mus = np.vstack([mus, mus])
    mus = mus[:, :L]; mus = np.pad(mus, ((0, 0), (0, L - mus.shape[1])))
else: mus = np.zeros((2, L))
out = np.zeros((2, L)); cache = {}
for c in cues:
    f = M.get(c['type'])
    if not f or not os.path.exists(f): print('skip (no file for type):', c['type']); continue
    check_pack_asset(f, 'sfx')
    if f not in cache:
        y, _ = librosa.load(f, sr=sr, mono=False); y = np.atleast_2d(y); cache[f] = np.vstack([y, y]) if y.shape[0] == 1 else y[:2]
    y = cache[f].copy(); env = np.abs(y).max(0)
    align = c.get('align') or ('peak' if 'swoosh' in c['type'] or 'whoosh' in c['type'] or 'rise' in c['type'] else 'onset')
    ref = int(np.argmax(env)) if align == 'peak' else int(np.argmax(env > env.max() * .05))
    y *= 10 ** (c.get('gain', -18) / 20) / max(1e-6, env.max())
    s = int(c['beat'] * B * sr) - ref; i0, i1 = max(0, s), min(L, s + y.shape[1])
    if i1 > i0: out[:, i0:i1] += y[:, i0 - s:i1 - s]
mix = mus * 10 ** (a.music_gain / 20) + out
tmp = tempfile.mktemp(suffix='.wav'); sf.write(tmp, mix.T, sr)
os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-af', f'loudnorm=I={a.lufs}:TP=-1.5:LRA=11,afade=t=out:st={max(0, dur - a.fade):.3f}:d={a.fade:.3f}', '-ar', str(sr), a.out], check=True)
os.remove(tmp); print(f'Wrote {a.out}  ({len(cues)} cues, {dur:.2f} s, target {a.lufs} LUFS)')
