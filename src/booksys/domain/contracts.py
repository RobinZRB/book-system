"""Small dependency-free validators shared by catalog and learning."""

from __future__ import annotations

import re
from typing import Any


class ContractError(ValueError):
    pass


ALLOWED_RATINGS = frozenset({"again", "hard", "good", "easy"})
_ID_RE = re.compile(r"^[a-z][a-z0-9_:-]{7,127}$")


def validate_identifier(value: Any, field: str = "id") -> str:
    if not isinstance(value, str) or not _ID_RE.match(value):
        raise ContractError(f"{field} must be an opaque stable identifier")
    return value
