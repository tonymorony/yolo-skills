#!/usr/bin/env python3
"""List every source row of a product spec as a ledger, one row per rule.

Usage: python3 -I atoms.py <spec.md> > ledger.md

A table row whose first cell is an ID (BR-1, EC-3, OQ-21) keeps that ID.
Every other bullet, paragraph and table gets an ID from its section:
goals-2, out-of-scope-4, worked-example-T1. A prose spec with no IDs
still lists every line a reviewer can hold a screen to.
"""
import re
import sys

ID = re.compile(r"^[A-Z]{2,4}-\d+$")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "top"


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def esc(text):
    return text.replace("|", "\\|")


def main(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    rows, section, counters = [], "top", {}
    header, table_rows, para = None, [], []

    def next_id(prefix=""):
        counters[(section, prefix)] = counters.get((section, prefix), 0) + 1
        return f"{slug(section)}-{prefix}{counters[(section, prefix)]}"

    def flush_para():
        if para:
            rows.append((next_id(), section, " ".join(para), ""))
            para.clear()

    def flush_table():
        nonlocal header
        if header and table_rows:
            rows.append((next_id("T"), section,
                         f"table: {' / '.join(header)} ({len(table_rows)} rows)", ""))
        header = None
        table_rows.clear()

    for line in lines + [""]:
        s = line.strip()
        if s.startswith("|"):
            flush_para()
            c = cells(s)
            if header is None:
                header = c
            elif set("".join(c)) <= set("-: "):
                continue
            elif ID.match(c[0]):
                detail = "; ".join(f"{h}: {v}" for h, v in zip(header[2:], c[2:]) if v)
                rows.append((c[0], section, c[1] if len(c) > 1 else "", detail))
            else:
                table_rows.append(c)
            continue
        flush_table()
        heading = re.match(r"^#{1,6}\s+(.*)", s)
        bullet = re.match(r"^(?:[-*]|\d+\.)\s+(.*)", s)
        if heading:
            flush_para()
            section = heading.group(1)
        elif bullet:
            flush_para()
            rows.append((next_id(), section, bullet.group(1), ""))
        elif s:
            para.append(s)
        else:
            flush_para()

    ids = sum(1 for r in rows if ID.match(r[0]))
    print(f"Ledger of `{path}`: {len(rows)} rows, {ids} with a spec ID.\n")
    print("| Source | Section | Text | Detail | Atoms | Element | Trace | Verdict |")
    print("|---|---|---|---|---|---|---|---|")
    for rid, sec, text, detail in rows:
        print(f"| {rid} | {esc(sec)} | {esc(text)} | {esc(detail)} | | | | |")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
