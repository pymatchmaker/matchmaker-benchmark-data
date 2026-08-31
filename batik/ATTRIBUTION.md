# Batik-plays-Mozart — attribution and licence

## Source

Symbolic data from **The Batik-plays-Mozart corpus**:
<https://github.com/huispaty/batik_plays_mozart>

Twelve complete Mozart piano sonatas performed by Viennese concert pianist
**Roland Batik** on a computer-monitored Bösendorfer grand piano, note-aligned
to scores from the New Mozart Edition.

## Licence

**[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)** — the
licence applied to the corpus by its authors. The full text is in
[LICENSE-CC-BY-NC-SA-4.0.md](LICENSE-CC-BY-NC-SA-4.0.md).

You may share and adapt this material provided you credit the corpus (see the
citation below), do not use it commercially, and distribute anything built on
it under the same licence.

The Disklavier recordings in `audio/` were made at the Institute of
Computational Perception, JKU Linz, and are distributed under the same terms.

## The audio is a new recording, not the commercial release

> The Batik corpus README notes that "the audio files are commercially
> available", and the corpus itself ships no audio. **The recordings in
> `audio/` are not that commercial release.**

They were produced for this benchmark by replaying the corpus performance MIDI
on a **Yamaha Disklavier reproducing piano** at the Institute of Computational
Perception, Johannes Kepler University Linz, and recording the result. The
recordings are therefore the institute's own.

This is a **reproducing-piano rendering of a recorded performance**, not a
microphone recording of a pianist playing live. The performance timing and
dynamics are Roland Batik's, faithfully replayed; the room, the instrument and
the recording chain are the institute's.

The acoustic conditions are uniform across the whole Batik set and differ from 
the ASAP audio (concert recordings via MAESTRO) and the Vienna audio (the 
original corpus recordings). Results on this dataset should be read with that 
in mind, and comparisons across the three datasets are comparisons across three 
different recording conditions.

## What is here

| Folder | Files | Origin |
| --- | --- | --- |
| `audio/` | 30 mp3 | Disklavier recordings made at JKU from the corpus MIDI |
| `midi/` | 30 | Performance MIDI from the corpus |
| `score/` | 30 MusicXML | Scores from the corpus |
| `match/` | 30 | Note-level alignments from the corpus |

## Citation

```bibtex
@inproceedings{hu2023batik,
  title     = {{The Batik-plays-Mozart Corpus: Linking Performance to Score to
               Musicological Annotations}},
  author    = {Hu, Patricia and Widmer, Gerhard},
  booktitle = {Proceedings of the International Society for Music Information
               Retrieval Conference (ISMIR)},
  year      = {2023}
}
```

The musicological harmony, cadence and phrase annotations that the corpus links
to were published separately as *The Annotated Mozart Sonatas*
(<https://transactions.ismir.net/articles/10.5334/tismir.63>); cite that too if
you use them.

If you use the audio, please note in your write-up that it is a Disklavier
rendering of the corpus MIDI rather than the commercial recording.

## Acknowledgment

The corpus was supported by the European Research Council (ERC) under the EU's
Horizon 2020 research and innovation programme, grant agreement No. 10101937
("Whither Music?").
