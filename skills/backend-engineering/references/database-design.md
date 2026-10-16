# Database design

## Read this when

Read before creating persisted state, changing a schema, or deciding where a data
invariant is enforced. Identify the actual storage model and version first.

## Decisions before implementation

Write invariants before columns or documents. Identify identity, tenant ownership,
relationships, lifecycle/deletion, read/write patterns, precision, time semantics,
and which rules span rows or systems. Decide which writes must be atomic.

## Implementation guidance

REQUIRED: For relational storage, use appropriate primary keys, uniqueness, foreign
keys, nullability, and row-level checks. Application checks alone cannot protect
concurrent callers or other writers. A CHECK is not a general mechanism for cross-row
or cross-system rules. Choose transactions, concurrency control, or coordinated
workflows for those rules. Verify violations against the actual engine and configured
enforcement. [S09](sources.md#s09), [S19](sources.md#s19)

REQUIRED: Scope uniqueness and relationships to tenants when ownership requires it.
A composite relationship can prevent a child from naming another tenant's parent.
Choose cascade, restrict, archival, or soft deletion from ownership and retention
requirements. Soft deletion changes uniqueness and every read path; it does not
automatically solve retention or privacy. Verify deletion and cross-tenant writes.
[S09](sources.md#s09), [S24](sources.md#s24)

REQUIRED: Check engine/configuration behavior for null uniqueness, collation, case
sensitivity, and foreign keys. For SQLite, inspect and enable foreign-key enforcement
on each connection as appropriate, outside an active transaction. Do not infer it
from DDL alone. Test the actual connection setup. [S45](sources.md#s45)

DEFAULT: Use exact decimal or scaled integers for quantities requiring exact
arithmetic. Define units, scale, rounding, conversion boundaries, and overflow.
Floating point can fit approximate measurement; avoid treating all numbers as money.
Test rounding and boundary values in storage and application arithmetic.
[S10](sources.md#s10)

REQUIRED: Distinguish an instant, a calendar date, and a local scheduled time.
A birthday is not a UTC instant. A recurring local schedule may need its timezone
identifier and an explicit daylight-saving ambiguity policy. For PostgreSQL,
`timestamp with time zone` represents an instant, not the original named zone.
Preserve that zone separately when required. Verify serialization and boundary dates.
[S11](sources.md#s11)

CONDITIONAL: For document databases, choose aggregate boundaries from access and
atomicity needs. Bound embedded-array growth, apply validation, and verify actual
single-document versus multi-document atomicity. MongoDB's documented single-document
atomicity does not make all multi-document operations atomic. Avoid blindly importing
relational normalization rules. [S12](sources.md#s12)

## Worked example: Concurrent membership creation

An authorized administrator adds a user to a workspace. The invariant is at most
one membership per workspace and user. The following check can race:

```text
if membership_does_not_exist(workspace_id, user_id):
    create_membership(workspace_id, user_id)
```

Two requests can both observe absence before either inserts. In a relational
design, require non-null workspace/user identifiers and appropriate references,
then enforce `UNIQUE (workspace_id, user_id)`. Include tenant ownership in related
keys where the schema needs it. This protects competing writes, not authorization.

Choose the duplicate contract deliberately: return the existing membership, report
already-exists, or another specified result. Catch only the expected constraint
violation using the driver's structured error and constraint identity. Do not
mislabel connection failures or other constraints as duplicates. Never change a
member's role as a side effect of retrying creation. Role changes need separate
authorization. [S09](sources.md#s09), [S24](sources.md#s24)

PostgreSQL-specific: `ON CONFLICT DO NOTHING RETURNING ...` returns rows actually
inserted, not the conflicting existing row. At Read Committed, an insert may be
skipped due to a competing row not visible in the statement snapshot. If the contract
returns an existing row, use a verified follow-up read/protocol and account for
concurrent deletion. `DO UPDATE` performs an update and can require different
permissions or fire update triggers. Do not use it as an innocent read shortcut.
[S19](sources.md#s19), [S54](sources.md#s54)

## Common mistakes

Avoid application-only invariants, globally unique tenant-local values, accidental
cascades, unchecked unbounded documents, and automatic role overwrites on conflicts.
There is no universal requirement to normalize, denormalize, use UUIDs, or store JSON.

## Verification and exceptions

For the membership fixture, overlap two requests on independent connections using
a barrier and bounded waits. Assert one stored membership, correct duplicate results,
and no role elevation after retries. Verify different users can join the same workspace,
one user can join different workspaces, and unauthorized callers cannot add anyone.
Test constraints directly as well as through the API. If storage lacks the needed
constraint, specify and test an equivalent coordination protocol rather than silently
weakening the invariant. SQL snippets here are illustrative, not production test evidence.
