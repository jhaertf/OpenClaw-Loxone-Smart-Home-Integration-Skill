#!/usr/bin/env python3
import datetime as dt, os, sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
WORKSPACE = Path(os.getenv('OPENCLAW_WORKSPACE', BASE.parent.parent))
DB_PATH = WORKSPACE / 'memory/pv-history.sqlite'


def mae(pairs):
    return sum(abs(a-b) for a,b in pairs)/len(pairs) if pairs else 0.0

def imp(base, cand):
    return ((base-cand)/base*100.0) if base>0 else 0.0


def main():
    if not DB_PATH.exists():
        print('PV Shadow Accuracy Report\nStatus: keine DB vorhanden.'); return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    today = dt.datetime.now().astimezone().date().isoformat()
    since = (dt.datetime.now().astimezone().date()-dt.timedelta(days=7)).isoformat()

    rows = cur.execute('''SELECT actual_day_kwh,v1_exp_now,v2_exp_now,v3_exp_now,v31_exp_now
                          FROM pv_shadow_eval_v31 WHERE d>=? AND d<?''', (since, today)).fetchall()
    if not rows:
        print('PV Shadow Accuracy Report (7 Tage)\nStatus: noch keine V3.1-Shadow-Daten vorhanden.'); return

    v1 = mae([(a,b) for a,b,_,_,_ in rows if a>=0.3])
    v2 = mae([(a,b) for a,_,b,_,_ in rows if a>=0.3])
    v3 = mae([(a,b) for a,_,_,b,_ in rows if a>=0.3])
    v31= mae([(a,b) for a,_,_,_,b in rows if a>=0.3])

    print('📈 PV Shadow Accuracy Report (V1 vs V2 vs V3 vs V3.1)')
    print(f'- V1 MAE:   {v1:.3f}')
    print(f'- V2 MAE:   {v2:.3f} ({imp(v1,v2):+.1f}% ggü. V1)')
    print(f'- V3 MAE:   {v3:.3f} ({imp(v1,v3):+.1f}% ggü. V1)')
    print(f'- V3.1 MAE: {v31:.3f} ({imp(v1,v31):+.1f}% ggü. V1)')

    winner = min([('V1',v1),('V2',v2),('V3',v3),('V3.1',v31)], key=lambda x:x[1])[0]
    print(f'- Bestes Modell: {winner}')


if __name__ == '__main__':
    main()
