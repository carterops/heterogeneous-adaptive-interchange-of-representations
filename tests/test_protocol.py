import copy
import json
import unittest

from hairbridge import (
    acknowledge_hair_message,
    create_hair_message,
    validate_hair_message,
)


class SpecialistMessageTests(unittest.TestCase):
    def setUp(self):
        self.native = {"kind": "data-contract", "fields": ["crew_id", "period"]}
        self.rendering = {"summary": "The crew and period identify one report."}
        self.message = create_hair_message(
            "data-specialist", "frontend-specialist", self.native, self.rendering,
            ["sha256:b", "sha256:a", "sha256:a"], "intent:sha256:123",
        )

    def test_wire_round_trip_and_copies(self):
        self.native["fields"].append("secret")
        self.rendering["summary"] = "changed"
        self.assertEqual(self.message["nativeMessage"]["fields"], ["crew_id", "period"])
        self.assertEqual(self.message["evidenceRefs"], ["sha256:a", "sha256:b"])
        self.assertEqual(self.message["messageId"], "hair-168abd16c58e84dc")
        self.assertFalse(self.message["authorityGranted"])
        validate_hair_message(json.loads(json.dumps(self.message)))

    def test_acknowledgement_requires_recipient_and_preserves_identity(self):
        with self.assertRaisesRegex(ValueError, "addressed recipient"):
            acknowledge_hair_message(self.message, actor="other", status="UNDERSTOOD",
                                     interpretation={"summary": "understood"})
        acknowledged = acknowledge_hair_message(
            self.message, actor="frontend-specialist", status="NEEDS_CLARIFICATION",
            interpretation={"question": "Which period format?"},
            differences=["period format is missing"],
        )
        self.assertEqual(acknowledged["messageId"], self.message["messageId"])
        self.assertEqual(self.message["acknowledgement"]["status"], "PENDING")
        self.assertEqual(acknowledged["acknowledgement"]["status"], "NEEDS_CLARIFICATION")
        with self.assertRaisesRegex(ValueError, "already been acknowledged"):
            acknowledge_hair_message(acknowledged, actor="frontend-specialist",
                                     status="UNDERSTOOD", interpretation="yes")

    def test_identity_and_authority_tampering_rejected(self):
        for change in (
            {"authorityGranted": True},
            {"messageId": "hair-forged"},
            {"authorityBindingRef": "intent:other"},
            {"evidenceRefs": ["sha256:b", "sha256:a"]},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_hair_message(dict(self.message, **change))
        changed = copy.deepcopy(self.message)
        changed["nativeMessage"]["fields"].append("unreviewed")
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            validate_hair_message(changed)
        with self.assertRaises(ValueError):
            validate_hair_message(dict(self.message, evidenceRefs=[["unhashable"]]))

    def test_invalid_acknowledgements_rejected(self):
        for status, interpretation in (("PENDING", "ready"), ("UNVERIFIED", "ready"),
                                       ("UNDERSTOOD", None)):
            with self.subTest(status=status), self.assertRaises(ValueError):
                acknowledge_hair_message(self.message, actor="frontend-specialist",
                                         status=status, interpretation=interpretation)


if __name__ == "__main__":
    unittest.main()
