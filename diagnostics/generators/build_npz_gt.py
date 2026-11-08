"""GT TSV for the synthetic conditions that ship an alignment npz instead of a .match.

Same rule as matchmaker.utils.eval.gt_from_match: every matched note gives
(performance onset, score onset beat), sorted by time, consecutive equal beats
merged. Both come from the arrays stored in the npz itself, whose note ids need
not match those of the score part Matchmaker builds for the run; the beats are
checked to be onsets of that score part.
    python build_npz_gt.py   (benchmark env, from this directory)
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "matchmaker_eval"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from rescore import score_part
from matchmaker_eval.folds import load_fold

#: (fold, condition, alignment npz)
CONDITIONS = [
    ("synthetic_audio.csv", "Fumbles/kv279_3-fumbles",
     Path("/Users/jiyun/data/synthetic_performances/match/Fumbles/kv279_3-fumbles.npz")),
    ("schubert_secrep_audio.csv", "Section_Repetition/Schubert_D783_no15_p17-repetition-beat_22-46-bpm_149",
     Path("schubert_secrep/Schubert_D783_no15_p17-repetition-beat_22-46-bpm_149.npz")),
]
for fold, cond, npz in CONDITIONS:
    piece = next(p for p in load_fold(fold, "audio") if p.piece_id == f"synthetic/{cond}")
    d = np.load(npz, allow_pickle=True)
    beat_at = {str(n["id"]): float(n["onset_beat"]) for n in d["score_note_array"]}
    run_beats = set(np.round(score_part(piece, "audio").note_array()["onset_beat"], 4))
    onset = {str(n["id"]): float(n["onset_sec"]) for n in d["performance_note_array"]}
    pairs = [(onset[a["performance_id"]], beat_at[a["score_id"]]) for a in d["alignment"]
             if a.get("label") == "match" and a["score_id"] in beat_at and a["performance_id"] in onset]
    n_align = sum(a.get("label") == "match" for a in d["alignment"])
    secs, beats = np.array(pairs).T
    order = np.argsort(secs, kind="stable"); secs, beats = secs[order], beats[order]
    keep = np.ones(len(beats), bool); keep[1:] = beats[1:] != beats[:-1]
    assert set(np.round(beats, 4)) <= run_beats, "GT beat that is not a score onset"
    out = Path("gt") / f"{cond}.tsv"; out.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(out, np.column_stack([secs[keep], beats[keep]]), fmt="%.6f", delimiter="\t",
               header="perf_sec\tscore_beat", comments="")
    print(cond, f"{len(pairs)}/{n_align} matched notes joined, {keep.sum()} onsets ->", out)
