import json
import unittest
from dataclasses import FrozenInstanceError, replace

from hairbridge import SharedBridgeRepresentation, ai_to_human_translate, human_to_ai_translate
from hairbridge.translation import load_cases


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.cases = load_cases()
        self.data = self.cases[0]["bridge"]
        self.bridge = SharedBridgeRepresentation.from_dict(self.data)

    def test_json_round_trip(self):
        self.assertEqual(self.bridge, SharedBridgeRepresentation.from_dict(
            json.loads(json.dumps(self.bridge.to_dict()))))

    def test_every_field_required(self):
        for key in self.data:
            with self.subTest(key=key), self.assertRaises(ValueError):
                SharedBridgeRepresentation.from_dict({k: v for k, v in self.data.items() if k != key})

    def test_unknown_fields_rejected(self):
        with self.assertRaises(ValueError):
            SharedBridgeRepresentation.from_dict(dict(self.data, unexpected=True))

    def test_invalid_confidence(self):
        for value in (-.01, 1.01, float('nan'), float('inf'), True, '0.5', None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                replace(self.bridge, confidence=value)

    def test_confidence_endpoints(self):
        for value in (0, 1):
            self.assertEqual(replace(self.bridge, confidence=value).confidence, value)

    def test_invalid_fields(self):
        for key, value in [('raw_input', ''), ('domain', None), ('literal_ask', '  '),
                           ('taste_hypotheses', 'blue'), ('ambiguity_reasons', [3]),
                           ('failure_classes', [])]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                SharedBridgeRepresentation.from_dict(dict(self.data, **{key: value}))

    def test_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.bridge.confidence = .9

    def test_expected_fixture_classifications(self):
        expected = {
            'reference': ('gestalt loss', 'wrong abstraction level'),
            'slow': ('pragmatic loss',),
            'same': ('over-preservation', 'wrong abstraction level'),
            'missing': ('assumption loss',),
        }
        self.assertEqual(set(expected), {case['id'] for case in self.cases})
        for case in self.cases:
            with self.subTest(case=case['id']):
                bridge = human_to_ai_translate(case['bridge']['raw_input'], context=case['context'])
                self.assertEqual(bridge.failure_classes, expected[case['id']])
                rendered = ai_to_human_translate(bridge)
                for value in (bridge.human_readable_reconstruction, bridge.underlying_assumption,
                              bridge.what_would_prove_this_wrong, 'uncalibrated'):
                    self.assertIn(value, rendered)

    def test_unknown_input_or_context_is_not_silently_classified(self):
        for raw, context in [('An unseen request', ''), (self.bridge.raw_input, 'Only change colors.')]:
            with self.assertRaises(ValueError):
                human_to_ai_translate(raw, context=context)

    def test_invalid_inputs(self):
        for raw, context in [('', ''), (None, ''), ('hello', None)]:
            with self.assertRaises(ValueError):
                human_to_ai_translate(raw, context=context)

    def test_custom_provider(self):
        expected = replace(self.bridge, raw_input='A new request')
        calls = []

        class MockTranslator:
            def interpret(self, raw_input, *, context):
                calls.append((raw_input, context))
                return expected

        result = human_to_ai_translate('A new request', context='New context', translator=MockTranslator())
        self.assertEqual(result, expected)
        self.assertEqual(calls, [('A new request', 'New context')])

    def test_bad_provider_contracts(self):
        for result, error in [(self.bridge.to_dict(), TypeError), (self.bridge, ValueError)]:
            class BadTranslator:
                def interpret(self, raw_input, *, context):
                    return result
            with self.assertRaises(error):
                human_to_ai_translate('Different input', context='', translator=BadTranslator())

    def test_renderer_requires_schema(self):
        with self.assertRaises(TypeError):
            ai_to_human_translate(self.data)


if __name__ == '__main__':
    unittest.main()
