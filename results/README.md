# Measured results

This directory is reserved for results from actual human evaluations. It intentionally
contains no result data yet.

Store each measured run as a JSON array whose records follow
[`evals/v0.1/result.schema.json`](../evals/v0.1/result.schema.json). Use stable,
non-identifying run names such as `v0.1.1-run-001.json`. Each evaluated case may have
one `direct` record and one `sbr` record. Use `null` for a missing RTSF rating; never
substitute zero.

Direct records set `sbr`, `disproof_condition`, and `uncertainty` to `null`. SBR
records preserve the complete validated SBR plus its disproof condition and a concise
uncertainty statement. Record the evaluator's correction in `correction`; it must be
separate from the initial `reconstruction` and general `notes`. Use `null` only when
`correction_depth` is `none`.

The two conditions must use the same versioned cases and intended meanings. Preserve
the randomized, blinded presentation order outside result records if it is needed for
the study audit trail. Do not commit names, private conversation history, or other
participant identifiers.

Validate and summarize a run from the repository root:

```sh
python -m hairbridge.eval results/v0.1.1-run-001.json
```

Files belong here only after an evaluation has actually occurred. Software-generated
examples, fixtures, and anticipated scores are not measured results.
