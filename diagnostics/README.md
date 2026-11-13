# Diagnostic inputs

Inputs for the score-following diagnostics that the benchmark runs in
`evaluate-diagnostics.yml`. `manifest.json` lists every case and the SHA-256 of
each file in `files/`. One file can be used by several cases.

| Suite | Cases | What it tests |
| --- | --- | --- |
| perturbations | 41 audio, 34 MIDI | K.279/III with deletions, insertions, tempo changes and local fumbles; detuned audio; BWV 858 with two repeats |
| repeat_examples | 2 audio | K.282/I with a local repeat (mm. 5–6) and the written repeat (mm. 1–15), first 18 measures |
| folded_batik | 24 audio | Batik recordings followed on their folded (not unfolded) scores |
| global_skip | 2 MIDI | K.279/III fumbles and a repeated section, for the OPHMM global-skip ablation |

Annotations are in performance seconds and score beats (denominator notes).
Audio is mp3. The folded Batik audio is the same file as `batik/audio/` on the
`eval` branch.

## Attribution and licensing

Distributed under CC BY-NC-SA 4.0, as in [the repository license](../LICENSE.md).
The Mozart scores, performance MIDI and Batik recordings come from the
Batik-plays-Mozart corpus ([attribution](../batik/ATTRIBUTION.md)); the BWV 858
score comes from ASAP ([attribution](../asap/ATTRIBUTION.md)). The perturbed
performances are synthetic transformations of these scores, not recordings by
the corpus performers. See [LICENSING.md](../LICENSING.md) for citations.
