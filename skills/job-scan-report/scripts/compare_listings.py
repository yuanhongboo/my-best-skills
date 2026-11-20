#!/usr/bin/env python3
"""Compare two user-verified snapshots. No network or file writes."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path


STATES = {"qualified", "ineligible", "closed", "unverified"}


def index_by_id(rows, label):
    if not isinstance(rows, list):
        raise ValueError(f"{label} must be an array")
    result = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"{label} must contain objects")
        key = row.get("id")
        if not isinstance(key, str) or not key.strip() or key != key.strip() or key in result:
            raise ValueError(f"{label} needs distinct nonempty IDs without surrounding spaces")
        if row.get("state") not in STATES:
            raise ValueError(f"{key}: unsupported state")
        result[key] = row
    return result


def compare(data):
    if not isinstance(data, dict):
        raise ValueError("expected an object")
    today = data.get("as_of")
    if not isinstance(today, str) or date.fromisoformat(today).isoformat() != today:
        raise ValueError("as_of must be an ISO calendar date")
    previous = index_by_id(data.get("previous"), "previous")
    current = index_by_id(data.get("current"), "current")
    changes = []
    for key in sorted(previous.keys() | current.keys()):
        row = current.get(key, {})
        old = previous.get(key, {}).get("state")
        evidence = row.get("evidence")
        state = row.get("state")
        if state in (None, "unverified") or row.get("checked_on") != today or not isinstance(evidence, str) or not evidence.strip():
            change = "needs_check"
        elif state == "qualified":
            change = "retained" if old == "qualified" else "new_match"
        elif old == "qualified":
            change = "removed" if state == "closed" else "downgraded"
        else:
            change = "outside_current_matches"
        changes.append({"id": key, "previous_state": old, "observed_state": state, "change": change})
    return {"as_of": today, "changes": changes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", nargs="?", help="JSON file; omit to read stdin")
    args = parser.parse_args()
    try:
        source = Path(args.snapshot).read_text(encoding="utf-8") if args.snapshot else sys.stdin.read()
        result = compare(json.loads(source))
    except (OSError, TypeError, ValueError) as exc:
        parser.exit(2, f"Invalid snapshot: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
