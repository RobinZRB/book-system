## Why

The current runtime duplicates semantic work that an online AI is better placed
to do: choosing books and chapters, deciding the relevant analysis path, and
interpreting external evidence.  That duplication has accumulated into
operation workspaces, fixed analysis plans, and a large request/result
contract that slow down ordinary book questions without verifying the truth of
the resulting answer.

The project still needs durable book material and a reliable learning record.
This change keeps book preparation, coaching, training, stable identities, and
FSRS, while making question answering an AI-led, direct-read workflow.

## What Changes

- **BREAKING** Replace formal v2 package resources with a small book package:
  `book.json`, `book.md`, and per-chapter `source.md`, `guide.md`, and
  `concepts.json`.
- **BREAKING** Remove the active-stage pointer, generic `prepare`/`commit`
  workspaces, analysis-context copies, operation receipts, and projection
  commands from the ordinary runtime path.
- Add a catalog interface that lists and locates declared book and chapter
  resources by stable identifier, without attempting semantic selection.
  **BREAKING** It no longer resolves a title, display name, or alias and no
  longer returns candidates: mapping a name to an identifier belongs to the AI.
- Make `book-user` choose relevant books, chapters, material current-fact
  research, and answer structure. Its guidance retains disclosure and
  uncertainty rules across domains, but no runtime-generated `analysis_plan`,
  `assurance`, Gate, risk list, or external-fact state machine.
- Preserve `book-coach` and `book-trainer` as independent learning skills.
  Replace their generic operation flow with a small learning interface for
  status, chapter completion, due work, and review recording; retain
  append-only events, stable IDs, and FSRS behind that interface. **BREAKING**
  Review takes a concept ID alone, status is no longer filtered per book, and a
  repeated chapter completion appends a further event instead of failing.
- **BREAKING** Remove the installer, the release archive, and the config-writing
  command. Roots are declared with command-line options or a hand-written
  `.booksys/config.json`, and no code path builds a distribution artifact.
- Simplify validation and behavioral evaluation around package integrity,
  learning invariants, and answer-quality rubrics rather than keyword-routing
  and generated analysis-state contracts.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `booksys-operations`: replace generic prepared workspaces with direct catalog
  and learning command interfaces.
- `knowledge-packages`: define the small package resource set while preserving
  stable identities and per-chapter source binding.
- `learning-state`: retain event-backed coaching, training, and FSRS through a
  narrow learning interface.
- `skill-distribution`: redefine the four skills' direct workflows and the
  self-contained bundle each one carries.
- `framework-analysis-assurance`: move answer-assurance behavior from runtime
  plans to AI-owned skill guidance.
- `v2-only-runtime`: replace active-stage-pointer resolution with one
  canonical direct catalog and learning-state layout.

## Impact

Affected code includes `analysis_context.py`, `operations/`, package
validation/importing, CLI routing, the four skill bundles, schemas, tests,
and evaluations.  The `learning/` implementation remains but receives a
smaller public seam.  Existing v2 content must be migrated before its current
package readers are removed; no migration implementation is included in this
planning change.
