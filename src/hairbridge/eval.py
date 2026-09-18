"""Validate and summarize baseline evaluation records using the standard library."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
from statistics import mean, median
from typing import Any, Iterable

from .model import SharedBridgeRepresentation


CONDITIONS = {"direct", "sbr"}
CASE_TYPES = {"hidden_intent", "literal_control"}
CORRECTION_DEPTHS = {"none", "detail", "scope", "abstraction", "concept"}
RTSF_ANCHORS = {0.0, 0.25, 0.5, 0.75, 1.0}

CASE_FIELDS = {
    "case_id", "case_type", "input", "context", "intended_meaning",
    "expected_failure_classes",
}
RESULT_FIELDS = {
    "case_id", "condition", "input", "context", "intended_meaning",
    "reconstruction", "rtsf", "failure_classes", "clarification_required",
    "correction_depth", "correction", "sbr", "disproof_condition",
    "uncertainty", "notes",
}


def _require_exact_fields(record: dict[str, Any], expected: set[str], label: str) -> None:
    if set(record) != expected:
        raise ValueError(
            f"{label} schema mismatch: missing={sorted(expected - set(record))}, "
            f"unknown={sorted(set(record) - expected)}"
        )


def _require_string(record: dict[str, Any], key: str, *, allow_empty: bool = False) -> None:
    value = record[key]
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        qualifier = "a string" if allow_empty else "a nonempty string"
        raise ValueError(f"{key} must be {qualifier}")


def _require_string_list(record: dict[str, Any], key: str) -> None:
    value = record[key]
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ValueError(f"{key} must be a list of nonempty strings")


def _require_nullable_string(record: dict[str, Any], key: str) -> None:
    value = record[key]
    if value is not None and (not isinstance(value, str) or not value.strip()):
        raise ValueError(f"{key} must be null or a nonempty string")


def validate_case(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("case must be an object")
    _require_exact_fields(record, CASE_FIELDS, "case")
    for key in ("case_id", "input", "context", "intended_meaning"):
        _require_string(record, key)
    if record["case_type"] not in CASE_TYPES:
        raise ValueError(f"case_type must be one of {sorted(CASE_TYPES)}")
    _require_string_list(record, "expected_failure_classes")
    return record


def load_eval_cases(path: str | Path = "evals/v0.1/cases.json") -> list[dict[str, Any]]:
    source = Path(path)
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("evaluation dataset must be a nonempty JSON array")
    cases = [validate_case(item) for item in data]
    ids = [case["case_id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("evaluation case_id values must be unique")
    return cases


def validate_result(
    record: dict[str, Any], *, cases_by_id: dict[str, dict[str, Any]] | None = None
) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("result must be an object")
    _require_exact_fields(record, RESULT_FIELDS, "result")
    for key in ("case_id", "input", "context", "intended_meaning", "reconstruction"):
        _require_string(record, key)
    _require_string(record, "notes", allow_empty=True)
    if record["condition"] not in CONDITIONS:
        raise ValueError(f"condition must be one of {sorted(CONDITIONS)}")
    score = record["rtsf"]
    if score is not None:
        if (isinstance(score, bool) or not isinstance(score, (int, float))
                or not math.isfinite(score) or float(score) not in RTSF_ANCHORS):
            raise ValueError(f"rtsf must be null or one of {sorted(RTSF_ANCHORS)}")
    _require_string_list(record, "failure_classes")
    if not isinstance(record["clarification_required"], bool):
        raise ValueError("clarification_required must be a boolean")
    if record["correction_depth"] not in CORRECTION_DEPTHS:
        raise ValueError(f"correction_depth must be one of {sorted(CORRECTION_DEPTHS)}")
    for key in ("correction", "disproof_condition", "uncertainty"):
        _require_nullable_string(record, key)
    if record["correction_depth"] == "none":
        if record["correction"] is not None:
            raise ValueError("correction must be null when correction_depth is none")
    elif record["correction"] is None:
        raise ValueError("correction is required when correction_depth is not none")

    if record["condition"] == "direct":
        if any(record[key] is not None for key in ("sbr", "disproof_condition", "uncertainty")):
            raise ValueError("direct results must not contain SBR condition artifacts")
    else:
        if not isinstance(record["sbr"], dict):
            raise ValueError("sbr results must contain a validated SBR object")
        bridge = SharedBridgeRepresentation.from_dict(record["sbr"])
        if bridge.raw_input != record["input"]:
            raise ValueError("SBR raw_input must match the result input")
        if bridge.human_readable_reconstruction != record["reconstruction"]:
            raise ValueError("result reconstruction must match the SBR reconstruction")
        if record["disproof_condition"] != bridge.what_would_prove_this_wrong:
            raise ValueError("disproof_condition must match the SBR falsification field")
        if record["uncertainty"] is None:
            raise ValueError("sbr results must record uncertainty")

    if cases_by_id is not None:
        case = cases_by_id.get(record["case_id"])
        if case is None:
            raise ValueError(f"unknown case_id: {record['case_id']}")
        for key in ("input", "context", "intended_meaning"):
            if record[key] != case[key]:
                raise ValueError(f"result {key} does not match dataset case {record['case_id']}")
    return record


def load_results(
    paths: Iterable[str | Path], *, cases: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    cases_by_id = {case["case_id"]: case for case in cases}
    results: list[dict[str, Any]] = []
    for path in paths:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"result file must contain a JSON array: {path}")
        results.extend(validate_result(item, cases_by_id=cases_by_id) for item in data)
    keys = [(item["case_id"], item["condition"]) for item in results]
    if len(keys) != len(set(keys)):
        raise ValueError("each case_id and condition pair may appear only once")
    return results


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_condition: dict[str, dict[str, Any]] = {}
    for condition in sorted(CONDITIONS):
        rows = [item for item in results if item["condition"] == condition]
        scores = [float(item["rtsf"]) for item in rows if item["rtsf"] is not None]
        by_condition[condition] = {
            "count": len(rows),
            "measured_rtsf_count": len(scores),
            "missing_rtsf_count": len(rows) - len(scores),
            "mean_rtsf": mean(scores) if scores else None,
            "median_rtsf": median(scores) if scores else None,
            "clarification_rate": (
                sum(item["clarification_required"] for item in rows) / len(rows)
                if rows else None
            ),
        }

    failures = Counter(
        failure for item in results for failure in item["failure_classes"]
    )
    return {
        "record_count": len(results),
        "by_condition": by_condition,
        "failure_class_counts": dict(sorted(failures.items())),
        "wrong_abstraction_count": failures["wrong abstraction level"],
        "notice": (
            "RTSF anchors are provisional ordinal ratings. Means and medians are "
            "descriptive summaries, not evidence that the scale is interval-valued."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "results", nargs="*", help="JSON result file(s); omit to validate the case dataset only"
    )
    parser.add_argument(
        "--cases", default="evals/v0.1/cases.json", help="path to the versioned case dataset"
    )
    args = parser.parse_args(argv)
    try:
        cases = load_eval_cases(args.cases)
        if not args.results:
            counts = Counter(case["case_type"] for case in cases)
            print(json.dumps({
                "dataset": args.cases,
                "case_count": len(cases),
                "case_types": dict(sorted(counts.items())),
                "measured_results": 0,
                "status": "case dataset valid; no result files supplied",
            }, indent=2))
            return 0
        results = load_results(args.results, cases=cases)
        print(json.dumps(summarize_results(results), indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.exit(2, f"evaluation error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
