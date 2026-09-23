# Astra Runtime 3 implementation evidence

This is a public, scoped record of the 2026-09-22 intent-driven specialist runtime
migration. The source Factory checkpoint is
`4cc7fab628f6f75b2bb94612aed6be51db734761` (`feat: activate intent-driven
specialist runtime v3`). The two machine-readable pilot artifacts in this directory
are byte-for-byte copies of that checkpoint's synthetic P&L pilot outputs. Run
`python evidence/runtime-3/verify.py` from the repository root to check their file
hashes, event chain, and reported control-plane counts.

| Source artifact | SHA-256 |
| --- | --- |
| `runtime-events.jsonl` | `ca59f0cb7975b4eef833c02b681e55840b6058b85a8e5901b4d5bca2333b8f7f` |
| `pilot-result.json` | `9bf1bd0b585df89404166a4a0fc86921f2a50002d3b4a405ae86e084dd2ff63d` |
| Private source `PILOT_REPORT.md` | `f2a0563fcddb255e7b07582ae88fc9023619327295120aacc2af5f58cd7e0df6` |
| Private source `INSTALLATION_AND_VALIDATION.md` | `97942af842c1c73a3833f7630746755e54ad74cf4b8728b84a64a9073eae5ea3` |

The two source reports remain in the Factory evidence package. They include local
installation and project context, so this public record quotes their measured
results rather than copying them wholesale. The copied JSONL and JSON contain
synthetic fixture data; no production records or credentials were used.

## Implementation checks

| Check | Recorded result |
| --- | ---: |
| Astra Harness | 65/65 tests passed |
| Code Builder Creation/Promotion authority | 8/8 passed |
| Evidence engine | 73/73 passed |
| Delivery workflow | 32/32 passed |
| Architecture contracts | 11/11 passed |
| Product Art Director | 12/12 passed |
| Visual Scout | 6/6 passed |
| Total component tests | 207/207 passed |
| Root architecture gate | 7/7 required checks passed; `ARCHITECTURE_VERIFIED` |
| Active installation comparison | 216 domain files and 25 runtime registry files `MATCH` |
| Active pipeline doctor | `READY` |

These are implementation and installation checks in the Factory environment. The
architecture gate recorded the then-current changed working tree before the final
checkpoint commit; its result should not be read as a separate test of every byte in
the final commit. The active installation comparison was recorded after activation.

## Synthetic short-intent pilot

The P&L fixture formed a 20-member capability graph. Selection is a routing result,
not proof that 20 agents independently executed work. Its 29 events form a valid
SHA-256 chain with head
`9790e07c3e4bdc0ea8bd4472b94e0ce888455b81be07acc627bff184cc8d442a`.

| Event-chain measurement | Result |
| --- | ---: |
| Human interruptions and corrections in the fixture | 0 and 0 |
| Internal repair loops | 2 |
| Synthetic regression caught before human review | 1 |
| Emergent requirement and resolved disagreement | 1 and 1 |
| H-A-I-R native messages, recipient renderings, acknowledgements | 2, 2, 2 |
| Messages pending acknowledgement | 0 |
| Applicable synthetic runtime checkpoints with evidence | 4/4 |
| Final product intent fidelity | `NOT_RUN` |
| Real product quality | `NOT_RUN` |
| Release authorized | `false` |

The messages preserve native payloads, recipient renderings, evidence pointers,
Intent Contract references, and recipient acknowledgements. The pilot's
`promotion.eligible: true` applies to the synthetic control-plane candidate only;
`releaseAuthorized` remains `false`. The 4/4 figure covers only tested runtime
checkpoints, not application evidence completeness.

A separate read-only test of the unchanged P&L application returned **1 PASS and 2
FAIL**. Its expected preparation path and grade-ledger callback were absent. Those
real-project findings are distinct from the one injected regression in the synthetic
event chain. Runtime 3 did not repair that application or touch production data.

## What this evidence establishes

It shows that the runtime formed a specialist graph, recorded representation-preserving
H-A-I-R exchanges, contained and repaired fixture failures, replayed a regression,
and kept release authority outside the bridge. The event hashes establish integrity
of the included record, not the truth of external observations. There was no real
rendered P&L candidate or human fidelity study, so this package cannot establish
product quality, semantic improvement, lower usage, or AGI benchmark performance.
