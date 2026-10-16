# Local validation record

Date: 2026-10-16. This record covers repository-maintenance checks, not backend
engineering effectiveness. Execution host was macOS, Python 3.14.2, uv 0.9.26,
in Codex desktop. No model identifier was recorded for an independent agent run
because no such run occurred. GitHub-hosted CI has not been executed.

## Revision and environment

Planned skill version: 0.1.0, unreleased, with no initial commit at validation time.
The canonical skill tree digest is
`591b246fbce8e7300e4a587191895e2392ce3a9cb3643c71036466cb075a7002`.
Compute it by sorting all file paths under `skills/backend-engineering`, then
hashing each relative POSIX path, a NUL byte, file bytes, and a NUL byte with SHA-256.
The archive command separately reports the ZIP digest.

Checks used local temporary directories and development dependencies. No database,
production credentials, deployment, global configuration edits, or publication was
needed. The source review and optional URL check used public HTTPS. The installed
skill remains Markdown-only.

## Initial repository checks

| Command | Result | Evidence |
| --- | --- | --- |
| `uv sync --locked` | PASS | Lock resolution and existing 19 installed packages audited; no direct dependency constraint changed |
| `uv lock --check` | PASS | Existing lock matched project metadata |
| `uv run --locked python scripts/validate.py` | PASS | Structure, sources, local paths/casing/anchors, frontmatter, and Markdown lint passed; main file has 191 lines |
| `uv run --locked skills-ref validate skills/backend-engineering` | PASS | Reported valid skill |
| `uv run --locked python -m unittest discover -s tests -v` | PASS | 19 tests executed, all passed |
| `uv run --locked python scripts/package.py` | PASS | 15 files extracted, compared with canonical source, and validated |
| `uv run --locked python scripts/check_external_links.py` | PASS | 58 URLs reachable, zero requiring review during this execution |

The final ZIP SHA-256 is
`ca91be8b9269a9ca57378315c74ade6b3f319196a77caf3cdb3e7a4f53b89e81`.
Its generated path is `dist/backend-engineering-v0.1.0.zip`. Rebuild it from
canonical contents with the packaging command; `dist/` is intentionally ignored.
The byte comparison detects stale archives independently of the versioned filename.

The initial validator test exposed same-document fragments resolving to the parent
directory. The resolver was fixed without weakening the test. The 19 tests retained
their behavior through the uv migration. Direct dependency pins and the skills-ref
Git revision were preserved. The obsolete requirements file was removed after its
consumers were updated. `.venv/` remains ignored.

## Unexecuted evaluation work

| Evaluation | State | Reason and next step |
| --- | --- | --- |
| Fresh Codex discovery/activation | NOT RUN | Run the integration guide in a supported isolated target session and record catalog/read evidence |
| Fresh Claude Code discovery/activation | NOT RUN | A configured target session was not available for this evaluation |
| Description-only versus instruction-assisted activation | NOT RUN | Use separate fresh sessions and the activation matrix |
| E01–E14 engineering quality | NOT RUN | No isolated, versioned application fixture runner was established |
| E02/E03/E07 matched baselines | NOT RUN | Prepare matched independent repositories/databases and follow the evaluator contracts |
| Two-language effectiveness | NOT RUN | No cross-ecosystem runs occurred; no effectiveness claim is supported |
| GitHub Actions execution | NOT RUN | Workflow prepared locally; no remote repository or workflow run was published |

These states are not passes. The [evaluation procedure](README.md) and
[case contracts](engineering-cases.md) describe reproducible setup and acceptance.
No live backend, race-safety, provider, or performance outcome has been inferred
from a format check or from an illustrative snippet.

## Release automation checks

On 2026-10-16, the tag workflow, release-note categories, and PR template were added.
`uv sync --locked` and `uv run --locked python scripts/validate.py` passed.
`uv run --locked python -m unittest discover -s tests -v` ran 30 passing tests:
the existing 19 plus 11 release checks. Development dependency constraints and the
lockfile were unchanged.

The release checks cover matching tag/project/changelog versions, valid dates and
nonempty highlights, unsupported tags, checksum contents, tag-only publication,
workflow permissions, and the actual publishing shell command with a local fake
`gh` executable. This stand-in records arguments and cannot publish anything.

The current `uv run --locked python scripts/package.py --tag v0.1.0` correctly
failed because the changelog entry remains Unreleased. A separate temporary checkout
with only that entry dated 2026-10-16 successfully ran the full tagged CLI build and
archive recheck. Its 15 extracted files matched the canonical skill, the checksum
matched the ZIP, and the notes included the matching highlights. The canonical skill
and its archive digest above did not change.

Live GitHub publication, generated contributor/PR attribution, and hosted workflow
execution remain NOT RUN. The repository has no remote or published release from
this work. Follow the [release procedure](../CONTRIBUTING.md#tag-a-release) for the
first deliberate tag push after review.
