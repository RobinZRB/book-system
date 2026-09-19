import json
import tempfile
import unittest
from pathlib import Path

from booksys.config import RootConfig
from booksys.learning.service import complete_chapter, due, review_concept, status

BOOK_ID = "book:demo1234"
CHAPTER_ID = "chapter:one1234"
CONCEPT_ID = "concept:oneconcept1234"


def _review(rating="good", passed=True):
    return {
        "question_kind": "recall",
        "target_level": 1,
        "emt_expectations": ["states the definition"],
        "misconceptions": ["confuses it with the neighbouring idea"],
        "emt_hits": ["states the definition"] if passed else [],
        "emt_score": 1.0 if passed else 0.2,
        "objective_pass": passed,
        "confidence": 0.9,
        "user_rating": rating,
    }


class LearningServiceTests(unittest.TestCase):
    def _roots(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        package = root / ".booksys" / "content" / "books" / "demo"
        chapter = package / "chapters" / "one"
        chapter.mkdir(parents=True)
        (package / "book.md").write_text("# Demo\n", encoding="utf-8")
        (package / "book.json").write_text(json.dumps({
            "schema_version": 1, "book_id": BOOK_ID, "title": "Demo",
            "chapters": [{"chapter_id": CHAPTER_ID, "slug": "one"}],
        }), encoding="utf-8")
        (chapter / "source.md").write_text("source\n", encoding="utf-8")
        (chapter / "guide.md").write_text("guide\n", encoding="utf-8")
        (chapter / "concepts.json").write_text(json.dumps([
            {"id": CONCEPT_ID, "name": "One", "aliases": ["Uno"]},
        ]), encoding="utf-8")
        return td, root, RootConfig(system_root=root, data_root=root)

    def _events(self, root: Path):
        path = root / ".booksys" / "runtime" / "learning" / "events.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").strip().splitlines()]

    def test_reading_events_accumulate(self):
        td, root, roots = self._roots()
        with td:
            first = complete_chapter(roots, BOOK_ID, CHAPTER_ID)
            second = complete_chapter(roots, BOOK_ID, CHAPTER_ID)
            self.assertEqual(first["status"]["reading"]["event_count"], 1)
            self.assertEqual(second["status"]["reading"]["event_count"], 2)
            self.assertEqual([event["kind"] for event in self._events(root)], ["reading", "reading"])
            self.assertEqual(self._events(root)[0]["payload"]["book_id"], BOOK_ID)

    def test_harness_retry_with_same_key_is_not_recorded_twice(self):
        td, root, roots = self._roots()
        with td:
            first = review_concept(roots, CONCEPT_ID, _review(), idempotency_key="harness-review-001")
            retry = review_concept(roots, CONCEPT_ID, _review(), idempotency_key="harness-review-001")
            self.assertTrue(first["recorded"])
            self.assertFalse(retry["recorded"])
            self.assertEqual(len(self._events(root)), 1)
            self.assertEqual(retry["event"]["event_id"], first["event"]["event_id"])

    def test_unknown_identifiers_are_rejected_without_writing(self):
        td, root, roots = self._roots()
        with td:
            with self.assertRaises(Exception):
                complete_chapter(roots, BOOK_ID, "chapter:nope1234")
            with self.assertRaises(ValueError):
                review_concept(roots, "concept:nope1234", _review())
            with self.assertRaises(ValueError):
                review_concept(roots, CONCEPT_ID, {"question_kind": "recall"})
            self.assertFalse((root / ".booksys" / "runtime" / "learning" / "events.jsonl").exists())

    def test_mastery_and_objective_failure(self):
        td, _root, roots = self._roots()
        with td:
            failed = review_concept(roots, CONCEPT_ID, _review(rating="easy", passed=False))
            self.assertEqual(failed["schedule"]["rating"], "again")
            self.assertEqual(failed["event"]["payload"]["user_rating"], "easy")
            self.assertEqual(status(roots)["mastery"][CONCEPT_ID], {"reviews": 1, "passes": 0, "last_rating": "again"})

    def test_scheduling_resumes_from_recorded_state(self):
        td, _root, roots = self._roots()
        with td:
            first = review_concept(roots, CONCEPT_ID, _review())
            second = review_concept(roots, CONCEPT_ID, _review())
            # A fresh card stays on its first learning step; resuming graduates it into review.
            self.assertEqual(first["schedule"]["state"]["state"], "Learning")
            self.assertEqual(second["schedule"]["state"]["state"], "Review")
            self.assertGreater(second["schedule"]["due"], first["schedule"]["due"])
            self.assertEqual(second["schedule"]["state"]["step"], None)
            self.assertEqual(status(roots)["mastery"][CONCEPT_ID]["reviews"], 2)

    def test_recorded_state_round_trips_through_the_scheduler(self):
        from booksys.learning.scheduler import FSRSAdapter
        td, _root, roots = self._roots()
        with td:
            first = review_concept(roots, CONCEPT_ID, _review())
            replayed = FSRSAdapter().schedule(rating="good", state=first["schedule"]["state"])
            recorded = review_concept(roots, CONCEPT_ID, _review())["schedule"]["state"]
            keys = ("state", "step", "stability", "difficulty")
            self.assertEqual({key: replayed["state"][key] for key in keys}, {key: recorded[key] for key in keys})
            self.assertIsNotNone(first["schedule"]["state"]["last_review"])

    def test_stability_grows_only_when_state_is_fed_back(self):
        from datetime import datetime, timedelta, timezone
        from booksys.learning.scheduler import FSRSAdapter
        adapter = FSRSAdapter()
        base = datetime(2026, 1, 1, tzinfo=timezone.utc)
        moments = [base, base + timedelta(minutes=10), base + timedelta(minutes=10, days=2), base + timedelta(minutes=10, days=9)]

        chained, state = [], None
        for moment in moments:
            state = adapter.schedule(rating="good", state=state, review_datetime=moment)["state"]
            chained.append(state["stability"])
        restarted = [adapter.schedule(rating="good", review_datetime=moment)["state"]["stability"] for moment in moments]

        self.assertEqual(chained[0], chained[1])
        self.assertGreater(chained[2], chained[1])
        self.assertGreater(chained[3], chained[2])
        self.assertEqual(len(set(restarted)), 1)
        self.assertEqual(restarted[0], chained[0])

    def test_due_only_after_the_scheduled_moment(self):
        td, _root, roots = self._roots()
        with td:
            self.assertEqual(due(roots), [])
            review_concept(roots, CONCEPT_ID, _review())
            self.assertEqual(due(roots), [])


if __name__ == "__main__":
    unittest.main()
