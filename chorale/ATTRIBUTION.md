# ChoraleBricks — attribution and licence

## Source

**ChoraleBricks** is the multitrack corpus of chorale recordings and scores released by Stefan Balke, Axel Berndt and Meinard Müller:

- Repository: <https://github.com/stefan-balke/choralebricks>
- Related publication: Balke, Berndt and Müller, “ChoraleBricks: A Modular Multitrack Dataset for Wind Music Research” (TISMIR, 2025)

The dataset contains multiple recordings of chorale excerpts, each with corresponding score data and alignment annotations for research in multitrack and wind-music analysis.

## Licence

This corpus is released under the **MIT License**. The full text is in [LICENSE](LICENSE).

You may use, copy, modify, merge, publish, distribute and sublicense the material, provided that the copyright notice and permission notice are included in all copies or substantial portions of the work.

This folder remains under the original corpus licence. The repository as a whole is distributed under CC BY-NC-SA 4.0 because of the other datasets it contains; that does not narrow your rights to the ChoraleBricks material, which remains available under the MIT licence from its source.

## What is here

| Folder | Files | Origin |
| --- | --- | --- |
| `audio/` | 191 mp3 | ChoraleBricks multitrack performance recordings |
| `score/` | 61 MusicXML | Original chorale part scores, and 21 octave-shifted copies |
| `annotations/` | 191 TSV | Performance-to-score alignment annotations |

Each part score is shared by every instrument that plays the part, but the flute and baritone stems of part 01 sound an octave above or below the notated part, and the tuba stems of part 04 an octave below. For those 21 stems, `metadata-chorale.csv` points to a copy of the part score moved by that octave (`*_8va.musicxml`, `*_8vb.musicxml`); the copies differ from the original only in their pitches.

The metadata index in `metadata-chorale.csv` is the authoritative list of the files in this folder.

## Citation

```bibtex
@article{BalkeBM24_ChoraleBricks,
  author  = {Stefan Balke and Axel Berndt and Meinard M{"u}ller},
  title   = {{ChoraleBricks}: A Modular Multitrack Dataset for Wind Music Research},
  journal = {Transactions of the International Society for Music Information Retrieval},
  volume = {8},
  number = {1},
  pages = {39--54},
  year = {2025},
  doi = {10.5334/tismir.252}
}
```

## Acknowledgment

Please credit the original ChoraleBricks authors when using this material, and preserve the MIT license notice if you redistribute the files.
