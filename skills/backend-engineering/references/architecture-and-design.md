# Architecture and design

## Read this when

Read before a new backend, a substantial feature, or a refactor that changes
ownership or contracts. Small changes can follow the established design.

## Decisions before implementation

Identify behavior, owners of data and state transitions, trust boundaries,
callers, and failure cases. Trace who can change each state and which module
enforces its rules. Choose synchronous versus background execution, transaction
boundaries, compatibility requirements, and required external dependencies.

## Implementation guidance

DEFAULT: Put each business rule with the module that owns its state transition.
Keep transport parsing, persistence mechanics, and provider details from spreading
through unrelated business logic. This makes a permission or state-rule change
traceable. Verify by following one request through its owner and tests. A repository
layer, dependency-injection container, or named architecture is not mandatory.
[S08](sources.md#s08)

DEFAULT: Begin with a simple deployment and clear modules. Split services only
for demonstrated ownership, isolation, independent deployment, or scaling needs.
Account for remote failure, consistency, and operational cost before splitting.
Verify a proposed boundary by tracing a full operation including dependency failure.
Reliability patterns from distributed systems do not require building one.
[S32](sources.md#s32), [S34](sources.md#s34)

REQUIRED: Preserve public and persisted contracts unless a change is authorized.
Inventory callers, API fields, events, and stored representations. Plan compatibility
before implementation. Internal abstractions can be removed when callers migrate
together, but simplifying internals does not justify breaking external consumers.
Verify old callers against the new behavior. [S08](sources.md#s08)

## Worked example: Add comments to an existing project backend

Assume authenticated workspace members can read a project and post comments.
Comment authors may edit their text; only authorized moderators may remove another
author's comment. Resolve different product rules before coding. These are example
assumptions, not universal permissions.

The data flow is:

```text
request -> authenticate -> validate text and page bounds
        -> resolve authorized workspace and project
        -> comment operation owns permission and state transition
        -> persist or read scoped records -> serialize allowed response fields
```

1. Inspect existing project access, membership checks, database conventions, and
   clients. Reuse the existing session and response contracts.
2. Design comment identity, project/workspace relationship, author, text limit,
   creation time, and edit behavior. Prevent a cross-tenant relationship in storage
   where supported. Decide what deletion of a project or author means.
3. Bound listing, order with a unique tie-breaker, and retrieve author information
   with suitable joins or bounded batches. Read the query reference before selecting
   an index. Author deletion must follow the response contract.
4. Keep creation and required durable effects atomic. If a notification is required
   to survive restart, choose durable acceptance and publication semantics. If it
   is explicitly best-effort, document loss rather than introducing a queue by habit.
5. Return intentional validation, permission, missing-project, and persistence
   failure responses. Do not expose internal errors or pretend a failed save worked.
6. Test success, another workspace, unauthorized edit, equal-time pagination,
   constraints, and persistence after restart. Test duplicates, concurrent edits,
   and notification failure only where the chosen contract makes them relevant.

This example connects API, permissions, schema, queries, and tests. Read their
references before those decisions rather than treating this walkthrough as a substitute.
[S24](sources.md#s24), [S34](sources.md#s34)

## Common mistakes

Do not replace usable backend behavior with folders and interfaces. Avoid broad
rewrites during a focused feature, layers with no ownership purpose, and untracked
background work for required effects. An architecture diagram does not prove a
request reaches persistence.

## Verification and exceptions

Walk through success, unauthorized access, duplicate execution, concurrent updates,
and dependency failure where relevant. Verify public callers still work. For a new
backend, start the application, initialize storage, run the documented local setup,
exercise connected endpoints or jobs, and run tests. Document required configuration
and intentional failure responses. A disposable prototype can use simpler deployment
and recovery procedures while retaining the correctness its promised behavior needs.
