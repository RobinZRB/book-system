# knowledge-packages Specification

## Purpose
The compact on-disk package that carries book material: one small declaration, one book-level narrative, and per-chapter source, guide, and concept resources. It fixes the rules for immutable identities, display-only titles and aliases, chapter-bound resources, strict validation, and publication without overwrite, and it requires the canonical catalog to contain only this format after migration.

## Requirements

### Requirement: Versioned package manifest
Each formal book SHALL have one small declaration containing its stable book identity, its display title, and its declared chapter resources. Each chapter SHALL declare a stable identity and a slug naming its directory. The declaration SHALL identify the package format version; it SHALL not require a digest, media type, or role entry for every resource.

#### Scenario: Valid package manifest
- **WHEN** a package is validated
- **THEN** its book declaration and every declared chapter resource exist, have unique stable identities, and conform to the declared format version

#### Scenario: Category changes
- **WHEN** a book is reclassified
- **THEN** its immutable identity and learning history remain unchanged while display metadata can be updated

### Requirement: Stable identities and aliases
Books, chapters, and trainable concepts SHALL have immutable internal identifiers. Human-readable titles, slugs, names, and aliases SHALL remain display values that let a reader or an AI recognise an entity; they SHALL not be a lookup key for the runtime and SHALL not be the join key for learning history. A book SHALL carry exactly one display title and a chapter SHALL carry exactly one slug, because each is already the display value for that entity; only trainable concepts SHALL additionally carry aliases, which record the alternate names by which a concept may be recognised.

#### Scenario: Concept rename
- **WHEN** a concept display name changes
- **THEN** existing review events continue to resolve through the unchanged concept identifier and the prior name can remain an alias

#### Scenario: Duplicate display names
- **WHEN** two concepts share a display name
- **THEN** the package preserves distinct identifiers, the runtime resolves identities only, and disambiguating the two is the caller's decision

### Requirement: Structured and narrative resource split
Each chapter SHALL retain a source resource, a concise narrative guide, and a structured concept resource. The book-level narrative resource SHALL contain the book framework and chapter map. Supplemental indexes, reference excerpts, relations files, global fact graphs, and glossaries are optional authored material rather than required authoritative resources.

#### Scenario: Direct framework reading
- **WHEN** book-user needs a framework before selecting a chapter
- **THEN** it can read the book-level narrative resource and declared chapter map directly

#### Scenario: Trainer concept loading
- **WHEN** book-trainer creates a review activity
- **THEN** it can read the selected chapter's declared concept resource without a global fact graph or generated concept index

#### Scenario: Optional derived material is removed
- **WHEN** optional derived indexes or views are removed
- **THEN** direct package resources remain usable and nothing the runtime reads has changed

#### Scenario: Derived material is edited by hand
- **WHEN** an optional derived view is edited manually
- **THEN** validation does not treat that edit as an authoritative source, guide, or concept change

### Requirement: Source binding and inference labels
Each chapter's guide and concept resource SHALL live inside that chapter's directory, so a chapter-bound claim is bound to its source by construction and no per-claim source reference is required. Character-span digests and per-claim references are optional authored metadata rather than an import prerequisite. Inference and synthesis SHALL be labelled as inference rather than presented as a verbatim source statement.

#### Scenario: Guide is bound to its chapter
- **WHEN** a guide summarizes a chapter-specific concept as a direct statement
- **THEN** its location inside the declaring chapter identifies the source a skill can inspect

#### Scenario: Inference is retained
- **WHEN** a package records an inference or synthesis
- **THEN** the resource labels it as inference or synthesis rather than a verbatim source statement

### Requirement: Strict package validation
Validation SHALL fail on a missing declaration, missing or empty required source, guide, or concept resource, malformed format version, duplicate stable identities, and invalid declared paths. It SHALL report actionable diagnostics without requiring projection-drift checks or per-resource digests.

#### Scenario: Missing chapter guide
- **WHEN** a formal package lacks a declared chapter guide
- **THEN** validation fails and identifies the chapter and resource

#### Scenario: Invalid package declaration
- **WHEN** a package declaration is malformed or contains an escaping path
- **THEN** validation fails rather than resolving a guessed or unsafe path

#### Scenario: Invalid configuration
- **WHEN** catalog configuration exists but cannot be parsed or contains an invalid required value
- **THEN** the command exits with failure rather than silently using default paths

### Requirement: V2 package publication
When formal package publication is enabled, the system SHALL validate a prepared small package before making it available in the canonical catalog. It SHALL reject an attempted overwrite of a published package without changing the catalog.

#### Scenario: Publish a valid package
- **WHEN** an operator imports a valid prepared package with a unique path
- **THEN** it becomes available from the canonical catalog

#### Scenario: Reject an existing package
- **WHEN** publication would overwrite an existing package
- **THEN** it fails without changing the catalog

#### Scenario: Catalog reads only declared resources
- **WHEN** the direct catalog passes small-package validation
- **THEN** catalog lookup reads only declared small-package resources

### Requirement: Full staged legacy migration
The canonical catalog SHALL contain only the small package format after migration. Legacy manifests, global fact graphs, required derivative chapter files, and active-stage metadata SHALL not remain runtime prerequisites.

#### Scenario: Migrated package is usable
- **WHEN** a migrated package passes validation
- **THEN** book-user, book-coach, and book-trainer can locate declared resources without legacy package metadata

#### Scenario: V1 provenance cleanup
- **WHEN** active package metadata is normalized after cutover
- **THEN** validation remains successful and stable identities remain unchanged
