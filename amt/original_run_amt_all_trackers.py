#!/usr/bin/env python
"""
Benchmark AMT + all MIDI score followers on the piano test split:
  - (n)ASAP (N=32)
  - Batik plays Mozart (N=30)
  - Vienna 4x22 (N=84)
Total: 146 performances.

Evaluates:
  - Tracking Rate (TR %) with W=30s, theta=1.0b
  - Method-Tracked Subset (event-pooled MeanAE +- std, MedAE, <=0.5b, <=1.0b, SPARC, RTF)
  - Common-Tracked Subset (event-pooled MeanAE +- std, MedAE, <=0.5b, <=1.0b, SPARC)
"""

import argparse
import copy
import json
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import partitura as pt

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "matchmaker_eval"))

from eval import compute_sparc, evaluate_alignment
from folds import nested_dataset_root
from matchmaker import Matchmaker
from matchmaker.matchmaker import DEFAULT_KWARGS
from matchmaker.utils.eval import resolve_gt, transfer_positions
from utils import (
    TOLERANCES_IN_BEATS,
    TOLERANCES_IN_MS,
    compute_event_pooled_summary,
    save_nparray_to_csv,
)
from verify_tracking import check_tracking

DATASETS = ["asap", "batik", "vienna"]
CANDIDATE_TRACKERS = [
    "arzt",
    "dixon",
    "hmm",
    "pthmm",
    "outerhmm",
    "SLT_OLTW",
    "SL_OLTW",
    "OTM",
    "OPTM",
]

COMMON_INDICES = {
    "asap": {1, 2, 3, 4, 5, 6, 9, 10, 30, 31, 32},
    "batik": {4, 5, 10, 13, 15, 25},
    "vienna": {
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 68, 72, 74, 77, 78, 79, 81, 82, 84,
    },
}

AMT_ROOTS = {
    "asap": Path("/home/jiyun/data/matchmaker-amt-output/asap"),
    "batik": Path("/home/jiyun/data/matchmaker-amt-output/batik"),
    "vienna": Path("/home/jiyun/data/matchmaker-amt-output/vienna4x22"),
}

CACHED_AMT_DIRS = {
    "asap": REPO_ROOT / "output/test_2026-04-10-18:29:07_amt_pipeline_pthmm_asap",
    "batik": REPO_ROOT / "output/test_2026-04-10-18:54:36_amt_pipeline_pthmm_batik",
    "vienna": REPO_ROOT / "output/test_2026-04-10-19:37:59_amt_pipeline_pthmm_vienna",
}


def load_piece_metadata(dataset: str):
    meta_path = REPO_ROOT / f"data/reduced/metadata-{dataset}.csv"
    df = pd.read_csv(meta_path)
    ds_root = nested_dataset_root(dataset)
    amt_root = AMT_ROOTS[dataset]
    cached_dir = CACHED_AMT_DIRS[dataset]

    pieces = []
    for i, row in enumerate(df.itertuples(), 1):
        score_xml = ds_root / row.xml_score
        match_path = ds_root / row.match
        if dataset == "asap":
            amt_midi = amt_root / row.midi_performance
            piece_name = row.title
            perf_name = Path(row.midi_performance).stem
        else:
            amt_midi = amt_root / Path(row.midi_performance).name
            piece_name = row.title
            perf_name = Path(row.midi_performance).stem

        # Load cached amt_sec and audio_sec
        cached_json = cached_dir / f"{i}.json"
        amt_sec, audio_sec = 0.0, 1.0
        if cached_json.exists():
            with open(cached_json) as f:
                c_data = json.load(f)
                amt_sec = c_data.get("amt_sec", 0.0)
                audio_sec = c_data.get("audio_sec", 1.0)

        pieces.append({
            "index": i,
            "piece": piece_name,
            "name": perf_name,
            "score_xml": str(score_xml),
            "match_path": str(match_path),
            "amt_midi": str(amt_midi),
            "amt_sec": amt_sec,
            "audio_sec": audio_sec,
        })
    return pieces


def evaluate_one_piece(piece_info: dict, method: str, run_dir: Path):
    score_xml = piece_info["score_xml"]
    amt_midi = piece_info["amt_midi"]
    match_path = piece_info["match_path"]
    idx = piece_info["index"]
    amt_sec = piece_info["amt_sec"]
    audio_sec = piece_info["audio_sec"]

    t0 = time.time()
    try:
        mm = Matchmaker(
            score_file=score_xml,
            performance_file=amt_midi,
            input_type="midi",
            method=method,
        )
        list(mm.run(verbose=False))
        mm_sec = time.time() - t0

        wp = mm.score_follower.alignment_path
        wp_perf_sec = mm._wp_perf_to_seconds(wp[0].astype(float))
        wp = np.stack([wp_perf_sec, wp[1].astype(float)])
        wp_T = wp.T if wp.shape[0] == 2 else wp

        ps, sb = resolve_gt(match_path, mm.score_part.note_array())
        gt = np.column_stack([ps, sb])

        # Tracking check at Table 3 standard: W=30s, theta=1.0 beat
        tr = check_tracking(wp_T, gt, segment_duration=30.0, threshold=1.0)
        is_tracked = bool(tr["tracked"])
        max_dev = float(tr["max_deviation"])
        n_failed = int(tr["n_failed"])

        # SPARC
        sparc_val = compute_sparc(wp_T[:, 1], wp_T[:, 0])

        # Pipeline RTF
        pipeline_sec = amt_sec + mm_sec
        rtf = pipeline_sec / audio_sec if audio_sec > 0 else 0.0

        # Save TSVs
        run_dir.mkdir(parents=True, exist_ok=True)
        save_nparray_to_csv(
            wp_T,
            (run_dir / f"wp_{idx}.tsv").as_posix(),
            header="perf_sec\tscore_beat",
        )
        save_nparray_to_csv(
            gt,
            (run_dir / f"gt_{idx}.tsv").as_posix(),
            header="perf_sec\tscore_beat",
        )

        return {
            "Index": idx,
            "Piece": piece_info["piece"],
            "Name": piece_info["name"],
            "tracked": is_tracked,
            "max_deviation": max_dev,
            "n_failed_segments": n_failed,
            "sparc": sparc_val,
            "amt_sec": amt_sec,
            "mm_sec": mm_sec,
            "pipeline_sec": pipeline_sec,
            "audio_sec": audio_sec,
            "rtf": rtf,
            "error": None,
        }
    except Exception as e:
        return {
            "Index": idx,
            "Piece": piece_info["piece"],
            "Name": piece_info["name"],
            "tracked": False,
            "max_deviation": 999.0,
            "n_failed_segments": 999,
            "sparc": -999.0,
            "amt_sec": amt_sec,
            "mm_sec": 0.0,
            "pipeline_sec": amt_sec,
            "audio_sec": audio_sec,
            "rtf": amt_sec / audio_sec if audio_sec > 0 else 0.0,
            "error": str(e),
        }


def run_dataset_method(dataset: str, method: str, num_workers: int = 6):
    pieces = load_piece_metadata(dataset)
    run_dir = REPO_ROOT / f"output/amt_bench_{method}_{dataset}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n>>> Running {dataset.upper()} with method={method} ({len(pieces)} pieces, workers={num_workers})...", flush=True)
    results_list = [None] * len(pieces)

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_idx = {
            executor.submit(evaluate_one_piece, p, method, run_dir): p["index"] - 1
            for p in pieces
        }
        for future in as_completed(future_to_idx):
            idx0 = future_to_idx[future]
            res = future.result()
            results_list[idx0] = res

    # Build results dict for compute_event_pooled_summary
    results_dict = defaultdict(list)
    for r in results_list:
        for k, v in r.items():
            results_dict[k].append(v)

    # Save per-piece results TSV
    res_df = pd.DataFrame(results_dict)
    res_tsv = REPO_ROOT / f"final_results/amt_{method}_{dataset}.tsv"
    res_tsv.parent.mkdir(parents=True, exist_ok=True)
    res_df.to_csv(res_tsv, sep="\t", index=False)

    # Compute Method-Tracked summary
    summary_method = compute_event_pooled_summary(
        results_dict,
        run_dir=run_dir,
        tracked_only=True,
        common_indices=None,
    )

    # Compute Common-Tracked summary
    c_indices = COMMON_INDICES[dataset]
    summary_common = compute_event_pooled_summary(
        results_dict,
        run_dir=run_dir,
        tracked_only=True,
        common_indices=c_indices,
    )

    tr_pct = summary_method.get("tracking_rate", 0.0) * 100
    n_meth = summary_method.get("selected_count", 0)
    m_b = summary_method.get("beat", {})
    m_mean = m_b.get("mean", 0.0)
    m_std = m_b.get("std", 0.0)
    m_med = m_b.get("median", 0.0)
    m_05 = m_b.get("0.5b", 0.0) * 100
    m_10 = m_b.get("1.0b", 0.0) * 100
    m_sparc = summary_method.get("sparc", 0.0)
    m_rtf = summary_method.get("rtf", 0.0)

    n_com = summary_common.get("selected_count", 0)
    c_b = summary_common.get("beat", {})
    c_mean = c_b.get("mean", 0.0)
    c_std = c_b.get("std", 0.0)
    c_med = c_b.get("median", 0.0)
    c_05 = c_b.get("0.5b", 0.0) * 100
    c_10 = c_b.get("1.0b", 0.0) * 100
    c_sparc = summary_common.get("sparc", 0.0)

    print(f"  [RESULT {dataset.upper()} | {method}]")
    print(f"    TR: {tr_pct:.1f}% ({n_meth}/{len(pieces)}) | RTF: {m_rtf:.3f}")
    print(f"    Method-Tracked: Mean={m_mean:.2f}+-{m_std:.2f}, Med={m_med:.2f}, <=0.5b={m_05:.1f}%, <=1.0b={m_10:.1f}%, SPARC={m_sparc:.2f}")
    print(f"    Common-Tracked: ({n_com} pcs) Mean={c_mean:.2f}+-{c_std:.2f}, Med={c_med:.2f}, <=0.5b={c_05:.1f}%, <=1.0b={c_10:.1f}%, SPARC={c_sparc:.2f}", flush=True)

    return {
        "dataset": dataset,
        "method": method,
        "n_total": len(pieces),
        "method_summary": summary_method,
        "common_summary": summary_common,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=DATASETS + ["all"], default="all")
    parser.add_argument("--method", default="all")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    datasets = DATASETS if args.dataset == "all" else [args.dataset]
    methods = CANDIDATE_TRACKERS if args.method == "all" else [args.method]

    summary_out = REPO_ROOT / "final_results/amt_all_trackers_summary.json"
    existing_summaries = {}
    if summary_out.exists():
        try:
            with open(summary_out) as f:
                loaded = json.load(f)
                for item in loaded:
                    k = (item["dataset"], item["method"])
                    existing_summaries[k] = item
        except Exception:
            pass

    for ds in datasets:
        for m in methods:
            summary = run_dataset_method(ds, m, num_workers=args.workers)
            existing_summaries[(ds, m)] = summary

            # Incrementally save
            with open(summary_out, "w") as f:
                json.dump(list(existing_summaries.values()), f, indent=2)

    print("\n" + "=" * 80)
    print("ALL RUNS COMPLETE. Summary saved to:", summary_out)
    print("=" * 80)


if __name__ == "__main__":
    main()
