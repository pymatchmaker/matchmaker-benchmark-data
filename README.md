# Matchmaker benchmark data

## Solo Piano Datasets

Included are audio, MIDI, scores and note-level ground-truth alignments for **166
performances** of Western classical piano music — the evaluation data behind
the [matchmaker benchmark](https://github.com/pymatchmaker/matchmaker_benchmark)
for real-time score following. These datasets are: 
- [(n)ASAP](https://github.com/CPJKU/asap-dataset) 
- [Batik Plays Mozart](https://github.com/huispaty/batik_plays_mozart)
- [Vienna 4x22 Corpus](https://github.com/CPJKU/vienna4x22)

[![Licence: CC BY-NC-SA 4.0](https://img.shields.io/badge/licence-CC%20BY--NC--SA%204.0-1f6b4f)](LICENSE.md)

| | |
| --- | --- |
| **Performances** | 166 (42 ASAP · 36 Batik · 88 Vienna) |
| **Formats** | mp3 audio · performance MIDI · MusicXML scores · `.match` alignments |
| **Size** | ~980 MB |
| **Licence** | [CC BY-NC-SA 4.0](LICENSE.md) — attribution, non-commercial, share-alike |

## Beyond Piano-Solo Datasets

Four other datasets of music performances, along with their scores and alignment 
annotations are also included in this collection, in order to test score-followers 
against music-performance datasets that are not restricted to solo piano performances. 
These datasets are: 
- [ChoraleBricks](https://github.com/stefan-balke/choralebricks)
- [KRAISLER](https://zenodo.org/records/21082251)
- [URMP](https://datadryad.org/dataset/doi:10.5061/dryad.ng3r749)
- [Schubert Winterreise Dataset](https://zenodo.org/records/4122060)

## Note

The `main` branch of this repository contains data pertaining to a total of 
166 piano performances from the three solo-piano corpora and all the performances 
from the beyond piano-solo datasets. The matchmaker benchmark however utilizes 
146 of the piano-solo performances and all the beyond piano-solo performances 
in the `benchmark` branch of this repository in order to 
evaluate the different score-followers (including future submissions to the 
matchmaker benchmark repository; refer to the 
[repository](https://github.com/pymatchmaker/matchmaker_benchmark) for 
instructions on how to make your own submission). For that reason, any future 
score-following implementation being submitted to the benchmark must not 
train its score-follower on the data inside the `main` or the `benchmark` branch of this 
repository. Instead, users can use the performances within the `experiment` 
branch of this repository while developing and fine-tuning their score-follower.

## Layout

This repository is not a new dataset, but offers a single location and structure 
to simplify the evaluation of various score following methods against all the 
existing corpora through the Matchmaker infrastructure.


```
asap/     audio/  midi/  score/  match/   metadata-asap.csv    ATTRIBUTION.md

batik/    audio/  midi/  score/  match/   metadata-batik.csv   ATTRIBUTION.md

vienna/   audio/  midi/  score/  match/   metadata-vienna.csv  ATTRIBUTION.md

chorale/   audio/  score/  annotations/   metadata-chorale.csv

urmp/   audio/  score/  annotations/   metadata-urmp.csv

kraisler/   audio/  score/  annotations/   metadata-kraisler.csv

winterreise/   audio/  score/  annotations/   metadata-winterreise.csv
```

| Folder | Contents |
| --- | --- |
| `audio/` | Performance audio, mp3 |
| `midi/` | Performance MIDI |
| `score/` | Scores, MusicXML |
| `match/` | Note-level performance-to-score alignments, [match format](https://arxiv.org/abs/2206.01104) |
| `annotations/` | TSV format performance-to-score alignments |

Filenames flatten the corpora's original directory structures. For ASAP the
path becomes the name — `Bach/Fugue/bwv_858/Zhang01M.mid` →
`midi/Bach_Fugue_bwv_858_Zhang01M.mid`; for Batik and Vienna the basename is
kept.

## Read paths from the metadata

`<dataset>/metadata-<dataset>.csv` is the authoritative index of its folder:

| Column | Meaning |
| --- | --- |
| `audio` | Performance audio, relative to the dataset folder |
| `score` | Score |
| `midi` | Performance MIDI |
| `match` | Note alignment |
| `annotations` | Performance-to-score alignment |

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
git clone https://github.com/pymatchmaker/matchmaker-benchmark-data.git
```

## Audio data sources for (n)ASAP and Batik Datasets

**(n)ASAP** — MAESTRO concert recordings, converted to mp3. ASAP's instructions
tell users to download MAESTRO and pair it with the performances; that step is
already done here.

**Batik** — the corpus performance MIDI replayed on a Yamaha Disklavier
reproducing piano at the Institute of Computational Perception, Johannes Kepler University, and
recorded there. This is **not** the commercial Roland Batik release. The timing and
dynamics are derived from Roland Batik's MIDI performances; the instrument, room and recording 
chain are the institute's.

## Licence and credit

**Using this data means citing the corpora it comes from.** The citations are
in [LICENSING.md](LICENSING.md) and, in full, in each dataset folder's
`ATTRIBUTION.md`. Citing this repository is not a substitute.

## Acknowledgments
This work has been supported by the Austrian Science Fund (FWF), grant agreement 
PAT 8820923 (Rach3: A Computational Approach to Study Piano Rehearsals) and PIN 1347924 
(AURA: Augmenting musical interaction via EVAs), as well as by the European Research Council (ERC) 
under the EU’s Horizon 2020 research & innovation programme, grant agreement 
No.101019375 (Whither Music?), and by the National Research Foundation of Korea (NRF) grant 
funded by the Korea government (MSIT) under Grant RS-2023-NR077289.


This dataset exists because the authors of all three corpora made their work
available.
