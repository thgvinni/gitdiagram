from __future__ import annotations

import os

DEFAULT_MODEL = "claude-sonnet-4-6"


def get_model() -> str:
    model = os.getenv("ANTHROPIC_MODEL", "").strip()
    return model or DEFAULT_MODEL
