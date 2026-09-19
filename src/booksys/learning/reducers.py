from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable


def reduce_reading(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(events)
    return {"event_count": len(rows), "last_occurred_at": rows[-1].get("occurred_at") if rows else None}


def reduce_mastery(events: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    state: dict[str, dict[str, Any]] = defaultdict(lambda: {"reviews": 0, "passes": 0, "last_rating": None})
    for event in events:
        aggregate = event.get("aggregate_id")
        payload = event.get("payload") or {}
        if not aggregate:
            continue
        state[aggregate]["reviews"] += 1
        state[aggregate]["passes"] += int(bool(payload.get("objective_pass")))
        state[aggregate]["last_rating"] = payload.get("final_rating")
    return dict(state)
