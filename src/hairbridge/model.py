"""Small runtime-validated SBR schema, with no third-party runtime dependencies."""

from dataclasses import asdict, dataclass, fields
import math


@dataclass(frozen=True)
class SharedBridgeRepresentation:
    raw_input: str
    literal_ask: str
    inferred_intent: str
    vision: str
    pragmatic_meaning: str
    underlying_assumption: str
    domain: str
    abstraction_level: str
    rework_mode: str
    taste_hypotheses: tuple[str, ...]
    confidence: float
    ambiguity_reasons: tuple[str, ...]
    missing_information: tuple[str, ...]
    wrong_but_literal_outcome: str
    what_would_prove_this_wrong: str
    human_readable_reconstruction: str
    failure_classes: tuple[str, ...]

    def __post_init__(self) -> None:
        sequence_fields = {
            "taste_hypotheses", "ambiguity_reasons", "missing_information", "failure_classes"
        }
        for field in fields(self):
            value = getattr(self, field.name)
            if field.name == "confidence":
                if (isinstance(value, bool) or not isinstance(value, (int, float))
                        or not math.isfinite(value) or not 0 <= value <= 1):
                    raise ValueError("confidence must be a finite number between 0 and 1")
            elif field.name in sequence_fields:
                if not isinstance(value, tuple) or any(
                    not isinstance(item, str) or not item.strip() for item in value
                ):
                    raise ValueError(f"{field.name} must be a tuple of nonempty strings")
                if field.name == "failure_classes" and not value:
                    raise ValueError("failure_classes must not be empty")
            elif not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field.name} must be a nonempty string")

    def to_dict(self) -> dict:
        """Return a JSON-compatible copy; no references to mutable model state."""
        return {key: list(value) if isinstance(value, tuple) else value
                for key, value in asdict(self).items()}

    @classmethod
    def from_dict(cls, data: dict) -> "SharedBridgeRepresentation":
        """Reject missing/unknown fields and validate JSON sequence values."""
        expected = {field.name for field in fields(cls)}
        if set(data) != expected:
            raise ValueError(f"schema mismatch: missing={sorted(expected - set(data))}, "
                             f"unknown={sorted(set(data) - expected)}")
        converted = dict(data)
        for key in ("taste_hypotheses", "ambiguity_reasons", "missing_information", "failure_classes"):
            if not isinstance(converted[key], (list, tuple)):
                raise ValueError(f"{key} must be a list or tuple")
            converted[key] = tuple(converted[key])
        return cls(**converted)
