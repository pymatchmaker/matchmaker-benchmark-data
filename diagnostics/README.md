# Frozen score-following diagnostic inputs

These are the actual inputs used for the Matchmaker manuscript's controlled
experiments, rather than newly synthesized replacements. `manifest.json` is the
portable experiment index; `files/` contains deduplicated, content-addressed
inputs. The companion benchmark workflow downloads only each job's files and
verifies SHA-256 before running a follower.

| Suite | Inputs | Purpose |
| --- | --- | --- |
| perturbations | 41 audio and 34 MIDI cases | K.279/III deletions, insertions, tempo oscillations/ramps, local fumbles; audio detuning; BWV 858 two-repeat condition |
| repeat_examples | 2 audio cases | K.282/I local repeat (mm. 5–6) and written repeat (mm. 1–15), first 18 measures |
| folded_batik | 24 audio performances | Recorded Batik performances and original folded scores; six development movements excluded |
| global_skip | 2 MIDI cases | K.279/III fumbles and section repetition, for symbolic OPHMM global-transition ablation |

The same input can occur in more than one suite. No aggregate combines all
103 manifest rows. `unfold_score` and nominal tempo are explicit per case.
All paths and annotations use performance seconds and score quarter-note beats;
the benchmark applies the score's meter when computing its musical-beat TR
criterion. The frozen library and benchmark revision define the evaluation.

Audio is losslessly compressed as FLAC. Decoded integer PCM was compared
sample-for-sample against each original WAV during packaging. Files above
90 MB are stored in ordered `.partNNN` chunks, reassembled and verified before
loading. This is storage chunking, not segmentation of the performance.
Source and distribution hashes are recorded separately. Original WAV container
metadata is not retained. There is no lossy re-encoding or re-synthesis.

The historical generator scripts in `generators/` document the construction
of the synthetic inputs. They include original local paths and are retained
for provenance; the CI evaluation does not run them or require those paths.
Frozen input files, not a new soundfont render, define this experiment release.
The synthetic perturbation generator uses RandomState(1984). The K.282 cases
use 60 BPM, velocity 64, no pedal, and note-offs at repeat boundaries.

## Attribution and licensing

These diagnostic derivatives are distributed under CC BY-NC-SA 4.0, as in
[the repository license](../LICENSE.md). Mozart scores, performance MIDI and
recorded folded-Batik audio derive from the Batik-plays-Mozart corpus; see
[its attribution](../batik/ATTRIBUTION.md). The Bach BWV 858 score derives from
ASAP; see [its attribution](../asap/ATTRIBUTION.md). Synthetic performances are
experimental transformations of these scores, not recordings by the corpus
performers. Cite the original corpora as detailed in [LICENSING.md](../LICENSING.md).
