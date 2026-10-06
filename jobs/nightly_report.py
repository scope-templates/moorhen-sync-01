"""Summarise data/latest.json: entries per category and the newest entry."""

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST_PATH = ROOT / "data" / "latest.json"


def main() -> None:
    if not LATEST_PATH.exists():
        print(f"{LATEST_PATH.relative_to(ROOT)} not found; run jobs/hourly_sync.py first", file=sys.stderr)
        sys.exit(1)
    snapshot = json.loads(LATEST_PATH.read_text())
    entries = snapshot["entries"]
    by_category = Counter(entry.get("category", "uncategorised") for entry in entries)
    print(f"report for the snapshot taken {snapshot['fetched_at']} from {snapshot['source']}")
    print(f"total entries: {len(entries)}")
    for category, count in sorted(by_category.items()):
        print(f"  {category}: {count}")
    newest = max(entries, key=lambda entry: entry.get("published_at", ""), default=None)
    if newest:
        print(f"newest: {newest['title']} ({newest.get('published_at', 'n/a')})")


if __name__ == "__main__":
    main()
