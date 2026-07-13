## ADDED Requirements

### Requirement: Subagent prompt-cache affinity is optional

The system SHALL identify subagent requests by `x-parent-session-id`. The dashboard setting `http_responses_session_bridge_fork_idle_ttl_seconds` SHALL use `NULL` as the default No Cache mode. When set to a positive number, it SHALL retain the subagent's PROMPT_CACHE mapping for that many seconds. The HTTP bridge session itself SHALL close when the subagent response stream ends regardless of the setting.

#### Scenario: Subagent uses No Cache by default

- **GIVEN** an incoming request carries `x-parent-session-id`
- **AND** the subagent prompt-cache TTL setting is `NULL`
- **WHEN** the HTTP bridge selects an account
- **THEN** it MUST NOT read or write a PROMPT_CACHE sticky mapping for the subagent
- **AND** the bridge session MUST close when the response stream ends

#### Scenario: Subagent can retain a temporary mapping

- **GIVEN** an incoming request carries `x-parent-session-id`
- **AND** the subagent prompt-cache TTL setting is a positive number
- **WHEN** the HTTP bridge selects an account
- **THEN** the subagent's PROMPT_CACHE mapping MAY be read or written
- **AND** its mapping expires according to the configured subagent TTL
- **AND** the bridge session MUST close when the response stream ends

#### Scenario: Canonical session retains standard PROMPT_CACHE behavior

- **GIVEN** an incoming request does not carry `x-parent-session-id`
- **WHEN** the session is created
- **THEN** the session uses the standard affinity-based idle TTL (PROMPT_CACHE/CODEX_SESSION/base)
- **AND** the subagent setting does not affect the canonical session

### Requirement: Completed subagent sessions do not retain sticky mappings

The system MUST delete any stale PROMPT_CACHE sticky mapping for a No Cache subagent when its HTTP bridge response stream ends. The system MUST NOT delete a retained mapping when a positive subagent TTL is configured, and MUST NOT delete the sticky mapping for the canonical parent session.

#### Scenario: Completed subagent releases its sticky mapping

- **GIVEN** an HTTP bridge session was marked as a subagent session from `x-parent-session-id`
- **WHEN** its response stream ends
- **THEN** the session's stream lease is released
- **AND** its No Cache PROMPT_CACHE sticky mapping is deleted if one exists
- **AND** the parent session's sticky mapping remains available
