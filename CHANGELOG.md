# Changelog

Versions describe guidance, activation, integrations, required capabilities, and
package layout as well as wording. See the contribution policy before selecting a
version. Entries marked Unreleased describe local preparation, not publication.

## [0.1.0] - 2026-10-16

- Add one portable backend-engineering skill for construction, extension, debugging,
  refactoring, performance work, and inspection.
- Add 11 focused references, worked examples, two optional assets, and a reviewed
  registry of sources S01–S55 with engine/provider limits.
- Document Codex, Claude Code, and generic installation separately from activation.
  Keep fresh host activation and engineering effectiveness explicitly untested.
- Add activation near misses, held-out prompts, 14 engineering scenarios, matched
  baseline procedures, and concrete evidence/status requirements.
- Add local structure/link/source/format validation, validator mutation tests,
  read-only CI, and canonical ZIP construction with extraction and byte checks.
- Manage the existing repository-maintenance dependencies in a uv development group
  and lockfile. Preserve their constraints and test behavior, use locked commands
  locally and in CI, and keep skill installation independent of Python/uv.
- Add a stable-tag release workflow that runs checks, validates release metadata,
  and publishes the installable ZIP and checksum with changelog highlights and
  GitHub-generated PR/contributor notes. Add release categories and a concise PR
  template.
- Add a concise README with live validation/release shields, installation steps,
  and a direct path to the downloadable skill.
