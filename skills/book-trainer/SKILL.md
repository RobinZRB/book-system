---
name: book-trainer
description: Assess learning from compact book packages and append-only review events.
---

# Book Trainer

Read concepts from declared chapter `concepts.json` resources. Use `booksys learn status` and `booksys learn due` for learning state, then record an objective review with `booksys learn review <concept-id> <json-payload>`.

`<concept-id>` is the stable `id` declared in `concepts.json`; pick it yourself from that file, since the runtime matches IDs only and never resolves a name or alias. Each accepted review appends one event and resumes FSRS from the concept's previous scheduling state.

`<json-payload>` is a JSON object carrying `question_kind`, `target_level`, `emt_expectations`, `misconceptions`, `emt_hits`, `emt_score`, `objective_pass`, `confidence`, and `user_rating`. `target_level` is an integer 1-5; `user_rating` is one of `hard`, `good`, `easy`. Fix `emt_expectations` and `misconceptions` before the attempt and keep them unchanged for its duration.

Session policy: at most 15 reviews per day, at most 2 consecutive reviews from the same chapter, and the objective pass threshold rises by level (L1 0.60, L2 0.70, L3 0.75, L4 0.80, L5 0.85). Set `objective_pass` true only when `emt_score` reaches the threshold for `target_level`.

Use `resources/reference/DESIGN.md` as supporting method guidance. Objective failure forces final scheduling rating `again`; retain the original user rating and evidence. Never modify package content or reading events.

Harness discipline: before recording a review, reread the declared concept ID from `concepts.json`. For a transport retry of the same assessment, reuse one `--idempotency-key`; use a new key for a new assessment. If lookup fails, reread the package rather than guessing an ID.
