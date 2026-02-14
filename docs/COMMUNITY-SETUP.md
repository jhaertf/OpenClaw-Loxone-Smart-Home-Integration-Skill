# Community Setup Guide (PV + Loxone)

## 1) Dateien kopieren

```bash
cp skills/loxone/config.example.json skills/loxone/config.json
cp skills/loxone/actions.example.json skills/loxone/actions.json
cp skills/loxone/pv-mapping.example.json skills/loxone/pv-mapping.json
```

## 2) Credentials anlegen (lokal, nicht committen)

```bash
mkdir -p /home/openclaw/.openclaw/credentials
printf 'https://YOUR-LOXONE-HOST' > /home/openclaw/.openclaw/credentials/loxone-host
printf 'YOUR-LOXONE-USER' > /home/openclaw/.openclaw/credentials/loxone-user
printf 'YOUR-LOXONE-PASSWORD' > /home/openclaw/.openclaw/credentials/loxone-password
chmod 600 /home/openclaw/.openclaw/credentials/loxone-*
```

## 3) Mapping befüllen

In `skills/loxone/pv-mapping.json`:
- Segment-UUIDs
- Gesamt-/Grid-/SOC-IDs
- Wetterstation-IDs
- Geometrie je Segment (`tilt_deg`, `azimuth_from_south_deg`, `weight`)

## 4) Tests

```bash
python3 skills/loxone/pv-history-db.py init
python3 skills/loxone/pv-history-db.py ingest
python3 skills/loxone/pv-compact-overview.py
python3 skills/loxone/pv-shadow-v3_1.py
python3 skills/loxone/pv-shadow-eval-report.py
```

## 5) Leak-Check vor Commit

```bash
bash scripts/sanitize-check.sh .
```
