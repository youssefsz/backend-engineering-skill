# Install and activate in Claude Code

Official references checked 2026-10-16: [skills](https://code.claude.com/docs/en/skills)
and [memory](https://code.claude.com/docs/en/memory). Paths below are documented
compatibility; a fresh Claude Code activation test has not been executed here.
Applicability notes: [S05](../skills/backend-engineering/references/sources.md#s05),
[S06](../skills/backend-engineering/references/sources.md#s06).

## Install the complete directory

Set `BACKEND_SKILL_SOURCE` to the absolute path of this repository's
`skills/backend-engineering/` or the extracted installable `backend-engineering/`.
Include all references, assets, and the license. From your application repository
root, install a project copy:

```sh
test -f "$BACKEND_SKILL_SOURCE/SKILL.md"
mkdir -p .claude/skills
test ! -e .claude/skills/backend-engineering &&
    cp -R "$BACKEND_SKILL_SOURCE" .claude/skills/backend-engineering
```

Or install locally for your user:

```sh
test -f "$BACKEND_SKILL_SOURCE/SKILL.md"
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/backend-engineering" &&
    cp -R "$BACKEND_SKILL_SOURCE" "$HOME/.claude/skills/backend-engineering"
```

Choose one. If the target exists, review an update instead of copying into a nested
directory. Local user installation does not automatically reach every cloud/hosted
session. Supply the skill through that environment's documented mechanism.

## Add a loading instruction

Merge this paragraph into the application's existing root `CLAUDE.md`. Preserve
its other contents; create it only if absent.

> Before designing, implementing, modifying, debugging, or reviewing backend behavior,
> load `.claude/skills/backend-engineering/SKILL.md`, relative to this repository root.
> Read relevant references before affected decisions. Apply it to new backends,
> features, database work, APIs, authorization, jobs, integrations, and performance
> work, including backend changes discovered during a frontend task. Follow its
> documentation-verification and testing requirements. Skip work that does not affect
> backend behavior. If loading fails, report the limitation instead of claiming use.

For a user install, use `~/.claude/skills/backend-engineering/SKILL.md` and optionally
merge that version into `~/.claude/CLAUDE.md`. Do not replace an entire instruction
file or change global settings automatically.

Direct `AGENTS.md` loading is documented for v2.1.277 and later, subject to settings
and session availability. The default can prefer an existing `CLAUDE.md`. Older or
restricted sessions may require importing a shared file from `CLAUDE.md` with
`@AGENTS.md`. Check the current memory documentation and actual host version before
relying on this route. The primary procedure here uses `CLAUDE.md`.

## Verify discovery and activation

Start a fresh session and look for `/backend-engineering` in the command menu.
Invoke `/backend-engineering` with a representative task to troubleshoot discovery.
Then test a new session without explicit invocation, checking actual main/reference
loading events before affected decisions where visible. Separate description-only
selection from selection with the loading paragraph. Neither explicit invocation
nor a final self-report proves automatic activation or good implementation.

Do not set `disable-model-invocation: true`. No Claude-specific metadata or alternate
copy of the main skill is needed. Host permissions, tests, database constraints,
and CI remain separate controls; instructions do not guarantee secure output.

## Update or remove

Review changes and back up the installed directory, then replace only
`backend-engineering` with the complete reviewed version. Start a new session and
repeat discovery and representative-task checks. Retain local changes deliberately
rather than accidentally mixing old references with a new main file.

To remove, delete only this skill's installed directory and loading paragraph.
Preserve other skills and instruction contents. Check for a second project/user copy
if the skill still appears.
