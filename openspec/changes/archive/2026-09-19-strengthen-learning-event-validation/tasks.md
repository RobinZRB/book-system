## 1. Shared event validation

- [x] 1.1 Add dependency-free validators for review submissions, event envelopes, reading/review payloads, and recorded FSRS schedule shapes; verify focused unit tests cover valid and invalid values for every required field.
- [x] 1.2 Add event-stream iteration that preserves JSONL line locations for validation consumers while retaining the existing public event-reading behavior; verify malformed JSON and multiple invalid parsed events report their source lines.

## 2. Learning command enforcement

- [x] 2.1 Validate review data before scheduler use and event append, and validate replayed event history before deriving status or due work; verify invalid submissions leave no event file changes and corrupt history fails without partial state.
- [x] 2.2 Preserve valid reading, review, idempotency, and FSRS state-resume behavior through the shared validator; verify all existing learning service tests remain green.

## 3. Health diagnostics

- [x] 3.1 Update `doctor` to validate every event and emit read-only, line-specific diagnostics for envelope, payload, timestamp, identity, and schedule failures; verify a corrupt fixture produces nonzero exit status and actionable JSON diagnostics.

## 4. Regression verification

- [x] 4.1 Add same-process CLI integration coverage by invoking the public CLI entry point against temporary roots; verify `doctor`, `learn status`, and `learn due` return expected JSON and exit codes for valid and corrupt event streams, and that no command returns partial state after a corrupt event.
- [x] 4.2 Update runtime documentation only where needed to explain that learning reads fail on corrupt authoritative history and `doctor` is the diagnostic path; verify documented commands and paths match the CLI.
