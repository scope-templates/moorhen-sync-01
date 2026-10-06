import json
import os
import signal
import sys
import time

import requests

from feedsource import ROOT, feed_label, load_entries

POLL_SECONDS = float(os.environ.get("POLL_SECONDS", "30"))
STATE_PATH = ROOT / "state.json"


def load_seen() -> set[str]:
    if not STATE_PATH.exists():
        return set()
    return set(json.loads(STATE_PATH.read_text())["seen_ids"])


def save_seen(seen: set[str]) -> None:
    STATE_PATH.write_text(json.dumps({"seen_ids": sorted(seen)}, indent=2) + "\n")


def stop(signum, frame):
    raise KeyboardInterrupt


def main() -> None:
    signal.signal(signal.SIGTERM, stop)
    seen = load_seen()
    print(f"polling {feed_label()} every {POLL_SECONDS:g}s ({len(seen)} entries already seen)", flush=True)
    try:
        while True:
            try:
                entries = load_entries()
            except (requests.RequestException, ValueError, OSError) as exc:
                print(f"feed error: {exc}", file=sys.stderr, flush=True)
            else:
                fresh = [entry for entry in entries if str(entry["id"]) not in seen]
                for entry in fresh:
                    print(f"new entry {entry['id']}: {entry['title']}", flush=True)
                    seen.add(str(entry["id"]))
                if fresh:
                    save_seen(seen)
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        pass
    print("stopping", flush=True)


if __name__ == "__main__":
    main()
