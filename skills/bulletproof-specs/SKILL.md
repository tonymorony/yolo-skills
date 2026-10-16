---
name: bulletproof-specs
description: Write or harden a product spec until an adversarial reviewer finds nothing. Use when drafting or revising a spec document, before a spec is pushed or its pull request is opened, or when review comments arrive on a spec.
---

A spec is **bulletproof** when a hostile, careful reader finds no gap: every rule is falsifiable, every combination has an outcome, every figure has a formula, every sentence has a source. Reviewers on real spec pull requests found ~160 defects that the author could have found alone. This skill moves that work before the push.

The loop: **ground → grid → slice → draft → red-team → grill → apply → repeat → gate**. Nothing leaves the machine until the gate.

When review comments arrive on a spec that is already pushed, go to [`REVIEW-REPLIES.md`](REVIEW-REPLIES.md) instead.

## 1. Ground

Read the sources of truth before writing a line: the project context, the glossary, every sibling spec that touches this feature, the ticket, the current design of each screen, and the code the feature reads or changes. Look up facts yourself; put only decisions to the user.

Keep a **ledger**: one line per fact, with its source (`file.md` + rule ID, `path/to/file.rb:42`, ticket ID, design frame, or "user, <date>"). Claims about current behaviour, limits and lists come from the code or the provider, opened in this session. Cite a ticket, pull request or rule ID only after you open it: a roadmap or a summary is a lead, not a source. Read the Open Questions of every sibling spec too: a resolved one is a decision, and it binds this spec as a rule does.

Done when: every element of the design is in the ledger, and every statement you plan to make about the existing system has a source next to it.

## 2. Grid

Before any prose, build the **grid** the rules must cover:

- Actors × operations (view, add, update, remove). Each cell is a story, out of scope with an owner, or refused by a rule.
- For each rule, each input × its states: present, absent, zero, at the boundary, stale, not yet computed, changed mid-session.
- For each figure shown: who sees it, the smallest group it is drawn from, and how often it changes.

Done when: every cell holds an outcome, an open Open Question with its **Until then** outcome, or an out-of-scope line naming where it lives.

## 3. Slice

Cut the grid into vertical **slices**. Each slice is a part of the feature a team can build and a member can use alone: its own rules, edge cases and open questions, and later its own build ticket. The first slice is the smallest one with no open dependency.

- One concept stays in one spec file. The slices build that file up, one pull request each, stacked in order (in an Argus project: `gh stack`, trunk `develop`).
- A slice that waits on another spec or an open decision goes last, so it holds back no other slice.
- Changes to sibling specs and the glossary go in the slice that needs them.

Done when: every grid cell belongs to exactly one slice, and each slice names what it depends on.

## 4. Draft

Use the project's spec format (the one sibling specs follow; fall back to Overview, User Stories, Business Rules, Edge Cases, Open Questions). Write every line under the writing rules at the end of this file.

- Every sentence traces to the ledger or a user decision. A sentence with no source becomes an Open Question instead. This is **provenance**: the spec states only what someone decided.
- Every rule is falsifiable: a reader can describe a case that breaks it.
- Every number carries its reason in the rationale: why this value and not half or double.
- Every computed figure has a formula, a tie rule, rounding, bounds and units, plus a worked example with real numbers under the rule.
- Every domain noun is a glossary term, defined before first use, with one meaning. A new term goes to the user as a proposal (term, definition, aliases, example) before it enters the spec.
- Every Edge Case cites the rule it applies; every Open Question follows the open-question rules at the end of this file.

Done when: the grid maps onto rule and edge-case IDs with no orphan cell, and no sentence lacks a ledger entry.

## 5. Red-team

Draft and red-team one slice at a time. Hand the draft to fresh subagents with no drafting context, so they read it as a reviewer does. Use the prompt in [`RED-TEAM.md`](RED-TEAM.md) and the classes in [`DEFECTS.md`](DEFECTS.md), one subagent per lens, in parallel (with no subagents available, run the lenses one after another in a clean pass):

- **Logic**: missing state, collision, two readings, formula, validation outcome.
- **Language and links**: term drift, plain words, ripple, overclaim, ownership.
- **Outside world**: inference leak, design mismatch, code claim, source claim.

Triage every finding into one verdict: **defect** (fix or ask), **tracked** (an Open Question already holds it; point to it), **design** (a design detail; note it for the designer), or **unsupported** (drop it, with the reason). Verify each defect yourself against the spec text before you keep it.

Done when: every finding carries a verdict and every defect carries either a proposed edit or a question for the user.

## 6. Grill

Put each decision to the user, one at a time. For each question give, in plain words:

1. What the spec says now (quote it, with its rule ID).
2. A concrete example with a persona and real figures that shows the gap.
3. The options, with your recommendation first and its reason.

Wait for the answer before the next question. Check each answer against the ledger and the sibling specs before you record it; a conflict becomes the next question.

Run each answer through the grid before you record it. This is the **consequence check**. Ask four things:

- Which figures use the decision?
- Which screens show it?
- Which inputs feed it, in every period, type and boundary value?
- What does a person using the app see between an edit and the next refresh?

Each gap becomes the next question. Check a decision that changes a computation or a refresh first: on one spec, two such decisions caused about 30 follow-up review comments. Record each answer as a rule edit or as a resolved Open Question: `Resolved (<date>) — <decision> (BR-n)`. An answer the user leaves open becomes an open Open Question under the rules below. An answer that blocks the first build stays in the grill.

Done when: every defect and every consequence-check gap has an answer or an Open Question.

## 7. Apply

Make the smallest edit that carries each decision; keep the surrounding sentences. Then run the **ripple** check: search this spec and every sibling spec for each rule ID, term and number the edit touched, and bring each reference into agreement.

Then run the **diff check**: read the diff against the version before this step. Only the intended lines may change. Restore any lost line. A scripted edit, a merge and a conflict resolution lose lines most often.

Done when: every touched ID, term and number agrees with the edit. The diff check shows only the intended lines.

## 8. Repeat

A **round** is one red-team pass on the changed rules, then one full pass, both with fresh subagents. The step 5 pass counts as round one. Count rounds per slice. Give the subagents the list of decisions taken since the last pass. Grill and apply again for any new defect.

Stop after three rounds that still find defects. Each round costs a full review, and a defect that survives three needs a user decision, not another pass. Put each such defect to the user. A defect that blocks the first build needs a decision. Any other defect can become an open Open Question with an owner, **Blocks** and **Until then**.

Done when: one full pass returns zero defects (only tracked, design or unsupported verdicts). After round three, done when the user has answered every defect left.

## 9. Gate

Enter the gate only when no open Open Question blocks the first build.

Show the user the diff, the list of decisions taken (with dates), the open Open Questions with their **Blocks** and **Until then**, and the ticket drafts (build tickets, design tickets, notes on owning tickets). Then stop. Commit, push, open or update a pull request only after the user says so in plain words, for this change. Keep a spec pull request to documents; a code or copy change the spec implies goes to a follow-up ticket.

Done when: the user has said go, revise or stop for this diff. On go, commit and push. On revise, return to step 7.

Tickets come after the spec. Create or update a ticket (a build ticket, a design ticket, or a note on an owning ticket) only after the spec pull request is merged. Use the drafts kept at the gate.

## Open Questions

An open question is a hole a reviewer can attack, so each one is either closed or **fenced**.

- **Resolved**: every grill decision is recorded as `Resolved (<date>) — <decision> (BR-n)`, naming the options set aside when they matter. It keeps the question from being reopened.
- **Open**: each carries an owner (a role, never a person), **Blocks** (the first build, a named later spec or ticket, or nothing) and **Until then** (the behaviour this spec states meanwhile, as a rule ID). A fenced question leaves no grid cell empty.
- **Blocks the first build**: such a question stays in the grill until it is decided; it never reaches the gate as open.
- **Owned elsewhere**: a question a later spec owns is a pointer to that spec's ticket. At the gate, draft a note for that ticket. Post the note after the spec pull request is merged.

## Writing

Every text this skill produces follows Simplified Technical English (ASD-STE100): the spec, its glossary rows, the replies, the commit messages, the pull request text, the ticket notes and the reports to the user.

- Use the active voice and simple tenses: present, past and future.
- Give one idea in each sentence, in 20 words or fewer. Keep paragraphs to six sentences or fewer.
- Use the same word for the same idea every time. Use plain words: no idiom, slang, metaphor or jargon.
- **Describe**: say what a thing does, what it costs, and what it cannot do. Leave praise and blame out.
- Define a term before its second use. Take domain words from the project glossary, and read it before naming a domain concept.
- Keep technical items exact: file paths, rule IDs, identifiers, commands, numbers, prices and quoted text.
- Name the noun again when a pronoun could point to two nouns. After "the tickets" and "the team", write "the tickets", not "them".
- Text a person reads in the app also follows the project's copy rules. In a spec, write the rule the copy must meet; the exact words are the design's call.

In an Argus project: the glossary is `docs/glossary.md`, and a new term goes through the term-lifecycle flow before it enters the spec. The copy rules are the Copy constraints in `.argus/project.md`. Specs live in `docs/specs/`. A table cell (a rule, a rationale, an edge case, an open question) obeys the same sentence rules as prose. Each rule cell holds one constraint, and its reason goes in the Rationale cell.
