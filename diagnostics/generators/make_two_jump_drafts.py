"""Listening drafts: one synthetic performance with a short and a long backward jump.

Built like the paper's section-repetition condition (remote
scripts/run_section_repetition_candidates.py): the maximally unfolded score
without grace notes is rendered deadpan at the performance's estimated tempo,
and each listed measure range is played twice in a row (one backward jump each).
Jump distances follow Nakamura et al. (2016), Table III: the short one is near
the median (7.75 s), the long one near the geometric mean of the first quartile
(15.5 s) and the maximum (84.8 s), about 36 s. Measure numbers are MusicXML's.
    python make_two_jump_drafts.py   (benchmark env, MATCHMAKER_DATA_DIR set)
"""
import json
from pathlib import Path

import numpy as np
import partitura as pt
from partitura.io.exportaudio import save_wav_fluidsynth
from partitura.performance import PerformedPart
from partitura.score import merge_parts, remove_grace_notes, unfold_part_maximal
from partitura.utils.music import performance_from_part

DATA = Path("/Users/jiyun/data/matchmaker-benchmark-data/eval/asap/score")
#: name -> (score file, bpm, [(first measure, last measure) played twice, in order])
DRAFTS = {
    "bwv858": ("Bach_Fugue_bwv_858_xml_score.musicxml", 65.0, [(9, 10), (17, 27)]),
    "op23_6": ("Rachmaninoff_Preludes_op_23_6_xml_score.musicxml", 60.0, [(10, 11), (21, 31)]),
}


def load_part(path):
    score = pt.load_score(str(path))
    part = unfold_part_maximal(merge_parts(score.parts))
    remove_grace_notes(part)
    return part


def measure_beats(part, first, last):
    ms = {m.number: m for m in part.iter_all(pt.score.Measure)}
    return float(part.beat_map(ms[first].start.t)), float(part.beat_map(ms[last].end.t))


def make_jumps(part, bpm, intervals):
    """Performance replaying each [start, end) beat interval once, its alignment and GT."""
    sna = part.note_array()
    beat_of = {str(i): float(b) for i, b in zip(sna["id"], sna["onset_beat"])}
    base = performance_from_part(part=part, bpm=bpm, velocity=64).note_array()
    beats = np.array([beat_of[str(i)] for i in base["id"]])
    # segments of the score in performed order: up to end1, start1..end1, end1..end2, ...
    cuts, segs, prev = [], [], -np.inf
    for start, end in intervals:
        segs += [(prev, end), (start, end)]
        prev = end
    segs.append((prev, np.inf))
    parts, alignment, gt, offset = [], [], [], 0.0
    for k, (b0, b1) in enumerate(segs):
        seg = base[(beats >= b0) & (beats < b1)].copy()
        if not len(seg):
            continue
        t0 = 60.0 * (max(b0, beats.min()) - beats.min()) / bpm
        seg_ids = [str(i) for i in seg["id"]]
        seg["onset_sec"] = seg["onset_sec"] - t0 + offset
        seg["id"] = np.asarray([f"s{k}_{i}" for i in seg_ids], dtype=seg["id"].dtype)
        alignment += [{"label": "match", "score_id": s, "performance_id": str(p)} for s, p in zip(seg_ids, seg["id"])]
        gt += [(float(t), beat_of[s]) for t, s in zip(seg["onset_sec"], seg_ids)]
        parts.append(seg)
        offset += 60.0 * (min(b1, beats.max() + 1e9) - max(b0, beats.min())) / bpm if np.isfinite(b1) else 0.0
    na = np.concatenate(parts)
    na.sort(order="onset_sec")
    gt = np.unique(np.round(np.array(gt), 9), axis=0)
    gt = gt[np.argsort(gt[:, 0], kind="stable")]
    return PerformedPart.from_note_array(na), alignment, gt, sna


def main():
    manifest = {}
    for name, (score, bpm, ranges) in DRAFTS.items():
        part = load_part(DATA / score)
        intervals = [measure_beats(part, a, b) for a, b in ranges]
        perf, alignment, gt, sna = make_jumps(part, bpm, intervals)
        stem = f"{name}-two_jump-" + "_".join(f"m{a}-{b}" for a, b in ranges) + f"-bpm_{bpm:g}"
        save_wav_fluidsynth(perf, out=f"{stem}.wav")
        pt.save_performance_midi(perf, out=f"{stem}.mid")
        np.savetxt(f"{stem}.tsv", gt, delimiter="\t", fmt="%.9f", header="perf_sec\tscore_beat", comments="")
        np.savez_compressed(f"{stem}.npz", alignment=np.asarray(alignment, dtype=object),
                            performance_note_array=perf.note_array(), score_note_array=sna)
        jumps = np.flatnonzero(np.diff(gt[:, 1]) < 0) + 1
        pna = perf.note_array()
        manifest[name] = {
            "file": stem, "score": score, "bpm": bpm,
            "jumps": [{"measures_twice": [a, b], "replayed_beats": [s, e],
                       "jump_back_sec": round(60 * (e - s) / bpm, 2), "jump_at_sec": round(float(gt[j, 0]), 2)}
                      for (a, b), (s, e), j in zip(ranges, intervals, jumps)],
            "n_backward_jumps": int(len(jumps)),
            "duration_sec": round(float(np.max(pna["onset_sec"] + pna["duration_sec"])), 2),
        }
        print(json.dumps(manifest[name]))
    Path("manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
