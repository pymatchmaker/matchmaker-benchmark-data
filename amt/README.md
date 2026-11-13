# AMT outputs

The 146 transcription MIDI files used for the AMT + symbolic-follower
comparison, one per piano performance in the `eval` fold (32 (n)ASAP, 30 Batik,
84 Vienna4x22). They are the output of the online AMT model of Kwon et al.
(2024), which is not included. `manifest.json` maps each file to its piece ID
and SHA-256.

The benchmark's `evaluate-amt.yml` feeds these files to a symbolic follower and
scores it against the original performance annotations. MIDI timestamps are
unchanged, so the measured time covers the follower only.

Licensed under CC BY-NC-SA 4.0, as in [the repository license](../LICENSE.md).
See `../asap`, `../batik` and `../vienna` for the corpus attribution and
[LICENSING.md](../LICENSING.md) for citations.
