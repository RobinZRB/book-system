## 1. Establish v2-only safety checks

- [x] 1.1 Inventory every v1/legacy marker in runnable source, active `.booksys` data, skill bundles, evaluations, and operator docs (excluding OpenSpec archives), and verify each candidate has a documented consumer or deletion/normalization path.
- [x] 1.2 Add failing tests for v2 default-root resolution without `compatibility_default`, explicit external data roots, and rejection of the removed baseline CLI command; verify the tests fail before implementation.
- [x] 1.3 Add a deterministic residue-scan check covering the defined runnable/active scope and verify it reports the current v1 markers before cleanup.

## 2. Remove executable v1 compatibility surface

- [x] 2.1 Simplify root configuration to v2-default semantics, remove the compatibility flag and terminology, and verify default and external-root runtime tests pass.
- [x] 2.2 Remove the baseline CLI registration, generator module, and obsolete baseline tests; verify `booksys baseline` is rejected without creating files.
- [x] 2.3 Update CLI help, public-surface tests, and operator documentation to describe only supported v2 behavior; verify no runnable v1 command or compatibility marker remains.

## 3. Normalize active v2 metadata safely

- [x] 3.1 Map v1-labelled manifest, id-map, plan, and event fields to their consumers and classify each as non-identity metadata or a migration blocker; verify the inventory is complete before changing active data.
- [x] 3.2 Normalize non-identity v1 provenance labels to v2-native metadata while preserving package content, resource digests, and stable IDs; verify strict package validation and stable-ID assertions pass.
- [x] 3.3 Cross-check `legacy-due.json` and migration-only legacy review evidence against authoritative v2 runtime inputs, remove them only after explicit approval, and verify strict health checks and learning-state tests pass.
- [x] 3.4 Rename evaluation manifests and reports to a v2-native baseline identity, then verify the evaluation runner passes and release behavior gates are unchanged.

## 4. Validate the completed cleanup

- [x] 4.1 Run the full unit/integration suite, strict `booksys doctor`, projection check, and behavioral evaluation suite; verify all pass without rewriting authoritative package data.
- [x] 4.2 Run the v1 residue scan and verify it is clean outside OpenSpec archives, while confirming the active pointer and package catalog validate and that the currently empty v2 event/projection paths remain a valid pre-first-write state.
- [x] 4.3 Run `check_all.py` and strict OpenSpec validation for this change; record the clean test, health, schema, and reference-scan evidence.
