"""Small text helpers used by the API and NLP pipeline."""

import re


def clean_text(value):
    """Normalize review text without changing its meaning."""
    text = str(value or "").lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s.,!?'-]", "", text)).strip()
