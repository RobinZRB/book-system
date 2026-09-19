import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from booksys.config import resolve_roots
from booksys.learning.events import finalize_rating, make_review_event
from booksys.learning.scheduler import FSRSAdapter


class CoreTests(unittest.TestCase):
    def test_root_precedence_and_containment(self):
        with tempfile.TemporaryDirectory() as td:
            roots = resolve_roots(td, data_root=Path(td) / "data")
            self.assertEqual(roots.data_root, Path(td, "data").resolve())
            with self.assertRaises(Exception):
                roots.data_path("..", "escape")

    def test_objective_failure_forces_again(self):
        self.assertEqual(finalize_rating("easy", False), "again")
        self.assertEqual(finalize_rating("good", True), "good")

    def test_review_keeps_evidence_and_scheduler_is_available(self):
        event = make_review_event("concept:12345678", question_kind="recall", target_level=1, emt_expectations=["x"], misconceptions=[], emt_hits=["x"], emt_score=1.0, objective_pass=True, confidence=0.9, user_rating="good", scheduler_version="fsrs==6.3.2", parameter_version="default-compact")
        self.assertEqual(event["payload"]["final_rating"], "good")
        result = FSRSAdapter().schedule(rating="good", review_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc))
        self.assertEqual(result["scheduler_version"], "fsrs==6.3.2")


if __name__ == "__main__":
    unittest.main()
