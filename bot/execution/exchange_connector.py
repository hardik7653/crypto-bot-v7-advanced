
import time, random, pandas as pd
class MockExchange:
    def fetch_ohlcv(self, symbol, timeframe='5m', limit=200):
        now = int(time.time()*1000)
        rows = []
        base = 60000 if 'BTC' in symbol else 2000 if 'ETH' in symbol else 100
        for i in range(limit):
            t = now - (limit-i)*300000
            o = base + random.uniform(-base*0.01, base*0.01)
            h = o + abs(random.uniform(0, base*0.003))
            l = o - abs(random.uniform(0, base*0.003))
            c = o + random.uniform(-base*0.002, base*0.002)
            v = random.uniform(10,1000)
            rows.append([t,o,h,l,c,v])
        df = pd.DataFrame(rows, columns=['timestamp','open','high','low','close','volume'])
        df['timestamp']=pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
