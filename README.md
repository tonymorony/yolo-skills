# yolo-skills

Personal agent skills for Claude Code.

| Skill | What it does |
|---|---|
| [`bulletproof-specs`](skills/bulletproof-specs/SKILL.md) | Writes or hardens a product spec until an adversarial reviewer finds nothing: ground, grid, draft, red-team, grill, apply, repeat, gate. Nothing is pushed before the gate. |

## Install

```sh
git clone git@github.com:tonymorony/yolo-skills.git ~/devel/yolo-skills
ln -s ~/devel/yolo-skills/skills/bulletproof-specs ~/.claude/skills/bulletproof-specs
```

## Sources

- The structure follows Matt Pocock's [`writing-for-agents`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) (steps with completion criteria, disclosed reference, leading words).
- The defect classes in `DEFECTS.md` come from the reviewer comments on two real spec pull requests, about 160 comments in total.
