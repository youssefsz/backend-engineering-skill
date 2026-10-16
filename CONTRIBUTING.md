# Contribute

Propose changes against a real failure or a clearly motivated risk. Keep this one
portable, instruction-only skill and preserve the existing toolchain and tests.

## Propose a rule

First decide whether the failure is missing knowledge, unclear wording, activation,
reference routing, testing/tooling, a conflict with project instructions, or a need
for a separate specialist capability. Not every failure needs another paragraph.

Describe applicable conditions, the action, prevented cost/failure, verification,
exceptions/tradeoffs, and a primary source where available. Choose REQUIRED, DEFAULT,
or CONDITIONAL deliberately. Change the smallest relevant instruction, remove
redundancy, and add/update an evaluation that would reveal the failure. Review changes
that broaden activation or add executable tools before accepting them.

For source disagreements, identify engine, version, configuration, and workload.
Preserve uncertainty where evidence does not settle a choice. Measurements may
justify a different performance strategy, but not broken authorization or data
invariants. Verify actual content and applicability; an HTTP success alone is not
source review. Record actual dates in the source registry, not assumed freshness.

## Set up maintenance tools

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and use Python
3.11 or later. Git is needed to fetch the pinned skills-ref development dependency.
From the repository root:

```sh
uv sync --locked
uv run --locked python scripts/validate.py
uv run --locked python -m unittest discover -s tests -v
uv run --locked python scripts/package.py
```

CI uses the same locked commands. All Python checks run through `uv run --locked`.
Do not disable assertions or substitute mocked archive validation to make tests pass.
Optional network checking is separate:

```sh
uv run --locked python scripts/check_external_links.py
```

PyMarkdown handles structure; the repository disables only line-length enforcement
so routing tables remain readable. The parser checks relative links from each
containing document, local anchors, casing, source identifiers, and installable
boundaries. The extracted ZIP is checked too. Static checks do not prove backend
engineering quality.

## Change development dependencies

Edit the `[dependency-groups].dev` constraints in `pyproject.toml`, then run `uv lock`
and `uv sync --locked`. Alternatively use `uv add --dev` with the intended explicit
constraint. Review both `pyproject.toml` and `uv.lock` and rerun the existing checks.
Avoid unrelated upgrades, including of the pinned Git revision. Commit both files.
Do not hand-edit the lockfile or create a second requirements list. Keep `.venv/`
ignored. Runtime skill consumers do not need uv or any Python dependency.

This uses uv's [development groups](https://docs.astral.sh/uv/concepts/projects/dependencies/)
and [locked synchronization](https://docs.astral.sh/uv/concepts/projects/sync/).
An intentionally changed constraint can require a lock update; `--locked` should
reject accidental drift instead of silently resolving it in CI.

## Evaluate behavior and cost

Follow [the evaluation procedure](evals/README.md), beginning with the feature,
query, and duplicate-execution cases. Define acceptance before seeing the output.
Keep baselines isolated without removing user configuration. Test description-only
activation separately from instruction-assisted loading. Keep failed and blocked
runs visible and redact retained logs.

Inspect traces for repeated searches, reading every reference for small work,
unrequested documents, speculative infrastructure, repeated verification, and
unrelated refactors. Simplify the instruction causing wasted work. Record exposed
time/token observations only when actually available.

## Version and review changes

Use semantic versions for this project, including during `0.x` development:

- Patch: Wording/examples that preserve intended guidance. Still test high-impact
  wording changes because a short edit can alter behavior.
- Minor: Changed engineering defaults, expanded activation, documented integration
  changes, or additive compatible package resources.
- Major: Incompatible package layout, newly required consumer capabilities, or
  removed/changed behavior on which existing integrations depend.

Record the affected category and rationale in the changelog. Keep the project version
in `pyproject.toml` consistent with the first version entry in `CHANGELOG.md` when
preparing a version. Refresh `uv.lock` when project metadata requires it. Do not call
an unreleased local version published.

## Tag a release

1. Set the intended stable version in `pyproject.toml` and the first version entry
   in `CHANGELOG.md`. Replace `Unreleased` with the actual release date in
   `YYYY-MM-DD` format. Keep the entry's highlights concise and useful to users.
   Run `uv lock` when updating project metadata and review the lockfile diff.
2. Run the existing checks above, then prepare that version's downloads locally.
   For version 0.1.0, the command is:

   ```sh
   uv run --locked python scripts/package.py --tag v0.1.0
   ```

   This only builds local files. It rejects an undated entry, mismatched versions,
   empty highlights, and unsupported tag formats. Inspect the ZIP, `.zip.sha256`,
   and generated `dist/release-notes.md` before proceeding.
3. Merge the reviewed release commit into the default branch, including workflow
   and release-note configuration changes. Confirm validation passes there. From
   that commit, deliberately create and push only the matching tag:

   ```sh
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

   Use the actual prepared version in both commands. Pushing this tag authorizes
   automatic publication. Only stable `vMAJOR.MINOR.PATCH` tags are supported;
   prereleases are outside the current workflow.
4. Check the release workflow result, published notes, ZIP, and checksum. Consumers
   download the installable ZIP rather than GitHub's complete source archive.
   They do not need Python or uv.

The workflow builds the tag's exact contents and repeats validation before calling
GitHub CLI. Its token has `contents: write` only in the tag-triggered release job.
The ordinary validation workflow remains read-only. No personal token is required.
GitHub CLI attaches the files before publishing the release, and `--verify-tag`
prevents it from creating a missing tag. See the [CLI release documentation](https://cli.github.com/manual/gh_release_create).

The [release-note configuration](.github/release.yml) groups PRs labeled
`enhancement`, `bug`, `documentation`, `maintenance`, or `dependencies`. Those labels
are optional; unmatched PRs appear under Other changes. GitHub supplies contributor
and comparison details from repository history, so an initial release or a release
without merged PRs can have fewer generated sections. Review changelog highlights
before tagging rather than relying on automation to explain why changes matter.
See [GitHub's generated-notes documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes).

Rerunning a successful tag does not overwrite a published release or replace its
assets; the CLI reports the existing release. If a failed upload leaves an unpublished
draft, inspect and remove only that draft before rerunning the unchanged tag. Do not
move published tags. Correct published content through a new version.

## Final release review

Before marking a version ready, review workflow contradictions and proportionality,
direct reference discovery, evaluation claims, source changes, and README accuracy.
Rerun affected tests, build the installable ZIP, inspect its contents, and revalidate
after extraction. New files inside the installable directory require a deliberate
allowlist and test update. Keep credentials, caches, and transcripts out.

Do not publish releases, push, change visibility, or modify global agent settings
without separate authorization. Unexecuted host compatibility tests stay labeled
untested. A small evaluation suite does not justify "production-ready" or
"guaranteed secure" claims. Source basis:
[S02](skills/backend-engineering/references/sources.md#s02),
[S51](skills/backend-engineering/references/sources.md#s51),
[S53](skills/backend-engineering/references/sources.md#s53).
