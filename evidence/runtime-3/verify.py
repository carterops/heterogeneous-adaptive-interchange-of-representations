"""Verify the published Runtime 3 synthetic pilot artifacts without Factory code."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

from hairbridge import validate_hair_message


ROOT = Path(__file__).resolve().parent
FILE_HASHES = {
    "runtime-events.jsonl": "ca59f0cb7975b4eef833c02b681e55840b6058b85a8e5901b4d5bca2333b8f7f",
    "pilot-result.json": "9bf1bd0b585df89404166a4a0fc86921f2a50002d3b4a405ae86e084dd2ff63d",
}
HEAD = "9790e07c3e4bdc0ea8bd4472b94e0ce888455b81be07acc627bff184cc8d442a"


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def canonical_hash(value: object) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def verify() -> dict[str, object]:
    for name, expected in FILE_HASHES.items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        require(actual == expected, f"source artifact hash mismatch: {name}")

    events = [json.loads(line) for line in
              (ROOT / "runtime-events.jsonl").read_text(encoding="utf-8").splitlines()
              if line.strip()]
    require(len(events) == 29, "unexpected event count")
    previous = "0" * 64
    for sequence, event in enumerate(events, start=1):
        require(event.get("sequence") == sequence, f"sequence mismatch: {sequence}")
        require(event.get("previousHash") == previous,
                f"predecessor mismatch: {sequence}")
        claimed = event.get("eventHash")
        require(claimed == canonical_hash({key: value for key, value in event.items()
                                           if key != "eventHash"}),
                f"event hash mismatch: {sequence}")
        previous = claimed
    require(previous == HEAD, "unexpected event chain head")

    result = json.loads((ROOT / "pilot-result.json").read_text(encoding="utf-8"))
    metrics = result["metrics"]
    counts = Counter(event["eventType"] for event in events)
    require(result["scenario"] == "SYNTHETIC_CONTROL_PLANE_PILOT",
            "pilot scope mismatch")
    require(len(result["team"]["members"]) == 20, "team size mismatch")
    require(metrics["eventCount"] == len(events), "reported event count mismatch")
    require(result["eventChain"] == {
        "valid": True, "errors": [], "events": len(events), "head": HEAD,
    }, "reported event chain mismatch")
    messages = result["state"]["hairMessages"]
    require(len(messages) == 2, "specialist message count mismatch")
    for message_id, message in messages.items():
        validate_hair_message(message)
        require(message_id == message["messageId"], "specialist message key mismatch")
        require(message["acknowledgement"]["status"] != "PENDING",
                "specialist message still pending")
    for event_type, metric in {
        "REPAIR_LOOP_OPENED": "internalRepairLoops",
        "EMERGENT_REQUIREMENT_DISCOVERED": "emergentRequirementsDiscovered",
        "DISAGREEMENT_RESOLVED": "specialistDisagreementsResolvedInternally",
        "HAIR_NATIVE_MESSAGE_RECORDED": "hairMessagesCreated",
        "HAIR_RECIPIENT_RENDERING_RECORDED": "hairRecipientRenderingsRecorded",
        "HAIR_ACKNOWLEDGEMENT_RECORDED": "hairAcknowledgementsRecorded",
    }.items():
        require(counts[event_type] == metrics[metric], f"metric mismatch: {metric}")
    completeness = metrics["evidenceCompleteness"]
    require(completeness["scope"] == "runtime checkpoints"
            and completeness["passed"] == 4
            and completeness["applicableTested"] == 4,
            "runtime checkpoint evidence mismatch")
    require(metrics["finalIntentFidelity"]["status"] == "NOT_RUN"
            and metrics["productQuality"]["status"] == "NOT_RUN",
            "unsupported product outcome claimed")
    require(result["promotion"]["releaseAuthorized"] is False,
            "release authority mismatch")
    return {"status": "PASS", "events": len(events), "head": previous,
            "specialists_selected": len(result["team"]["members"]),
            "scope": result["scenario"], "product_quality": "NOT_RUN"}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
