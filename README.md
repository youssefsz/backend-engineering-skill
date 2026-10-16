# Backend Engineering Skill

Build and extend backends with correctness, security, and failure handling considered from the first decision.

[![Validation](https://img.shields.io/github/actions/workflow/status/youssefsz/backend-engineering-skill/validate.yml?branch=main&style=flat-square&label=validation)](https://github.com/youssefsz/backend-engineering-skill/actions/workflows/validate.yml)
[![Latest release](https://img.shields.io/github/v/release/youssefsz/backend-engineering-skill?style=flat-square&color=2563eb)](https://github.com/youssefsz/backend-engineering-skill/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a?style=flat-square)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-standard-475569?style=flat-square)](https://agentskills.io/specification)

**[Download](https://github.com/youssefsz/backend-engineering-skill/releases/latest)** · **[Install](#install)** · **[References](#reference-library)** · **[Contribute](CONTRIBUTING.md)**

One portable, language-agnostic skill for AI coding agents. Use it to design new
backends, implement features, change databases, fix bugs, improve performance, and
review existing systems. It respects your project's stack and conventions.

> The installed skill is Markdown only. Using it requires no Python, uv, Node.js,
> database runtime, or shell. Repository-maintenance tools are separate.

## What it helps with

| Task | Guidance applied while building |
| --- | --- |
| New backends and features | Contracts, ownership, data flow, authorization, and connected implementation |
| Schemas and data access | Constraints, tenant isolation, bounded queries, pagination, and indexes |
| Concurrent work and integrations | Transactions, idempotency, retries, jobs, webhooks, and partial failure |
| Debugging and performance | Reproduction, actual query behavior, measurements, and targeted fixes |
| Refactoring and review | Compatibility, focused changes, meaningful tests, and evidence-backed findings |

The workflow starts with the affected code and requirements, loads relevant
references before decisions, checks version-specific official documentation, and
verifies real behavior. Small changes stay focused. Important data, permissions,
concurrency, and deployed migrations require stronger evidence.

## Install

### 1. Get the complete skill

Download the versioned `backend-engineering-vX.Y.Z.zip` from the
[latest release](https://github.com/youssefsz/backend-engineering-skill/releases/latest)
and extract it. The matching `.zip.sha256` file lets you verify the download.
Alternatively, use `skills/backend-engineering/` from a repository checkout.

```text
backend-engineering/
├── SKILL.md
├── references/
├── assets/
└── LICENSE
```

The ZIP contains only the installable skill. GitHub's automatic source archives
contain the entire repository, including maintenance tools and evaluations. A ZIP
is a distribution format; extracting it alone does not activate the skill.

### 2. Install for your agent

Copy the complete directory to one supported location, then follow the guide to
merge its loading instruction into your existing project or user instructions.

| Agent | Project location | Local user location | Guide |
| --- | --- | --- | --- |
| Codex | `.agents/skills/backend-engineering/` | `~/.agents/skills/backend-engineering/` | [Install and activate](integrations/codex.md) |
| Claude Code | `.claude/skills/backend-engineering/` | `~/.claude/skills/backend-engineering/` | [Install and activate](integrations/claude-code.md) |
| Other agents | Host-dependent | Host-dependent | [Connect another agent](integrations/generic-agent.md) |

Preserve existing instructions. The root [AGENTS.md](AGENTS.md) governs maintenance
of this repository; it is not the loading instruction to copy into your application.
Local user files may not be available in hosted sessions.

### 3. Check activation

Start a fresh session, confirm the skill is discoverable, and try a representative
backend task. Where traces are available, check that the agent reads `SKILL.md` and
relevant references before making the affected decisions. Explicit invocation helps
troubleshoot discovery but does not establish automatic activation.

Try requests such as:

- "Build the backend for a task management application."
- "Add workspace invitations using this application's existing stack."
- "Implement a paginated comments endpoint."
- "Fix duplicate orders when requests retry."
- "This endpoint gets slower as the database grows."
- "Inspect this backend without changing anything."

## Reference library

Load the references relevant to the task, rather than the whole library.

| Reference | Decisions it supports |
| --- | --- |
| [Architecture and design](skills/backend-engineering/references/architecture-and-design.md) | Boundaries, contracts, ownership, and feature construction |
| [Database design](skills/backend-engineering/references/database-design.md) | Invariants, relationships, types, and deletion |
| [Queries and indexes](skills/backend-engineering/references/queries-and-indexes.md) | Data access, pagination, query plans, and index tradeoffs |
| [Transactions and concurrency](skills/backend-engineering/references/transactions-and-concurrency.md) | Atomicity, races, locks, and transaction retries |
| [Migrations and recovery](skills/backend-engineering/references/migrations-and-recovery.md) | Compatible rollout, resumable backfills, and restoration |
| [API and security](skills/backend-engineering/references/api-and-security.md) | Trust boundaries, authorization, and external input |
| [Reliability and background jobs](skills/backend-engineering/references/reliability-and-background-jobs.md) | Jobs, remote calls, idempotency, and event publication |
| [Performance and observability](skills/backend-engineering/references/performance-and-observability.md) | Measurement, pools, caches, telemetry, and lifecycle |
| [Code and testing](skills/backend-engineering/references/code-and-testing.md) | Implementation, refactoring, and risk-focused verification |
| [Research policy](skills/backend-engineering/references/research-policy.md) | Focused, private, version-aware documentation checks |
| [Sources](skills/backend-engineering/references/sources.md) | 55 primary sources with review dates and applicability limits |

The optional [implementation checklist](skills/backend-engineering/assets/implementation-checklist.md)
and [verification report template](skills/backend-engineering/assets/verification-report-template.md)
can be used internally or in a response. They do not require creating extra files
inside every application.

## Update or remove

Review the [changelog](CHANGELOG.md), back up local modifications, and replace the
complete installed skill directory with the reviewed version. Retest discovery and
activation. To uninstall, remove only this skill's directory and loading paragraph,
preserving unrelated skills and instructions.

## Contribute and validate

Repository maintenance uses Python 3.11 or later, Git, and
[uv](https://docs.astral.sh/uv/getting-started/installation/). CI uses Python 3.12
and uv 0.9.26. From the repository root:

```sh
uv sync --locked
uv run --locked python scripts/validate.py
uv run --locked python -m unittest discover -s tests -v
uv run --locked python scripts/package.py
```

The development group in [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock)
manage this toolchain. The packager builds the versioned ZIP and checksum, extracts
it, and checks that all 15 files match the canonical skill and its local references.

Validation covers frontmatter, file structure, local links and anchors, casing,
source IDs, Markdown format, package boundaries, and release protections. It uses
PyYAML, markdown-it-py, PyMarkdown, and the pinned skills-ref format validator.
Format checks do not establish engineering effectiveness.
[S01](skills/backend-engineering/references/sources.md#s01)

Optional external reachability checks run separately from deterministic CI:

```sh
uv run --locked python scripts/check_external_links.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for proposing rules, changing dependencies,
and evaluating behavior. The [PR template](.github/pull_request_template.md) asks
what changed, why, and how it was verified.

## Releases

Push a prepared stable version tag such as `v0.1.0` to run the
[release workflow](.github/workflows/release.yml). It checks out that tag, runs the
locked checks and tests, and verifies matching versions and dated changelog
highlights before publishing the installable ZIP and checksum.

Release notes combine those highlights with GitHub-generated PR categories,
contributor details, and a full comparison when history permits.
[Categories](.github/release.yml) use PR labels and retain unmatched changes.
Follow the [release procedure](CONTRIBUTING.md#tag-a-release) before tagging.
Ordinary branches and PRs run read-only validation.

## Evidence and limits

[Validation evidence](evals/validation-results.md) records executed checks and their
limits. [Evaluation scenarios](evals/README.md) separately cover discovery,
activation, and engineering quality. Fresh host activation and matched engineering
baselines remain untested until recorded; CI badges do not claim otherwise.

The skill does not guarantee secure or correct output. Review important changes.
Instructions are not a security boundary; database constraints, tests, CI, and host
permissions provide independent controls. Database-specific guidance must match the
actual engine, version, configuration, and access path.

## License

Original repository material is available under the [MIT license](LICENSE).
External documentation keeps its own copyright and license. Guidance uses original
summaries with links to primary sources.
