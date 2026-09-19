## 1. Positive runtime contracts

- [x] 1.1 Rewrite the active v2 runtime and operation specifications as positive contracts; verify `openspec validate v2-only --strict` passes.
- [x] 1.2 Replace retired-surface tests with active-pointer and supported-command discovery tests; verify the runtime test modules pass.

## 2. Active material cleanup

- [x] 2.1 Remove retired-version terminology from non-OpenSpec health checks, documentation, evaluation assets, and skill guidance while retaining their positive v2 checks; verify a scoped vocabulary scan has no matches.
- [x] 2.2 Run `check_all.py`, strict `booksys doctor`, and the complete test suite; verify all commands pass.
