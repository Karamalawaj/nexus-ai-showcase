# AI Commerce SaaS Security & Readiness Checklist

A practical, portfolio-safe checklist for reviewing an AI-enabled multi-tenant commerce service before exposing it to real stores or customers.

## Tenant isolation

- [ ] Every store/client has a stable tenant identifier.
- [ ] Database queries are scoped by tenant at the repository/service layer, not only in the UI.
- [ ] Cross-tenant object access is explicitly tested and denied.
- [ ] Background jobs, caches, files, and analytics events preserve tenant scope.

## Authentication and API access

- [ ] Admin endpoints require authenticated, authorized access.
- [ ] Client API keys are revocable and stored as hashes/digests rather than plaintext.
- [ ] Keys are scoped to the minimum required permissions.
- [ ] Rotation does not require exposing previously stored secrets.
- [ ] Rate limits are enforced server-side per client/key.

## Browser/widget security

- [ ] Long-lived secret API keys never enter browser code.
- [ ] Embedded widgets use short-lived, origin-bound sessions or equivalent controls.
- [ ] CORS/origin checks use exact allowlists rather than substring matching or broad wildcards.
- [ ] Untrusted AI or product content is rendered safely without raw HTML injection.
- [ ] Widget configuration exposes only public identifiers and non-sensitive metadata.

## AI provider boundary

- [ ] Provider credentials stay server-side.
- [ ] Model/provider choice is controlled by trusted server configuration.
- [ ] Prompt/context construction separates trusted instructions from untrusted store/user content.
- [ ] Tool or commerce actions have explicit allowlists and authorization checks.
- [ ] Provider failures have a defined fallback or fail-closed behavior.

## Commerce integration

- [ ] WooCommerce/store credentials are held only on the server.
- [ ] Product/catalog access is read-only unless write access is explicitly required.
- [ ] Webhooks are authenticated and replay-resistant where applicable.
- [ ] Order/customer data is minimized and never included in logs unnecessarily.
- [ ] External API responses are validated before use.

## Data and privacy

- [ ] Logs redact API keys, tokens, customer identifiers, and sensitive payload fields.
- [ ] Chat/session retention is defined and tenant-scoped.
- [ ] Deletion/export requirements are understood before storing customer-linked data.
- [ ] Backups follow the same access controls as production data.
- [ ] Demo/showcase data is synthetic or sanitized.

## Reliability and deployment

- [ ] Liveness and readiness checks are distinct and truthful.
- [ ] Database migrations are versioned and repeatable.
- [ ] Dependencies are pinned/reproducible and scanned for known vulnerabilities.
- [ ] CI runs tests, lint/static checks, and secret scanning.
- [ ] Runtime configuration fails clearly when required secrets are missing.
- [ ] Rollback and key-rotation procedures are documented.

## Evidence before calling it production-ready

A project should not be labeled production-ready solely because the UI works. Keep evidence for:

1. automated tests covering authorization and tenant isolation;
2. dependency and secret scans;
3. a real deployment smoke test;
4. origin/CORS rejection tests;
5. API-key revocation/rotation tests;
6. rate-limit/quota tests;
7. backup/restore verification when persistent customer data is involved.

This checklist is intentionally implementation-agnostic so it can be reused when reviewing FastAPI, Node.js, WooCommerce, or similar AI-commerce SaaS architectures.
