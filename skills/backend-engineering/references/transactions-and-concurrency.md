# Transactions and concurrency

## Read this when

Read before shared-state transitions, concurrent writes, atomic multi-step operations,
or transaction retries. Identify all writers, including jobs and other instances.

## Decisions before implementation

State the invariant and operations that must commit or fail together. Determine
isolation, contention, lock behavior, duplicate-request semantics, and external
effects. Verify the actual engine, driver, and transaction lifecycle.

## Implementation guidance

REQUIRED: Choose concurrency control from the invariant. A transaction alone does
not prevent lost updates, duplicates, or write skew. Consider conditional atomic
updates, version-based optimistic concurrency, row locking, constraints, or stronger
isolation. Read actual guarantees rather than assuming isolation names mean the same
thing across engines. Verify overlapping operations. [S19](sources.md#s19),
[S12](sources.md#s12)

DEFAULT: Keep transactions focused and short. Move remote calls, user interaction,
and slow computation outside lock-holding regions when correctness permits. Acquire
locks in consistent order across paths, and handle deadlocks intentionally. A
process-local mutex cannot coordinate multiple processes or instances. Inspect lock
waits and competing paths under representative load. [S20](sources.md#s20)

REQUIRED: When retrying a retriable transaction failure, retry the appropriate
transaction scope, reread required state, and bound attempts and total time. Do not
reuse stale decisions or repeat external effects inside the loop. Check driver/SDK
retries first. Distinguish retryable concurrency errors from validation and permission
failures. [S19](sources.md#s19), [S32](sources.md#s32)

## Membership creation

Use the [concurrent membership example](database-design.md#worked-example-concurrent-membership-creation)
for the complete constraint and duplicate contract. Its preliminary existence check
can race even inside a transaction. Expected insert conflict is not permission to
overwrite roles or swallow all database errors. Verify authorization and retry effects
as well as uniqueness. [S09](sources.md#s09), [S54](sources.md#s54)

## Worked example: Prevent inventory overselling

An item has one available unit. Two independent requests try to reserve one unit.
Reading stock and later writing `stock - quantity` lets both requests use the same
old value and accept more reservations than inventory permits.

PostgreSQL-specific illustrative option:

```sql
UPDATE inventory
SET available = available - $1
WHERE tenant_id = $2
  AND item_id = $3
  AND available >= $1
RETURNING available;
```

Assume quantity is a validated positive integer, tenant/item scope is authorized,
the row is uniquely identified, the engine/isolation behavior is verified, and
every other inventory-changing path preserves nonnegative stock. Use an appropriate
row constraint as a further invariant protection. At PostgreSQL Read Committed,
a competing updater waits and reevaluates the condition on the updated row.
[S09](sources.md#s09), [S19](sources.md#s19), [S20](sources.md#s20)

Use the returned row or affected-row count to decide whether to proceed. No result
means no decrement; resolve unavailable versus missing/unauthorized according to the
API's information-disclosure contract. If a reservation record must commit with the
decrement, wrap both in an appropriate transaction and roll back on reservation failure.

The conditional update handles overlapping stock changes. It does not make repeated
requests idempotent. Define a scoped request identity and coordinate its persisted
result with reservation creation. Test duplicate identity separately from competing
valid purchases. [S33](sources.md#s33)

## Common mistakes

Avoid read-modify-write races, process-local coordination as the only protection,
long lock-holding transactions, retrying a single statement after a transaction has
failed, and external calls inside retried transactions. Serializable isolation can
still require handling transaction failures; it is not automatic success.

## Verification and exceptions

For the controlled inventory fixture, synchronize two independent connections so
operations genuinely overlap. Bound all waits and record attempted requests, committed
reservations, final stored stock, and unexpected errors. Require two attempts, one
committed reservation, and stock zero. Inject reservation failure and check atomic
rollback. Verify retries do not duplicate a reservation. Use barriers or explicit
coordination rather than arbitrary sleeps. Sequential tests cannot establish safety.
Other engines need an equivalent verified strategy, not a blind copy of PostgreSQL SQL.
