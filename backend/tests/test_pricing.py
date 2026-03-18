from app.services.pricing import estimate_text_token_cost_usd, resolve_pricing_model


def test_resolve_pricing_model_keeps_claude_sonnet_4_on_its_own_tier():
    assert resolve_pricing_model("claude-sonnet-4") == "claude-sonnet-4"
    assert resolve_pricing_model("claude-sonnet-4-20250514") == "claude-sonnet-4"


def test_estimate_text_token_cost_uses_claude_sonnet_4_pricing():
    cost_usd, pricing_model, pricing = estimate_text_token_cost_usd(
        model="claude-sonnet-4-20250514",
        input_tokens=1_000_000,
        output_tokens=1_000_000,
    )

    assert pricing_model == "claude-sonnet-4"
    assert pricing.input_per_million_usd == 3.0
    assert pricing.output_per_million_usd == 15.0
    assert cost_usd == 18.0
