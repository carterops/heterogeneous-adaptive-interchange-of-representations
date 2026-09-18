# v0.1 experiment and Round-Trip Semantic Fidelity

## Hypothesis

An explicit intermediate representation can make hidden interpretation assumptions
visible and testable. Whether it reduces semantic loss is a separate empirical question.

## Implemented demonstration

Four authored input/context pairs map to authored SBRs. A renderer exposes each
hypothesis, assumption, ambiguity, missing information, and falsification condition.
Tests check schema and contract behavior, including refusing unknown fixture inputs.
No model, screenshot analysis, user study, or automatic semantic scoring is included.

## Experimental metric: RTSF

Round-Trip Semantic Fidelity asks: after an idea is represented for AI and rendered
back to human-readable form, does the originating human recognize the intended meaning?

| Provisional score | Anchor |
| --- | --- |
| 1.00 | exact |
| 0.75 | mostly correct |
| 0.50 | partial |
| 0.25 | wrong abstraction |
| 0.00 | wrong object |

These are proposed ordinal anchors, not calibrated distances. Do not assume the
difference between every pair of adjacent scores is equivalent. Missing ratings
are unmeasured, not zero. Translator confidence is separate from RTSF.

## Proposed human evaluation (not run)

1. Have participants record intended meaning and success criteria before translation.
2. Preserve raw input, context, provider/version, and the complete bridge artifact.
3. Compare a direct reconstruction with a bridge reconstruction using randomized order.
4. Ask the originating participant to rate each reconstruction, explain mismatches,
   and correct the interpretation. Keep initial ratings distinct from post-correction ratings.
5. Report sample size, individual rating distributions, failure labels, missing ratings,
   time burden, and uncertainty. Include negative and ambiguous cases.

Use unseen inputs and alternate meanings of the same phrase. For example, “That's
slow” may really refer to measured latency. Evaluate whether the bridge surfaces
that alternative instead of imposing a workflow critique.

## Result and falsification boundary

The software demonstrates that authored assumptions can be stored, exposed, and
checked mechanically. It supplies no measured human RTSF result. Fixture test
success does not show that interpretations are correct or semantic loss is reduced.

Evidence against usefulness would include people consistently rejecting reconstructed
intent, greater error or effort than a direct baseline, or assumptions remaining hard
to notice and correct. Human recognition can itself be affected by suggestion, recall,
and evaluator disagreement. An agreeable paraphrase is not proof of faithful meaning.
