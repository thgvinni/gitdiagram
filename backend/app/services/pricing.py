from __future__ import annotations

from dataclasses import dataclass

DEFAULT_PRICING_MODEL = "claude-haiku-4-5"


@dataclass(frozen=True)
class ModelPricing:
    input_per_million_usd: float
    output_per_million_usd: float


MODEL_PRICING: dict[str, ModelPricing] = {
    "claude-opus-4-6": ModelPricing(input_per_million_usd=15.0, output_per_million_usd=75.0),
    "claude-sonnet-4-6": ModelPricing(input_per_million_usd=3.0, output_per_million_usd=15.0),
    "claude-opus-4": ModelPricing(input_per_million_usd=15.0, output_per_million_usd=75.0),
    "claude-sonnet-4": ModelPricing(input_per_million_usd=3.0, output_per_million_usd=15.0),
    "claude-haiku-4-5": ModelPricing(input_per_million_usd=0.80, output_per_million_usd=4.0),
    "claude-haiku-4": ModelPricing(input_per_million_usd=0.80, output_per_million_usd=4.0),
    "claude-3-5-sonnet": ModelPricing(input_per_million_usd=3.0, output_per_million_usd=15.0),
    "claude-3-5-haiku": ModelPricing(input_per_million_usd=0.80, output_per_million_usd=4.0),
}

DEFAULT_PRICING = MODEL_PRICING[DEFAULT_PRICING_MODEL]


def _strip_date_snapshot_suffix(model: str) -> str:
    import re

    return re.sub(r"-\d{8}$", "", model, flags=re.IGNORECASE)


def resolve_pricing_model(model: str) -> str:
    normalized = model.strip().lower()
    if normalized in MODEL_PRICING:
        return normalized

    without_date = _strip_date_snapshot_suffix(normalized)
    if without_date in MODEL_PRICING:
        return without_date

    if without_date.startswith("claude-opus-4"):
        return "claude-opus-4"
    if without_date.startswith("claude-sonnet-4"):
        return "claude-sonnet-4"
    if without_date.startswith("claude-haiku-4"):
        return "claude-haiku-4"
    if without_date.startswith("claude-3-5-sonnet"):
        return "claude-3-5-sonnet"
    if without_date.startswith("claude-3-5-haiku"):
        return "claude-3-5-haiku"

    return DEFAULT_PRICING_MODEL


def estimate_text_token_cost_usd(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> tuple[float, str, ModelPricing]:
    pricing_model = resolve_pricing_model(model)
    pricing = MODEL_PRICING.get(pricing_model, DEFAULT_PRICING)
    input_cost = (max(input_tokens, 0) / 1_000_000) * pricing.input_per_million_usd
    output_cost = (max(output_tokens, 0) / 1_000_000) * pricing.output_per_million_usd
    return (input_cost + output_cost, pricing_model, pricing)
