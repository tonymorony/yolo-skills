# Review replies

The branch for a spec that is already pushed and has reviewer comments.

## Triage

Read every comment, including threads GitHub collapses as outdated. When the user links one comment, read its whole thread first. A short reply often refers to an earlier comment in that thread. Group comments by root cause first: reviewers often raise one gap in parallel threads. Give each group one verdict:

- **Defect**: the scenario holds against the spec text. Fix it or ask the user.
- **Tracked**: an Open Question already holds it. Reply with a pointer to that OQ.
- **Design**: a design detail. Reply that the wording or layout is the design's call, and note it for the designer.
- **Unsupported**: the proposal has no reason, or the reason fails. Reply with a counter-question.

A specific proposal is still a claim. Before recommending it, check its reasoning holds: "Why 20, rather than 15 or 30?" When it fails, the recommendation is the counter-question, kept polite and concrete, with an example that shows the gap.

A pushback needs evidence: a cited rule or format convention, the codebase's own word, a counter-example, or a named owner ("the fetch time is engineering's call"). A belief is not evidence.

## Keep the round finite

Every decision taken in review is new spec text, and reviewers then review it. So prefer a new Open Question to a new rule. A proposal that opens a new question becomes a new Open Question with an owner. Change a rule in this pull request only when the comment is a **Defect**. When a batch of replies brings more new comments than it closed, tell the user. The user decides when the batch ends.

## Decisions

For each group that needs a decision, ask the user one group at a time, with:

- each comment's direct link (`#discussion_r…`) and a quote, saying when the thread is collapsed as outdated;
- what the spec says now, in plain words, with a short example;
- the options, your recommendation first, with its reason.

The user decides product questions themselves; write the reply as the decision. Run the consequence check from `SKILL.md` step 6 on each answer before the next question. Collect all decisions, then edit. Use the smallest change, the ripple check and the diff check from `SKILL.md` step 7. Then run every lens from `RED-TEAM.md` on the changed rules. Put each new defect to the user before you draft the replies.

Each later batch on the same pull request gets at least the check pass from `SKILL.md` step 8, however small its fix. This holds after the round cap too. A reviewer's next comment often lands on a fix that skipped it.

Done when: every group has a verdict, every decision is recorded, and the changed rules pass the red-team.

## Reply shapes

- `Updated in <sha>.` + the decision in one sentence + the rule IDs changed.
- `No change here.` + the reason (rule, convention, counter-example or owner).
- `New OQ-n asks this for <owner>.`
- One fix that answers several threads: the same reply in each thread.

Put `Thanks.` before the reply shape, and keep a neutral tone. When the owner is the reviewer's own role, ask for their view. Do not give the role as the reason. Link every ticket ID: GitHub does not turn Linear IDs into links.

Write replies under the writing rules in `SKILL.md`. A phrase the user asks for in one reply belongs to that reply only.

## Gate

Show the diff and every drafted reply. Push and post only after the user says so, for this batch.

After posting, check that each reply appears exactly once. A network error can post a reply and still report a failure, so look before you retry. Delete any duplicate reply.
