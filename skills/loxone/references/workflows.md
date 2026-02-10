# Workflows (Loxone Skill)

## PV-Anomaly-Check
1. `python3 {baseDir}/pv-anomaly-monitor.py` ausführen.
2. Output prüfen:
   - `NO_REPLY` => keine Anomalie.
   - Text => Anomalie priorisiert melden.

## PV-Status
1. `bash {baseDir}/pv-status-report.sh` ausführen.
2. Kurzfazit mit Ertrag, Leistung, Akku, Netz geben.

## Action-Ausführung
1. Action-ID in `actions.example.json` nachschlagen bzw. mappen.
2. `bash {baseDir}/loxone-api.sh run_action <action_id>` ausführen.
3. Ergebnis/Fehler klar zurückmelden.
