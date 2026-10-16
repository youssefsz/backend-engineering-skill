# Evaluate backend engineering behavior

Static validation establishes package structure. These evaluations test selection
and engineering behavior. Neither establishes guaranteed correctness.

Start with E02 feature construction, E03 query efficiency, and E07 duplicate
execution in [engineering cases](engineering-cases.md). The other cases cover
additional risks. [Activation cases](activation-cases.md) separately test when
the skill loads, including frontend-only negative controls.

## Run a matched baseline

1. Create a disposable repository meeting a case's setup. Pin its runtime,
   dependencies, database configuration, seed data, and acceptance tests. Keep
   evaluator tests outside the agent's editable directory. Never use production.
2. Snapshot the starting repository. Create two independent copies with the same
   prompt, model, tools, permissions, and resource budgets. Clear conversation
   history. Record inherited instructions so the baseline is interpretable.
3. For the skill arm, copy the complete installable directory into the host's
   project skill location and use its documented loading instruction. For the
   baseline arm, omit both. Check for user/global skills that contaminate either
   arm. Check ancestor loading instructions, conversation history, previous output,
   and database state too. Use supported temporary configuration or a separately
   configured evaluation environment; do not remove the user's real configuration.
4. Run the prompt in each copy. Capture tool reads and edits where the host permits.
   Report description-only activation and activation with the documented loading
   instruction as separate configurations. Test explicit invocation separately.
   Explicit loading is acceptable when measuring implementation quality.
5. Define acceptance criteria before inspecting candidate output. Execute the same
   checks against both artifacts. Inspect persisted
   state, network stub effects, executed queries, and crash recovery as applicable.
6. Fill [the result record](results-template.md). Store raw outputs locally under
   ignored `evals/runs/`. Publish only sanitized, reviewable results if authorized.
7. Correct instructions only for demonstrated failures or measurable overhead.
   Rerun affected cases. Keep original results rather than rewriting failures.
   Change an assertion only when it is demonstrably wrong, brittle, or inconsistent
   with the intended behavior, and record the reason. Valid alternative modules or
   query strategies must not fail solely for differing from an expected layout.

The setup and checks in each case are the reproducible fixture contract. Record
the fixture revision to make an individual execution reproducible. This repository
does not bundle application templates or claim the scenarios ran merely because
they are specified here.

## Current evidence status

| Evidence category | Status |
| --- | --- |
| Static package validation | PASS locally on 2026-10-16; see the [validation record](validation-results.md) for commands and limits |
| Documented compatibility | Codex and Claude Code paths verified against official sources; generic integration is host-dependent |
| Manual activation | Not run in a fresh target-host session |
| Engineering evaluations | E01–E14 not run; no isolated evaluation runner or two-ecosystem fixture set has been established |
| Matched baseline | E02, E03, E07 not run with and without the skill |

Do not claim cross-language effectiveness until actual evaluations cover at least
two language ecosystems. SQL example checks and static linting do not satisfy
that requirement. Source basis: [S02](../skills/backend-engineering/references/sources.md#s02),
[S07](../skills/backend-engineering/references/sources.md#s07),
[S51](../skills/backend-engineering/references/sources.md#s51),
[S53](../skills/backend-engineering/references/sources.md#s53).

## Evidence requirements

Distinguish discoverability, actual loading, and implementation improvement. A
successful format check establishes none of those. Use these check states:

| State | Meaning |
| --- | --- |
| PASS | Executed evidence satisfies the criterion |
| FAIL | Execution showed incorrect behavior |
| NOT RUN | No execution occurred |
| BLOCKED | Attempted execution could not produce a valid result due to environment limits |
| NOT APPLICABLE | The check does not apply, with a recorded reason |

Do not count BLOCKED or NOT RUN as passes. Keep authorization bypasses and data
invariant failures visible regardless of any average score. Record runtime/database
versions, exact commands, supporting output, and limits in each result. Redact logs
before retaining or publishing them. Do not collect real credentials or private
application contents merely to improve a report.

For concurrency, use independent overlapping connections, controlled synchronization,
bounded waits, and useful timeout diagnostics. Record attempted requests, committed
effects, final stored values, and unexpected errors. For query counts, exclude setup,
count the measured endpoint consistently, state treatment of authorization/control
statements, compare more than one size, and use a fixture-specific budget. Also inspect
data volume and plans where relevant.

For pagination, test static data with equal sort values separately from changes
between requests. For retries, inject failures before operation, before commit,
after commit before response, before external publication, and after acceptance
before local completion as applicable. Inspect effects, not just response codes.
For performance, record dataset, request mix, concurrency, environment, and method.
Do not infer latency improvement from query counts or statistical significance from
one uncontrolled sample.

Review traces for wasted searches, unnecessary reference reads, unrequested documents,
speculative infrastructure, duplicated checks, and unrelated refactoring. Record
efficiency only when observable; do not invent timing or token counts. Prefer a
small instruction fix over a larger evaluation framework without demonstrated need.
