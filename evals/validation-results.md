# Validation evidence

Date: 2026-10-16. This record covers repository-maintenance checks, not backend
engineering effectiveness. Execution host was macOS, Python 3.14.2, uv 0.9.26,
in Codex desktop. No model identifier was recorded for an independent agent run
because no such run occurred. This opening record describes the initial local
checks; the hosted publication results appear below.

## Revision and environment

At initial local validation, version 0.1.0 was unreleased and had no initial commit.
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
| GitHub Actions execution | PASS | See the hosted validation and release results below |

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

At the release-automation preparation stage, live publication and hosted execution
were NOT RUN. The first publication results are recorded below. The
[release procedure](../CONTRIBUTING.md#tag-a-release) describes future versions.

## GitHub publication checks

On 2026-10-16, the repository was published publicly as
[youssefsz/backend-engineering-skill](https://github.com/youssefsz/backend-engineering-skill).
The release commit is `6402d267977d9dc1a42597671be58300872485ce`.
The tagged skill contents match the canonical tree digest recorded above.

| Check | Result | Evidence |
| --- | --- | --- |
| Hosted branch validation | PASS | [Validation run](https://github.com/youssefsz/backend-engineering-skill/actions/runs/38955124119), including all 30 tests and extracted archive validation |
| Tag-triggered release | PASS | [Release run](https://github.com/youssefsz/backend-engineering-skill/actions/runs/38955281297) ran checks and published v0.1.0 automatically |
| Published assets | PASS | [v0.1.0](https://github.com/youssefsz/backend-engineering-skill/releases/tag/v0.1.0) contains the ZIP and SHA-256 file |
| Public downloads | PASS | Both assets downloaded with anonymous curl requests; checksum, GitHub asset digest, and actual ZIP bytes agree |
| Downloaded package | PASS | `uv run --locked python scripts/package.py --check dist/published-v0.1.0/backend-engineering-v0.1.0.zip` extracted and matched all 15 files |
| Published notes | PASS | Actual release body contains changelog highlights, download instructions, and a GitHub-generated full changelog link |
| External URLs | PASS | 66 URLs were reachable during the publication check; badge SVG labels were checked separately |
| README presentation | PASS | Rendered GitHub README inspected in a browser, with working navigation and live badges |

The downloaded ZIP SHA-256 is
`ca91be8b9269a9ca57378315c74ade6b3f319196a77caf3cdb3e7a4f53b89e81`.
The release badge uses Shields' dynamic JSON endpoint because its GitHub-specific
endpoint returned an intermittent token-pool error. The tested endpoint reads the
actual public latest-release API. The badge values observed were validation passing,
release v0.1.0, MIT license, and Agent Skills standard.

There were no merged PRs before this initial release. GitHub generated the full
commit-history link; PR categorization and first-contributor sections remain
unexercised with real PR history. The host activation and backend engineering
scenarios above remain NOT RUN. Publication checks do not establish those outcomes.
