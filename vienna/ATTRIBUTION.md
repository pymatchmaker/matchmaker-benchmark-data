# Vienna 4x22 Piano Corpus — attribution and licence

## Source

**The Vienna 4x22 Piano Corpus**, collected by **Werner Goebl**
(Institute of Music Acoustics, mdw — University of Music and Performing Arts
Vienna).

- Corpus DOI: <http://dx.doi.org/10.21939/4X22>
- Repository the files here come from: <https://github.com/CPJKU/vienna4x22>

Twenty-two performances by professional pianists of four excerpts from the
classical piano repertoire:

1. Chopin, op. 38, bars 1–46
2. Chopin, op. 10 no. 3, bars 1–22
3. Schubert, D783 no. 15, bars 1–33
4. Mozart, K331 1st movement, bars 1–36

## Licence

**[Creative Commons Attribution 4.0 International (CC BY
4.0)](https://creativecommons.org/licenses/by/4.0/)** — the full text is in
[LICENSE-CC-BY-4.0.txt](LICENSE-CC-BY-4.0.txt).

You may share and adapt this material, including commercially, provided you
give appropriate credit to Werner Goebl and the corpus (see the citation
below), link to the licence, and indicate whether changes were made.

CC BY is more permissive than the licence covering this repository as a whole.
The repository is distributed under CC BY-NC-SA 4.0 because of the ASAP and
MAESTRO content it also contains; that does not narrow your rights to *this*
material, which remains available under CC BY 4.0 from the sources above.

Updates to the match files by members of the Institute of Computational
Perception are distributed under the same CC BY 4.0 terms.

## What is here

| Folder | Files | Origin |
| --- | --- | --- |
| `audio/` | 88 mp3 | Vienna 4x22 corpus recordings |
| `midi/` | 88 | Performance MIDI |
| `score/` | 4 MusicXML | Scores |
| `match/` | 88 | Note-level alignments, match format version 1.0.0 |

The score count is lower than the performance count because the four excerpts
are shared across all 22 performances.

## Citation

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

## Note on the alignments

Match file format version 1.0.0, readable with
[partitura](https://github.com/CPJKU/partitura) >= 1.2.0. Note `id` attributes
in the MusicXML correspond to the `Anchor` fields in the `snote` elements of
the match files.
