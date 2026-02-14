#!/usr/bin/env python3
"""Community template for V3.1 shadow forecasting.

Features:
- V1/V2/V3/V3.1 comparison scaffold
- POA approximation hook
- weather + nowcast factor hooks
- segment-wise learning tables (shade/seg)

Fill `pv-mapping.json` and adapt formulas for your installation.
"""
import datetime as dt, json, os, sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
MAPPING = BASE / 'pv-mapping.json'
WORKSPACE = Path(os.getenv('OPENCLAW_WORKSPACE', BASE.parent.parent))
DB_PATH = WORKSPACE / 'memory/pv-history.sqlite'


def load_mapping():
    if not MAPPING.exists():
        raise SystemExit(f'Missing {MAPPING}. Copy pv-mapping.example.json to pv-mapping.json and fill values.')
    return json.loads(MAPPING.read_text(encoding='utf-8'))


def init_tables(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS pv_shadow_eval_v31 (
      ts TEXT NOT NULL,d TEXT NOT NULL,minute INTEGER NOT NULL,field TEXT NOT NULL,
      actual_day_kwh REAL NOT NULL,v1_exp_now REAL NOT NULL,v2_exp_now REAL NOT NULL,v3_exp_now REAL NOT NULL,v31_exp_now REAL NOT NULL,
      v1_exp_day REAL NOT NULL,v2_exp_day REAL NOT NULL,v3_exp_day REAL NOT NULL,v31_exp_day REAL NOT NULL,
      weather_factor REAL NOT NULL,solar_factor REAL NOT NULL,month_factor REAL NOT NULL,
      brightness_factor REAL NOT NULL,rain_factor REAL NOT NULL,sunshine_factor REAL NOT NULL,
      cloud_factor REAL NOT NULL,radiation_factor REAL NOT NULL,temp_factor REAL NOT NULL,wind_factor REAL NOT NULL,
      nowcast_factor REAL NOT NULL,poa_factor REAL NOT NULL,shade_factor REAL NOT NULL,seg_factor REAL NOT NULL,
      PRIMARY KEY (ts, field))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS pv_shadow_profile (
      field TEXT NOT NULL, minute_bucket INTEGER NOT NULL, shade_factor REAL NOT NULL,
      updated_ts TEXT NOT NULL, samples INTEGER NOT NULL DEFAULT 0,
      PRIMARY KEY(field, minute_bucket))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS pv_segment_profile (
      field TEXT NOT NULL, minute_bucket INTEGER NOT NULL, seg_factor REAL NOT NULL,
      updated_ts TEXT NOT NULL, samples INTEGER NOT NULL DEFAULT 0,
      PRIMARY KEY(field, minute_bucket))''')
    conn.commit()


def main():
    m = load_mapping()
    fields = list(m['segments'].keys())
    now = dt.datetime.now().astimezone()
    ts = now.isoformat(timespec='seconds')
    d = now.date().isoformat()
    minute = now.hour*60 + now.minute

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_tables(conn)

    # This template intentionally stores neutral placeholder values.
    # Replace with your site-specific V3.1 implementation.
    for f in fields:
        conn.execute('''INSERT OR REPLACE INTO pv_shadow_eval_v31
          (ts,d,minute,field,actual_day_kwh,v1_exp_now,v2_exp_now,v3_exp_now,v31_exp_now,v1_exp_day,v2_exp_day,v3_exp_day,v31_exp_day,
           weather_factor,solar_factor,month_factor,brightness_factor,rain_factor,sunshine_factor,cloud_factor,radiation_factor,
           temp_factor,wind_factor,nowcast_factor,poa_factor,shade_factor,seg_factor)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
          (ts,d,minute,f,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1))

    conn.commit()
    print(f'V3.1 template shadow logged {ts} fields={len(fields)}')


if __name__ == '__main__':
    main()
