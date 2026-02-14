#!/usr/bin/env python3
import argparse, base64, datetime as dt, json, re, sqlite3, ssl, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
MAPPING = BASE / 'pv-mapping.json'
DB_PATH = Path('/home/openclaw/.openclaw/workspace/memory/pv-history.sqlite')
HOST = Path('/home/openclaw/.openclaw/credentials/loxone-host').read_text().strip().replace('https://','').replace('http://','')
USER = Path('/home/openclaw/.openclaw/credentials/loxone-user').read_text().strip()
PASS = Path('/home/openclaw/.openclaw/credentials/loxone-password').read_text().strip()

ctx = ssl._create_unverified_context()
auth = 'Basic ' + base64.b64encode(f'{USER}:{PASS}'.encode()).decode()


def load_mapping():
    if not MAPPING.exists():
        raise SystemExit(f'Missing {MAPPING}. Copy pv-mapping.example.json to pv-mapping.json and fill values.')
    return json.loads(MAPPING.read_text(encoding='utf-8'))


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={'Authorization': auth})
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        return r.read().decode('utf-8', 'ignore')


def fetch_val(path: str) -> float:
    raw = http_get(f'https://{HOST}/jdev/sps/io/{path}')
    m = re.search(r'"value"\s*:\s*"?([-+]?\d*\.?\d+)"?', raw)
    return float(m.group(1)) if m else 0.0


def init_db(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS pv_snapshots (
      ts TEXT NOT NULL, d TEXT NOT NULL, minute INTEGER NOT NULL, month INTEGER NOT NULL,
      field TEXT NOT NULL, day_kwh REAL NOT NULL, power_kw REAL NOT NULL,
      total_power_kw REAL NOT NULL, soc REAL NOT NULL, grid_now_kw REAL NOT NULL,
      PRIMARY KEY (ts, field))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS env_snapshots (
      ts TEXT PRIMARY KEY, d TEXT NOT NULL, minute INTEGER NOT NULL,
      temp_north_c REAL, temp_station_c REAL, brightness_lux REAL,
      wind_kmh REAL, rain_active REAL, sunshine_active REAL)''')
    conn.commit()


def ingest(conn, m):
    now = dt.datetime.now().astimezone()
    ts = now.isoformat(timespec='seconds')
    d = now.date().isoformat()
    minute = now.hour * 60 + now.minute
    month = now.month

    ids = m['ids']
    total_power = fetch_val(ids['total_power'])
    soc = fetch_val(ids['soc'])
    grid_now = fetch_val(f"{ids['grid']}/actual")

    rows = []
    for name, cfg in m['segments'].items():
        uid = cfg['uuid']
        day_kwh = fetch_val(f'{uid}/totalDay')
        power_kw = fetch_val(f'{uid}/actual')
        rows.append((ts, d, minute, month, name, day_kwh, power_kw, total_power, soc, grid_now))

    env_cfg = m.get('weather_ids', {})
    env = {}
    for k, uid in env_cfg.items():
        try: env[k] = fetch_val(uid)
        except Exception: env[k] = 0.0

    conn.executemany('''INSERT OR REPLACE INTO pv_snapshots
      (ts,d,minute,month,field,day_kwh,power_kw,total_power_kw,soc,grid_now_kw)
      VALUES (?,?,?,?,?,?,?,?,?,?)''', rows)
    conn.execute('''INSERT OR REPLACE INTO env_snapshots
      (ts,d,minute,temp_north_c,temp_station_c,brightness_lux,wind_kmh,rain_active,sunshine_active)
      VALUES (?,?,?,?,?,?,?,?,?)''', (ts,d,minute,env.get('temp_north_c',0),env.get('temp_station_c',0),env.get('brightness_lux',0),env.get('wind_kmh',0),env.get('rain_active',0),env.get('sunshine_active',0)))
    conn.commit()
    print(f'OK ingest {ts} rows={len(rows)} env=1')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['init','ingest','stats'])
    args = ap.parse_args()
    m = load_mapping()

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    if args.cmd == 'init':
        print('OK init')
    elif args.cmd == 'ingest':
        ingest(conn, m)
    else:
        cur = conn.cursor()
        print('PV DB stats')
        print(f"- rows: {cur.execute('SELECT COUNT(*) FROM pv_snapshots').fetchone()[0]}")
        print(f"- env_rows: {cur.execute('SELECT COUNT(*) FROM env_snapshots').fetchone()[0]}")


if __name__ == '__main__':
    main()
