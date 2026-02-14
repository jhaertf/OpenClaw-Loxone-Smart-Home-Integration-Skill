#!/usr/bin/env python3
import base64, datetime as dt, json, os, re, sqlite3, ssl, statistics, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
MAPPING = BASE / 'pv-mapping.json'
WORKSPACE = Path(os.getenv('OPENCLAW_WORKSPACE', BASE.parent.parent))
DB_PATH = WORKSPACE / 'memory/pv-history.sqlite'
CRED_DIR = Path(os.getenv('OPENCLAW_CREDENTIALS_DIR', '/home/openclaw/.openclaw/credentials'))
HOST = (CRED_DIR / 'loxone-host').read_text().strip().replace('https://','').replace('http://','')
USER = (CRED_DIR / 'loxone-user').read_text().strip()
PASS = (CRED_DIR / 'loxone-password').read_text().strip()

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


def med(vals, d=0.0):
    return statistics.median(vals) if vals else d


def bar(ratio: float, w: int = 14):
    ratio = max(0.0, min(1.0, ratio))
    n = int(round(ratio*w))
    return '█'*n + '·'*(w-n)


def expected_from_db(conn, fields, now_min, today):
    cur = conn.cursor()
    exp_day, exp_now, samples = {}, {}, {}
    for f in fields:
        day = cur.execute('''SELECT final FROM (
          SELECT d, MAX(day_kwh) final FROM pv_snapshots WHERE field=? AND d<? GROUP BY d
        ) WHERE final>=0.3 ORDER BY d DESC LIMIT 60''', (f, today)).fetchall()
        now = cur.execute('''SELECT upto FROM (
          SELECT d, MAX(day_kwh) upto FROM pv_snapshots WHERE field=? AND d<? AND minute<=? GROUP BY d
        ) ORDER BY d DESC LIMIT 60''', (f, today, now_min)).fetchall()
        exp_day[f] = med([r[0] for r in day], 0.0)
        exp_now[f] = med([r[0] for r in now], 0.0)
        samples[f] = len(day)
    if min(samples.values()) < 7:
        return None
    return exp_day, exp_now


def main():
    m = load_mapping()
    seg = m['segments']
    fields = list(seg.keys())
    ids = m['ids']

    now = dt.datetime.now().astimezone()
    today = now.date().isoformat()
    now_min = now.hour*60 + now.minute

    p_total = fetch_val(ids['total_power'])
    soc = fetch_val(ids['soc'])
    grid_now = fetch_val(f"{ids['grid']}/actual")
    grid_imp = fetch_val(f"{ids['grid']}/totalDay")
    grid_exp = fetch_val(f"{ids['grid']}/totalNegDay")

    actual = {f: fetch_val(f"{seg[f]['uuid']}/totalDay") for f in fields}

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    out = expected_from_db(conn, fields, now_min, today)
    if out is None:
        exp_day = {f: 0.0 for f in fields}
        exp_now = {f: 0.0 for f in fields}
        source = 'insufficient-history'
    else:
        exp_day, exp_now = out
        source = 'db'

    t_act = sum(actual.values()); t_day = sum(exp_day.values()); t_now = sum(exp_now.values())

    print('☀️ PV-Kompaktreport')
    print(f"Zeit: {now.strftime('%d.%m.%Y %H:%M')}")
    print('\nSegmentvergleich (IST vs SOLL jetzt | SOLL Tag)')
    for f in fields:
        ist, sn, sd = actual[f], exp_now[f], exp_day[f]
        r = ist/sn if sn>0 else 1.0
        status = 'nachts ok' if (sn < 0.05 and ist < 0.05) else ('ok' if r>=0.75 else ('niedrig' if r>=0.45 else 'kritisch'))
        print(f'- {f:14} {ist:5.2f} | {sn:5.2f} | {sd:5.2f} kWh  [{bar(r)}] {status}')

    print('\nGesamt')
    print(f'- Heute IST:      {t_act:.2f} kWh')
    print(f'- SOLL bis jetzt: {t_now:.2f} kWh   [{bar(t_act/t_now if t_now>0 else 1.0)}]')
    print(f'- SOLL Tag:       {t_day:.2f} kWh')
    print(f'- PV-Leistung:    {p_total:.2f} kW')
    print(f'- Netz jetzt:     {grid_now:.2f} kW')
    print(f'- Netz Tag B/E:   {grid_imp:.2f} / {grid_exp:.2f} kWh')
    print(f'- Akku SOC:       {soc:.0f}%')
    print(f'- Erwartungsquelle: {source}')


if __name__ == '__main__':
    main()
