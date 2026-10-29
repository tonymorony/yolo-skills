#!/usr/bin/env python3
"""Check a spec file for the mistakes a script can find.

Usage: python3 -I spec_lint.py <spec.md> [--upper REF ...] [--since REF]
                              [--repo-path PATH]

Run it from the repository root. It reports:

- duplicate: one ID (BR-1, EC-3, OQ-21) heads two table rows.
- dangling: a row cites an ID of this spec that no row defines.
- line-cite: a code citation carries a line number (`app/x.rb:25`),
  which goes stale; name the declaration or the key instead.
- missing-path: a cited path does not exist in the working tree.
- out-of-order: an ID heads a row after a higher ID of its kind
  (BR-118 above BR-16). A spec whose slices keep numbers stable says
  "Numbers are stable across slices", and then this check is skipped.
- long-rule: a rule cell holds more than 5 sentences; split the rule.
- long-sentence: a sentence in a rule cell has more than 20 words.
  Both size checks read only the rows added or changed since --since.
- upstack: with --upper, an ID that this file added since --since
  (default HEAD) heads a different row in a higher slice of the stack.
  --repo-path names the file in git when <spec.md> is a copy.

An ID cited after a spec name ("user-accounts BR-5", "billing
OQ-11": a hyphenated word, a sibling spec file, or "its BR-42") belongs to that
spec and is not checked here. Exit status 1
when anything is reported.
"""
import os
import re
import subprocess
import sys

ROW = re.compile(r"^\|\s*([A-Z]{2,4}-\d+)\s*\|")
CITE = re.compile(r"(?<![\w-])((?:BR|EC|OQ)-\d+)\b")
EXTERNAL = re.compile(r"(?<![\w-])([A-Za-z][a-z-]*)\s+(?:BR|EC|OQ)-\d+\s*$")
CODE = re.compile(r"`([\w./-]+\.[a-z]{1,5})(:\d+(?:-\d+)?)?`")
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"`(])")
STABLE = "Numbers are stable across slices"
MAX_SENTENCES, MAX_WORDS = 5, 20


def rows(text):
    found = {}
    for n, line in enumerate(text.splitlines(), 1):
        m = ROW.match(line)
        if m:
            first = line.split("|")[2].strip()
            found.setdefault(m.group(1), []).append((n, first))
    return found


def is_spec(word, specs):
    word = word.lower()
    return word == "its" or "-" in word or os.path.exists(os.path.join(specs, word + ".md"))


def git_show(ref, path):
    out = subprocess.run(["git", "show", f"{ref}:{path}"],
                         capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else ""


def main(argv):
    path, upper, since, repo_path = None, [], "HEAD", None
    args = iter(argv)
    for a in args:
        if a == "--upper":
            upper.append(next(args))
        elif a == "--since":
            since = next(args)
        elif a == "--repo-path":
            repo_path = next(args)
        else:
            path = a
    if not path:
        sys.exit(__doc__)
    text = open(path, encoding="utf-8").read()
    specs = os.path.dirname(repo_path or path)
    defined = rows(text)
    report = []

    for id_, places in defined.items():
        if len(places) > 1:
            report.append(f"duplicate {id_}: lines {', '.join(str(n) for n, _ in places)}")

    if STABLE not in text:
        last = {}
        for id_, places in sorted(defined.items(), key=lambda kv: kv[1][0][0]):
            kind, num = id_.split("-")
            prev = last.get(kind)
            if prev and int(num) < int(prev.split("-")[1]):
                report.append(f"out-of-order {prev}: line {defined[prev][0][0]}, above {id_}")
            last[kind] = id_

    before = rows(git_show(since, repo_path or path))
    for id_, places in defined.items():
        n, cell = places[0]
        if id_ in before and before[id_][0][1] == cell:
            continue
        sentences = [x for x in SENTENCE.split(cell) if x.strip()]
        if len(sentences) > MAX_SENTENCES:
            report.append(f"long-rule {id_}: line {n}, {len(sentences)} sentences")
        for x in sentences:
            if len(x.split()) > MAX_WORDS:
                report.append(f"long-sentence {id_}: line {n}, {len(x.split())} words: {x[:50]}...")

    for n, line in enumerate(text.splitlines(), 1):
        for m in CITE.finditer(line):
            ext = EXTERNAL.search(line[:m.end()])
            if ext and is_spec(ext.group(1), specs):
                continue
            if m.group(1) not in defined:
                report.append(f"dangling {m.group(1)}: line {n}")
        for m in CODE.finditer(line):
            file, lineno = m.group(1), m.group(2)
            if "/" not in file and not file.startswith("."):
                continue
            if lineno:
                report.append(f"line-cite {file}{lineno}: line {n}")
            if not os.path.exists(file) and "no spec yet" not in line:
                report.append(f"missing-path {file}: line {n}")

    if upper:
        repo_path = repo_path or path
        added = [i for i in defined if i not in before]
        for ref in upper:
            theirs = rows(git_show(ref, repo_path))
            for id_ in added:
                if id_ in theirs and theirs[id_][0][1] != defined[id_][0][1]:
                    report.append(f"upstack {id_}: {ref} line {theirs[id_][0][0]} holds another row")

    for line in dict.fromkeys(report):
        print(line)
    sys.exit(1 if report else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
