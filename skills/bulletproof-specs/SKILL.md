---
name: bulletproof-specs
description: Write or harden a product spec until an adversarial reviewer finds nothing. Use when drafting or revising a spec document, before a spec is pushed or its pull request is opened, or when review comments arrive on a spec.
---

A spec is **bulletproof** when a hostile, careful reader finds no gap: every rule is falsifiable, every combination has an outcome, every figure has a formula, every sentence has a source. Reviewers on real spec pull requests found ~160 defects that the author could have found alone. This skill moves that work before the push.

The loop: **ground → grid → draft → red-team → grill → apply → repeat → gate**. Nothing leaves the machine until the gate.

When review comments arrive on a spec that is already pushed, go to [`REVIEW-REPLIES.md`](REVIEW-REPLIES.md) instead.

## 1. Ground

Read the sources of truth before writing a line: the project context, the glossary, every sibling spec that touches this feature, the ticket, the current design of each screen, and the code the feature reads or changes. Look up facts yourself; put only decisions to the user.

Keep a **ledger**: one line per fact, with its source (`file.md` + rule ID, `path/to/file.rb:42`, ticket ID, design frame, or "user, <date>"). Claims about current behaviour, limits and lists come from the code or the provider, opened in this session.

Done when: every element of the design is in the ledger, and every statement you plan to make about the existing system has a source next to it.

## 2. Grid

Before any prose, build the **grid** the rules must cover:

- Actors × operations (view, add, update, remove). Each cell is a story, out of scope with an owner, or refused by a rule.
- For each rule, each input × its states: present, absent, zero, at the boundary, stale, not yet computed, changed mid-session.
- For each figure shown: who sees it, the smallest group it is drawn from, and how often it changes.

Done when: every cell holds an outcome, an Open Question with an owner, or an out-of-scope line naming where it lives.

## 3. Draft

Use the project's spec format (the one sibling specs follow; fall back to Overview, User Stories, Business Rules, Edge Cases, Open Questions). Match the sibling specs' voice.

- Every sentence traces to the ledger or a user decision. A sentence with no source becomes an Open Question instead. This is **provenance**: the spec states only what someone decided.
- Every rule is falsifiable: a reader can describe a case that breaks it.
- Every number carries its reason in the rationale: why this value and not half or double.
- Every computed figure has a formula, a tie rule, rounding, bounds and units, plus a worked example with real numbers under the rule.
- Every domain noun is a glossary term, defined before first use, with one meaning. A new term goes to the user as a proposal (term, definition, aliases, example) before it enters the spec.
- Every Edge Case cites the rule it applies; every Open Question has an owner (a role) and a status.

Done when: the grid maps onto rule and edge-case IDs with no orphan cell, and no sentence lacks a ledger entry.

## 4. Red-team

Hand the draft to fresh subagents with no drafting context, so they read it as a reviewer does. Use the prompt in [`RED-TEAM.md`](RED-TEAM.md) and the classes in [`DEFECTS.md`](DEFECTS.md), one subagent per lens, in parallel (with no subagents available, run the lenses one after another in a clean pass):

- **Logic**: missing state, collision, two readings, formula, validation outcome.
- **Language and links**: term drift, ripple, overclaim, ownership.
- **Outside world**: inference leak, design mismatch, unchecked code claim, unchecked source.

Triage every finding into one verdict: **defect** (fix or ask), **tracked** (an Open Question already holds it; point to it), **design** (a design detail; note it for the designer), or **unsupported** (drop it, with the reason). Verify each defect yourself against the spec text before you keep it.

Done when: every finding carries a verdict and every defect carries either a proposed edit or a question for the user.

## 5. Grill

Put each decision to the user, one at a time. For each question give, in plain words:

1. What the spec says now (quote it, with its rule ID).
2. A concrete example with a persona and real figures that shows the gap.
3. The options, with your recommendation first and its reason.

Wait for the answer before the next question. Record each answer as a rule edit or as a resolved Open Question: `Resolved (<date>) — <decision> (BR-n)`. An answer the user leaves open stays an Open Question with an owner, marked when it blocks the first build.

Done when: no defect is left without an answer or an Open Question.

## 6. Apply

Make the smallest edit that carries each decision; keep the surrounding sentences. Then run the **ripple** check: search this spec and every sibling spec for each rule ID, term and number the edit touched, and bring each reference into agreement.

Done when: every hit of every touched ID, term and number agrees with the edit.

## 7. Repeat

Red-team again: once on the changed sections, then one full pass with fresh subagents. Grill and apply again for any new defect.

Done when: one full red-team pass returns zero defects (only tracked, design or unsupported verdicts).

## 8. Gate

Show the user the diff, the list of decisions taken (with dates), and the Open Questions still open. Then stop. Commit, push, open or update a pull request only after the user says so in plain words, for this change. Keep a spec pull request to documents; a code or copy change the spec implies goes to a follow-up ticket.
