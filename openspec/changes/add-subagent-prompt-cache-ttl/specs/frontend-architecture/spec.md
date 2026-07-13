## ADDED Requirements

### Requirement: Subagent prompt-cache TTL appears in Routing Settings

The Routing Settings section SHALL include a persisted integer control for the subagent prompt-cache TTL, labelled "Subagent prompt-cache TTL", with a default of 120 seconds. The control follows the same persistence pattern as the existing prompt-cache affinity TTL field.

#### Scenario: Save subagent prompt-cache TTL

- **WHEN** a user enters a positive integer value for the subagent prompt-cache TTL in the Routing Settings section
- **AND** clicks save
- **THEN** the app calls `PUT /api/settings` with the updated TTL
- **AND** the settings response reflects the saved value
- **AND** subsequent requests carrying `x-openai-subagent` use the new TTL

#### Scenario: Invalid subagent TTL is rejected

- **WHEN** a user enters a non-positive or non-integer value for the subagent TTL
- **THEN** the control shows a validation error
- **AND** the save button is disabled until a valid value is entered

### Requirement: Active bridge sessions appear in Sticky Sessions section

The Settings page Sticky Sessions section SHALL include a table of active HTTP bridge sessions for the current account. Each row SHALL display the session id (truncated), model, created timestamp, last-seen timestamp, lease expiry status, and a "Close" action button. The list SHALL be fetched from `GET /api/http-bridge-sessions`. The "Close" button SHALL call `DELETE /api/http-bridge-sessions/{id}` and SHALL be disabled when the session has visible pending requests. Closing a session SHALL detach it from the in-memory registry, close its upstream WebSocket, release the account stream lease, and mark the durable row CLOSED.

#### Scenario: View active bridge sessions

- **WHEN** a user opens the Sticky Sessions section on the Settings page
- **THEN** the page fetches both sticky-session mappings (existing) and active bridge sessions (new)
- **AND** active bridge sessions are displayed as a separate table below the sticky-sessions table or as an integrated tab

#### Scenario: Close an idle bridge session

- **WHEN** a user clicks the "Close" button on an active bridge session row
- **AND** the session has no visible pending requests
- **THEN** the app calls `DELETE /api/http-bridge-sessions/{id}`
- **AND** the session is removed from the active sessions list
- **AND** the account stream lease count decreases

#### Scenario: Close button disabled for active session

- **WHEN** a session has visible pending requests (lease not expired)
- **THEN** the "Close" button for that row is disabled
- **AND** a tooltip explains "Session has active requests"

