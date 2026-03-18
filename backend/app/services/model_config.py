from __future__ import annotations

import os

DEFAULT_MODEL = "claude-haiku-4-5"


def get_model() -> str:
    model = os.getenv("ANTHROPIC_MODEL", "").strip()
    return model or DEFAULT_MODEL
