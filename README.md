# human-ai-representation-bridge

**HAIR Bridge — Human–AI Representation Bridge**

An experimental human–AI interface research project. v0.1.1 asks one question:
**Can an explicit intermediate representation make hidden interpretation assumptions
visible and testable?**

## Problem and hypothesis

Human–AI collaboration can fail when meaning is lost between different forms of
representation, even when both sides are capable. A compressed request may carry
context, intuition, or a structural expectation that a literal reading misses.

**Hypothesis:** exposing interpretation assumptions in a Shared Bridge Representation
(SBR) may help people identify and correct that loss. This repository claims neither
novelty nor validated improvement.

## Architecture

- **H — human-native representation:** intuition, gestalt, taste, lived context,
  implicit assumptions, and compressed natural language.
- **A — AI-native representation:** explicit relationships, constraints, hypotheses,
  decomposed concepts, confidence, and formal representations.
- **B — Shared Bridge Representation:** an inspectable intermediate artifact.

```text
Human → Bridge → AI
Human ← Bridge ← AI

v0.1.1: input + context → direct or SBR condition → human fidelity rating
```

The conceptual model is bidirectional. The implementation provides a provider
interface for human-to-AI interpretation and a deterministic SBR-to-human renderer.
It does not parse arbitrary AI output. Neither side needs to imitate the other.

## Example failure

“Make mine look like this,” accompanied by a structurally different UI reference,
could mean copying colors and typography. It could also mean adopting layout,
hierarchy, density, interaction model, and composition. Copying only styling can
produce a technically completed but semantically wrong result.

The bridge records the structural interpretation as a **hypothesis**, asks which
qualities matter, and records a disproof condition: the user may want surface changes
only. The demo represents screenshot context as text; it does not inspect an image.

## Shared Bridge Representation

The immutable, runtime-validated `SharedBridgeRepresentation` includes:

| Purpose | Fields |
| --- | --- |
| Preserve input and interpretation | `raw_input`, `literal_ask`, `inferred_intent` |
| Expose purpose and premises | `vision`, `pragmatic_meaning`, `underlying_assumption` |
| Locate the interpretation | `domain`, `abstraction_level`, `rework_mode` |
| Make uncertainty visible | `taste_hypotheses`, `confidence`, `ambiguity_reasons`, `missing_information` |
| Enable challenge and correction | `wrong_but_literal_outcome`, `what_would_prove_this_wrong`, `human_readable_reconstruction` |
| Record provisional classifications | `failure_classes` |

All fields are required. Text must be nonempty; sequence fields can be empty except
`failure_classes`. Confidence must be finite and within [0, 1]. Fixture confidence
values are illustrative and uncalibrated. Labels are extensible strings; their working
definitions are in the [failure taxonomy](docs/failure-taxonomy.md).

## How to run

Requires Python 3.10 or newer. Run from the repository root:

```sh
python -m venv .venv
```

Activate on macOS/Linux with `source .venv/bin/activate`, or on Windows PowerShell
with `.venv\Scripts\Activate.ps1`. Then:

```sh
python -m pip install -e .
python -m hairbridge
python -m hairbridge.eval
python examples/round_trip.py
python -m unittest discover -s tests -v
```

There are no third-party runtime dependencies, API keys, or model calls. Installation
uses setuptools as its build dependency and may download it.

```python
from hairbridge import human_to_ai_translate, ai_to_human_translate

bridge = human_to_ai_translate(
    "That's slow.",
    context="The user comments on an ongoing approach; no timing measurements are supplied.",
)
print(ai_to_human_translate(bridge))
```

The default `FixtureTranslator` matches exact input **and context**. Unknown pairs
raise `ValueError`. A future provider can implement `Translator.interpret(raw_input,
*, context)` and return a validated SBR, passed using the `translator=` argument.
General semantic interpretation would require an additional provider, such as an
LLM-backed implementation; none is included in v0.1.1. Interpretation never executes actions.

## Tests and examples

The four translator fixtures cover reference imitation, “That's slow,” “It's still the
same,” and “What am I missing?” Tests check schema, required fields, confidence
bounds, translation contracts, context mismatch, and fixture classifications.
They are deterministic software checks, not semantic evaluation results.

The separate [v0.1 evaluation dataset](evals/v0.1/cases.json) contains 16 cases:
eight hidden-intent cases and eight literal-is-correct controls. The controls test the
failure mode in which an interpreter invents deeper meaning even when the literal ask
is correct. The [baseline experiment](docs/baseline-experiment.md) compares direct and
SBR-assisted reconstructions on the same cases. Run `python -m hairbridge.eval` to
validate the dataset; pass measured result files to calculate descriptive summaries.

## RTSF

**Round-Trip Semantic Fidelity (RTSF)** is an experimental human rating of whether
the reconstructed meaning matches the originating person's intent. Proposed anchors:
1.00 exact; 0.75 mostly correct; 0.50 partial; 0.25 wrong abstraction; 0.00 wrong object.
It is not scientifically validated, and v0.1.1 has **no measured RTSF results**.
See the [baseline protocol](docs/baseline-experiment.md) and the original
[metric discussion](docs/experiment.md).

## Limitations

The implementation demonstrates inspectable authored assumptions, not automatic
understanding or reduced semantic loss. Reconstructions and classifications are
handwritten; schema validity cannot establish truth. More structure may increase
effort, and plausible interpretations may bias a person's response. There is no
personality clone, consciousness claim, agent framework, or heavy infrastructure.

## Roadmap

- v0.1: explicit schema, four fixture cases, readable reconstruction, and contract tests.
- v0.1.1: balanced evaluation cases, direct-versus-SBR protocol, result schema,
  local evaluator, and continuous integration. This is a scaffold, not a measured result.
- Future research, outside this implementation: run the protocol with originating
  humans and unseen holdout inputs, then consider a semantic provider only when the
  evidence justifies it.

## Research questions

- Which exposed assumptions help people detect an incorrect interpretation?
- When does structured representation increase burden or introduce meaning?
- Can a reconstruction preserve ambiguity without becoming unhelpful?
- How sensitive are RTSF ratings to wording, context, and evaluator disagreement?

## Contributing

Contribute minimal anonymized input/context pairs, competing interpretations,
disproof conditions, and regression tests. Separate hypotheses from observations
and measured results. Avoid private conversation history and credentials. Explain
how a proposal helps answer the v0.1.1 research question before adding dependencies or scope.

Licensed under the [Apache License 2.0](LICENSE).
