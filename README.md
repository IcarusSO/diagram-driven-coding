# diagram-driven-coding

[English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

A skill for AI coding assistants. Each component folder carries its own `ARCHITECTURE.md` (class and sequence diagrams, responsibilities, data contracts) that is written first, combined with TDD and interface layering, so that an AI-written change stays inside a component boundary.

> Note: `SKILL.md` and the demo documents are written in English. The READMEs are available in three languages.

## What problem does it solve?

> Want to see the result first? [demo/ARCHITECTURE.md](demo/ARCHITECTURE.md) is the root component map; follow its links to the component and sub-component documents.

You ask an AI to change one feature and it also edits three unrelated files; fixing A breaks B; and after a mistake you still have to debug line by line.

This skill does not ask the AI to "be more careful". It leaves the AI no room to wander:

- **Clear boundaries**: one folder per component, exposed only through its interface; nobody outside touches private helpers.
- **Diagram first, then tests, then code**: the diagram is a map that both the AI and the human can read, and it is the focus of review.
- **Test public promises, not internal structure**: stops the AI from producing piles of structural tests that give a false sense of coverage.
- **Interface changes need human approval**: the AI first estimates whether the interface has users unrelated to the current work, then asks you whether to approve.
- **A broken class can be replaced wholesale**: all implementations share one set of behavioural contract tests.

More detail is in "Principles in detail" at the end.

## Contents

| Path | Content |
| --- | --- |
| `SKILL.md` | The skill itself, one file (core practice, optional advanced items, ARCHITECTURE.md template) |
| `demo/` | A small Python demo project (root, components and a sub-component each have an `ARCHITECTURE.md`) with three scenarios showing how the skill works; see `demo/DEMO.md`. For a quick look: [demo/ARCHITECTURE.md](demo/ARCHITECTURE.md) (root component map) → [demo/pricing/ARCHITECTURE.md](demo/pricing/ARCHITECTURE.md) (component) → [demo/pricing/rules/ARCHITECTURE.md](demo/pricing/rules/ARCHITECTURE.md) (sub-component) |

## How to use

- **Claude Code**: put `SKILL.md` at `.claude/skills/diagram-driven-coding/SKILL.md`.
- **ChatGPT / Codex**:
  - ChatGPT: if your account has Skills, upload it via Plugins → Skills → Create → Upload from your computer; otherwise paste `SKILL.md` into a Project's instructions or upload it as a file.
  - Codex: put it at `.agents/skills/diagram-driven-coding/SKILL.md` in your project (or in `~/.agents/skills/` to use it everywhere) and invoke it explicitly with `$diagram-driven-coding`. No separate `AGENTS.md` is needed.
- **Other AI tools**: put it in the tool's skills directory, or merge its content into the project's instruction file (for example `.cursorrules`).

Suited to medium or larger projects that AI will help maintain over a long time. Not for small scripts or one-off projects.

## Status

The core practice comes from long-term use in several real projects. The "advanced" part (automatic enforcement, commit hashes, tiered approval and so on) is not yet validated; treat it as suggestions.

## Run the demo tests

```bash
cd demo
python3 -m unittest discover -v
```

Requires Python 3.9 or later and no external dependencies.

## Run the type checkers (optional)

Signature compatibility of interfaces is enforced by type checkers (see the "signature compatibility" principle in the skill). The demo ships the config files:

```bash
pip install mypy pyright
cd demo
mypy       # reads mypy.ini (strict)
pyright    # reads pyrightconfig.json (standard)
```

Both should report 0 errors.

## Principles in detail

### Layered documentation

- **Root `ARCHITECTURE.md`**: only the component map (who depends on whom) and the main cross-component flows; no implementation details.
- **Component `ARCHITECTURE.md`**: one per component, with responsibilities, class and sequence diagrams, the data contract and what it is *not* responsible for.
- **Sub-components**: split out only when they meet the conditions for having an interface (used across folders, several replaceable implementations, or an external system). They get their own `ARCHITECTURE.md` and appear in the parent's diagram as a single participant. Keep depth to 2–3 levels.
- Examples: [root](demo/ARCHITECTURE.md), [component](demo/pricing/ARCHITECTURE.md), [sub-component](demo/pricing/rules/ARCHITECTURE.md).

### Spell out data shapes

- A return value with fixed keys uses a `TypedDict`, defined in the component's `data_types.py` and exported from `__init__.py`. No bare `dict` (you cannot tell what is inside), and no class wrapper just for packaging (hidden logic, awkward to use).
- A value drawn from a fixed set of strings uses `Literal` (for example `CustomerTier`).
- A DataFrame's columns and dtypes are a data contract: define the column list once, share it between the docs and the validation, and validate input and output at the component boundary (consider `pandera`).
- Every public function and class has a Google-style docstring (`Args:`, `Returns:`, `Raises:`, `Not responsible for:` and so on).

### Signature compatibility, enforced by type checkers

- Principle: an implementation's signature must be compatible with its interface: parameter names, order and kind match; types follow the type checker's rules (parameters may be wider, the return type may be narrower).
- Note that tools guarantee compatibility, not textual identity.
- Do not rely on the AI's good intentions; let tools block it: pyright or mypy for Python, `tsc --strict` for TypeScript, the compiler for Java and C#.
- The demo ships `demo/mypy.ini` and `demo/pyrightconfig.json`; see "Run the type checkers" above.

### Do DIP, but keep the interface clean (YAGNI)

- An implementation's constructor may take dependencies typed as interfaces, but those parameters are the component's internal business.
- Wiring lives in a factory function in the component's `__init__.py` (for example `default_pricer()`). Export only the interface, the `TypedDict`s and the factory; keep implementation classes out of `__all__` and agree that other folders use only the factory and the interface. Python does not enforce this; use a dependency checker if you need enforcement.
- Small internal classes without an interface (validation, subtotals and so on) are created by the implementation itself and need no injection.
- If the AI proposes new public parameters or exports an implementation class "in case we swap it later", it must name the concrete requirement; if it cannot, do not add it.
- In the demo: `demo/pricing/__init__.py` and `demo/pricing/standard_pricer.py`.

### Testing rules

- Test public promises (behaviour) and do not lock down internal structure. The check: if this test fails, would downstream really break? Import paths and keyword parameter names that downstream depends on count as contracts and can be tested.
- Implementations share one set of contract tests, so when a whole class is replaced the behavioural guarantees remain.

### Interface changes need human approval

- By default, every interface change needs approval.
- The AI first estimates whether other users unrelated to the current work exist (references from other folders), explains the impact, and asks you whether to approve.

### Taking over an existing project

- For a non-OOP project, do not rewrite everything at once: first add a thin caller to the existing code (minimal change) and write characterization tests to pin down current behaviour.
- Then write the core logic with OOP in a new folder, run it alongside the old logic (shadow run) to compare results, switch over when satisfied, and keep a way back.
- When the core logic is large, move it piece by piece, and show the parts not yet moved as a `<<legacy>>` participant in the root diagram.

### Honest reporting

- The AI must distinguish `PASSED`, `FAILED`, `NOT RUN` and `BLOCKED`, and must not present tests that were never run as passing.

### Advanced (optional, not yet validated)

Automatic enforcement, commit hashes, test plans and notebooks, tiered approval; see the "advanced" part of `SKILL.md`.

## Licence

MIT, see [LICENSE](LICENSE).
