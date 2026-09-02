# Licensing and attribution

**This data is licensed under
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).**
The full text is in [LICENSE.md](LICENSE.md).

In short, you may copy, redistribute and build on this data, including
reformatting or re-encoding it, provided you:

- **credit** the corpora it comes from — the citations are below and in each
  dataset folder's `ATTRIBUTION.md`;
- do not use it for **commercial** purposes;
- release anything you distribute that is built on it under the **same
  licence**.

CC BY-NC-SA 4.0 is the licence of the (n)ASAP corpus, of the MAESTRO recordings it
uses, and of the Batik-plays-Mozart corpus. Share-alike obliges the whole
distribution to match. The Vienna material is CC BY 4.0 at source, which is
compatible; including it here does not narrow anyone's rights to it from its
own source.

Note that the licence covers this **data**. The benchmark software that reads
it is a separate work under its own licence.

## Where each part comes from

| Content | Source | Terms |
| --- | --- | --- |
| `asap/` MIDI, scores, match | [CPJKU/asap-dataset](https://github.com/CPJKU/asap-dataset) | CC BY-NC-SA 4.0 |
| `asap/audio` | [MAESTRO v2.0.0](https://magenta.tensorflow.org/datasets/maestro) | CC BY-NC-SA 4.0 |
| `batik/` MIDI, scores, match | [huispaty/batik_plays_mozart](https://github.com/huispaty/batik_plays_mozart) | CC BY-NC-SA 4.0 |
| `batik/audio` | Recorded at JKU on a Disklavier from the corpus MIDI | CC BY-NC-SA 4.0 |
| `vienna/` all | [Vienna 4x22 Piano Corpus](http://dx.doi.org/10.21939/4X22) by Werner Goebl, via [CPJKU/vienna4x22](https://github.com/CPJKU/vienna4x22) | CC BY 4.0 |

Per-folder licence texts:
[asap/LICENSE-CC-BY-NC-SA-4.0.md](asap/LICENSE-CC-BY-NC-SA-4.0.md),
[batik/LICENSE-CC-BY-NC-SA-4.0.md](batik/LICENSE-CC-BY-NC-SA-4.0.md),
[vienna/LICENSE-CC-BY-4.0.txt](vienna/LICENSE-CC-BY-4.0.txt).

## Audio data sources for (n)ASAP and Batik Datasets

**(n)ASAP** — MAESTRO concert recordings, converted to mp3. ASAP's instructions
tell users to download MAESTRO and pair it with the performances; that step is
already done here.

**Batik** — the corpus performance MIDI replayed on a Yamaha Disklavier
reproducing piano at the Institute of Computational Perception, Johannes Kepler 
University, and recorded there. This is **not** the commercial Roland Batik release. 
The timing and dynamics are derived from Roland Batik's MIDI performances; the instrument, 
room and recording chain are the institute's.

## Citing

Using this data means citing the corpora it comes from. Citing this repository
is not a substitute — it contains no original scores or performances.

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

@inproceedings{hu2023batik,
  title     = {{The Batik-plays-Mozart Corpus: Linking Performance to Score to
               Musicological Annotations}},
  author    = {Hu, Patricia and Widmer, Gerhard},
  booktitle = {Proceedings of the International Society for Music Information
               Retrieval Conference (ISMIR)},
  year      = {2023}
}
```

```bibtex
@electronic{vienna4x22,
  author       = {Goebl, Werner},
  year         = {1999},
  title        = {The Vienna 4x22 Piano Corpus},
  language     = {English},
  howpublished = {\url{http://dx.doi.org/10.21939/4X22}},
  doi          = {10.21939/4X22},
  owner        = {mdw}
}
```

Each dataset folder's `ATTRIBUTION.md` carries the full detail, including the
note-level (n)ASAP alignments and *The Annotated Mozart Sonatas* annotations
that the Batik corpus links to.

## Redistributing onward

The CC BY-NC-SA licence lets you redistribute this data under the same terms.
Please credit the original corpora as described above, and if you are
repackaging any of it as a dataset of your own, a note to the corpus authors is
the courteous step.
