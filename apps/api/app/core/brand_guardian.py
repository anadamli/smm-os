"""Rule-based brand / claim checks for generated drafts (Slice 2)."""

from __future__ import annotations

import re
from typing import Any, Dict, List
from urllib.parse import urlparse

# Subset of brand-pack §9 guardrails — extend as pack evolves.
BANNED_PHRASES: tuple[str, ...] = (
    "guaranteed returns",
    "risk-free",
    "token moon",
    "guaranteed apy",
    "we're already profitable",
    "last chance ico",
    "revolutionary",
    "game-changing",
    "groundbreaking",
    "world-class",
    "the future is here",
    "the future is now",
    "fully decentralized",
    "bank-grade",
    "all networks live",
    "every agent",
    "enterprise-ready",
    "market leader",
    "fully audited",
    "regulatory-compliant",
    "fdic",
)

ALLOWED_URL_HOSTS: frozenset[str] = frozenset(
    {
        "aifinpay.io",
        "www.aifinpay.io",
        "dash.aifinpay.io",
        "github.com",
        "www.github.com",
        "npmjs.com",
        "www.npmjs.com",
    }
)

FORBIDDEN_DOMAIN_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"aifinpay\.com\b", re.I),
    re.compile(r"aifinpay\.company\b", re.I),
)

URL_RE = re.compile(r"https?://[^\s)\]\"'<>]+", re.I)
TBD_RE = re.compile(r"\bTBD\b", re.I)


def _flag(code: str, message: str, severity: str = "error") -> Dict[str, str]:
    return {"code": code, "message": message, "severity": severity}


def score_draft(text: str) -> Dict[str, Any]:
    """Return scorecard: flags list + pass bool (no error-severity flags)."""
    flags: List[Dict[str, str]] = []

    if TBD_RE.search(text):
        flags.append(_flag("tbd_leak", "Draft contains unresolved TBD"))

    for pattern in FORBIDDEN_DOMAIN_PATTERNS:
        if pattern.search(text):
            flags.append(
                _flag(
                    "wrong_cta_domain",
                    "Use https://aifinpay.io only (not .com / .company)",
                )
            )

    for raw_url in URL_RE.findall(text):
        url = raw_url.rstrip(".,;:")
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if not host:
            continue
        if host in ALLOWED_URL_HOSTS:
            continue
        if host.endswith(".aifinpay.io"):
            continue
        if host == "github.com" and parsed.path.lower().startswith("/aifinpay"):
            continue
        flags.append(
            _flag(
                "unexpected_url",
                f"URL host not in allowlist: {host} ({url})",
            )
        )

    lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            flags.append(
                _flag(
                    "banned_phrase",
                    f"Forbidden phrase from brand-pack guardrails: «{phrase}»",
                )
            )

    if re.search(r"\bbank\b", lower) and "not a bank" not in lower:
        flags.append(
            _flag(
                "banned_phrase",
                "Word «bank» without negation — brand-pack forbids bank positioning",
            )
        )

    passed = not any(f["severity"] == "error" for f in flags)
    return {"flags": flags, "pass": passed}
