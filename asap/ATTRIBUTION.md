# (n)ASAP — attribution and licence

## Source

Symbolic data (MIDI, MusicXML scores, note alignments) from the **(n)ASAP
dataset**: <https://github.com/CPJKU/asap-dataset>

Audio from the **MAESTRO dataset v2.0.0**:
<https://magenta.tensorflow.org/datasets/maestro>

ASAP does not distribute audio itself. Its README directs users to download
MAESTRO and run `initialize_dataset.py` to pair the recordings with the ASAP
performances. The mp3s in `audio/` are those MAESTRO recordings, converted from
their original format.

## Licence

Both sources are released under
**[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)** — the
full text is in
[LICENSE-CC-BY-NC-SA-4.0.md](LICENSE-CC-BY-NC-SA-4.0.md).

| Content | Source | Licence |
| --- | --- | --- |
| MIDI, scores, alignments | [(n)ASAP](https://github.com/CPJKU/asap-dataset) | CC BY-NC-SA 4.0 |
| Audio | [MAESTRO v2.0.0](https://magenta.tensorflow.org/datasets/maestro) | CC BY-NC-SA 4.0 |


Anyone using this folder must therefore:

- **credit** both (n)ASAP and MAESTRO (citations below);
- not use it **commercially**;
- distribute any derivative under the **same licence**.

This is the licence that obliges the repository as a whole to be CC BY-NC-SA
4.0, since share-alike extends to the distribution the material is part of.

## What is here

| Folder | Files | Origin |
| --- | --- | --- |
| `audio/` | 42 mp3 | MAESTRO recordings, converted to mp3 |
| `midi/` | 42 | ASAP performance MIDI |
| `score/` | 24 MusicXML | ASAP scores |
| `match/` | 42 | Note-level alignments |

Filenames flatten the original ASAP directory structure:
`Bach/Fugue/bwv_858/Zhang01M.mid` → `midi/Bach_Fugue_bwv_858_Zhang01M.mid`.

## Citation

Cite both the ASAP papers and MAESTRO.

```bibtex
@article{Peter-2023,
 title = {Automatic Note-Level Score-to-Performance Alignments in the ASAP Dataset},
 author = {Peter, Silvan David and Cancino-Chacón, Carlos Eduardo and Foscarin, Francesco and McLeod, Andrew Philip and Henkel, Florian and Karystinaios, Emmanouil and Widmer, Gerhard},
 doi = {10.5334/tismir.149},
 journal = {Transactions of the International Society for Music Information Retrieval {(TISMIR)}},
 year = {2023}
}

@inproceedings{asap-dataset,
  title     = {{ASAP}: a dataset of aligned scores and performances for piano transcription},
  author    = {Foscarin, Francesco and McLeod, Andrew and Rigaux, Philippe and
               Jacquemard, Florent and Sakai, Masahiko},
  booktitle = {International Society for Music Information Retrieval Conference (ISMIR)},
  year      = {2020}
}

@inproceedings{hawthorne2019maestro,
  title     = {Enabling Factorized Piano Music Modeling and Generation with the
               {MAESTRO} Dataset},
  author    = {Hawthorne, Curtis and Stasyuk, Andriy and Roberts, Adam and
               Simon, Ian and Huang, Cheng-Zhi Anna and Dieleman, Sander and
               Elsen, Erich and Engel, Jesse and Eck, Douglas},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2019}
}
```

The note-level alignments come from the (n)ASAP extension; check the ASAP
repository's README for the additional TISMIR citation if you use those
specifically.
