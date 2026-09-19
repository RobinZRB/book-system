import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from booksys.cli import main


BOOK_ID = "book:cli12345"
CHAPTER_ID = "chapter:cli12345"
CONCEPT_ID = "concept:cli12345"


def _project() -> tuple[tempfile.TemporaryDirectory, Path]:
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    package = root / ".booksys" / "content" / "books" / "demo"
    chapter = package / "chapters" / "one"
    chapter.mkdir(parents=True)
    (package / "book.json").write_text(json.dumps({
        "schema_version": 1,
        "book_id": BOOK_ID,
        "title": "CLI demo",
        "chapters": [{"chapter_id": CHAPTER_ID, "slug": "one"}],
    }), encoding="utf-8")
    (package / "book.md").write_text("# CLI demo\n", encoding="utf-8")
    (chapter / "source.md").write_text("source\n", encoding="utf-8")
    (chapter / "guide.md").write_text("guide\n", encoding="utf-8")
    (chapter / "concepts.json").write_text(json.dumps([{"id": CONCEPT_ID, "name": "Concept"}]), encoding="utf-8")
    return td, root


def _invoke(root: Path, *args: str) -> tuple[int, str, str]:
    stdout, stderr = StringIO(), StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = main(["--project-root", str(root), *args])
    return code, stdout.getvalue(), stderr.getvalue()


class CliIntegrationTests(unittest.TestCase):
    def test_valid_commands_return_json_and_success(self):
        td, root = _project()
        with td:
            code, output, error = _invoke(root, "doctor")
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output)["status"], "ok")
            self.assertEqual(error, "")
            code, output, _error = _invoke(root, "learn", "status")
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output)["reading"]["event_count"], 0)
            code, output, _error = _invoke(root, "learn", "due")
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output), {"due": []})

    def test_invalid_review_cli_input_does_not_create_event(self):
        td, root = _project()
        with td:
            payload = json.dumps({
                "question_kind": "recall",
                "target_level": "1",
                "emt_expectations": ["definition"],
                "misconceptions": [],
                "emt_hits": ["definition"],
                "emt_score": 1.0,
                "objective_pass": True,
                "confidence": 0.8,
                "user_rating": "good",
            }, ensure_ascii=False)
            code, output, error = _invoke(root, "learn", "review", CONCEPT_ID, payload)
            self.assertEqual(code, 2)
            self.assertEqual(output, "")
            self.assertIn("target_level", error)
            self.assertFalse((root / ".booksys" / "runtime" / "learning" / "events.jsonl").exists())

    def test_corrupt_history_fails_closed_and_doctor_reports_line(self):
        td, root = _project()
        with td:
            event_path = root / ".booksys" / "runtime" / "learning" / "events.jsonl"
            event_path.parent.mkdir(parents=True)
            event_path.write_text(json.dumps({
                "schema_version": 1,
                "event_id": "evt:12345678",
                "kind": "reading",
                "aggregate_id": CHAPTER_ID,
                "occurred_at": "2026-01-01T00:00:00+00:00",
                "idempotency_key": "key-1",
                "payload": {"book_id": BOOK_ID, "chapter_id": "chapter:wrong123"},
            }) + "\n", encoding="utf-8")
            original = event_path.read_bytes()
            code, output, error = _invoke(root, "doctor")
            self.assertEqual(code, 1)
            report = json.loads(output)
            self.assertEqual(report["status"], "error")
            self.assertTrue(any(item.get("line") == 1 for item in report["diagnostics"]))
            self.assertEqual(error, "")
            for command in (("learn", "status"), ("learn", "due")):
                code, output, error = _invoke(root, *command)
                self.assertEqual(code, 2)
                self.assertEqual(output, "")
                self.assertIn("aggregate_id must equal payload.chapter_id", error)
            self.assertEqual(event_path.read_bytes(), original)

    def test_malformed_json_doctor_reports_line(self):
        td, root = _project()
        with td:
            event_path = root / ".booksys" / "runtime" / "learning" / "events.jsonl"
            event_path.parent.mkdir(parents=True)
            event_path.write_text("{}\nnot-json\n", encoding="utf-8")
            code, output, _error = _invoke(root, "doctor")
            self.assertEqual(code, 1)
            report = json.loads(output)
            self.assertTrue(any(item.get("line") == 2 and "invalid JSON" in item["error"] for item in report["diagnostics"]))

    def test_doctor_reports_multiple_invalid_event_lines(self):
        td, root = _project()
        with td:
            event_path = root / ".booksys" / "runtime" / "learning" / "events.jsonl"
            event_path.parent.mkdir(parents=True)
            rows = []
            for index in (1, 2):
                rows.append(json.dumps({
                    "schema_version": 1,
                    "event_id": f"evt:invalid{index}",
                    "kind": "reading",
                    "aggregate_id": CHAPTER_ID,
                    "occurred_at": "2026-01-01T00:00:00+00:00",
                    "idempotency_key": f"key-{index}",
                    "payload": {"book_id": BOOK_ID, "chapter_id": f"chapter:wrong{index}"},
                }))
            event_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
            code, output, _error = _invoke(root, "doctor")
            self.assertEqual(code, 1)
            report = json.loads(output)
            lines = {item.get("line") for item in report["diagnostics"] if "line" in item}
            self.assertEqual(lines, {1, 2})


if __name__ == "__main__":
    unittest.main()
