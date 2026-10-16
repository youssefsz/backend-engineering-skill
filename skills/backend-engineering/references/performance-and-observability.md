# Performance and observability

## Read this when

Read before optimization claims, caching, pool sizing, concurrency limits,
instrumentation, or relevant process lifecycle changes.

## Decisions before implementation

Identify the actual bottleneck, workload, resource budgets, deployment topology,
and existing telemetry. Separate sensible bounds from optimizations requiring
measurement. Define acceptable staleness and consistency before choosing a cache
or read replica.

## Implementation guidance

REQUIRED: Collect a baseline before claiming an optimization. Measure relevant
latency percentiles, throughput, errors, query time, connection/lock waits,
resource use, and payload size. Use comparable datasets, request mix, concurrency,
warm-up, and environments. Record method and sample count. Explain what the numbers
represent, and avoid percentage claims from one uncontrolled run. There is no
universal 100-millisecond endpoint target. [S37](sources.md#s37), [S14](sources.md#s14)

DEFAULT: Where pooling applies, reuse connections through the supported driver/pool.
Budget total demand across instances, workers, deployment overlap, administrative
access, and reserves. Test acquisition timeouts and request/worker concurrency together.
A larger pool may increase contention instead of throughput. HikariCP illustrates
tradeoffs; its formulas are not universal driver settings. [S36](sources.md#s36)

REQUIRED: Bound memory, fan-out, parallel remote requests, and large-result processing.
Consider batching or streaming when needed, including cancellation and backpressure.
Measure resource growth and failure behavior under the intended load rather than
assuming asynchronous code makes unlimited concurrency safe. [S27](sources.md#s27)

CONDITIONAL: Before caching, define key scope, staleness, invalidation, expiry,
capacity, and failure behavior. Include tenant/permission context as required and
avoid retaining stale permissions. Test cold caches, stampedes, and outage. Bound
database fallback with measured capacity and deliberate overload behavior; unrestricted
fallback can turn cache failure into database failure. [S35](sources.md#s35)

CONDITIONAL: Before replica reads, verify consistency and lag for the actual engine
and service. Route read-after-write operations according to required consistency,
not blindly to an asynchronous replica. Test delayed replication and stale-read
behavior. AWS RDS documents its own replica implementations, not every topology.
[S47](sources.md#s47)

DEFAULT: Use the existing telemetry tools. Emit structured logs with useful
correlation IDs, and redact secrets and sensitive data. Choose signals that identify
request/job failures and dependency bottlenecks without logging raw customer payloads.
Keep metric label dimensions bounded; arbitrary user IDs and full URLs create
unbounded cardinality. Verify actual emitted telemetry and redaction.
[S43](sources.md#s43), [S38](sources.md#s38), [S48](sources.md#s48)

CONDITIONAL: For database maintenance problems, inspect the actual engine's
statistics, vacuuming, checkpointing, or equivalent. PostgreSQL vacuum and SQLite
WAL checkpoint behavior differ. Do not apply one engine's maintenance commands to
another. Verify observed waits and storage behavior before changing configuration.
[S44](sources.md#s44), [S46](sources.md#s46)

CONDITIONAL: When the deployment routes traffic to long-lived processes, distinguish
process health from readiness to accept work. On shutdown, stop new acceptance,
drain or safely return in-flight work within a deadline, and close resources using
the host's documented lifecycle. Read its version-specific documentation. Test
termination during requests and jobs; a running process need not be ready.
[S37](sources.md#s37), [S32](sources.md#s32)

## Common mistakes

Avoid connection exhaustion, unlimited asynchronous fan-out, caches without scoped
keys or outage limits, arbitrary metrics labels, and fabricated speedups. Do not
install a monitoring stack or prescribe maintenance commands without a task need.

## Verification and exceptions

Keep correctness and permission checks in the optimization acceptance criteria.
Compare before/after measurements under the same conditions and disclose uncertainty.
Exercise saturation, cache loss, slow dependencies, and shutdown where affected.
A small bounded change may need only targeted regression checks; it does not require
a database benchmark unless it makes a material performance claim.
