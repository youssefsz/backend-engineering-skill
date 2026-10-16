# Reliability and background jobs

## Read this when

Read before remote calls, retries, jobs, webhooks, or required event publication.
Define which effects must survive process restart and which may be lost.

## Decisions before implementation

Identify acceptance, durability, deadlines, acknowledgement, duplicate identity,
ordering, and recovery ownership. Inspect SDK/client retries before adding another
layer. Determine where an uncertain outcome needs reconciliation rather than retry.

## Implementation guidance

REQUIRED: Set suitable timeouts/deadlines for remote work, including connection and
response behavior. Retry only appropriate transient failures within bounded attempts
and elapsed time. Use backoff and jitter when applicable, and avoid multiplying
retries across layers. A timeout does not prove a mutation failed remotely. Verify
slow responses and uncertain outcomes against the provider contract.
[S32](sources.md#s32)

REQUIRED: For retryable mutations, scope the idempotency key to the operation and
principal, bind it to request identity, coordinate concurrent duplicates, persist
results, and define expiry and changed-input behavior. Store a local effect and its
deduplication state atomically when supported. A separate "processed" flag can leave
a crash window. For external effects, use provider support or explicit reconciliation.
Verify crash boundaries and persisted effects, not just repeated success responses.
[S33](sources.md#s33)

REQUIRED: For required jobs, acknowledge after the chosen durable acceptance or
completion boundary. Handle redelivery, overlap, bounded concurrency, poison messages,
failure visibility, and recovery. Required work must not rely on untracked
fire-and-forget tasks. Do not assume exactly-once execution. Check the selected
queue/provider's documented behavior and test interruption. [S34](sources.md#s34),
[S49](sources.md#s49)

## Worked example: Reliable project-created publication

The sequence `save_project(); publish_event()` can commit a project and crash before
publication. If notification must eventually occur, one conditional design is:

```text
begin_transaction()
save_project()
save_outbox_event(stable_event_id, project_id, payload)
commit_transaction()

# A separate publisher processes committed outbox events.
```

Persist change and event atomically where supported. The publisher resumes unfinished
records after restart, bounds each retry cycle, and exposes persistent failures for
recovery. Mark delivered only after the publication mechanism accepts according to
its documented contract. Publication can succeed before the publisher records
completion, so duplicate delivery remains possible. Consumers need a stable identity
and atomic deduplication with their local business effect, or a documented alternative.
Define per-aggregate ordering if business behavior needs it. [S34](sources.md#s34)

Test interruption before commit, after commit before publish, and after publication
before recording completion. Match committed projects to eventual logical effects.
For explicitly best-effort notifications, losing an event may be acceptable and
does not automatically justify an outbox. [S32](sources.md#s32)

## Worked example: A provider creation times out

The provider may have created the resource even though the response was lost.
Before retrying, inspect which operations accept idempotency keys, key scope and
retention, input matching, concurrent-key behavior, and existing SDK retries.
Reuse the same identity for the same logical operation, not a fresh key per attempt.
Keep application state durable enough to reuse that identity after restart.

Stripe API v1 example: its idempotency contract can return the saved first result,
including a failed response, compares request parameters, and permits pruning keys
after at least 24 hours. Validation failures and concurrent conflicts before execution
do not save an executed result. These details are provider-specific and need checking
for the chosen endpoint; they are not universal retry semantics. [S55](sources.md#s55)

If provider retention or support is insufficient, reconcile through a stable external
reference, a status lookup, or an operator recovery process before risking another
creation. Document uncertainty when no safe automatic resolution exists. Do not
promise exactly-once effects across arbitrary providers. [S33](sources.md#s33)

## Common mistakes

Avoid fresh keys per attempt, retries of permanent errors, nested unlimited retries,
early acknowledgement that loses work, duplicate external side effects, and marking
processed before the required effect. An outbox solves a specific dual-write gap;
it does not make delivery unique.

## Verification and exceptions

Inject failures before the operation, before commit, after commit before response,
before publication, and after external acceptance before local completion. Restart
workers, overlap duplicate deliveries, and inspect stored outcomes and provider stub
effects. Test out-of-order webhooks according to the state-transition contract.
Use bounded waits and useful diagnostics so recovery tests cannot hang indefinitely.
