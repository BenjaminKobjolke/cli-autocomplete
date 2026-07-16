# CLAUDE.md — cli-autocomplete-auto-tool

Interactive Windows CLI path autocomplete tool (`clicomplete.py` + `src/` modules,
`prompt_toolkit`). This file carries the XIDA coding rules that apply to this project.

## Coding Rules Source

Path: `D:\GIT\BenjaminKobjolke\claude-code\coding-rules`
(used by `/coding-rules:add-or-update` — reuse this path, don't re-ask)

Files applied: `COMMON_RULES.md` (full), `AI_RULES.md` (full, always applies),
`PYTHON_RULES.md` (applicable subset — see "Skipped Python rules" below).

---

# AI Workflow Rules (always apply)

These are language-independent and not subject to applicability filtering. Each step is an
existing skill referenced by its slash name; run the skill rather than reimplementing it.

## Feature / Change Workflow

After a plan is proposed and the user approves it, follow this chain. The DRY gate is a
precondition for implementing — not just an earlier step.

```
plan approved
  → /plan:dry            check approved plan for DRY/consolidation BEFORE code
  → /plan:dry-checked    reload + review the DRY-adjusted plan
  → /convention:check    scan for existing patterns/components to reuse
  ─────────────────────  DRY GATE — must be cleared to proceed
  → restate Definition-of-Done aloud
  → implement
  → /dry:check           post-implementation DRY audit (template below)
  → /verify:after-change run tests + code analysis
```

### DRY gate (precondition for implementing)

Do not write a single line until ALL are true. Restate this gate aloud at the moment you
start implementing — if you cannot, the gate is not cleared:

- [ ] `/plan:dry` ran and the plan was adjusted for any duplication found.
- [ ] `/plan:dry-checked` reloaded and confirmed the adjusted plan.
- [ ] `/convention:check` found the existing utilities/patterns to reuse.

The gate survives the `implement` step: if mid-implementation you add a new helper, type,
or pattern the gate would have caught, stop and re-clear it before continuing.

### Definition of Done — restate aloud before implementing

Before the first edit, state in chat what "done" means for THIS change:

- [ ] Scope: <one line — what changes, what does not>
- [ ] Reuse: <existing function/component this builds on, with path>
- [ ] DRY gate cleared (above)
- [ ] `/dry:check` clean
- [ ] `/verify:after-change` green (tests + analysis)

### Post-implementation DRY audit — paste-in template

Run `/dry:check`, then paste and fill:

```
DRY audit — <change name>
Changed files:     <list>
Duplication found: <none | describe>
Consolidated into: <shared fn/module + path | n/a>
Convention reused: <name + path>
Verdict:           <clean | needs rework>
```

## Bug-Fix Workflow

Bug fixes use a shorter variant (no plan-DRY phase):

```
bugs:fix
  → /verify:after-change
```

## Optional Addons

Optional addons live in `coding-rules/ai_rules_addons/` (e.g. graphify). They are opt-in
per project — ask the user before wiring one into this file. None are enabled here.

---

# Common Rules (all languages)

- **Keep CLAUDE.md in sync** — copy relevant rules from the coding-rules repo into this
  file; when it exists, compare, update, and deduplicate.
- **Use objects for related values** — bundle related parameters into a dedicated object
  (DTO/Settings/Config) instead of passing many parameters.
- **No bag-of-keys returns at module boundaries** — public methods on managers/
  repositories/services return typed objects (DTO, value object, domain model), never raw
  dicts indexed by string keys. `get_thing() -> Thing | None` (zero or one) vs
  `get_things() -> list[Thing]` — never overload one return to mean both. `None` = not
  found; empty collection = found but empty. JSON-decoded blobs crossing a boundary get
  wrapped in a value object too. Private, single-method dict juggling is fine.
- **Reuse existing models before inventing shapes** — search for an existing domain class
  that already owns the data before designing a new DTO or dict shape.
- **Tests pin the shape before the refactor** — when converting a dict return to a typed
  object, write a characterization test first, green before and after.
- **Test-Driven Development** — for features and bug fixes: write tests first, confirm
  they fail, implement, confirm they pass.
- **Integration tests** — every project includes integration tests alongside unit tests.
- **Test runner scripts** — `tools/run_tests.bat` (unit) and
  `tools/run_integration_tests.bat` (integration) are mandatory.
- **Prefer type-safe values** — typed DTOs, enums, typed settings over stringly typed
  values.
- **String constants** — centralize in a dedicated module/class; no raw strings scattered
  across the codebase.
- **Reusable tooling** — before building project-specific infra scripts, check
  `coding-rules/python_setup_files/` for an existing equivalent; if you build a new one,
  copy it back there and document it in `PYTHON_RULES.md`.
- **README.md is mandatory** — name/description, setup, usage, dependencies.
- **DRY** — extract repeated logic into reusable functions/modules; constants for
  repeated values.
- **Derive, don't duplicate** — when one value strictly determines another, pass only the
  determinant and derive the rest (cheap, pure, exhaustive mapping). Never thread two
  co-varying parameters side-by-side. Don't force it on genuinely independent values.
- **KISS / YAGNI** — simplest solution that works; no interface with one implementation,
  no factory for one product, no config for a value that never changes. Boring over
  clever; deletion over addition.
- **Confirm dependency versions** — before adding any package, confirm the version with
  the user; don't assume.
- **Error handling & logging strategy** — centralized error handler, structured logging
  (no `print`), levels debug/info/warning/error, context in messages.
- **Centralized logger — single off switch** — all logging goes through one logger class;
  built-in output calls appear in exactly one file (the logger implementation). Python:
  class `AppLogger` in `app_logger.py`. Callers pass a level; the logger decides emission
  from central config.
- **Input validation at boundaries** — validate user input, file content, and external
  data before processing; fail fast with clear errors.
- **Maximum file length — 300 lines** — split by domain when exceeded. Exceptions:
  generated files, config, repetitive test files.
- **Naming conventions** — files `snake_case`, classes `PascalCase`,
  functions/variables `snake_case` (Python), constants `UPPER_SNAKE_CASE`.
- **Comments explain why, not what** — document intent, workarounds, non-local
  constraints; module/class purpose at top; delete stale comments.
- **Security baseline** — never commit secrets; escape output; parameterized queries
  only; validate/sanitize input; keep dependencies updated.
- **No hardcoded environment values** — no filesystem paths, hostnames, IPs, ports, or
  URLs in code; read from central config with a committed `.example` template.
- **No god classes** — single responsibility; warning signs: >5 public methods, >4
  constructor dependencies, unrelated domains in one class. Complements the 300-line rule.
- **Self-describing classes** — when behavior depends on a class's fields (search,
  serialization, display, validation), the class declares those fields via a contract;
  never hardcode field lists in consumers.
- **Inject collaborators, don't fold dependencies in** — prefer constructor-injected
  collaborators over mixins/traits; never instantiate a service with a constructor call
  inside a method; collapse config-callback swarms into one value object.

---

# Python Rules (applicable subset)

Target standard is **uv + `pyproject.toml`** even though this project currently uses
venv + `requirements.txt` (see Known Deviations).

- **`pyproject.toml` is the single source of truth** — Python version pinned
  (e.g. `>=3.11,<3.13`), dependencies via `uv add`, `uv.lock` committed. Migrate this
  project with `/python:upgrade-to-uv`.
- **Formatting + linting + type checking** — `uv add --dev ruff mypy`. Ruff handles lint
  + formatting (replaces black/isort/flake8); mypy for typing. CI/checks run
  `ruff check`, `ruff format --check`, `mypy`.
- **Type hints on public APIs** — all public functions/classes/methods have typed
  parameters and return types. Use `Sequence`, `Mapping`, `Protocol`, `TypedDict`,
  `Literal` where helpful; avoid `Any` except at I/O or third-party boundaries.
- **Centralized env-driven settings** — one frozen `Settings` dataclass reading
  `os.getenv` in one place; nothing else touches `os.getenv` directly.
- **Tests: pytest, fast, isolated** — `uv add --dev pytest`; unit tests for core logic;
  no network in unit tests; tmp dirs/fixtures, no reliance on machine state.
- **`spec=` with MagicMock** — always `MagicMock(spec=RealClass)` so nonexistent
  attributes raise `AttributeError`. Mock methods as methods
  (`mock.get_body.return_value = ...`), not as fake attributes. Properties via
  `PropertyMock`.
- **Structured logging via `AppLogger`** — one class `AppLogger` in `app_logger.py`
  wrapping `logging`/`structlog`; feature code never calls `logging.getLogger(...)` or
  `print()` directly.
- **Required batch files** — `start.bat` (root, starts the app), `tools/run_tests.bat`.
- **Project setup scripts** — copy from
  `D:\GIT\BenjaminKobjolke\claude-code\coding-rules\python_setup_files`
  (`install.bat`, `update.bat`, `tools/run_tests.bat`).
- **Async patterns** — `asyncio` for I/O-bound work; no blocking calls (`time.sleep`,
  sync HTTP) inside async contexts.
- **Validation** — Pydantic for data validation at boundaries where warranted.
- **Self-describing classes (Python)** — `Protocol` with an abstract method for simple
  cases; dataclass `field(metadata=...)` for declarative per-field control.

## Skipped Python rules

Not applicable to this CLI project, intentionally omitted: template engine/Jinja2,
PySide6 GUI, localization (`python-localization`), SQLAlchemy ORM, release workflow.
Re-add via `/coding-rules:add-or-update` if the project grows those concerns.

---

# Known Deviations

None. Migrated to uv (`pyproject.toml` + `uv.lock`), logger is `AppLogger` in
`src/app_logger.py`, tests live in `tests/` (unit) + `tests/integration/`, batch files
`start.bat`, `auto.bat`, `install.bat`, `update.bat`, `tools/run_tests.bat`,
`tools/run_integration_tests.bat` are in place.
