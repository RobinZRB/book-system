from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import importlib
from typing import Any


class SchedulerUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class SchedulerPolicy:
    desired_retention: float = 0.90
    scheduler_version: str = "fsrs==6.3.2"
    parameter_version: str = "default-compact"


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _moment(value: Any) -> datetime | None:
    return datetime.fromisoformat(value) if isinstance(value, str) and value else None


class FSRSAdapter:
    """Private adapter; third-party FSRS objects never cross the domain seam.

    ``schedule`` accepts the previously recorded ``state`` mapping verbatim, so a
    concept's review history feeds the next scheduling decision rather than
    restarting from a fresh card.
    """

    def __init__(self, policy: SchedulerPolicy | None = None):
        self.policy = policy or SchedulerPolicy()
        try:
            importlib.import_module("fsrs")
        except ImportError as exc:
            raise SchedulerUnavailable("pinned fsrs dependency is unavailable") from exc

    def schedule(self, *, rating: str, state: dict[str, Any] | None = None, review_datetime: datetime | None = None) -> dict[str, Any]:
        if rating not in {"again", "hard", "good", "easy"}:
            raise ValueError("invalid final scheduling rating")
        try:
            from fsrs import Card, Rating, Scheduler, State
            card = self._card(Card, State, state)
            fsrs_rating = {"again": Rating.Again, "hard": Rating.Hard, "good": Rating.Good, "easy": Rating.Easy}[rating]
            reviewed, log = Scheduler(desired_retention=self.policy.desired_retention, enable_fuzzing=False).review_card(card, fsrs_rating, review_datetime or datetime.now(timezone.utc))
        except (ImportError, AttributeError, TypeError, KeyError, ValueError) as exc:
            raise SchedulerUnavailable(f"unsupported pinned fsrs dependency: {exc}") from exc
        return {
            "rating": rating,
            "desired_retention": self.policy.desired_retention,
            "scheduler_version": self.policy.scheduler_version,
            "parameter_version": self.policy.parameter_version,
            "due": _iso(reviewed.due),
            "state": self._dump(reviewed),
            "review_datetime": log.review_datetime.isoformat(),
        }

    @staticmethod
    def _dump(card: Any) -> dict[str, Any]:
        return {
            "state": card.state.name,
            "step": card.step,
            "stability": card.stability,
            "difficulty": card.difficulty,
            "due": _iso(card.due),
            "last_review": _iso(card.last_review),
        }

    @staticmethod
    def _card(card_type: Any, state_type: Any, state: dict[str, Any] | None) -> Any:
        if not state:
            return card_type()
        return card_type(
            state=state_type[state["state"]],
            step=state.get("step"),
            stability=state.get("stability"),
            difficulty=state.get("difficulty"),
            due=_moment(state.get("due")),
            last_review=_moment(state.get("last_review")),
        )
