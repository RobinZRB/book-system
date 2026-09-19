## Context

See [proposal.md](proposal.md) for motivation. The current source combines a formal v2 package catalog, generic operation workspaces, AI-analysis preparation, and learning state. The only state that needs a durable transactional seam is learning: book and chapter completion, review history, and FSRS scheduling. Analysis is read-only and its relevance decisions depend on the live question and available AI capabilities.

The direct catalog remains private project content at `<system_root>/.booksys/content/books`. It replaces only the active-stage indirection; it does not move raw book material into release artifacts.

## Goals / Non-Goals

**Goals:**

- Make direct book resources the only input required for AI question answering.
- Give coaching and training a small, durable, stable-ID learning seam.
- Reduce a formal book package to the resources used by reader, user, coach, and trainer.
- Preserve a safe migration path before removing legacy runtime code or data.

**Non-Goals:**

- Proving external facts, semantic truth, or the quality of an AI conclusion in Python.
- Replacing FSRS, changing its scheduling policy, or redesigning trainer pedagogy.
- Publishing raw book content in source or release distributions.
- Supporting legacy v2 package readers after migration is complete.

## Decisions

### 1. Direct catalog, not an active stage

The canonical catalog is the directory `.booksys/content/books/<book-slug>/` under `system_root`. The catalog discovers packages by their `book.json` declaration. There is no `current.json`, stage directory, or query-specific context copy.

A package has this fixed small shape:

```text
<book-slug>/
  book.json
  book.md
  chapters/<chapter-slug>/
    source.md
    guide.md
    concepts.json
```

`book.json` declares the format version, the stable book ID, the display title, and every chapter's stable ID together with the slug naming its directory. `book.md` contains the framework, the concise overview, and the complete chapter map, so chapter display titles live there instead of being duplicated into the declaration. `concepts.json` contains stable trainable concept IDs, display names, and aliases. The declaration carries no field that only repeats another field: a book title already is the book's display value, and a chapter slug already is the chapter's. The catalog validates path containment, declared resource existence, non-emptiness, and ID uniqueness.

This is chosen over preserving a rich manifest because the rich resource graph is not consumed by direct question answering or learning. It is chosen over a global catalog index because scanning a small local book directory avoids another mutable registry.

### 2. One direct read seam for book-user

The catalog exposes read commands equivalent to:

```text
booksys books list
booksys books show <book-id>
booksys books chapter <book-id> <chapter-id>
```

They return only declared metadata and absolute resource paths. They do not accept a natural-language query, rank relevance, choose a chapter, create a workspace, or write an audit receipt.

Every argument is a stable identifier. Resolving a title, display name, or alias to an identifier is the caller's job, so the catalog never matches on display values, never disambiguates, and never returns candidates for the caller to pick from.

Book-user reads `book.md`, then the guides, concepts, and sources it judges relevant. It explains source selection when useful to the answer. This is chosen over retaining `prepare user.analyze` because a deterministic keyword matcher cannot reliably replace semantic judgment by an online AI.

### 3. Put assurance and current-fact care in guidance

Source separation, counter-evidence expectations, and uncertainty disclosure are retained as book-user protocol guidance that the AI applies when it answers. Domain-specific checklists, including any investment-oriented Gate or risk dimensions, belong in the selected book protocol rather than a runtime or separate product capability. They are not JSON fields or a fixed response sequence emitted by the runtime.

For any question that depends materially on unstable or high-stakes external facts, guidance requires source/date disclosure, distinction between book evidence and inference, material counter-evidence, and a bounded conclusion. The AI decides which research is material from the question and selected framework.

This is chosen over a structured fact package because that package validates completeness of a claim's shape, not the truth of the claim. It retains the useful quality bar without presenting format validation as factual verification.

### 4. Make learning a deep module with four commands

Learning retains append-only events, stable IDs, event replay, and FSRS. Its public interface is equivalent to:

```text
booksys learn status
booksys learn complete <book-id> <chapter-id>
booksys learn due
booksys learn review <concept-id> <review-payload>
```

Only the learning module knows event storage, reducers, projection caches, locking, and scheduler objects. Coach calls completion/status; trainer calls due/review. A review payload retains the current objective assessment and rating evidence.

An identifier that already implies its owner carries no extra scope: a concept ID is unique across the catalog, so review takes no book argument. Status is reported for the whole event stream rather than filtered per book, because grouping events by book is a matching decision the caller can make from the declarations it already read.

Each review records the scheduling state FSRS produced, and the next review of the same concept resumes from that recorded state. Without it a concept never leaves its first learning step and its interval never grows.

An event carries an optional idempotency key. Without one the event is always new, so re-reading a chapter appends a further reading event instead of being rejected as a conflicting retry.

This is chosen over letting skills edit JSONL directly because append-only history and FSRS correctness need a real write seam. It is chosen over generic `prepare`/`commit` because those commands make every workflow learn storage and result-file conventions that only learning needs.

### 5. Derived state is private and rebuildable

Reading status, mastery state, and due work are computed from events on demand. A cache may exist under the private learning root, but no skill or user-facing contract refers to a projection file or requires a separate projection command.

This retains recoverability while removing a second public storage contract.

### 6. Migration is additive before cutover

Implementation first adds the small-package reader, validator, direct catalog commands, and learning commands with isolated tests. Each existing book is converted into a new package and validated while legacy content remains untouched. After all four skills and migration fixtures use the new interface, documentation and distribution references change. Legacy code and data are removed only after a successful cutover verification and a recoverable backup has been retained outside the active catalog.

This is chosen over in-place mutation because the project has no current Git repository to make destructive rollback automatic.

## Risks / Trade-offs

- [AI omits a source, uncertainty, or counterargument] -> Keep concise quality rules in book-user guidance and test representative final responses rather than generated JSON fields.
- [Small package loses useful extracted information] -> Preserve `guide.md` and `concepts.json`; migrate optional legacy material only when it has a demonstrated consumer.
- [Stable IDs change during conversion] -> Derive and record a mapping from existing book/chapter/concept IDs before event migration; reject a conversion with duplicate or missing IDs.
- [Direct catalog reads expose private raw text through releases] -> `.booksys/content` and private learning state stay out of every distribution artifact by construction, because no distribution is built: the manifest, the build configuration, the console-script entry, and the typing marker were removed together with the release command.
- [Learning regression during interface replacement] -> Characterize current event and FSRS outputs, then test command results against those fixtures before routing coach/trainer to the new interface.
- [No active-stage rollback] -> Preserve the old catalog as a dated, non-active backup until the cutover is accepted.

## Migration Plan

1. Add the small package format, catalog validation, and direct read commands alongside legacy code.
2. Add the learning command interface backed by the existing event and FSRS behavior.
3. Convert the two active books and verify package resources, stable IDs, catalog lookups, coaching, training, and due results.
4. Rewrite the four skill bundles and behavioral evaluations to use direct catalog and learning commands.
5. Switch the documented and default runtime path to the new catalog and learning interface.
6. Run strict health checks, package validation, full tests, behavioral evaluations, and a manual representative book-user query.
7. Retire legacy analysis context, generic operations, stage metadata, schemas, and no-longer-consumed book derivatives only after the acceptance checks pass; retain a recoverable backup until the user approves final removal.

## Retired surface

These requirements existed before this change and are gone; the deployed spec store no longer contains them, so they are recorded here rather than as a spec delta.

- Prepare an operation workspace, and commit operations deterministically — generic prepared workspaces duplicated AI-owned selection and exposed a broad result contract. Replaced by direct catalog reads and narrow event recording.
- Catalog candidates on selection failure, honest match reasons, recorded selection rationale, distinguish selection failure from missing evidence, caller-selected chapter rationale — the runtime no longer keyword-matches questions to chapters, so it has nothing to explain about a match it did not make. Book-user states its source choices instead.
- Complete chapter-selection context — direct resource access replaces copied context sections.
- Superseding correction events — an append-only stream plus recomputation from the whole stream already satisfies auditability, and no producer ever emitted a correction. The `supersedes_event_id` envelope field and its event kind were removed rather than left declared and unproduced.
- Per-claim source references and character-span validation — a chapter's guide and concepts already live inside that chapter, so the binding is structural. The compact format carries no per-claim reference and validation does not require one.
- Zero-tolerance release gate, and then the offline contract check that briefly replaced it — judging fabrication, spoiler leakage, unauthorized writes, premature feedback, mutable expectations, or unsupported claims requires reading a candidate response, which a deterministic offline check cannot do; the gate was retired for that reason. The check itself was then removed too: it asserted only bundle presence, a declared command name, and catalog integrity that `doctor` already validates, and no runtime path consumed it. Its four contract files and its runner are gone rather than left as an unused harness, and no behavioural evaluation artifact remains in the repository at all; the quality expectations those artifacts used to encode live only in the skill guidance a reader or an AI applies.
- Installer, release archive, and config-writing command — the installer targeted a single harness that decision-making later dropped, the archive published raw book content that this design excludes from distribution, and roots are expressible with command-line options or a hand-written config file.
- Packaging and distribution metadata — `pyproject.toml`, `requirements.lock`, `MANIFEST.in`, the console-script entry, and `py.typed` exist only to build, install, or ship a distribution, and the runtime is invoked as `python -m booksys` against the source tree. They were removed rather than kept as a surface nothing can build. Nothing unique was lost: the version lives in `src/booksys/__init__.py`, the FSRS pin in `learning/scheduler.py`, and the Python floor in `RUNTIME.md`.
- Redundant declaration fields — the book-level `aliases` (identical to `title` in every active package), the book-level `overview` (empty in every active package, and already carried by the `book.md` narrative), and each chapter's `title` (identical to its `slug` in 29 of 31 active chapters, with display titles already carried by the `book.md` chapter map). Concept `aliases` are kept: they record real alternate names and are the material a caller uses to recognise a concept.
- `doctor` scheduler and installation probes — a missing scheduler already fails explicitly at review time, and there is no installation target left to probe.

## Open Questions

None. The optional installer and the release archive were removed rather than maintained: they duplicated a distribution path the project does not need, and the release archive published raw book content that this design excludes from distribution. Distribution is now the source tree alone — no packaging file, manifest, build configuration, or typing marker remains — and the runtime surface is four command groups that all read or write the catalog and the learning event stream. The evaluation assets and the offline contract check were removed as well: the four contract files and their runner were deleted, and the check only re-asserted bundle presence, one declared command name, and catalog integrity that `doctor` already validates.
