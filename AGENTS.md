# Repository maintenance

This file governs maintenance of `backend-engineering-skill`, not application
backend work. Use [the integration guides](integrations/generic-agent.md) for
loading instructions in consuming projects.

- Preserve one portable core in `skills/backend-engineering/`. Keep runtime guidance
  self-contained, language/host neutral, and instruction-only. Do not require Python
  or uv to consume it. Keep the main file within this project's 150–250-line target.
- Guide construction and extension during implementation. Do not turn the skill
  into a final-audit checklist or require unrelated artifacts for small changes.
- Verify sources for content and actual version applicability. Keep stable IDs,
  dates, and limits honest. Original summaries only; no copied vendor manuals.
- Update relevant activation and engineering evaluations. Separate discovery,
  loading, and implementation quality. Do not invent results or compatibility claims.
- Preserve existing tools, constraints, and test behavior. Manage development tools
  only in `pyproject.toml` and `uv.lock`; keep both tracked and `.venv/` ignored.
- Run `uv sync --locked`, `uv run --locked python scripts/validate.py`,
  `uv run --locked python -m unittest discover -s tests -v`, and
  `uv run --locked python scripts/package.py` from the repository root.
  Run external link checks separately when relevant. Never weaken checks for a pass.
- Inspect extracted archive references, casing, allowed files, byte equality, and
  license. Update root and installable licenses together. Do not add a custom installer.
- Review changes that broaden activation, require capabilities, or introduce
  executable tooling. Record meaningful guidance, compatibility, and evaluation
  changes in the changelog, preserving honest untested statuses.
- Keep the validation workflow read-only. Only the version-tag release job may have
  `contents: write`. Never expose publication credentials to untrusted PR code.
  Release tooling must check tag/version/date consistency before publishing.
  No publication, push, visibility changes, or global agent configuration changes
  without separate authorization.

Follow [CONTRIBUTING.md](CONTRIBUTING.md) for rule, source, version, and release review.
Source basis: [S41](skills/backend-engineering/references/sources.md#s41).
