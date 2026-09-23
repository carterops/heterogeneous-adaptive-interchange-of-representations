# H-A-I-R

**Heterogeneous Adaptive Interchange of Representations**

H-A-I-R is a research project and reference implementation for a specific problem:
**different AI specialists can each be good at their own job while still losing
important meaning when work moves between them.**

Instead of forcing every specialist into one shared representation, H-A-I-R preserves
the sender's native artifact, creates a representation adapted to the recipient, and
records how the recipient understood it.

> **Core law:** H-A-I-R adapts the communication layer to the participants; it does
> not force the participants to adapt to the communication layer.

## 30-second version

**What is this?**  
A representation-preserving interchange layer for heterogeneous AI specialists and
human↔AI collaboration.

**Why does it matter?**  
As agent systems become more specialized, the human can become the coordination
bottleneck: carrying context, translating between specialists, catching
misunderstandings, routing failures, and repeatedly explaining what changed. H-A-I-R
tests whether that translation burden can move into the system without flattening the
specialists' native reasoning.

**What has actually been built?**  
This repository implements H-A-I-R message envelopes, deterministic message identity,
recipient-specific renderings, acknowledgements, evidence references, and an earlier
human-intent representation experiment. H-A-I-R has also been integrated into a
separate intent-driven specialist runtime used for controlled runtime experiments.

**What evidence exists right now?**  
A public Runtime 3 evidence package contains the synthetic pilot artifacts and a local
verifier. In that pilot, the runtime formed a **20-member capability graph**, recorded
**29 chained events**, required **0 human interruptions or corrections in the
fixture**, completed **2 internal repair loops**, caught **1 synthetic regression
before human review**, discovered **1 emergent requirement**, resolved **1 specialist
disagreement**, and recorded **2 H-A-I-R exchanges with recipient acknowledgements**.

Those results are evidence of **runtime control-plane behavior**, not proof that 20
independent agents all executed work or that H-A-I-R improves final product quality.
The pilot explicitly records final product intent fidelity and real product quality as
`NOT_RUN`, and release remained unauthorized.

→ [Inspect the Runtime 3 evidence](evidence/runtime-3/README.md)  
→ [Inspect the machine-readable pilot result](evidence/runtime-3/pilot-result.json)  
→ Run `python evidence/runtime-3/verify.py` locally to verify the public evidence package.

## Research direction

H-A-I-R began as the **Human–AI Representation Bridge**. Human↔AI intent translation
remains an application, but it is no longer the definition of the project.

The broader direction is an **adaptive interoperability layer for heterogeneous
representations**: participants keep their native representations while the
communication layer adapts between them.

The larger runtime experiment asks a related systems question:

> **How much coordination, review, repair, and evidence management can an AI
> specialist organization absorb while the human remains responsible for intent,
> hard constraints, and final authority?**

This repository provides the representation contracts for that work. It is not itself
the team orchestrator or autonomous runtime.

The GitHub repository now uses the H-A-I-R project name. The Python distribution
currently retains the historical `human-ai-representation-bridge` identifier for
compatibility until a deliberate package migration is performed.

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

The [Runtime 3 implementation evidence](evidence/runtime-3/README.md) includes
the synthetic pilot's original event chain and result artifact, a local verifier,
component test counts, and unresolved real-project findings. The evidence package is
deliberately scoped: it establishes recorded runtime behavior and artifact integrity,
while product fidelity and real product quality remain `NOT_RUN`.

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
