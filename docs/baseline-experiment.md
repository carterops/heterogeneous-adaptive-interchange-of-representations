# v0.1.1 baseline experiment

## Research question

For the same input and context, how do originating humans rate a direct reconstruction
of their intended meaning compared with a reconstruction produced through an explicit
Shared Bridge Representation (SBR)? This is a protocol for collecting evidence. No
comparison result has been measured yet.

## Versioned cases

The experiment uses [`evals/v0.1/cases.json`](../evals/v0.1/cases.json): 16 authored
cases split evenly between hidden-intent cases and literal-is-correct controls. The
controls guard against treating every ambiguous phrase as evidence of deeper intent.
They are design fixtures, not observations from participants and not evidence that the
listed intended meanings generalize.

## Conditions

### A — direct interpretation

The interpreter receives only `input` and `context`. It returns one human-readable
reconstruction of intended meaning. It must not receive or generate SBR fields before
writing that reconstruction.

### B — SBR-assisted interpretation

The interpreter receives the same `input` and `context`. It returns a validated SBR,
then its human-readable reconstruction, disproof condition, and uncertainty. The SBR
must remain visible in the study record even when the reconstruction is shown alone to
the evaluator.

Use the same interpreter family, version, system instructions, decoding settings, and
case order policy in both conditions unless the run documents a deliberate difference.
Do not let one condition see the authored `intended_meaning` or
`expected_failure_classes`. Those are evaluation references, not interpreter inputs.

## Human evaluation protocol

1. Capture the originating person's intended meaning before showing either
   reconstruction whenever possible. Record deviations from this order.
2. Generate direct and SBR-assisted reconstructions from the same input and context.
3. Randomize which reconstruction is presented first for each case.
4. Hide condition labels and SBR-specific framing from the evaluator during scoring.
5. Ask the originating person to score initial semantic fidelity using one anchor:
   1.00 exact, 0.75 mostly correct, 0.50 partial, 0.25 wrong abstraction, or 0.00 wrong object.
6. Record the mismatch explanation, observed failure classes, whether clarification
   was required, and correction depth (`none`, `detail`, `scope`, `abstraction`, or
   `concept`).
7. Record corrections separately from the initial rating. A corrected output does not
   replace the initial score.
8. Store a missing rating as `null`. Never convert it to 0.00.

An evaluation record follows
[`evals/v0.1/result.schema.json`](../evals/v0.1/result.schema.json). Each case-condition
pair may appear once in a result set. The local evaluator also verifies that input,
context, and intended meaning exactly match the versioned case. An SBR-condition
record must retain the complete validated SBR, a matching disproof condition, and an
uncertainty statement; its rated reconstruction must match the reconstruction stored
in that SBR. A direct-condition record must leave SBR-only fields null. Any correction
is stored separately from the initial reconstruction and notes.

The bundled v0.1 cases and intended meanings are researcher-authored fixtures for
rehearsing this protocol. For a study with new originating people, capture each
person's intended meaning first and freeze it into a new versioned case dataset before
generating either condition. Do not overwrite the v0.1 reference meaning inside a
result record.

## Running the evaluator

Validate the case dataset without claiming a measured result:

```sh
python -m hairbridge.eval
```

Validate and summarize one or more actual result files:

```sh
python -m hairbridge.eval results/v0.1.1-run-001.json
```

The summary reports record count; measured and missing RTSF counts; mean and median
RTSF by condition; failure-class counts; clarification rate by condition; and the count
of records labeled `wrong abstraction level`.

RTSF anchors are provisional ordinal categories. The requested means and medians are
descriptive summaries only. Their presence does not establish equal distance between
anchors, statistical significance, causal effect, or scientific validity. Report the
rating distribution and individual records alongside summaries in any study report.

## Bias and validity risks

- The authored intended meaning can privilege the researchers' framing over the
  originating person's meaning.
- An SBR reconstruction may be longer or sound more careful, revealing the condition
  despite label blinding.
- Presentation order, memory, and seeing the first reconstruction can change the
  evaluation of the second.
- The same person supplying intent and scoring fidelity improves direct relevance but
  can introduce recall and demand effects.
- Fixture familiarity can contaminate provider comparisons; use unseen holdout cases
  for any generalization claim.
- Literal controls are essential, because a system that always infers a hidden meaning
  can look insightful while being systematically wrong.
- The current controls use more explicit disambiguating context than several
  hidden-intent cases, and the set is concentrated in software, product, and design.
  Its 8/8 count balance does not establish equal difficulty or representativeness.
- Clarification can improve the final answer while concealing a poor initial
  interpretation; preserve both stages.

## Evidence boundary

Passing software tests establishes schema, validation, fixture, renderer, and summary
behavior. A completed human run may provide evidence about recognition, correction
burden, and observed failure patterns for that sample. Neither establishes that SBR is
generally better, that RTSF is validated, or that the taxonomy is exhaustive.
