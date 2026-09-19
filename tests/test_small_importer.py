import json
import tempfile
import unittest
from pathlib import Path

from booksys.config import RootConfig
from booksys.packages.importer import import_package


class SmallImporterTests(unittest.TestCase):
    def test_imports_compact_package_and_rejects_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "prepared"
            chapter = source / "chapters" / "one"
            chapter.mkdir(parents=True)
            (source / "book.md").write_text("demo", encoding="utf-8")
            (chapter / "source.md").write_text("source", encoding="utf-8")
            (chapter / "guide.md").write_text("guide", encoding="utf-8")
            (chapter / "concepts.json").write_text("[]", encoding="utf-8")
            (source / "book.json").write_text(json.dumps({"schema_version": 1, "book_id": "book:demo1234", "title": "Demo", "chapters": [{"chapter_id": "chapter:one1234", "slug": "one"}]}), encoding="utf-8")
            roots = RootConfig(system_root=root, data_root=root)
            import_package(roots, source)
            with self.assertRaises(FileExistsError):
                import_package(roots, source)

    def test_rejects_a_stable_id_used_by_another_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first"
            second = root / "second"
            for source in (first, second):
                chapter = source / "chapters" / "one"
                chapter.mkdir(parents=True)
                (source / "book.md").write_text("demo", encoding="utf-8")
                (chapter / "source.md").write_text("source", encoding="utf-8")
                (chapter / "guide.md").write_text("guide", encoding="utf-8")
                (chapter / "concepts.json").write_text("[]", encoding="utf-8")
                (source / "book.json").write_text(json.dumps({"schema_version": 1, "book_id": "book:demo1234", "title": source.name, "chapters": [{"chapter_id": f"chapter:{source.name}123", "slug": "one"}]}), encoding="utf-8")
            roots = RootConfig(system_root=root, data_root=root)
            import_package(roots, first)
            with self.assertRaises(ValueError) as raised:
                import_package(roots, second)
            self.assertIn("duplicate stable id book:demo1234", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
