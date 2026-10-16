# Connect another agent

Native skill discovery varies by host. This repository supplies standard Agent
Skills frontmatter and ordinary Markdown. It does not claim universal compatibility.

1. Read the host's current skill and instruction documentation. Confirm supported
   project/user locations and whether local files reach hosted sessions.
2. Install the complete `skills/backend-engineering/` directory or its extracted
   archive counterpart in a supported location. Preserve `SKILL.md`, references,
   assets, and the license together. Register or expose it as the host requires.
3. Merge a loading requirement into the host's always-loaded instructions without
   replacing existing instructions. For a project that keeps the copy at
   `.agents/skills/backend-engineering/`, use the paragraph below. If the actual
   supported location differs, update the path to that real installed location.
4. In a fresh session, check discovery, then use a representative task and inspect
   actual reads before decisions where the host exposes them. Separately check
   implicit activation without the loading requirement if measuring the description.

> Before designing, implementing, modifying, debugging, or reviewing backend behavior,
> read `.agents/skills/backend-engineering/SKILL.md`, relative to the project root.
> Read its relevant references before affected decisions. Apply it to new backends,
> features, database work, APIs, authorization, jobs, integrations, and performance
> work, including backend changes discovered during a frontend task. Follow its
> documentation-verification and testing requirements. Skip work that does not affect
> the backend. If the files cannot be read, report the limitation rather than claiming
> to have followed the skill.

For a host without native skills, configure its always-loaded instructions to read
the actual local main file and supporting references on relevant tasks. A path printed
in a prompt does not make inaccessible files available. Use the host's supported
file/context mechanism, preserving relative paths. Do not flatten the library into
a second handwritten skill or assume a ZIP activates anything by itself.

Resolve reference links from their containing document. Paths explicitly described
as relative to the skill root use the installed directory, not the agent's current
shell directory. No Python, Node.js, database client, or shell is needed merely to
consume the instructions. An agent unable to read local Markdown needs another
supported context mechanism and must disclose that limitation.

For updates, review changes and local modifications, back up only the installed
directory, replace the complete reviewed copy, and retest. For removal, delete only
this skill and its loading paragraph. Preserve unrelated skills and instruction
files. Do not edit global settings without user authorization.

Instructions improve consistency but are not a security boundary. Host permissions,
tests, constraints, and CI supply independent checks. Documented format compatibility
is separate from tested activation and engineering quality.
