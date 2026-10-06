"""Fetch the feed once and write data/latest.json."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from feedsource import ROOT, feed_label, load_entries  # noqa: E402

LATEST_PATH = ROOT / "data" / "latest.json"


def main() -> None:
    entries = load_entries()
    snapshot = {
        "source": feed_label(),
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "entries": entries,
    }
    LATEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    LATEST_PATH.write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"synced {len(entries)} entries from {feed_label()} to {LATEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
