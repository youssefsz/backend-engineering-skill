# Sources

## Read this when

Use this registry to inspect the authority and limits behind guidance or to maintain
source-backed rules. The individual references route to specific entries.

## Decisions and interpretation

Match the rule to the engine, version, configuration, and workload before applying
it. These sources support original summaries, not copied manuals. Workflow sizes,
policy categories, filenames, and evaluation fixtures are project design decisions.
External material retains its own license; the repository MIT license covers its
original material. No source guarantees the generated backend is correct.

## Verification method and exceptions

Last content review date below means the page was fetched with certificate validation
and relevant content inspected on 2026-10-16. It is not an automated promise of future
freshness or installed-version compatibility. All listed URLs returned HTTP 200 during
that review. S03/S04 and S32/S35 redirected as noted. Check the actual project's version
again during a task. Reachability-only checks do not update content-review dates.

## Common mistakes

Do not treat PostgreSQL as every database, EF Core as required, HikariCP pool formulas
as universal, GitLab helpers as portable commands, or AWS advice as a hosting mandate.
Resolve disagreements by applicability and evidence rather than merging incompatible
claims. Source checks and engineering evaluations are separate evidence.

## S01

- Publisher and page: [Agent Skills: Agent Skills specification](https://agentskills.io/specification).
- Supports: Frontmatter, naming, progressive disclosure, validation.
- Applicability and limits: Format requirements; the 150–250-line target is this project's choice.
- Last content verification: 2026-10-16.

## S02

- Publisher and page: [Agent Skills: Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices).
- Supports: Focused instructions, conditional references, evidence-led iteration.
- Applicability and limits: Authoring advice, not proof that this skill improves outcomes.
- Last content verification: 2026-10-16.

## S03

- Publisher and page: [OpenAI: building skills and local discovery](https://developers.openai.com/codex/skills).
- Supports: Codex project/user skill discovery and explicit/implicit invocation.
- Applicability and limits: Original URL redirects to ChatGPT Learn build-skills. Host/version settings can affect discovery.
- Last content verification: 2026-10-16.

## S04

- Publisher and page: [OpenAI: AGENTS.md instructions](https://developers.openai.com/codex/guides/agents-md).
- Supports: Layered project instructions and Codex-home instruction files.
- Applicability and limits: Original URL redirects to ChatGPT Learn agents-md. Overrides and size limits can affect loading.
- Last content verification: 2026-10-16.

## S05

- Publisher and page: [Anthropic: skills](https://code.claude.com/docs/en/skills).
- Supports: Claude Code skill paths, description activation, slash invocation.
- Applicability and limits: Claude Code host behavior; local personal skills do not automatically reach cloud sessions.
- Last content verification: 2026-10-16.

## S06

- Publisher and page: [Anthropic: persistent project instructions](https://code.claude.com/docs/en/memory).
- Supports: CLAUDE.md instruction scope and version-dependent AGENTS.md support.
- Applicability and limits: AGENTS.md direct support requires v2.1.277 or later and applicable settings/session support.
- Last content verification: 2026-10-16.

## S07

- Publisher and page: [Anthropic: skill authoring and evaluation practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- Supports: Evaluate before expanding, concise body, reference organization.
- Applicability and limits: Claude-focused authoring examples; not universal host behavior.
- Last content verification: 2026-10-16.

## S08

- Publisher and page: [Google: code review considerations](https://google.github.io/eng-practices/review/reviewer/looking-for.html).
- Supports: Design, simplicity, ownership, tests, understandable changes.
- Applicability and limits: Code-review considerations generalized to construction, not a mandatory architecture.
- Last content verification: 2026-10-16.

## S09

- Publisher and page: [PostgreSQL Global Development Group: constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).
- Supports: Keys, unique/foreign/check constraints, nullability, deletion.
- Applicability and limits: PostgreSQL current documentation only; other engines/configurations can differ.
- Last content verification: 2026-10-16.

## S10

- Publisher and page: [PostgreSQL Global Development Group: numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html).
- Supports: Exact numeric representation, rounding, overflow tradeoffs.
- Applicability and limits: PostgreSQL numeric semantics; choose application arithmetic deliberately too.
- Last content verification: 2026-10-16.

## S11

- Publisher and page: [PostgreSQL Global Development Group: date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html).
- Supports: Dates, timestamps, instant and timezone semantics.
- Applicability and limits: PostgreSQL type behavior; timestamp-with-zone does not retain the original zone name.
- Last content verification: 2026-10-16.

## S12

- Publisher and page: [MongoDB: atomicity and transactions](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/).
- Supports: Single-document atomicity and multi-document transaction boundaries.
- Applicability and limits: MongoDB storage/deployment semantics; not a claim about every document database.
- Last content verification: 2026-10-16.

## S13

- Publisher and page: [PostgreSQL Global Development Group: indexes](https://www.postgresql.org/docs/current/indexes.html).
- Supports: Index overhead, types, and workload-driven design.
- Applicability and limits: Index chapter links to engine-specific features; no universal column-order formula.
- Last content verification: 2026-10-16.

## S14

- Publisher and page: [PostgreSQL Global Development Group: interpreting query plans](https://www.postgresql.org/docs/current/using-explain.html).
- Supports: Plans, estimated/actual work, scans, joins, loops.
- Applicability and limits: PostgreSQL plan interpretation; costs are not directly elapsed milliseconds.
- Last content verification: 2026-10-16.

## S15

- Publisher and page: [PostgreSQL Global Development Group: EXPLAIN execution behavior](https://www.postgresql.org/docs/current/sql-explain.html).
- Supports: EXPLAIN options and execution with ANALYZE.
- Applicability and limits: ANALYZE runs the statement; rollback is not permission or universal side-effect protection.
- Last content verification: 2026-10-16.

## S16

- Publisher and page: [Microsoft: efficient querying](https://learn.microsoft.com/en-us/ef/core/performance/efficient-querying).
- Supports: Projection, result bounds, round trips, N+1, join multiplication.
- Applicability and limits: EF Core examples illustrate query principles; EF Core is not required.
- Last content verification: 2026-10-16.

## S17

- Publisher and page: [Microsoft: pagination](https://learn.microsoft.com/en-us/ef/core/querying/pagination).
- Supports: Fully unique ordering, keyset/offset tradeoffs.
- Applicability and limits: EF Core examples; database ordering/types still need actual-engine verification.
- Last content verification: 2026-10-16.

## S18

- Publisher and page: [SQLite maintainers: many small queries](https://www.sqlite.org/np1queryprob.html).
- Supports: Many local queries avoid client/server network overhead.
- Applicability and limits: Local in-process access only; not a blanket efficiency guarantee or remote-service exception.
- Last content verification: 2026-10-16.

## S19

- Publisher and page: [PostgreSQL Global Development Group: transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html).
- Supports: Isolation, anomalies, conditional updates, transaction retries.
- Applicability and limits: PostgreSQL current isolation behavior; names alone do not establish other engines' guarantees.
- Last content verification: 2026-10-16.

## S20

- Publisher and page: [PostgreSQL Global Development Group: locking and deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html).
- Supports: Lock scope, ordering, waits, deadlock handling.
- Applicability and limits: PostgreSQL locks; other engines and managed services need their own documentation.
- Last content verification: 2026-10-16.

## S21

- Publisher and page: [GitLab: avoiding downtime in migrations](https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/).
- Supports: Compatible staged schema changes during deployed version overlap.
- Applicability and limits: Rails/GitLab-specific helpers and release counts are not prescribed here.
- Last content verification: 2026-10-16.

## S22

- Publisher and page: [GitLab: batched background migrations](https://docs.gitlab.com/development/database/batched_background_migrations/).
- Supports: Batched, retry-safe, resumable data changes.
- Applicability and limits: GitLab framework details do not define universal migration commands.
- Last content verification: 2026-10-16.

## S23

- Publisher and page: [AWS: verifying backups through recovery](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_backing_up_data_periodic_recovery_testing_data.html).
- Supports: Recovery rehearsal, backup integrity, loss/time objectives.
- Applicability and limits: General recovery lessons; no AWS hosting requirement or recovery-time guarantee.
- Last content verification: 2026-10-16.

## S24

- Publisher and page: [OWASP: authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).
- Supports: Default deny, object/action permission checks, negative tests.
- Applicability and limits: Authorization guidance; actual roles and public access follow product requirements.
- Last content verification: 2026-10-16.

## S25

- Publisher and page: [OWASP: SQL injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).
- Supports: Parameterized values and safe construction of dynamic SQL.
- Applicability and limits: Query builders and ORMs still need safe identifier/operator handling.
- Last content verification: 2026-10-16.

## S26

- Publisher and page: [OWASP: REST security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html).
- Supports: HTTP API boundary validation, tokens, errors, CORS, resource controls.
- Applicability and limits: HTTP examples do not require REST or a particular authentication protocol.
- Last content verification: 2026-10-16.

## S27

- Publisher and page: [OWASP: unrestricted resource consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/).
- Supports: Bound externally controlled work, batches, cost, and rates.
- Applicability and limits: API Security Top 10 2023 risk description; choose deployment-specific budgets.
- Last content verification: 2026-10-16.

## S28

- Publisher and page: [OWASP: password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).
- Supports: Established password hashing and parameter selection.
- Applicability and limits: Living security guidance; do not freeze algorithm parameters into forever-current rules.
- Last content verification: 2026-10-16.

## S29

- Publisher and page: [OWASP: session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).
- Supports: Session lifecycle, cookies, expiration, revocation considerations.
- Applicability and limits: Apply to the actual browser/credential model and framework version.
- Last content verification: 2026-10-16.

## S30

- Publisher and page: [OWASP: SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).
- Supports: SSRF destination, redirect, resolution, and network protections.
- Applicability and limits: URL filtering alone is insufficient; verify the actual resolver and connection path.
- Last content verification: 2026-10-16.

## S31

- Publisher and page: [OWASP: file uploads](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html).
- Supports: Untrusted file validation, naming, size, storage permissions.
- Applicability and limits: Only applies when uploads exist; scanners and isolation depend on requirements.
- Last content verification: 2026-10-16.

## S32

- Publisher and page: [AWS: timeouts, retries, backoff, and jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/).
- Supports: Remote timeouts, retry budgets, backoff, jitter, ambiguous effects.
- Applicability and limits: Original Builders Library URL redirects to AWS Builder Center; operational lessons do not require AWS.
- Last content verification: 2026-10-16.

## S33

- Publisher and page: [AWS: idempotent mutations](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_prevent_interaction_failure_idempotent.html).
- Supports: Scoped identity and safe retryable mutations.
- Applicability and limits: AWS examples; actual provider idempotency semantics still require verification.
- Last content verification: 2026-10-16.

## S34

- Publisher and page: [AWS: transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).
- Supports: Atomic publication intent, dual-write gap, duplicate-tolerant consumption.
- Applicability and limits: Transactional outbox is conditional; its presence does not ensure exactly-once delivery.
- Last content verification: 2026-10-16.

## S35

- Publisher and page: [AWS: caching challenges](https://aws.amazon.com/builders-library/caching-challenges-and-strategies/).
- Supports: Staleness, stampedes, cache dependence and outage behavior.
- Applicability and limits: Original Builders Library URL redirects to AWS Builder Center; no mandated cache product.
- Last content verification: 2026-10-16.

## S36

- Publisher and page: [HikariCP maintainers: connection-pool sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing).
- Supports: Connection-pool sizing and contention tradeoffs.
- Applicability and limits: JDBC/HikariCP examples and formulas are not universal settings for every driver.
- Last content verification: 2026-10-16.

## S37

- Publisher and page: [Google SRE: monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/).
- Supports: Latency, traffic, errors, saturation and actionable monitoring.
- Applicability and limits: Distributed-service operational experience; no universal latency target or required stack.
- Last content verification: 2026-10-16.

## S38

- Publisher and page: [OWASP: logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
- Supports: Useful structured security events and sensitive-data redaction.
- Applicability and limits: Logging does not authorize collecting secrets or arbitrary customer payloads.
- Last content verification: 2026-10-16.

## S39

- Publisher and page: [Microsoft: database testing strategies](https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy).
- Supports: Test doubles versus real database behavior and integration strategy.
- Applicability and limits: Use isolated compatible engines, not live production. EF Core-specific examples are optional.
- Last content verification: 2026-10-16.

## S40

- Publisher and page: [OWASP: prompt injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).
- Supports: Retrieved instructions as untrusted content and layered defenses.
- Applicability and limits: Prompt-injection advice does not establish a complete defense or override host permissions.
- Last content verification: 2026-10-16.

## S41

- Publisher and page: [GitHub: secure use of Actions](https://docs.github.com/en/actions/reference/security/secure-use).
- Supports: Minimal workflow permissions, immutable action pins, untrusted PR isolation.
- Applicability and limits: GitHub Actions-specific guidance; package validation is separate from publication.
- Last content verification: 2026-10-16.

## S42

- Publisher and page: [IETF: HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
- Supports: HTTP methods, safe/idempotent semantics, status and caching contracts.
- Applicability and limits: RFC 9110, June 2022; applies to HTTP interfaces, not every backend protocol.
- Last content verification: 2026-10-16.

## S43

- Publisher and page: [OpenTelemetry maintainers: telemetry signals](https://opentelemetry.io/docs/concepts/signals/).
- Supports: Telemetry signals and correlation concepts.
- Applicability and limits: Concepts only; keep the project's existing tools unless change is justified.
- Last content verification: 2026-10-16.

## S44

- Publisher and page: [PostgreSQL Global Development Group: routine vacuuming and maintenance](https://www.postgresql.org/docs/current/routine-vacuuming.html).
- Supports: Vacuum, statistics, storage and maintenance behavior.
- Applicability and limits: PostgreSQL only; never copy maintenance commands into other engines.
- Last content verification: 2026-10-16.

## S45

- Publisher and page: [SQLite maintainers: foreign-key enforcement](https://www.sqlite.org/foreignkeys.html).
- Supports: Connection-level foreign-key enforcement and configuration.
- Applicability and limits: Verify actual build/runtime and PRAGMA state; DDL presence alone is not enforcement evidence.
- Last content verification: 2026-10-16.

## S46

- Publisher and page: [SQLite maintainers: write-ahead logging](https://www.sqlite.org/wal.html).
- Supports: WAL read/write interaction and checkpoint behavior.
- Applicability and limits: SQLite WAL only, with version/environment constraints. No universal maintenance recipe.
- Last content verification: 2026-10-16.

## S47

- Publisher and page: [AWS: read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html).
- Supports: Read replica asynchronous propagation and engine differences.
- Applicability and limits: Amazon RDS topology; not every replica implementation. Check read-after-write requirements.
- Last content verification: 2026-10-16.

## S48

- Publisher and page: [Prometheus maintainers: metric labels and cardinality](https://prometheus.io/docs/practices/naming/).
- Supports: Bounded label cardinality and naming.
- Applicability and limits: Prometheus guidance; the underlying cardinality cost applies to many systems, not every API identically.
- Last content verification: 2026-10-16.

## S49

- Publisher and page: [OWASP: webhook security](https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html).
- Supports: Webhook authenticity, raw payload, replay/duplicate risks.
- Applicability and limits: Provider-specific authentication and ordering still need their official contract.
- Last content verification: 2026-10-16.

## S50

- Publisher and page: [OWASP: WebSocket security](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html).
- Supports: WebSocket handshake/message authorization, session lifecycle and bounds.
- Applicability and limits: Applies only to WebSocket features; not a reason to add them.
- Last content verification: 2026-10-16.

## S51

- Publisher and page: [Agent Skills: evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills).
- Supports: Matched baselines, independent assertions, fresh contexts and evidence.
- Applicability and limits: Suggested evaluation layout is optional; this repository retains top-level evals.
- Last content verification: 2026-10-16.

## S52

- Publisher and page: [Agent Skills: optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions).
- Supports: Description-only selection, near misses, held-out evaluation.
- Applicability and limits: Activation depends on host and context; description matching is not enforcement.
- Last content verification: 2026-10-16.

## S53

- Publisher and page: [OpenAI: testing agent skills systematically](https://developers.openai.com/blog/eval-skills).
- Supports: Captured runs, outcome/process/efficiency checks for skill evaluation.
- Applicability and limits: Blog examples can age; use current product docs S03/S04 for installation paths.
- Last content verification: 2026-10-16.

## S54

- Publisher and page: [PostgreSQL Global Development Group: INSERT and ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html).
- Supports: INSERT conflict handling and RETURNING behavior.
- Applicability and limits: PostgreSQL-specific: DO NOTHING does not return the pre-existing conflicting row.
- Last content verification: 2026-10-16.

## S55

- Publisher and page: [Stripe: idempotent requests](https://docs.stripe.com/api/idempotent_requests).
- Supports: Provider-scoped idempotency, saved results, retention and request matching.
- Applicability and limits: Checked API v1 behavior; do not generalize to other providers, endpoints, or API versions.
- Last content verification: 2026-10-16.
