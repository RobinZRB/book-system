import json
import tempfile
import unittest
from pathlib import Path

from booksys.catalog import CatalogError, list_books, locate_chapter, locate_concept, select_book
from booksys.config import resolve_roots


def _write_package(root: Path, slug: str, book_id: str, chapter_id: str) -> Path:
    package = root / ".booksys" / "content" / "books" / slug
    chapter = package / "chapters" / "01-intro"
    chapter.mkdir(parents=True)
    (package / "book.json").write_text(json.dumps({
        "schema_version": 1, "book_id": book_id, "title": slug.title(),
        "chapters": [{"chapter_id": chapter_id, "slug": "01-intro"}],
    }), encoding="utf-8")
    (package / "book.md").write_text(f"# {slug}", encoding="utf-8")
    (chapter / "source.md").write_text("source", encoding="utf-8")
    (chapter / "guide.md").write_text("guide", encoding="utf-8")
    (chapter / "concepts.json").write_text(json.dumps([{"id": f"concept:{book_id[-8:]}", "name": "One", "aliases": ["Uno"]}]), encoding="utf-8")
    return package


class CatalogTests(unittest.TestCase):
    def _roots(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        _write_package(root, "demo", "book:12345678", "chapter:12345678")
        return td, root, resolve_roots(root)

    def test_list_and_id_lookup(self):
        td, _root, roots = self._roots()
        with td:
            self.assertEqual(list_books(roots)[0]["book_id"], "book:12345678")
            self.assertTrue(select_book(roots, "book:12345678")["package_path"].endswith("demo"))
            located = locate_chapter(roots, "book:12345678", "chapter:12345678")
            self.assertTrue(located["source_path"].endswith("01-intro\\source.md"))
            self.assertTrue(located["concepts_path"].endswith("01-intro\\concepts.json"))

    def test_concept_is_located_by_declared_id(self):
        td, _root, roots = self._roots()
        with td:
            self.assertEqual(locate_concept(roots, "concept:12345678")["chapter_id"], "chapter:12345678")
            with self.assertRaises(CatalogError):
                locate_concept(roots, "concept:00000000")

    def test_names_and_unknown_ids_are_not_resolved(self):
        td, _root, roots = self._roots()
        with td:
            for selector in ("demo", "Demo", "Demo title", "missing"):
                with self.assertRaises(CatalogError):
                    select_book(roots, selector)
            with self.assertRaises(CatalogError):
                locate_chapter(roots, "book:12345678", "01-intro")
            with self.assertRaises(CatalogError):
                locate_chapter(roots, "book:12345678", "chapter:00000000")

    def test_invalid_package_is_reported(self):
        td, root, roots = self._roots()
        with td:
            _write_package(root, "second", "book:87654321", "chapter:87654321")
            (root / ".booksys" / "content" / "books" / "second" / "chapters" / "01-intro" / "guide.md").write_text("", encoding="utf-8")
            with self.assertRaises(CatalogError) as raised:
                list_books(roots)
            self.assertIn("missing or empty resource", str(raised.exception))

    def test_global_stable_id_collision_is_rejected(self):
        td, root, roots = self._roots()
        with td:
            second = _write_package(root, "second", "book:87654321", "chapter:87654321")
            concepts_path = second / "chapters" / "01-intro" / "concepts.json"
            concepts_path.write_text(json.dumps([{"id": "concept:12345678", "name": "Duplicate"}]), encoding="utf-8")
            with self.assertRaises(CatalogError) as raised:
                list_books(roots)
            self.assertIn("duplicate stable id concept:12345678", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
