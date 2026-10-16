# API and security

## Read this when

Read before API contracts, authentication, authorization, external input, or any
feature crossing a trust boundary. Load feature-specific sections only as relevant.

## Decisions before implementation

Identify trusted identity, object and action permissions, tenant scope, explicitly
public operations, writable fields, resource budgets, and error contracts. Determine
whether browser credentials attach automatically and which downstream systems are trusted.

## Implementation guidance

REQUIRED: Deny protected operations by default and enforce permissions server-side.
Authenticate, resolve trusted tenant context, then check both object and action.
Do not trust input user IDs, tenant IDs, roles, or ownership claims. Apply scope to
bulk, export, cache, storage, and job paths as well as ordinary endpoints. Test
negative access and side effects for each relevant path. Public endpoints remain
allowed by explicit design. [S24](sources.md#s24)

REQUIRED: Bind SQL values as parameters. Construct dynamic identifiers/operators
through safe allowlists or a verified builder. An ORM does not prevent every
injection. Allowlist writable fields before persistence to prevent clients from
changing privileged fields. Test hostile values and unexpected fields at boundaries.
[S25](sources.md#s25), [S26](sources.md#s26)

REQUIRED: Bound payloads, pages, nested results, batches, expensive filters, uploads,
and externally driven work. Set rate limits around the protected resource and actual
deployment, including shared limits across instances where required. Test oversize
and overload behavior without uncontrolled allocations or provider spending.
[S27](sources.md#s27)

DEFAULT: Use established authentication and cryptographic libraries. Verify current
official password hashing, session, and token guidance for the selected library.
Validate token integrity, trusted issuer/audience, permitted algorithms, expiry,
and revocation requirements. Test expiration, invalid signatures, logout, and role
changes. Do not invent cryptography or freeze security parameters forever.
[S28](sources.md#s28), [S29](sources.md#s29), [S26](sources.md#s26)

REQUIRED: For HTTP, preserve method semantics, meaningful status/error contracts,
cache controls, and retry expectations. Safe read methods must not mutate business
state. Sensitive responses must not leak through shared caches. Useful client errors
must not disclose credentials, internal stacks, or unauthorized record existence.
[S42](sources.md#s42), [S26](sources.md#s26)

CONDITIONAL: Where browsers automatically attach credentials, apply the framework's
documented CSRF protections and appropriate cookie policy. CORS controls browser
cross-origin access; it is not authorization and does not stop direct clients.
Verify the actual authentication model rather than assuming tokens eliminate CSRF.
[S26](sources.md#s26), [S29](sources.md#s29)

## Feature-specific protections

- CONDITIONAL, URL fetch: Validate schemes, destinations, resolved addresses, and
  every redirect. Address DNS rebinding and private/link-local destinations with
  a verified connection policy and network egress restrictions. Disable redirects
  if safe revalidation is unavailable. Test blocked destinations and alternate
  encodings. Input URL validation alone can leave SSRF paths. [S30](sources.md#s30)
- CONDITIONAL, uploads: Bound size and processing cost, validate expected content
  rather than trusting names or declared type, generate safe storage names, and
  isolate storage permissions. Treat parsers and contents as untrusted. Test false
  types, traversal names, and unauthorized retrieval. [S31](sources.md#s31)
- CONDITIONAL, webhooks: Verify the provider's documented authentication against
  the required raw bytes, including replay controls. Validate the authenticated
  payload, handle duplicates and out-of-order delivery, and choose acknowledgement
  after durable acceptance when required. Test forged and repeated deliveries.
  See the reliability reference before implementing effects. [S49](sources.md#s49)
- CONDITIONAL, WebSockets: Validate origins under the browser model, authenticate
  connection setup, authorize subscriptions and messages, and handle expiry,
  revocation, and tenant changes. Bound connections, message sizes, rates, and idle
  lifetime. Test authorization after session changes, not just at handshake.
  [S50](sources.md#s50)

Do not add any of these features merely because the reference mentions them.

## Common mistakes

Avoid UI-only permission checks, client-trusted ownership, cross-tenant cache keys,
unrestricted field binding, unlimited batches, homegrown token validation, and
secret-bearing errors. A successful login test does not establish authorization.

## Verification and exceptions

Create distinct identities and tenants. Test protected actions anonymously, as the
wrong owner, with insufficient role, and through alternate paths. Verify persisted
state stays unchanged after rejection. Exercise malformed and excessive input,
intentional public access, and credential lifecycle. A specialist review can be
appropriate for novel security design; it does not replace these implementation checks.
