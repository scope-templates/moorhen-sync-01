# Moorhen Sync

Moorhen Sync, a feed poller with two scheduled jobs. The worker watches a JSON feed and prints every entry it
has not seen before; the two jobs run once and exit.

## Run locally

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python worker.py                 # long-running poller, stop with Ctrl-C
python jobs/hourly_sync.py       # fetch the feed once, write data/latest.json
python jobs/nightly_report.py    # summarise data/latest.json
```

## Processes

| Entry point              | Kind         | What it does                                                                        |
| ------------------------ | ------------ | ----------------------------------------------------------------------------------- |
| `worker.py`              | long-running | polls the feed every `POLL_SECONDS`, prints new entries, remembers seen ids in `state.json` |
| `jobs/hourly_sync.py`    | runs once    | meant to run hourly: fetches the feed and writes `data/latest.json`                 |
| `jobs/nightly_report.py` | runs once    | meant to run nightly: prints a count per category from `data/latest.json`           |

## Environment

| Variable       | Default                       | Purpose                                                                  |
| -------------- | ----------------------------- | ------------------------------------------------------------------------ |
| `FEED_URL`     | unset, reads `feed/sample.json` | URL of a JSON feed shaped like `feed/sample.json`                      |
| `POLL_SECONDS` | `30`                          | worker poll interval                                                     |

A feed is an object with an `entries` list; each entry has an `id`, a `title`, a `category` and a
`published_at` timestamp. `state.json` and `data/latest.json` are written next to the code and are ignored by git.
