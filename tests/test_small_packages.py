import json
import tempfile
import unittest
from pathlib import Path

from booksys.packages.small import validate_book_md_links, validate_small_package


class SmallPackageTests(unittest.TestCase):
    def _package(self, root: Path) -> Path:
        package = root / "book"
        chapter = package / "chapters" / "01-intro"
        chapter.mkdir(parents=True)
        (package / "book.json").write_text(json.dumps({
            "schema_version": 1,
            "book_id": "book:12345678",
            "title": "Demo",
            "chapters": [{"chapter_id": "chapter:12345678", "slug": "01-intro"}],
        }), encoding="utf-8")
        (package / "book.md").write_text("# Demo\n", encoding="utf-8")
        (chapter / "source.md").write_text("source\n", encoding="utf-8")
        (chapter / "guide.md").write_text("guide\n", encoding="utf-8")
        (chapter / "concepts.json").write_text(json.dumps([{"id": "concept:12345678", "name": "Concept"}]), encoding="utf-8")
        return package

    def test_valid_small_package(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(validate_small_package(self._package(Path(td))), [])

    def test_missing_required_resource_fails(self):
        with tempfile.TemporaryDirectory() as td:
            package = self._package(Path(td))
            (package / "chapters" / "01-intro" / "guide.md").unlink()
            errors = validate_small_package(package)
            self.assertIn("chapter 01-intro missing or empty resource: guide.md", errors)

    def test_duplicate_concept_id_fails(self):
        with tempfile.TemporaryDirectory() as td:
            package = self._package(Path(td))
            (package / "chapters" / "01-intro" / "concepts.json").write_text(json.dumps([
                {"id": "concept:12345678", "name": "Concept"},
                {"id": "concept:12345678", "name": "Duplicate"},
            ]), encoding="utf-8")
            self.assertIn("duplicate concept id: concept:12345678", validate_small_package(package))

    def _catalog_package(self, system: Path) -> Path:
        """A package already published under the catalog, as doctor sees it."""
        package = system / ".booksys" / "content" / "books" / "book"
        chapter = package / "chapters" / "01-intro"
        chapter.mkdir(parents=True)
        (package / "book.json").write_text(json.dumps({
            "schema_version": 1,
            "book_id": "book:12345678",
            "title": "Demo",
            "chapters": [{"chapter_id": "chapter:12345678", "slug": "01-intro"}],
        }), encoding="utf-8")
        (package / "book.md").write_text("# Demo\n", encoding="utf-8")
        (chapter / "source.md").write_text("source\n", encoding="utf-8")
        (chapter / "guide.md").write_text("guide\n", encoding="utf-8")
        (chapter / "concepts.json").write_text(json.dumps([{"id": "concept:12345678", "name": "Concept"}]), encoding="utf-8")
        return package

    def test_book_md_links_resolve_against_system_root(self):
        with tempfile.TemporaryDirectory() as td:
            system = Path(td)
            package = self._catalog_package(system)
            (package / "book.md").write_text(
                "# Demo\n\n[ch1](.booksys/content/books/book/chapters/01-intro/source.md)\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_book_md_links(package, system), [])

    def test_book_md_missing_link_target_fails(self):
        with tempfile.TemporaryDirectory() as td:
            system = Path(td)
            package = self._catalog_package(system)
            (package / "book.md").write_text(
                "# Demo\n\n[gone](.booksys/content/books/book/chapters/99-nope/source.md)\n",
                encoding="utf-8",
            )
            errors = validate_book_md_links(package, system)
            self.assertEqual(len(errors), 1)
            self.assertIn("99-nope", errors[0])

    def test_book_md_external_and_anchor_links_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            system = Path(td)
            package = self._catalog_package(system)
            (package / "book.md").write_text(
                "# Demo\n\n"
                "[web](https://example.com/a) [mail](mailto:a@b.c) "
                "[frag](#section) [proto](//host/x)\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_book_md_links(package, system), [])

if __name__ == "__main__":
    unittest.main()
