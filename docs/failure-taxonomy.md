# Provisional failure taxonomy

These labels are working definitions, not validated or mutually exclusive diagnoses.

## Human → AI

| Failure | Meaning |
| --- | --- |
| gestalt loss | Overall composition is reduced to isolated surface details. |
| pragmatic loss | Communicative purpose is lost despite understanding the literal words. |
| compression loss | Meaning packed into shorthand is not recovered. |
| assumption loss | An implicit premise is omitted or silently substituted. |
| social-context loss | Relevant roles or conversational circumstances are ignored. |
| taste loss | A tentative aesthetic preference is lost or overgeneralized. |
| temporal-context loss | Recent revisions or changes in intent are ignored. |

## AI → Human

| Failure | Meaning |
| --- | --- |
| abstraction overload | The response uses more abstraction than the recipient can use. |
| structure burial | The relationships that matter are hidden in detail. |
| confidence opacity | Uncertainty and evidence strength are unclear. |
| causal opacity | The explanation omits why a conclusion follows. |
| representation mismatch | The form of the explanation does not fit the recipient's task. |
| relevance mismatch | Correct information does not address the current objective. |

## Cross-cutting labels used by the fixtures

- **wrong abstraction level**: reasoning about surface details when the intended issue may be structure, or the reverse.
- **over-preservation**: retaining a structure the user may expect to replace.
- **over-interpretation**: inventing hidden meaning when the literal request is supported by context.
- **scope expansion**: broadening a bounded request beyond the change the user asked for.

Labels describe candidate failures, not properties of a person. The fixture tests
verify authored classifications are preserved; they do not validate a classifier.
