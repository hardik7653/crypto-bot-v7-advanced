
import sqlite3, os, time, csv
DB = os.path.join(os.path.dirname(__file__),'..','trades.db')
DB = os.path.abspath(DB)
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS trades (ts INTEGER, symbol TEXT, signal TEXT, price REAL, sl REAL, tp REAL, size REAL)')
    conn.commit(); conn.close()
def log_trade(symbol, signal, price, sl, tp, size):
    init_db()
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute('INSERT INTO trades VALUES (?,?,?,?,?,?,?)', (int(time.time()), symbol, signal, price, sl, tp, size))
    conn.commit(); conn.close()
    csvf = os.path.join(os.path.dirname(__file__),'..','logs','trade_logs.csv')
    write_header = not os.path.exists(csvf)
    with open(csvf,'a', newline='') as f:
        w = csv.writer(f)
        if write_header: w.writerow(['ts','symbol','signal','price','sl','tp','size'])
        w.writerow([int(time.time()), symbol, signal, price, sl, tp, size])
