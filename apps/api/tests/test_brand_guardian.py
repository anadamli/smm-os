"""Unit tests for brand guardian (no API keys required)."""

from app.core.brand_guardian import score_draft


def test_clean_draft_passes():
    text = (
        "Agents need per-action settlement. AIFP-1 handles HTTP 402 on the rail. "
        "Learn more at https://aifinpay.io"
    )
    result = score_draft(text)
    assert result["pass"] is True
    assert result["flags"] == []


def test_tbd_fails():
    result = score_draft("Our ICP is TBD but agents are the future.")
    assert result["pass"] is False
    assert any(f["code"] == "tbd_leak" for f in result["flags"])


def test_wrong_domain_fails():
    result = score_draft("Visit https://aifinpay.com for docs.")
    assert result["pass"] is False
    assert any(f["code"] == "wrong_cta_domain" for f in result["flags"])


def test_banned_phrase_fails():
    result = score_draft("This revolutionary product changes everything.")
    assert result["pass"] is False
    assert any(f["code"] == "banned_phrase" for f in result["flags"])


def test_allowed_github_url_passes():
    text = "SDK: https://github.com/AiFinPay/Protocol-AIFP-1 and https://aifinpay.io"
    result = score_draft(text)
    assert result["pass"] is True
