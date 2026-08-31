# Matchmaker benchmark data

Audio, MIDI, scores and note-level ground-truth alignments for **146
performances** of Western classical piano music — the evaluation data behind
the [matchmaker benchmark](https://github.com/pymatchmaker/matchmaker_benchmark)
for real-time score following.

These files are the performances against which score-followers in the matchmaker 
framework are evaluated for the benchmark. For this reason, any new score-followers 
submitting to the matchmaker benchmark should **NOT** train their models on these 
performances. Users can use the data within the `experiment` branch of this repository 
to test, fine-tune and improve their score-followers.

[![Licence: CC BY-NC-SA 4.0](https://img.shields.io/badge/licence-CC%20BY--NC--SA%204.0-1f6b4f)](LICENSE.md)

This repository is not a new dataset, but offers a single location and structure 
to simplify the evaluation of various score following methods against three 
existing corpora — (n)ASAP, Batik-plays-Mozart and the Vienna 4x22 Piano
Corpus — through the Matchmaker infrastructure.


| | |
| --- | --- |
| **Performances** | 146 (32 ASAP · 30 Batik · 84 Vienna) |
| **Formats** | mp3 audio · performance MIDI · MusicXML scores · `.match` alignments |
| **Size** | ~1.1 GB |
| **Licence** | [CC BY-NC-SA 4.0](LICENSE.md) — attribution, non-commercial, share-alike |

## Layout

```
asap/     audio/  midi/  score/  match/   metadata-asap.csv    ATTRIBUTION.md
batik/    audio/  midi/  score/  match/   metadata-batik.csv   ATTRIBUTION.md
vienna/   audio/  midi/  score/  match/   metadata-vienna.csv  ATTRIBUTION.md
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

`<dataset>/metadata-<dataset>.csv` is the authoritative index of its folder:

| Column | Meaning |
| --- | --- |
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
git clone https://github.com/<owner>/<repo>.git ~/data
```

## About the audio

None of the three source corpora distributes audio, so the recordings come from
three different places:

| Dataset | Recordings | Licence |
| --- | --- | --- |
| `asap/` | MAESTRO concert recordings — many pianists, instruments and halls | CC BY-NC-SA 4.0 |
| `batik/` | The corpus MIDI replayed on a Disklavier reproducing piano at JKU and recorded there. **Not** the commercial Roland Batik release | CC BY-NC-SA 4.0 |
| `vienna/` | The original Vienna 4x22 corpus recordings | CC BY 4.0 |

Worth knowing when reading results: the Batik audio has uniform acoustics and
is synchronous with its MIDI by construction, while the ASAP audio is varied
concert recordings. Comparing one method's audio scores *across* datasets is
partly comparing recording conditions. Comparing methods *within* a dataset is
unaffected, and MIDI results are unaffected entirely.

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

This dataset exists because the authors of all three corpora made their work
available. Thanks to the (n)ASAP authors, to the Magenta team for MAESTRO, to
Patricia Hu and Gerhard Widmer for Batik-plays-Mozart, and to Werner Goebl and
the Institute of Music Acoustics at mdw for the Vienna 4x22 Piano Corpus.
