# Matchmaker benchmark data

Audio, MIDI, scores and note-level ground-truth alignments for **20
performances** of Western classical piano music — the evaluation data behind
the [matchmaker benchmark](https://github.com/pymatchmaker/matchmaker_benchmark)
for real-time score following. This data is intended to be used locally in the 
user's machine in order to test the implementation of a score-follow and to also 
fine-tune its parameters. The benchmark results do not take the results of these 
performances into consideration.

[![Licence: CC BY-NC-SA 4.0](https://img.shields.io/badge/licence-CC%20BY--NC--SA%204.0-1f6b4f)](LICENSE.md)

This repository is not a new dataset, but offers a single location and structure 
to simplify the evaluation of various score following methods against three 
existing corpora — (n)ASAP, Batik-plays-Mozart and the Vienna 4x22 Piano
Corpus — through the Matchmaker infrastructure.


| | |
| --- | --- |
| **Performances** | 20 (10 ASAP · 6 Batik · 4 Vienna) |
| **Formats** | mp3 audio · performance MIDI · MusicXML scores · `.match` alignments |
| **Licence** | [CC BY-NC-SA 4.0](LICENSE.md) — attribution, non-commercial, share-alike |

## Layout

```
asap/     audio/  midi/  score/  match/   ATTRIBUTION.md
batik/    audio/  midi/  score/  match/   ATTRIBUTION.md
vienna/   audio/  midi/  score/  match/   ATTRIBUTION.md
```

| Folder | Contents |
| --- | --- |
| `audio/` | Performance audio, mp3 |
| `midi/` | Performance MIDI |
| `score/` | Scores, MusicXML |
| `match/` | Note-level performance-to-score alignments, [match format](https://arxiv.org/abs/2206.01104) |

Filenames flatten the corpora's original directory structures. For ASAP the
path becomes the name — `Bach/Fugue/bwv_858/Zhang01M.mid` →
`midi/Bach_Fugue_bwv_858_Zhang01M.mid`; for Batik and Vienna the basename is
kept.

## Read paths from the metadata

`metadata-experiment.csv` is the authoritative index of its folder:

| Column | Meaning |
| --- | --- |
| `dataset` | The dataset to which this performance belongs |
| `audio` | Performance audio, relative to the dataset folder |
| `score` | Score |
| `midi` | Performance MIDI |
| `match` | Note alignment |

Take paths from these files rather than reconstructing them from a naming rule.
That way the layout here can change without breaking anything downstream — the
benchmark works this way (`make_folds.py --from-repo`), and the metadata is
what makes it possible.

## Getting the data

**With the benchmark** — individual files are fetched over HTTPS as needed, so
no clone and no full download:

```bash
export MATCHMAKER_DATA_DIR=~/data
python matchmaker_eval/fetch_data.py --fold eval --input-type audio
```

**Directly** — clone it and point `MATCHMAKER_DATA_DIR` at the result:

```bash
git clone --branch experiment --single-branch \
    https://github.com/pymatchmaker/matchmaker-benchmark-data.git
```

## Audio data sources for (n)ASAP and Batik Datasets

**(n)ASAP** — MAESTRO concert recordings, converted to mp3. ASAP's instructions
tell users to download MAESTRO and pair it with the performances; that step is
already done here.

**Batik** — the corpus performance MIDI replayed on a Yamaha Disklavier
reproducing piano at the Institute of Computational Perception, Johannes Kepler 
University, and recorded there. This is **not** the commercial Roland Batik release. 
The timing and dynamics are derived from Roland Batik's MIDI performances; the instrument, 
room and recording chain are the institute's.

## Licence and credit

[CC BY-NC-SA 4.0](LICENSE.md): use it, redistribute it, build on it — with
attribution, not commercially, and share-alike.

**Using this data means citing the corpora it comes from.** The citations are
in [LICENSING.md](LICENSING.md) and, in full, in each dataset folder's
`ATTRIBUTION.md`. Citing this repository is not a substitute: it contains no
original scores or performances.

- [asap/ATTRIBUTION.md](asap/ATTRIBUTION.md) — ASAP and MAESTRO (CC BY-NC-SA 4.0)
- [batik/ATTRIBUTION.md](batik/ATTRIBUTION.md) — Batik-plays-Mozart (CC BY-NC-SA 4.0), and how the recordings were made
- [vienna/ATTRIBUTION.md](vienna/ATTRIBUTION.md) — Vienna 4x22 by Werner Goebl (CC BY 4.0)

## Acknowledgments
This work has been supported by the Austrian Science Fund (FWF), grant agreement 
PAT 8820923 (Rach3: A Computational Approach to Study Piano Rehearsals) and PIN 1347924 
(AURA: Augmenting musical interaction via EVAs), as well as by the European Research Council (ERC) 
under the EU’s Horizon 2020 research & innovation programme, grant agreement 
No.101019375 (Whither Music?), and by the National Research Foundation of Korea (NRF) grant 
funded by the Korea government (MSIT) under Grant RS-2023-NR077289.


This dataset exists because the authors of all three corpora made their work
available.
