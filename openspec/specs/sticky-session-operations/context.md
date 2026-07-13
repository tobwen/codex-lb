# Sticky Session Operations Context

## Purpose and Scope

This capability covers operational control of sticky-session mappings after prompt-cache affinity was made bounded. It distinguishes durable backend/session routing from bounded prompt-cache affinity and defines the admin controls around those mappings.

See `openspec/specs/sticky-session-operations/spec.md` for normative requirements.

## Decisions

- Sticky-session rows store an explicit `kind` so prompt-cache cleanup can target only bounded mappings.
- Dashboard prompt-cache TTL is persisted in settings so operators can adjust it without restart.
- Subagent requests are identified by `x-parent-session-id`. Their prompt-cache affinity is `NULL` by default (No Cache) and may be enabled with a positive, dashboard-configured TTL.
- Subagent bridge sessions close at response-stream completion independently of sticky-mapping retention, so retained mappings do not retain account stream leases.
- Background cleanup removes stale prompt-cache rows proactively, while manual delete and purge endpoints provide operator override.

## Constraints

- Historical sticky-session rows created before the `kind` column are backfilled conservatively to a durable kind to avoid accidental purge.
- Durable `codex_session` and `sticky_thread` mappings are never deleted by automatic cleanup.
- No-Cache subagent cleanup may remove a stale `prompt_cache` mapping, but it never removes the canonical parent mapping or a deliberately retained subagent mapping.

## Failure Modes

- Cleanup failures are logged and retried on the next interval; request handling continues.
- Manual purge and delete operations are dashboard-auth protected and return normal dashboard API errors on invalid input or missing keys.
