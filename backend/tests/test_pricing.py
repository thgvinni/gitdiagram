from app.services.pricing import estimate_text_token_cost_usd, resolve_pricing_model


def test_resolve_pricing_model_keeps_claude_haiku_4_5_on_its_own_tier():
    assert resolve_pricing_model("claude-haiku-4-5") == "claude-haiku-4-5"


def test_estimate_text_token_cost_uses_claude_haiku_4_5_pricing():
    cost_usd, pricing_model, pricing = estimate_text_token_cost_usd(
        model="claude-haiku-4-5",
        input_tokens=1_000_000,
        output_tokens=1_000_000,
    )

    assert pricing_model == "claude-haiku-4-5"
    assert pricing.input_per_million_usd == 0.80
    assert pricing.output_per_million_usd == 4.0
    assert cost_usd == 4.8
