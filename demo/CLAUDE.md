# AI instructions for the demo project

Work according to `../SKILL.md` (diagram-driven-coding), including section 4: name dict shapes with `TypedDict`, and give public items Google-style docstrings.

## Read the documents before changing anything

Read `ARCHITECTURE.md` (the component map) first, then the target component's own `ARCHITECTURE.md`. Sub-components (for example `pricing/rules`) have their own document. Read only what you need; do not scan the whole project.

## Approval settings for this project

These interface changes always need approval in advance: changes to a signature, a return value, a data structure, a unit, a meaning, a class responsibility or a cross-folder dependency, and changing or deleting a contract test.

Before changing an interface, search for and list the other users that are unrelated to the current work, report them to me together with the contract before and after, and wait for my approval before continuing.

## Running the tests

```bash
cd demo
python3 -m unittest discover -v
```
