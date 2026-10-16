# Evaluation result record

Copy this record for a real run. Unfilled fields in this reusable template are
not evidence. Mark each check PASS, FAIL, BLOCKED, NOT RUN, or NOT APPLICABLE,
with its reason. BLOCKED means attempted but prevented from producing a valid result.

| Field | Record |
| --- | --- |
| Date and operator | Supply actual date and evaluator |
| Agent, model, runtime version | Record exact identifiers exposed by the host |
| Skill revision | Commit ID, or file-tree digest before any commit exists |
| Fixture revision and language | Record clean start and dependency versions |
| Scenario and exact prompt | Case ID and prompt artifact |
| Arm | With skill, without skill, or explicit activation diagnostic |
| Tools and permissions | Include browsing, execution, and isolation |
| Instruction sources | Include global or inherited instructions that may confound comparison |
| Trace | Path or accessible artifact, with sensitive material removed |
| Activation | Selected skill, actual reads, and timing before decisions |
| Activation configuration | Description only, documented loading instruction, or explicit load |
| Discovery | Host catalog evidence, separate from selection and loading |
| Acceptance checks | Commands, outputs, and observed behavior |
| Observed failures | Concrete output or state, not inferred intent |
| Safety failures | Keep authorization bypasses and corrupted invariants visible |
| Concurrency evidence | Attempted requests, independent overlap, committed effects, final state, unexpected errors, and bounded waits |
| Query evidence | Measured scope, setup exclusions, authorization/control counting, sizes, budget, data volume, and plans |
| Efficiency observations | Actual exposed timing or token counts; otherwise unavailable |
| Measurements | Dataset, load, environment, samples, and uncertainty if relevant |
| Limitations | Unavailable checks and possible confounders |
| Verdict | Pass, fail, blocked, or not run with reason |

Compare artifacts, test output, and state across matched arms. Do not substitute
the agent's self-assessment for acceptance checks. Keep failed runs as evidence.
