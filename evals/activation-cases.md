# Activation cases

Run each prompt in a fresh session with the same available skill catalog. Do not
name the skill in the prompt when testing implicit activation. Record selection,
main-file reads, reference reads, and their order relative to decisions and edits.
An explicit invocation is a separate troubleshooting test.

| ID | Prompt | Expected | References before affected decisions |
| --- | --- | --- | --- |
| A01 | Build the backend for a task management application. | Activate | Architecture, database, queries, API, code |
| A02 | Add workspace invitations. | Activate | Architecture, database, queries, transactions, API, reliability, code |
| A03 | Implement a paginated comments endpoint. | Activate | Queries, API, code; database if schema changes |
| A04 | Fix duplicate orders. | Activate | Transactions, reliability, code; database and queries as affected |
| A05 | Inspect this backend without changing anything. | Activate, read only | Route after inspection to affected areas |
| A06 | Refactor this service. | Activate for a server service fixture | Architecture, code, plus affected contracts |
| A07 | Add a webhook handler. | Activate | API, reliability, transactions, code |
| A08 | This endpoint gets slower as the database grows. | Activate | Queries, performance, code |
| A09 | Build this frontend feature; change the backend if required. | Conditional | Load before backend decisions once the fixture requires a server change |
| A10 | Change the button colors. | Do not activate | None |
| A11 | Fix this frontend spacing. | Do not activate | None |
| A12 | Write a social media caption. | Do not activate | None |
| A13 | Translate this paragraph. | Do not activate | None |
| A14 | Correct a spelling mistake in the README. | Do not activate | None |
| A15 | Stop two shoppers from buying the last item. | Activate | Transactions, database, API, code |
| A16 | Move this client-only dropdown into its own component. | Do not activate | None |
| A17 | Make the API settings page use the same button colors as the rest of the app. | Do not activate | None |
| A18 | Translate this paragraph about database indexes into French. | Do not activate | None |
| A19 | Correct the spelling of PostgreSQL in the README. | Do not activate | None |
| A20 | Rearrange the backend architecture image on the landing page without changing its content. | Do not activate | None |
| A21 | Write a short social post about releasing our new API. | Do not activate | None |
| A22 | The API settings page needs a new saved preference. Implement the UI and the required backend behavior. | Activate at backend work | Database, queries, API, code |
| A23 | The export button crashes when a workspace has many records. | Activate for server export fixture | Queries, performance, API, code |
| A24 | Sometimes users receive the same notification twice. | Activate for delivery fixture | Reliability, transactions, code |
| A25 | A user can open another workspace's record by changing the URL. | Activate | API, queries, code |
| A26 | Add a search filter to this endpoint. | Activate | Queries, API, code |
| A27 | This job should resume safely after a restart. | Activate | Reliability, transactions, code |

Use references by their filenames in the [skill routing table](../skills/backend-engineering/SKILL.md#3-load-references-before-decisions).
Always include the focused research check when browsing is available. A09 needs
two fixtures: one with an existing suitable endpoint and one requiring a new
protected endpoint. A06 needs code context; the word "service" alone is ambiguous.

Fail a positive case if implementation precedes the relevant reads, the agent
loads the entire library without need, or the only evidence is a final statement
that the skill was followed. Mark trace visibility as unavailable when the host
does not expose it. Do not turn that absence into a pass.

Run two configurations separately: description-only installation and installation
with the documented loading instruction. Record discovery independently from actual
selection and reading. Explicit invocation does not prove automatic activation.
Reserve A20, A21, A24, and A27 as initial held-out prompts. Do not tune the description
against those prompts before measuring the revision. Add fresh held-out prompts after
they have informed a change. Source basis: [S52](../skills/backend-engineering/references/sources.md#s52),
[S53](../skills/backend-engineering/references/sources.md#s53).
