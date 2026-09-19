# Compact Package Preparation

Prepare exactly one current compact book package. Do not create legacy analysis files or staging artifacts.

## Required package layout

```
<book-slug>/
  book.json
  book.md
  chapters/
    <chapter-slug>/
      source.md
      guide.md
      concepts.json
```

`book.json` declares `schema_version`, a stable `book_id`, the display `title`, and every chapter's stable `chapter_id` together with the `slug` that names its directory. Do not repeat a chapter's display title into the declaration; the chapter map in `book.md` is where display titles live. `concepts.json` is a JSON array of objects; every object has a stable `id` and a non-empty `name`, and may carry `aliases` listing the alternate names by which the concept is also known.

Write source material to `source.md` and a reader-facing, non-spoiler guide to `guide.md`. Keep all package resources self-contained. Validate the prepared directory before publication, then publish only through `booksys packages import <prepared-package-dir>`.
