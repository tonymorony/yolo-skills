---
name: spec-review
description: Review a design pull request against the product spec it builds. Use when the user asks to review a PR, branch or prototype "vs spec" or "against the spec", or whether a screen or component follows its spec.
---

A design pull request is **on spec** when every spec atom it touches holds on the page, in its letter and in its reason, and when its example figures could come from real data. This skill finds where it is not. It fixes nothing and posts nothing before the gate.

The loop: **ground → atomise → trace → lenses → reproduce → report → gate**.

## 1. Ground

Collect every source in this session, into the session scratchpad, never into the repo:

- The PR: `gh pr view <n> --json title,body,files,commits,baseRefName,headRefName,headRefOid` and `gh pr diff <n>`. Record the head SHA. A branch with no PR: `git diff main...<branch>`. A stacked PR's diff is its own delta; review that delta and read its parent only for context.
- Every changed file in full at the head SHA, saved to disk: `git show <sha>:<path> > <scratch>/files/<path>`. Read lines from these copies with `grep -n`, `sed -n` or `awk`. Text passed through `echo "$var"` loses its line numbers, because zsh's `echo` expands `\n` inside the file.
- The spec, from the link in the PR body, its ticket or the project's `CLAUDE.md`. The link gives the repo, the ref and the path. Pin it to the commit that last changed it, and quote the URLs, because zsh reads `?` as a glob:
  ```sh
  gh api 'repos/<owner>/<repo>/contents/<path>?ref=<ref>' --jq .content | base64 -d > <scratch>/spec.md
  gh api 'repos/<owner>/<repo>/commits?path=<path>&sha=<ref>&per_page=1' --jq '.[0].sha'
  ```
- Every sibling spec that a touched rule cites, fetched the same way.
- Every other rule source the PR names, such as a knowledge-base or design-system PR, as its diff: `gh pr diff <n> -R <owner>/<repo>`.

Done when: the PR head and the spec are each pinned to a SHA, and every spec, rule and file that the PR body or a touched rule names is on disk. With no spec found, ask the user for it; a review with no spec is not this skill.

## 2. Atomise

Run `python3 -I <this skill's folder>/atoms.py <scratch>/spec.md > <scratch>/ledger.md`. The **ledger** holds every rule, edge case, open question, goal, story, scope line and prose bullet of the spec, one row each, with its source ID. A prose spec with no IDs gets IDs from its sections.

Split each row into **atoms**: one assertion a reviewer can watch hold or break on a page. "No count per band, no P10 or P90, no margin" is three atoms: BR-22a, BR-22b, BR-22c. For each atom record:

- **Element**: the component or screen part it constrains (a menu, a readout, a chart, a panel, a copy string). A row that constrains nothing visible, such as a query or a refresh schedule, takes `— not visible` and no atoms.
- **Reason**: the row's rationale, or the reason the spec gives elsewhere. The Reason lens reads it.
- A resolved open question binds as a rule does. An open one is a single atom, `open: <question>`, with its owner. An out-of-scope line is an atom of absence: "the panel offers no action".

Done when: every ledger row has atoms or `— not visible`, and every atom has an Element.

## 3. Trace

Map every element the PR adds or changes (a component, an example, a screen state, a copy string, an icon, a guide sentence) to the atoms of that Element, and write the **trace** into the ledger as `file:line`, each line confirmed on the head-SHA copy.

- An element no atom asks for is **unsourced**.
- An atom inside the PR's declared scope with no element is a **gap**. The PR body sets the scope. Atoms outside it are **not reviewed**, not gaps.

Done when: every hunk of the diff maps to an atom, or is marked unsourced or mechanical (a re-pasted asset, a changelog line).

## 4. Lenses

Run the five lenses in [`LENSES.md`](LENSES.md): Letter, Reason, Figures, Ripple, Claims. Give each one to a fresh subagent, all in parallel, with the prompt in that file, the pinned spec, the ledger with its trace, the diff and the full files. A fresh agent reads as a reviewer does, without the context of steps 1–3. With no subagents, or past the subagent limit, run the lenses one after another, each as a clean pass.

Done when: all five lenses have returned findings or "nothing found" with the atoms they checked, and the Figures lens shows its arithmetic.

## 5. Reproduce

A finding survives only when you **reproduce** it yourself: open the line on the head-SHA copy, rerun the arithmetic with `python3 -I -c`, reread the atom and its Reason. Drop what you cannot reproduce, and merge the same defect from several lenses into one finding. Rate each one:

- **High**: breaks an atom or its Reason on an element that ships or that later PRs copy, or a canonical example whose figures cannot come from real data.
- **Medium**: breaks an atom on an element the screen uses but the PR leaves stale, or breaks a format or copy rule.
- **Low**: a mechanical defect, an open question the PR answers, wording that claims more than the spec.

A defect that this PR copies from a parent or sibling PR is reported once, marked "copied from #n", at most Medium here, because the fix lives in the other PR.

Name who acts: **designer** (fix in this PR), **product** (a decision between changing the design and changing the spec), or **spec owner** (a spec edit).

Done when: every surviving finding has a `file:line`, an atom ID, evidence a reader can check, a fix or the decision to ask, and an owner.

## 6. Report

In chat:

1. The PR with its head SHA, the spec path with its pinned SHA, and the other rule sources.
2. Findings, High to Low. Each gives its title, `file:line`, atom ID, the spec's words (short quote), what the page does, the evidence, the fix or decision, the owner, and whether its line is inside the diff.
3. **On spec**: the atoms the PR meets, grouped by element, one line each.
4. **Not reviewed**: the elements outside the PR's scope, one line.

When the review disproves something said earlier in the conversation, correct it in the report.

## 7. Gate

Stop at the report. Post only when the user says so, as one GitHub review with an inline comment per finding. The event is `COMMENT`, unless the user names another; "request changes on major findings" means `REQUEST_CHANGES` when a High finding survives.

Before posting, compare the PR's current head with the pinned SHA. When it moved, read `git diff <pinned>..<head>`, recheck each finding and its line at the new head, and post against the new head.

```sh
gh api repos/<owner>/<repo>/pulls/<n>/reviews --input <scratch>/review.json
```

`review.json` holds `commit_id` (the head SHA), `body`, `event` and `comments` (`path`, `line`, `side: "RIGHT"`, `body`; `start_line` and `start_side` for a range), one comment per finding, written as the report wrote it. GitHub takes an inline comment only on a line inside a diff hunk; a finding on an untouched line, such as a stale component, goes in `body` with its `file:line`.

## Several PRs

To review several PRs, give each one to its own agent, which runs steps 1–6 and returns its report as its final message (the harness keeps subagents from writing report files). You then reproduce every High and Medium finding yourself and run the gate for each PR.
