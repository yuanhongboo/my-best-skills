#!/usr/bin/env python3
"""Plan measured voice segments on an integer frame timeline. No dependencies."""
import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


def seconds(value, field):
    if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
        raise ValueError(f"{field} must be a JSON number")
    number = Decimal(value)
    if not number.is_finite() or number < 0:
        raise ValueError(f"{field} must be finite and nonnegative")
    return number


def plan(data):
    if not isinstance(data, dict):
        raise ValueError("expected an object")
    fps = data.get("fps")
    if type(fps) is not int or fps <= 0:
        raise ValueError("fps must be a positive integer")
    rows = data.get("segments")
    if not isinstance(rows, list) or not rows:
        raise ValueError("segments must be a nonempty array")
    def frame(at):
        return int((at * fps).to_integral_value(rounding=ROUND_HALF_UP))

    seen = set()
    result = []
    at = Decimal(0)
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each segment must be an object")
        key = row.get("id")
        if not isinstance(key, str) or not key.strip() or key in seen:
            raise ValueError("segment IDs must be unique nonempty strings")
        seen.add(key)
        end_speech = at + seconds(row.get("seconds"), "seconds")
        end = end_speech + seconds(row.get("pause_after", 0), "pause_after")
        if frame(end_speech) <= frame(at):
            raise ValueError(f"{key}: speech must occupy at least one frame")
        result.append({"id": key, "start_frame": frame(at), "speech_end_frame": frame(end_speech), "end_frame": frame(end)})
        at = end
    return {"fps": fps, "total_frames": frame(at), "segments": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timing", nargs="?", help="JSON file; omit to read stdin")
    args = parser.parse_args()
    try:
        source = Path(args.timing).read_text(encoding="utf-8") if args.timing else sys.stdin.read()
        result = plan(json.loads(source, parse_float=Decimal))
    except (OSError, ValueError, InvalidOperation) as exc:
        parser.exit(2, f"Invalid timing: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
