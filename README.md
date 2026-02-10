# OpenClaw Loxone Smart Home Integration Skill

Sanitized, public-safe Loxone AgentSkill templates for OpenClaw.

## Included
- `skills/loxone/SKILL.md`
- sanitized shell/python templates
- `*.example` config and mapping files
- references for workflows and data-sensitivity

## Setup
1. Copy `skills/loxone` into your OpenClaw workspace.
2. Create runtime files from examples:
   - `config.example.json` → `config.json`
   - `actions.example.json` → `actions.json`
   - `pv-day-overrides.example.json` → `pv-day-overrides.json`
   - `loxone-controls-inventory.example.csv` → `loxone-controls-inventory.csv`
3. Replace all placeholders (`REPLACE_WITH_*`).
4. Store credentials outside git (e.g. `~/.openclaw/credentials`).

## Security
- No real UUIDs, hosts, usernames, passwords, or local IPs should be committed.
- Run a sanitizer check before pushing.
