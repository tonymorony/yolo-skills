# Review replies

The branch for a spec that is already pushed and has reviewer comments.

## Triage

Read every comment, including threads GitHub collapses as outdated. Give each one verdict:

- **Sound**: the scenario holds against the spec text. Fix it or ask the user.
- **Tracked**: an Open Question already holds it. Reply with a pointer to that OQ.
- **Design**: a design detail. Reply that the wording or layout is the design's call, and note it for the designer.
- **Unsupported**: the proposal has no reason, or the reason fails. Reply with a counter-question.

A specific proposal is still a claim. Before recommending it, check its reasoning holds: "Why 20, rather than 15 or 30?" When it fails, the recommendation is the counter-question, kept polite and concrete, with an example that shows the gap.

A pushback needs evidence: a cited rule or format convention, the codebase's own word, a counter-example, or a named owner ("the fetch time is engineering's call"). A belief is not evidence.

## Decisions

For each comment that needs a decision, ask the user one comment at a time, with:

- the comment's direct link (`#discussion_r…`) and a quote, saying when the thread is collapsed as outdated;
- what the spec says now, in plain words, with a short example;
- the options, your recommendation first, with its reason.

The user decides product questions themselves; write the reply as the decision. Collect all decisions first, then edit (smallest change, ripple check from `SKILL.md` step 6), then draft every reply.

## Reply shapes

- `Updated in <sha>.` + the decision in one sentence + the rule IDs changed.
- `No change here.` + the reason (rule, convention, counter-example or owner).
- `New OQ-n asks this for <owner>.`
- One fix that answers several threads: the same reply in each thread.

Keep replies short and plain. A phrase the user asks for in one reply belongs to that reply only.

## Gate

Show the diff and every drafted reply. Push and post only after the user says so, for this batch.
