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
- Shape: "'Band' means a stretch of the chart, then the precision the cohort allows, in the same sentence." / "'Role' already means member, consultant or principal." / "'Total compensation' means pay as paid in one panel and adjusted pay in another."

## Formula

A computed figure lacks its formula, base, tie rule, method, rounding or cap; or a number appears with no reason.

- Check: does a worked example with real numbers reproduce each figure? For each threshold, cap, window or floor: why this value and not half or double? What can the data actually resolve at the smallest group size? Does each comparison use one basis on both sides: as paid or adjusted (for example, annualised), gross or net, one currency, one date?
- Shape: "Which base does a months-of-base bonus multiply?" / "The part reads '50% below median': the member's amount is as paid, but the median uses adjusted amounts." / "With 34 members, neighbouring totals are 3 percentile points apart, so 'a couple of points' is finer than the cohort resolves."

## Inference leak

A figure lets a curious or hostile user derive one person's data: at the smallest allowed group, by comparing views over time, by editing their own data repeatedly, or by combining fields that each look anonymous.

- Check: take the smallest group the rules allow and a user who knows one peer or controls their own entries. What can they compute? Does an "anonymised" row still name one person?
- Shape: "In a cohort of ten, P90 is the ninth-highest total; a member who knows the top earner learns the next one's pay to within a few thousand." / "Job title + company + city still names one person."

## Design mismatch

The spec and the current design disagree: an element with no rule, a rule with no element, a label in different words.

- Check: walk every element of every frame. Does each map to a rule? Does each rule have an element? Do the labels match the spec's words? Record the spec as the decision; list design changes for the designer.
- Shape: "The design draws one column per pay band with a count above it; the spec says nothing of counts."

## Plain words

A sentence breaks the writing rules in `SKILL.md`: over 20 words, more than one idea, passive voice, an idiom or metaphor, a judgement word ("simple", "clean", "obviously"), or a synonym for a word used earlier.

- Check: does each sentence give one idea in 20 words or fewer, in the active voice? Does each idea keep one word throughout? Does each rule cell hold one constraint?
- Shape: "The threshold, which is optional and only shown when the member is open, is cleared if the status is later changed to not looking, keeping data clean." (one sentence, four ideas, a judgement word)

## Ripple

An edit changed a rule, term or number, and another rule, edge case, open question or sibling spec still says the old thing.

- Check: after each edit, search the whole repository for each touched ID, term, alias and number. Include the specs, glossary, agent context, app copy and plans. Does every hit agree? Does a sentence the edit extended still agree with its own start? Then list every row that cites each changed rule, and every row the changed rule cites. Does each row still agree with the new meaning, also where it shares no word with the edit?
- Shape: "OQ-16 still says 'no package is left out', but BR-17 now leaves one out." / "EC-2 still says 'the next time Home loads'." / "The compensation spec's OQ-13 still gives the old formula." / "The glossary drops 'Firm principal' as an alias, but compensation BR-1 still uses it." / "The follow-up pull request still says 'pointing those lines here is a follow-up'."

## Code claim

A statement about current behaviour, limits, callers, cited rule numbers or cited tickets that nobody checked at its source.

- Check: did you open the code for each claim about the existing system, and the ticket or spec for each ID you cite? Cite `file:line` or the ID's title in the ledger. Does a resolved open question in a sibling spec, or a decision on a ticket, already decide the point? Does a rule that records a decision keep its nouns and qualifiers?
- Shape: "Only one policy calls that predicate." / "The ticket decided to leave out a package with a no-rate amount in its total; the rule leaves out any no-rate amount, allowances included." / "The rule treats 20 days as a full month; the field accepts 23."

## Convention override

A rule asks for a mechanism that the project's conventions do otherwise, and the spec does not say so. A builder who copies the closest sibling follows the convention and breaks the rule.

- Check: for each mechanism a rule asks for (deletion, caching, headers, storage), what does the conventions file say? Where they differ, does the rationale name the override, and does the build ticket draft carry the exception?
- Shape: "The rule hard-deletes a record; the conventions soft-delete every record a user can see." / "The rule keeps a page out of the client page cache; the conventions cache every page of that kind."

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

- Check: is each rule owned by exactly one spec? Does every operation (view, add, update, remove) appear in a story? Does every deferral name its owner or ticket? Does a rule that hands a case to a ticket also have an open Open Question row with **Blocks** and **Until then**?
- Shape: "The picker is written in two specs." / "BR-34 says 'WEB-246 settles what they see', and no Open Question gives a state until then." / "A backlog cut story by story leaves removing a pick in no ticket." / "The glossary restates the conditions of BR-24 and misses a later change to them."
