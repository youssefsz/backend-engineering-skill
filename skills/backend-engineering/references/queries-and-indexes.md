# Queries and indexes

## Read this when

Read before adding or modifying data access, pagination, related-data loading, or
indexes, and when diagnosing query cost. Determine the actual local or remote path.

## Decisions before implementation

Identify authorized scope, returned fields, maximum cardinality, sorting semantics,
related data, and expected workload. Inspect executed SQL or database operations,
including ORM-generated queries, and review existing indexes before adding one.

## Implementation guidance

DEFAULT: Select needed fields, filter and aggregate in the database when appropriate,
and bound results before materialization. Bound nested collections too. Verify rows,
bytes, memory, and query count as result sizes increase. Small fixed local datasets
can justify simpler processing; state the bound. [S16](sources.md#s16)

REQUIRED: Investigate client/server N+1 access when queries grow once per parent.
Choose batching, suitable joins, eager loading, or separate bounded queries. A join
across several one-to-many relationships can multiply rows and transfer more data
than separate queries. Compare both round trips and rows processed.
[S16](sources.md#s16)

CONDITIONAL: Local in-process SQLite avoids the network round-trip cost underlying
many N+1 warnings. Measure actual work instead of forcing one query. A remote API
backed by SQLite still incurs its network path, and many local queries can still
do excessive work. [S18](sources.md#s18)

REQUIRED: Use deterministic, fully unique ordering for pagination. Validate cursor
shape, types, allowed sort, and page limits. Reapply authorization on every request.
Keyset pagination fits sequential traversal; offset fits page jumps and bounded
datasets where its scan and shifting-row costs are acceptable. Neither alone creates
a frozen snapshot between requests. [S17](sources.md#s17)

CONDITIONAL: Design indexes from filters, joins, ordering, selectivity, and workload.
Inspect existing coverage. Composite order, partial/covering indexes, and operator
support depend on the engine. Weigh read benefit against write cost and storage.
Do not apply a universal column-order formula. [S13](sources.md#s13)

REQUIRED: For consequential optimization, inspect representative plans. Compare
estimated and actual rows, loops, scans, joins, sorts, and work performed. A sequential
scan can be the correct choice. Ensure statistics and data distribution represent
the workload. [S14](sources.md#s14)

REQUIRED: `EXPLAIN ANALYZE` executes the statement. Do not treat writes or expensive
production analysis as read-only inspection. Even rolling back can leave external
effects or consume substantial resources. Use an authorized isolated environment
and understand the engine's command first. [S15](sources.md#s15)

## Worked example: Paginated comments

Assume authorized project members can read comments with author display names.
Choose a maximum page size, response fields, deletion behavior for authors, and
whether replies exist. Bound replies separately if included. Resolve project and
tenant permissions before querying. [S24](sources.md#s24)

For non-null, immutable ordering values, an illustrative descending SQL pattern is:

```sql
ORDER BY created_at DESC, id DESC
```

After the last returned pair, add this grouped predicate alongside tenant/project
filters. Placeholder binding syntax depends on the driver:

```sql
AND (created_at < :cursor_created_at
     OR (created_at = :cursor_created_at AND id < :cursor_id))
```

Match comparison direction, types, timestamp precision, and collation to the actual
engine. Retrieve authors through a suitable join or bounded batch, handling missing
authors according to the contract. Consider an index matching scope and ordering
only after inspecting schema, current indexes, and workload.
[S13](sources.md#s13), [S16](sources.md#s16), [S17](sources.md#s17)

An inserted newer comment may appear only after refreshing the first page. Deleted
rows disappear. Changes to sort values can cause repeats or omissions across requests.
If the product needs snapshot traversal, design that separately and state its cost.

## Common mistakes

Avoid unbounded nested responses, hidden ORM round trips, join explosions, cursors
treated as permissions, timestamp-only ordering, and indexes added without evidence.
A constant query count alone does not establish efficient execution.

## Verification and exceptions

On unchanged data with equal timestamps, traverse every page and compare exact IDs
with the expected set. Test limits, malformed cursors, tenant scope, and missing
authors. Separately test mutations between pages against documented semantics.
Count statements during measured endpoint execution, excluding fixture setup and
accounting consistently for authorization and transaction-control queries. Compare
multiple sizes against a fixture-specific budget, not a universal one-query target.
Inspect transferred volume and plans when they dominate cost. Do not convert a lower
query count into an unmeasured latency claim.
