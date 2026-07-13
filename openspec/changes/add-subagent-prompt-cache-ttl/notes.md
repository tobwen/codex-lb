# Subagent Prompt-Cache TTL — Empirical Findings

## Session Origin

OpenCode sends `x-parent-session-id` on requests originating from subagents. Tool calls are sent as ordinary conversation requests and are not used as a lifecycle signal.

## Fork Behaviour

When multiple requests share one OpenCode session header but carry no explicit turn-state or `previous_response_id`, codex-lb may create an **unanchored parallel fork**. This feature does not classify those requests as subagents.

## Timing Profile (measured on 2026-07-13)

| Stage | Duration |
|---|---|
| Actual upstream work (single read) | <60s |
| Bridge session idle retention (fork) | 3600s (1h) |
| Stream lease stale reclaim (safety net) | ~7260s (2h) |

Tool-call concurrency is outside this change because tool calls are represented as ordinary conversation requests.

## Capacity Impact

Subagent bridge sessions are closed at response-stream completion. An optional positive subagent mapping TTL affects only sticky mapping retention, not stream-lease lifetime.

## Visibility Gap

Active bridge-session visibility is outside this change.

## Implementation Constraints

During implementation, every modified or new file MUST be checked against:

- **coding-guardrails**: surgical changes (only request-relevant lines), no unrelated churn, match local style, no fake comments/TODOs, ground truth over guessing.
- **ponytail** (full): the ladder (YAGNI → stdlib → native → already-installed dep → one line → minimum code). No unrequested abstractions, no boilerplate, no scaffolding. Use the smallest working diff. If a `ponytail:` comment is needed for a deliberate shortcut, add it with ceiling and upgrade path.
- **anti-slop** (generation mode): avoid generic names, placeholder logic, invented APIs, filler comments. Comments explain WHY, not WHAT. No fake-human notes, no apologetic comments.

Foreign code (existing files with established patterns) MUST follow the majority style of the surrounding file rather than introducing a different convention. Consistency in-context beats theoretical best practices. If an existing file uses a specific comment style, pattern, or naming convention, follow it.
