# Implementation checklist

Use internally or adapt in the task response. No application checklist file is
required. Mark an item not applicable with a reason when its conditions do not apply.

- [ ] Intended behavior, callers, and acceptance criteria are clear.
- [ ] Relevant references were read before affected decisions.
- [ ] Task-specific official documentation matches the actual versions, or access limits are recorded.
- [ ] Data invariants, ownership, authorization, and tenant boundaries are enforced.
- [ ] Queries, nested results, inputs, and externally driven resource use are bounded.
- [ ] Concurrent actors, duplicate execution, retries, and partial failure are addressed.
- [ ] Migration, compatibility, rollout, and recovery needs are resolved where relevant.
- [ ] Important behavior has appropriate tests and actual measurements where claimed.
- [ ] Final changes are connected, follow project conventions, and pass diff review.
- [ ] Completion evidence distinguishes executed checks from remaining limitations.
