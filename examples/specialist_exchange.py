"""Synthetic specialist exchange with no model, network, or project data."""

from hairbridge import acknowledge_hair_message, create_hair_message


message = create_hair_message(
    sender="data-specialist",
    recipient="frontend-specialist",
    native_message={"kind": "field-contract", "fields": ["crew_id", "period"]},
    recipient_rendering={"summary": "Show one report per crew and period."},
    evidence_refs=["sha256:synthetic-contract"],
    authority_binding_ref="intent:synthetic-project",
)
acknowledged = acknowledge_hair_message(
    message,
    actor="frontend-specialist",
    status="NEEDS_CLARIFICATION",
    interpretation={"question": "Which period format should the UI display?"},
)

print(message["messageId"])
print(acknowledged["acknowledgement"])
print("Authority granted:", acknowledged["authorityGranted"])
