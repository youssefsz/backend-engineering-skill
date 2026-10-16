# Migrations and recovery

## Read this when

Read before schema rollout, data backfill, compatibility changes, or recovery work.
Separate local disposable changes from deployed systems with important data.

## Decisions before implementation

Identify deployed versions, readers/writers, existing data defects, table size,
engine/DDL transaction support, locks, interruption behavior, and operational authority.
Agree acceptable data loss and recovery time before selecting recovery procedures.

## Implementation guidance

REQUIRED: Inspect generated SQL or equivalent operations before execution. Check
existing data and lock/rewrite behavior on the relevant engine. An ORM migration
name does not establish safety. Test populated data and concurrent application work
in an isolated rehearsal. Never treat this guidance as production authorization.
[S21](sources.md#s21)

DEFAULT: For deployed systems, expand compatible structures, migrate data and callers,
verify convergence, then contract only after old readers and writers have drained.
Keep already-applied shared migrations immutable; add a forward change instead.
Version overlap determines the sequence, not a universal number of releases.
[S21](sources.md#s21)

CONDITIONAL: For large backfills, use bounded batches with stable checkpointing,
retry-safe updates, and progress verification. Resume after interruption without
skipping late or concurrently updated rows. Bound lock duration and load, and report
failed batches. Small disposable datasets may need only a direct migration.
[S22](sources.md#s22)

REQUIRED: Distinguish code rollback, compatible schema, forward repair, and restoration
of data. A down migration cannot recreate deleted values. Test restore procedures
on a disposable target and compare measured recovery time and data loss with the
agreed objectives. Possessing a backup is not restore evidence. [S23](sources.md#s23)

## Worked example: Replace a deployed stored field

Assume `display_label` is replaced by `public_name` without changing meaning. Old
instances still write `display_label`. Both fields must agree through the transition.
A semantic conversion would require additional conflict and loss rules.

| Stage | Old instances | New instances | Consistency and recovery |
| --- | --- | --- | --- |
| Expand | Read/write old field | Not deployed yet | Add nullable new field without removing old compatibility |
| Bridge | Read/write old field | Read/write old field until bridge is verified | A verified database trigger copies old writes to new in the same transaction |
| Backfill | Continue old writes | Continue old-field writes | Bounded row updates copy current old values while the bridge handles concurrent changes |
| Switch reads | Still compatible | Read new, retain old write path | Verify all rows agree before enabling new reads |
| Switch writes | Must have drained | Write both atomically until final cutover | Keep old representation recoverable during the agreed rollback window |
| Contract | Cannot run | Use new representation | Remove bridge and obsolete structures in separately authorized cleanup |

The trigger is one conditional strategy, not a portable requirement. Verify its
engine support, write ordering, permissions, and transaction behavior. If trigger
execution fails, the originating write must fail atomically. An alternative is to
upgrade every writer to a compatible bridge version before backfill, then update
both representations in one transaction. Do not dual-write only in new code while
old instances silently leave the new representation stale.

For backfill, reread/update current values under the verified concurrency protocol.
Do not write values from an old exported snapshot over newer writes. Checkpoint
completed key ranges, retry interrupted ranges safely, and check both missing values
and disagreement. New inserts and old writes must remain covered throughout.

Before switching reads, compare relevant counts and values, exercise old/new versions
together, and verify the catch-up procedure after an interrupted batch. Before
destructive cleanup, confirm no old writer remains, all callers migrated, data
converged, and rollback no longer needs the old field. Before cleanup, code rollback
can retain both fields; afterward, an old binary may be incompatible. Forward repair
or a tested restore may be needed, with its actual data-loss implications.
[S21](sources.md#s21), [S22](sources.md#s22), [S23](sources.md#s23)

## Common mistakes

Avoid testing only empty databases, editing applied history, long blocking backfills,
one-step renames during version overlap, and conflating rollback with data recovery.
Two writes in separate transactions leave inconsistency when either fails.

## Verification and exceptions

Rehearse with relevant existing data, old/new application overlap, lock observation,
and interrupted/resumed work. Exercise recovery before claiming it works. Local
disposable schemas can follow a shorter path when no deployed caller or valuable
data needs compatibility. Record which production checks remain unexecuted and who
must authorize execution; do not invent downtime or recovery guarantees.
