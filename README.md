# yolo-skills

Personal agent skills for Claude Code.

| Skill | What it does |
|---|---|
| [`bulletproof-specs`](skills/bulletproof-specs/SKILL.md) | Writes or hardens a product spec until an adversarial reviewer finds nothing: ground, grid, draft, red-team, grill, apply, repeat, gate. Nothing is pushed before the gate. |
| [`spec-review`](skills/spec-review/SKILL.md) | Reviews a design pull request against the spec it builds: splits the spec into atoms, traces them to the page, runs five lenses (Letter, Reason, Figures, Ripple, Claims), reproduces each finding, and posts one GitHub review only after the gate. |

## Install

```sh
git clone git@github.com:tonymorony/yolo-skills.git ~/devel/yolo-skills
ln -s ~/devel/yolo-skills/skills/bulletproof-specs ~/.claude/skills/bulletproof-specs
ln -s ~/devel/yolo-skills/skills/spec-review ~/.claude/skills/spec-review
```

## Sources

- The structure follows Matt Pocock's [`writing-for-agents`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) (steps with completion criteria, disclosed reference, leading words).
- The lenses in `spec-review` come from a review of six design pull requests against one spec. `atoms.py` reads specs with BR, EC and OQ tables, and prose specs.
- `bulletproof-specs/spec_lint.py` checks a spec for duplicate and dangling IDs, line-number code citations, missing paths and, in a stack, IDs that a higher slice already uses.
- The defect classes in `DEFECTS.md` come from the reviewer comments on two real spec pull requests, about 160 comments in total.
