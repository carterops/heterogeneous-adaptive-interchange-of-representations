import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from hairbridge import SharedBridgeRepresentation
from hairbridge.eval import (
    RESULT_FIELDS,
    load_eval_cases,
    load_results,
    summarize_results,
    validate_case,
    validate_result,
)


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_eval_cases()
        cls.case = cls.cases[0]

    def result(self, **changes):
        value = {
            "case_id": self.case["case_id"],
            "condition": "direct",
            "input": self.case["input"],
            "context": self.case["context"],
            "intended_meaning": self.case["intended_meaning"],
            "reconstruction": "A reconstruction to be rated.",
            "rtsf": 0.75,
            "failure_classes": [],
            "clarification_required": False,
            "correction_depth": "none",
            "correction": None,
            "sbr": None,
            "disproof_condition": None,
            "uncertainty": None,
            "notes": "",
        }
        value.update(changes)
        return value

    def sbr_result(self, **changes):
        bridge = SharedBridgeRepresentation(
            raw_input=self.case["input"],
            literal_ask="Apply the stated change.",
            inferred_intent=self.case["intended_meaning"],
            vision="The requested outcome.",
            pragmatic_meaning="Act on the intended meaning.",
            underlying_assumption="The supplied context is relevant.",
            domain="evaluation",
            abstraction_level="intent",
            rework_mode="evaluate",
            taste_hypotheses=(),
            confidence=0.5,
            ambiguity_reasons=("This is an authored test artifact.",),
            missing_information=(),
            wrong_but_literal_outcome="A reconstruction that misses the intended meaning.",
            what_would_prove_this_wrong="The originating person rejects this reading.",
            human_readable_reconstruction="A tentative SBR-assisted reconstruction.",
            failure_classes=("pragmatic loss",),
        )
        value = self.result(
            condition="sbr",
            reconstruction=bridge.human_readable_reconstruction,
            sbr=bridge.to_dict(),
            disproof_condition=bridge.what_would_prove_this_wrong,
            uncertainty="Confidence is uncalibrated and the interpretation remains tentative.",
        )
        value.update(changes)
        return value

    def test_dataset_is_balanced_and_versioned(self):
        self.assertEqual(len(self.cases), 16)
        counts = {
            kind: sum(case["case_type"] == kind for case in self.cases)
            for kind in ("hidden_intent", "literal_control")
        }
        self.assertEqual(counts, {"hidden_intent": 8, "literal_control": 8})
        self.assertEqual(len({case["case_id"] for case in self.cases}), 16)

    def test_published_result_schema_matches_runtime_contract(self):
        schema = json.loads(
            Path("evals/v0.1/result.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(schema["required"]), RESULT_FIELDS)
        self.assertEqual(set(schema["properties"]), RESULT_FIELDS)
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            set(schema["properties"]["rtsf"]["enum"]),
            {None, 0, 0.25, 0.5, 0.75, 1},
        )

    def test_case_schema_is_exact(self):
        with self.assertRaises(ValueError):
            validate_case(dict(self.case, extra=True))
        incomplete = dict(self.case)
        del incomplete["context"]
        with self.assertRaises(ValueError):
            validate_case(incomplete)

    def test_result_accepts_missing_rtsf(self):
        self.assertIsNone(validate_result(self.result(rtsf=None))["rtsf"])

    def test_result_rejects_non_anchor_or_invalid_rtsf(self):
        for value in (0.6, -0.25, 1.25, True, "0.75", float("nan")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_result(self.result(rtsf=value))

    def test_result_schema_and_enums_are_strict(self):
        invalid = [
            {"condition": "bridge"},
            {"correction_depth": "large"},
            {"clarification_required": 1},
            {"failure_classes": "none"},
            {"correction_depth": "detail", "correction": None},
            {"correction_depth": "none", "correction": "A correction"},
        ]
        for change in invalid:
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_result(self.result(**change))
        with self.assertRaises(ValueError):
            validate_result(dict(self.result(), unexpected=True))

    def test_condition_artifacts_are_preserved_and_separated(self):
        self.assertEqual(validate_result(self.result())["condition"], "direct")
        for change in (
            {"sbr": {}},
            {"disproof_condition": "Not applicable"},
            {"uncertainty": "Not applicable"},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_result(self.result(**change))

        valid = validate_result(self.sbr_result())
        self.assertIsInstance(valid["sbr"], dict)
        self.assertIsNotNone(valid["disproof_condition"])
        self.assertIsNotNone(valid["uncertainty"])
        for change in (
            {"sbr": None},
            {"disproof_condition": "A different disproof condition."},
            {"uncertainty": None},
            {"sbr": dict(valid["sbr"], raw_input="Different input")},
            {"reconstruction": "A different reconstruction."},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_result(self.sbr_result(**change))

    def test_result_must_match_versioned_case(self):
        case_map = {self.case["case_id"]: self.case}
        for change in (
            {"case_id": "unknown"},
            {"input": "Changed input"},
            {"context": "Changed context"},
            {"intended_meaning": "Changed intended meaning"},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_result(self.result(**change), cases_by_id=case_map)

    def test_duplicate_case_condition_is_rejected(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            path.write_text(json.dumps([self.result(), self.result()]), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_results([path], cases=self.cases)

    def test_summary_keeps_missing_separate(self):
        rows = [
            self.result(rtsf=0.75, clarification_required=False),
            self.result(case_id=self.cases[1]["case_id"], condition="direct",
                        input=self.cases[1]["input"], context=self.cases[1]["context"],
                        intended_meaning=self.cases[1]["intended_meaning"], rtsf=None,
                        clarification_required=True,
                        failure_classes=["wrong abstraction level"]),
            self.sbr_result(rtsf=1.0),
        ]
        summary = summarize_results(rows)
        direct = summary["by_condition"]["direct"]
        self.assertEqual(direct["count"], 2)
        self.assertEqual(direct["measured_rtsf_count"], 1)
        self.assertEqual(direct["missing_rtsf_count"], 1)
        self.assertEqual(direct["mean_rtsf"], 0.75)
        self.assertEqual(direct["median_rtsf"], 0.75)
        self.assertEqual(direct["clarification_rate"], 0.5)
        self.assertEqual(summary["wrong_abstraction_count"], 1)

    def test_empty_condition_reports_null_summaries(self):
        summary = summarize_results([self.result()])
        sbr = summary["by_condition"]["sbr"]
        self.assertEqual(sbr["count"], 0)
        self.assertIsNone(sbr["mean_rtsf"])
        self.assertIsNone(sbr["median_rtsf"])
        self.assertIsNone(sbr["clarification_rate"])


if __name__ == "__main__":
    unittest.main()
