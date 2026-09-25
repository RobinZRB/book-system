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

## Identifier rules

`book_id` is `book:` plus 24 lowercase hex characters, every `chapter_id` is `chapter:` plus 24, every concept `id` is `concept:` plus 24 — all generated with `secrets.token_hex(12)`. The full identifier must match `^[a-z][a-z0-9_:-]{7,127}$`, and the catalog treats all three kinds as a single namespace, so never sequence, reuse, or hand-write one.

## Chapter brief (hand this to each extraction subagent)

Give every subagent the layout above, the two templates below, and the self-check. Bind it to one chapter: it reads only that chapter's `source.md`, and writes only that chapter's `guide.md` and `concepts.json`. Write the output in the language the user is working in — the templates below are written in Chinese only because that has been this project's working language; the section structure is the contract, the heading text simply follows the output language.

### `guide.md`

A non-spoiler reading guide: structure, orientation, and questions to carry into the text — never the chapter's conclusions, and never a substitute summary that removes the reason to read the original. Preserve this section structure exactly and replace only the content. Aim for roughly 600–1200 characters; an appendix or postscript may come in leaner, but never drop a heading.

```markdown
# 读前导读（chapter-guide）

> 非剧透：供人类读前/读中阅读，book-coach 可自由读取；**不含章节结论**。
> 读后总结不落库：需要 recap / 概念图谱时，按需从 AI 侧文件现场渲染（AI 侧文件含结论，不得作为读前/读中材料）。

## 本章速览
- **章节**: <序号>/<总章数> · **所属篇**: <如：第四章 查理十一讲>
- **一句话概括**: <这一章围绕什么问题展开，给出主题定位而非答案>
- **适合读者**: <谁最该读、以什么心态读>

## 本章结构
1. <小标题或论题，8～15 条；`source.md` 里的 `##` / `###` / `####` 就是原书小标题，据此归纳但不要机械罗列>
2. ...

## 读前问题

- <3～6 个能带着读的问题，指向张力与判断，不要提前给出答案>
- ...

## 阅读检查点

- [ ] <2～4 条读中自查动作>
- ...

## 作者框架与衔接
**本章采用的方法论**：<这一段是用什么结构推进的（定义→反例→归纳；案例→原则→清单…），可点出作者特有的修辞或论证手法。>

**阅读衔接**：<读本章前最好已掌握什么；本章与其余章节的关系。>
```

### `concepts.json`

```json
[
  {
    "id": "concept:3f1a9c7d20b84e5fa1c6d903",
    "name": "误判心理学",
    "aliases": ["Psychology of Human Misjudgment", "人类误判心理学"]
  }
]
```

Ten to twenty concepts per chapter, taken only from that chapter's `source.md`. A `name` must be a trainable knowledge point a reader could be questioned on, not a chapter title, a book-structure item, or a vague topic word; short beats descriptive. `aliases` carries the English original, the names the text itself uses, and common synonyms; use `[]` when there are none. Emit the file as a bare array — no wrapper object, no code fence, no comments, no trailing comma. Stay driven by the chapter's own text: never invent material, and flag anything that is your inference rather than the book's own claim with an explicit inline marker (in Chinese output, 「（推断）」).

## Self-check (required before reporting)

```bash
export PATH="/usr/bin:/bin:/c/Windows/System32:$PATH"
"/c/Users/ZRB/.workbuddy/binaries/python/versions/3.13.12/python.exe" -c "
import json,re
p=r'<chapter-dir>'
d=json.load(open(p+r'\concepts.json',encoding='utf-8'))
assert isinstance(d,list) and d
ids=set()
for i,c in enumerate(d):
    assert isinstance(c,dict), i
    assert re.fullmatch(r'concept:[0-9a-f]{24}', c['id']), (i,c.get('id'))
    assert c['id'] not in ids, ('duplicate', c['id']); ids.add(c['id'])
    assert isinstance(c['name'],str) and c['name'].strip(), i
    assert isinstance(c.get('aliases',[]),list), i
print('OK', len(d), 'concepts')
print(len(open(p+r'\guide.md',encoding='utf-8').read()), 'guide chars')
"
```

Report the printed output verbatim, along with the chapter slug, the guide's length, and the concept count — enough for the orchestrator to collect results without ever reading the chapter text. Then, at package level, check that no concept `name` repeats across chapters under the same meaning — that is what convergence removes.
