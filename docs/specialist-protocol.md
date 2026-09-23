# Specialist message protocol, schema version 1

H-A-I-R conveys a specialist's native representation and a rendering prepared for
one recipient. The recipient must record its interpretation. This is a communication
contract; the owning runtime decides which specialists may act, which evidence is
valid, and whether a candidate may be promoted.

## Envelope

| Field | Meaning |
| --- | --- |
| `schemaVersion` | `1` for this wire shape |
| `messageId` | `hair-` plus the first 16 hex characters of the canonical body hash |
| `sender`, `recipient` | Distinct specialist identifiers |
| `nativeMessage` | Nonempty JSON object in the sender's own representation |
| `recipientRendering` | Nonempty JSON object written for the named recipient |
| `evidenceRefs` | Sorted unique nonempty strings; pointers, not verified evidence |
| `authorityBindingRef` | Optional nonempty reference to an external Intent Contract |
| `acknowledgement` | Status, recipient interpretation, and differences |
| `authorityGranted` | Always `false` |

The body used for `messageId` contains `sender`, `recipient`, `nativeMessage`,
`recipientRendering`, `evidenceRefs`, and `authorityBindingRef`. Hash it as UTF-8
JSON with sorted keys, compact separators, and non-ASCII characters preserved. The
acknowledgement is excluded from identity, so it can change from `PENDING` without
changing the underlying message. Changing either representation or authority
reference invalidates the identity.

Allowed acknowledgement statuses are `PENDING`, `UNDERSTOOD`, `MISUNDERSTOOD`, and
`NEEDS_CLARIFICATION`. Only the addressed recipient can resolve a pending message
through the public API. A resolved acknowledgement requires a non-null
`recipientInterpretation`; `differences` may explain a mismatch or question. The
returned message is a copy, leaving the original pending record intact.

## Boundary of this package

Schema validation checks structure, hash identity, and the fixed `false` authority
flag. It does not verify the sender's identity, evidence references, Intent Contract,
recipient understanding, or whether the rendering faithfully represents the native
artifact. A host must make those checks with its own authenticated actors, evidence
store, and promotion rules. It should retain both pending and resolved records in its
event history.

The earlier [Shared Bridge Representation](../README.md#human-intent-research)
serves a different job: exposing assumptions in a human request. A specialist
message may contain an SBR as a native artifact, but does not require one.
