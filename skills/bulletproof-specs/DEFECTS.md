# Defect classes

The classes reviewers raised on real spec pull requests, largest first. Each has its leading word, what it looks like, the self-check that catches it, and an example of the shape.

## Missing state

A rule set gives no outcome for one combination of inputs, or for a gap in time. The largest class by far.

- Check: list every input of each rule, including absent, zero, stale and not yet computed. Does every combination have a stated outcome? What does the user see between an event and the next refresh?
- Shape: "With no package and no headline position at all, does the panel show four empty parts or disappear?"

## Collision

Two rules replace, hide or reorder the same element and can both be true at once, with no precedence.

- Check: for each pair of rules that act on the same element, can both apply? Which wins, and does the text say so?
- Shape: "Rule 2 says no field is mandatory; the field table marks three as required. Which does an engineer validate?"

## Two readings

A phrase reads two ways: a time window, a quantifier (none, each, all, once), "replaces", "after".

- Check: write the boundary case for each window and quantifier. Does the text give exactly one result on a named date?
- Shape: "'The last 12 months' — twelve months ending with this one, or this month plus the twelve before it?" / "'none carries any of the three' or 'none carries all three'?"

## Term drift

One word for two ideas, a synonym for a glossary term, a word used before it is defined, or a word that differs from the label users see elsewhere in the product.

- Check: is each domain noun in the glossary, defined before first use, used with one meaning, and the same as the visible labels in the rest of the product and the codebase?
- Shape: "'Band' means a stretch of the chart, then the precision the cohort allows, in the same sentence." / "'Role' already means member, consultant or principal."

## Formula

A computed figure lacks its formula, base, tie rule, method, rounding or cap; or a number appears with no reason.

- Check: does a worked example with real numbers reproduce each figure? For each threshold, cap, window or floor: why this value and not half or double? What can the data actually resolve at the smallest group size?
- Shape: "Which base does a months-of-base bonus multiply?" / "With 34 members, neighbouring totals are 3 percentile points apart, so 'a couple of points' is finer than the cohort resolves."

## Inference leak

A figure lets a curious or hostile user derive one person's data: at the smallest allowed group, by comparing views over time, by editing their own data repeatedly, or by combining fields that each look anonymous.

- Check: take the smallest group the rules allow and a user who knows one peer or controls their own entries. What can they compute? Does an "anonymised" row still name one person?
- Shape: "In a cohort of ten, P90 is the ninth-highest total; a member who knows the top earner learns the next one's pay to within a few thousand." / "Job title + company + city still names one person."

## Design mismatch

The spec and the current design disagree: an element with no rule, a rule with no element, a label in different words.

- Check: walk every element of every frame. Does each map to a rule? Does each rule have an element? Do the labels match the spec's words? Record the spec as the decision; list design changes for the designer.
- Shape: "The design draws one column per pay band with a count above it; the spec says nothing of counts."

## Ripple

An edit changed a rule, term or number, and another rule, edge case, open question or sibling spec still says the old thing.

- Check: after each edit, search this spec and every sibling spec for each touched ID, term and number. Does every hit agree?
- Shape: "EC-2 still says 'the next time Home loads'." / "The compensation spec's OQ-13 still gives the old formula."

## Code claim

A statement about current behaviour, limits, callers or cited rule numbers that nobody checked in the code.

- Check: did you open the code for each claim about the existing system? Cite `file:line` in the ledger.
- Shape: "Only one policy calls that predicate." / "The rule treats 20 days as a full month; the field accepts 23."

## Source claim

An external provider, standard or fixed list is assumed to cover what the spec needs.

- Check: what does the source really cover, when does it update, what happens on its failure days, and what happens to stored values when the list changes?
- Shape: "That provider covers about 30 currencies." / "The language standard has one code for Chinese." / "No rates are published on weekends."

## Overclaim

A rationale says "because", "always", "cannot" or "can fix it themselves", and one allowed case makes it false.

- Check: is each rationale true for every case the rules allow?
- Shape: "'The member can fix each of these', which is false for a member who knows only their net pay."

## Validation outcome

A refused input with no statement of what is saved, what is not saved, and where the error shows.

- Check: for each refusal, does the spec state the saved state and the message location?
- Shape: "Does the rest of the position save with that one field left empty?"

## Ownership

A rule owned by two specs (copies that drift), an operation in no story, a deferral with no owner, a first-build list that misses a part.

- Check: is each rule owned by exactly one spec? Does every operation (view, add, update, remove) appear in a story? Does every deferral name its owner or ticket?
- Shape: "The picker is written in two specs." / "A backlog cut story by story leaves removing a pick in no ticket."
