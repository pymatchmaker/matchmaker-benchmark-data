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
| `score/` | 40 MusicXML | Original chorale scores |
| `annotations/` | 191 TSV | Performance-to-score alignment annotations |

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
