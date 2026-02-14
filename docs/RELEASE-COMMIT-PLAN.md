# Release Commit Plan (ohne Push)

Vorschlag für eine saubere Commit-Serie, damit Review leichter ist.

## Commit 1 — Security/Config hardening

**Message**
`chore(security): switch loxone user to userFile + tighten gitignore`

**Files**
- `.gitignore`
- `skills/loxone/config.example.json`
- `skills/loxone/loxone-api.sh`
- `README.md` (Config/Credentials Abschnitt)

---

## Commit 2 — Community PV templates

**Message**
`feat(pv): add sanitized community templates for history/report/shadow/eval`

**Files**
- `skills/loxone/pv-mapping.example.json`
- `skills/loxone/pv-history-db.py`
- `skills/loxone/pv-compact-overview.py`
- `skills/loxone/pv-shadow-v3_1.py`
- `skills/loxone/pv-shadow-eval-report.py`

---

## Commit 3 — Docs & onboarding

**Message**
`docs(pv): add community setup and sanitized output examples`

**Files**
- `docs/COMMUNITY-SETUP.md`
- `docs/pv-script-output-examples.md`
- `README.md` (What's New + Feature-Update + Links)

---

## Commit 4 — Dev utility

**Message**
`chore(tooling): add bootstrap script for local community setup`

**Files**
- `scripts/bootstrap-community-skill.sh`

---

## Optional local review commands

```bash
cd OpenClaw-Loxone-Smart-Home-Integration-Skill
bash scripts/sanitize-check.sh .
git status --short
git diff --stat
```

## Optional staging commands

```bash
# Commit 1
git add .gitignore skills/loxone/config.example.json skills/loxone/loxone-api.sh README.md
git commit -m "chore(security): switch loxone user to userFile + tighten gitignore"

# Commit 2
git add skills/loxone/pv-mapping.example.json skills/loxone/pv-history-db.py skills/loxone/pv-compact-overview.py skills/loxone/pv-shadow-v3_1.py skills/loxone/pv-shadow-eval-report.py
git commit -m "feat(pv): add sanitized community templates for history/report/shadow/eval"

# Commit 3
git add docs/COMMUNITY-SETUP.md docs/pv-script-output-examples.md README.md
git commit -m "docs(pv): add community setup and sanitized output examples"

# Commit 4
git add scripts/bootstrap-community-skill.sh
git commit -m "chore(tooling): add bootstrap script for local community setup"
```
