# Code and testing

## Read this when

Read before implementation, debugging, refactoring, or regression prevention.
Use the project toolchain rather than importing this repository's validation tools.

## Decisions before implementation

Identify rule ownership, boundaries, input/configuration sources, affected callers,
and observable acceptance criteria. Decide which behaviors need an actual database
or infrastructure boundary and which can be tested as isolated rules.

## Implementation guidance

DEFAULT: Prefer understandable functions, meaningful names, and modules that own
clear behavior. Remove unnecessary indirection rather than adding layers to match
an architectural slogan. Preserve public contracts while simplifying internals.
Verify by tracing a caller and reviewing the final diff. [S08](sources.md#s08)

REQUIRED: Validate untrusted input at boundaries. Where supported, represent valid
domain states in types. Avoid unchecked casts, suppressed errors, broad exception
swallowing, and silent fallbacks that hide a failed business effect. Validate required
configuration at an appropriate lifecycle boundary, and never embed credentials in
code or fixtures. Exercise invalid configuration and intentional errors.
[S08](sources.md#s08), [S24](sources.md#s24)

REQUIRED: Use the project's formatter, linter, compiler, and test conventions.
Do not disable checks or weaken assertions to make a build pass. Reproduce and
report pre-existing failures separately from introduced ones. Fix the actual cause
of a failing behavior instead of suppressing its error. [S08](sources.md#s08)

DEFAULT: Use unit tests for isolated rules and integration tests for database and
infrastructure behavior. If an assertion depends on production-engine constraints,
collation, isolation, queries, or migrations, use an isolated compatible engine and
configuration. A substitute database or mock does not prove that behavior. Never
interpret this as permission to test against live production data. [S39](sources.md#s39)

CONDITIONAL: Mock third-party boundaries for deterministic failure injection, then
verify their integration contracts through available safe mechanisms such as official
test environments or contract fixtures. Clearly identify what the mock cannot prove.
Do not call a live external mutation without appropriate authorization.
[S39](sources.md#s39)

REQUIRED: Cover important affected behavior and identified risks. Include relevant
negative authorization, tenant boundaries, malformed inputs, constraints, pagination,
duplicates, concurrency, and partial failure. Coordinate concurrent tests with barriers
or equivalent tools and bounded waits; arbitrary sleeps are unreliable. Assert
observable state and effects rather than private file layout. [S08](sources.md#s08)

## Proportionate verification

For a small change, inspect callers, read relevant references, check the specific
documentation, make a focused edit, and run targeted tests plus applicable project
checks. A short report is enough. Do not require unrelated architecture documents,
benchmarks, migration plans, or runbooks.

For a substantial feature, define its API contract, data model, authorization, and
failure cases before implementation. Connect all required layers. Include database
and authorization integration tests, resource/query bounds, and migration compatibility
notes where needed.

For high-risk behavior, require stronger evidence such as concurrent integration
tests, migration rehearsal, failure injection, or a reviewed recovery procedure.
Judge risk from permissions, data importance, concurrency, and deployment impact.
A one-line authorization edit can be riskier than a large internal refactor.

For greenfield work, verify application startup, configuration instructions, storage
initialization/migrations, connected endpoints or jobs, required authentication and
authorization, intentional errors, executable tests, and accurate local setup.
Do not add deployment services or infrastructure without requirements.

These are project workflow choices, not source-mandated modes or separate skills.

## Common mistakes

Avoid mocks that remove the very behavior being claimed, coverage quotas without
risk analysis, sequential "concurrency" tests, assertions of implementation wording,
disabled checks, unrelated refactors, and greenfield output containing only interfaces.

## Verification and exceptions

Execute checks and inspect their real output and stored effects. Compilation proves
neither authorization nor correct concurrency. State commands, results, unavailable
checks, and limitations. No arbitrary 100% coverage target is required. A test that
cannot run remains unverified; supply a reproducible next step rather than inventing
a pass or expanding the task into an unrelated tooling migration.
