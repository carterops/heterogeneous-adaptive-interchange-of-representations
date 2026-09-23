# H-A-I-R

**Heterogeneous Adaptive Interchange of Representations** (H-A-I-R) is a small
Python library for representation-preserving communication between people and AI
specialists that do not naturally reason in the same form. It preserves the sender's
native artifact, adds a recipient-adapted rendering, and records whether the recipient
understood it.

H-A-I-R began as the **Human–AI Representation Bridge**. Human↔AI intent translation
remains the first application, but it is no longer the definition of the project. The
broader research direction is an **adaptive interoperability layer for heterogeneous
representations**: participants keep their native representations while the
communication layer adapts between them instead of forcing everyone into one shared
schema.

The project is moving toward **intent-driven specialist teams**: a person states the
outcome and hard limits once; relevant specialists work in their own representations;
H-A-I-R carries meaning between them; evidence supports verification; the person
decides on release. This repository provides representation contracts for that
direction. It is not a team orchestrator or an autonomous agent runtime.

> **Core law:** H-A-I-R adapts the communication layer to the participants; it does
> not force the participants to adapt to the communication layer.

The repository and Python distribution currently retain the historical
`human-ai-representation-bridge` identifier for continuity; the project name and
research definition are H-A-I-R — Heterogeneous Adaptive Interchange of
Representations.

## What is implemented

| Capability | Status |
| --- | --- |
| Specialist message envelope with native artifact, recipient rendering, evidence references, and acknowledgement | Implemented in v0.2.0 |
| Deterministic message identity and schema validation | Implemented in v0.2.0 |
| Intent Contract reference without authority transfer | Implemented in v0.2.0 |
| Shared Bridge Representation for human-intent hypotheses | Implemented in v0.1.1 and retained |
| 16-case direct-versus-bridge evaluation scaffold | Implemented; no human fidelity results measured |
| Automatic specialist selection, tool execution, evidence verification, and release | Outside this library |

The message format is compatible with the H-A-I-R exchange used by Astra's
intent-driven Factory runtime. Compatibility means the same envelope shape and
identity calculation. The Factory remains responsible for task authority, tool
admission, evidence, promotion, and release decisions.

The [Runtime 3 implementation evidence](evidence/runtime-3/README.md) now includes
the synthetic pilot's original event chain and result artifact, a local verifier,
component test counts, and the unresolved real-project findings. It reports product
fidelity and quality as `NOT_RUN`.

## Specialist exchange

```text
Human objective + hard constraints
            ↓
       Intent Contract
            ↓
Specialists produce native artifacts
            ↓
H-A-I-R: native message → recipient rendering → acknowledgement
            ↓
Candidate evidence and independent review
            ↓
Human release decision
```

A data specialist can send a field contract to a frontend specialist. The original
field contract remains intact; the rendering explains what the frontend needs to
display. The frontend acknowledges its reading or asks for clarification. The
message may point to an Intent Contract and evidence, but those references are not
proof of validity or permission to act.

```python
from hairbridge import create_hair_message, acknowledge_hair_message

message = create_hair_message(
    sender="data-specialist",
    recipient="frontend-specialist",
    native_message={"kind": "field-contract", "fields": ["crew_id", "period"]},
    recipient_rendering={"summary": "Show one report per crew and period."},
    evidence_refs=["sha256:reviewed-contract"],
    authority_binding_ref="intent:project-123",
)

acknowledged = acknowledge_hair_message(
    message,
    actor="frontend-specialist",
    status="NEEDS_CLARIFICATION",
    interpretation={"question": "Which period format should the UI display?"},
)
```

See the [message protocol](docs/specialist-protocol.md) and
[runnable exchange](examples/specialist_exchange.py). The functions only create and
validate data. They do not call models, run tools, contact services, or authorize work.

## Human intent research

The original `SharedBridgeRepresentation` makes a tentative interpretation
inspectable: literal ask, inferred intent, assumptions, uncertainty, and what would
disprove the interpretation. Its bundled `FixtureTranslator` recognizes four exact
input-and-context pairs. Unknown pairs raise `ValueError`; there is no general
semantic interpreter in this repository.

The [baseline protocol](docs/baseline-experiment.md) compares direct and bridge
assisted reconstructions using eight hidden-intent cases and eight literal-is-correct
controls. [Round-Trip Semantic Fidelity](docs/experiment.md) is a proposed human
rating, not a validated metric. No measured improvement is claimed.

## Run locally

Requires Python 3.10 or newer. From the repository root:

```sh
python -m venv .venv
python -m pip install -e .
python examples/specialist_exchange.py
python examples/round_trip.py
python -m hairbridge.eval
python -m unittest discover -s tests -v
```

Activate the environment before installation if needed: `source .venv/bin/activate`
on macOS/Linux or `.venv\Scripts\Activate.ps1` in Windows PowerShell. There are no
third-party runtime dependencies or model API calls. Editable installation uses
setuptools as a build dependency.

## Boundaries and next work

- Native artifacts must remain available beside recipient-specific renderings.
- An acknowledgement records the recipient's interpretation; it does not certify
  that the interpretation is correct.
- `authorityGranted` is always `false`. An Intent Contract reference cannot create
  or expand delegated authority.
- Evidence references are pointers. The owning runtime must validate their source,
  freshness, and relevance before making a claim.
- Missing or failed real-world evidence must stay visible as `NOT_RUN`, `BLOCKED`, or
  `FAIL`; fixture checks are not product validation.

Next work is to measure semantic fidelity with originating humans, test exchanges
across more specialist representations, and evaluate whether explicit acknowledgement
reduces costly misunderstandings. Keep examples synthetic and avoid private project
history in public fixtures.

Licensed under the [Apache License 2.0](LICENSE).
