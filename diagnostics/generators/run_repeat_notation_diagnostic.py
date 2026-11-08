"""Controlled local/notated repeat diagnostic for TISMIR Figure 8.

K.282/i was chosen for simple, unambiguous repeat barlines, before examining
algorithm outputs. Both conditions use the same folded score and first 18
measures. This is an illustrative diagnostic, not a new benchmark aggregate.
Run: python scripts/run_repeat_notation_diagnostic.py --output-dir OUTPUT
"""
import argparse
import contextlib
import hashlib
import inspect
import json
from pathlib import Path
import subprocess
import time

import numpy as np
import partitura as pt
from partitura.score import merge_parts, remove_grace_notes, Repeat, Measure
from partitura.performance import PerformedPart
from partitura.utils.music import performance_from_part


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_cases(score, out, bpm):
    part = merge_parts(pt.load_musicxml(str(score), force_note_ids="keep",
                                    ignore_invisible_objects=True).parts)
    remove_grace_notes(part)
    measures = {m.number: m for m in part.iter_all(Measure)}
    at = lambda t: float(part.beat_map(t))
    first_repeat = sorted(part.iter_all(Repeat), key=lambda r: r.end.t)[0]
    marked = (at(first_repeat.start.t), at(first_repeat.end.t))
    local = (at(measures[5].start.t), at(measures[6].end.t))
    stop = at(measures[18].end.t)
    assert marked == (0., 60.) and local == (16., 24.) and stop == 72.
    sna = part.note_array()
    beat_of = dict(zip(map(str, sna['id']), map(float, sna['onset_beat'])))
    base = performance_from_part(part, bpm=bpm, velocity=64).note_array()
    beats = np.array([beat_of[str(n)] for n in base['id']])
    assert np.isclose(beats.min(), 0.)
    cases = []
    for name, interval in [('local', local), ('notated', marked)]:
        dest = out / name
        dest.mkdir(parents=True, exist_ok=True)
        start, end = interval
        segments = [(0., end), (start, end), (end, stop)]
        arrays, gt, alignment, offset = [], [], [], 0.
        for k, (b0, b1) in enumerate(segments):
            notes = base[(beats >= b0) & (beats < b1)].copy()
            original_ids = list(map(str, notes['id']))
            # Short unique IDs avoid silent truncation of the fixed-width field.
            ids = [f's{k}n{i}' for i in range(len(notes))]
            notes['id'] = ids
            notes['onset_sec'] = notes['onset_sec'] - b0 * 60 / bpm + offset
            segment_end = offset + (b1 - b0) * 60 / bpm
            # Explicit note-offs at the splice; no sustained note spans a jump.
            notes['duration_sec'] = np.minimum(notes['duration_sec'],
                                               segment_end - notes['onset_sec'])
            assert np.all(notes['duration_sec'] > 0)
            arrays.append(notes)
            gt.extend((float(t), beat_of[s]) for t, s in zip(notes['onset_sec'], original_ids))
            alignment.extend(dict(label='match', score_id=s, performance_id=p)
                             for s, p in zip(original_ids, ids))
            offset = segment_end
        notes = np.concatenate(arrays)
        notes.sort(order='onset_sec')
        assert len(np.unique(notes['id'])) == len(notes)
        perf = PerformedPart.from_note_array(notes)
        gt = np.unique(np.round(gt, 8), axis=0)
        assert np.sum(np.diff(gt[:, 1]) < 0) == 1
        pt.save_wav_fluidsynth(perf, out=str(dest/'performance.wav'), samplerate=22050)
        pt.save_performance_midi(perf, out=str(dest/'performance.mid'))
        np.savetxt(dest/'gt.tsv', gt, delimiter='\t', header='perf_sec\tscore_beat', comments='')
        np.savez_compressed(dest/'notes.npz', performance=notes, score=sna)
        (dest/'alignment.json').write_text(json.dumps(alignment))
        case = dict(condition=name, score=str(score), score_sha256=digest(score), bpm=bpm,
                    measures_repeated=[5,6] if name=='local' else [1,15],
                    repeat_beats=list(interval), segments=segments, duration_sec=offset,
                    first_visit_sec=start*60/bpm, replay_start_sec=end*60/bpm,
                    replay_end_sec=(2*end-start)*60/bpm,
                    repeat_sign_used=name=='notated',
                    synthesis='constant tempo, velocity 64, no pedal, note-offs at segment boundaries',
                    audio_sha256=digest(dest/'performance.wav'))
        (dest/'case.json').write_text(json.dumps(case, indent=2))
        cases.append(case)
    return cases


def run_one(case, method, out):
    from matchmaker import Matchmaker
    from matchmaker.matchmaker import DEFAULT_KWARGS
    from matchmaker.prob.outer_product_hmm_audio import AudioOuterProductHMM
    import matchmaker
    dest = out/case['condition']/method
    dest.mkdir(exist_ok=True)
    kwargs = dict(DEFAULT_KWARGS['audio'][method])
    if method == 'outerhmm':
        # The registry disables global jumps; use the class's fixed default.
        kwargs['s_j'] = inspect.signature(AudioOuterProductHMM).parameters['s_j'].default
    with (dest/'run.log').open('w') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        t = time.perf_counter()
        mm = Matchmaker(score_file=case['score'], performance_file=out/case['condition']/'performance.wav',
                        input_type='audio', method=method, unfold_score=False,
                        tempo=case['bpm'], wait=False, kwargs=kwargs)
        setup = time.perf_counter()-t
        t = time.perf_counter()
        for _ in mm.run(verbose=False):
            pass
        elapsed = time.perf_counter()-t
        raw = mm.score_follower.alignment_path.T
        np.savetxt(dest/'wp.tsv', raw, delimiter='\t', header='perf_sec\tscore_beat', comments='')
        gt = np.loadtxt(out/case['condition']/'gt.tsv', skiprows=1)
        wp = raw[np.argsort(raw[:,0], kind='stable')]
        _, first = np.unique(wp[:,0], return_index=True)
        wp = wp[np.r_[first[1:], len(wp)]-1]
        idx = np.searchsorted(wp[:,0],gt[:,0],side='right')-1
        error = np.full(len(gt), np.inf)
        valid = idx>=0
        error[valid]=abs(wp[idx[valid],1]-gt[valid,1])
        intervals={'before':gt[:,0]<case['replay_start_sec'],
                   'replay':(gt[:,0]>=case['replay_start_sec'])&(gt[:,0]<case['replay_end_sec']),
                   'after':gt[:,0]>=case['replay_end_sec']}
        summary = {name:dict(onsets=int(mask.sum()), within_1_beat=float(np.mean(error[mask]<=1)),
                             median_beat_error=float(np.median(error[mask]))) for name,mask in intervals.items()}
        hypotheses=[]
        for h in getattr(mm.score_follower, 'hypotheses', []):
            hypotheses.append({key: (value if isinstance(value,(str,int,float,bool)) else
                                     {'shape':list(value.shape)} if isinstance(value,np.ndarray) else type(value).__name__)
                               for key,value in h.items()})
        result=dict(method=method, condition=case['condition'], kwargs=kwargs,
                    unfold_score=False, tempo=case['bpm'], setup_seconds=setup, run_seconds=elapsed,
                    source=matchmaker.__file__, git_head=subprocess.check_output(
                        ['git','-C',str(Path(matchmaker.__file__).parents[1]),'rev-parse','HEAD'],text=True).strip(),
                    intervals=summary, hypotheses=hypotheses, frames=len(raw))
        (dest/'result.json').write_text(json.dumps(result,indent=2,default=str))
    print(json.dumps(result),flush=True)
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--score',type=Path,default=Path.home()/'data/batik_plays_mozart/scores_edited/kv282_1.musicxml')
    p.add_argument('--bpm',type=float,default=60.)
    p.add_argument('--reuse-inputs',action='store_true')
    p.add_argument('--methods',nargs='+',default=['arzt','arzt_multi_fold','outerhmm'])
    args=p.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    if args.reuse_inputs:
        cases=[json.loads((args.output_dir/c/'case.json').read_text()) for c in ['local','notated']]
    else:
        cases=build_cases(args.score,args.output_dir,args.bpm)
    manifest=dict(piece='Mozart, K.282, first movement',cases=cases,
                  scope='two illustrative conditions; different jump lengths, not a controlled effect of notation alone',
                  script_sha256=digest(__file__))
    (args.output_dir/'manifest.json').write_text(json.dumps(manifest,indent=2))
    results=[]
    for case in cases:
        for method in args.methods:
            results.append(run_one(case,method,args.output_dir))
    (args.output_dir/'results.json').write_text(json.dumps(results,indent=2))


if __name__=='__main__':
    main()
