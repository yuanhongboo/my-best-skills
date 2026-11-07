#!/usr/bin/env python3
"""Read-only Shanghai date conversion and supplied title snapshot verification."""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

SHANGHAI = ZoneInfo('Asia/Shanghai')
TITLE = re.compile(r'\d{4}\|(功能|设计|修复|优化|发布|探索|文档|研究)\|[^|\r\n]+')
REQUIRED = {'id', 'title', 'created_at', 'project_id', 'position', 'pinned', 'archived'}


def created_date(value, unit='iso'):
    if unit == 'iso':
        if not isinstance(value, str):
            raise ValueError('ISO creation time must be a string with an explicit timezone')
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if dt.tzinfo is None or dt.utcoffset() is None:
            raise ValueError('Creation time has no explicit timezone')
    else:
        scale = 1000 if unit == 'milliseconds' else 1
        dt = datetime.fromtimestamp(float(value) / scale, timezone.utc)
    return dt.astimezone(SHANGHAI)


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def exact_equal(left, right):
    options = {'sort_keys': True, 'ensure_ascii': False, 'allow_nan': False}
    return json.dumps(left, **options) == json.dumps(right, **options)


def index_records(rows, label):
    if not isinstance(rows, list):
        raise ValueError(f'{label} must be an array')
    found = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id']:
            raise ValueError(f'{label} contains a missing or invalid id')
        if row['id'] in found:
            raise ValueError(f'{label} contains duplicate id: {row["id"]}')
        found[row['id']] = row
    return found


def snapshot(data):
    if not isinstance(data, dict) or not {'threads', 'projects', 'sections'} <= data.keys():
        raise ValueError('Snapshot must contain threads, projects and sections')
    if not isinstance(data['projects'], list) or not isinstance(data['sections'], list):
        raise ValueError('projects and sections must be arrays in source order')
    rows = index_records(data['threads'], 'threads')
    for row in rows.values():
        if not REQUIRED <= row.keys():
            raise ValueError(f'Missing snapshot fields for {row["id"]}: {sorted(REQUIRED-row.keys())}')
        if not isinstance(row['title'], str):
            raise ValueError(f'title must be a string for {row["id"]}')
        if not isinstance(row['pinned'], bool) or not isinstance(row['archived'], bool):
            raise ValueError(f'pinned and archived must be boolean for {row["id"]}')
    return rows


def check_plan(before, plan):
    rows, targets = snapshot(before), index_records(plan, 'plan')
    errors = []
    if rows.keys() != targets.keys():
        errors.append('Plan target ids differ from snapshot ids')
    for ident, target in targets.items():
        if ident not in rows:
            continue
        if 'new_title' not in target:
            errors.append(f'{ident}: missing new_title; use null to retain original')
            continue
        title = target['new_title']
        if title is None:
            continue
        if not isinstance(title, str) or not TITLE.fullmatch(title):
            errors.append(f'{ident}: invalid title format or type')
            continue
        parts = title.split('|')
        if any(part != part.strip() for part in parts):
            errors.append(f'{ident}: whitespace around separator or title')
        try:
            mmdd = created_date(rows[ident]['created_at']).strftime('%m%d')
            if parts[0] != mmdd:
                errors.append(f'{ident}: title date differs from Shanghai creation date {mmdd}')
        except (ValueError, TypeError, OverflowError) as exc:
            errors.append(f'{ident}: unverified creation time: {exc}')
    return errors


def verify(before, after, plan):
    errors = check_plan(before, plan)
    old, new, targets = snapshot(before), snapshot(after), index_records(plan, 'plan')
    if list(old) != list(new):
        errors.append('Thread ids or source order changed')
    if before.keys() != after.keys():
        errors.append('Snapshot metadata keys changed')
    for key in sorted(before.keys() | after.keys()):
        if key != 'threads' and not exact_equal(before.get(key), after.get(key)):
            errors.append(f'Snapshot metadata changed: {key}')
    renamed = unchanged = 0
    for ident in old:
        if ident not in new:
            continue
        expected = targets.get(ident, {}).get('new_title')
        if expected is None:
            expected = old[ident]['title']
        if new[ident]['title'] != expected:
            errors.append(f'{ident}: actual title differs from verification plan')
        elif expected == old[ident]['title']:
            unchanged += 1
        else:
            renamed += 1
        if not exact_equal(
            {k: v for k, v in old[ident].items() if k != 'title'},
            {k: v for k, v in new[ident].items() if k != 'title'},
        ):
            errors.append(f'{ident}: protected fields changed')
    return {'ok': not errors, 'renamed': renamed, 'unchanged': unchanged, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    date = sub.add_parser('date')
    date.add_argument('--value', required=True)
    date.add_argument('--unit', choices=['iso', 'seconds', 'milliseconds'], default='iso')
    for command in ['check-plan', 'verify']:
        cmd = sub.add_parser(command)
        cmd.add_argument('--before', required=True)
        cmd.add_argument('--plan', required=True)
        if command == 'verify':
            cmd.add_argument('--after', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'date':
            dt = created_date(args.value, args.unit)
            result = {'created_at_shanghai': dt.isoformat(), 'mmdd': dt.strftime('%m%d')}
        else:
            before, plan = load_json(args.before), load_json(args.plan)
            if args.command == 'verify':
                result = verify(before, load_json(args.after), plan)
            else:
                errors = check_plan(before, plan)
                result = {'ok': not errors, 'errors': errors}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get('ok', True) else 1
    except (ValueError, TypeError, OverflowError, OSError, KeyError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
