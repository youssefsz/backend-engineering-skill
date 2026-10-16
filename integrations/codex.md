# Install and activate in Codex

Official references checked 2026-10-16: [local skills](https://developers.openai.com/codex/skills)
and [AGENTS.md](https://developers.openai.com/codex/guides/agents-md). These describe
supported discovery paths, not a tested compatibility claim for every Codex host.
Applicability notes: [S03](../skills/backend-engineering/references/sources.md#s03),
[S04](../skills/backend-engineering/references/sources.md#s04).

## Install the complete directory

Use `skills/backend-engineering/` from this repository, or `backend-engineering/`
from the installable ZIP. Set `BACKEND_SKILL_SOURCE` to that directory's absolute
path in your shell. It must contain `SKILL.md`, `references/`, `assets/`, and `LICENSE`.
No runtime is required to consume these instructions.

From the target application repository root, install for that project:

```sh
test -f "$BACKEND_SKILL_SOURCE/SKILL.md"
mkdir -p .agents/skills
test ! -e .agents/skills/backend-engineering &&
    cp -R "$BACKEND_SKILL_SOURCE" .agents/skills/backend-engineering
```

For user-wide local discovery instead:

```sh
test -f "$BACKEND_SKILL_SOURCE/SKILL.md"
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/backend-engineering" &&
    cp -R "$BACKEND_SKILL_SOURCE" "$HOME/.agents/skills/backend-engineering"
```

Run one installation choice. If the destination exists, stop and use the update
procedure below. Avoid ambiguous duplicate installations with the same skill name.
Local files are not automatically present in a remote or hosted session.

## Add a loading instruction

Merge the following paragraph into the application's existing root `AGENTS.md`.
Create that file if absent, but preserve its existing instructions. Do not copy this
repository's maintenance `AGENTS.md` into an application.

> Before designing, implementing, modifying, debugging, or reviewing backend behavior,
> load the backend-engineering skill at `.agents/skills/backend-engineering/SKILL.md`,
> relative to this repository root. Read relevant references before affected decisions.
> Apply it to new backends, features, database work, APIs, authorization, jobs,
> integrations, and performance work, including backend changes discovered during a
> frontend task. Follow its documentation-verification and testing requirements.
> Skip work that does not affect backend behavior. If loading fails, report the
> limitation instead of claiming to have followed the skill.

For the user installation, use `~/.agents/skills/backend-engineering/SKILL.md` in
that instruction. Optionally merge that version into `AGENTS.md` in your Codex home,
normally `~/.codex/AGENTS.md`, or `$CODEX_HOME/AGENTS.md` when configured. An active
`AGENTS.override.md` takes precedence at its level. Inspect it instead of replacing
files or changing global configuration automatically. Check instruction size limits
and nested overrides if a rule is missing.

## Verify discovery and activation

1. Start a fresh Codex session in the target repository. Open the skill selector
   by typing `$` or use `/skills` where supported, and confirm `backend-engineering`
   appears. This establishes discovery only.
2. Ask for a representative backend change without naming the skill. Where traces
   are available, check reads of the actual main file and relevant references before
   decisions or edits. A final claim alone is not proof of activation.
3. Troubleshoot explicit invocation with `$backend-engineering` followed by the task.
   Explicit success does not prove automatic selection. Use the evaluation cases to
   test description-only and instruction-assisted activation separately.

Keep implicit invocation enabled. The portable core requires no `agents/openai.yaml`
and does not disable selection through host metadata. Host permissions, tests,
constraints, and CI remain independent controls; loading instructions are not a
security boundary or a guarantee of correct output.

## Update or remove

Review the source change, changelog, and local modifications. Back up only the
installed `backend-engineering` directory, replace it with the complete reviewed
directory, and verify discovery again in a fresh session. Do not merge only SKILL.md
while leaving stale references. Remove the backup after confirming the update.

To uninstall, remove only the installed `backend-engineering` directory and its
loading paragraph. Preserve the parent skills directory, other skills, and the rest
of every instruction file. Removing a project copy does not remove a user copy.
