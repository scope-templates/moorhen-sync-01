import json
import os
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
FEED_URL = os.environ.get("FEED_URL", "").strip()
SAMPLE_FEED = ROOT / "feed" / "sample.json"


def feed_label() -> str:
    return FEED_URL or str(SAMPLE_FEED.relative_to(ROOT))


def load_entries() -> list[dict]:
    if FEED_URL:
        response = requests.get(FEED_URL, timeout=15)
        response.raise_for_status()
        payload = response.json()
    else:
        payload = json.loads(SAMPLE_FEED.read_text())
    entries = payload.get("entries") if isinstance(payload, dict) else None
    if not isinstance(entries, list):
        raise ValueError("feed payload must be an object with an 'entries' list")
    for entry in entries:
        if not isinstance(entry, dict) or "id" not in entry or "title" not in entry:
            raise ValueError("every feed entry needs an 'id' and a 'title'")
    return entries
