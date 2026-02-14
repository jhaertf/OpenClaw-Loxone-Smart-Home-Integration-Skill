# PV Script Output Examples (Sanitized)

Diese Beispiele zeigen typische, **anonymisierte** Ausgaben der PV-Skripte für die Community.

## 1) `pv-status-report.sh` (kompakter Status)

```text
PV-Report

Heute (Anteil je Feld)
- Feld A          8.42 kWh  [#######---] 68.4%
- Feld B          1.76 kWh  [#---------] 14.3%
- Feld C          1.12 kWh  [#---------]  9.1%
- Feld D          1.00 kWh  [#---------]  8.1%

Gesamt
- Leistung jetzt: 4.32 kW
- Heute gesamt: 12.30 kWh
- Ertrag/kWp:   0.84 kWh/kWp

Akku
- SOC:          71%
- Laden heute:   4.10 kWh
- Entladen:      2.90 kWh

Netz
- Bezug heute:       1.20 kWh
- Einspeisung heute: 5.60 kWh
```

## 2) `pv-anomaly-monitor.py` – unauffällig

```text
NO_REPLY
```

## 3) `pv-anomaly-monitor.py` – Anomalie erkannt

```text
⚠️ PV-Anomalie erkannt (Wetter-korrigierter Plausibilitätscheck)
Heute gesamt: 6.20 kWh
Wetter: Wolken 82% | Strahlung 7.4 MJ/m² | Schnee 0.0 cm
- Feld C: IST 0.12 kWh vs. SOLL ~1.45 kWh (kritisch)
Bitte OpenDTU-Datenfluss/Wechselrichter/String prüfen.
```

## 4) `pv-compact-overview.py` – Segmentvergleich

```text
☀️ PV-Kompaktreport
Zeit: 14.02.2026 12:30

Segmentvergleich (IST vs SOLL jetzt | SOLL Tag)
- Feld A         6.80 | 7.10 | 11.90 kWh  [████████████··] ok
- Feld B         1.30 | 1.55 |  2.40 kWh  [███████████···] niedrig
- Feld C         0.75 | 1.10 |  1.80 kWh  [█████████·····] niedrig

Gesamt
- Heute IST:      8.85 kWh
- SOLL bis jetzt: 9.75 kWh   [███████████···]
- SOLL Tag:      16.10 kWh
- Erwartungsquelle: DB

Anomalie-Check: unauffällig ✅
```

## 5) `pv-shadow-eval-report.py` – Modellvergleich

```text
📈 PV Shadow Accuracy Report (V1 vs V2 vs V3 vs V3.1, letzte 7 Tage)
Zeitraum: 2026-02-07 bis 2026-02-14 (exkl. heute)

- Feld A         V1 1.12 | V2 0.96 (+14.3%) | V3 0.88 (+21.4%) | V3.1 0.81 (+27.7%)
- Feld B         V1 0.54 | V2 0.52 ( +3.7%) | V3 0.48 (+11.1%) | V3.1 0.42 (+22.2%)

Gesamt
- V1 MAE: 0.86
- V2 MAE: 0.75 (+12.8% ggü. V1)
- V3 MAE: 0.68 (+20.9% ggü. V1)
- V3.1 MAE: 0.61 (+29.1% ggü. V1)
- Empfehlung: V3.1 bereit: Live-Test starten
```

---

## Hinweise für Community-Repos

- Keine echten UUIDs, Hosts, API-User oder internen Namen committen.
- Beispieloutputs immer anonymisieren (Feld A/B/C statt realer Segmentnamen).
- Für reale Installationen lokale `config.json` + `actions.json` nutzen (in `.gitignore`).
