## ADDED Requirements

### Requirement: Catalog candidates on selection failure
When automatic book selection fails, preparation SHALL return an `insufficient_evidence` result with structured candidates instead of a bare error. Candidates SHALL provide a compact per-book summary (slug, title, category, aliases, profile path, chapter directory names) within the configured context budget, and SHALL NOT include keyword maps, profile bodies, or chapter internals.

#### Scenario: Company query without domain words
- **WHEN** a query names a company or concept without any literal category keyword (e.g., 分析下中国平安, 看看宁德时代怎么样)
- **THEN** preparation returns candidates covering the catalog's books under `insufficient_evidence` instead of raising a bare selection error

#### Scenario: Book core keyword query
- **WHEN** a query contains a book's own core keyword but no category keyword (e.g., 分析AXTI的瓶颈点, 用安全边际的思路看平安)
- **THEN** preparation returns candidates containing that book, and the caller may retry with an explicit selector

#### Scenario: Candidates stay compact at scale
- **WHEN** the catalog grows
- **THEN** candidate entries remain compact summaries while per-book detail (profile, keyword map) loads only after a book is selected

### Requirement: Caller-selected chapters
The `user.analyze` request SHALL accept an optional `chapters` array naming chapter directories of the selected package. Valid names SHALL become the chapter candidates with reason `caller_selected`, bypassing keyword matching. Unknown names SHALL fail with the available chapter list. Explicit chapters SHALL take precedence over indexed matching, and `whole_book` scope behavior SHALL remain unchanged.

#### Scenario: Skill selects chapters after reading the profile
- **WHEN** a caller retries with explicit `chapters` drawn from the prepared profile's chapter index
- **THEN** preparation loads evidence for exactly those chapters and records `caller_selected` as the match reason

#### Scenario: Unknown chapter name
- **WHEN** a request names a chapter that does not exist in the selected package
- **THEN** preparation fails with the available chapter list and does not substitute a guessed chapter

### Requirement: Honest match reasons
Chapter keyword matching SHALL be symmetric: a hit occurs when a query token appears inside a keyword cell or when the full keyword text appears in the query. Match reasons SHALL record the keyword-cell text rather than a query fragment.

#### Scenario: Full keyword mention
- **WHEN** a query contains the complete text of a keyword-map keyword (e.g., 安全边际 inside 用安全边际的思路看平安)
- **THEN** the mapped chapter is matched and the reason names the keyword 安全边际

### Requirement: Complete chapter-selection context
For a selected book, preparation SHALL include the complete chapter index and the complete keyword-to-chapter map as dedicated context sections, and SHALL record the profile's full path.

#### Scenario: Phase-two chapter review
- **WHEN** a caller reviews the prepared context to decide which chapters to name explicitly
- **THEN** every chapter-index row and every keyword-map row of the selected book is present, without truncation

#### Scenario: Source profile remains reachable
- **WHEN** a caller needs detail beyond the prepared sections
- **THEN** the profile's full path is recorded in the manifest

### Requirement: Distinguish selection failure from missing evidence
Preparation SHALL carry an explicit diagnostic distinguishing "no book selected" from "book selected but protocol sections lack evidence", alongside any candidate list.

#### Scenario: No book selected
- **WHEN** automatic book selection fails and candidates are returned
- **THEN** the diagnostic marks the selection failure and reports the candidate count, so the caller knows to choose a book and retry

#### Scenario: Book selected without section evidence
- **WHEN** a book is selected but indexed evidence does not cover required protocol sections
- **THEN** the diagnostic reports missing sections and the whole-book-search option without marking a selection failure

### Requirement: Recorded selection rationale
The request SHALL accept an optional `selection_rationale` string, which preparation SHALL copy into the analysis manifest and operation receipt unchanged.

#### Scenario: Candidate-based retry
- **WHEN** a caller retries with an explicit selector after reviewing candidates
- **THEN** the manifest records the caller's rationale alongside the chosen book or chapters

## MODIFIED Requirements

### Requirement: Prepare an operation workspace
The system SHALL expose concrete preparation intents for reader, user, coach, and trainer workflows. Preparation SHALL produce a versioned operation workspace containing the normalized request, only the context required for that intent, result instructions, a strict result schema when a commit is permitted, and a snapshot of relevant input identities. A `book-user` investment analysis workspace SHALL select the applicable book or books and protocol, construct an evidence package from the book profile and every matched chapter resource without a default context-size ceiling, return a machine-readable execution report, accept a validated external fact package, retain its provenance, freshness, conflicts, counter-evidence, and missing-data diagnostics, and expose those records separately from book evidence without a writable result contract. For investment or finance requests it SHALL also expose structured protocol execution metadata sufficient to render the Gate, risk investigation, dimension states, counter-evidence status, and missing-fact status without guessing from unstructured prose. When automatic selection cannot resolve books, preparation SHALL return structured catalog candidates rather than a bare error, and the request MAY name explicit chapters and carry a caller selection rationale.

#### Scenario: Prepare a chapter extraction
- **WHEN** `book-reader` prepares an extraction for a known book and chapter
- **THEN** the workspace contains the raw source, applicable extraction guidance, identifiers, provenance requirements, and result schema without requiring the skill to discover project paths

#### Scenario: Prepare a read-only analysis
- **WHEN** `book-user` prepares an analysis request
- **THEN** the workspace contains the selected protocol and minimum relevant evidence package, detailed execution metadata when the request is investment or finance related, validated external facts when supplied, and does not expose a writable result contract

#### Scenario: External fact conflict
- **WHEN** an analysis request contains conflicting external facts for the same field and applicable date
- **THEN** preparation exposes the conflict diagnostic and does not collapse the values into one asserted fact

#### Scenario: Ambiguous selector
- **WHEN** a request matches more than one book, chapter, or concept
- **THEN** preparation fails with structured candidates and does not guess a target

#### Scenario: Analysis context audit
- **WHEN** a uniquely selected analysis request has indexed evidence
- **THEN** preparation includes every matched protocol section, chapter, or resource without a default context-size ceiling, reports elapsed time and actual context size, and records evidence counts and skipped sections

#### Scenario: Insufficient evidence
- **WHEN** indexed selection cannot supply sufficient evidence for one or more applicable protocol sections, or automatic book selection fails
- **THEN** preparation returns an `insufficient_evidence` diagnostic with query terms, every matched chapter or resource, missing sections, structured catalog candidates where applicable, and an explicit whole-book-search option without silently widening the search; matched evidence remains available for partial analysis

#### Scenario: Explicit whole-book search
- **WHEN** a caller explicitly requests whole-book search after an insufficient-evidence result
- **THEN** preparation performs the expanded search under its separately reported budget and returns the scope, elapsed time, context size, and resulting evidence coverage

#### Scenario: External facts are incomplete
- **WHEN** an analysis request includes external facts with missing source, retrieval time, applicable date, or field value
- **THEN** preparation preserves each missing item in the execution report and marks it unverified rather than treating it as book-derived or validated evidence

#### Scenario: Partial investment evidence
- **WHEN** an investment analysis has matched evidence but some protocol sections or external facts are unavailable
- **THEN** preparation retains the matched evidence and records the unavailable sections and facts as explicit states rather than suppressing the analysis
