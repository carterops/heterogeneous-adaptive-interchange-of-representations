"""Translation boundary. The bundled provider retrieves authored fixtures only."""

import json
from importlib.resources import files
from typing import Protocol

from .model import SharedBridgeRepresentation


class Translator(Protocol):
    """A future semantic provider can implement this interface without execution rights."""

    def interpret(self, raw_input: str, *, context: str) -> SharedBridgeRepresentation: ...


def load_cases() -> list[dict]:
    return json.loads(files("hairbridge").joinpath("cases.json").read_text(encoding="utf-8"))


class FixtureTranslator:
    """Exact input AND context lookup, not a language-understanding algorithm."""

    def interpret(self, raw_input: str, *, context: str) -> SharedBridgeRepresentation:
        for case in load_cases():
            if case["bridge"]["raw_input"] == raw_input and case["context"] == context:
                return SharedBridgeRepresentation.from_dict(case["bridge"])
        raise ValueError("No exact fixture matches this input and context; supply a semantic provider.")


def human_to_ai_translate(
    raw_input: str, *, context: str, translator: Translator | None = None
) -> SharedBridgeRepresentation:
    if not isinstance(raw_input, str) or not raw_input.strip():
        raise ValueError("raw_input must be a nonempty string")
    if not isinstance(context, str):
        raise ValueError("context must be a string")
    bridge = (translator if translator is not None else FixtureTranslator()).interpret(
        raw_input, context=context
    )
    if not isinstance(bridge, SharedBridgeRepresentation):
        raise TypeError("translator must return a SharedBridgeRepresentation")
    if bridge.raw_input != raw_input:
        raise ValueError("translator must preserve raw_input")
    return bridge


def ai_to_human_translate(bridge: SharedBridgeRepresentation) -> str:
    """Render an inspectable hypothesis, including uncertainty and a correction route."""
    if not isinstance(bridge, SharedBridgeRepresentation):
        raise TypeError("bridge must be a SharedBridgeRepresentation")
    ambiguity = "; ".join(bridge.ambiguity_reasons) or "None recorded (not proof of certainty)."
    missing = "; ".join(bridge.missing_information) or "None recorded."
    return (
        f"My tentative reading: {bridge.human_readable_reconstruction}\n"
        f"Assumption: {bridge.underlying_assumption}\n"
        f"Confidence (uncalibrated): {bridge.confidence:.2f}\n"
        f"Ambiguity: {ambiguity}\n"
        f"Missing information: {missing}\n"
        f"This reading would be wrong if: {bridge.what_would_prove_this_wrong}\n"
        "Does this capture what you meant? Please correct the interpretation before action."
    )
