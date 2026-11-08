# Frozen AMT outputs for the piano reference comparison

This collection contains the 146 author-provided transcription MIDI files used
for the manuscript's AMT + symbolic-follower comparison. The test performances
are the same 32 (n)ASAP, 30 Batik, and 84 Vienna4x22 inputs in the `eval` fold.
`manifest.json` maps every file to its test ID and records its SHA-256.

The private front end from Kwon et al. (2024) is not included or run by CI.
The public workflow runs the symbolic follower on these frozen transcription
outputs and evaluates against the original performance annotations, not against
the transcribed notes. MIDI timestamps are unchanged. A CI processing time
therefore measures the follower only, not end-to-end AMT computation or latency.

`original_run_amt_all_trackers.py` documents the historical source selection;
its local paths and old evaluation settings are not used by the CI workflow.
The public benchmark supplies the current common scoring rules.

These derivative annotations follow the repository's CC BY-NC-SA 4.0 license.
See the original corpus attribution in `../asap`, `../batik`, and `../vienna4x22`
and the repository's `LICENSING.md`.
