"""Portable H-A-I-R message envelope for specialist-to-specialist exchange.

This module validates representation and acknowledgement. It does not execute a
specialist, verify an evidence reference, or grant authority to act.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Sequence


ACKNOWLEDGEMENT_STATES = {
    "PENDING", "UNDERSTOOD", "MISUNDERSTOOD", "NEEDS_CLARIFICATION"
}


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def create_hair_message(
    sender: str,
    recipient: str,
    native_message: dict[str, Any],
    recipient_rendering: dict[str, Any],
    evidence_refs: Sequence[str] | None = None,
    authority_binding_ref: str | None = None,
) -> dict[str, Any]:
    """Preserve both representations in a deterministic, non-authoritative envelope."""
    body = {
        "sender": sender,
        "recipient": recipient,
        "nativeMessage": copy.deepcopy(native_message),
        "recipientRendering": copy.deepcopy(recipient_rendering),
        "evidenceRefs": sorted(set(evidence_refs or [])),
        "authorityBindingRef": authority_binding_ref,
    }
    message = {
        "schemaVersion": 1,
        "messageId": "hair-" + _digest(body)[:16],
        **body,
        "acknowledgement": {
            "status": "PENDING", "recipientInterpretation": None, "differences": []
        },
        "authorityGranted": False,
    }
    validate_hair_message(message)
    return message


def validate_hair_message(message: dict[str, Any]) -> None:
    """Check wire shape and identity; evidence and authority still need their owners."""
    if not isinstance(message, dict):
        raise ValueError("H-A-I-R message must be an object")
    required = {
        "schemaVersion", "messageId", "sender", "recipient", "nativeMessage",
        "recipientRendering", "acknowledgement", "evidenceRefs",
        "authorityBindingRef", "authorityGranted",
    }
    if set(message) != required:
        raise ValueError("H-A-I-R message fields do not match schema version 1")
    if message["schemaVersion"] != 1 or message["authorityGranted"] is not False:
        raise ValueError("H-A-I-R cannot create authority")
    for key in ("sender", "recipient"):
        if not isinstance(message[key], str) or not message[key].strip():
            raise ValueError(f"invalid H-A-I-R {key}")
    if message["sender"] == message["recipient"]:
        raise ValueError("H-A-I-R sender and recipient must differ")
    for key in ("nativeMessage", "recipientRendering"):
        if not isinstance(message[key], dict) or not message[key]:
            raise ValueError(f"{key} must be a non-empty object")
    refs = message["evidenceRefs"]
    if (not isinstance(refs, list)
            or not all(isinstance(item, str) and item.strip() for item in refs)
            or refs != sorted(set(refs))):
        raise ValueError("evidence references must be sorted unique non-empty strings")
    authority_ref = message["authorityBindingRef"]
    if authority_ref is not None and (
        not isinstance(authority_ref, str) or not authority_ref.strip()
    ):
        raise ValueError("invalid authority binding reference")
    ack = message["acknowledgement"]
    if not isinstance(ack, dict) or set(ack) != {
        "status", "recipientInterpretation", "differences"
    } or ack["status"] not in ACKNOWLEDGEMENT_STATES:
        raise ValueError("invalid H-A-I-R acknowledgement")
    if (not isinstance(ack["differences"], list)
            or not all(isinstance(item, str) for item in ack["differences"])):
        raise ValueError("invalid H-A-I-R acknowledgement differences")
    if ack["status"] != "PENDING" and ack["recipientInterpretation"] is None:
        raise ValueError("acknowledgement requires the recipient interpretation")
    identity = {
        "sender": message["sender"],
        "recipient": message["recipient"],
        "nativeMessage": message["nativeMessage"],
        "recipientRendering": message["recipientRendering"],
        "evidenceRefs": refs,
        "authorityBindingRef": authority_ref,
    }
    if message["messageId"] != "hair-" + _digest(identity)[:16]:
        raise ValueError("H-A-I-R message identity mismatch")


def acknowledge_hair_message(
    message: dict[str, Any],
    *,
    actor: str,
    status: str,
    interpretation: Any,
    differences: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Return an acknowledged copy after the addressed recipient responds."""
    validate_hair_message(message)
    if actor != message["recipient"]:
        raise ValueError("only the addressed recipient may acknowledge")
    if message["acknowledgement"]["status"] != "PENDING":
        raise ValueError("message has already been acknowledged")
    if status == "PENDING" or status not in ACKNOWLEDGEMENT_STATES:
        raise ValueError("acknowledgement must resolve the pending state")
    updated = copy.deepcopy(message)
    updated["acknowledgement"] = {
        "status": status,
        "recipientInterpretation": copy.deepcopy(interpretation),
        "differences": list(differences or []),
    }
    validate_hair_message(updated)
    return updated
