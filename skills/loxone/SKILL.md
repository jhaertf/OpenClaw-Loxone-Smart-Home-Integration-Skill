---
name: loxone
description: Steuere ein Loxone Smart Home über lokale Skripte und API-Aufrufe (Szenen/Actions, Status, PV-Report, PV-Anomaly-Check, geplante Routinen). Verwenden bei Anfragen wie „führe Loxone-Szene aus“, „zeige PV-Status“, „prüfe PV-Anomalie“, „starte Loxone-Action“ oder ähnlicher Hausautomations-Steuerung.
metadata: {"openclaw":{"emoji":"🏠","requires":{"bins":["bash","python3","curl","jq"]}}}
---

# Loxone

Führe Loxone-bezogene Aufgaben über die vorhandenen Skill-Skripte aus, mit Fokus auf Sicherheit, Nachvollziehbarkeit und robustes Fehlermanagement.

## Pfade
- Skill-Basis: `{baseDir}`
- Relevante Skripte unter `{baseDir}` (alle neutral/sanitized):
  - `loxone-api.sh`
  - `pv-status-report.sh`
  - `pv-anomaly-monitor.py`
  - `pv-anomaly-alert-after-sunset.sh`
  - `pv-sunset-report-monitor.sh`
  - `wake-weather-report.sh`
  - `wake-weather-tts.sh`

## Verhaltensregeln
1. Führe Standardabfragen (Status/Checks/Reports) direkt aus.
2. Frage vor potenziell riskanten Aktionen nach Bestätigung, falls die Intention nicht eindeutig ist.
3. Gib niemals Secrets oder interne Infrastrukturdetails aus (Passwörter, Hosts, interne IDs/UUIDs).
4. Behandle `NO_REPLY` als „kein Alarm/kein weiterer Nutzerhinweis nötig“.
5. Wenn Daten unvollständig sind, liefere das bestmögliche Ergebnis mit klar markierter Unsicherheit.

## Referenzen
- Workflows: `references/workflows.md`
- Datenquellen/Sensitivität: `references/data-sources.md`
