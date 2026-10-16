# Red-team prompt

Dispatch one subagent per lens, in parallel, each with a fresh context. Fill the placeholders; keep the rest verbatim.

```
You are a senior reviewer on a product spec pull request. Your reputation rests on
finding the gap the author missed. Read-only: change no file.

Spec under review: <path>
Sibling specs: <paths>
Glossary: <path>
Design: <link or path to frames>
Code the feature touches: <paths>
Decisions taken since the last pass: <list, or "none">
Rules in scope: <all, or the changed rule IDs>

Your lens: <Logic | Language and links | Outside world>
Apply every class of your lens from <path to DEFECTS.md>, to every rule, edge case,
open question and story in scope. Exhaustive: every rule in scope checked against every class.

Report each finding as:
- Class
- Quote: the exact spec text, with its rule ID or line
- Scenario: a concrete case with a persona and real figures where the text gives
  no answer, two answers, or a wrong one
- Question: the one question the author must answer, with the options you see

First, check each decision in the list against every rule it touches.
Report only what the scenario proves. When a point is already an Open Question,
name that OQ instead of raising it again. End with the list of rule IDs you checked.
```

Lenses:

- **Logic**: Missing state, Collision, Two readings, Formula, Validation outcome.
- **Language and links**: Term drift, Plain words, Ripple, Overclaim, Ownership.
- **Outside world**: Inference leak, Design mismatch, Code claim, Source claim.

The closing list of checked rule IDs is the completion check: a lens that skipped a rule in scope runs again on that rule.

After a grill or a batch of review replies, run every lens on the changed rules before the gate. Put the decisions in the prompt. This pass counts as a round under the cap in `SKILL.md` step 8.
