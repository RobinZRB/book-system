import json
import tempfile
import unittest
from pathlib import Path

from booksys.learning.events import EventStreamError, iter_event_records
from booksys.learning.validation import validate_event, validate_review_payload


class ValidationTests(unittest.TestCase):
    def test_review_payload_rejects_wrong_types_and_ranges(self):
        payload = {
            "question_kind": "recall",
            "target_level": "1",
            "emt_expectations": ["definition"],
            "misconceptions": [],
            "emt_hits": ["definition"],
            "emt_score": 1.1,
            "objective_pass": "true",
            "confidence": -0.1,
            "user_rating": "good",
        }
        errors = validate_review_payload(payload)
        self.assertIn("target_level must be an integer from 1 to 5", errors)
        self.assertIn("emt_score must be a number from 0 to 1", errors)
        self.assertIn("objective_pass must be a boolean", errors)
        self.assertIn("confidence must be a number from 0 to 1", errors)

    def test_event_validation_checks_kind_specific_consistency(self):
        event = {
            "schema_version": 1,
            "event_id": "evt:12345678",
            "kind": "reading",
            "aggregate_id": "chapter:12345678",
            "occurred_at": "2026-01-01T00:00:00+00:00",
            "idempotency_key": "key-1",
            "payload": {"book_id": "book:12345678", "chapter_id": "chapter:87654321"},
        }
        self.assertIn("aggregate_id must equal payload.chapter_id", validate_event(event))

    def test_event_records_preserve_line_numbers(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "events.jsonl"
            path.write_text("\n".join([
                json.dumps({"line": 1}),
                json.dumps({"line": 2}),
                json.dumps({"line": 3}),
            ]) + "\n", encoding="utf-8")
            self.assertEqual([line for line, _event in iter_event_records(path)], [1, 2, 3])

    def test_malformed_json_reports_source_line(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "events.jsonl"
            path.write_text("{}\nnot-json\n", encoding="utf-8")
            with self.assertRaisesRegex(EventStreamError, r"events\.jsonl:2: invalid JSON"):
                list(iter_event_records(path))


if __name__ == "__main__":
    unittest.main()
