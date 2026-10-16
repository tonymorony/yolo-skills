# Lenses

Five lenses, one subagent each. Every lens reads the same inputs and returns the same finding shape; only its question differs.

## Prompt

Send each subagent this, with `<lens>` replaced by one section below:

> You review a design pull request in `<owner>/<repo>` against the spec it builds. You find defects; you change no file.
>
> Inputs: the pinned spec `<spec.md>`, the ledger `<ledger.md>` (every spec row split into atoms, each with its Element, Reason and trace to `file:line`), the diff `<pr.diff>`, and the changed files in full at the head SHA under `<files/>`. Atoms marked not reviewed are outside this PR. Read lines from the files on disk with `grep -n`, `sed -n` or `awk`, never through `echo "$var"`.
>
> `<lens>`
>
> For each finding return: lens, atom ID, `file:line`, the spec's words (short quote), what the page does, the evidence a reader can check, and a suggested fix. Cite only what you opened in these files. When you find nothing, return "nothing found" and the atom IDs you checked. Return everything as your final message. The repo's own markup and coding conventions belong to another review; leave them out.

## Letter

Does each traced element meet its atoms word for word?

- Text, labels, order, presence. Formats: the currency code, the rounding, the unit, the period and the basis.
- Atoms of absence ("no action", "no P90", "no margin"): search the whole element for the absent thing, including hover readouts, `aria-label`s, comments and `data-*` attributes.
- Links and controls reach the destination the atom names.
- An `aria-label` says what the visible text says.

## Reason

For each traced atom with a Reason: can a reader of the page reach what the Reason protects against by another route?

- A count recovered from bar heights and a stated group size; an extreme from the axis extent; one person from a combination of shown facts; a tie from a rounded rank and the group size; precision implied by the digits shown.
- Name the page fact that opens the route and the spec sentence it defeats.
- When the letter holds and the Reason fails, give both cures, one in the design and one in the spec, and leave the choice to the owner.

## Figures

Recompute every figure the page derives from other drawn data, with `python3 -I -c`, and show each computation beside the drawn value.

- Sums against stated totals, counts against the group size, "N more" against a threshold.
- Percentiles and ranks by the spec's formula and its tie rule; check that each drawn value can occur at all for the stated size.
- Positions on a scale: value to coordinate, and back.
- Rounding and currency conversion by the spec's rules.
- Every sample state the page offers, not only the default one.
- A spec worked example gives expected values. When the page reuses a spec figure, check that the rest of the drawing agrees with it.

## Ripple

The PR changes a rule, a guide sentence, a token, an icon or a component. What else in the repo now contradicts that change, or the atoms it implements, while the PR neither changes it nor notes it as deferred?

- Search the component library, every screen or prototype, any gallery or index of states, and the paired rule change, for the old wording, the old rule name, the old icon.
- Check the elements the screen will use, from the trace, against the spec even where the diff does not touch them.

## Claims

Is everything the PR says about itself true in the diff? Leave conformance to Letter and arithmetic to Figures.

- Each claim in the PR body, the commit messages and the changelog entries ("follows BR-14", "now in step", "answers OQ-21", "unchanged") is visible in the diff.
- Each open question the PR answers, or builds on, is named for the spec owner.
- Name every unsourced element and every gap from the trace.
